# test_movimento_regina.py

from scacchi.control.MovimentoRegina import MovimentoRegina
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Regina import Regina
from scacchi.entity.Torre import Torre


class MockScacchiera:
    """Mock class per simulare una scacchiera per i test."""

    def __init__(self):
        self.scacchiera = [[None for _ in range(8)] for _ in range(8)]
    
    def get_pezzo(self, x, y):
        return self.scacchiera[x][y]
    
    def set_pezzo(self, x, y, pezzo):
        self.scacchiera[x][y] = pezzo

def test_regina_mossa_valida_mossa_semplice():
    """Test che la regina possa effettuare una mossa semplice valida."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    scacchiera.set_pezzo(0, 3, regina_bianca)
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dd4", scacchiera)
    assert risultato == (0, 3)

def test_regina_mossa_valida_cattura():
    """Test che la regina possa catturare avversario in una posizione valida."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    pedone_nero = Pedone("nero")
    scacchiera.set_pezzo(0, 3, regina_bianca)
    scacchiera.set_pezzo(3, 3, pedone_nero)
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dxd4", scacchiera)
    assert risultato == (0, 3)

def test_regina_mossa_valida_cattura2():
    """Test che la regina possa catturare avversarsio usando notazione alternativa."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    pedone_nero = Pedone("nero")
    scacchiera.set_pezzo(0, 3, regina_bianca)
    scacchiera.set_pezzo(3, 3, pedone_nero)
    risultato = MovimentoRegina.regina_mossa_valida(0, "D:d4", scacchiera)
    assert risultato == (0, 3)

def test_regina_mossa_valida_ambiguita_colonna():
    """Test che la regina gestisca correttamente ambigu di colonna nella notazione."""
    scacchiera = MockScacchiera()
    regina1 = Regina("bianco")
    regina2 = Regina("bianco")
    scacchiera.set_pezzo(0, 3, regina1)  # d1
    scacchiera.set_pezzo(0, 5, regina2)  # f1
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dd1d4", scacchiera)
    assert risultato == (0, 3)

def test_regina_mossa_valida_mossa_non_valida():
    """Test che la regina non possa effettuare una mossa non valida."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    scacchiera.set_pezzo(0, 3, regina_bianca)
    risultato = MovimentoRegina.regina_mossa_valida(0, "De5", scacchiera)
    assert risultato is None

def test_aggiorna_mossa_valida_senza_scacco():
    """Test che la regina possa effettuare una mossa valida senza dare scacco."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    re_nero = Re("nero")
    scacchiera.set_pezzo(0, 3, regina_bianca)
    scacchiera.set_pezzo(7, 4, re_nero)
    risultato = MovimentoRegina.aggiorna(0, "Dd4", scacchiera)
    assert risultato is True
    assert scacchiera.get_pezzo(3, 3) == regina_bianca
    assert scacchiera.get_pezzo(0, 3) is None

def test_aggiorna_mossa_con_scacco_non_dichiarato():
    """Test che la regina non possa effettuare  mossa che dà scacco senz dichiararlo."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    re_nero = Re("nero")
    scacchiera.set_pezzo(0, 3, regina_bianca)
    scacchiera.set_pezzo(7, 3, re_nero)
    risultato = MovimentoRegina.aggiorna(0, "Dd4", scacchiera)
    assert risultato is False
    assert scacchiera.get_pezzo(0, 3) == regina_bianca

def test_aggiorna_mossa_con_scacco_dichiarato():
    """Test che la regina possa effettuare una mossa che dà scacco dichiarato."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    re_nero = Re("nero")
    scacchiera.set_pezzo(0, 3, regina_bianca)
    scacchiera.set_pezzo(7, 3, re_nero)
    risultato = MovimentoRegina.aggiorna(0, "Dd4+", scacchiera)
    assert risultato is True
    assert scacchiera.get_pezzo(3, 3) == regina_bianca
    assert scacchiera.get_pezzo(0, 3) is None

def test_aggiorna_mossa_con_scacco_dichiarato2():
    """Test che la regina possa effettuare una mossa che dà scacco dichiarato."""
    scacchiera = MockScacchiera()
    # Configurazione semplice di scacco (non matto)
    regina_bianca = Regina("bianco")
    re_nero = Re("nero")
    scacchiera.set_pezzo(0, 3, regina_bianca)  # d1
    scacchiera.set_pezzo(7, 3, re_nero)        # d8
    
    # Muovi la regina in d4 per dare scacco
    risultato = MovimentoRegina.aggiorna(0, "Dd4+", scacchiera)
    assert risultato is True
    assert scacchiera.get_pezzo(3, 3) == regina_bianca
    assert scacchiera.get_pezzo(0, 3) is None

def test_movimento_diagonale_alto_destra():
    """Test movimento diagonale verso alto-destra."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dd4", scacchiera)
    assert risultato == (0, 0)

def test_movimento_diagonale_alto_sinistra():
    """Test movimento diagonale verso alto-sinistra."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    scacchiera.set_pezzo(0, 7, regina_bianca)  # h1
    
    risultato = MovimentoRegina.regina_mossa_valida(0, "De4", scacchiera)
    assert risultato == (0, 7)

def test_movimento_orizzontale_sinistra():
    """Test movimento orizzontale verso sinistra."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    scacchiera.set_pezzo(0, 7, regina_bianca)  # h1
    
    risultato = MovimentoRegina.regina_mossa_valida(0, "Da1", scacchiera)
    assert risultato == (0, 7)

def test_movimento_orizzontale_destra():
    """Test movimento orizzontale verso destra."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dh1", scacchiera)
    assert risultato == (0, 0)

def test_blocco_percorso_orizzontale():
    """Test che la regina non possa saltare sopra pezzi in movimento orizzontale."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    pedone_bianco = Pedone("bianco")
    
    # Posiziona la regina in a1 e un pedone in c1
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(0, 2, pedone_bianco)  # c1
    
    # Mock della funzione get_pezzo per verificare il percorso
    def mock_get_pezzo(riga, colonna):
        if riga == 0 and colonna == 2:  # c1
            return pedone_bianco
        return None
    
    scacchiera.get_pezzo = mock_get_pezzo
    
    assert not MovimentoRegina.regina_mossa_valida(0, "Dd1", scacchiera)

def test_blocco_percorso_verticale():
    """Test che la regina non possa saltare sopra pezzi in movimento verticale."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    torre_nera = Torre("nero")
    
    # Posizioniamo la regina in a1 (riga 7, colonna 0)
    scacchiera.set_pezzo(7, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(5, 0, torre_nera)     # a3 (blocca il percorso)
    
    # Mock della funzione get_pezzo per verificare il percorso
    def mock_get_pezzo(riga, colonna):
        if riga == 5 and colonna == 0:  # a3
            return torre_nera
        if riga == 7 and colonna == 0:  # a1 (regina)
            return regina_bianca
        return None
    
    scacchiera.get_pezzo = mock_get_pezzo
    
    # Tentativo di muoversi in a5 (riga 3), ma a3 (riga 5) è occupato
    risultato = MovimentoRegina.regina_mossa_valida(0, "Da5", scacchiera)
    assert risultato is None  # La mossa dovrebbe essere negata

def test_blocco_percorso_diagonale():
    """Test che la regina non possa saltare sopra pezzi in movimento diagonale."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    alfiere_nero = Alfiere("nero")
    
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(1, 1, alfiere_nero)   # b2 (blocca il percorso diagonale)
    
    # Tentativo di muoversi in c3, ma b2 è occupato
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dc3", scacchiera)
    assert risultato is None

def test_movimento_ai_bordi_scacchiera():
    """Test movimenti della regina ai bordi della scacchiera."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    
    # Regina nell'angolo in alto a destra
    scacchiera.set_pezzo(7, 7, regina_bianca)  # h8
    
    # Movimento valido verso il centro
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dd4", scacchiera)
    assert risultato == (7, 7)

def test_auto_cattura_non_permessa():
    """Test che la regina non possa catturare pezzi dello stesso colore."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    pedone_bianco = Pedone("bianco")
    
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(3, 3, pedone_bianco)  # d4 (stesso colore)
    
    # Tentativo di "catturare" il proprio pezzo
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dxd4", scacchiera)
    assert risultato is None

def test_movimento_lungo_diagonale():
    """Test movimento lungo su tutta la diagonale."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    
    # Movimento lungo tutta la diagonale fino a h8
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dh8", scacchiera)
    assert risultato == (0, 0)

def test_movimento_lungo_orizzontale():
    """Test movimento lungo su tutta la riga."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    
    # Movimento lungo tutta la prima riga fino a h1
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dh1", scacchiera)
    assert risultato == (0, 0)

def test_movimento_lungo_verticale():
    """Test movimento lungo su tutta la colonna."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    
    # Movimento lungo tutta la colonna a fino a a8
    risultato = MovimentoRegina.regina_mossa_valida(0, "Da8", scacchiera)
    assert risultato == (0, 0)

def test_cattura_ai_bordi():
    """Test cattura di un pezzo posizionato ai bordi della scacchiera."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    torre_nera = Torre("nero")
    
    scacchiera.set_pezzo(3, 3, regina_bianca)  # d4
    scacchiera.set_pezzo(7, 7, torre_nera)     # h8 (angolo)
    
    # Cattura del pezzo nell'angolo
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dxh8", scacchiera)
    assert risultato == (3, 3)

def test_mossa_invalida_movimento_cavallo():
    """Test che la regina non possa muoversi come un cavallo."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    
    scacchiera.set_pezzo(3, 3, regina_bianca)  # d4
    
    # Tentativo di movimento come un cavallo (2+1 caselle a L)
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dc6", scacchiera)
    assert risultato is None  

def test_blocco_multiple_pezzi_sul_percorso():
    """Test che la regina non possa passare oltre più pezzi sullo stesso percorso."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    pedone_nero = Pedone("nero")
    torre_nera = Torre("nero")

    # Posiziona la regina in d1 e due pezzi sul suo percorso
    scacchiera.set_pezzo(0, 3, regina_bianca)  # d1
    scacchiera.set_pezzo(3, 3, pedone_nero)  # d4 (prima barriera)
    scacchiera.set_pezzo(5, 3, torre_nera)   # d6 (seconda barriera)

    # Tentativo di movimento in d8
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dd8", scacchiera)
    assert risultato is None  # Non dovrebbe essere una mossa valida, ci sono ostacoli

def test_blocco_percorso_salto_pezzi():
    """Test che la regina non possa saltare sopra pezzi lungo il percorso."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    cavallo_nero = Cavallo("nero")

    # Posiziona la regina in d1 e il cavallo in d3
    scacchiera.set_pezzo(0, 3, regina_bianca)  # d1
    scacchiera.set_pezzo(2, 3, cavallo_nero)  # d3

    # Tentativo di movimento in d8 (regina dovrebbe fermarsi su d3)
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dd8", scacchiera)
    assert risultato is None  # La regina non può saltare sopra il cavallo

def test_movimento_lungo_diagonale_con_blocco():
    """Test che la regina non possa muoversi  se ci sono pezzi che bloccano casella."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    alfiere_nero = Alfiere("nero")
    pedone_bianco = Pedone("bianco")

    # Posiziona la regina in a1 e l'alfiere e pedone lungo la diagonale
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(1, 1, alfiere_nero)   # b2 (alfiere nero blocca)
    scacchiera.set_pezzo(2, 2, pedone_bianco)  # c3 (pedone bianco)

    # Tentativo di muoversi fino a g7, ma la diagonale è bloccata
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dg7", scacchiera)
    assert risultato is None  # Dovrebbe essere None, perché il percorso è bloccato

def test_cattura_diagonale_regina():
    """Test che la regina possa catturare un pezzo avversario lungo una diagonale."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    cavallo_nero = Cavallo("nero")

    # Posiziona la regina in a1 e il cavallo in b2 (permette una cattura diagonale)
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(1, 1, cavallo_nero)  # b2 (pezzo avversario)

    # La regina muove da a1 a b2 per catturare il cavallo
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dxb2", scacchiera)
    assert risultato == (0, 0)  # La regina cattura il cavallo

def test_cattura_verticale_regina():
    """Test che la regina possa catturare un pezzo avversario  una colonna verticale."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    alfiere_nero = Alfiere("nero")

    # Posiziona la regina in a1 e l'alfiere in a3 (nella stessa colonna)
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(2, 0, alfiere_nero)  # a3

    # La regina muove da a1 a a3 per catturare l'alfiere
    risultato = MovimentoRegina.regina_mossa_valida(0, "Da3", scacchiera)
    assert risultato == (0, 0)  # La regina cattura l'alfiere

def test_auto_cattura_non_permessa2():
    """Test che la regina non possa catturare un pezzo dello stesso colore."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    pedone_bianco = Pedone("bianco")

    # Posiziona la regina in a1 e il pedone bianco in a3
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(2, 0, pedone_bianco)  # a3

    # Tentativo di cattura del pedone bianco (mossa non valida)
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dxa3", scacchiera)
    assert risultato is None  # La regina non può catturare il pedone bianco

def test_movimento_lungo_colonna_senza_ostacoli():
    """Test che la regina possa muoversi in colonna  se non ci sono ostacoli."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")

    # Posiziona la regina in a1
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1

    # La regina si muove lungo tutta la colonna a (fino a a8)
    risultato = MovimentoRegina.regina_mossa_valida(0, "Da8", scacchiera)
    assert risultato == (0, 0)  # La mossa lungo la colonna a è valida

def test_regina_non_puo_trascorrere_altri_pezzi():
    """Test che la regina non possa attraversare altri pezzi durante la cattura."""
    scacchiera = MockScacchiera()
    regina_bianca = Regina("bianco")
    pedone_bianco = Pedone("bianco")
    pedone_nero = Pedone("nero")

    # Posiziona la regina in a1, il pedone bianco in a3 e il pedone nero in a4
    scacchiera.set_pezzo(0, 0, regina_bianca)  # a1
    scacchiera.set_pezzo(2, 0, pedone_bianco)  # a3 (ostacolo)
    scacchiera.set_pezzo(3, 0, pedone_nero)    # a4 (pezzo da catturare)

    # Tentativo di cattura il pedone nero (a4), ma il pedone bianco blocca il percorso
    risultato = MovimentoRegina.regina_mossa_valida(0, "Dxa4", scacchiera)
    assert risultato is None  # Non può attraversare il pedone bianco

def test_mossa_malformattata():
    """Test che mosse malformattate vengano rifiutate."""
    scacchiera = MockScacchiera()
    regina = Regina("bianco")
    scacchiera.set_pezzo(0, 0, regina)
    
    # Notazioni strane o malformattate
    assert MovimentoRegina.regina_mossa_valida(0, "Dx", scacchiera) is None
    assert MovimentoRegina.regina_mossa_valida(0, "D123", scacchiera) is None
    assert MovimentoRegina.regina_mossa_valida(0, "Daa1", scacchiera) is None