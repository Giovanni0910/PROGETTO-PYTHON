"""<<Entity>>."""

from scacchi.entity.Pezzo import Pezzo


class Pedone(Pezzo):
    """Rappresenta un Pedone nel gioco degli scacchi.

    Il Pedone può muoversi in avanti di una casella, ma può muovere di due
    caselle solo dalla sua posizione iniziale. Può catturare pezzi avversari
    in diagonale.
    """

    def __init__(self, colore):
        super().__init__(colore)
        self.tipo = "pedone"

    def __str__(self):
        """Ritorna il colore del pedone."""
        return f"pedone di colore {self.colore}"
    
    def puo_attaccare(self, x_part, y_part, x_arr, y_arr, scacchiera):
        # Controlla se la casella di arrivo è occupata da un pezzo alleato
        pezzo_arrivo = scacchiera.get_pezzo(x_arr, y_arr)
        if pezzo_arrivo and pezzo_arrivo.colore == self.colore:
            # Non puoi muoverti in una casella occupata da un pezzo alleato
            return False 
        if x_arr== x_part +1 and y_arr in [y_part - 1, y_part + 1]:
            # Cattura diagonale a destra
            return True
        
        elif x_arr == x_part -1 and y_arr in [y_part - 1, y_part + 1]:
            # Cattura diagonale sinistra
            return True
        return False

        
    def mosse_possibili(self, x, y, scacchiera):
        mosse = []
        direzione = -1 if self.colore == "bianco" else 1
        start_row = 6 if self.colore == "bianco" else 1

        # Movimento in avanti (1 casella)
        nuova_x = x + direzione
        if 0 <= nuova_x < 8 and scacchiera.get_pezzo(nuova_x, y) is None:
            mosse.append((nuova_x, y))
            
            # Doppio avanzamento (solo dalla posizione iniziale)
            if x == start_row:
                new_x_double = x + 2 * direzione
                if (
                    0 <= new_x_double < 8
                    and scacchiera.get_pezzo(new_x_double, y) is None
                ):
                    mosse.append((new_x_double, y))

        # Catture diagonali (standard)
        for dy in [-1, 1]:
            nx, ny = x + direzione, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                pezzo = scacchiera.get_pezzo(nx, ny)
                if pezzo and pezzo.colore != self.colore:
                    mosse.append((nx, ny))
        return mosse
