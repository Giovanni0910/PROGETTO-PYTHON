"""<<Control>>."""

import sys

from rich import print

from scacchi.boundary.BoundaryHelp import Help
from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.boundary.PrintScacchiera import StampatoreScacchiera
from scacchi.boundary.StampeMenu import StampeMenu
from scacchi.control.ControlArrocco import ArroccoC
from scacchi.control.ControlScacchi import ControlScacchi
from scacchi.control.MovimentoAlfiere import MovimentoAlfiere
from scacchi.control.MovimentoCavallo import MovimentoCavallo
from scacchi.control.MovimentoPedone import MovimentoPedone
from scacchi.control.MovimentoRe import MovimentoRe
from scacchi.control.MovimentoRegina import MovimentoRegina
from scacchi.control.MovimentoTorre import MovimentoTorre


class ControlPartita:
    """Gestisce il controllo e il flusso di una partita a scacchi.

    Questa classe coordina i turni dei giocatori, la gestione delle mosse, le richieste
    di patta, abbandono e uscita, oltre a verificare condizioni di scacco matto
    o stallo.
    Metodi:
        __init__(self, partita, menu_control): Inizializza la partita e i controlli.
        inizia_partita(self) -> bool: Avvia la partita e gestisce i turni.
        giocatore_turno(self) -> bool: Gestisce il turno del giocatore corrente.
        patta(self) -> bool: Gestisce la richiesta di patta tra i giocatori.
        mossa(self, scelta: str) -> bool: Applica la mossa scelta alla scacchiera.
        memorizza_mossa(self, nuova_posizione): Memorizza la mossa effettuata.
        help(self): Mostra il messaggio di aiuto.
        abbandona(self) -> bool: Gestisce la richiesta di abbandono della partita.
        conferma_uscita_applicazione(self) -> bool: Gestisce la conferma di uscita.
        scacco_matto_stallo(self): Verifica condizioni di scacco matto o stallo.
    """

    def __init__(self, partita, menu_control):
        """Inizializza la partita con due giocatori e una scacchiera."""
        self.menu_control = menu_control
        self.partita = partita
        self.stato = True

    def inizia_partita(self) -> bool:
        """Inizia la partita e gestisce i turni dei giocatori."""
        while self.partita.partita_in_corso :
            self.giocatore_turno()

            self.partita.turno = (self.partita.turno + 1) % 2
          
    def giocatore_turno(self) -> bool:
        self.stato = True
        """Gestisce il turno del giocatore corrente."""
        self.giocatore = (
            self.partita.giocatore1 
            if self.partita.turno == 0 
            else self.partita.giocatore2
        )

        nome_colore = "blue" if self.giocatore.colore.lower() == "bianco" else "red"

        PartitaB.print_turno_di(nome_colore,self.giocatore)
        
        StampatoreScacchiera.stampa(self.partita.scacchiera, self.giocatore.colore)

        ControlPartita.scacco_matto_stallo(self)
        while self.stato:
            #devo verificare se il Re puo muoversi altrimenti è scacco matto
            scelta = PartitaB.print_inserire_comando()
            if self.menu_control.parser.mossa_valida_p(scelta):
                self.stato = False
                self.mossa(scelta)
            elif self.menu_control.eseguo_comando(
                scelta, self.giocatore.nome
                ) is False:
                StampeMenu.print_scelta_errata()
                    
    def patta(self) -> bool:
        """Gestisce la richiesta di patta."""
        PartitaB.print_patta()
        richiedente = (
            self.partita.giocatore1 
            if self.partita.turno == 0 
            else self.partita.giocatore2
        )
        print(f"Patta proposta da {richiedente.nome}.")
        PartitaB.print_patta_proposta_da(richiedente)
        avversario = (
            self.partita.giocatore2 
            if self.partita.turno == 0 
            else self.partita.giocatore1
        )
        risposta = PartitaB.print_patta_richiesta(avversario, richiedente)
        if risposta.lower() == "s":
            PartitaB.print_pattaA()
            self.stato = False
            self.partita.partita_in_corso = False
            return True
        elif risposta.lower() == "n": 
            PartitaB.print_patta_r()
            return False
        else:  # Input non valido
            PartitaB.print_input_errato()

        
    def mossa(self, scelta: str) -> bool :
        """Applica la mossa alla scacchiera."""
        if scelta[0] == 'C':
            s = MovimentoCavallo.aggiorna(
                0 if self.giocatore.colore == "bianco" else 1,
                scelta,
                self.partita.scacchiera
            )
            if s is True:
                self.memorizza_mossa(scelta)

            if s is False:
                self.stato= True
            
        elif scelta[0] == 'D':
            s = MovimentoRegina.aggiorna(
                0 if self.giocatore.colore == "bianco" else 1,
                scelta,
                self.partita.scacchiera
                )
            if s is True:
                self.memorizza_mossa(scelta)

            if s is False:
                self.stato= True

        elif scelta[0] == 'T':  
            s = MovimentoTorre.aggiorna(
                0 if self.giocatore.colore == "bianco" else 1,
                scelta,
                self.partita.scacchiera
                )
            if s is True:
                self.memorizza_mossa(scelta)

            if s is False:
                self.stato= True

        elif scelta[0] == 'A':
            s = MovimentoAlfiere.aggiorna(
                0 if self.giocatore.colore == "bianco" else 1,
                scelta,
                self.partita.scacchiera
                )
            if s is True:
                self.memorizza_mossa(scelta)

            if s is False:
                self.stato= True
        elif scelta[0] == 'R':
            
            s= MovimentoRe.aggiorna(
                0 if self.giocatore.colore == "bianco" else 1,
                scelta,
                self.partita.scacchiera
                )
            if s is True:
                self.memorizza_mossa(scelta)

            if s is False:
                self.stato= True


        elif scelta[0] == '0':
            s = ArroccoC.muovi(scelta,0 if self.giocatore.colore == "bianco" else 1,
                               self.partita.scacchiera, self.partita.storico_mosse)
            if s is True:
                self.memorizza_mossa(scelta)

            if s is False:
                self.stato= True
            
        else:
            s = MovimentoPedone.aggiorna(
                0 if self.giocatore.colore == "bianco" else 1,
                scelta,
                self.partita.scacchiera
            )
            if s is True:
                self.memorizza_mossa(scelta)

            if s is False:
                self.stato= True


    def memorizza_mossa(self,nuova_posizione):
        try:
            self.partita.storico_mosse[self.giocatore.colore].append(nuova_posizione)
        except KeyError as e:
            print(f"Errore chiave: {e}")  # Verifica se la chiave esiste
        except AttributeError as e:
            print(f"Errore attributo: {e}") 

    def help(self):
        Help.print_help()
        self.stato= True

    def abbandona(self) -> bool:
        """Chiede conferma per l'abbandono della partita.
        
        Se confermato, dichiara la vittoria dell'avversario per abbandono.
        """
        while True:
            risposta = PartitaB.print_abbandona_richiesta()
            if risposta == "s":
                avversario = (
                    self.partita.giocatore2 if self.partita.turno == 0 else \
                    self.partita.giocatore1
                )
                self.stato = False
                PartitaB.print_abbandono_a(avversario)
                self.partita.partita_in_corso = False
                return True
            elif risposta == "n":
                PartitaB.print_abbandono_r()
                self.statto = True
                return False
            else:
                PartitaB.print_input_errato()

    def conferma_uscita_applicazione(self)-> bool:
        """Chiede conferma per uscire dall'applicazione.

        Se confermato, termina l'app. Altrimenti resta nel ciclo dei comandi.
        """
        while True:
            risposta = PartitaB.print_esci_conferma()
            if risposta == "s":
                PartitaB.print_chiusura()
                sys.exit(0)
            elif risposta == "n":
                PartitaB.print_annullo_usita()
                self.stato = True
                return False
            else:
                PartitaB.print_input_errato()

    
    def scacco_matto_stallo(self):
        if ControlScacchi.verifica_scacco_scacco_matto(
            self.partita.scacchiera,
            self.giocatore.colore
        ) is True :
            PartitaB.print_scacco_matto()
            self.stato = False
            self.partita.partita_in_corso = False
            self.menu_control = False
            if self.partita.turno == 0:
                PartitaB.giocatore1_perde(self.partita.giocatore1,self.partita.giocatore2) 
                return True
            else:
                PartitaB.giocatore1_vince(self.partita.giocatore1,self.partita.giocatore2)
                return True
        elif ControlScacchi.verifica_scacco_scacco_matto(
            self.partita.scacchiera,
            self.giocatore.colore
        ) == 'stallo':
            PartitaB.print_stallo()
            self.stato = False
            self.partita.partita_in_corso = False
            self.menu_control = False
            return True
        else:
            #print("ne stallo ne scacco matto")
            return False