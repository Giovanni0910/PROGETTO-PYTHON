"""<<Entity>>."""

class Pezzo:
    """Rappresenta un pezzo generico nel gioco degli scacchi.

    Attributi
    ---------
    colore : str
        Il colore del pezzo ('bianco' o 'nero').
    
    """

    def __init__(self, colore):
        self.colore = colore  # 'bianco' o 'nero'

    def __str__(self):
        """Restituisce una rappresentazione testuale del pezzo.

        Indica il colore del pezzo.
        """
        return f"Pezzo di colore {self.colore}"
    
    def puo_attaccare(self, x_part, y_part, x_arr, y_arr, scacchiera):
        """Metodo da implementare nelle sottoclassi.

        Deve restituire True se il pezzo può attaccare la posizione (x_arr, y_arr).
        """
        raise NotImplementedError(
            "Devi implementare puo_attaccare nelle sottoclassi di Pezzo"
        )
    
    def mosse_possibili(self, x, y, scacchiera):
        """Restituisce la lista delle posizioni a cui il pezzo può muoversi  (x, y)."""
        pass