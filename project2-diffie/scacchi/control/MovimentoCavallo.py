
"""<<Control>>."""
import re

from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.AggiornaScacchiera import ControlScacchiera
from scacchi.control.ControlScacchi import ControlScacchi
from scacchi.entity.Cavallo import Cavallo


class MovimentoCavallo:
    """Gestisce la logica delle mosse del cavallo negli scacchi.

    Questa classe fornisce metodi per validare, gestire ambiguità e applicare le
    mosse del cavallo sulla scacchiera, secondo la notazione italiana e le regole
    degli scacchi, inclusa la gestione di scacco e scacco matto.

    Metodi:
        cavallo_mossa_valida(turno, mossa, scacchiera)
            Verifica se una mossa del cavallo è valida secondo la notazione italiana.
        controllo_ambiguita(
            scacchiera, colore_turno, specificatore, cavallo_specifica,
            x_dest, y_dest, mossa
        )
            Risolve le ambiguità quando più cavalli possono raggiungere la stessa
            casella.
        aggiorna(turno, mossa, scacchiera)
            Applica la mossa del cavallo sulla scacchiera, gestendo scacco e scacco
            matto.
    """

    def cavallo_mossa_valida(turno, mossa, scacchiera):
        """Verifica se la mossa del cavallo è valida con notazione italiana.

        Richiede 'x' per le catture.
        Gestisce ambiguità con specifica di colonna/riga (es. Cbd5, C3d5)
        """
        cavallo_specifica = re.compile(r"""^C([a-h]|[1-8])x?[a-h][1-8][+#]?$""")
        cattura = 'x' in mossa or ':' in mossa
        colore_turno = "bianco" if turno == 0 else "nero"
        
        # Estrai destinazione
        dest_str = mossa.split('x')[-1] if cattura else mossa
        dest_str = dest_str[-2:]  # Ultimi due caratteri: es. 'b5'
        
        try:
            x_dest, y_dest = ControlScacchiera.notazione_to_posizione(dest_str)
        except Exception:
            PartitaB.print_mossa_negata2()
            return None

        # Controlla se c'è un pezzo nella casella di destinazione
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

        # Estrai eventuali specificatori di colonna/riga (es. 'Cbd5' o 'C3d5')
        specificatore = None
        if len(mossa) > 3:  # Se c'è più della semplice notazione (es. 'Cd5')
            if cattura:
                parte_specifica = mossa.split('x')[0].split(':')[0]
            else:
                parte_specifica = mossa[:-2]
            if parte_specifica.startswith('C'):
                parte_specifica = parte_specifica[1:]
                if parte_specifica:  # Se c'è uno specificatore
                    specificatore = parte_specifica
        return (MovimentoCavallo.controllo_ambiguita
                (scacchiera,colore_turno,specificatore,
                 cavallo_specifica, x_dest,y_dest, mossa))

    def controllo_ambiguita(scacchiera,colore_turno,specificatore,cavallo_specifica,
                            x_dest, y_dest, mossa):

        # Genera le posizioni di origine possibili per un cavallo
        possibili_origini = [
            (x_dest - 2, y_dest - 1), (x_dest - 1, y_dest - 2),
            (x_dest + 1, y_dest - 2), (x_dest + 2, y_dest - 1),
            (x_dest + 2, y_dest + 1), (x_dest + 1, y_dest + 2),
            (x_dest - 1, y_dest + 2), (x_dest - 2, y_dest + 1)
        ]

        cavalli_validi = []
        for x_orig, y_orig in possibili_origini:
            if 0 <= x_orig < 8 and 0 <= y_orig < 8:
                pezzo = scacchiera.get_pezzo(x_orig, y_orig)
                if isinstance(pezzo, Cavallo) and pezzo.colore == colore_turno:
                    cavalli_validi.append((x_orig, y_orig))

        # Gestione ambiguità
        if len(cavalli_validi) == 0:
            PartitaB.print_mossa_negata2()
            return None
        elif len(cavalli_validi) == 1:
            if cavallo_specifica.match(mossa):
                for x, y in cavalli_validi:
                        # Controlla se lo specificatore corrisponde alla colonna o riga
                        col = ControlScacchiera.posizione_to_notazione(x, y)[0]
                        riga = ControlScacchiera.posizione_to_notazione(x, y)[1]
                        
                        if specificatore in (col, riga):
                            return cavalli_validi[0]
                        else:
                            PartitaB.colonna_riga_inidcata_errata()
                            return None
            else:
                return cavalli_validi[0]

        else:
            # Ci sono più cavalli che possono muovere, controlla lo specificatore
            if specificatore:
                cavalli_filtrati = []
                for x, y in cavalli_validi:
                    # Controlla se lo specificatore corrisponde alla colonna o riga
                    col = ControlScacchiera.posizione_to_notazione(x, y)[0]
                    riga = ControlScacchiera.posizione_to_notazione(x, y)[1]
                    
                    if specificatore in (col, riga):
                        cavalli_filtrati.append((x, y))
                
                if len(cavalli_filtrati) == 1:
                    return cavalli_filtrati[0]
                else:
                    PartitaB.print_mossa_cavallo_ambiguità_non_valida()
                    return None
            else:
                PartitaB.print_ambiguità()
                return None
    
    @staticmethod
    def aggiorna(turno, mossa, scacchiera):
        # Verifica se la mossa dichiara scacco (+) o scacco matto (#)
        dichiara_scacco = '+' in mossa
        dichiara_scacco_matto = '#' in mossa
        mossa_senza_simboli = mossa.replace('+', '').replace('#', '')

        
        # Valida la mossa come mossa del Cavallo
        origine = MovimentoCavallo.cavallo_mossa_valida(
            turno, mossa_senza_simboli, scacchiera
        )
        if origine is None:
            return False

        arrivo = mossa_senza_simboli.strip()[-2:]
        mossa_dest = ControlScacchiera.traduci_mossa(arrivo)
        if mossa_dest is None:
            return False
        x_dest, y_dest = mossa_dest
        x_orig, y_orig = origine

        # Salva il pezzo di destinazione per eventuale ripristino
        pezzo_dest_originale = scacchiera.get_pezzo(x_dest, y_dest)
        
        # Simula la mossa
        cavallo = scacchiera.get_pezzo(x_orig, y_orig)
        scacchiera.set_pezzo(x_dest, y_dest, cavallo)
        scacchiera.set_pezzo(x_orig, y_orig, None)

        # Controlla se il Re del giocatore è sotto scacco dopo la mossa
        colore_giocatore = "bianco" if turno == 0 else "nero"
        if ControlScacchi.re_sotto_scacco(scacchiera, colore_giocatore):
            # Ripristina la scacchiera
            scacchiera.set_pezzo(x_orig, y_orig, cavallo)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            #print("RE SOTTO SCACCO (mossa illegale)")
            PartitaB.print_re_minacciato()
            return False

        # Controlla se il Re avversario è sotto scacco o scacco matto
        colore_avversario = "nero" if turno == 0 else "bianco"
        re_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, colore_avversario)
        re_in_scacco_matto = (
            re_sotto_scacco and
            ControlScacchi.verifica_scacco_scacco_matto(scacchiera, colore_avversario)
        )
        print(re_sotto_scacco,ControlScacchi.verifica_scacco_scacco_matto(scacchiera, 
                                                                         colore_avversario))
        # Gestione errori nella dichiarazione di scacco/scacco matto
        if re_in_scacco_matto:
            if not dichiara_scacco_matto:
                # Scacco matto non dichiarato
                scacchiera.set_pezzo(x_orig, y_orig, cavallo)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                PartitaB.print_scacco_matto_non_indicato()
                return False
        elif re_sotto_scacco:
            if not dichiara_scacco:
                # Scacco non dichiarato
                scacchiera.set_pezzo(x_orig, y_orig, cavallo)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                PartitaB.print_scacco_non_indicato()
                return False
        elif dichiara_scacco_matto:
            # Dichiara scacco matto ma non è vero
            scacchiera.set_pezzo(x_orig, y_orig, cavallo)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_scacco_matto_non_valido()
            return False
        elif dichiara_scacco:
            # Dichiara scacco ma non è vero
            scacchiera.set_pezzo(x_orig, y_orig, cavallo)
            scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_scacco_non_valido()
            return False
        
        #conferma la mossa 
        return True
