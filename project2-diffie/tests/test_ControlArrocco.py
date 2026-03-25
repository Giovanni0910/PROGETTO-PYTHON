import pytest

from scacchi.control.ControlArrocco import ArroccoC
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Regina import Regina
from scacchi.entity.Scacchiera import Scacchiera
from scacchi.entity.Torre import Torre


@pytest.fixture
def scacchiera_con_re_e_torre():
    """Scacchiera con Re e Torri bianchi in posizione iniziale."""
    scacchiera = Scacchiera()
    # Posizionamento Re e Torre per Bianco
    scacchiera.set_pezzo(4, 0, Re("bianco"))  # e1
    scacchiera.set_pezzo(7, 0, Torre("bianco"))  # h1
    scacchiera.set_pezzo(0, 0, Torre("bianco"))  # a1
    return scacchiera

def test_arrocco_corto_bianco(scacchiera_con_re_e_torre):
    """Test arrocco corto bianco valido."""
    scacchiera = scacchiera_con_re_e_torre
    # liberiamo f1 e g1
    scacchiera.set_pezzo(5, 0, None)  # f1
    scacchiera.set_pezzo(6, 0, None)  # g1
    mosse = {"bianco": []}
    risultato = ArroccoC.muovi("0-0", 0, scacchiera, mosse)
    assert risultato is True
    assert scacchiera.get_pezzo(6, 0).__class__.__name__ == "Re"
    assert scacchiera.get_pezzo(5, 0).__class__.__name__ == "Torre"

def test_arrocco_corto_nero():
    """Test arrocco corto nero valido."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 7, Re("nero"))     # e8
    scacchiera.set_pezzo(7, 7, Torre("nero"))  # h8
    scacchiera.set_pezzo(5, 7, None)  # f8
    scacchiera.set_pezzo(6, 7, None)  # g8
    mosse = {"nero": []}
    risultato = ArroccoC.muovi("0-0", 1, scacchiera, mosse)
    assert risultato is True
    assert scacchiera.get_pezzo(6, 7).__class__.__name__ == "Re"
    assert scacchiera.get_pezzo(5, 7).__class__.__name__ == "Torre"

def test_arrocco_lungo_bianco(scacchiera_con_re_e_torre):
    """Test arrocco lungo bianco valido."""
    scacchiera = scacchiera_con_re_e_torre
    scacchiera.set_pezzo(1, 0, None)
    scacchiera.set_pezzo(2, 0, None)
    scacchiera.set_pezzo(3, 0, None)
    mosse = {"bianco": []}
    risultato = ArroccoC.muovi("0-0-0", 0, scacchiera, mosse)
    assert risultato is True
    assert scacchiera.get_pezzo(2, 0).__class__.__name__ == "Re"
    assert scacchiera.get_pezzo(3, 0).__class__.__name__ == "Torre"

def test_arrocco_lungo_nero():
    """Test arrocco lungo nero valido."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 7, Re("nero"))     # e8
    scacchiera.set_pezzo(0, 7, Torre("nero"))  # a8
    scacchiera.set_pezzo(1, 7, None)  # b8
    scacchiera.set_pezzo(2, 7, None)  # c8
    scacchiera.set_pezzo(3, 7, None)  # d8
    mosse = {"nero": []}
    risultato = ArroccoC.muovi("0-0-0", 1, scacchiera, mosse)
    assert risultato is True
    assert scacchiera.get_pezzo(2, 7).__class__.__name__ == "Re"
    assert scacchiera.get_pezzo(3, 7).__class__.__name__ == "Torre"

def test_arrocco_corto_bianco_scacco_intermedio_da_torre():
    """Verifica che l'arrocco corto bianco fallisca se f1 è sotto scacco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(7, 0, Torre("bianco"))
    scacchiera.set_pezzo(5, 5, Torre("nero"))  # attacca f1
    mosse = {"bianco": []}
    assert not ArroccoC.muovi("0-0", 0, scacchiera, mosse)

def test_arrocco_lungo_bianco_scacco_finale_da_alfiere():
    """Test che l'arrocco lungo bianco fallisca se la casa finale è sotto scacco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(0, 0, Torre("bianco"))
    scacchiera.set_pezzo(5, 5, Alfiere("nero"))  # attacca c1
    mosse = {"bianco": []}
    assert not ArroccoC.muovi("0-0-0", 0, scacchiera, mosse)

def test_arrocco_corto_nero_scacco_da_regina():
    """Arrocco corto nero fallisce se f8 è sotto scacco da regina bianca."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 7, Re("nero"))  # e8
    scacchiera.set_pezzo(7, 7, Torre("nero"))  # h8
    scacchiera.set_pezzo(2, 5, Regina("bianco"))  # c6 - attacca f8
    mosse = {"nero": []}
    assert not ArroccoC.muovi("0-0", 1, scacchiera, mosse)

def test_arrocco_corto_nero_scacco_intermedio_da_pedone():
    """Arrocco corto nero fallisce se f8 è sotto scacco da pedone bianco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 7, Re("nero"))  # e8
    scacchiera.set_pezzo(7, 7, Torre("nero"))  # h8
    scacchiera.set_pezzo(5, 6, Pedone("bianco"))  # f7 - attacca f8
    mosse = {"nero": []}
    risultato = ArroccoC.muovi("0-0", 1, scacchiera, mosse)
    assert risultato is False

def test_arrocco_corto_bianco_bloccato_da_cavallo():
    """Arrocco corto bianco fallisce se f1 è occupata da cavallo bianco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(7, 0, Torre("bianco"))
    scacchiera.set_pezzo(5, 0, Cavallo("bianco"))
    mosse = {"bianco": []}
    assert not ArroccoC.muovi("0-0", 0, scacchiera, mosse)

def test_arrocco_corto_bianco_bloccato_da_re():
    """Verifica che l'arrocco corto bianco fallisca se f1 è occupata da un re bianco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))  # e1
    scacchiera.set_pezzo(7, 0, Torre("bianco"))  # h1
    scacchiera.set_pezzo(5, 0, Re("bianco"))  # f1 - blocca
    mosse = {"bianco": []}
    risultato = ArroccoC.muovi("0-0", 0, scacchiera, mosse)
    assert risultato is False

def test_arrocco_corto_nero_ostacolato_da_torre_alleata():
    """Verifica che l'arrocco corto nero fallisca se f8 è occupata da una torre nera."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 7, Re("nero"))
    scacchiera.set_pezzo(7, 7, Torre("nero"))
    scacchiera.set_pezzo(5, 7, Torre("nero"))
    mosse = {"nero": []}
    assert not ArroccoC.muovi("0-0", 1, scacchiera, mosse)

def test_arrocco_corto_nero_ostacolato_da_regina_alleata():
    """Arrocco corto nero fallisce se f8 è occupata da regina nera."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 7, Re("nero"))  # e8
    scacchiera.set_pezzo(7, 7, Torre("nero"))  # h8
    scacchiera.set_pezzo(5, 7, Regina("nero"))  # f8 - blocca
    mosse = {"nero": []}
    risultato = ArroccoC.muovi("0-0", 1, scacchiera, mosse)
    assert risultato is False

def test_arrocco_bianco_con_re_sotto_scacco():
    """Verifica che l'arrocco corto bianco fallisca se il re è sotto scacco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))  # e1
    scacchiera.set_pezzo(7, 0, Torre("bianco"))  # h1
    scacchiera.set_pezzo(5, 4, Torre("nero"))  # f5 - attacca e1
    mosse = {"bianco": []}
    assert not ArroccoC.muovi("0-0", 0, scacchiera, mosse)

def test_arrocco_nero_con_re_sotto_scacco():
    """Verifica che l'arrocco corto nero fallisca se il re è sotto scacco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 7, Re("nero"))  # e8
    scacchiera.set_pezzo(7, 7, Torre("nero"))  # h8
    scacchiera.set_pezzo(2, 4, Torre("bianco"))  # c5 - attacca e8
    mosse = {"nero": []}
    risultato = ArroccoC.muovi("0-0", 1, scacchiera, mosse)
    assert risultato is False

def test_arrocco_bianco_torre_gia_mossa():
    """Verifica che l'arrocco corto bianco fallisca se la torre ha già mosso."""
    scacchiera = Scacchiera()
    torre = Torre("bianco")
    torre.ha_mosso = True
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(7, 0, torre)
    mosse = {"bianco": []}
    assert ArroccoC.muovi("0-0", 0, scacchiera, mosse) is False

def test_arrocco_bianco_re_gia_mosso():
    """Verifica che l'arrocco corto bianco fallisca se il re ha già mosso."""
    scacchiera = Scacchiera()
    re = Re("bianco")
    re.ha_mosso = True
    scacchiera.set_pezzo(4, 0, re)  # e1
    scacchiera.set_pezzo(7, 0, Torre("bianco"))  # h1
    mosse = {"bianco": []}
    risultato = ArroccoC.muovi("0-0", 0, scacchiera, mosse)
    assert risultato is False

def test_arrocco_nero_torre_gia_mossa():
    """Verifica che l'arrocco corto nero fallisca se la torre ha già mosso."""
    scacchiera = Scacchiera()
    torre = Torre("nero")
    torre.ha_mosso = True
    scacchiera.set_pezzo(4, 7, Re("nero"))  # e8
    scacchiera.set_pezzo(7, 7, torre)  # h8
    mosse = {"nero": []}
    risultato = ArroccoC.muovi("0-0", 1, scacchiera, mosse)
    assert risultato is False

def test_arrocco_nero_re_gia_mosso():
    """Verifica che l'arrocco corto nero fallisca se il re ha già mosso."""
    scacchiera = Scacchiera()
    re = Re("nero")
    re.ha_mosso = True
    scacchiera.set_pezzo(4, 7, re)
    scacchiera.set_pezzo(7, 7, Torre("nero"))
    mosse = {"nero": []}
    assert ArroccoC.muovi("0-0", 1, scacchiera, mosse) is False

def test_arrocco_corto_bianco_con_alfiere_avversario_su_g1():
    """Arrocco corto bianco fallisce se g1 è occupata da alfiere nero."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(7, 0, Torre("bianco"))
    scacchiera.set_pezzo(6, 0, Alfiere("nero"))
    mosse = {"bianco": []}
    assert ArroccoC.muovi("0-0", 0, scacchiera, mosse) is False

def test_arrocco_corto_bianco_con_scacco_dopo_la_mossa():
    """Verifica che l'arrocco corto bianco fallisca se il re finisce sotto scacco."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(7, 0, Torre("bianco"))
    scacchiera.set_pezzo(6, 1, Regina("nero"))  # minaccia g1
    mosse = {"bianco": []}
    assert ArroccoC.muovi("0-0", 0, scacchiera, mosse) is False

def test_arrocco_corto_bianco_con_casella_f1_controllata():
    """Arrocco corto bianco fallisce se f1 è controllata da un avversario."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(7, 0, Torre("bianco"))
    scacchiera.set_pezzo(5, 2, Regina("nero"))  # controlla f1
    mosse = {"bianco": []}
    assert ArroccoC.muovi("0-0", 0, scacchiera, mosse) is False

def test_arrocco_lungo_bianco_con_torre_non_in_a1():
    """Verifica che l'arrocco lungo bianco fallisca se la torre non è in a1."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(4, 0, Re("bianco"))
    scacchiera.set_pezzo(1, 0, Torre("bianco"))  # Torre non in a1
    mosse = {"bianco": []}
    assert ArroccoC.muovi("0-0-0", 0, scacchiera, mosse) is False

def test_arrocco_con_re_non_in_posizione_iniziale():
    """Verifica che l'arrocco corto fallisca se il re non è nella posizione iniziale."""
    scacchiera = Scacchiera()
    scacchiera.set_pezzo(3, 0, Re("bianco"))  # d1 - non in e1
    scacchiera.set_pezzo(7, 0, Torre("bianco"))  # h1
    mosse = {"bianco": []}
    risultato = ArroccoC.muovi("0-0", 0, scacchiera, mosse)
    assert risultato is False  # Il re deve essere nella posizione iniziale