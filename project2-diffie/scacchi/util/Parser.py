# classe per il parsing dei comandi del menu all'interno del pacchetto scacchi.util

import re


class CommandParser:
    """Parser di comandi per un'interfaccia scacchistica testuale.

    Gestisce il riconoscimento e la validazione di comandi e mosse in notazione
    algebrica.

    Metodi:
        - valido(comando: str) -> bool:
            Verifica se il comando è tra quelli validi.
        - comando_gioca_p(comando: str) -> bool:
            Riconosce i comandi per iniziare una partita.
        - comando_scacchiera_p(comando: str) -> bool:
            Riconosce i comandi per mostrare la scacchiera.
        - comando_esci_p(comando: str) -> bool:
            Riconosce i comandi per uscire dal programma.
        - comando_help_p(comando: str) -> bool:
            Riconosce il comando di aiuto.
        - comando_patta_p(comando: str) -> bool:
            Riconosce i comandi per proporre la patta.
        - comando_mosse_p(comando: str) -> bool:
            Riconosce i comandi per mostrare le mosse.
        - comando_abbandona_p(comando: str) -> bool:
            Riconosce i comandi per abbandonare la partita.
        - mossa_valida_p(movimento: str) -> bool:
            Verifica se una mossa è valida in notazione algebrica.
        - scelta (property):
            Restituisce o imposta la scelta dell'utente.
    """

    COMANDI_VALIDI = [
        'gioca', '/g', '/gioca',
        'scacchiera', '/scacchiera',
        'esci', '/esci',
        '/help',
        'patta', '/patta',
        'mosse', '/mosse',
        'abbandona', '/abbandona',
    ]

    MOVIMENTO_NOTAZIONE_ALGEBRICA = re.compile(
      r"""^(?:0-0(?:-0)?)|(?:(?:[RDTAC])?)(?:[a-h]?[1-8]?)[x:]?[a-h][1-8](?:=?[DTAC])?[+#]?$"""


    )  

    def valido(self, comando: str) -> bool:
        """Controlla se il comando è valido."""
        return comando in self.COMANDI_VALIDI

    def comando_gioca_p(self, comando: str) -> bool:
        return comando in ['gioca', '/g', '/gioca']

    def comando_scacchiera_p(self, comando: str) -> bool:
        return comando in ['scacchiera', '/scacchiera']

    def comando_esci_p(self, comando: str) -> bool:
        return comando in ['esci', '/esci']

    def comando_help_p(self, comando: str) -> bool:
        return comando in ['/help']
    def comando_patta_p(self, comando: str) -> bool:
        return comando in ['patta', '/patta']
    def comando_mosse_p(self, comando: str) -> bool:
        return comando in ['mosse', '/mosse']
    def comando_abbandona_p(self, comando: str) -> bool:
        return comando in ['abbandona', '/abbandona']
    def mossa_valida_p(self, movimento: str) -> bool:
        """Controlla se il movimento è valido."""
        return bool(self.MOVIMENTO_NOTAZIONE_ALGEBRICA.match(movimento))

    @property
    def scelta(self):
        """Restituisce la scelta dell'utente."""
        return self._scelta
    @scelta.setter
    def scelta(self, value):
        """Imposta la scelta dell'utente."""
        self._scelta = value
