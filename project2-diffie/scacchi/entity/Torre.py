"""<<Entity>>."""
from scacchi.entity.Pezzo import Pezzo


class Torre(Pezzo):
    """Rappresenta una Torre nel gioco degli scacchi.

    La Torre può muoversi in linea retta orizzontalmente o verticalmente
    sulla scacchiera, senza limitazioni di distanza, a meno che non ci siano
    ostacoli lungo il percorso.
    """

    def __init__(self, colore):
        super().__init__(colore)
        self.tipo = "torre"

    def __str__(self):
        """Ritorna il colore della Torre."""
        return f"Torre di colore {self.colore}"
    
    def mosse_possibili(self, x, y, scacchiera):
        mosse = []
        direzioni = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Su, giù, sinistra, destra

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

    
    def puo_attaccare(self, x_part, y_part, x_arr, y_arr, scacchiera):
        # Se la Torre prova a "attaccare" la sua stessa casella
        if x_part == x_arr and y_part == y_arr:
            return False

        # Controlla se la casella di arrivo ha un pezzo alleato (non può attaccarlo)
        pezzo_arrivo = scacchiera.get_pezzo(x_arr, y_arr)
        if pezzo_arrivo and pezzo_arrivo.colore == self.colore:
            return False

        # Controllo movimento rettilineo (orizzontale o verticale)
        if x_part == x_arr:  # Movimento verticale
            step = 1 if y_arr > y_part else -1
            for y in range(y_part + step, y_arr, step):
                if scacchiera.get_pezzo(x_part, y):
                    return False
            return True
        elif y_part == y_arr:  # Movimento orizzontale
            step = 1 if x_arr > x_part else -1
            for x in range(x_part + step, x_arr, step):
                if scacchiera.get_pezzo(x, y_part):
                    return False
            return True

        return False