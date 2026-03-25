"""<<Entity>>."""
from scacchi.entity.Pezzo import Pezzo


class Cavallo(Pezzo):
    """Rappresenta un Cavallo nel gioco degli scacchi.

    Il Cavallo si muove a 'L' sulla scacchiera: due caselle in una direzione
    (orizzontale o verticale) e una casella perpendicolare, oppure viceversa.
    Può saltare sopra altri pezzi.
    """

    def __init__(self, colore):
        super().__init__(colore)
        self.tipo = "cavallo"

    def __str__(self):
        """Ritorna il clore del Cavallo."""
        return f"Cavallo di colore {self.colore}"
    
    def puo_attaccare(self, x_part, y_part, x_arr, y_arr, scacchiera):
        # Calcola la distanza tra la posizione di partenza e quella di arrivo
        dx = abs(x_part - x_arr)
        dy = abs(y_part - y_arr)

        # Controlla se la mossa è a forma di "L"
        if (dx, dy) not in [(2, 1), (1, 2)]:
            return False

        # Controlla se la casella di arrivo è occupata da un pezzo alleato
        pezzo_arrivo = scacchiera.get_pezzo(x_arr, y_arr)
        return not (pezzo_arrivo and pezzo_arrivo.colore == self.colore)


    def mosse_possibili(self, x, y, scacchiera):
        mosse = []
        spostamenti = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]

        for dx, dy in spostamenti:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                pezzo = scacchiera.get_pezzo(nx, ny)
                # Aggiungi se la casella è vuota o contiene un pezzo avversario
                if pezzo is None or pezzo.colore != self.colore:
                    mosse.append((nx, ny))
        return mosse