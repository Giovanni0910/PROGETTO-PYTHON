"""<<Entity>>."""
from scacchi.entity.Pezzo import Pezzo


class Regina(Pezzo):
    """Rappresenta una Regina nel gioco degli scacchi.

    La Regina può muoversi in linea retta orizzontalmente, verticalmente
    o in diagonale sulla scacchiera, senza limitazioni di distanza,
    a meno che non ci siano ostacoli lungo il percorso.
    """

    def __init__(self, colore):
        super().__init__(colore)
        self.tipo = "regina"

    def __str__(self):
        """Ritorna il colore della Regina."""
        return f"Regina di colore {self.colore}"
    
    def puo_attaccare(self, x_part, y_part, x_arr, y_arr, scacchiera):
        # Caso speciale: sta muovendo nella sua stessa casella?
        if x_part == x_arr and y_part == y_arr:
            return False

        # Controlla se il pezzo di arrivo è alleato (non si può muovere lì)
        pezzo_arrivo = scacchiera.get_pezzo(x_arr, y_arr)
        if pezzo_arrivo and pezzo_arrivo.colore == self.colore:
            return False

        # Movimento da Torre (linee rette)
        if x_part == x_arr or y_part == y_arr:
            if x_part == x_arr:  # Verticale
                step = 1 if y_arr > y_part else -1
                for y in range(y_part + step, y_arr, step):
                    if scacchiera.get_pezzo(x_part, y):
                        return False
            else:  # Orizzontale
                step = 1 if x_arr > x_part else -1
                for x in range(x_part + step, x_arr, step):
                    if scacchiera.get_pezzo(x, y_part):
                        return False
            return True

        # Movimento da Alfiere (diagonale)
        dx = abs(x_part - x_arr)
        dy = abs(y_part - y_arr)
        if dx == dy:
            step_x = 1 if x_arr > x_part else -1
            step_y = 1 if y_arr > y_part else -1
            x, y = x_part + step_x, y_part + step_y
            while x != x_arr and y != y_arr:
                if scacchiera.get_pezzo(x, y):
                    return False
                x += step_x
                y += step_y
            return True

        return False

    
    def mosse_possibili(self, x, y, scacchiera):
        mosse = []
        # Direzioni: Torre (4) + Alfiere (4)
        direzioni = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Torre
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Alfiere
        ]
        
        for dx, dy in direzioni:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                pezzo = scacchiera.get_pezzo(nx, ny)
                if pezzo is None:
                    mosse.append((nx, ny))
                elif pezzo.colore != self.colore:
                    mosse.append((nx, ny))  # Aggiungi la cattura
                    break  # Fermati dopo un pezzo avversario
                else:
                    break  # Pezzo alleato: blocca il percorso
                nx += dx
                ny += dy
        return mosse