"""<<Control>>."""
import re

from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.AggiornaScacchiera import ControlScacchiera
from scacchi.control.ControlScacchi import ControlScacchi
from scacchi.entity.Regina import Regina


class MovimentoRegina:
    """Gestisce la logica delle mosse della regina negli scacchi.

    Questa classe fornisce metodi statici per validare e applicare le mosse della
    regina, inclusa la gestione delle ambiguità, delle catture e delle dichiarazioni
    di scacco.

    Metodi:
        regina_mossa_valida(turno, mossa, scacchiera): Valida una mossa di regina.
        _movimento_valido(dx, dy): Verifica se il movimento è valido per una regina.
        _strada_libera(x1, y1, x2, y2, scacchiera): Controlla se il percorso è libero.
        aggiorna(turno, mossa, scacchiera): Applica la mossa della regina e aggiorna
            la scacchiera.
    """

    @staticmethod
    def regina_mossa_valida(turno, mossa, scacchiera):
        Regina_specifica = re.compile(r"""^D([a-h]|[1-8])x?[a-h][1-8][+#]?$""")
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

        pezzo_dest = scacchiera.get_pezzo(x_dest, y_dest)
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

        # Estrai specificatore (es. Dbd5 o D3d5)
        specificatore = None
        if len(mossa) > 3:
            parte_specifica = (
                mossa.split('x')[0].split(':')[0]
                if cattura else mossa[:-2]
            )
            if parte_specifica.startswith('D'):
                parte_specifica = parte_specifica[1:]
                if parte_specifica:
                    specificatore = parte_specifica

        regine_valide = []

        # Trova tutte le regine che possono raggiungere la destinazione
        for x in range(8):
            for y in range(8):
                pezzo = scacchiera.get_pezzo(x, y)
                if isinstance(pezzo, Regina) and pezzo.colore == colore_turno:
                    dx = x_dest - x
                    dy = y_dest - y

                    if (
                        MovimentoRegina._movimento_valido(dx, dy)
                        and MovimentoRegina._strada_libera(
                            x, y, x_dest, y_dest, scacchiera
                        )
                    ):
                        regine_valide.append((x, y))

        if len(regine_valide) == 0:
            PartitaB.print_mossa_negata2()
            return None
        elif len(regine_valide) == 1:
            if Regina_specifica.match(mossa):
                for x, y in regine_valide:
                        # Controlla se lo specificatore corrisponde alla colonna o riga
                        col = ControlScacchiera.posizione_to_notazione(x, y)[0]
                        riga = ControlScacchiera.posizione_to_notazione(x, y)[1]
                        
                        if specificatore in (col, riga):
                            return regine_valide[0]
                        else:
                            PartitaB.colonna_riga_inidcata_errata()
                            return None
            else:
                return regine_valide[0]
        else:
            # Ambiguità: verifica specificatore
            if specificatore:
                regine_filtrate = []
                for x, y in regine_valide:
                    col = ControlScacchiera.posizione_to_notazione(x, y)[0]
                    riga = ControlScacchiera.posizione_to_notazione(x, y)[1]
                    if specificatore in (col, riga):
                        regine_filtrate.append((x, y))

                if len(regine_filtrate) == 1:
                    return regine_filtrate[0]
                else:
                    PartitaB.print_mossa_regina_ambiguità_non_valida()
                    return None
            else:
                PartitaB.print_ambiguità()
            return None

    @staticmethod
    def _movimento_valido(dx, dy):
        return (dx == 0 or dy == 0) or (abs(dx) == abs(dy))

    @staticmethod
    def _strada_libera(x1, y1, x2, y2, scacchiera):
        dx = x2 - x1
        dy = y2 - y1
        step_x = 0 if dx == 0 else dx // abs(dx)
        step_y = 0 if dy == 0 else dy // abs(dy)

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
        mossa_pulita = mossa.replace('+', '').replace('#', '')
        
        # Valida la mossa della regina
        origine = MovimentoRegina.regina_mossa_valida(
            turno, mossa_pulita, scacchiera
        )
        if origine is None:
            return False

        x_orig, y_orig = origine
        
        # Ottieni le coordinate di destinazione
        try:
            x_dest, y_dest = ControlScacchiera.notazione_to_posizione(
                mossa_pulita[-2:]
            )
        except Exception:
            return False

        # Salva il pezzo di destinazione originale per eventuale ripristino
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
