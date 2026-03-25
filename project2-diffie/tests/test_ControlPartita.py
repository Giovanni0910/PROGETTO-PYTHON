from unittest.mock import MagicMock, patch

import pytest

from scacchi.boundary.BoundayPartita import PartitaB
from scacchi.control.ControlPartita import ControlPartita
from scacchi.control.ControlScacchi import ControlScacchi


# Fixture che configura un'istanza di ControlPartita con giocatori mockati (o simulati)
@pytest.fixture
def setup_control_partita():
    """Fixture per configurare ControlPartita con giocatori mock."""
    partita = MagicMock()
    partita.giocatore1 = MagicMock(nome="Giocatore1", colore="bianco")
    partita.giocatore2 = MagicMock(nome="Giocatore2", colore="nero")
    partita.turno = 0
    partita.partita_in_corso = True
    menu_control = MagicMock()
    control = ControlPartita(partita, menu_control)
    control.giocatore = partita.giocatore1
    return control, partita, menu_control

# Testa il comportamento in caso di scacco matto al giocatore bianco
def test_scacco_matto_bianco(setup_control_partita):
    """Test scacco matto al bianco."""
    c, p, _ = setup_control_partita
    c.giocatore = p.giocatore1
    p.turno = 0
    with patch.object(
        ControlScacchi, 'verifica_scacco_scacco_matto', return_value=True
    ), patch.object(
        PartitaB, 'print_scacco_matto'
    ) as m_print, patch.object(
        PartitaB, 'giocatore1_perde'
    ) as m_perde:
        res = c.scacco_matto_stallo()
        m_print.assert_called_once()
        m_perde.assert_called_once_with(p.giocatore1, p.giocatore2)
        assert res is True
        assert c.stato is False
        assert p.partita_in_corso is False

# Testa il comportamento in caso di scacco matto al giocatore nero
def test_scacco_matto_nero(setup_control_partita):
    """Test scacco matto al giocatore nero."""
    control_partita, partita_mock, _ = setup_control_partita
    
    # Configura giocatore nero come corrente
    control_partita.giocatore = partita_mock.giocatore2
    partita_mock.turno = 1
    
    with patch.object(
        ControlScacchi, 'verifica_scacco_scacco_matto', return_value=True
    ), patch.object(
        PartitaB, 'print_scacco_matto'
    ) as mock_print, patch.object(
        PartitaB, 'giocatore1_vince'
    ) as mock_vince:
        result = control_partita.scacco_matto_stallo()

        mock_print.assert_called_once()
        mock_vince.assert_called_once_with(
            partita_mock.giocatore1, partita_mock.giocatore2
        )
        assert result is True
        assert control_partita.stato is False
        assert partita_mock.partita_in_corso is False

# Testa il comportamento in caso di stallo
def test_stallo(setup_control_partita):
    """Testa il comportamento della funzione scacco_matto_stallo in caso di stallo."""
    control_partita, partita_mock, _ = setup_control_partita
    
    with patch.object(
        ControlScacchi, 'verifica_scacco_scacco_matto', return_value='stallo'
    ), patch.object(PartitaB, 'print_stallo') as mock_print:
        result = control_partita.scacco_matto_stallo()

        mock_print.assert_called_once()
        assert result is True
        assert control_partita.stato is False
        assert partita_mock.partita_in_corso is False

# Testa il comportamento in caso di semplice scacco (non scacco matto o stallo)
def test_solo_scacco(setup_control_partita):
    """Test scacco semplice."""
    control_partita, partita_mock, _ = setup_control_partita
    
    # Simula che c'è scacco ma non matto (valore di ritorno diverso da True/'stallo')
    with patch.object(ControlScacchi, 'verifica_scacco_scacco_matto', 
                      return_value='scacco'):
        result = control_partita.scacco_matto_stallo()
        
        assert result is False
        assert control_partita.stato is True  # Lo stato non dovrebbe cambiare
        assert partita_mock.partita_in_corso is True

def test_risposta_inaspettata(setup_control_partita):
    """Test comportamento per valore di ritorno inaspettato."""
    c, p, _ = setup_control_partita
    with patch.object(ControlScacchi, 'verifica_scacco_scacco_matto', 
                      return_value='???'):
        assert c.scacco_matto_stallo() is False

# Testa il comportamento quando verifica_scacco_scacco_matto restituisce None
def test_verifica_none(setup_control_partita):
    """Test se verifica_scacco_scacco_matto restituisce None."""
    c, _, _ = setup_control_partita
    with patch.object(ControlScacchi, 'verifica_scacco_scacco_matto', 
                      return_value=None):
        assert c.scacco_matto_stallo() is False