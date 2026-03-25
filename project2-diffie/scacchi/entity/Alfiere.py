"""<<Entity>>."""
from scacchi.entity.Pezzo import Pezzo


class Alfiere(Pezzo):
    """Rappresenta un Alfiere nel gioco degli scacchi.

    L'Alfiere può muoversi in diagonale sulla scacchiera,
    senza limitazioni di distanza, a meno che non ci siano
    ostacoli lungo il percorso.
    """

    def __init__(self, colore):
        super().__init__(colore)
        self.tipo= "alfiere"

    def __str__(self):
        """Ritorna il colore dell'Alfiere."""
        return f"Alfiere di colore {self.colore}"
    
    def puo_attaccare(self, x_part, y_part, x_arr, y_arr, scacchiera):
        dx = abs(x_part - x_arr)
        dy = abs(y_part - y_arr)

        # Controlla se il movimento è diagonale
        if dx != dy:
            return False

        step_x = 1 if x_arr > x_part else -1
        step_y = 1 if y_arr > y_part else -1
        x, y = x_part + step_x, y_part + step_y

        # Verifica che non ci siano pezzi intermedi
        while x != x_arr or y != y_arr:
            if scacchiera.get_pezzo(x, y):
                return False
            x += step_x
            y += step_y

        # Controlla se la casella di arrivo è occupata da un pezzo alleato
        pezzo_arrivo = scacchiera.get_pezzo(x_arr, y_arr)
        return not (pezzo_arrivo and pezzo_arrivo.colore == self.colore)

    
    def mosse_possibili(self, x, y, scacchiera):
        mosse = []
        direzioni = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonali

        for dx, dy in direzioni:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                pezzo = scacchiera.get_pezzo(nx, ny)
                if pezzo is None:
                    mosse.append((nx, ny))
                elif pezzo.colore != self.colore:
                    mosse.append((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy
        return mosse

