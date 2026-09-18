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
        self.assertEqual(hra.hrac.dark_energy, 12)
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
        self.assertTrue(hra.nastaveni.barvy)
        self.assertEqual(hra.nastaveni.obtiznost, "normalni")
        self.assertFalse(hra.nastaveni.ironman)
        self.assertFalse(hra.nastaveni.ai_dialogy)

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

    def test_koupit_uzemi_oznaci_obsazeno_a_generuje_prijem(self):
        from game.mafie import koupit_uzemi
        hra = Hra()
        hra.hrac.gold = 2000
        uspech = koupit_uzemi(hra.hrac, hra.mafie, "Tržiště")
        self.assertTrue(uspech)
        self.assertEqual(len(hra.mafie.uzemi), 1)
        uzemi = hra.mafie.uzemi[0]
        self.assertTrue(uzemi.obsazeno)
        self.assertEqual(uzemi.kontrola, 50)
        prijem = hra.mafie.vypocet_prijmu()
        self.assertEqual(prijem, 80 * 50 // 100)

    def test_valka_uzemi_s_vitezstvim(self):
        from game.mafie import valka_uzemi, koupit_uzemi
        hra = Hra()
        hra.hrac.gold = 2000
        koupit_uzemi(hra.hrac, hra.mafie, "Přístav")
        hra.mafie.vojaci = 20
        hra.mafie.kapitanove = 3
        zlato_pred = hra.hrac.gold
        with patch("builtins.input", side_effect=["1", "1"]):
            valka_uzemi(hra.hrac, hra.mafie, hra)
        self.assertGreater(hra.hrac.gold, zlato_pred)
        self.assertGreater(hra.mafie.vliv_ve_meste, 0)

    def test_cerny_trh_okovy_a_ametyst(self):
        from game.obchod import cerny_trh
        hra = Hra()
        hra.hrac.gold = 1000
        hra.mafie.korupce = 30
        o = Otrokyně("Zoe", loajalita=40)
        hra.harem.pridat(o)
        with patch("builtins.input", side_effect=["2", ""]):
            cerny_trh(hra)
        self.assertEqual(o.loajalita, 45)
        self.assertEqual(hra.hrac.gold, 880)

        temno_max_pred = hra.hrac.max_temno()
        with patch("builtins.input", side_effect=["6", ""]):
            cerny_trh(hra)
        self.assertEqual(hra.hrac.max_temno(), temno_max_pred + 10)

    def test_ai_dialog_fallback_variety(self):
        from game.ai_dialog import generuj_dialog
        hra = Hra()
        o = Otrokyně("Kassandra", faze_zkazenosti=12, loajalita=90)
        hra.nastaveni.ai_dialogy = True
        dialog = generuj_dialog(o, hra.hrac, typ="trest", nastaveni=hra.nastaveni, ticho=True)
        self.assertTrue(len(dialog) > 10)
        self.assertIn("Kassandra", dialog)

    def test_nove_questy_jsou_v_databazi(self):
        from game.questy import QUESTY
        nazvy = [q["nazev"] for q in QUESTY]
        self.assertIn("Pád inkvizičního vyšetřovatele", nazvy)
        self.assertIn("Krvavý rituál v podzemní kryptě", nazvy)
        self.assertIn("Infiltrace šlechtického plesu", nazvy)
        self.assertIn("Lov vzpurné rebelky", nazvy)
        self.assertIn("Obsazení městské zbrojnice", nazvy)

    def test_mapa_nove_lokace_a_cestovani(self):
        from game.svet import LOKACE
        hra = Hra()
        self.assertIn("katakomby", LOKACE)
        self.assertIn("svatyne_krvaveho_mesice", LOKACE)
        self.assertIn("palac_bohatych", LOKACE)

        self.assertEqual(hra.svet.aktualni_lokace, "pevnost")
        with patch("random.random", return_value=0.99):
            self.assertTrue(hra.svet.cestuj("trh", hra))
        self.assertEqual(hra.svet.aktualni_lokace, "trh")

    def test_mapa_pruzkum_lokace(self):
        hra = Hra()
        hra.hrac.sex_energy = 20
        zlato_pred = hra.hrac.gold
        with patch("random.random", return_value=0.1), patch("builtins.input", return_value=""):
            hra.svet.pruzkum_lokace(hra)
        self.assertGreater(hra.hrac.gold, zlato_pred)

    def test_nove_frakce_a_reputace(self):
        hra = Hra()
        self.assertIn("kult_krve", hra.frakce.frakce)
        self.assertIn("syndikat_stinu", hra.frakce.frakce)
        self.assertIn("cech_kurtizan", hra.frakce.frakce)
        hra.frakce.frakce["cech_kurtizan"].zmenit(10)
        self.assertEqual(hra.frakce.frakce["cech_kurtizan"].reputace, 25)

    def test_nove_charaktery_v_databazi(self):
        from data.charaktery import CHARAKTERY
        self.assertIn("kurtizana", CHARAKTERY)
        self.assertIn("fanaticka", CHARAKTERY)
        self.assertIn("amazonka", CHARAKTERY)
        self.assertIn("carodejka", CHARAKTERY)

    def test_nevestinec_otevreni_a_zarazeni_divky(self):
        from game.nevestinec import spocitej_denni_vynos_divky, vypocti_denni_prijem
        hra = Hra()
        hra.hrac.gold = 500
        otrok = Otrokyně(jmeno="Roxana", charakter="kurtizana", vek=22)
        otrok.touha = 80
        otrok.vlhkost = 80
        otrok.faze_zkazenosti = 2
        hra.harem.pridat(otrok)

        # Otevření nevěstince
        with patch("builtins.input", return_value="1"):
            from game.nevestinec import otevrit_nevestinec
            otevrit_nevestinec(hra)

        self.assertTrue(hra.nevestinec.otevreno)
        self.assertEqual(hra.hrac.gold, 200)

        # Zařazení otrokyně do nevěstince
        otrok.v_nevestinci = True
        vynos = spocitej_denni_vynos_divky(otrok, hra.nevestinec)
        self.assertGreater(vynos, 40)

        # Denní zisk
        zisk = vypocti_denni_prijem(hra)
        self.assertGreaterEqual(zisk, vynos)
        self.assertEqual(hra.nevestinec.celkovy_zisk, zisk)

    def test_nevestinec_prodej_otrokyně(self):
        from game.nevestinec import vypocti_cenu_prodeje, prodat_otrokyni
        hra = Hra()
        otrok = Otrokyně(jmeno="Bella", poslusnost=70, submisivita=80, charakter="kurtizana")
        hra.harem.pridat(otrok)
        cena = vypocti_cenu_prodeje(otrok)
        self.assertGreater(cena, 300)

        # Provedení prodeje (volba 1 = první otrokyně, potvrdit = ano)
        zlato_pred = hra.hrac.gold
        with patch("builtins.input", side_effect=["1", "ano", ""]):
            prodat_otrokyni(hra)

        self.assertEqual(hra.hrac.gold, zlato_pred + cena)
        self.assertEqual(len(hra.harem.vsechny_aktivni()), 0)

    def test_svet_nove_lokace_a_npc(self):
        from game.svet import LOKACE, NPC
        self.assertIn("cervena_ctvrt", LOKACE)
        self.assertIn("podzemni_arena", LOKACE)
        self.assertIn("stribrne_terasy", LOKACE)

        self.assertIn("madame_scarlett", NPC)
        self.assertIn("baron_archibald", NPC)
        self.assertIn("gladiator_gor", NPC)
        self.assertIn("lady_eleanor", NPC)

    def test_nove_tresty_a_odmeny(self):
        from data.tresty import TRESTY
        from data.odmeny import ODMENY
        from game.tresty_odmeny import proved_trest, proved_odmenu

        self.assertIn("solna_komora", TRESTY)
        self.assertIn("verejny_pranyr", TRESTY)
        self.assertIn("krvave_znackovani", TRESTY)
        self.assertIn("senzoricka_deprivace", TRESTY)

        self.assertIn("sladke_privilegium", ODMENY)
        self.assertIn("hedvabny_zupan", ODMENY)
        self.assertIn("intimni_laska", ODMENY)
        self.assertIn("pansky_slib", ODMENY)

        hra = Hra()
        hra.hrac.dark_energy = 30
        hra.hrac.gold = 100
        hra.hrac.sex_energy = 30
        otrok = Otrokyně(jmeno="Vanda", charakter="amazonka")
        hra.harem.pridat(otrok)

        # Provedení solné komory
        self.assertTrue(proved_trest(otrok, hra.hrac, "solna_komora"))
        self.assertGreater(otrok.submisivita, 40)

        # Provedení sladké hostiny
        self.assertTrue(proved_odmenu(otrok, hra.hrac, "sladke_privilegium"))
        self.assertGreater(otrok.loajalita, 30)

    def test_vice_manzelek_zarlivost_a_spolecna_noc(self):
        from models.marriage import Marriage
        from game.manzelstvi import spolecna_noc_manzelek
        hra = Hra()
        m1 = Otrokyně(jmeno="Elena", je_manzelkou=True, partnerka=True)
        m2 = Otrokyně(jmeno="Diana", je_manzelkou=True, partnerka=True)
        hra.harem.pridat(m1)
        hra.harem.pridat(m2)

        mar1 = Marriage(partner_jmeno="Elena", den_zasnubin=1, den_svatby=1, stav="vdana", zarlivost=50)
        mar2 = Marriage(partner_jmeno="Diana", den_zasnubin=1, den_svatby=1, stav="vdana", zarlivost=40)
        hra.marriage_system["Elena"] = mar1
        hra.marriage_system["Diana"] = mar2

        hra.hrac.sex_energy = 50
        with patch("builtins.input", return_value=""):
            spolecna_noc_manzelek(hra)

        self.assertLess(mar1.zarlivost, 50)
        self.assertLess(mar2.zarlivost, 40)

    def test_svet_nove_mestske_lokace(self):
        from game.svet import LOKACE, NPC
        self.assertIn("chram_cistoty", LOKACE)
        self.assertIn("tajna_svatyne_stinu", LOKACE)
        self.assertIn("zahradni_altan", LOKACE)

        self.assertIn("vladyka_aurelius", NPC)
        self.assertIn("stinovy_mistr_kage", NPC)
        self.assertIn("knezka_valeria", NPC)


if __name__ == "__main__":
    unittest.main()


