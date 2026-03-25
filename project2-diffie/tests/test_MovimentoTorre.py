import pytest

from scacchi.control.MovimentoTorre import MovimentoTorre
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Scacchiera import Scacchiera
from scacchi.entity.Torre import Torre


class TestMovimentoTorre:
    """Test suite for MovimentoTorre class."""

    @pytest.fixture
    def scacchiera(self):
        sc = Scacchiera()
        # Pulisci la scacchiera
        for x in range(8):
            for y in range(8):
                sc.set_pezzo(x, y, None)
        return sc

    def test_mossa_semplice_torre(self, scacchiera):
        torre = Torre("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        result = MovimentoTorre.torre_mossa_valida(0, "Ta3", scacchiera)
        assert result == (0, 0, 0, 2)

    def test_mossa_orizzontale_torre(self, scacchiera):
        torre = Torre("bianco")
        scacchiera.set_pezzo(3, 3, torre)
        result = MovimentoTorre.torre_mossa_valida(0, "Td6", scacchiera)
        assert result == (3, 3, 3, 5)

    def test_cattura_valida(self, scacchiera):
        torre = Torre("bianco")
        pedone = Pedone("nero")
        scacchiera.set_pezzo(2, 2, torre)
        scacchiera.set_pezzo(2, 5, pedone)
        result = MovimentoTorre.torre_mossa_valida(0, "Txc6", scacchiera)
        assert result == (2, 2, 2, 5)

    def test_cattura_valida2(self, scacchiera):
        torre = Torre("bianco")
        pedone = Pedone("nero")
        scacchiera.set_pezzo(2, 2, torre)
        scacchiera.set_pezzo(2, 5, pedone)
        result = MovimentoTorre.torre_mossa_valida(0, "T:c6", scacchiera)
        assert result == (2, 2, 2, 5)

    def test_cattura_non_valida(self, scacchiera):
        torre = Torre("bianco")
        altro_pezzo = Torre("bianco")
        scacchiera.set_pezzo(1, 1, torre)
        scacchiera.set_pezzo(1, 4, altro_pezzo)
        assert MovimentoTorre.torre_mossa_valida(0, "Txb5", scacchiera) is None

    def test_mossa_con_ostacolo(self, scacchiera):
        torre = Torre("bianco")
        pedone = Pedone("bianco")
        scacchiera.set_pezzo(4, 0, torre)
        scacchiera.set_pezzo(4, 2, pedone)
        assert MovimentoTorre.torre_mossa_valida(0, "Te5", scacchiera) is None

    def test_ambiguita_colonna(self, scacchiera):
        torre1 = Torre("bianco")
        torre2 = Torre("bianco")
        scacchiera.set_pezzo(2, 0, torre1)
        scacchiera.set_pezzo(5, 0, torre2)
        
        # La mossa non può essere eseguita senza disambiguare la torre da muovere
        result = MovimentoTorre.torre_mossa_valida(0, "Ta3", scacchiera)
        # La mossa è non valida per ambiguità, quindi il risultato dovrebbe essere None
        assert result is None

    def test_ambiguita_riga(self, scacchiera):
        torre1 = Torre("bianco")
        torre2 = Torre("bianco")
        scacchiera.set_pezzo(3, 1, torre1)
        scacchiera.set_pezzo(3, 4, torre2)
        
        # Ambiguità tra le torri, ma una delle torri è bloccata dalla seconda.
        # La mossa dovrebbe fallire perché la casella è occupata
        result = MovimentoTorre.torre_mossa_valida(0, "Td5", scacchiera)
        assert result is None  # La mossa non è valida perché la casella è occupata

    def test_ambiguita_non_risolta(self, scacchiera):
        torre1 = Torre("bianco")
        torre2 = Torre("bianco")
        scacchiera.set_pezzo(2, 0, torre1)
        scacchiera.set_pezzo(5, 0, torre2)
        # Ambiguità tra le torri, non è chiaro quale si muove, quindi mossa non valida
        assert MovimentoTorre.torre_mossa_valida(0, "Ta3", scacchiera) is None

    def test_mossa_non_valida_diagonale(self, scacchiera):
        torre = Torre("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        # La torre non può muoversi in diagonale
        assert MovimentoTorre.torre_mossa_valida(0, "Tb2", scacchiera) is None

    def test_aggiorna_mossa_valida(self, scacchiera):
        torre = Torre("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        assert MovimentoTorre.aggiorna(0, "Ta3", scacchiera) is True
        assert scacchiera.get_pezzo(0, 0) is None
        assert isinstance(scacchiera.get_pezzo(0, 2), Torre)

    def test_aggiorna_mossa_scacco(self, scacchiera):
        torre = Torre("bianco")
        re_nero = Re("nero")
        scacchiera.set_pezzo(0, 0, torre)
        scacchiera.set_pezzo(0, 7, re_nero)
        
        # La torre muove e mette il re nero sotto scacco
        # Se la mossa fosse legale, aggiornerebbe la scacchiera, ma la mossa è illegale
        # poiché la torre non può muovere lasciando il proprio re sotto scacco
        result = MovimentoTorre.aggiorna(0, "Ta8+", scacchiera)
        assert result is False  # La mossa è illegale perché mette il re sotto scacco

    def test_percorso_libero(self, scacchiera):
        assert MovimentoTorre._percorso_libero(3, 1, 3, 5, scacchiera) is True
        assert MovimentoTorre._percorso_libero(2, 4, 6, 4, scacchiera) is True
        scacchiera.set_pezzo(3, 3, Pedone("bianco"))
        assert MovimentoTorre._percorso_libero(3, 1, 3, 5, scacchiera) is False
        assert MovimentoTorre._percorso_libero(1, 1, 3, 3, scacchiera) is False

    def test_mossa_formato_illegale(self, scacchiera):
        torre = Torre("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        result = MovimentoTorre.torre_mossa_valida(0, "Tz9", scacchiera)
        assert result is None

    def test_mossa_torre_con_scacco_proprio_re(self, scacchiera):
        """Test che la torre non può muovere lasciando il proprio re sotto scacco."""
        torre = Torre("bianco")
        re_bianco = Re("bianco")
        torre_nera = Torre("nero")
        scacchiera.set_pezzo(0, 0, torre)
        scacchiera.set_pezzo(4, 0, re_bianco)
        scacchiera.set_pezzo(4, 7, torre_nera)  # Torre nera che controlla la colonna
        
        # La torre bianca non può muoversi perché lascerebbe il re bianco sotto scacco
        assert MovimentoTorre.aggiorna(0, "Ta3", scacchiera) is False
        assert scacchiera.get_pezzo(0, 0) is not None  # La torre non si è mossa

    def test_disambiguazione_con_cattura(self, scacchiera):
        """Test disambiguazione con cattura valida."""
        torre1 = Torre("bianco")
        torre2 = Torre("bianco")
        pedone = Pedone("nero")
        scacchiera.set_pezzo(2, 0, torre1)
        scacchiera.set_pezzo(5, 0, torre2)
        scacchiera.set_pezzo(2, 4, pedone)
        
        # Muove la torre in c2 per catturare il pedone in c5
        result = MovimentoTorre.torre_mossa_valida(0, "T2c2xc5", scacchiera)
        assert result == (2, 0, 2, 4)

    def test_mossa_torre_con_promozione_non_ammessa(self, scacchiera):
        """Test che la torre non possa essere promossa (non applicabile)."""
        torre = Torre("bianco")
        scacchiera.set_pezzo(0, 6, torre)
        
        # Tentativo di mossa con promozione (non valida per la torre)
        assert MovimentoTorre.torre_mossa_valida(0, "Ta8=Q", scacchiera) is None

    def test_mossa_torre_con_notazione_alternativa(self, scacchiera):
        """Test notazione alternativa senza 'T' (non standard ma da considerare)."""
        torre = Torre("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        
        # Notazione non standard (manca il 'T')
        assert MovimentoTorre.torre_mossa_valida(0, "a1", scacchiera) is None

    def test_mossa_torre_con_pezzo_avversario_di_tipo_diverso(self, scacchiera):
        """Test cattura di un pezzo avversario di tipo diverso."""
        torre = Torre("bianco")
        alfiere = Alfiere("nero")  # Assumendo che esista la classe Alfiere
        scacchiera.set_pezzo(3, 3, torre)
        scacchiera.set_pezzo(3, 5, alfiere)
        
        # Cattura valida di un pezzo diverso
        result = MovimentoTorre.torre_mossa_valida(0, "Txd6", scacchiera)
        assert result == (3, 3, 3, 5)

    def test_mossa_torre_causa_stallo(self, scacchiera):
        """Test che la torre può causare stallo."""
        # Configurazione:
        # - Re nero in h8
        # - Torre bianca in g6 (controlla tutta la 7a traversa)
        # - Re bianco in a1 (lontano, non coinvolto)
        torre = Torre("bianco")
        re_nero = Re("nero")
        re_bianco = Re("bianco")
        
        scacchiera.set_pezzo(6, 5, torre)      # g6
        scacchiera.set_pezzo(7, 7, re_nero)    # h8
        scacchiera.set_pezzo(0, 0, re_bianco)  # a1 
        
        # La torre muove in g7, mettendo il re nero in stallo (senza scacco)
        result = MovimentoTorre.aggiorna(0, "Tg7", scacchiera)
        
        # Verifica:
        assert result is True  # La mossa è legale
        assert scacchiera.get_pezzo(6, 5) is None  # g6 è vuoto
        assert isinstance(scacchiera.get_pezzo(6, 6), Torre)  # g7 ha la torre
        
        # Stato del re nero:
        # - Non è sotto scacco diretto (nessun pezzo bianco lo attacca)
        # - Non può muovere (h7 e h8 sono controllati dalla torre in g7)
        # - Non ci sono altri pezzi neri che possono muovere
        # => Situazione di stallo

    def test_mossa_torre_su_proprio_pezzo(self, scacchiera):
        torre = Torre("bianco")
        pedone = Pedone("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        scacchiera.set_pezzo(0, 2, pedone)  # Pedone bianco blocca la torre
        result = MovimentoTorre.torre_mossa_valida(0, "Tc3", scacchiera)
        assert result is None  

    def test_mossa_torre_a_cavallo(self, scacchiera):
        torre = Torre("bianco")
        scacchiera.set_pezzo(4, 4, torre)
        result = MovimentoTorre.torre_mossa_valida(0, "Te5", scacchiera)
        assert result is None  # La torre non può muoversi come un cavallo

    def test_mossa_torre_con_due_ostacoli(self, scacchiera):
        torre = Torre("bianco")
        pedone1 = Pedone("bianco")
        pedone2 = Pedone("nero")
        scacchiera.set_pezzo(2, 2, torre)
        scacchiera.set_pezzo(2, 4, pedone1)
        scacchiera.set_pezzo(2, 6, pedone2)
        result = MovimentoTorre.torre_mossa_valida(0, "Tg8", scacchiera)
        assert result is None  # La torre non può attraversare due ostacoli

    def test_mossa_torre_con_blocco_parziale(self, scacchiera):
        torre = Torre("bianco")
        pedone = Pedone("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        scacchiera.set_pezzo(1, 0, pedone)  # Blocco parziale sulla colonna
        # Ora ci aspettiamo che la mossa sia valida 
        assert MovimentoTorre.torre_mossa_valida(0, "Ta4", scacchiera) == (0, 0, 0, 3)

    def test_mossa_torre_angolo(self, scacchiera):
        torre = Torre("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        result = MovimentoTorre.torre_mossa_valida(0, "Ta8", scacchiera)
        assert result == (0, 0, 0, 7)  # La torre può muoversi lungo la colonna
        result = MovimentoTorre.torre_mossa_valida(0, "Th1", scacchiera)
        assert result == (0, 0, 7, 0)  # La torre può muoversi lungo la riga

    def test_mossa_torre_con_colonna_occiupata(self, scacchiera):
        torre = Torre("bianco")
        pedone1 = Pedone("bianco")
        pedone2 = Pedone("bianco")
        scacchiera.set_pezzo(0, 0, torre)
        scacchiera.set_pezzo(0, 1, pedone1)
        scacchiera.set_pezzo(0, 2, pedone2)
        result = MovimentoTorre.torre_mossa_valida(0, "Ta4", scacchiera)
        assert result is None  # La torre non può attraversare pezzi dello stesso colore

    def test_mossa_torre_sotto_controllo_avversario(self, scacchiera):
        torre = Torre("bianco")
        cavallo = Pedone("nero")
        scacchiera.set_pezzo(0, 0, torre)
        scacchiera.set_pezzo(4, 0, cavallo)
        # Ora ci aspettiamo che la mossa sia valida 
        assert MovimentoTorre.torre_mossa_valida(0, "Ta5", scacchiera) == (0, 0, 0, 4)
