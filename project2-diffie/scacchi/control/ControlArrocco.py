import re

from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.ControlScacchi import ControlScacchi
from scacchi.control.MovimentoRe import MovimentoRe
from scacchi.entity.Re import Re
from scacchi.entity.Torre import Torre


class ArroccoC:
    """Classe che permette al re di effettuare l'arrocco."""

    def muovi(mossa, giocatore, scacchiera, mosse: dict[str, list[str]]):
        re_arrocco_corto = r"^0-0[+#]?$"
        re_arrocco_lungo = r"^0-0-0[+#]?$"

        try:
            # Usa fullmatch per entrambi i casi per consistenza
            if re.fullmatch(re_arrocco_corto, mossa):
                PartitaB.print_tentativo_arrocco_corto()
                return ArroccoC.arrocco_corto(giocatore, scacchiera, mosse, mossa)
                    
            elif re.fullmatch(re_arrocco_lungo, mossa):
                PartitaB.print_tentativo_arrocco_lungo()
                return ArroccoC.arrocco_lungo(giocatore, scacchiera, mosse, mossa)
            else:
                PartitaB.print_mossa_non_valida()
                return False
        except Exception as e:
            print(f"Errore durante l'arrocco: {str(e)}")
            return False

    def arrocco_corto(giocatore, scacchiera, mosse: dict[str, list[str]], mossa):
        # Pattern per riconoscere se è stato dichiarato scacco o scacco matto
        pattern_scacco = r"^0-0[+#]$"
        scacco_dichiarato = re.fullmatch(pattern_scacco, mossa) is not None
        
        if giocatore == 1:  # Nero
            if ArroccoC.arrocco_corto_applicabile(giocatore, scacchiera, mosse):
                # Salva le posizioni originali
                torre = scacchiera.get_pezzo(7, 7)
                king = scacchiera.get_pezzo(4, 7)
                
                # Esegui l'arrocco
                scacchiera.set_pezzo(7, 7, None)
                scacchiera.set_pezzo(4, 7, None)
                scacchiera.set_pezzo(6, 7, king)
                scacchiera.set_pezzo(5, 7, torre)
                
                # Verifica se l'arrocco mette sotto scacco l'avversario
                colore_avversario = "bianco"
                re_avversario_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, 
                                                                            colore_avversario)
                
                if re_avversario_sotto_scacco and not scacco_dichiarato:
                    PartitaB.print_scacco_non_indicato()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(7, 7, torre)
                    scacchiera.set_pezzo(4, 7, king)
                    scacchiera.set_pezzo(6, 7, None)
                    scacchiera.set_pezzo(5, 7, None)
                    return False
                elif not re_avversario_sotto_scacco and scacco_dichiarato:
                    PartitaB.print_scacco_non_valido()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(7, 7, torre)
                    scacchiera.set_pezzo(4, 7, king)
                    scacchiera.set_pezzo(6, 7, None)
                    scacchiera.set_pezzo(5, 7, None)
                    return False
                else:
                    return True
            else:
                raise Exception("Arrocco corto non " \
                "eseguibile il re o la torre è stata mossa")
                
        elif giocatore == 0:  # Bianco
            if ArroccoC.arrocco_corto_applicabile(giocatore, scacchiera, mosse):
                # Salva le posizioni originali
                torre = scacchiera.get_pezzo(7, 0)
                king = scacchiera.get_pezzo(4, 0)
                
                # Esegui l'arrocco
                scacchiera.set_pezzo(7, 0, None)
                scacchiera.set_pezzo(4, 0, None)
                scacchiera.set_pezzo(6, 0, king)
                scacchiera.set_pezzo(5, 0, torre)
                
                # Verifica se l'arrocco mette sotto scacco l'avversario
                colore_avversario = "nero"
                re_avversario_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, 
                                                                            colore_avversario)
                
                if re_avversario_sotto_scacco and not scacco_dichiarato:
                    PartitaB.print_scacco_non_indicato()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(7, 0, torre)
                    scacchiera.set_pezzo(4, 0, king)
                    scacchiera.set_pezzo(6, 0, None)
                    scacchiera.set_pezzo(5, 0, None)
                    return False
                elif not re_avversario_sotto_scacco and scacco_dichiarato:
                    PartitaB.print_scacco_non_valido()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(7, 0, torre)
                    scacchiera.set_pezzo(4, 0, king)
                    scacchiera.set_pezzo(6, 0, None)
                    scacchiera.set_pezzo(5, 0, None)
                    return False
                else:
                    return True
            else:
                raise Exception("Arrocco corto non " \
                "eseguibile il re o la torre è stata mossa")
        else:
            raise ValueError("Parametro giocatore non valido.")

    @staticmethod
    def arrocco_lungo(giocatore, scacchiera, mosse: dict[str, list[str]], mossa):
        # Pattern per riconoscere se è stato dichiarato scacco o scacco matto
        pattern_scacco = r"^0-0-0[+#]$"
        scacco_dichiarato = re.fullmatch(pattern_scacco, mossa) is not None

        if giocatore == 1:  # Nero
            if ArroccoC.arrocco_lungo_applicabile(giocatore, scacchiera, mosse):
                # Salva le posizioni originali
                torre = scacchiera.get_pezzo(0, 7)
                king = scacchiera.get_pezzo(4, 7)
                
                # Esegui l'arrocco
                scacchiera.set_pezzo(0, 7, None)
                scacchiera.set_pezzo(4, 7, None)
                scacchiera.set_pezzo(2, 7, king)
                scacchiera.set_pezzo(3, 7, torre)
                
                # Verifica se l'arrocco mette sotto scacco l'avversario
                colore_avversario = "bianco"
                re_avversario_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, 
                                                                            colore_avversario)
                
                if re_avversario_sotto_scacco and not scacco_dichiarato:
                    PartitaB.print_scacco_non_indicato()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(0, 7, torre)
                    scacchiera.set_pezzo(4, 7, king)
                    scacchiera.set_pezzo(2, 7, None)
                    scacchiera.set_pezzo(3, 7, None)
                    return False
                elif not re_avversario_sotto_scacco and scacco_dichiarato:
                    PartitaB.print_scacco_non_valido()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(0, 7, torre)
                    scacchiera.set_pezzo(4, 7, king)
                    scacchiera.set_pezzo(2, 7, None)
                    scacchiera.set_pezzo(3, 7, None)
                    return False
                else:
                    return True
            else:
                raise Exception("Arrocco lungo non eseguibile, " \
                "il re o la torre è stata mossa")
                
        elif giocatore == 0:  # Bianco
            if ArroccoC.arrocco_lungo_applicabile(giocatore, scacchiera, mosse):
                # Salva le posizioni originali
                torre = scacchiera.get_pezzo(0, 0)
                king = scacchiera.get_pezzo(4, 0)
                
                # Esegui l'arrocco
                scacchiera.set_pezzo(0, 0, None)
                scacchiera.set_pezzo(4, 0, None)
                scacchiera.set_pezzo(2, 0, king)
                scacchiera.set_pezzo(3, 0, torre)
                
                # Verifica se l'arrocco mette sotto scacco l'avversario
                colore_avversario = "nero"
                re_avversario_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, 
                                                                            colore_avversario)
                
                if re_avversario_sotto_scacco and not scacco_dichiarato:
                    PartitaB.print_scacco_non_indicato()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(0, 0, torre)
                    scacchiera.set_pezzo(4, 0, king)
                    scacchiera.set_pezzo(2, 0, None)
                    scacchiera.set_pezzo(3, 0, None)
                    return False
                elif not re_avversario_sotto_scacco and scacco_dichiarato:
                    PartitaB.print_scacco_non_valido()
                    # Annulla l'arrocco
                    scacchiera.set_pezzo(0, 0, torre)
                    scacchiera.set_pezzo(4, 0, king)
                    scacchiera.set_pezzo(2, 0, None)
                    scacchiera.set_pezzo(3, 0, None)
                    return False
                else:
                    return True
            else:
                raise Exception("Arrocco lungo non eseguibile, " \
                "il re o la torre è stata mossa")
        else:
            raise ValueError("Parametro giocatore non valido.")

    @staticmethod
    def arrocco_lungo_applicabile(
        giocatore, scacchiera, mosse: dict[str, list[str]]
    ) -> bool:
        mosse_da_controllare = {
            0: r"^(R[x]?e1)|(T([a-h][1-8]?)?[x]?a1[+#]?)$",
            1: r"^(R[x]?e8)|(T([a-h][1-8]?)?[x]?a8[+#]?)$"
        }
        
        chiave = "bianco" if giocatore == 0 else "nero"
        storico = mosse.get(chiave, [])
        movimento_illegale = any(
            re.match(mosse_da_controllare[giocatore], m)
            for m in storico
        )
        
        if giocatore == 0:
            y = 0 
            king = scacchiera.get_pezzo(4, y)
            torre = scacchiera.get_pezzo(0, y)
        else:
            y = 7
            king = scacchiera.get_pezzo(4, y)
            torre = scacchiera.get_pezzo(0, y) 

        colore = "nero" if giocatore == 1 else "bianco"
        case_intermedie = [(1, y), (2, y), (3, y)]
        return (
            king and torre
            and isinstance(king, Re) and isinstance(torre, Torre)
            and king.colore == colore
            and not movimento_illegale
            and all(scacchiera.get_pezzo(*pos) is None for pos in case_intermedie)
            and all(
                not MovimentoRe.casella_sotto_scacco(scacchiera, col, y, colore)
                for col in [4, 3, 2]
            )
        )
    
    def arrocco_corto_applicabile(giocatore, scacchiera, 
                                  mosse: dict[str, list[str]]) -> bool:
        mosse_da_controllare = {
            0: r"^(R[x]?e1)|(T([a-h][1-8]?)?[x]?h1[+#]?)$",
            1: r"^(R[x]?e8)|(T([a-h][1-8]?)?[x]?h8[+#]?)$"
        }
        chiave = "bianco" if giocatore == 0 else "nero"
        storico = mosse.get(chiave, [])
        movimento_illegale = any(re.match(mosse_da_controllare[giocatore], m) 
                                 for m in storico)
        if giocatore == 0:
            y = 0 
            king = scacchiera.get_pezzo(4, y)
            torre = scacchiera.get_pezzo(7, y)
        else:
            y = 7
            king = scacchiera.get_pezzo(4, y)
            torre = scacchiera.get_pezzo(7, y)
        
        colore = "nero" if giocatore == 1 else "bianco"
        case_intermedie = [(5, y), (6, y)]  
        return (
            king and torre
            and isinstance(king, Re) and isinstance(torre, Torre)
            and king.colore == colore
            and not movimento_illegale
            and all(scacchiera.get_pezzo(*pos) is None for pos in case_intermedie)
            and all(not MovimentoRe.casella_sotto_scacco(scacchiera, col, y, colore) 
                    for col in [4, 5, 6])
        )