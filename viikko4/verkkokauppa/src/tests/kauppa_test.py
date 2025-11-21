import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):

    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 20
            if tuote_id == 3:
                return 0

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "olut", 3)

            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)


        
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista
        
    
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan_oikein(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        #(nimi, viite, tili_numero, self._kaupan_tili, summa)
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)

    def test_maksettaessa_2_eri_ostosta_pankin_metodia_tilisiirto_kutsutaan_oikein(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 8)
    

    def test_maksettaessa_2_samaa_ostosta_pankin_metodia_tilisiirto_kutsutaan_oikein(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 10)


    def test_lisattaessa_tuote_ja_loppunut_tuote_pankin_metodia_tilisiirto_kutsutaan_oikein(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)


    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)
    

    def test_uusi_viiite_jokaiseen_maksuun(self):

        # alustetaan kauppa
        self.viitegeneraattori_mock = Mock(wraps=Viitegeneraattori())
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)
    

    def test_poisto(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)


        '''

           def poista_korista(self, id):
        tuote = self._varasto.hae_tuote(id)
        self._ostoskori.poista(tuote)
        self._varasto.palauta_varastoon(tuote)
    def hae_tuote(self, id):
        tuotteet = self._saldot.keys()

        for tuote in tuotteet:
            if tuote.id == id:
                return tuote

        return None

        
    def ota_varastosta(self, tuote):
        saldo = self.saldo(tuote.id)

        self._saldot[tuote] = saldo - 1

        self._kirjanpito.lisaa_tapahtuma(f"otettiin varastosta {tuote}")

    def palauta_varastoon(self, tuote):
        saldo = self.saldo(tuote.id)

        self._saldot[tuote] = saldo + 1

        self._kirjanpito.lisaa_tapahtuma(f"palautettiin varastoon {tuote}")

        '''

