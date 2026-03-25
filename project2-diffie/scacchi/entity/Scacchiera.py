from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Regina import Regina
from scacchi.entity.Torre import Torre


class Scacchiera:
    """Rappresenta una scacchiera per il gioco degli scacchi.

    Attributi:
        caselle (list[list[Optional[object]]]): Una matrice 8x8 che rappresenta le 
        caselle della scacchiera.
            Ogni casella può contenere un oggetto rappresentante un pezzo 
            degli scacchi o None se la casella è vuota.
    Metodi:
        __init__():
            Inizializza una nuova scacchiera vuota e posiziona i 
            pezzi nella configurazione iniziale.
        inizializza():
            Posiziona i pezzi degli scacchi nella configurazione iniziale standard.
        get_pezzo(x: int, y: int):
            Restituisce il pezzo presente nella casella specificata.
            Parametri:
                x (int): La colonna della casella (0-7).
                y (int): La riga della casella (0-7).
            Ritorna:
                object o None: Il pezzo presente nella casella o 
                None se la casella è vuota.
        set_pezzo(x: int, y: int, pezzo):
            Imposta un pezzo nella casella specificata.
            Parametri:
                x (int): La colonna della casella (0-7).
                y (int): La riga della casella (0-7).
                pezzo (object): Il pezzo da posizionare nella casella.
    """

    def __init__(self):
        self.caselle = [[None for _ in range(8)] for _ in range(8)]
        self.inizializza()
        #self.en_passant_target = None

    def inizializza(self):
        # Inizializza i pezzi come oggetti
        # Bianchi (righe 0 e 1)
        self.caselle[0] = [
            Torre(colore="bianco"),
            Cavallo(colore="bianco"),
            Alfiere(colore="bianco"),
            Regina(colore="bianco"),
            Re(colore="bianco"),
            Alfiere(colore="bianco"),
            Cavallo(colore="bianco"),
            Torre(colore="bianco")
        ]
        
        for x in range(8):
            self.caselle[1][x] = Pedone(colore="bianco")

        # Neri (righe 7 e 6)
        self.caselle[7] = [
            Torre(colore="nero"),
            Cavallo(colore="nero"),
            Alfiere(colore="nero"),
            Regina(colore="nero"),
            Re(colore="nero"),
            Alfiere(colore="nero"),
            Cavallo(colore="nero"),
            Torre(colore="nero")
        ]
        
        for x in range(8):
            self.caselle[6][x] = Pedone(colore="nero")

    def get_pezzo(self, x: int, y: int):
        return self.caselle[y][x]
        # Restituisce il pezzo presente nella casella specificata
    def set_pezzo(self, x: int, y: int, pezzo):
        self.caselle[y][x] = pezzo