"""<<Control>>."""
class ControlScacchiera:
    """Classe per gestire il controllo della scacchiera in un gioco di scacchi.

    Questa classe fornisce metodi per tradurre le mosse, convertire le notazioni
    in coordinate e aggiornare lo stato della scacchiera dopo un movimento.
    """

    def traduci_mossa( scelta: str):
        """Converti una mossa come ' e4' nella corrispettiva cordinata (x1, y1))."""
        try:
           # partenza, arrivo = scelta.strip().split() se ci sono due coordinate
            arrivo = scelta.strip()
            
            return (
                #ControlScacchiera.notazione_to_posizione(partenza),
                ControlScacchiera.notazione_to_posizione(arrivo)

            )
        except Exception:
            print("Formato della mossa non valido. Usa ad esempio 'e2 e4'.")

    def notazione_to_posizione( notazione: str):
        """Convert 'la scelta' into the corresponding coordinate (x, y)."""  
        colonne = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        riga = int(notazione[1]) - 1
        colonna = colonne[notazione[0].lower()]

        return colonna, riga
    
    @staticmethod
    def posizione_to_notazione(x: int, y: int) -> str:
        """Convert coordinates (x, y) into Italian notation (e.g., (0,0) -> 'a1')."""
        colonne = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] #converte la x nella colonna
        righe = ['1', '2', '3', '4', '5', '6', '7', '8'] #coverte la y=0 nella riga
        return colonne[x] + righe[y]



        
        
