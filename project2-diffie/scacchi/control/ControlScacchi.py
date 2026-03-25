from scacchi.control.MovimentoRe import MovimentoRe


class ControlScacchi:
    """Classe di controllo per la logica degli scacchi.

    Gestisce la verifica dello scacco e dello scacco matto sulla scacchiera.
    Metodi:
        - re_sotto_scacco(scacchiera, colore_re): Verifica se il re di un dato
          colore è sotto scacco.
        - verifica_scacco_scacco_matto(scacchiera, colore): Determina se il re è
          sotto scacco, scacco matto o stallo.
    """

    @staticmethod
    def re_sotto_scacco(scacchiera, colore_re):
            # Trova la posizione del re
            x_re, y_re = None, None
            for x in range(8):
                for y in range(8):
                    pezzo = scacchiera.get_pezzo(x, y)
                    if pezzo and pezzo.tipo == "re" and pezzo.colore == colore_re:
                        x_re, y_re = x, y
                        break
                if x_re is not None:
                    break
            if x_re is None or y_re is None: #re non trovato
                return False

            # Controlla se qualche pezzo avversario può attaccare il re
            for x in range(8):
                for y in range(8):
                    pezzo = scacchiera.get_pezzo(x, y)
                    if (
                        pezzo is not None
                        and pezzo.colore != colore_re
                        and pezzo.puo_attaccare(
                            x, y, x_re, y_re, scacchiera
                        )
                    ):
                        return True
            return False
    
    @staticmethod
    def verifica_scacco_scacco_matto(scacchiera, colore):
        mosse_legali = False
        re_sotto_scacco = ControlScacchi.re_sotto_scacco(scacchiera, colore)

        for x in range(8):
            for y in range(8):
                pezzo = scacchiera.get_pezzo(x, y)
                if pezzo is not None and pezzo.colore == colore:
                    mosse = pezzo.mosse_possibili(x, y, scacchiera)
                    for x_nuova, y_nuova in mosse:
                        pezzo_catturato = scacchiera.get_pezzo(x_nuova, y_nuova)
                        scacchiera.set_pezzo(x_nuova, y_nuova, pezzo)
                        scacchiera.set_pezzo(x, y, None)

                        # Verifica che il re non sia sotto scacco dopo la simulazione
                        if (
                            not ControlScacchi.re_sotto_scacco(scacchiera, colore) 
                            and MovimentoRe.re_attaccato
                            (scacchiera, colore) is False):
                            mosse_legali = True

                        scacchiera.set_pezzo(x, y, pezzo)
                        scacchiera.set_pezzo(x_nuova, y_nuova, pezzo_catturato)

                        if mosse_legali:
                            break
                    if mosse_legali:
                        break
            if mosse_legali:
                break

        if not re_sotto_scacco:
            #re slavo
            return None
        elif not mosse_legali and re_sotto_scacco:
            #Re è sotto scacco matto
            return True
        elif mosse_legali and re_sotto_scacco:
            # re è sotto scacco ma ha mosse legali
            return False
        elif not mosse_legali and re_sotto_scacco is False:
            return "stallo"
    
