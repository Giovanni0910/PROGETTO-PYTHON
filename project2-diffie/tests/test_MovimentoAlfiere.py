import pytest

from scacchi.control.MovimentoAlfiere import MovimentoAlfiere
from scacchi.entity.Alfiere import Alfiere
from scacchi.entity.Pedone import Pedone
from scacchi.entity.Re import Re
from scacchi.entity.Scacchiera import Scacchiera
from scacchi.entity.Torre import Torre


class TestMovimentoAlfiere:
    """Test MovimentoAlfiere logic."""

    @pytest.fixture
    def scacchiera(self):
        sc = Scacchiera()
        # Pulisco la scacchiera per i test
        for x in range(8):
            for y in range(8):
                sc.set_pezzo(x, y, None)
        return sc

    def test_mossa_diagonale_inverso(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(5, 5, alfiere)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ac3", scacchiera) == (5, 5)

    # TEST OSTRUZIONI
    def test_mossa_con_ostacolo_stesso_colore(self, scacchiera):
        alfiere = Alfiere("bianco")
        pedone = Pedone("bianco")
        scacchiera.set_pezzo(1, 1, alfiere)
        scacchiera.set_pezzo(3, 3, pedone)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ad4", scacchiera) is None

    def test_mossa_con_ostacolo_avversario(self, scacchiera):
        alfiere = Alfiere("bianco")
        pedone = Pedone("nero")
        scacchiera.set_pezzo(1, 1, alfiere)
        scacchiera.set_pezzo(3, 3, pedone)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Axd4", scacchiera) == (1, 1)

    # TEST CATTURE
    def test_cattura_valida(self, scacchiera):
        alfiere = Alfiere("bianco")
        pedone = Pedone("nero")
        scacchiera.set_pezzo(2, 2, alfiere)
        scacchiera.set_pezzo(4, 4, pedone)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Axe5", scacchiera) == (2, 2)

    def test_cattura_non_valida_stesso_colore(self, scacchiera):
        alfiere = Alfiere("bianco")
        torre = Torre("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        scacchiera.set_pezzo(5, 5, torre)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Axf6", scacchiera) is None

    # TEST MOSSE NON DIAGONALI
    def test_mossa_orizzontale_invalida(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ad5", scacchiera) is None

    def test_mossa_verticale_invalida(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "A3d", scacchiera) is None

    def test_mossa_lascia_re_sotto_scacco(self, scacchiera):
        alfiere = Alfiere("bianco")
        re_bianco = Re("bianco")
        torre_nera = Torre("nero")
        scacchiera.set_pezzo(2, 2, alfiere)
        scacchiera.set_pezzo(0, 0, re_bianco)
        scacchiera.set_pezzo(0, 7, torre_nera)
        assert MovimentoAlfiere.aggiorna(0, "Ad3", scacchiera) is False

    # TEST AGGIORNAMENTO SCACCHIERA
    def test_aggiornamento_scacchiera_valido(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        assert MovimentoAlfiere.aggiorna(0, "Ae5", scacchiera) is True
        assert scacchiera.get_pezzo(3, 3) is None
        assert isinstance(scacchiera.get_pezzo(4, 4), Alfiere)

    def test_aggiornamento_scacchiera_invalido(self, scacchiera):
        alfiere = Alfiere("bianco")
        pedone = Pedone("bianco")
        scacchiera.set_pezzo(1, 1, alfiere)
        scacchiera.set_pezzo(3, 3, pedone)
        assert MovimentoAlfiere.aggiorna(0, "Ad4", scacchiera) is False
        assert isinstance(scacchiera.get_pezzo(1, 1), Alfiere)

    # TEST CASI SPECIALI
    def test_mossa_alfiere_angolo(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(0, 0, alfiere)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ah8", scacchiera) == (0, 0)

    # TEST PERCORSO LIBERO
    def test_percorso_libero(self, scacchiera):
        assert MovimentoAlfiere._strada_libera(1, 1, 4, 4, scacchiera) is True
        scacchiera.set_pezzo(2, 2, Pedone("bianco"))
        assert MovimentoAlfiere._strada_libera(1, 1, 4, 4, scacchiera) is False

    # TEST MOSSA NON VALIDA
    def test_mossa_non_valida(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Axz9", scacchiera) is None

    # TEST MOSSA CON PROMOZIONE (NON APPLICABILE)
    def test_mossa_con_promozione(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ad8=Q", scacchiera) is None

    # TEST MOSSA CON SCACCO NON DICHIARATO
    def test_scacco_non_dichiarato(self, scacchiera):
        alfiere = Alfiere("bianco")
        re_nero = Re("nero")
        scacchiera.set_pezzo(1, 1, alfiere)
        scacchiera.set_pezzo(3, 3, re_nero)
        assert MovimentoAlfiere.aggiorna(0, "Ad3", scacchiera) is False

    # TEST MOSSA CON SCACCO MATTO NON DICHIARATO
    def test_scacco_matto_non_dichiarato(self, scacchiera):
        alfiere = Alfiere("bianco")
        re_nero = Re("nero")
        torre = Torre("bianco")
        scacchiera.set_pezzo(1, 1, alfiere)
        scacchiera.set_pezzo(3, 3, re_nero)
        scacchiera.set_pezzo(3, 0, torre)
        assert MovimentoAlfiere.aggiorna(0, "Ad3", scacchiera) is False

    # TEST MOSSA CON SCACCO DICHIARATO
    def test_scacco_dichiarato_non_reale(self, scacchiera):
        alfiere = Alfiere("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        assert MovimentoAlfiere.aggiorna(0, "Ad4+", scacchiera) is False

    def test_ostacolo_avversario_che_blocca(self, scacchiera):
        alfiere = Alfiere("bianco")
        pedone = Pedone("nero")
        scacchiera.set_pezzo(1, 1, alfiere)
        scacchiera.set_pezzo(2, 2, pedone)  # Blocca la diagonale
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ad4", scacchiera) is None

    def test_mossa_non_salva_re(self, scacchiera):
        alfiere = Alfiere("bianco")
        re_bianco = Re("bianco")
        torre_nera = Torre("nero")
        scacchiera.set_pezzo(2, 2, alfiere)
        scacchiera.set_pezzo(0, 0, re_bianco)
        scacchiera.set_pezzo(0, 7, torre_nera)  # Torre che dà scacco
        assert MovimentoAlfiere.aggiorna(0, "Ad3", scacchiera) is False

    def test_notazione_completa(self, scacchiera):
        alfiere1 = Alfiere("bianco")
        alfiere2 = Alfiere("bianco")
        scacchiera.set_pezzo(1, 1, alfiere1)  # Alfiere in b2
        scacchiera.set_pezzo(1, 3, alfiere2)  # Alfiere in b4
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ab2d4", scacchiera) == (1, 1)

    def test_alfiere_bloccato(self, scacchiera):
        alfiere = Alfiere("bianco")
        pedone1 = Pedone("bianco")
        pedone2 = Pedone("bianco")
        pedone3 = Pedone("bianco")
        pedone4 = Pedone("bianco")
        scacchiera.set_pezzo(3, 3, alfiere)
        scacchiera.set_pezzo(2, 2, pedone1)  # NO
        scacchiera.set_pezzo(4, 2, pedone2)  # NE
        scacchiera.set_pezzo(4, 4, pedone3)  # SE
        scacchiera.set_pezzo(2, 4, pedone4)  # SO
        assert MovimentoAlfiere.alfiere_mossa_valida(0, "Ae5", scacchiera) is None

