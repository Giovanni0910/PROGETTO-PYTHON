"""<<Boundary>>."""
class StampatoreScacchiera:
    """Classe per la stampa della scacchiera con orientamento e simboli corretti.

    Gestisce la visualizzazione della scacchiera a seconda del turno e del colore.
    Metodi:
        - stampa(scacchiera, turno_colore): Stampa la scacchiera con numeri e lettere
          orientati in base al colore del turno.
        - _get_simbolo(pezzo, colore): Restituisce il simbolo Unicode del pezzo in base
          al tipo e al colore.
    """
    
    @staticmethod
    def stampa(scacchiera, turno_colore):
        """Stampa la scacchiera con orientamento e numeri corretti."""
        inverti = turno_colore.lower() == "nero"
        
        # Intestazione colonne
        colonne = "   A   B   C   D   E   F   G   H"
        if inverti:
            colonne = "   H   G   F   E   D   C   B   A"
        print(colonne)
        print("  "+"+---" * 8 + "+")

        # Stampa righe (visual_row 0=top, 7=bottom)
        for visual_row in range(8):
            if not inverti:
                # turno bianchi: 1 in basso, 8 in alto
                logic_row = 7 - visual_row
                cols = range(8)
                num_riga = 8 - visual_row
            else:
                # turno neri: 8 in basso, 1 in alto, matrice capovolta
                logic_row = visual_row
                cols = range(7, -1, -1)
                num_riga = visual_row + 1

            riga = []
            for visual_col in cols:
                logic_col = visual_col if not inverti else visual_col
                pezzo = scacchiera.get_pezzo(logic_col, logic_row)

                if pezzo:
                    simbolo = StampatoreScacchiera._get_simbolo(pezzo, pezzo.colore)
                    colore_ansi = (
                        '\033[1;97m' if pezzo.colore == "bianco" else '\033[0;30m'
                    )
                    riga.append(f"{colore_ansi}{simbolo}\033[0m")
                else:
                    riga.append(" ")

            print(f"{num_riga} | {' | '.join(riga)} | {num_riga}")
            print("  "+"+---" * 8 + "+")

        print(colonne)

    @staticmethod
    def _get_simbolo(pezzo, colore):
        """Restituisce il simbolo Unicode corretto per tipo e colore."""
        simboli = {
            'pedone': {'bianco': '♙', 'nero': '♟'},
            'torre': {'bianco': '♖', 'nero': '♜'},
            'cavallo': {'bianco': '♘', 'nero': '♞'},
            'alfiere': {'bianco': '♗', 'nero': '♝'},
            'regina': {'bianco': '♕', 'nero': '♛'},
            're': {'bianco': '♔', 'nero': '♚'}
        }
        return simboli[pezzo.tipo][colore]