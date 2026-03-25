"""<<<Entity>>>."""

class Giocatore:
    """Rappresenta un giocatore di scacchi.

    Attributi
    ----------
    nome : str
        Il nome del giocatore.
    colore : str
        Il colore dei pezzi del giocatore (bianco o nero).
    """

    def __init__(self, nome: str, colore: str):
        self.nome = nome
        self.colore = colore

    def __str__(self) -> str:
        """Restituisce una rappresentazione in stringa del giocatore."""
        return f"Giocatore {self.nome} ({self.colore})"
    