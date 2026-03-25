import re

from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.AggiornaScacchiera import ControlScacchiera
from scacchi.control.ControlScacchi import ControlScacchi
from scacchi.entity.Torre import Torre


class MovimentoTorre:
    """Gestisce la logica delle mosse della torre negli scacchi.

    Questa classe fornisce metodi statici per validare e applicare le mosse della torre,
    inclusa la gestione di catture, ambiguità, controllo del percorso libero e verifica
    di scacco e scacco matto.
    Metodi:
        torre_mossa_valida(turno, mossa, scacchiera):
            Verifica se una mossa della torre è valida, considerando catture, ambiguità
            e regole di scacchi.
        _percorso_libero(x1, y1, x2, y2, scacchiera):
            Controlla se il percorso tra due posizioni è libero da ostacoli.
        aggiorna(turno, mossa, scacchiera):
            Applica la mossa della torre sulla scacchiera, gestendo scacco e 
            scacco matto.
    """

    @staticmethod
    def torre_mossa_valida(turno, mossa, scacchiera):
        """Verifica se la mossa della torre è valida (gestisce catture e ambiguità)."""
        Torre_specifica = re.compile(r"""^T([a-h]|[1-8])x?[a-h][1-8][+#]?$""")
        cattura = 'x' in mossa or ':' in mossa
        colore_turno = "bianco" if turno == 0 else "nero"

        # Estrai destinazione (es. 'g5' da 'Txg5' o 'Tg5')
        dest_str = mossa.split('x')[-1].split(':')[-1] if cattura else mossa[-2:]

        try:
            x_dest, y_dest = ControlScacchiera.notazione_to_posizione(dest_str)
        except Exception:
            PartitaB.print_mossa_negata2()
            return None


        # Controlla ambiguità: es. 'Tbd4', 'T3d4'
        specificatore = None
        if len(mossa) > 3:
            parte_specifica = (
                mossa.split('x')[0].split(':')[0]
                if cattura else mossa[:-2]
            )
            if parte_specifica.startswith('T'):
                parte_specifica = parte_specifica[1:]
                if parte_specifica:
                    specificatore = parte_specifica

        # Ricerca torri che possono muoversi in (x_dest, y_dest)
        torri_valide = []
        for x in range(8):
            for y in range(8):
                pezzo = scacchiera.get_pezzo(x, y)
                if (
                    isinstance(pezzo, Torre)
                    and pezzo.colore == colore_turno
                    and (x == x_dest or y == y_dest)
                    and MovimentoTorre._percorso_libero(
                        x, y, x_dest, y_dest, scacchiera
                    )
                ):
                    torri_valide.append((x, y))

        if len(torri_valide) == 0:
            PartitaB.print_mossa_negata2()
            return None
        
        # Controllo pezzo destinazione
        pezzo_dest = scacchiera.get_pezzo(x_dest, y_dest)
        if pezzo_dest:
            if pezzo_dest.colore == colore_turno:
                PartitaB.print_casella_occupata()
                return None
            elif not cattura:
                PartitaB.print_mossa_illegale()
                return None
        elif cattura:
            PartitaB.print_mossa_negata2()
            return None

        if len(torri_valide) == 1:
            if Torre_specifica.match(mossa):
                for x, y in torri_valide: 
                        #codice che controlla se nella colonna o 
                        # riga indicata ci sia il pezzo 
                        col = ControlScacchiera.posizione_to_notazione(x, y)[0]
                        riga = ControlScacchiera.posizione_to_notazione(x, y)[1]
                        print(col, riga)
                        
                        if specificatore in (col, riga):
                            #print("colonna o riga corretta")
                            return (*torri_valide[0], x_dest, y_dest)
                        else:
                            PartitaB.colonna_riga_inidcata_errata()
                            return None
            else:
                return (*torri_valide[0], x_dest, y_dest)

        else:
            # Ambiguità: controlla specificatore (es. colonna o riga)
            if specificatore:
                torri_filtrate = []
                for x, y in torri_valide:
                    notazione = ControlScacchiera.posizione_to_notazione(x, y)
                    if specificatore in notazione and len(torri_valide) > 1:
                        torri_filtrate.append((x, y))

                if len(torri_filtrate) == 1:
                    return (*torri_filtrate[0], x_dest, y_dest)
                PartitaB.print_mossa_torre_ambiguità_non_valida()
                return None
            else:
                PartitaB.print_ambiguità()
                return None

    @staticmethod
    def _percorso_libero(x1, y1, x2, y2, scacchiera):
        """Verifica se il percorso tra (x1,y1) e (x2,y2) è libero (esclusi estremi)."""
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if scacchiera.get_pezzo(x1, y):
                    return False
        elif y1 == y2:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if scacchiera.get_pezzo(x, y1):
                    return False
        else:
            return False  
        return True
    
    @staticmethod
    def aggiorna(turno, mossa, scacchiera):
        # Verifica se la mossa dichiara scacco (+) o scacco matto (#)
        dichiara_scacco = '+' in mossa
        dichiara_scacco_matto = '#' in mossa
        mossa_senza_simboli = mossa.replace('+', '').replace('#', '')
        
        # Valida la mossa come mossa della Torre
        origine_dest = MovimentoTorre.torre_mossa_valida(
            turno, mossa_senza_simboli, scacchiera
        )
        if origine_dest is None:
            return False

        x_orig, y_orig, x_dest, y_dest = origine_dest

        # Salva il pezzo di destinazione per eventuale ripristino
        pezzo_dest_originale = scacchiera.get_pezzo(x_dest, y_dest)
        
        # Simula la mossa
        torre = scacchiera.get_pezzo(x_orig, y_orig)
        scacchiera.set_pezzo(x_dest, y_dest, torre)
        scacchiera.set_pezzo(x_orig, y_orig, None)

        # Controlla se il Re del giocatore è sotto scacco dopo la mossa
        colore_giocatore = "bianco" if turno == 0 else "nero"
        if ControlScacchi.re_sotto_scacco(scacchiera, colore_giocatore):
            # Ripristina la scacchiera
            scacchiera.set_pezzo(x_orig, y_orig, torre)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_re_minacciato()
            return False

        # Controlla se il Re avversario è sotto scacco o scacco matto
        colore_avversario = "nero" if turno == 0 else "bianco"
        re_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, colore_avversario)
        re_in_scacco_matto = (
            re_sotto_scacco and
            ControlScacchi.verifica_scacco_scacco_matto(scacchiera, colore_avversario)
        )
        print(
            re_sotto_scacco,
            ControlScacchi.verifica_scacco_scacco_matto(
                scacchiera, colore_avversario
            )
        )
        # Gestione errori nella dichiarazione di scacco/scacco matto
        if re_in_scacco_matto:
            if not dichiara_scacco_matto:
                # Scacco matto non dichiarato
                scacchiera.set_pezzo(x_orig, y_orig, torre)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                PartitaB.print_scacco_matto_non_indicato()
                return False
        elif re_sotto_scacco:
            if not dichiara_scacco:
                # Scacco non dichiarato
                scacchiera.set_pezzo(x_orig, y_orig, torre)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                PartitaB.print_scacco_non_indicato()
                return False
        elif dichiara_scacco_matto:
            # Dichiara scacco matto ma non è vero
            scacchiera.set_pezzo(x_orig, y_orig, torre)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_scacco_matto_non_valido()
            return False
        elif dichiara_scacco:
            # Dichiara scacco ma non è vero
            scacchiera.set_pezzo(x_orig, y_orig, torre)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_scacco_non_valido()
            return False
        
        #conferma la mossa 
        return True