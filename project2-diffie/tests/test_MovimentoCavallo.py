# test_movimento_cavallo.py
import pytest

from scacchi.control.MovimentoCavallo import MovimentoCavallo
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Torre import Torre


class MockScacchiera:
    """Mock chessboard class for testing chess piece movements."""

    def __init__(self):
        self.scacchiera = [[None for _ in range(8)] for _ in range(8)]
    
    def get_pezzo(self, x, y):
        return self.scacchiera[x][y]
    
    def set_pezzo(self, x, y, pezzo):
        self.scacchiera[x][y] = pezzo

@pytest.fixture
def scacchiera():
    """Fixture that returns a mock chessboard for testing."""
    return MockScacchiera()

def test_cavallo_mossa_valida_mossa_semplice(scacchiera):
    """Test che una mossa semplice del cavallo sia riconosciuta come valida."""
    # Posiziona un cavallo bianco in b1 (notazione: (1, 0))
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(1, 0, cavallo_bianco)
    
    # Mossa valida: Cc3 (da b1 a c3 - (2, 2))
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cc3", scacchiera)
    assert risultato == (1, 0)  # Restituisce la posizione di origine

def test_cavallo_mossa_valida_cattura(scacchiera):
    """Test che una mossa di cattura del cavallo sia riconosciuta come valida."""
    # Posiziona un cavallo bianco in b1 (1, 0) e un pedone nero in c3 (2, 2)
    cavallo_bianco = Cavallo("bianco")
    pedone_nero = Pedone("nero")
    scacchiera.set_pezzo(1, 0, cavallo_bianco)
    scacchiera.set_pezzo(2, 2, pedone_nero)
    
    # Mossa valida: Cxc3
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cxc3", scacchiera)
    assert risultato == (1, 0)  # Restituisce la posizione di origine

def test_cavallo_mossa_valida_cattura2(scacchiera):
    """Test cattura cavallo notazione alternativa."""
    # Posiziona un cavallo bianco in b1 (1, 0) e un pedone nero in c3 (2, 2)
    cavallo_bianco = Cavallo("bianco")
    pedone_nero = Pedone("nero")
    scacchiera.set_pezzo(1, 0, cavallo_bianco)
    scacchiera.set_pezzo(2, 2, pedone_nero)
    
    # Mossa valida: Cxc3
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "C:c3", scacchiera)
    assert risultato == (1, 0)  # Restituisce la posizione di origine

def test_cavallo_mossa_valida_ambiguita_colonna(scacchiera):
    """Test ambiguità colonna cavallo."""
    # Due cavalli bianchi in b1 (1, 0) e f1 (5, 0) che possono muovere in d2 (3, 1)
    cavallo1 = Cavallo("bianco")
    cavallo2 = Cavallo("bianco")
    scacchiera.set_pezzo(1, 0, cavallo1)  # b1
    scacchiera.set_pezzo(5, 0, cavallo2)  # f1
    
    # Mossa ambigua: specifica il cavallo in b1 con Cbd2
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cbd2", scacchiera)
    assert risultato == (1, 0)  # Restituisce la posizione di origine del cavallo in b1

def test_cavallo_mossa_valida_mossa_non_valida(scacchiera):
    """Test che una mossa non valida del cavallo sia riconosciuta come tale."""
    # Posiziona un cavallo bianco in b1 (1, 0)
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(1, 0, cavallo_bianco)
    
    # Mossa non valida: Cc4 (non è una mossa a L)
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cc4", scacchiera)
    assert risultato is None

def test_aggiorna_mossa_valida_senza_scacco(scacchiera):
    """Test mossa valida del cavallo senza scacco al proprio re."""
    # Configurazione con cavallo bianco in b1 (1, 0) e re nero in e8 (4, 7)
    cavallo_bianco = Cavallo("bianco")
    re_nero = Re("nero")
    scacchiera.set_pezzo(1, 0, cavallo_bianco)
    scacchiera.set_pezzo(4, 7, re_nero)
    
    # Aggiungi re bianco in e1 (4, 0) per evitare scacco
    re_bianco = Re("bianco")
    scacchiera.set_pezzo(4, 0, re_bianco)
    
    # Mossa valida: Cc3 (da b1 a c3)
    risultato = MovimentoCavallo.aggiorna(0, "Cc3", scacchiera)
    assert risultato is True
    assert scacchiera.get_pezzo(2, 2) == cavallo_bianco
    assert scacchiera.get_pezzo(1, 0) is None

def test_aggiorna_mossa_con_scacco_dichiarato(scacchiera):
    """Test mossa cavallo con scacco dichiarato."""
    # Configurazione corretta: cavallo bianco che dà scacco senza catturare il re
    cavallo_bianco = Cavallo("bianco")
    re_nero = Re("nero")
    scacchiera.set_pezzo(5, 2, cavallo_bianco)  # f3
    scacchiera.set_pezzo(4, 5, re_nero)         # e6
    
    # Aggiungi re bianco in e1 (4, 0) per evitare problemi
    re_bianco = Re("bianco")
    scacchiera.set_pezzo(4, 0, re_bianco)
    
    # Mossa che dà scacco: Cd4+ (da f3 a d4, minacciando il re in e6)
    risultato = MovimentoCavallo.aggiorna(0, "Cd4+", scacchiera)
    assert risultato is True
    assert scacchiera.get_pezzo(3, 3) == cavallo_bianco
    assert scacchiera.get_pezzo(5, 2) is None

def test_aggiorna_mossa_con_scacco_non_dichiarato(scacchiera):
    """Test che una mossa che dà scacco senza dichiararlo venga rifiutata."""
    # Configurazione dove il cavallo dà scacco ma non è dichiarato
    cavallo_bianco = Cavallo("bianco")
    re_nero = Re("nero")
    scacchiera.set_pezzo(5, 2, cavallo_bianco)  # f3
    scacchiera.set_pezzo(4, 5, re_nero)         # e6
    
    # Aggiungi re bianco in e1 (4, 0)
    re_bianco = Re("bianco")
    scacchiera.set_pezzo(4, 0, re_bianco)
    
    # Mossa che dà scacco ma non dichiarata: Cd4 (da f3 a d4)
    # Il cavallo in d4 minaccia il re in e6
    risultato = MovimentoCavallo.aggiorna(0, "Cd4", scacchiera)
    assert risultato is False
    assert scacchiera.get_pezzo(5, 2) == cavallo_bianco  # Mossa annullata

def test_aggiorna_mossa_che_mette_il_proprio_re_sotto_scacco(scacchiera):
    """Test mossa cavallo che espone il proprio re a scacco."""
    # Muovere il cavallo espone il re bianco a scacco
    cavallo_bianco = Cavallo("bianco")
    re_bianco = Re("bianco")
    torre_nera = Torre("nero")
    scacchiera.set_pezzo(4, 4, cavallo_bianco)  # e5
    scacchiera.set_pezzo(0, 4, re_bianco)       # e1
    scacchiera.set_pezzo(7, 4, torre_nera)      # e8
    
    # Mossa che esporrebbe il re bianco alla torre nera in e8: Cc6
    risultato = MovimentoCavallo.aggiorna(0, "Cc6", scacchiera)
    assert risultato is False
    assert scacchiera.get_pezzo(4, 4) == cavallo_bianco  # Mossa annullata

def test_cavallo_mossa_valida_ambiguita_riga(scacchiera):
    """Test ambiguità riga cavallo."""
    cavallo1 = Cavallo("bianco")
    cavallo2 = Cavallo("bianco")
    scacchiera.set_pezzo(1, 2, cavallo1)
    scacchiera.set_pezzo(1, 4, cavallo2)
    assert MovimentoCavallo.cavallo_mossa_valida(0, "C3d4", scacchiera) == (1, 2)

def test_aggiorna_mossa_con_scacco_matto_non_dichiarato(scacchiera):
    """Test che una mossa che dà scacco matto senza dichiararlo venga rifiutata."""
    # Configurazione di scacco matto con cavallo
    cavallo_bianco = Cavallo("bianco")
    re_nero = Re("nero")
    torre_bianca = Torre("bianco")
    scacchiera.set_pezzo(3, 3, cavallo_bianco)  # d4
    scacchiera.set_pezzo(4, 7, re_nero)         # e8
    scacchiera.set_pezzo(0, 7, torre_bianca)    # a8

    # Aggiungi re bianco in e1 (4, 0)
    re_bianco = Re("bianco")
    scacchiera.set_pezzo(4, 0, re_bianco)

    # Mossa che dà scacco matto ma non dichiarato: Cf5
    risultato = MovimentoCavallo.aggiorna(0, "Cf5", scacchiera)
    assert risultato is False  # Mossa annullata per mancata dichiarazione
    assert scacchiera.get_pezzo(3, 3) == cavallo_bianco  # d4 ancora occupato

def test_cavallo_mossa_valida_mossa_con_promozione_invalida(scacchiera):
    """Il cavallo non può promuovere."""
    cavallo = Cavallo("bianco")
    scacchiera.set_pezzo(1, 6, cavallo)
    assert MovimentoCavallo.cavallo_mossa_valida(0, "Cb8=D", scacchiera) is None

def test_aggiorna_mossa_con_arrocco_invalido(scacchiera):
    """Test arrocco non valido con cavallo."""
    # Cavallo bianco in b1 (1, 0), re bianco in e1 (4, 0)
    cavallo_bianco = Cavallo("bianco")
    re_bianco = Re("bianco")
    scacchiera.set_pezzo(1, 0, cavallo_bianco)
    scacchiera.set_pezzo(4, 0, re_bianco)
    
    # Tentativo di arrocco con cavallo (mossa non valida)
    risultato = MovimentoCavallo.aggiorna(0, "0-0", scacchiera)
    assert risultato is False
    assert scacchiera.get_pezzo(1, 0) == cavallo_bianco  # Cavallo non si è mosso

def test_cavallo_mossa_valida_cattura_pezzo_protetto(scacchiera):
    """Test che il cavallo possa catturare un pezzo protetto da un altro pezzo."""
    cavallo_bianco = Cavallo("bianco")
    pedone_nero = Pedone("nero")
    torre_nera = Torre("nero")
    scacchiera.set_pezzo(1, 0, cavallo_bianco)
    scacchiera.set_pezzo(2, 2, pedone_nero)
    scacchiera.set_pezzo(2, 7, torre_nera)  # Torre che protegge il pedone
    
    # Mossa valida ma rischiosa: Cxc3
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cxc3", scacchiera)
    assert risultato == (1, 0) 

def test_aggiorna_mossa_con_presa_en_passant_invalida(scacchiera):
    """En passant non valido per cavallo."""
    # Tentativo di presa en passant con cavallo (non valida)
    cavallo_bianco = Cavallo("bianco")
    pedone_nero = Pedone("nero")
    scacchiera.set_pezzo(1, 4, cavallo_bianco)  # b5
    scacchiera.set_pezzo(2, 4, pedone_nero)     # c5 (simulando pedone appena mosso)
    
    # Mossa en passant invalida: Cxc6
    risultato = MovimentoCavallo.aggiorna(0, "Cxc6", scacchiera)
    assert risultato is False
    assert scacchiera.get_pezzo(1, 4) == cavallo_bianco  # Cavallo non si è mosso

def test_aggiorna_mossa_con_promozione_finta(scacchiera):
    """Test che una promozione finta del cavallo venga rifiutata."""
    # Cavallo bianco in b7 (1, 6) - tenta finta promozione
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(1, 6, cavallo_bianco)
    
    # Mossa con promozione finta: Cb8=C
    risultato = MovimentoCavallo.aggiorna(0, "Cb8=C", scacchiera)
    assert risultato is False  # I cavalli non possono promuovere
    assert scacchiera.get_pezzo(1, 6) == cavallo_bianco  # Cavallo non si è mosso

def test_cavallo_mossa_valida_bordo_sinistro(scacchiera):
    """Test cavallo bordo sinistro."""
    # Posiziona un cavallo bianco in a3 (0, 2)
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(0, 2, cavallo_bianco)

    # Mossa valida: Cb5 (da a3 a b5)
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cb5", scacchiera)
    assert risultato == (0, 2)  # Restituisce la posizione di origine

def test_cavallo_mossa_valida_bordo_destro(scacchiera):
    """Test cavallo bordo destro."""
    # Posiziona un cavallo bianco in h3 (7, 2)
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(7, 2, cavallo_bianco)

    # Mossa valida: Cg1 (da h3 a g1)
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cg1", scacchiera)
    assert risultato == (7, 2)  # Restituisce la posizione di origine

def test_cavallo_mossa_valida_bordo_superiore(scacchiera):
    """Test cavallo bordo superiore."""
    # Posiziona un cavallo bianco in a8 (0, 7)
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(0, 7, cavallo_bianco)

    # Mossa valida: Cb6 (da a8 a b6)
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cb6", scacchiera)
    assert risultato == (0, 7)  # Restituisce la posizione di origine

def test_cavallo_mossa_valida_bordo_inferiore(scacchiera):
    """Test cavallo bordo inferiore."""
    # Posiziona un cavallo bianco in h8 (7, 7)
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(7, 7, cavallo_bianco)

    # Mossa valida: Cg6 (da h8 a g6)
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cg6", scacchiera)
    assert risultato == (7, 7)  # Restituisce la posizione di origine

def test_cavallo_mossa_valida_interni(scacchiera):
    """Test mossa valida cavallo da posizione interna."""
    # Posiziona un cavallo bianco in e5 (4, 4)
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(4, 4, cavallo_bianco)

    # Mossa valida: Cg6 (da e5 a g6)
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cg6", scacchiera)
    assert risultato == (4, 4)  # Restituisce la posizione di origine

def test_aggiorna_mossa_con_scacco_proprio(scacchiera):
    """Test cavallo che mette il proprio re sotto scacco."""
    cavallo = Cavallo("bianco")
    re_bianco = Re("bianco")
    scacchiera.set_pezzo(2, 2, cavallo)
    scacchiera.set_pezzo(4, 4, re_bianco)
    assert MovimentoCavallo.aggiorna(0, "Cb4", scacchiera) is False

def test_cavallo_mossa_valida_cattura_doppia(scacchiera):
    """Test cattura cavallo con pezzo bianco e nero sulla stessa colonna."""
    cavallo_bianco = Cavallo("bianco")
    pedone_nero = Pedone("nero")
    pedone_bianco = Pedone("bianco")
    scacchiera.set_pezzo(3, 3, cavallo_bianco)
    scacchiera.set_pezzo(2, 5, pedone_nero)
    scacchiera.set_pezzo(4, 5, pedone_bianco)

    # Mossa che cattura un pezzo nero e un pezzo bianco: Cxc6
    risultato = MovimentoCavallo.cavallo_mossa_valida(0, "Cxc6", scacchiera)
    assert risultato == (3, 3)  # La mossa è valida e si muove alla posizione c6

def test_aggiorna_mossa_con_trasformazione_pezzo_in_valida(scacchiera):
    """Test che una trasformazione non valida del cavallo venga rifiutata."""
    # Configurazione con cavallo bianco in e4 (4, 3)
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(4, 3, cavallo_bianco)

    # Tentativo di trasformare il cavallo in altro pezzo (non valido)
    risultato = MovimentoCavallo.aggiorna(0, "Ce8=R", scacchiera)
    assert risultato is False  # I cavalli non possono trasformarsi in altri pezzi

def test_aggiorna_mossa_con_cattura_in_casella_vuota(scacchiera):
    """Test che una cattura in una casella vuota venga rifiutata."""
    # Configurazione di un cavallo bianco che tenta di muovere in una casella vuota
    cavallo_bianco = Cavallo("bianco")
    scacchiera.set_pezzo(2, 2, cavallo_bianco)

    # Tentativo di cattura di una casella vuota (mossa non valida)
    risultato = MovimentoCavallo.aggiorna(0, "Cc4", scacchiera)
    assert risultato is False  # La mossa non è valida, la casella c4 è vuota

def test_mossa_malformattata():
    """Test che mosse malformattate vengano rifiutate."""
    scacchiera = MockScacchiera()
    cavallo = Cavallo("bianco")
    scacchiera.set_pezzo(1, 7, cavallo)
    
    # Notazioni strane o malformattate
    assert MovimentoCavallo.cavallo_mossa_valida(0, "Cx", scacchiera) is None
    assert MovimentoCavallo.cavallo_mossa_valida(0, "C111", scacchiera) is None
    assert MovimentoCavallo.cavallo_mossa_valida(0, "Cab3", scacchiera) is None
