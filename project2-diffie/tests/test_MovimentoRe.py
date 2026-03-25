
from scacchi.control.MovimentoRe import MovimentoRe
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Regina import Regina
from scacchi.entity.Scacchiera import Scacchiera
from scacchi.entity.Torre import Torre


# Helper
def setup_scacchiera_con_re(x, y, colore="bianco"):
    """Crea una scacchiera con un Re posizionato alle coordinate specificate.

    Args:
        x (int): Coordinata x (colonna) dove posizionare il Re.
        y (int): Coordinata y (riga) dove posizionare il Re.
        colore (str, optional): Colore del Re, default "bianco".

    Returns:
        Scacchiera: Oggetto Scacchiera con il Re posizionato.

    """
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(x, y, Re(colore))
    return scacchiera

# Movimento troppo lungo
def test_re_mossa_troppo_lunga_verticale():
    """Test che il re non possa muoversi di più di una casella in verticale."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    assert MovimentoRe.re_mossa_valida(0, "Re2", scacchiera) is None

def test_re_mossa_troppo_lunga_diagonale():
    """Test che il re non possa muoversi di più di una casella in diagonale."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    assert MovimentoRe.re_mossa_valida(0, "Rg7", scacchiera) is None

# Blocco da alleato
def test_re_mossa_bloccata_da_alleato():
    """Test che il re non possa muoversi su una casella occupata da un pezzo alleato."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(5, 4, Torre("bianco"))
    assert MovimentoRe.re_mossa_valida(0, "Rf5", scacchiera) is None

# Casella minacciata da avversari
def test_re_mossa_in_casella_minacciata_dritta():
    """Test che il re non possa muoversi in cas avv da un avversario in linea dritta."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(7, 4, Torre("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Re5", scacchiera) is None

def test_re_mossa_in_casella_minacciata_diagonale():
    """Test che il re non possa muoversi in una cas avv da un avversario in diag."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(7, 7, Alfiere("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Rf5", scacchiera) is None

def test_re_mossa_in_casella_minacciata_da_pedone():
    """Test che il re non possa muoversi in una cas avv da un pedone avversario."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(3, 3, Pedone("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Rd4", scacchiera) is None

def test_re_mossa_in_casella_minacciata_da_cavallo():
    """Test che il re non possa muoversi in una cas avv da un cavallo avversario."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(2, 5, Cavallo("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Rf5", scacchiera) is None

def test_re_mossa_adiacente_altro_re():
    """Test che il re non possa muoversi in una casella adiacente a un altro re."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(5, 4, Re("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Rf5", scacchiera) is None

def test_re_cattura_senza_x_illegale():
    """Test che il re non possa catturare senza 'x' nella notazione."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(5, 4, Torre("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Rf5", scacchiera) is None

def test_re_cattura_con_x_ma_vuoto():
    """Test che il re non possa catturare con 'x' se la casella è vuota."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    assert MovimentoRe.re_mossa_valida(0, "Rxf5", scacchiera) is None

def test_re_cattura_alterativa_ma_vuoto():
    """Test che il re non possa catturare con ':' se la casella è vuota."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    assert MovimentoRe.re_mossa_valida(0, "R:f5", scacchiera) is None

def test_re_attaccato_da_alfiere():
    """Test che il re sia attaccato da un alfiere avversario."""
    scacchiera = setup_scacchiera_con_re(2, 2)
    scacchiera.set_pezzo(5, 5, Alfiere("nero"))
    assert MovimentoRe.re_attaccato(scacchiera, "bianco") is True

def test_re_non_attaccato():
    """Test che il re non sia attaccato quando non ci sono nemici che lo minacciano."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    assert MovimentoRe.re_attaccato(scacchiera, "bianco") is False

# Bordo e assenza re
def test_re_mossa_fuori_bordi():
    """Test che il re non possa muoversi fuori dai bordi della scacchiera."""
    scacchiera = setup_scacchiera_con_re(0, 0)
    assert MovimentoRe.re_mossa_valida(0, "Ra0", scacchiera) is None

def test_re_mancante_sulla_scacchiera():
    """Test che la funzione ritorni None se il re è mancante sulla scacchiera."""
    scacchiera = Scacchiera()
    assert MovimentoRe.re_mossa_valida(0, "Re5", scacchiera) is None

def test_re_cattura_con_pezzo_alleato_illegale():
    """Test che il re non possa catturare un pezzo alleato."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(5, 4, Torre("bianco"))
    assert MovimentoRe.re_mossa_valida(0, "Rxf5", scacchiera) is None

# 4. Test per mosse speciali
def test_re_mossa_arrocco_non_valida():
    """L'arrocco non dovrebbe essere gestito qui ma in ControlArrocco."""
    scacchiera = setup_scacchiera_con_re(4, 0)
    scacchiera.set_pezzo(7, 0, Torre("bianco"))
    assert MovimentoRe.re_mossa_valida(0, "0-0", scacchiera) is None

# 5. Test per situazioni di bordo complesse
def test_re_angolo_con_attacco():
    """Test che il re sia attaccato da un cav nem quando si trova in  scacchiera."""
    scacchiera = setup_scacchiera_con_re(0, 0)
    scacchiera.set_pezzo(1, 2, Cavallo("nero"))
    assert MovimentoRe.re_attaccato(scacchiera, "bianco") is True

def test_re_bordo_superiore_con_regina():
    """Test che il re sia attaccato da una regina nemic quando si trova sul bordo sup.

    della scacchiera.
    """
    scacchiera = setup_scacchiera_con_re(4, 7)
    scacchiera.set_pezzo(4, 0, Regina("nero"))
    assert MovimentoRe.re_attaccato(scacchiera, "bianco") is True

# 6. Test per situazioni di stallo
def test_re_non_attaccato_ma_bloccato():
    """Test che il re non sia attaccato ma bloccato dai pezzi alleati."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    # Circondiamo il re con pezzi alleati
    scacchiera.set_pezzo(3, 4, Pedone("bianco"))
    scacchiera.set_pezzo(5, 4, Pedone("bianco"))
    scacchiera.set_pezzo(4, 3, Pedone("bianco"))
    scacchiera.set_pezzo(4, 5, Pedone("bianco"))
    assert MovimentoRe.re_attaccato(scacchiera, "bianco") is False
    # Verifica che non ci sono mosse valide
    assert MovimentoRe.re_mossa_valida(0, "Re5", scacchiera) is None
    assert MovimentoRe.re_mossa_valida(0, "Rf4", scacchiera) is None

# 7. Test per notazione sbagliata
def test_re_notazione_sbagliata():
    """Test che il re non possa muoversi con una notazione sbagliata."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(5, 4, Torre("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Ke5", scacchiera) is None

# 8. Test per en-passant (non dovrebbe essere possibile per il re)
def test_re_cattura_en_passant_invalida():
    """Test che il re non possa catturare en passant (mossa non valida per il re)."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(5, 4, Pedone("nero"))
    assert MovimentoRe.re_mossa_valida(0, "Rxf5", scacchiera) is None

# 9. Test per controllo pezzi intermedi
def test_re_attaccato_con_pezzo_intermedio():
    """Test che il re non attacato se un pezzo intermedio casua l'attacco ."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    scacchiera.set_pezzo(4, 0, Torre("nero"))  # a4
    scacchiera.set_pezzo(4, 2, Pedone("bianco"))  # a6 (blocca)
    assert MovimentoRe.re_attaccato(scacchiera, "bianco") is False

def test_re_centro_con_attacco_360():
    """Test che il re al centro sia attaccato da pezzi avversari."""
    scacchiera = setup_scacchiera_con_re(4, 4)
    # Attacchi da tutte le direzioni
    scacchiera.set_pezzo(4, 0, Torre("nero"))  # a4
    scacchiera.set_pezzo(4, 7, Torre("nero"))  # h4
    scacchiera.set_pezzo(0, 4, Torre("nero"))  # e8
    scacchiera.set_pezzo(7, 4, Torre("nero"))  # e1
    scacchiera.set_pezzo(1, 1, Alfiere("nero"))  # b7
    scacchiera.set_pezzo(7, 7, Alfiere("nero"))  # h1
    scacchiera.set_pezzo(2, 6, Cavallo("nero"))  # c2
    scacchiera.set_pezzo(3, 3, Pedone("nero"))  # d5
    assert MovimentoRe.re_attaccato(scacchiera, "bianco") is True

