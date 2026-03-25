"""<<Control>>."""
from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.AggiornaScacchiera import ControlScacchiera
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Regina import Regina
from scacchi.entity.Torre import Torre


class MovimentoRe:
    """Gestisce le regole di movimento e controllo del Re negli scacchi.

    Questa classe fornisce metodi statici per verificare la validità delle mosse
    del Re, aggiornare la scacchiera, controllare se una casella è sotto scacco
    e determinare se il Re è attaccato.
    Metodi:
        re_mossa_valida(turno, mossa, scacchiera):
            Verifica se la mossa del Re è valida secondo le regole degli scacchi.
        aggiorna(turno, mossa, scacchiera):
            Aggiorna la scacchiera eseguendo una mossa valida del Re.
        casella_sotto_scacco(scacchiera, x, y, colore):
            Determina se una casella è minacciata da pezzi avversari.
        re_attaccato(scacchiera, colore_re):
            Verifica se il Re del colore specificato è sotto scacco.
    """

    @staticmethod
    def re_mossa_valida(turno, mossa, scacchiera):
        """Verifica se la mossa del re è valida con notazione italiana."""
        colore_turno = "bianco" if turno == 0 else "nero"
        cattura = 'x' in mossa

        # Estrai destinazione
        dest_str = mossa.strip()[-2:]
        try:
            x_dest, y_dest = ControlScacchiera.notazione_to_posizione(dest_str)
        except Exception:
            PartitaB.print_mossa_negata2()
           # print("Mossa illegale: notazione non valida")
            return None

        # Trova la posizione attuale del re
        re_pos = None
        for x in range(8):
            for y in range(8):
                pezzo = scacchiera.get_pezzo(x, y)
                if isinstance(pezzo, Re) and pezzo.colore == colore_turno:
                    re_pos = (x, y)
                    break
            if re_pos:
                break

        if not re_pos:
            PartitaB.print_re_non_trovato()
            return None

        x_re, y_re = re_pos

        # Verifica movimento legale (1 casella in qualsiasi direzione)
        if abs(x_re - x_dest) > 1 or abs(y_re - y_dest) > 1:
            PartitaB.print_movimento_re_errato()
            #print("Mossa illegale: il re può muoversi solo di una casella")
            return None

        # Controlla se la destinazione è minacciata
        if MovimentoRe.casella_sotto_scacco(scacchiera, x_dest, y_dest, colore_turno):
            PartitaB.print_movimento_re_negato()
            #print("Mossa illegale: la casella è minacciata")
            return None

        # Controlla presenza pezzo nella casella di destinazione
        pezzo_dest = scacchiera.get_pezzo(x_dest, y_dest)
        if pezzo_dest:
            if pezzo_dest.colore == colore_turno:
                PartitaB.print_casella_occupata()
                return None
            elif not cattura:
                PartitaB.print_cattura_non_specificata()
                #print("Mossa illegale: per catturare usa 'x'")
                return None
        elif cattura:
             PartitaB.print_cattura_negata2(dest_str)
             return None

        return (x_re, y_re)


    @staticmethod
    def aggiorna(turno, mossa, scacchiera):
        """Esegue l'aggiornamento della scacchiera dopo una mossa valida del re."""
        origine = MovimentoRe.re_mossa_valida(turno, mossa, scacchiera)
        if origine is None:
            return False

        arrivo = mossa.strip()[-2:]
        x_dest, y_dest = ControlScacchiera.notazione_to_posizione(arrivo)
        x_orig, y_orig = origine

        # Esegui la mossa
        scacchiera.set_pezzo(x_dest, y_dest, scacchiera.get_pezzo(x_orig, y_orig))
        scacchiera.set_pezzo(x_orig, y_orig, None)
        return True

    @staticmethod
    def casella_sotto_scacco(scacchiera, x, y, colore):
        
        colore_avversario = "nero" if colore == "bianco" else "bianco"
        
        # Controlla minacce da pedoni 
        direzione_pedone = 1 if colore_avversario == "nero" else -1
        for dx in [-1, 1]:
            px, py = x + dx, y + direzione_pedone 
            if 0 <= px < 8 and 0 <= py < 8:
                pezzo = scacchiera.get_pezzo(px, py)
                if isinstance(pezzo, Pedone) and pezzo.colore == colore_avversario:
                    return True

        # Controlla minacce da cavalli
        movimenti_cavallo = [(-2,-1), (-1,-2), (1,-2), (2,-1),
                            (2,1), (1,2), (-1,2), (-2,1)]
        for dx, dy in movimenti_cavallo:
            cx, cy = x + dx, y + dy
            if 0 <= cx < 8 and 0 <= cy < 8:
                pezzo = scacchiera.get_pezzo(cx, cy)
                if isinstance(pezzo, Cavallo) and pezzo.colore == colore_avversario:
                    return True

        # Controlla minacce in linee rette (torre, Regina)
        direzioni_linee = [(-1,0), (1,0), (0,-1), (0,1)]
        for dx, dy in direzioni_linee:
            for dist in range(1, 8):
                tx, ty = x + dx*dist, y + dy*dist
                if not (0 <= tx < 8 and 0 <= ty < 8):
                    break
                pezzo = scacchiera.get_pezzo(tx, ty)
                if pezzo:
                    if (
                        pezzo.colore == colore_avversario and
                        isinstance(pezzo, Torre | Regina)
                    ):
                        return True
                    break

        # Controlla minacce diagonali (alfiere, Regina)
        direzioni_diagonali = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dx, dy in direzioni_diagonali:
            for dist in range(1, 8):
                ax, ay = x + dx*dist, y + dy*dist
                if not (0 <= ax < 8 and 0 <= ay < 8):
                    break
                pezzo = scacchiera.get_pezzo(ax, ay)
                if pezzo:
                    if (
                        pezzo.colore == colore_avversario and
                        isinstance(pezzo, Alfiere | Regina)
                    ):
                        return True
                    break

        # Controlla minacce dal re avversario (caselle adiacenti)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                kx, ky = x + dx, y + dy
                if 0 <= kx < 8 and 0 <= ky < 8:
                    pezzo = scacchiera.get_pezzo(kx, ky)
                    if isinstance(pezzo, Re) and pezzo.colore == colore_avversario:
                        return True

        return False
    @staticmethod
    def re_attaccato(scacchiera, colore_re):
        x_re, y_re = None, None
        for x in range(8):
            for y in range(8):
                pezzo = scacchiera.get_pezzo(x, y)
                if pezzo and pezzo.tipo == "re" and pezzo.colore == colore_re:
                    x_re, y_re = x, y
                    break
            if x_re is not None:
                break
        if x_re is None or y_re is None:
            #print("Re non trovato sulla scacchiera!")
            return False
        return MovimentoRe.casella_sotto_scacco(
            scacchiera, x_re, y_re, colore_re
        ) #True se è sotto scacco altrimenti false