"""<<Boundary>>."""

from rich import print as rprint


class PartitaB:
    """Gestisce l'interfaccia testuale della partita a scacchi.

    Questa classe fornisce metodi per stampare messaggi, richieste e notifiche 
    relative allo svolgimento di una partita a scacchi, inclusi input da parte 
    dell'utente e visualizzazione dello storico delle mosse.
    Metodi:
        __init__(): Inizializza un'istanza della classe PartitaB.
        print_turno_di(nome_colore, giocatore): Mostra il turno del giocatore.
        print_inserire_comando() -> str: Richiede l'inserimento di un comando o mossa.
        print_patta(): Notifica la ricezione di una richiesta di patta.
        print_patta_a(): Comunica che la patta è stata accettata.
        print_patta_r(): Comunica che la patta è stata rifiutata.
        print_casella_occupata(): Segnala che la casella è occupata.
        print_mossa_negata(): Segnala che la mossa del pedone non è consentita.
        print_mossa_negata2(): Segnala che la mossa non è consentita.
        print_patta_richiesta(avversario, richiedente) -> str:
            Chiede se accettare la patta.
        print_patta_proposta_da(richiedente): Notifica una proposta di patta.
        print_input_errato(): Segnala risposta non valida.
        print_mossa_negata3(): Segnala che non si può scavalcare.
        print_chiusura(): Comunica la chiusura dell'applicazione.
        stampa_storico(partita): Stampa lo storico delle mosse.
        print_cattura_non_specificata(): Richiede di specificare la cattura.
        print_cattura_negata2(dest_str): Segnala che non c'è un pezzo da catturare.
        print_ambiguità(): Richiede di specificare colonna o riga.
        print_mossa_cavallo_ambiguità_non_valida(): Segnala ambiguità sul cavallo.
        print_abbandono_r(): Notifica annullamento dell'abbandono.
        print_abbandono_a(avversario): Comunica vittoria per abbandono.
        print_abbandona_richiesta() -> str: Chiede conferma per abbandonare.
        print_esci_conferma(): Chiede conferma per uscire dall'applicazione.
        print_movimento_re_errato(): Segnala movimento illegale del re.
        print_movimento_re_negato(): Segnala che la casella del re è minacciata.
        print_re_minacciato(): Notifica che il re è sotto scacco.
        print_scacco_matto_non_valido(): Segnala scacco matto non valido.
        print_scacco_non_valido(): Segnala scacco non valido.
        print_scacco_non_indicato(): Segnala scacco non dichiarato.
        print_scacco_matto_non_indicato(): Segnala scacco matto non dichiarato.
        print_mossa_illegale(): Segnala mossa illegale.
        print_mossa_torre_ambiguità_non_valida(): Segnala ambiguità sulla torre.
        print_mossa_regina_ambiguità_non_valida(): Segnala ambiguità sulla regina.
        promozione_non_specificata(): Segnala promozione non indicata.
        promozione(turno): Notifica promozione del pedone.
        promozione_non_valida(): Segnala promozione non valida.
        colonna_riga_inidcata_errata(): Segnala colonna o riga errata.
        giocatore1_vince(giocatore1, giocatore2): Comunica la vittoria di un giocatore.
        giocatore1_perde(giocatore1, giocatore2): Comunica la sconfitta di un giocatore.
        print_stallo(): Notifica lo stallo.
        print_scacco_matto(): Notifica lo scacco matto.
        print_annullo_usita(): Notifica annullamento dell'uscita.
    """

    def __init__(self):
        """Inizializza un'istanza della classe Partita_B."""    
    def print_turno_di(nome_colore, giocatore):
        rprint(
            f"Turno di [{nome_colore}]{giocatore.nome}[/{nome_colore}] "
            f"({giocatore.colore})"
        )

    def print_inserire_comando()-> str:
         return input(
                "inserisci un comando o una mossa "
            )
    def print_patta():
        print("Richiesta di patta ricevuta.")

    def print_patta_a():
        print("Patta accettata. La partita termina in pareggio.")

    def print_patta_r():
        print("Patta rifiutata.")
    
    def print_casella_occupata():
        print("mossa non consentita, la casella è occupata")

    def print_mossa_negata():
        print(
            "mossa errata. il pedone può muoversi solo di 1 cella "
            "o di 2 in avanti se è il suo primo movimento"
        )
    
    def print_mossa_negata2():
        print("mossa non consentita.")

    def print_patta_richiesta(avversario, richiedente)->str:
        return input(
            f"{avversario.nome}, vuoi accettare la patta da "
            f"{richiedente.nome}? (s/n): "
        )
    def print_patta_proposta_da(richiedente):
         print(f"Patta proposta da {richiedente.nome}.")
    
    def print_input_errato():
        print("Risposta non valida. Inserisci 's' per sì o 'n' per no.")

    def print_mossa_negata3():
        print("mossa non consentita, non si può scavalcare")
    #metodo che stampa le mosse effettuate dal giocatore
    @staticmethod
    
    def print_chiusura():
        print("Chiusura dell'applicazione in corso...")
        
    def stampa_storico(partita):
        """Stampa lo storico delle mosse per un giocatore."""
        if not partita.storico_mosse.get("bianco"):
            print("Non hai effettuato alcuna mossa")
        else:
            for i in range(len(partita.storico_mosse["bianco"])):
                # Stampa numero mossa
                print(f"{i+1}.", end=' ')
                
                # Stampa mossa bianco
                mossa_b = partita.storico_mosse["bianco"][i]
                if isinstance(mossa_b, tuple):
                    # Per mosse in formato tupla: stampa partenza e arrivo
                    print(f"{mossa_b[0]}{mossa_b[1]}", end=' ')
                else:
                    # Per stringhe (mosse di pezzi): stampa l'intera stringa
                    print(mossa_b, end=' ')
                
                # Stampa mossa nero se esiste
                if i < len(partita.storico_mosse["nero"]):
                    mossa_n = partita.storico_mosse["nero"][i]
                    if isinstance(mossa_n, tuple):
                        # Uso rich.print con markup disattivato per evitare che 
                        # combinazioni di caratteri 
                        # nella mossa vengano interpretate come comandi 
                        # di formattazione e stampate con colori indesiderati.
                        rprint(f"{mossa_n[0]}{mossa_n[1]}", end=' ', markup=False)
                    else:
                        print(mossa_n, end=' ')
                print()  # A capo dopo ogni coppia
    
    def print_cattura_non_specificata():
        print("Devi specificare la cattura con 'x' (es. Cxb5)")

    def print_cattura_negata2(dest_str):
        print("Non c'è un pezzo da catturare in " + dest_str)

    def print_ambiguità():
        print("Ambiguità: specificare colonna o riga (es. Cbd5 o C3d5)")

    def print_mossa_cavallo_ambiguità_non_valida():
        print("Mossa non valida! " \
                    "Nessun cavallo è presente in quella posizione")

    def print_abbandono_r():
        print("Hai annullato l'abbandono.")
    
    def print_abbandono_a(avversario)->str:
        print(f"{avversario.nome} ha vinto per abbandono dell'avversario.")
        
    def print_abbandona_richiesta()->str:
        return input(
            "Sei sicuro di voler abbandonare la partita? (s/n): "
        ).strip().lower()

    def print_esci_conferma():
        return input(
            "Sei sicuro di voler uscire dall'applicazione? (s/n): "
        ).strip().lower()
    def print_movimento_re_errato():
        print("Mossa illegale: il re può muoversi solo di una casella")

    def print_movimento_re_negato():
        print("Mossa illegale: la casella è minacciata")
    
    def print_re_minacciato():
        print("RE SOTTO SCACCO (mossa illegale)")

    def print_scacco_matto_non_valido():
        print("SCACCO MATTO NON VALIDO (il Re avversario non è matto)")
    
    def print_scacco_non_valido():
        print("SCACCO NON VALIDO (il Re avversario non è minacciato)")

    def print_scacco_non_indicato():
        print("SCACCO NON DICHIARATO (mossa illegale)")

    def print_scacco_matto_non_indicato():
        print("SCACCO MATTO NON DICHIARATO (mossa illegale)")

    def print_mossa_illegale():
        print("mossa illegale")

    def print_mossa_torre_ambiguità_non_valida():
        print("Mossa non valida! " \
                    "Nessun torre è presente in quella posizione")
        
    def print_mossa_regina_ambiguità_non_valida():
        print("Mossa non valida! " \
                    "Nessun regina è presente in quella posizione")
        
    def promozione_non_specificata():
        print("promozione non indicata")

    def promozione(turno):
        print(f"Promozione Pedone {'Bianco' if turno == 0 else 'Nero'}!")

    def promozione_non_valida():
        print("Promozione non valida (lettera sbagliata). Riprova.")

    def colonna_riga_inidcata_errata():
        print("colonna o riga indicata errata")
        
    def giocatore1_vince(giocatore1, giocatore2):
        print(giocatore2, "ha perso\n", giocatore1, "ha vinto") 

    def giocatore1_perde(giocatore1, giocatore2):
        print(giocatore1, "ha perso\n", giocatore2, "ha vinto") 
    
    def print_stallo():
        print("stallo , la partita finisce con la patta")

    def print_scacco_matto():
        print("Scacco Matto")

    def print_annullo_usita():
        print("Hai annullato l'uscita. Puoi inserire un nuovo comando.")

    def print_mossa_non_valida():
        print("Mossa non valida. Riprova con una mossa corretta.")

    def print_tentativo_arrocco_corto():
        print("Tentativo di arrocco corto non valido. Riprova.")
    
    def print_tentativo_arrocco_lungo():
        print("Tentativo di arrocco lungo non valido. Riprova.")