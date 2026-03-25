"""<<Control>>."""

from scacchi.boundary.StampeMenu import StampeMenu
from scacchi.control.ControlMenu import MenuControl


class InizioC:
    """Gestisce l'interfaccia utente del menu principale dell'applicazione.

    Metodi:
    init__(player_name): inizializza il nome del giocatore e il controller del menu.
    get_command(): legge un comando valido da input.
    run(): avvia il ciclo del menu finché l’utente non inserisce esci o /esci
    """

    def __init__(self, nome_giocatore):
        self.nome_giocatore = nome_giocatore
        self.menu_control = MenuControl()

    def get_command(self):
        """Ottiene il comando dall'utente."""
        while True:
            command = StampeMenu.print_avvio_gioco()
            if command:  # Se l'utente ha inserito qualcosa
                return command
            print("Per favore inserisci un comando valido")

    def run(self):
        """Esegue il loop principale del menu."""
        while True:
            command = self.get_command()
            self.menu_control.eseguo_comando(command, self.nome_giocatore)
            if command in ('esci', '/esci'):
                StampeMenu.print_uscita_dal_gioco()
                break
