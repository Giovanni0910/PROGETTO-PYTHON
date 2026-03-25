from unittest.mock import MagicMock, patch

import pytest

from scacchi.control.MovimentoPedone import MovimentoPedone
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Cavallo import Cavallo
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Regina import Regina
from scacchi.entity.Torre import Torre


class TestMovimentoPedone:
    """Classe di test per MovimentoPedone."""

    def setup_method(self):
        """Configura i mock per ogni test."""
        self.scacchiera_mock = MagicMock()
        self.scacchiera_mock.en_passant_target = None
        
        # Mock per ControlScacchiera.traduci_mossa
        self.traduci_mossa_mock = MagicMock()
        
        # Mock per PartitaB
        self.partita_mock = MagicMock()

    def crea_pedone_bianco(self):
        """Crea un pedone bianco mock."""
        pedone = MagicMock(spec=Pedone)
        pedone.colore = "bianco"
        return pedone

    def crea_pedone_nero(self):
        """Crea un pedone nero mock."""
        pedone = MagicMock(spec=Pedone)
        pedone.colore = "nero"
        return pedone

    def crea_regina_nera(self):
        """Crea una regina nera mock."""
        regina = MagicMock(spec=Regina)
        regina.colore = "nero"
        return regina

    def crea_re_nero(self):
        """Crea un re nero mock."""
        re = MagicMock(spec=Re)
        re.colore = "nero"
        return re

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_movimento_pedone_bianco_una_casella(self, partita_mock, control_mock):
        """Testa movimento di un pedone bianco di una casella."""
        # Arrange
        control_mock.traduci_mossa.return_value = (4, 3)  # e4
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (4, 3): None,  # destinazione libera
            (4, 2): pedone_bianco  # pedone in posizione di partenza
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(0, "e4", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato == (4, 2)
        control_mock.traduci_mossa.assert_called_with("e4")

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_movimento_pedone_bianco_due_caselle(self, partita_mock, control_mock):
        """Testa movimento pedone bianco di due caselle dalla posizione iniziale."""
        # Arrange
        control_mock.traduci_mossa.return_value = (4, 3)  # e4
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (4, 3): None,  # destinazione libera
            (4, 2): None,  # casella intermedia libera
            (4, 1): pedone_bianco  # pedone in posizione iniziale
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(0, "e4", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato == (4, 1)

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_movimento_pedone_nero_una_casella(self, partita_mock, control_mock):
        """Testa movimento di un pedone nero di una casella."""
        # Arrange
        control_mock.traduci_mossa.return_value = (4, 4)  # e5
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (4, 4): None,  # destinazione libera
            (4, 5): pedone_nero  # pedone in posizione di partenza
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(1, "e5", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato == (4, 5)

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_movimento_pedone_nero_due_caselle(self, partita_mock, control_mock):
        """Testa movimento di un pedone nero di due caselle dalla posizione iniziale."""
        # Arrange
        control_mock.traduci_mossa.return_value = (4, 4)  # e5
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (4, 4): None,  # destinazione libera
            (4, 5): None,  # casella intermedia libera
            (4, 6): pedone_nero  # pedone in posizione iniziale
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(1, "e5", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato == (4, 6)

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_movimento_casella_occupata(self, partita_mock, control_mock):
        """Testa che il movimento fallisca se la casella di destinazione è occupata."""
        # Arrange
        control_mock.traduci_mossa.return_value = (4, 3)  # e4
        pedone_bianco = self.crea_pedone_bianco()
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (4, 3): pedone_nero,  # destinazione occupata
            (4, 2): pedone_bianco
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(0, "e4", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato is None
        partita_mock.print_casella_occupata.assert_called_once()

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_cattura_diagonale_valida(self, partita_mock, control_mock):
        """Testa cattura diagonale valida."""
        # Arrange
        control_mock.traduci_mossa.return_value = (5, 3)  # f4
        pedone_bianco = self.crea_pedone_bianco()
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (5, 3): pedone_nero,  # pezzo nemico da catturare
            (4, 2): pedone_bianco  # pedone che cattura
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.cattura_pezzo(0, "exf4", self.scacchiera_mock)
        
        # Assert
        assert risultato == (4, 2)

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_cattura_re_non_permessa(self, partita_mock, control_mock):
        """Testa che non sia possibile catturare il re."""
        # Arrange
        control_mock.traduci_mossa.return_value = (5, 3)  # f4
        pedone_bianco = self.crea_pedone_bianco()
        re_nero = self.crea_re_nero()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (5, 3): re_nero,  # re nemico
            (4, 2): pedone_bianco
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.cattura_pezzo(0, "exf4", self.scacchiera_mock)
        
        # Assert
        assert risultato is None
        partita_mock.print_mossa_negata2.assert_called()

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_cattura_stesso_colore_non_permessa(self, partita_mock, control_mock):
        """Testa che non sia possibile catturare un pezzo del proprio colore."""
        # Arrange
        control_mock.traduci_mossa.return_value = (5, 3)  # f4
        pedone_bianco1 = self.crea_pedone_bianco()
        pedone_bianco2 = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (5, 3): pedone_bianco2,  # pezzo stesso colore
            (4, 2): pedone_bianco1
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.cattura_pezzo(0, "exf4", self.scacchiera_mock)
        
        # Assert
        assert risultato is None
        partita_mock.print_mossa_negata2.assert_called()

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_en_passant_bianco(self, partita_mock, control_mock):
        """Testa cattura en passant per il bianco."""
        # Arrange
        control_mock.traduci_mossa.side_effect = [
            (5, 5),  # f6 - destinazione
            (4, 4)   # e4 - origine
        ]
        pedone_bianco = self.crea_pedone_bianco()
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (5, 5): None,  # destinazione vuota
            (5, 4): pedone_nero,  # pedone nero da catturare
            (4, 4): pedone_bianco  # pedone bianco che cattura
        }.get((x, y))
        
        self.scacchiera_mock.en_passant_target = (5, 4)
        
        # Act
        risultato = MovimentoPedone.cattura_pezzo(0, "exf6", self.scacchiera_mock)
        
        # Assert
        assert len(risultato) == 5
        assert risultato[:2] == (4, 4)  # posizione origine
        assert risultato[2:4] == (5, 4)  # posizione pezzo catturato

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_en_passant_nero(self, partita_mock, control_mock):
        """Testa cattura en passant per il nero."""
        # Arrange
        control_mock.traduci_mossa.side_effect = [
            (5, 2),  # f3 - destinazione
            (4, 3)   # e3 - origine
        ]
        pedone_nero = self.crea_pedone_nero()
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (5, 2): None,  # destinazione vuota
            (5, 3): pedone_bianco,  # pedone bianco da catturare
            (4, 3): pedone_nero  # pedone nero che cattura
        }.get((x, y))
        
        self.scacchiera_mock.en_passant_target = (5, 3)
        
        # Act
        risultato = MovimentoPedone.cattura_pezzo(1, "exf3", self.scacchiera_mock)
        
        # Assert
        assert len(risultato) == 5
        assert risultato[:2] == (4, 3)  # posizione origine
        assert risultato[2:4] == (5, 3)  # posizione pezzo catturato

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_promozione_regina(self, partita_mock, control_mock):
        """Testa promozione a regina."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.return_value = pedone_bianco
        
        # Act
        risultato = MovimentoPedone.promozione_pedone(0, self.scacchiera_mock, "a8D")
        
        # Assert
        assert risultato is True
        self.scacchiera_mock.set_pezzo.assert_called_once()
        args = self.scacchiera_mock.set_pezzo.call_args[0]
        assert args[0] == 0 and args[1] == 7  # coordinate
        assert isinstance(args[2], type(Regina(colore="bianco")))  # regina bianca

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_promozione_torre(self, partita_mock, control_mock):
        """Testa promozione a torre."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.return_value = pedone_bianco
        
        # Act
        risultato = MovimentoPedone.promozione_pedone(0, self.scacchiera_mock, "a8T")
        
        # Assert
        assert risultato is True
        self.scacchiera_mock.set_pezzo.assert_called_once()
        args = self.scacchiera_mock.set_pezzo.call_args[0]
        assert isinstance(args[2], type(Torre(colore="bianco")))

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_promozione_alfiere(self, partita_mock, control_mock):
        """Testa promozione ad alfiere."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.return_value = pedone_bianco
        
        # Act
        risultato = MovimentoPedone.promozione_pedone(0, self.scacchiera_mock, "a8A")
        
        # Assert
        assert risultato is True
        args = self.scacchiera_mock.set_pezzo.call_args[0]
        assert isinstance(args[2], type(Alfiere(colore="bianco")))

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    
    def test_promozione_cavallo(self, partita_mock, control_mock):
        """Testa promozione a cavallo."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.return_value = pedone_bianco
        
        # Act
        risultato = MovimentoPedone.promozione_pedone(0, self.scacchiera_mock, "a8C")
        
        # Assert
        assert risultato is True
        args = self.scacchiera_mock.set_pezzo.call_args[0]
        # Fix: confronta i tipi correttamente
        assert isinstance(args[2], Cavallo)
        # Oppure, se vuoi essere più specifico sul colore:
        # assert isinstance(args[2], Cavallo) and args[2].colore == "bianco"
    
    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_promozione_pattern_non_trovato(self, partita_mock, control_mock):
        """Testa quando la mossa non contiene pattern di promozione valido."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.return_value = pedone_bianco
        
        # Act - mossa senza pattern di promozione valido
        risultato = MovimentoPedone.promozione_pedone(0, self.scacchiera_mock, "a8X")
        
        # Assert
        assert risultato is None
        # promozione_non_valida NON viene chiamata in questo caso
        partita_mock.promozione_non_valida.assert_not_called()


    
    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_promozione_nero_ottava_traversa(self, partita_mock, control_mock):
        """Testa che il nero non possa promuovere sull'ottava traversa."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.return_value = pedone_nero
        
        # Act
        risultato = MovimentoPedone.promozione_pedone(1, self.scacchiera_mock, "a8D")
        
        # Assert
        assert risultato is None

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_promozione_nero_prima_traversa(self, partita_mock, control_mock):
        """Testa promozione del nero sulla prima traversa."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 0)  # a1
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.return_value = pedone_nero
        
        # Act
        risultato = MovimentoPedone.promozione_pedone(1, self.scacchiera_mock, "a1D")
        
        # Assert
        assert risultato is True

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_mossa_promozione_valida_bianco(self, partita_mock, control_mock):
        """Testa movimento con promozione per il bianco."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        pedone_bianco = self.crea_pedone_bianco()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (0, 7): None,  # destinazione libera
            (0, 6): pedone_bianco  # pedone in settima traversa
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(0, "a8D", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato == (0, 6)

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_mossa_promozione_senza_specifica_pezzo(self, partita_mock, control_mock):
        """Testa che fallisca una promozione senza specificare il pezzo."""
        # Arrange
        control_mock.traduci_mossa.return_value = (0, 7)  # a8
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(0, "a8", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato is None
        partita_mock.promozione_non_specificata.assert_called_once()

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_coordinate_fuori_scacchiera(self, partita_mock, control_mock):
        """Testa movimento con coordinate fuori dalla scacchiera."""
        # Arrange
        control_mock.traduci_mossa.return_value = None
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(0, "z9", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato is None

    @patch('scacchi.control.MovimentoPedone.ControlScacchiera')
    @patch('scacchi.control.MovimentoPedone.PartitaB')
    def test_movimento_pedone_colore_sbagliato(self, partita_mock, control_mock):
        """Testa che fallisca se si cerca di muovere un pedone del colore sbagliato."""
        # Arrange
        control_mock.traduci_mossa.return_value = (4, 3)  # e4
        pedone_nero = self.crea_pedone_nero()
        
        self.scacchiera_mock.get_pezzo.side_effect = lambda x, y: {
            (4, 3): None,  # destinazione libera
            (4, 2): pedone_nero  # pedone nero quando è il turno del bianco
        }.get((x, y))
        
        # Act
        risultato = MovimentoPedone.is_pedone_mossa_valida(0, "e4", 
                                                           self.scacchiera_mock)
        
        # Assert
        assert risultato is None
        partita_mock.print_mossa_negata3.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])