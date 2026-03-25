"""<<Control>>."""
from scacchi.boundary.BoundaryHelp import Help
from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.boundary.PrintScacchiera import StampatoreScacchiera
from scacchi.boundary.StampeMenu import StampeMenu
from scacchi.control.ControlPartita import ControlPartita
from scacchi.entity.Partita import Partita
from scacchi.util.Parser import CommandParser


class MenuControl:
    """Controlla le interazioni del menu per il gioco degli scacchi.

    Questa classe gestisce i comandi degli utenti, controlla lo stato del gioco 
    e forniscefunzionalità per iniziare una partita, 
    visualizzare la scacchiera e uscire dal programma.
    """

    def __init__(self):
        self.parser = CommandParser()  #  parser
        self.Partita_Attiva = False

    def eseguo_comando(self, comando, nome_giocatore)-> bool:
        """Esegue azioni in base al comando."""
        if not self.parser.valido(comando):
            StampeMenu.print_comando_valido()    
            return False
        if self.parser.comando_gioca_p(comando):
            self.gioca_partita(nome_giocatore)
        elif self.parser.comando_scacchiera_p(comando):
            self.print_scacchiera()
        elif self.parser.comando_help_p(comando):
            self.comando_help()
        elif self.parser.comando_esci_p(comando):
            self.exit()
        elif self.parser.comando_patta_p(comando):
            self.comando_patta()
        elif self.parser.comando_mosse_p(comando):
            self.comando_mossa()
        elif self.parser.comando_abbandona_p(comando):
            self.comando_abbandona()
        elif self.parser.mossa_valida_p(comando):
            return True
            # controllo se la mossa è valida
            #self.movimento_valido(comando)
        
    def comando_help(self) -> bool:
        if self.Partita_Attiva is False:
            Help.print_help()
        else:
            self.control.help()

    def gioca_partita(self, nome_giocatore) -> bool:
        if not self.Partita_Attiva:
            self.Partita_Attiva = True
            StampeMenu.stampa_gioco()
            name1 = StampeMenu.print_inserimento_giocatore2()
            partita = Partita(nome_giocatore, name1, self.Partita_Attiva)
            self.control = ControlPartita(partita, self)
            self.control.inizia_partita()
            self.Partita_Attiva = False
        else:
            StampeMenu.print_gioco_in_corso()

    def print_scacchiera(self):
            if not self.Partita_Attiva : 
                StampeMenu.stampa_scacchiera_negata()
            else:
                StampeMenu.stampa_scacchiera()
                # Recupera scacchiera e turno dalla partita attiva
                scacchiera = self.control.partita.scacchiera
                turno_colore = self.control.partita.turno_colore
                StampatoreScacchiera.stampa(scacchiera, turno_colore)

    def comando_patta(self) -> bool:
        if self.Partita_Attiva is False:
            StampeMenu.print_patta_non_concessa()
        else:
            if self.control.patta() is True:
                #accetta patta
                ControlPartita.stato = False
                self.Partita_Attiva = False
                
    """def movimento_valido(self, move) -> bool:
        #Controlla se il movimento è valido.
        if self.parser.valido(move):
            print("Movimento valido.")
            return True
        else:
            print("Movimento non valido.")
            return False"""
        
    def comando_mossa(self) -> bool:
        if not self.Partita_Attiva:
            print("Nessuna partita in corso")
        else:    
            PartitaB.stampa_storico(self.control.partita)

    def comando_abbandona(self) -> bool:
        if self.Partita_Attiva is False:
            StampeMenu.print_abbandona_non_concessa() #caso in cui no partita attiva
            ControlPartita.stato = False
        else:
            #caso in cui c'è partita attiva
            if self.control.abbandona() is True: 
                ControlPartita.stato = False
                self.Partita_Attiva = False
    
    def exit(self) -> bool:
        if self.Partita_Attiva is False: #caso in cui non c'è partita attiva
            PartitaB.print_chiusura()
            exit(0)
            #caso in cui c'è partita attiva 
        else:
            self.control.conferma_uscita_applicazione()
                
