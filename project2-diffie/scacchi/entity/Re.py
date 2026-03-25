"""<<Entity>>."""
from scacchi.entity.Pezzo import Pezzo


class Re(Pezzo):
    """Rappresenta un Re nel gioco degli scacchi.

    Il Re può muoversi di una casella in qualsiasi direzione.
    """
    
    def __init__(self, colore):
        super().__init__(colore) # 'bianco' o 'nero'
        self.tipo = "re"

    def __str__(self):
        """Restituisce una rappresentazione testuale del Re.

        Indica il colore del Re.
        """
        return f"Re di colore {self.colore}"
    
    def puo_attaccare(self, x_part, y_part, x_arr, y_arr, scacchiera):
        dx = abs(x_part - x_arr)
        dy = abs(y_part - y_arr)

        # Controlla se la casella di destinazione è adiacente
        if max(dx, dy) != 1:
            return False

        # Controlla se il pezzo di arrivo è alleato (non si può muovere lì)
        pezzo_arrivo = scacchiera.get_pezzo(x_arr, y_arr)
        return not (pezzo_arrivo and pezzo_arrivo.colore == self.colore)

    def mosse_possibili(self, x, y, scacchiera):
        mosse = []
        direzioni = [  # Le 8 direzioni possibili
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

        for dx, dy in direzioni:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:  # Dentro la scacchiera?
                pezzo = scacchiera.get_pezzo(nx, ny)
                if pezzo is None or pezzo.colore != self.colore:
                    mosse.append((nx, ny))
        return mosse