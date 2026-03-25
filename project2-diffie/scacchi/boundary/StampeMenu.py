"""<<Boundary>>."""

class StampeMenu:
    """contiene metodi per stampare vari messaggi per il gioco degli scacchi.

    Metodi
    -------
    stampaGioco(): Stampa un messaggio che indica che non c'è nessuna partita in 
    corso e avvia una nuova partita.
    stampa_show_board(): Stampa un messaggio che indica che non c'è nessuna 
    partita in corso e suggerisce di avviare una nuova partita.
    stampa_show_board1(): Stampa la scacchiera.
    print_scelta_errata(): Stampa un messaggio per un comando o mossa non valida.
    print_scelta_corretta(): Stampa un messaggio per un comando eseguito correttamente.
    """ 

    def stampa_gioco():
        """Stampa un messaggio che indica che non c'è una partita in corsa."""
        print("Nessuna partita in corso. Inizio una nuova partita.")

    def stampa_scacchiera_negata():
        """Stampa un messaggio che indica che non c'è una partita in cors."""
        print(
            "Nessuna partita in corso. Non posso mostrare la scacchiera."
            "Inizio una nuova partita con /gioca"
        )
    def stampa_scacchiera():
        print("Scacchiera degli scacchi:")

    def print_scelta_errata():
        print("Comando o mossa non valida. Riprova.")
        
    def print_scelta_corretta():
        print("Comando eseguito con successo.")
    
    def print_comando_valido():
        print("Comando non valido.") 

    def print_gioco_in_corso():
        print("Partita già in corso. Non puoi iniziarne una nuova.")

    def print_inserimento_giocatore2()-> str:
        return input("Inserisci il nome del giocatore 2: ")
    
    def print_abbandona_non_concessa():
        print("non puoi abbandonare , non c'è nessuna partita attiva.")
        
    def print_patta_non_concessa():
        print(" non puoi richedere la patta, nessuna partita in corso")

    def print_uscita_dal_gioco():
        print("Uscita dal gioco.")

    def print_avvio_gioco():
        return input(
                "Inserisci un comando (es. gioca, scacchiera, esci): "
            ).strip().lower()