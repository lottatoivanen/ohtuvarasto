import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 3)
    
    def test_konstruktori_asettaa_saldon_oikein(self):
        self.varasto.lisaa_varastoon(3)
        self.assertEqual(str(self.varasto), f"saldo = {self.varasto.saldo}, vielä tilaa {self.varasto.paljonko_mahtuu()}")

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_negatiivinen_tilavuus_nollautuu(self):
        varasto = Varasto(-1)
        self.assertAlmostEqual(varasto.tilavuus, 0.0)
        self.assertAlmostEqual(varasto.saldo, -1)

    def test_negatiivinen_saldo_nollaantuu(self):
        varasto = Varasto(5, -3)
        self.assertAlmostEqual(varasto.saldo, 0.0)

    def test_alkusaldo_mahtuu(self):
        varasto = Varasto(5, 3)
        self.assertAlmostEqual(varasto.tilavuus, 5)
        self.assertAlmostEqual(varasto.saldo, 3)
        self.assertAlmostEqual(varasto.paljonko_mahtuu(), 2)

    def test_saldo_yli_tilavuuden(self):
        varasto = Varasto(5, 10)
        self.assertAlmostEqual(varasto.tilavuus, 5)
        self.assertAlmostEqual(varasto.saldo, 5)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)
    
    def test_negatiivinen_lisays_ei_muuta_saldoa(self):
        self.varasto.lisaa_varastoon(2)
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 2)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 8)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_ottaminen_negatiivinen_palauttaa_nolla(self):
        self.varasto.lisaa_varastoon(6)
        saatu = self.varasto.ota_varastosta(-2)
        self.assertAlmostEqual(saatu, 0.0)
        self.assertAlmostEqual(self.varasto.saldo, 6)

    def test_ottaminen_yli_saldon_nollaa(self):
        self.varasto.lisaa_varastoon(7)
        saatu = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu, 7)
        self.assertAlmostEqual(self.varasto.saldo, 0.0)
    
    def test_lisays_tasan_vapaan_tilan_verran(self):
        self.varasto.lisaa_varastoon(10)
        self.assertAlmostEqual(self.varasto.saldo, 10)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)

    def test_ei_ylita_maksimiarvoa(self):
        self.varasto.lisaa_varastoon(12)

        self.assertAlmostEqual(self.varasto.saldo, 10)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)

