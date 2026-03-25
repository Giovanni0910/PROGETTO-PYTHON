"""<<Control>>."""
import re

from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.AggiornaScacchiera import ControlScacchiera
from scacchi.control.ControlScacchi import ControlScacchi
from scacchi.entity.Alfiere import Alfiere


class MovimentoAlfiere:
    """Gestisce la logica di movimento dell'Alfiere negli scacchi.

    Questa classe fornisce metodi statici per validare e applicare le mosse
    dell'Alfiere, inclusi i controlli su ambiguità, catture, scacco e scacco matto.
    Metodi:
        alfiere_mossa_valida(turno, mossa, scacchiera)
            Valida una mossa di Alfiere secondo le regole degli scacchi.
        _strada_libera(x1, y1, x2, y2, scacchiera)
            Verifica che il percorso diagonale sia libero da ostacoli.
        aggiorna(turno, mossa, scacchiera)
            Applica la mossa dell'Alfiere e controlla scacco/scacco matto.
    """

    @staticmethod
    def alfiere_mossa_valida(turno, mossa, scacchiera):
        Alfiere_specifica = re.compile(r"""^A([a-h]|[1-8])x?[a-h][1-8][+#]?$""")
        colore_turno = "bianco" if turno == 0 else "nero"
        cattura = 'x' in mossa or ':' in mossa

        # Estrai destinazione (ultimi 2 caratteri)
        dest_str = (
            mossa.split('x')[-1]
            if 'x' in mossa
            else (mossa.split(':')[-1] if ':' in mossa else mossa)
        )
        dest_str = dest_str[-2:]

        try:
            x_dest, y_dest = ControlScacchiera.notazione_to_posizione(dest_str)
        except Exception:
            PartitaB.print_mossa_negata2()
            return None
        
        # Estrai specificatore (es. Abd5 o A3d5)
        specificatore = None
        if len(mossa) > 3:
            parte_specifica = (
                mossa.split('x')[0].split(':')[0]
                if cattura else mossa[:-2]
            )
            if parte_specifica.startswith('A'):
                parte_specifica = parte_specifica[1:]
                if parte_specifica:
                    specificatore = parte_specifica

        alfiere_valido = []

        # Trova tutti gli Alfieri che possono raggiungere la destinazione
        for x in range(8):
            for y in range(8):
                pezzo = scacchiera.get_pezzo(x, y)
                if isinstance(pezzo, Alfiere) and pezzo.colore == colore_turno:
                    dx = x_dest - x
                    dy = y_dest - y
                    
                    # MODIFICA CHIAVE: solo movimento diagonale
                    if (
                        abs(dx) == abs(dy)
                        and dx != 0
                        and MovimentoAlfiere._strada_libera(
                            x, y, x_dest, y_dest, scacchiera
                        )
                    ):
                        alfiere_valido.append((x, y))

        if len(alfiere_valido) == 0:
            PartitaB.print_mossa_negata2()
            return None
        
        pezzo_dest = scacchiera.get_pezzo(x_dest, y_dest)
        print(pezzo_dest)
        if pezzo_dest:
            if pezzo_dest.colore == colore_turno:
                PartitaB.print_casella_occupata()
                return None
            elif not cattura:
                PartitaB.print_cattura_non_specificata()
                return None
        elif cattura:
            PartitaB.print_cattura_negata2(dest_str)
            return None

        if len(alfiere_valido) == 1:
            if Alfiere_specifica.match(mossa):
                for x, y in alfiere_valido:
                        # Controlla se lo specificatore corrisponde alla colonna o riga
                        col = ControlScacchiera.posizione_to_notazione(x, y)[0]
                        riga = ControlScacchiera.posizione_to_notazione(x, y)[1]
                        
                        if specificatore in (col, riga):
                           # print("colonna o riga corretta")
                            return alfiere_valido[0]
                        else:
                            PartitaB.colonna_riga_inidcata_errata()
                            return None
            else:
                return alfiere_valido[0]
        else:
            # Ambiguità: verifica specificatore
            if specificatore:
                alfiere_filtrati = []
                for x, y in alfiere_valido:
                    col = ControlScacchiera.posizione_to_notazione(x, y)[0]
                    riga = ControlScacchiera.posizione_to_notazione(x, y)[1]
                    if specificatore in (col, riga):
                        alfiere_filtrati.append((x, y))

                if len(alfiere_filtrati) == 1:
                    return alfiere_filtrati[0]
                else:
                    PartitaB.print_ambiguità()
                    return None
            else:
                PartitaB.print_ambiguità()
                return None

    @staticmethod
    def _strada_libera(x1, y1, x2, y2, scacchiera):
        """Controlla che non ci siano ostacoli in diagonale."""
        dx = x2 - x1
        dy = y2 - y1
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        x, y = x1 + step_x, y1 + step_y
        while (x, y) != (x2, y2):
            if scacchiera.get_pezzo(x, y) is not None:
                return False
            x += step_x
            y += step_y
        return True

    @staticmethod
    def aggiorna(turno, mossa, scacchiera):
        # Verifica se la mossa dichiara scacco (+) o scacco matto (#)
        dichiara_scacco = '+' in mossa
        dichiara_scacco_matto = '#' in mossa
        mossa_senza_simboli = mossa.replace('+', '').replace('#', '')

        # Valida la mossa come mossa dell'Alfiere
        origine_dest = MovimentoAlfiere.alfiere_mossa_valida(
            turno, mossa_senza_simboli, scacchiera
        )
        if origine_dest is None:
            return False

        x_orig, y_orig= origine_dest
        try:
            x_dest, y_dest = ControlScacchiera.notazione_to_posizione(
                mossa_senza_simboli[-2:]
            )
        except Exception:
            return False
        
        # Salva il pezzo di destinazione per eventuale ripristino
        pezzo_originale_dest = scacchiera.get_pezzo(x_dest, y_dest)

        
        # Simula la mossa
        regina = scacchiera.get_pezzo(x_orig, y_orig)
        scacchiera.set_pezzo(x_dest, y_dest, regina)
        scacchiera.set_pezzo(x_orig, y_orig, None)

        # Controlla se il re del giocatore è sotto scacco dopo la mossa
        colore_giocatore = "bianco" if turno == 0 else "nero"
        if ControlScacchi.re_sotto_scacco(scacchiera, colore_giocatore):
            # Ripristina la scacchiera allo stato originale
            scacchiera.set_pezzo(x_orig, y_orig, regina)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_originale_dest)
            PartitaB.print_re_minacciato()
            return False

        # Controlla lo stato del re avversario
        colore_avversario = "nero" if turno == 0 else "bianco"
        re_sotto_scacco = ControlScacchi.re_sotto_scacco(
            scacchiera, colore_avversario
        )
        re_in_scacco_matto = (
            re_sotto_scacco
            and ControlScacchi.verifica_scacco_scacco_matto(
                scacchiera, colore_avversario
            )
        )

        # Valida le dichiarazioni di scacco/scacco matto
        if re_in_scacco_matto:
            if not dichiara_scacco_matto:
                # Scacco matto non dichiarato
                scacchiera.set_pezzo(x_orig, y_orig, regina)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_originale_dest)
                PartitaB.print_scacco_matto_non_indicato()
                return False
        elif re_sotto_scacco:
            if not dichiara_scacco:
                # Scacco non dichiarato
                scacchiera.set_pezzo(x_orig, y_orig, regina)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_originale_dest)
                PartitaB.print_scacco_non_indicato()
                return False
        elif dichiara_scacco_matto:
            # Dichiara scacco matto ma non è vero
            scacchiera.set_pezzo(x_orig, y_orig, regina)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_originale_dest)
            PartitaB.print_scacco_matto_non_valido()
            return False
        elif dichiara_scacco:
            # Dichiara scacco ma non è vero
            scacchiera.set_pezzo(x_orig, y_orig, regina)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_originale_dest)
            PartitaB.print_scacco_non_valido()
            return False
        
        #conferma la mossa 
        return True