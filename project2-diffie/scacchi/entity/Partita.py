"""<<Entity>>."""

import random

from scacchi.entity.Giocatore import Giocatore
from scacchi.entity.Scacchiera import Scacchiera


class Partita:
    """Rappresenta una partita di scacchi tra due giocatori.

    La partita gestisce il turno dei giocatori e la scacchiera.
    """

    def __init__(
        self, giocatore1_nome, giocatore2_nome, partita_in_corso,
    ):
        """Inizializza la partita con due giocatori e una scacchiera."""
        self.scacchiera = Scacchiera()
        #Dizionario con lo storico mosse
        self.storico_mosse = {
            "bianco": [],
            "nero": []
        }
        colori = ["bianco", "nero"]
        random.shuffle(colori)
        self.giocatore1 = Giocatore(giocatore1_nome, colori[0].lower())
        self.giocatore2 = Giocatore(giocatore2_nome, colori[1].lower())
        self.turno = (
            0 if colori[0] == "bianco" else 1
        )  # 0 per il giocatore 1, 1 per il giocatore 2
        self.partita_in_corso = partita_in_corso


    @property
    def turno_colore(self):
        """Restituisce il colore del giocatore di turno.
        
        'bianco' se è il turno del giocatore con i pezzi bianchi,
        'nero' se è il turno del giocatore con i pezzi neri.
        """
        return self.giocatore1.colore if self.turno == 0 else self.giocatore2.colore