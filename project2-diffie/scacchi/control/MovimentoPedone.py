"""<<Control>>."""
import re

from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.AggiornaScacchiera import ControlScacchiera
from scacchi.control.ControlScacchi import ControlScacchi
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Regina import Regina
from scacchi.entity.Torre import Torre


class MovimentoPedone:
    """Classe statica per validare le mosse dei pedoni.

    Utilizza due for per individuare il pedone del colore di turno
    e verifica se la mossa è valida avanti di 1 o 2 caselle.
    """

    @staticmethod
    def is_pedone_mossa_valida(turno, scelta, scacchiera):
        """Controlla se la mossa del pedone è valida.

        Parametri
        ----------
        turno_colore : str
            "bianco" o "nero".
        nuova_posizione : (x, y)
            Coppia di interi per la nuova posizione.
        scacchiera : Scacchiera
            Istanza della scacchiera con get_pezzo(x, y).

        Ritorna
        -------
        True se la mossa è valida, False altrimenti.
        """
        #verifica se la mossa è una promozione
        if '1' in scelta or '8' in scelta:
            match = re.search(r'=?[DTAC]', scelta)
            if match:
                # estraggo la parte prima della lettera di promozione
                scelta = scelta[:match.start()]      # da 'b8D' ottengo 'b8'
                destinazione_new = ControlScacchiera.traduci_mossa(scelta[-2:])
                
                if destinazione_new is None:
                    return None

                #verifico se è promozione con cattura
                if scelta[1] == 'x' or scelta[1] == ':':
                    # serve a prendere la parte finale della stringa dopo la lettera "x"
                    scelta = scelta.replace(':', 'x')
                    mossa_valida = MovimentoPedone.cattura_pezzo(
                        turno, scelta, scacchiera
                    )
                    if mossa_valida is None:
                        PartitaB.print_mossa_negata2()
                        return None
                    elif len(mossa_valida) == 2:
                        # cattura normale
                        x_part, y_part = mossa_valida
                        # non c'è coordinata “dietro” da ripristinare
                        return (x_part, y_part)
                    elif len(mossa_valida) == 5:
                        x_part, y_part, x_elimina, y_elimina,pezzo_elim = mossa_valida
                        # memorizzo le coords della pedina catturata 
                        # per il futuro rollback
                        return (x_part, y_part, x_elimina, y_elimina,pezzo_elim)
                   
                else:
                    # * VERIFICA MOVIMENTO VALIDO *
                    x_dest, y_dest = destinazione_new
                    y_orig = y_dest - 1 if turno == 0 else y_dest + 1
                    # controlla che ci sia effettivamente il pedone lì
                    pez = scacchiera.get_pezzo(x_dest, y_orig)
                    if (
                        isinstance(pez, Pedone)
                        and pez.colore in ("bianco", "nero")[turno]
                    ):
                        return (x_dest, y_orig)
                    else:
                        PartitaB.print_mossa_negata2()
                        return None

            else:
                PartitaB.promozione_non_specificata()
                return None


        # verifica se la mossa è una cattura
        if scelta[1] == 'x' or scelta[1] == ':':
            # serve a prendere la parte finale della stringa dopo la lettera "x"
            scelta = scelta.replace(':', 'x')

            mossa_valida = MovimentoPedone.cattura_pezzo(turno, scelta, scacchiera)
            if mossa_valida is None:
                PartitaB.print_mossa_negata2()
                return None
            elif len(mossa_valida) == 2:
                # cattura normale
                x_part, y_part = mossa_valida
                # non c'è coordinata “dietro” da ripristinare
                return (x_part, y_part)
            elif len(mossa_valida) == 5:
                # en passant: m == (x_part, y_part, x_elimina, y_elimina)
                x_part, y_part, x_elimina, y_elimina,pezzo_elim = mossa_valida
                # memorizzo le coords della pedina catturata per il futuro rollback
                return (x_part, y_part, x_elimina, y_elimina,pezzo_elim)

        # Altrimenti, è una mossa normale
        mossa = ControlScacchiera.traduci_mossa(scelta)

        if mossa is None:
            return None

        x, y = mossa
        if scacchiera.get_pezzo(x, y) is not None:
            PartitaB.print_casella_occupata()
            return None

            # Aggiungi questo controllo all'inizio
        pezzo_origine = None
        if turno == 0:  # turno bianco
            if y == 3:
                pezzo_origine = scacchiera.get_pezzo(x, 1) or scacchiera.get_pezzo(x, 2)
            else:
                pezzo_origine = scacchiera.get_pezzo(x, y-1)
        else:  # turno nero
            if y == 4:
                pezzo_origine = scacchiera.get_pezzo(x, 6) or scacchiera.get_pezzo(x, 5)
            else:
                pezzo_origine = scacchiera.get_pezzo(x, y+1)

        # Verifica che il pezzo sia del giocatore corrente
        if pezzo_origine is not None and (
            (turno == 0 and pezzo_origine.colore != "bianco") or
            (turno == 1 and pezzo_origine.colore != "nero")
        ):
            PartitaB.print_mossa_negata3()
            return None

        if turno == 0 and y in range(1,8) and x in range(0,8):
        #bianco
            if y==3:
                if isinstance(scacchiera.get_pezzo(x, 1), Pedone) and \
                    scacchiera.get_pezzo(x, 2) is None and \
                    scacchiera.get_pezzo(x, 1).colore == "bianco":
                    return (x,1)
                elif isinstance(scacchiera.get_pezzo(x,2) , Pedone) and \
                            scacchiera.get_pezzo(x, 2).colore == "bianco":
                            return (x,2)
                else:
                    PartitaB.print_mossa_negata2()
                    return None
            else:
                if isinstance(scacchiera.get_pezzo((x), y-1), Pedone) and \
                    scacchiera.get_pezzo(x, y-1).colore == "bianco":
                    return (x,y-1)
                else:
                    PartitaB.print_mossa_negata()
                    return None
        elif turno == 1 and y<=5 and x in range(0,8):
        #nero
            if y==4:
                if isinstance(scacchiera.get_pezzo(x,5) , Pedone) and \
                    scacchiera.get_pezzo(x, 5).colore == "nero":
                    return (x,5)
                elif isinstance(scacchiera.get_pezzo(x, 6), Pedone) and \
                    scacchiera.get_pezzo(x, 5) is None and \
                    scacchiera.get_pezzo(x, 6).colore == "nero":
                    return (x,6)
                else:
                    PartitaB.print_mossa_negata()
                    return None
            else:
                if isinstance(scacchiera.get_pezzo((x), y+1), Pedone) and \
                    scacchiera.get_pezzo(x, y+1).colore == "nero":
                    return (x,y+1)
                else:
                    PartitaB.print_mossa_negata()
                    return None
        else:
            PartitaB.print_mossa_negata()
            return None

    @staticmethod
    def cattura_pezzo(turno, mossa, scacchiera):
        """Gestisce la cattura di un pezzo da parte di un pedone.

        Parametri
        ----------
        turno : int
            0 per il bianco, 1 per il nero.
        mossa : str
            Mossa in notazione algebrica, es. "hxg5".
        scacchiera : Scacchiera
            Istanza della scacchiera.

        Ritorna
        -------
        (x_dest, y_dest) se la cattura è valida, None altrimenti.
        """
        # 1) Estraggo la colonna da cui parte il pedone, es. "h" in "hxg5"
        lettera_orig = mossa[0].lower()
        x_origine = ord(lettera_orig) - ord('a')  # "h" → 7

        try:
            notazione_dest = mossa.split("x")[-1]
        except Exception:
            return None

        #3) Converto "g5" in coordinate (x_dest, y_dest) tramite il metodo traduci_mossa
        match = re.search(r':x', notazione_dest)
        if match:
            # estraggo la parte prima della lettera di promozione
            notazione_dest = notazione_dest[:match.start(-2)]      

        dest = ControlScacchiera.traduci_mossa(notazione_dest)
        if dest is None:
            return None
        x_dest, y_dest = dest

        #controllo che la destinazione non sia la posizione del re
        if scacchiera.get_pezzo(x_dest, y_dest) is not None:
            pezzo = scacchiera.get_pezzo(x_dest, y_dest)
            if isinstance(pezzo, Re):
                PartitaB.print_mossa_negata2()
                return None

        # 4) Controllo che tutte le coordinate siano entro i limiti 0–7
        if not (0 <= x_origine <= 7 and 0 <= x_dest <= 7 and 0 <= y_dest <= 7):
            PartitaB.print_mossa_negata2()
            return None

        # 5) Controllo  se in (x_dest, y_dest) c'è un pezzo da catturare
        pezzo_dest = scacchiera.get_pezzo(x_dest, y_dest)
        if pezzo_dest is None:
            mossa_enP=MovimentoPedone.en_passant(pezzo_dest, y_dest, x_dest, 
                                                 mossa,turno,scacchiera)
            return mossa_enP
        

        # 8) Verifico che il pezzo in destinazione sia effettivamente avversario
        if (turno == 0 and pezzo_dest.colore == "bianco") or \
        (turno == 1 and pezzo_dest.colore == "nero"):
            # Non puoi catturare un pezzo dello stesso colore
            PartitaB.print_mossa_negata2()
            return None

        # 9) Stimo la riga di origine del pedone che cattura:
        #    - Per i bianchi, l'origine sta a y_dest - 1 (uno step più in basso)
        #    - Per i neri, l'origine sta a y_dest + 1 (uno step più in alto)
        y_origine = y_dest - 1 if turno == 0 else y_dest + 1

        # 10) Controllo che anche y_origine sia dentro la scacchiera
        if not (0 <= y_origine <= 7):
            PartitaB.print_mossa_negata2()
            return None

        # 11) Controllo che la mossa sia diagonale:
        #     x_origine deve essere x_dest - 1 o x_dest + 1
        if x_origine == x_dest - 1 or x_origine == x_dest + 1:
            # Verifico che nella casella di origine stimata ci sia un pedone
            pezzo_origin = scacchiera.get_pezzo(x_origine, y_origine)
            if pezzo_origin is None or not isinstance(pezzo_origin, Pedone):
                PartitaB.print_mossa_negata2()
                return None

            # 12) Controllo che il pedone di origine sia dello stesso colore del turno
            if (pezzo_origin.colore == "bianco" and turno == 0) or \
            (pezzo_origin.colore == "nero" and turno == 1):
                # 13) Per cattura normale, non elimino il pezzo qui
                # L'eliminazione avverrà nel metodo aggiorna
                return (x_origine, y_origine)
            else:
                PartitaB.print_mossa_negata2()
                return None

        # 14) Se non è una diagonale valida, mossa negata
        PartitaB.print_mossa_negata2()
        return None

    def en_passant(pezzo_dest, y_dest, x_dest, mossa,turno,scacchiera):
        # 6) Se non c'è nessun pezzo in destinazione, controlla en passant
        if pezzo_dest is None:
            # ─── Controllo "en passant" per il bianco ───────────────────────────
            if turno == 0 and y_dest == 5:
                pedone_nero = scacchiera.get_pezzo(x_dest, 4)
                if (isinstance(pedone_nero, Pedone) and pedone_nero.colore == "nero"
                            and scacchiera.en_passant_target == (x_dest, 4)):
                        if turno == 0:
                            y_origine = y_dest - 1
                        x_origine = mossa[0].lower()
                        coord_origine=str(x_origine) + str(y_origine)
                        dest = ControlScacchiera.traduci_mossa(coord_origine)
                        if dest is None:
                            PartitaB.print_mossa_negata2()
                            return None
                        #X origine convertia
                        x_origine_Conv=dest[0]
                        pezzo_origin = scacchiera.get_pezzo(x_origine_Conv, 4)
                        if (pezzo_origin.colore == "bianco" and turno == 0) or (
                            pezzo_origin.colore == "nero" and turno == 1):
                        # 13) Per cattura normale, non elimino il pezzo qui
                        # L'eliminazione avverrà nel metodo aggiorna
                            # NON elimino il pezzo qui, ritorno solo le coordinate
                            # L'eliminazione avverrà nel metodo aggiorna 
                            # dopo i controlli
                            return (x_origine_Conv, 4, x_dest, 4, pedone_nero)
            # ─── Controllo "en passant" per il nero ─────────────────────────────
            elif turno == 1 and y_dest == 2:
                pedone_bianco = scacchiera.get_pezzo(x_dest, 3)
                if (isinstance(pedone_bianco, Pedone) 
                            and pedone_bianco.colore == "bianco"
                            and scacchiera.en_passant_target == (x_dest, 3)):
                        if turno == 1:
                            y_origine = y_dest + 1
                        x_origine = mossa[0].lower()
                        coord_origine=str(x_origine) + str(y_origine)
                        dest = ControlScacchiera.traduci_mossa(coord_origine)
                        if dest is None:
                            PartitaB.print_mossa_negata2()
                            return None
                        x_origine_Conv=dest[0]
                        pezzo_origin = scacchiera.get_pezzo(x_origine_Conv, 3)
                        if (pezzo_origin.colore == "bianco" and turno == 0) or (
                            pezzo_origin.colore == "nero" and turno == 1):
                        # 13) Per cattura normale, non elimino il pezzo qui
                        # L'eliminazione avverrà nel metodo aggiorna
                            # NON elimino il pezzo qui, ritorno solo le coordinate
                            return (x_origine_Conv, 3, x_dest, 3, pedone_bianco)



    @staticmethod
    def promozione_pedone(turno, scacchiera, mossa):
        """Gestisce la promozione del pedone quando la notazione contiene D, T, A o C.

        - turno: 0 per Bianco, 1 per Nero
        - scacchiera: l’istanza di Scacchiera
        - mossa: stringa in notazione algebrica italiana, es. "bxa8D" o "a8D".

        Ritorna True se la promozione è andata a buon fine, None altrimenti.
        """
        # 1) Estrae l’ultimo carattere per la promozione
        tipo_promozione = mossa[-1]

        match = re.search(r'=?[DTAC]', mossa)
        if not match:
            return None  # se non trovo mai D/T/A/C, esco

        # 2) Prendo la parte prima di match.start(), ad es. "bxa8" da "bxa8D"
        parte_senza_prom = mossa[: match.start()]  # "bxa8"

        # 3) Ora devo isolare la “casella” vera e propria, che può essere
        if 'x' in parte_senza_prom or ':' in parte_senza_prom:
            # sostituisco eventuale ':' con 'x' e splitto
            mossa_omogenea = parte_senza_prom.replace(':', 'x')
            casella = mossa_omogenea.split('x')[-1]
        else:
            casella = parte_senza_prom

        # 4) Traduci "a8" in coordinate
        coord_tradotte = ControlScacchiera.traduci_mossa(casella)
        if coord_tradotte is None:
            return None
        x_dest, y_dest = coord_tradotte
        # 6) Controllo che lì ci sia davvero un pedone
        pedone = scacchiera.get_pezzo(x_dest, y_dest)
        if not isinstance(pedone, Pedone):
            return None

        # 7) In base al turno, controlla che sia in traversa di promozione
        colore = "bianco" if turno == 0 else "nero"
        if turno == 0 and y_dest != 7:
            return None
        if turno == 1 and y_dest != 0:
            return None

        # 8) Sostituisco il pedone con il pezzo scelto
        PartitaB.promozione(turno)
        match tipo_promozione:
            case 'D':
                scacchiera.set_pezzo(x_dest, y_dest, Regina(colore=colore))
                return True
            case 'T':
                scacchiera.set_pezzo(x_dest, y_dest, Torre(colore=colore))
                return True
            case 'A':
                scacchiera.set_pezzo(x_dest, y_dest, Alfiere(colore=colore))
                return True
            case 'C':
                scacchiera.set_pezzo(x_dest, y_dest, Cavallo(colore=colore))
                return True
            case _:
                PartitaB.promozione_non_valida()
                return None
                
    @staticmethod
    def aggiorna(turno, mossa, scacchiera):
        # Verifica se la mossa dichiara scacco (+) o scacco matto (#)
        dichiara_scacco = '+' in mossa
        dichiara_scacco_matto = '#' in mossa
        mossa_senza_simboli = mossa.replace('+', '').replace('#', '')
        
        # 1) Verifico preliminarmente se la mossa è valida (usa la mossa senza simboli)
        risultato_prelim = MovimentoPedone.is_pedone_mossa_valida(
            turno, mossa_senza_simboli, scacchiera
        )
        if risultato_prelim is None:
            return False
        # Inizializza le variabili per en passant
        x_eliminato, y_eliminato, pezz_elimin = None, None, None
        
        if len(risultato_prelim) == 5:  # En passant
            (
                x_partenza,
                y_partenza,
                x_eliminato,
                y_eliminato,
                pezz_elimin,
            ) = risultato_prelim
        else:
            (x_partenza, y_partenza) = risultato_prelim

        # Salva il pezzo di destinazione originale per eventuale ripristino
        pezzo_dest_originale = None
        x_dest, y_dest = None, None

        # 2) Se NON è promozione
        match_promozione = re.search(r'=?[DTAC]', mossa_senza_simboli)
        if not match_promozione:
            # Caso "cattura oppure mossa semplice"
            if re.search(r'[x:]', mossa_senza_simboli):
                part_dest = re.split(r'[x:]', mossa_senza_simboli)[-1]
                sq = re.match(r'^([a-h][1-8])', part_dest)
                if sq is None:
                    return False
                
                coords_tradotte = ControlScacchiera.traduci_mossa(sq.group(1))
            else:
                coords_tradotte = ControlScacchiera.traduci_mossa(mossa_senza_simboli)

            if coords_tradotte is None:
                return False
            x_dest, y_dest = coords_tradotte
            
            # Salva il pezzo di destinazione originale
            pezzo_dest_originale = scacchiera.get_pezzo(x_dest, y_dest)
            
            # Gestione en passant
            if abs(y_dest - y_partenza) == 2 and (y_partenza == 1 or y_partenza == 6):
                scacchiera.en_passant_target = (x_dest, y_dest)
            else:
                # Salva il target en passant precedente per eventuale ripristino
                old_en_passant_target = scacchiera.en_passant_target
                scacchiera.en_passant_target = None
                
            # Sposta il pedone (simulazione)
            pedone = scacchiera.get_pezzo(x_partenza, y_partenza)
            scacchiera.set_pezzo(x_dest, y_dest, pedone)
            scacchiera.set_pezzo(x_partenza, y_partenza, None)
            
            # Se è en passant, rimuovi il pezzo catturato SOLO ADESSO
            if x_eliminato is not None and y_eliminato is not None:
                scacchiera.set_pezzo(x_eliminato, y_eliminato, None)

        # 3) Se è promozione 
        else:
            notation_base = mossa_senza_simboli[:match_promozione.start()]
            if len(notation_base) < 2:
                return False
                
            if 'x' in notation_base or ':' in notation_base:
                mossa_omogenea = notation_base.replace(':','x')
                casella = mossa_omogenea.split('x')[-1]
            else:
                casella = notation_base
            coord_tradotte = ControlScacchiera.traduci_mossa(casella)
            if coord_tradotte is None:
                return False
            x_dest, y_dest = coord_tradotte
            
            # Salva il pezzo di destinazione originale
            pezzo_dest_originale = scacchiera.get_pezzo(x_dest, y_dest)
            
            # Se c'è una cattura, rimuovi il pezzo avversario
            if re.search(r'[x:]', notation_base):
                scacchiera.set_pezzo(x_dest, y_dest, None)
                old_en_passant_target = scacchiera.en_passant_target
                scacchiera.en_passant_target = None

            # Sposta il pedone (simulazione)
            pedone = scacchiera.get_pezzo(x_partenza, y_partenza)
            scacchiera.set_pezzo(x_dest, y_dest, pedone)
            scacchiera.set_pezzo(x_partenza, y_partenza, None)

            # Esegui la promozione (simulazione)
            esito_promozione = MovimentoPedone.promozione_pedone(
                turno, scacchiera, mossa_senza_simboli
            )
            if esito_promozione is None:
                # Ripristina se la promozione fallisce
                scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                return False

        # Controlla se il Re del giocatore è sotto scacco dopo la mossa
        colore_giocatore = "bianco" if turno == 0 else "nero"
        if ControlScacchi.re_sotto_scacco(scacchiera, colore_giocatore):
            # Ripristina la scacchiera
            if not match_promozione:
                scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                # Ripristina il pezzo eliminato dall'en passant se c'era
                if x_eliminato is not None and y_eliminato is not None:
                    scacchiera.set_pezzo(x_eliminato, y_eliminato, pezz_elimin)
                    scacchiera.en_passant_target = old_en_passant_target
            else:
                scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_re_minacciato()
            return False

        # Controlla se il Re avversario è sotto scacco o scacco matto
        colore_avversario = "nero" if turno == 0 else "bianco"
        re_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, colore_avversario)
        re_in_scacco_matto = (
            re_sotto_scacco and 
            ControlScacchi.verifica_scacco_scacco_matto(
                scacchiera, colore_avversario
            )
        )

        # Gestione errori nella dichiarazione di scacco/scacco matto
        if re_in_scacco_matto:
            if not dichiara_scacco_matto:
                # Ripristina e segnala errore
                if not match_promozione:
                    scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                    scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                    # Ripristina il pezzo eliminato dall'en passant se c'era
                    if x_eliminato is not None and y_eliminato is not None:
                        scacchiera.set_pezzo(x_eliminato, y_eliminato, pezz_elimin)
                        scacchiera.en_passant_target = old_en_passant_target
                else:
                    scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                    scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                PartitaB.print_scacco_matto_non_indicato()
                return False
        elif re_sotto_scacco:
            if not dichiara_scacco:
                if not match_promozione:
                    scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                    scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                    # Ripristina il pezzo eliminato dall'en passant se c'era
                    if x_eliminato is not None and y_eliminato is not None:
                        scacchiera.set_pezzo(x_eliminato, y_eliminato, pezz_elimin)
                        scacchiera.en_passant_target = old_en_passant_target
                else:
                    scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                    scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                PartitaB.print_scacco_non_indicato()
                return False
        elif dichiara_scacco_matto:
            if not match_promozione:
                scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                # Ripristina il pezzo eliminato dall'en passant se c'era
                if x_eliminato is not None and y_eliminato is not None:
                    scacchiera.set_pezzo(x_eliminato, y_eliminato, pezz_elimin)
                    scacchiera.en_passant_target = old_en_passant_target
            else:
                scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_scacco_matto_non_valido()
            return False
        elif dichiara_scacco:
            if not match_promozione:
                scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
                # Ripristina il pezzo eliminato dall'en passant se c'era
                if x_eliminato is not None and y_eliminato is not None:
                    scacchiera.set_pezzo(x_eliminato, y_eliminato, pezz_elimin)
                    scacchiera.en_passant_target = old_en_passant_target
            else:
                scacchiera.set_pezzo(x_partenza, y_partenza, pedone)
                scacchiera.set_pezzo(x_dest, y_dest, pezzo_dest_originale)
            PartitaB.print_scacco_non_valido()
            return False

        # Se tutto ok, conferma la mossa (non serve ri-spostare perché già spostato)
        return True