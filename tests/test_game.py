import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import config
from game.balance import profil_obtiznosti
from game.automaticky_tah import (
    MIN_ZLATO_REZERVA,
    naplanuj_automaticky_tah,
    proved_automaticky_tah,
)
from game.energie import meditace
from game.save_load import Hra, nacti_slot, uloz_slot
from game.settings import NastaveniHry
from game.souboje import BOSSOVE, Nepritel, Souboj
from main import nova_hra
from models.otrokyne import Otrokyně
from utils.vypis import barva


class HraTesty(unittest.TestCase):
    def test_nova_hra_ma_dve_dospele_postavy_a_defaulty(self):
        hra = nova_hra()
        self.assertEqual(len(hra.harem.otrokyne), 2)
        self.assertTrue(all(otrok.vek >= 18 for otrok in hra.harem.otrokyne))
        self.assertEqual(hra.nastaveni.obtiznost, "normalni")

    def test_save_load_slotu_neprepise_hlavni_save(self):
        hra = Hra()
        hra.hrac.gold = 777
        with tempfile.TemporaryDirectory() as slozka:
            hlavni = Path(slozka) / "hlavni.json"
            self.assertTrue(uloz_slot(hra, 2, hlavni))
            self.assertFalse(hlavni.exists())
            nactena = nacti_slot(2, hlavni)
            self.assertIsNotNone(nactena)
            self.assertEqual(nactena.hrac.gold, 777)
            self.assertEqual(nactena.nastaveni.obtiznost, "normalni")

    def test_souboj_vyhra_a_prida_odmenu(self):
        hra = Hra()
        hra.hrac.gold = 0
        souboj = Souboj(hra.hrac, hra.mafie, hra)
        souboj.nepritel = Nepritel("Testovací bandita", 1, 1, 0, 25, 10)
        with patch("builtins.input", side_effect=["1", ""]), patch(
            "random.randint", return_value=0
        ):
            self.assertTrue(souboj.proved_boj())
        self.assertEqual(hra.hrac.gold, 25)
        self.assertEqual(hra.hrac.kill_count, 1)

    def test_energie_meditace_obnovi_energie(self):
        hra = Hra()
        hra.hrac.sex_energy = 0
        hra.hrac.dark_energy = 0
        with redirect_stdout(io.StringIO()):
            self.assertTrue(meditace(hra))
        self.assertEqual(hra.hrac.sex_energy, 5)
        self.assertEqual(hra.hrac.dark_energy, 18)
        self.assertFalse(meditace(hra))

    def test_migrace_stareho_save_ma_bezpecne_defaulty(self):
        stare_data = {
            "verze": "18.0",
            "hrac": {"gold": 123, "dark_energy": 7},
            "harem": {"otrokyne": [{"jmeno": "Eva", "vek": 17}]},
        }
        hra = Hra.from_dict(stare_data)
        self.assertEqual(hra.hrac.gold, 123)
        self.assertGreaterEqual(hra.harem.otrokyne[0].vek, 18)
        self.assertEqual(hra.nastaveni.to_dict(), {"barvy": True, "obtiznost": "normalni"})

    def test_obtiznost_meni_silu_a_odmenu(self):
        self.assertLess(
            profil_obtiznosti("lehka")["nepritel"],
            profil_obtiznosti("normalni")["nepritel"],
        )
        self.assertGreater(
            profil_obtiznosti("tezka")["odmena"],
            profil_obtiznosti("normalni")["odmena"],
        )

    def test_bossove_a_konce_reaguji_na_rozhodnuti(self):
        self.assertGreaterEqual(len(BOSSOVE), 3)
        hra = Hra()
        hra.hrac.reputace_mesta = 30
        hra.svet.vztahy_npc = {klic: 30 for klic in hra.svet.vztahy_npc}
        hra.harem.pridat(Otrokyně("Mira"))
        hra.harem.pridat(Otrokyně("Radan"))
        for otrok in hra.harem.otrokyne:
            otrok.loajalita = 60
            otrok.duvera = 60
        hra.kampan.volby = [{"volba": "spolecna_cesta"}]
        self.assertEqual(hra.kampan.urci_zaver(hra), "Sjednocené město")
        hra.kampan.volby = [{"volba": "vyuzit"}]
        self.assertEqual(hra.kampan.urci_zaver(hra), "Vláda stínů")

    def test_barvy_terminalu_se_promitnou_do_vypisu(self):
        puvodni = config.USE_COLORS
        try:
            NastaveniHry(barvy=False).aplikuj()
            self.assertEqual(barva("test", config.GREEN), "test")
            NastaveniHry(barvy=True).aplikuj()
            self.assertIn("\033[", barva("test", config.GREEN))
        finally:
            config.set_colors_enabled(puvodni)

    def test_automaticky_tah_planuje_bez_vstupu_a_chrani_najem(self):
        hra = Hra()
        hra.harem.pridat(Otrokyně("Na nájmu"))
        hra.harem.pridat(Otrokyně("Volná"))
        hra.harem.otrokyne[0].na_najmu = True
        hra.harem.otrokyne[0].najem_zbyva_dni = 1
        hra.hrac.sex_energy = 0
        hra.hrac.dark_energy = 0

        plan = naplanuj_automaticky_tah(hra)

        self.assertTrue(plan.akce)
        self.assertTrue(any("Meditace" == akce.nazev for akce in plan.akce))
        self.assertTrue(any("Volná" == akce.cil for akce in plan.akce))
        self.assertFalse(any("Na nájmu" == akce.cil for akce in plan.akce))

    def test_automaticky_tah_neutrati_zlatou_rezervu(self):
        hra = Hra()
        hra.hrac.gold = 1_000
        hra.harem.pridat(Otrokyně("Alena"))
        plan = naplanuj_automaticky_tah(hra)

        vysledek = proved_automaticky_tah(hra, plan)

        self.assertGreaterEqual(hra.hrac.gold, MIN_ZLATO_REZERVA)
        self.assertEqual(vysledek.zlato_po, hra.hrac.gold)


if __name__ == "__main__":
    unittest.main()
