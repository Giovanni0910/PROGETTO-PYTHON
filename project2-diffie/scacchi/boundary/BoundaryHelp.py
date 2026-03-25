"""<<Boundary>>."""
from rich import print as rprint


class Help:
    """Una classe di supporto che fornisce informazioni sui comandi disponibili.
    
    Metodi
    -------
    print_help() -> None
        Stampa un elenco dei comandi disponibili e delle loro descrizioni.
    """

    @staticmethod
    def print_help():
        rprint("[green]Comandi disponibili:[/green]")
        rprint("[green]  gioca, /g, /gioca         - Avvia una nuova partita[/green]")
        rprint("[green]  scacchiera, /scacchiera   - Mostra la scacchiera[/green]")
        rprint("[green]  esci, /esci               - Esce dall'applicazione[/green]")
        rprint("[green]  /help                     "
        "- Mostra questo messaggio di aiuto[/green]")
        rprint("[green]  /mosse, mosse             "
        "- Mostra lo storico delle mosse[/green]")
        rprint("[green]  /abbandona, abbandona     "
        "- Permette l'uscita dalla partita[/green]")
        rprint("[green]  /patta, patta             "
        "- Permette la patta della partita[/green]")
