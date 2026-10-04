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
from game.save_load import Hra, nacti_hru, nacti_slot, uloz_hru, uloz_slot
from game.settings import NastaveniHry
from game.souboje import BOSSOVE, Nepritel, Souboj
from main import nova_hra
from models.otrokyne import Otrokyně
from utils.vypis import barva, hlavicka, vytiskni_volbu


class HraTesty(unittest.TestCase):
    def test_nova_hra_ma_dve_dospele_postavy_a_defaulty(self):
        hra = nova_hra()
        self.assertEqual(len(hra.harem.otrokyne), 2)
        self.assertTrue(all(otrok.vek >= 18 for otrok in hra.harem.otrokyne))
        self.assertEqual(len({otrok.jmeno.casefold() for otrok in hra.harem.otrokyne}), 2)
        from data.charaktery import CHARAKTERY
        self.assertTrue(all(otrok.charakter in CHARAKTERY for otrok in hra.harem.otrokyne))
        self.assertEqual(hra.nastaveni.obtiznost, "normalni")

    def test_generator_jmen_a_legacy_aliasy_charakteru(self):
        from data.charaktery import CHARAKTERY, normalizuj_charakter, vyber_charakter
        from data.jmena import vyber_nove_jmeno

        obsazena = [Otrokyně("Aurelia"), Otrokyně("Nela")]
        nove_jmeno = vyber_nove_jmeno(obsazena)
        self.assertNotIn(nove_jmeno.casefold(), {o.jmeno.casefold() for o in obsazena})
        self.assertIn(vyber_charakter(), CHARAKTERY)
        self.assertEqual(normalizuj_charakter("Amazonka (bojovnice)"), "amazonka")
        self.assertEqual(normalizuj_charakter("Čarodějka"), "carodejka")

    def test_harem_a_statistiky_vykresluji_grafy_a_povahy(self):
        from game.harem_interakce import menu_haremu
        from game.statistiky import zobraz_statistiky

        hra = Hra()
        hra.harem.pridat(Otrokyně("Amálie", charakter="badatelka", duvera=75))
        vystup = io.StringIO()
        with patch("builtins.input", return_value="0"), redirect_stdout(vystup):
            menu_haremu(hra)
        self.assertIn("Zvídavá badatelka", vystup.getvalue())
        self.assertIn("█", vystup.getvalue())

        vystup = io.StringIO()
        with patch("builtins.input", return_value=""), redirect_stdout(vystup):
            zobraz_statistiky(hra)
        self.assertIn("Průměrná důvěra", vystup.getvalue())
        self.assertIn("Zvídavá badatelka", vystup.getvalue())
        self.assertIn("Postup XP", vystup.getvalue())

    def test_osobni_rozhovor_respektuje_volbu_a_zaznamena_historii(self):
        from game.harem_interakce import _osobni_akce

        hra = Hra()
        otrok = Otrokyně("Mira", charakter="badatelka", duvera=50, strach=20)
        with patch("builtins.input", side_effect=["11", "3", ""]), redirect_stdout(io.StringIO()):
            _osobni_akce(hra, otrok)
        self.assertGreater(otrok.duvera, 50)
        self.assertEqual(otrok.strach, 15)
        self.assertEqual(otrok.historie_voleb[-1]["typ"], "rozhovor")

    def test_osobni_pribeh_a_statistiky_se_ukladaji_a_vykresli_diary(self):
        from game.osobni_pribehy import pokracuj_v_pribehu, zobraz_denik_postavy
        from game.harem_interakce import zobraz_graf_statistik
        from data.charaktery import CHARAKTERY
        from game.osobni_pribehy import PRIBEHY

        self.assertEqual(set(PRIBEHY), set(CHARAKTERY))
        self.assertTrue(all(len(pribeh["sceny"]) == 3 for pribeh in PRIBEHY.values()))

        hra = Hra()
        otrok = Otrokyně("Alma", charakter="umelkyne", duvera=55, loajalita=45)
        hra.harem.pridat(otrok)
        with patch("builtins.input", side_effect=["1", "1", "2"]), redirect_stdout(io.StringIO()):
            for _ in range(3):
                self.assertTrue(pokracuj_v_pribehu(hra, otrok))
        self.assertTrue(otrok.osobni_pribeh_dokonceno)
        self.assertEqual(otrok.osobni_pribeh_krok, 3)
        self.assertEqual(len(otrok.osobni_pribeh_volby), 3)

        otrok.zaznamenej_statistiky(1)
        otrok.duvera = 90
        otrok.zaznamenej_statistiky(2)
        nactena = Otrokyně.from_dict(otrok.to_dict())
        self.assertEqual(nactena.osobni_pribeh_krok, 3)
        self.assertTrue(nactena.osobni_pribeh_dokonceno)
        self.assertEqual([bod["den"] for bod in nactena.historie_statistik], [1, 2])
        stara = Otrokyně.from_dict({"jmeno": "Stará členka"})
        self.assertEqual(stara.osobni_pribeh_krok, 0)
        self.assertFalse(stara.osobni_pribeh_dokonceno)
        self.assertEqual(stara.historie_statistik, [])

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            zobraz_denik_postavy(nactena)
            zobraz_graf_statistik(nactena)
        self.assertIn("umělkyně", vystup.getvalue().lower())
        self.assertIn("uzavřený příběh", vystup.getvalue().lower())
        self.assertIn("Důvěra", vystup.getvalue())
        self.assertIn("1 2", vystup.getvalue())

    def test_povahove_schopnosti_pusobi_v_prislusnych_systemech(self):
        from game.diplomacie import Diplomacie
        from game.souboje import Souboj
        from game.vyzkum import VyzkumSystem

        hra = Hra()
        badatelka = Otrokyně("Ada", charakter="badatelka", duvera=40)
        diplomatka = Otrokyně("Běla", charakter="diplomatka", duvera=50)
        ochranitelka = Otrokyně("Cora", charakter="ochranitelka", duvera=50)
        umelkyne = Otrokyně("Dora", charakter="umelkyne", duvera=40)
        for otrok in (badatelka, diplomatka, ochranitelka, umelkyne):
            hra.harem.pridat(otrok)

        vyzkum = VyzkumSystem()
        vyzkum.body = 10
        self.assertEqual(vyzkum.cena_vyzkumu(hra.hrac, "temna_magie", hra), 270)
        zlato_pred = hra.hrac.gold
        with redirect_stdout(io.StringIO()):
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "temna_magie", hra))
        self.assertEqual(hra.hrac.gold, zlato_pred - 270)

        diplomacie = Diplomacie(hra.frakce)
        hra.hrac.gold = 500
        with patch("random.randint", return_value=10), redirect_stdout(io.StringIO()):
            diplomacie.vyjednavat(hra.hrac, "obchodnici", "uplatek", hra)
        self.assertEqual(hra.frakce.frakce["obchodnici"].reputace, 22)

        hra.pevnost.bojova_partnerka = ochranitelka.jmeno
        souboj = Souboj(hra.hrac, hra.mafie, hra)
        self.assertEqual(souboj.hracova_obrana(), hra.hrac.skill_body + 5)
        self.assertEqual(
            hra.harem.pasivni_prijem(),
            10 * hra.harem.harem_level
            + sum(b.uroven * 3 for b in hra.harem.budovy.values())
            + sum(o.loajalita for o in hra.harem.vsechny_aktivni())
            // len(hra.harem.vsechny_aktivni())
            // 10
            + 5,
        )

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
        self.assertEqual(hra.hrac.gold, 47)
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

    def test_vyzkum_ma_vetve_predpoklady_slevy_a_ulozitelne_bonusy(self):
        hra = Hra()
        hra.hrac.gold = 5000
        vyzkum = hra.vyzkum
        vyzkum.body = 500

        dostupne, duvod = vyzkum.muzes_vyzkoumat(hra.hrac, "pokrocile_muceni", hra)
        self.assertFalse(dostupne)
        self.assertIn("Psychologie zlomení", duvod)

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            vyzkum.zobraz_vyzkum(hra.hrac, hra)
        self.assertIn("Technologický strom dominia", vystup.getvalue())
        self.assertIn("🔒 Uzamčeno", vystup.getvalue())
        self.assertIn("Hospodářství", vystup.getvalue())
        self.assertIn("Válečnictví", vystup.getvalue())

        gold_pred = hra.hrac.gold
        temno_pred = hra.hrac.max_temno()
        with redirect_stdout(io.StringIO()):
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "temna_magie", hra))
            self.assertFalse(vyzkum.vyzkoumat(hra.hrac, "temna_magie", hra))
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "psychologie_zlomeni", hra))
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "pokrocile_muceni", hra))
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "obchodni_sit", hra))
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "investicni_kruh", hra))
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "utajeni", hra))
            self.assertTrue(vyzkum.vyzkoumat(hra.hrac, "tajne_archivy", hra))

        self.assertEqual(hra.hrac.max_temno(), temno_pred + 20)
        self.assertEqual(hra.hrac.skilly["temnota"], 10)
        self.assertEqual(hra.hrac.vliv_inkvizice, 5)
        self.assertEqual(vyzkum.bonus_denniho_prijmu(), 40)
        self.assertEqual(vyzkum.sleva_vyzkumu(hra.hrac, hra), 5)
        self.assertEqual(vyzkum.cena_vyzkumu(hra.hrac, "dvojiti_agent", hra), 760)
        self.assertEqual(vyzkum.body, 500 - 10 - 15 - 25 - 10 - 15 - 8 - 12)
        self.assertEqual(gold_pred - hra.hrac.gold, 300 + 400 + 700 + 500 + 650 + 250 + 500 - 50)

        ulozena = Hra.from_dict(hra.to_dict())
        self.assertEqual(ulozena.vyzkum.bonus_denniho_prijmu(), 40)
        self.assertEqual(ulozena.vyzkum.sleva_vyzkumu(ulozena.hrac, ulozena), 5)
        self.assertEqual(ulozena.vyzkum.body, vyzkum.body)

    def test_laboratore_vyrabeji_vyzkumne_body_a_zobrazuji_produkci(self):
        hra = Hra()
        hra.pevnost.budovy["archiv"] = 2
        hra.pevnost.budovy["alchymisticka_laborator"] = 1
        self.assertEqual(hra.vyzkum.produkce_bodu_za_den(hra), 7)

        with redirect_stdout(io.StringIO()):
            vysledek = hra.pevnost.denni_produkce(hra)
        self.assertEqual(hra.vyzkum.body, 7)
        self.assertEqual(vysledek["vyzkum"], 7)
        self.assertTrue(any("7 výzkumných bodů" in zprava for zprava in vysledek["zpravy"]))

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            hra.vyzkum.zobraz_vyzkum(hra.hrac, hra)
        self.assertIn("Výzkumné body: 7", vystup.getvalue())
        self.assertIn("Produkce: +7 výzkumných bodů za den", vystup.getvalue())

    def test_vyzkum_vyzaduje_body_i_zlato_a_save_migruje_body(self):
        hra = Hra()
        hra.hrac.gold = 1000
        dostupne, duvod = hra.vyzkum.muzes_vyzkoumat(hra.hrac, "utajeni", hra)
        self.assertFalse(dostupne)
        self.assertIn("výzkumných bodů", duvod)

        hra.vyzkum.body = 8
        hra.hrac.gold = 0
        dostupne, duvod = hra.vyzkum.muzes_vyzkoumat(hra.hrac, "utajeni", hra)
        self.assertFalse(dostupne)
        self.assertIn("zlata", duvod)

        hra.hrac.gold = 1000
        with redirect_stdout(io.StringIO()):
            self.assertTrue(hra.vyzkum.vyzkoumat(hra.hrac, "utajeni", hra))
        self.assertEqual(hra.vyzkum.body, 0)
        self.assertEqual(Hra.from_dict({"vyzkum": {"ziskane": []}}).vyzkum.body, 0)
        self.assertEqual(
            Hra.from_dict({"vyzkum": {"ziskane": [], "body": "bad"}}).vyzkum.body,
            0,
        )

    def test_vyzkum_valecne_bonusy_se_projevi_v_souboji(self):
        from game.souboje import Souboj

        hra = Hra()
        hra.hrac.gold = 2000
        hra.vyzkum.body = 25
        souboj = Souboj(hra.hrac, hra.mafie, hra)
        utok_pred = souboj.hracuv_utok()
        obrana_pred = souboj.hracova_obrana()
        with redirect_stdout(io.StringIO()):
            self.assertTrue(hra.vyzkum.vyzkoumat(hra.hrac, "vojenska_taktika", hra))
            self.assertTrue(hra.vyzkum.vyzkoumat(hra.hrac, "disciplinovana_legie", hra))
        self.assertEqual(souboj.hracuv_utok() - utok_pred, 12)
        self.assertEqual(souboj.hracova_obrana() - obrana_pred, 4)

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
        self.assertFalse(hra.nastaveni.vyvojarsky_rezim)

    def test_vyvojarsky_rezim_se_uklada_a_stary_save_jej_ma_vypnuty(self):
        hra = Hra()
        hra.nastaveni.vyvojarsky_rezim = True
        with tempfile.TemporaryDirectory() as slozka:
            cesta = Path(slozka) / "developer-mode.json"
            with redirect_stdout(io.StringIO()):
                self.assertTrue(uloz_hru(hra, cesta))
                nactena = nacti_hru(cesta)

        self.assertIsNotNone(nactena)
        self.assertTrue(nactena.nastaveni.vyvojarsky_rezim)
        self.assertFalse(NastaveniHry.from_dict({"barvy": True}).vyvojarsky_rezim)

    def test_menu_nastaveni_preklopi_vyvojarsky_rezim(self):
        from main import menu_nastaveni

        hra = Hra()
        with patch("builtins.input", side_effect=["7", "2", "", "7", "5", "", "6", "", "0"]), redirect_stdout(
            io.StringIO()
        ):
            menu_nastaveni(hra)
        self.assertTrue(hra.nastaveni.vyvojarsky_rezim)
        self.assertEqual(hra.nastaveni.styl_menu, "mrizka")

    def test_styl_menu_a_skin_se_ukladaji_a_meni_vzhled_menu(self):
        import config
        from game.menu_hlavni import vykresli_hlavni_menu

        hra = Hra()
        puvodni_tema = config.CURRENT_THEME
        puvodni_barvy = config.USE_COLORS
        try:
            hra.nastaveni.styl_menu = "seznam"
            hra.nastaveni.tema = "azurovy_kristal"
            hra.nastaveni.aplikuj()
            self.assertEqual(
                str(config.CYAN),
                config.THEMES["azurovy_kristal"]["barvy"]["CYAN"],
            )
            nactena_nastaveni = NastaveniHry.from_dict(hra.nastaveni.to_dict())
            self.assertEqual(nactena_nastaveni.styl_menu, "seznam")
            self.assertEqual(nactena_nastaveni.tema, "azurovy_kristal")
            nactena_hra = Hra.from_dict(hra.to_dict())
            self.assertEqual(nactena_hra.nastaveni.styl_menu, "seznam")
            self.assertEqual(nactena_hra.nastaveni.tema, "azurovy_kristal")
            self.assertEqual(NastaveniHry.from_dict({}).styl_menu, "kategorie")

            vystup = io.StringIO()
            with redirect_stdout(vystup):
                vykresli_hlavni_menu(hra)
            text = vystup.getvalue()
            self.assertIn("HLAVNÍ MENU — VŠECHNY VOLBY", text)
            self.assertNotIn("HARÉM & VZTAHY", text)

            hra.nastaveni.styl_menu = "kompaktni"
            vystup = io.StringIO()
            with redirect_stdout(vystup):
                vykresli_hlavni_menu(hra)
            self.assertIn("Kompaktní", hra.nastaveni.styl_menu_text)
            self.assertIn("📜 HLAVNÍ MENU", vystup.getvalue())

            from game.settings import STYLY_MENU
            for styl in STYLY_MENU:
                hra.nastaveni.styl_menu = styl
                vystup = io.StringIO()
                with redirect_stdout(vystup):
                    vykresli_hlavni_menu(hra)
                text = vystup.getvalue()
                self.assertTrue(
                    all(f"{cislo:>2})" in text for cislo in range(1, 32)),
                    f"Menu style {styl} omitted an option",
                )
                if styl == "kategorie":
                    self.assertIn("HARÉM & VZTAHY", text)

            for tema, informace in config.THEMES.items():
                hra.nastaveni.tema = tema
                hra.nastaveni.aplikuj()
                self.assertEqual(str(config.CYAN), informace["barvy"]["CYAN"])
                self.assertEqual(
                    NastaveniHry.from_dict(hra.nastaveni.to_dict()).tema,
                    tema,
                )
        finally:
            config.set_colors_enabled(puvodni_barvy)
            config.apply_theme(puvodni_tema)
            hra.nastaveni.tema = puvodni_tema
            hra.nastaveni.barvy = puvodni_barvy

    def test_obtiznost_meni_silu_a_odmenu(self):
        self.assertLess(
            profil_obtiznosti("lehka")["nepritel"],
            profil_obtiznosti("normalni")["nepritel"],
        )
        self.assertGreater(
            profil_obtiznosti("tezka")["odmena"],
            profil_obtiznosti("normalni")["odmena"],
        )

    def test_npc_ukol_a_zvolena_vetev_preziji_save_load(self):
        from game.balance import uprav_odmenu

        hra = Hra()
        hra.svet.vztahy_npc["mira"] = 100
        hra.npc_questy.dokoncene["mira"] = 1
        self.assertTrue(hra.npc_questy.prijmi(hra, "mira"))
        self.assertEqual(
            hra.npc_questy.aktivni["mira"]["quest"]["nazev"],
            "Dům bez řetězů",
        )

        with tempfile.TemporaryDirectory() as slozka:
            cesta = Path(slozka) / "quest-save.json"
            with redirect_stdout(io.StringIO()):
                self.assertTrue(uloz_hru(hra, cesta))
                nactena = nacti_hru(cesta)

        self.assertIsNotNone(nactena)
        self.assertEqual(
            nactena.npc_questy.aktivni["mira"]["quest"]["nazev"],
            "Dům bez řetězů",
        )
        zlato_pred = nactena.hrac.gold
        self.assertEqual(
            nactena.npc_questy.dokoncit(nactena, "mira", temna=True),
            "temna",
        )
        self.assertEqual(
            nactena.hrac.gold - zlato_pred,
            uprav_odmenu(340, nactena.nastaveni.obtiznost),
        )
        self.assertEqual(
            nactena.hrac.inventar.pocet_predmetu("balzam_stinu"), 1
        )
        self.assertEqual(nactena.npc_questy.dokoncene["mira"], 2)

    def test_stary_save_s_aktivnim_npc_ukolem_dokonci_spravnou_retezovou_cast(self):
        from game.npc_questy import NPCQuestSystem

        hra = Hra()
        hra.svet.vztahy_npc["mira"] = 100
        hra.npc_questy = NPCQuestSystem.from_dict({
            "aktivni": {"mira": {"npc_id": "mira", "pokrok": 0, "temna": False}},
            "dokoncene": {"mira": 1},
        })
        zlato_pred = hra.hrac.gold

        self.assertEqual(hra.npc_questy.dokoncit(hra, "mira"), "normal")
        self.assertEqual(hra.hrac.gold - zlato_pred, 260)
        self.assertEqual(
            hra.hrac.inventar.pocet_predmetu("zdravotni_balicek"), 1
        )

    def test_odmeny_questu_respektuji_obtiznost_a_nejsou_druhe_vyplaty(self):
        from game.balance import uprav_odmenu, uprav_xp
        from game.questy import QuestSystem
        from game.menu_hlavni import vykresli_hlavni_menu

        hra = Hra()
        hra.nastaveni.obtiznost = "tezka"
        hra.hrac.gold = 0
        quest = {
            "nazev": "Kontrolní úkol",
            "popis": "Test odměn.",
            "typ": "pomoc",
            "narocnost": 2,
            "odmena_zlato": 100,
            "riziko": 0,
            "doba_trvani": 1,
        }
        hra.questy = QuestSystem()
        hra.questy.aktivni_quest = quest
        hra.questy.dny_zbyva = 1

        with patch("random.random", return_value=0.99), redirect_stdout(io.StringIO()):
            hra.questy.proved_quest(hra.hrac, hra.harem, hra.mafie, hra)

        odmena = uprav_odmenu(100, "tezka")
        bonus = uprav_odmenu(25 + 2 * 12, "tezka")
        self.assertEqual(hra.hrac.gold, odmena + bonus)
        self.assertEqual(hra.hrac.bonus_za_questy, bonus)
        self.assertEqual(hra.hrac.xp, uprav_xp(20 + 2 * 10, "tezka"))
        self.assertFalse(hra.questy.aktivni_quest)

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            vykresli_hlavni_menu(hra)
        self.assertIn("Quest bonus získaný celkem", vystup.getvalue())
        self.assertNotIn("k dispozici", vystup.getvalue())

    def test_odmeny_npc_ukolu_respektuji_obtiznost(self):
        from game.balance import uprav_odmenu, uprav_xp

        hra = Hra()
        hra.nastaveni.obtiznost = "tezka"
        hra.svet.vztahy_npc["radan"] = 100
        self.assertTrue(hra.npc_questy.prijmi(hra, "radan"))
        zlato_pred = hra.hrac.gold
        xp_pred = hra.hrac.xp

        hra.npc_questy.dokoncit(hra, "radan")

        self.assertEqual(
            hra.hrac.gold - zlato_pred, uprav_odmenu(110, "tezka")
        )
        self.assertEqual(
            hra.hrac.xp - xp_pred, uprav_xp(30, "tezka")
        )

    def test_spolecne_menu_nadpisy_a_volby_maji_ikonografii(self):
        vystup = io.StringIO()
        with redirect_stdout(vystup):
            hlavicka("Menu nastavení")
            vytiskni_volbu("0", "Zpět")
            vytiskni_volbu("1", "Vybrat arénový souboj")
        text = vystup.getvalue()
        self.assertIn("⚙️", text)
        self.assertIn("↩️", text)
        self.assertIn("⚔️", text)

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

    def test_nova_uzemi_a_nelegalni_podniky_zvysuji_prijem_a_ukladaji_se(self):
        from game.mafie import DOSTUPNA_UZEMI, koupit_uzemi, spravovat_podniky_uzemi

        hra = Hra()
        hra.hrac.gold = 5000
        nove_lokace = {"Černá čtvrť", "Říční nábřeží", "Univerzitní okrsek"}
        self.assertTrue(nove_lokace.issubset({u[0] for u in DOSTUPNA_UZEMI}))
        self.assertTrue(koupit_uzemi(hra.hrac, hra.mafie, "Černá čtvrť"))

        for _ in range(3):
            with patch("builtins.input", side_effect=["1", "5"]), redirect_stdout(
                io.StringIO()
            ):
                spravovat_podniky_uzemi(hra.hrac, hra.mafie)

        podniky = hra.mafie.uzemi[0].podniky
        self.assertEqual(
            set(podniky),
            {"paseracky_sklad", "padelatelska_dilna", "tajna_arena"},
        )
        self.assertEqual(hra.mafie.vypocet_prijmu(), 130 * 50 // 100 + 75 + 60 + 85)

        nactena = Hra.from_dict(hra.to_dict())
        self.assertEqual(nactena.mafie.vypocet_prijmu(), hra.mafie.vypocet_prijmu())
        self.assertEqual(set(nactena.mafie.uzemi[0].podniky), set(podniky))

    def test_expanzni_ctvrti_reaguji_frakce_a_zobrazi_se_v_siti(self):
        from game.mafie import (
            DOSTUPNA_UZEMI, KATALOG_PODNIKU, koupit_uzemi,
            vykresli_mapu_uzemi,
        )

        hra = Hra()
        hra.hrac.gold = 5000
        nove_ctvrti = {
            "Dýmová čtvrť", "Cechovní uličky", "Půlnoční trh",
            "Staré katakomby", "Kovárenský okrsek", "Lucernová čtvrť",
            "Severní hradby", "Akademické náměstí",
        }
        dostupne = {uzemi[0] for uzemi in DOSTUPNA_UZEMI}
        self.assertTrue(nove_ctvrti.issubset(dostupne))
        self.assertTrue({
            "informacni_burza", "cerna_slvarna", "falesny_archiv",
        }.issubset(KATALOG_PODNIKU))
        reputace_pred = hra.frakce.frakce["obchodnici"].reputace
        self.assertTrue(koupit_uzemi(hra.hrac, hra.mafie, "Akademické náměstí", hra))
        self.assertEqual(
            hra.frakce.frakce["obchodnici"].reputace, reputace_pred + 2
        )

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            vykresli_mapu_uzemi(hra.mafie)
        self.assertIn("Městská síť: 16 čtvrtí", vystup.getvalue())
        self.assertIn("Akademické náměstí", vystup.getvalue())

    def test_nove_technologie_posiluji_vyzkum_a_prijem_uzemi(self):
        from game.vyzkum import VYZKUM
        from models.mafie import Uzemi

        hra = Hra()
        hra.mafie.uzemi.append(Uzemi("Přístav", 100, 50, 5))
        hra.vyzkum.ziskane.update({
            "dvojiti_agent", "monopolni_smlouvy",
            "sit_informatoru", "ucty_podsveti",
        })
        self.assertIn("sit_informatoru", VYZKUM)
        self.assertIn("ucty_podsveti", VYZKUM)
        self.assertEqual(hra.vyzkum.produkce_bodu_za_den(hra), 1)
        self.assertEqual(hra.vyzkum.bonus_denniho_prijmu(hra), 50)

    def test_vitezstvi_nad_bossem_prinasi_vyzkum(self):
        from game.mafie import koupit_uzemi, valka_uzemi
        from models.mafie import Mafie

        hra = Hra()
        hra.hrac.gold = 5000
        koupit_uzemi(hra.hrac, hra.mafie, "Přístav")
        hra.mafie.vojaci = 100
        body_pred = hra.vyzkum.body
        vystup = io.StringIO()
        with patch("builtins.input", side_effect=["5", "1"]), patch(
            "random.randint", return_value=1
        ), redirect_stdout(vystup):
            valka_uzemi(hra.hrac, hra.mafie, hra)

        self.assertEqual(hra.vyzkum.body, body_pred + 8)
        self.assertIn("Železný baron Vargan", vystup.getvalue())
        self.assertIn("zelezny_baron_vargan", hra.mafie.bossove_porazeni)
        self.assertEqual(
            Mafie.from_dict({"uzemi": []}).bossove_porazeni, []
        )

        nactena = Hra.from_dict(hra.to_dict())
        self.assertEqual(
            nactena.mafie.bossove_porazeni,
            ["zelezny_baron_vargan"],
        )
        zlato_po_vitezstvi = nactena.hrac.gold
        body_po_vitezstvi = nactena.vyzkum.body
        vystup = io.StringIO()
        with patch("builtins.input", return_value="5"), redirect_stdout(vystup):
            valka_uzemi(nactena.hrac, nactena.mafie, nactena)
        self.assertEqual(nactena.hrac.gold, zlato_po_vitezstvi)
        self.assertEqual(nactena.vyzkum.body, body_po_vitezstvi)
        self.assertIn("už byl poražen", vystup.getvalue())

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

    def test_spravovat_mafii_menu_bez_padu(self):
        from game.mafie import spravovat_mafii
        hra = Hra()
        with patch("builtins.input", return_value="0"):
            spravovat_mafii(hra)

    def test_graficka_sit_mafie_zobrazuje_kontrolu_a_podniky(self):
        from game.mafie import koupit_uzemi, spravovat_mafii

        hra = Hra()
        hra.hrac.gold = 2000
        koupit_uzemi(hra.hrac, hra.mafie, "Přístav")
        hra.mafie.uzemi[0].podniky["tajne_doupe"] = {
            "nazev": "Tajné drogové doupě",
            "prijem": 45,
        }
        vystup = io.StringIO()
        with patch("builtins.input", return_value="0"), redirect_stdout(vystup):
            spravovat_mafii(hra)

        text = vystup.getvalue()
        self.assertIn("SÍŤ PODSVĚTÍ", text)
        self.assertIn("Přístav", text)
        self.assertIn("50%", text)
        self.assertIn("Tajné drogové doupě", text)
        self.assertIn("+45 zl/den", text)

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
        self.assertIn("Ztracená zásilka z Dýmové čtvrti", nazvy)
        self.assertIn("Dlužní kniha Půlnočního trhu", nazvy)
        self.assertIn("Tajemství akademického sklepení", nazvy)
        self.assertIn("Zapečetěná brána katakomb", nazvy)

    def test_uzemni_quest_vyzaduje_ctvrt_a_odmenuje_vyzkumem(self):
        from game.questy import QuestSystem, QUESTY
        from models.mafie import Uzemi

        hra = Hra()
        quest = next(
            q for q in QUESTY
            if q["nazev"] == "Ztracená zásilka z Dýmové čtvrti"
        )
        hra.questy = QuestSystem()
        hra.questy.aktivni_quest = quest
        hra.questy.dny_zbyva = 1
        hra.svet.aktualni_lokace = "pristav"
        body_pred = hra.vyzkum.body
        with redirect_stdout(io.StringIO()):
            hra.questy.proved_quest(hra.hrac, hra.harem, hra.mafie, hra)
        self.assertEqual(hra.questy.aktivni_quest, quest)
        self.assertEqual(hra.questy.dny_zbyva, 1)

        hra.mafie.uzemi.append(Uzemi("Dýmová čtvrť", 160, 50, obsazeno=True))
        with patch("game.questy.random.random", return_value=1), redirect_stdout(
            io.StringIO()
        ):
            hra.questy.proved_quest(hra.hrac, hra.harem, hra.mafie, hra)
        self.assertIsNone(hra.questy.aktivni_quest)
        self.assertEqual(hra.vyzkum.body, body_pred + 4)

    def test_generovani_questu_neodemyka_nevlastnena_uzemi(self):
        from game.questy import QUESTY, QuestSystem

        hra = Hra()
        hra.hrac.level = 20
        hra.svet.odhalene_lokace.append("pristav")
        system = QuestSystem()
        zachycene = {}

        def vyber_questu(questy):
            zachycene["nazvy"] = [q["nazev"] for q in questy]
            return questy[0]

        with patch("game.questy.random.choice", side_effect=vyber_questu), redirect_stdout(
            io.StringIO()
        ):
            system.generuj_quest(hra.hrac, hra)

        uzemni_questy = {
            q["nazev"] for q in QUESTY if q.get("pozadovane_uzemi")
        }
        self.assertTrue(uzemni_questy.isdisjoint(zachycene["nazvy"]))

    def test_informacni_burza_odemyka_udalost_s_vyzkumnou_odmenou(self):
        from game.udalosti import spust_nahodnou_udalost
        from models.mafie import Uzemi

        hra = Hra()
        hra.mafie.uzemi.append(Uzemi(
            "Přístav", 100, 50, obsazeno=True,
            podniky={"informacni_burza": {"nazev": "Burza"}},
        ))
        vybrane = {}

        def vyber_udalost(udalosti, weights, k):
            vybrane["nazvy"] = [udalost["nazev"] for udalost in udalosti]
            return [next(
                udalost for udalost in udalosti
                if udalost["nazev"] == "Tip z městské informační burzy"
            )]

        body_pred = hra.vyzkum.body
        with patch("game.udalosti.random.random", return_value=0), patch(
            "game.udalosti.random.choices", side_effect=vyber_udalost
        ), patch("game.udalosti.random.randint", return_value=3), redirect_stdout(
            io.StringIO()
        ):
            spust_nahodnou_udalost(hra)

        self.assertIn("Zátah na nelegální podnik", vybrane["nazvy"])
        self.assertEqual(hra.vyzkum.body, body_pred + 3)

    def test_hlavni_menu_zkratky_a_zobrazeni_testovaci_volby(self):
        from game.menu_hlavni import (
            MAPOVANI_CISEL_MENU,
            normalizuj_volbu,
            vykresli_hlavni_menu,
        )
        from main import (
            _obnov_hru_runtime,
            _obsluz_volbu_hlavniho_menu,
            hlavni_menu,
            start,
        )
        hra = Hra()

        self.assertEqual(normalizuj_volbu("t"), "test")
        self.assertEqual(normalizuj_volbu("10"), "11")
        self.assertEqual(normalizuj_volbu("31"), "32")
        self.assertEqual(normalizuj_volbu("s"), "26")
        self.assertEqual(
            list(MAPOVANI_CISEL_MENU),
            [str(cislo) for cislo in range(1, 32)],
        )
        self.assertEqual(normalizuj_volbu("$"), "cheat")
        self.assertEqual(normalizuj_volbu("&"), "cheat_suroviny")
        self.assertEqual(normalizuj_volbu("#"), "cheat_dovednosti")
        self.assertEqual(normalizuj_volbu("*"), "cheat_budovy")
        self.assertEqual(normalizuj_volbu(":"), "cheat_loajalita")
        self.assertEqual(normalizuj_volbu("neznama"), "neznama")

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            vykresli_hlavni_menu(hra)
        self.assertNotIn("T) 🧪 Testovací otrokyně", vystup.getvalue())
        self.assertNotIn("$) 💰 Cheat:", vystup.getvalue())
        self.assertNotIn("&) 🧪 Cheat:", vystup.getvalue())
        self.assertNotIn("#) 📈 Cheat:", vystup.getvalue())
        self.assertNotIn("*) 🏗️ Cheat:", vystup.getvalue())
        self.assertNotIn(":) 💚 Cheat:", vystup.getvalue())
        self.assertIn("10)", vystup.getvalue())
        self.assertIn("🎯 Lov otrokyň", vystup.getvalue())
        self.assertIn("31)", vystup.getvalue())
        self.assertIn("📅 Kalendář a události", vystup.getvalue())

        zlato_pred = hra.hrac.gold
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("$"), _obnov_hru_runtime(hra)
            )
        self.assertEqual(hra.hrac.gold, zlato_pred)
        self.assertEqual(hra.harem.pocet(), 0)

        hra_bez_developer = Hra()
        otrok = Otrokyně("Nízká loajalita", loajalita=20)
        hra_bez_developer.harem.pridat(otrok)
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra_bez_developer, normalizuj_volbu(":"),
                _obnov_hru_runtime(hra_bez_developer)
            )
        self.assertEqual(otrok.loajalita, 20)

        suroviny_pred = dict(hra.alchymie.suroviny)
        zasoby_pevnosti_pred = {
            atribut: getattr(hra.pevnost, atribut)
            for atribut in ("zasoby", "drevo", "kamen", "zelezo", "krystaly")
        }
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("&"), _obnov_hru_runtime(hra)
            )
        self.assertEqual(hra.alchymie.suroviny, suroviny_pred)
        self.assertEqual(
            {
                atribut: getattr(hra.pevnost, atribut)
                for atribut in zasoby_pevnosti_pred
            },
            zasoby_pevnosti_pred,
        )
        dovednosti_pred = dict(hra.hrac.skilly)
        skill_body_pred = hra.hrac.skill_body
        vyzkum_body_pred = hra.vyzkum.body
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("#"), _obnov_hru_runtime(hra)
            )
        self.assertEqual(hra.hrac.skilly, dovednosti_pred)
        self.assertEqual(hra.hrac.skill_body, skill_body_pred)
        budovy_pred = dict(hra.pevnost.budovy)
        uroven_citadely_pred = hra.pevnost.uroven
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("*"), _obnov_hru_runtime(hra)
            )
        self.assertEqual(hra.pevnost.budovy, budovy_pred)
        self.assertEqual(hra.pevnost.uroven, uroven_citadely_pred)

        hra.nastaveni.vyvojarsky_rezim = True
        vystup = io.StringIO()
        with redirect_stdout(vystup):
            vykresli_hlavni_menu(hra)
        self.assertIn("T)", vystup.getvalue())
        self.assertIn("🧪 Testovací otrokyně", vystup.getvalue())
        self.assertIn("$) 💰 Cheat:", vystup.getvalue())
        self.assertIn("&) 🧪 Cheat:", vystup.getvalue())
        self.assertIn("#) 📈 Cheat:", vystup.getvalue())
        self.assertIn("*) 🏗️ Cheat:", vystup.getvalue())
        self.assertIn(
            ":) 💚 Cheat: loajalita, důvěra a romance všech otrokyň na maximum",
            vystup.getvalue(),
        )

        hra_cheat = Hra()
        hra_cheat.nastaveni.vyvojarsky_rezim = True
        hra_cheat.harem.pridat(Otrokyně("První", loajalita=20))
        hra_cheat.harem.pridat(Otrokyně("Druhá", loajalita=75))
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra_cheat, normalizuj_volbu(":"),
                _obnov_hru_runtime(hra_cheat)
            )
        self.assertTrue(all(
            o.loajalita == 100 and o.duvera == 100 and o.romance_body == 100
            for o in hra_cheat.harem.otrokyne
        ))

        for volba in ("t",):
            hra = Hra()
            hra.nastaveni.vyvojarsky_rezim = True
            with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
                _obsluz_volbu_hlavniho_menu(
                    hra, normalizuj_volbu(volba), _obnov_hru_runtime(hra)
                )
            self.assertEqual(hra.harem.pocet(), 1)

        hra = Hra()
        hra.nastaveni.vyvojarsky_rezim = True
        hra.hrac.gold = 321
        hra.hrac.sex_energy = 0
        hra.hrac.dark_energy = 0
        hra.hrac.max_sex_energy = 130
        hra.hrac.max_dark_energy = 125
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("$"), _obnov_hru_runtime(hra)
            )
        self.assertEqual(hra.hrac.gold, 10_321)
        self.assertEqual(hra.hrac.sex_energy, 130)
        self.assertEqual(hra.hrac.dark_energy, 125)

        from game.alchymie import SUROVINY
        hra.alchymie.suroviny["bylina_mesicni"] = 17
        zasoby_pevnosti_pred = {
            atribut: getattr(hra.pevnost, atribut)
            for atribut in ("zasoby", "drevo", "kamen", "zelezo", "krystaly")
        }
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("&"), _obnov_hru_runtime(hra)
            )
        self.assertEqual(hra.alchymie.suroviny["bylina_mesicni"], 1_017)
        self.assertTrue(all(
            hra.alchymie.suroviny.get(surovina_id) == 1_000
            for surovina_id in SUROVINY
            if surovina_id != "bylina_mesicni"
        ))
        for atribut, puvodni in zasoby_pevnosti_pred.items():
            self.assertEqual(getattr(hra.pevnost, atribut), puvodni + 1_000)

        dovednosti_pred = dict(hra.hrac.skilly)
        skill_body_pred = hra.hrac.skill_body
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("#"), _obnov_hru_runtime(hra)
            )
        self.assertTrue(all(
            hra.hrac.skilly[klic] == hodnota + 10
            for klic, hodnota in dovednosti_pred.items()
        ))
        self.assertEqual(hra.hrac.skill_body, skill_body_pred + 10)
        self.assertEqual(hra.vyzkum.body, vyzkum_body_pred + 10)

        from models.fortress import PEVNOSTNI_BUDOVY
        hra.pevnost.budovy["pila"] = 3
        uroven_citadely_pred = hra.pevnost.uroven
        with patch("builtins.input", return_value=""), redirect_stdout(io.StringIO()):
            _obsluz_volbu_hlavniho_menu(
                hra, normalizuj_volbu("*"), _obnov_hru_runtime(hra)
            )
        self.assertEqual(hra.pevnost.budovy["pila"], 4)
        self.assertTrue(all(
            hra.pevnost.budovy[budova_id] >= 1
            for budova_id in PEVNOSTNI_BUDOVY
        ))
        self.assertEqual(hra.pevnost.uroven, uroven_citadely_pred + 1)

        vystup = io.StringIO()
        with patch("builtins.input", side_effect=["neplatne", "0"]), redirect_stdout(vystup):
            start()
        self.assertIn("Neplatná volba.", vystup.getvalue())

        hra = Hra()
        hra.harem.pridat(Otrokyně("Alena"))
        with patch("builtins.input", side_effect=["1", EOFError]), patch(
            "main.uloz_hru"
        ) as uloz, redirect_stdout(io.StringIO()):
            hlavni_menu(hra)
        uloz.assert_called_once_with(hra)

    def test_hlavni_menu_doporucuje_konretni_cil_a_podminky_postupu(self):
        from game.cile_hry import prehled_cilu
        from game.pruvodce import _doporuceni
        from game.menu_hlavni import vykresli_hlavni_menu

        hra = Hra()
        prehled = prehled_cilu(hra)
        self.assertIn("Kampaň 1/5", prehled["aktivni"][0])
        self.assertIn("Mapa (8)", prehled["doporuceni"])
        self.assertIn("Starý trh", prehled["doporuceni"])
        self.assertEqual(_doporuceni(hra)[0], prehled["doporuceni"])
        self.assertTrue(any("volbě 3" in tip for tip in _doporuceni(hra)))

        hra.questy.aktivni_quest = {
            "nazev": "Zpráva pro Miru",
            "lokace": "trh",
        }
        hra.questy.dny_zbyva = 2
        prehled = prehled_cilu(hra)
        self.assertTrue(any(cil.startswith("Úkol: Zpráva pro Miru") for cil in prehled["aktivni"]))
        self.assertIn("zbývá 2 dní", prehled["doporuceni"])
        self.assertIn("Mapa (8)", prehled["doporuceni"])

        hra.questy.aktivni_quest = None
        hra.kampan.kapitola = 4
        if "observator" not in hra.svet.odhalene_lokace:
            hra.svet.odhalene_lokace.append("observator")
        hra.svet.aktualni_lokace = "observator"
        prehled = prehled_cilu(hra)
        self.assertIn("Souboj (17)", prehled["doporuceni"])
        hra.kampan.boss_porazeni.append("strazce_hvezdne_brany")
        self.assertIn("Kampaň (9)", prehled_cilu(hra)["doporuceni"])

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            vykresli_hlavni_menu(hra)
        self.assertIn("AKTIVNÍ CÍLE A DOPORUČENÝ KROK", vystup.getvalue())
        self.assertIn("vyber závěr příběhu", vystup.getvalue())

    def test_denik_ukolu_zobrazuje_stav_bez_zmeny_hry(self):
        from game.denik_ukolu import zobraz_denik_ukolu
        from game.questy import QuestSystem

        hra = Hra()
        hra.svet.vztahy_npc["mira"] = 100
        self.assertTrue(hra.npc_questy.prijmi(hra, "mira"))
        hra.questy = QuestSystem()
        hra.questy.aktivni_quest = {
            "nazev": "Zkouška deníku",
            "popis": "Kontrolní popis úkolu.",
            "odmena_zlato": 120,
            "riziko": 0.25,
            "lokace": "trh",
        }
        hra.questy.dny_zbyva = 2
        stav_pred = hra.to_dict()
        vystup = io.StringIO()
        with redirect_stdout(vystup):
            zobraz_denik_ukolu(hra)

        text = vystup.getvalue()
        self.assertIn("Deník úkolů", text)
        self.assertIn("Zkouška deníku", text)
        self.assertIn("Léky pro poutníky", text)
        self.assertIn("Hlavní kampaň", text)
        self.assertEqual(hra.to_dict(), stav_pred)

    def test_pruvodce_dava_doporuceni_a_nemeni_hru(self):
        from game.pruvodce import zobraz_pruvodce

        hra = Hra()
        stav_pred = hra.to_dict()
        vystup = io.StringIO()
        with redirect_stdout(vystup):
            zobraz_pruvodce(hra)

        text = vystup.getvalue()
        self.assertIn("Průvodce dominiem", text)
        self.assertIn("Doporučení pro tuto hru", text)
        self.assertIn("volbě 3", text)
        self.assertEqual(hra.to_dict(), stav_pred)

    def test_nahodne_udalosti_se_ridi_lokaci_a_zapisuji_do_kalendare(self):
        from game.udalosti import spust_nahodnou_udalost

        hra = Hra()
        hra.kalendar.den = 8
        vyber = {}

        def vyber_udalost(udalosti, weights, k):
            vyber["nazvy"] = [udalost["nazev"] for udalost in udalosti]
            vyber["weights"] = weights
            return [next(
                udalost for udalost in udalosti
                if udalost["nazev"] == "Inkvizice je blízko"
            )]

        with patch("game.udalosti.random.random", return_value=0), patch(
            "game.udalosti.random.choices", side_effect=vyber_udalost
        ), patch("game.udalosti.random.randint", return_value=3), redirect_stdout(
            io.StringIO()
        ):
            spust_nahodnou_udalost(hra)

        self.assertNotIn("Večer světel", vyber["nazvy"])
        self.assertNotIn("Signál z věže", vyber["nazvy"])
        self.assertNotIn("Tichá sklizeň", vyber["nazvy"])
        self.assertNotIn("Nemoc otrokyně", vyber["nazvy"])
        self.assertEqual(
            hra.kalendar.udalosti[-1],
            {"den": hra.hrac.den, "udalost": "Inkvizice je blízko"},
        )
        nactena = Hra.from_dict(hra.to_dict())
        self.assertEqual(nactena.kalendar.udalosti[-1], hra.kalendar.udalosti[-1])

    def test_jaro_zvysi_dostupnost_udalosti_tiche_sklizne(self):
        from game.udalosti import spust_nahodnou_udalost

        hra = Hra()
        hra.kalendar.den = 1
        zachycene = {}

        def vyber_udalost(udalosti, weights, k):
            zachycene["nazvy"] = [udalost["nazev"] for udalost in udalosti]
            zachycene["weights"] = dict(
                zip(zachycene["nazvy"], weights)
            )
            return [next(
                udalost for udalost in udalosti
                if udalost["nazev"] == "Inkvizice je blízko"
            )]

        with patch("game.udalosti.random.random", return_value=0), patch(
            "game.udalosti.random.choices", side_effect=vyber_udalost
        ), patch("game.udalosti.random.randint", return_value=3), redirect_stdout(
            io.StringIO()
        ):
            spust_nahodnou_udalost(hra)

        self.assertIn("Tichá sklizeň", zachycene["nazvy"])
        self.assertEqual(zachycene["weights"]["Tichá sklizeň"], 1)

    def test_hrozby_a_stav_haremu_vyvazuji_udalosti(self):
        from game.udalosti import spust_nahodnou_udalost

        hra = Hra()
        otrokyne = Otrokyně("Nela", loajalita=20, hp=30)
        hra.harem.pridat(otrokyne)
        hra.hrac.vliv_inkvizice = 80
        zachycene = {}

        def vyber_udalost(udalosti, weights, k):
            zachycene.update(dict(
                zip((udalost["nazev"] for udalost in udalosti), weights)
            ))
            return [next(
                udalost for udalost in udalosti
                if udalost["nazev"] == "Inkvizice je blízko"
            )]

        with patch("game.udalosti.random.random", return_value=0), patch(
            "game.udalosti.random.choices", side_effect=vyber_udalost
        ), patch("game.udalosti.random.randint", return_value=3), redirect_stdout(
            io.StringIO()
        ):
            spust_nahodnou_udalost(hra)

        self.assertEqual(zachycene["Inkvizice je blízko"], 5)
        self.assertEqual(zachycene["Vzpoura otrokyň"], 2)
        self.assertEqual(zachycene["Nemoc otrokyně"], 2)

    def test_kalendar_zobrazi_ulozenou_historii_udalosti(self):
        from game.kalendar import zobraz_kalendar

        hra = Hra()
        hra.kalendar.udalosti.append({
            "den": 4,
            "udalost": "Večer světel",
        })
        stav_pred = hra.to_dict()
        vystup = io.StringIO()
        with patch("builtins.input", return_value="0"), redirect_stdout(vystup):
            zobraz_kalendar(hra)

        self.assertIn("Kalendář a sezónní události", vystup.getvalue())
        self.assertIn("den 4: Večer světel", vystup.getvalue())
        self.assertEqual(hra.to_dict(), stav_pred)

    def test_prvni_npc_ukol_neodemkne_achievement_retezce(self):
        hra = Hra()
        hra.svet.vztahy_npc["mira"] = 100
        self.assertTrue(hra.npc_questy.prijmi(hra, "mira"))

        self.assertEqual(hra.npc_questy.dokoncit(hra, "mira"), "normal")
        self.assertEqual(hra.achievementy.statistiky.get("npc_retezce", 0), 0)

        self.assertTrue(hra.npc_questy.prijmi(hra, "mira"))
        self.assertEqual(hra.npc_questy.dokoncit(hra, "mira"), "normal")
        self.assertEqual(hra.achievementy.statistiky.get("npc_retezce"), 1)

    def test_selene_a_eleanor_odemykaji_navazujici_ukoly(self):
        hra = Hra()
        for npc_id, nazev in (
            ("selene", "Zrcadla astrální citadely"),
            ("lady_eleanor", "Dopis bez podpisu"),
        ):
            hra.svet.vztahy_npc[npc_id] = 100
            self.assertTrue(hra.npc_questy.prijmi(hra, npc_id))
            self.assertEqual(hra.npc_questy.dokoncit(hra, npc_id), "normal")
            dalsi = dict(hra.npc_questy.dostupne(hra))[npc_id]
            self.assertEqual(dalsi["nazev"], nazev)

    def test_vip_odmena_prida_lektvar_do_inventare(self):
        from game.nevestinec import vip_zakazky

        hra = Hra()
        divka = Otrokyně(jmeno="Aurelia", charakter="alchymistka")
        divka.v_nevestinci = True
        hra.harem.pridat(divka)
        hra.nevestinec.vip_nabidky = [{
            "id": "alchymisticky_mistr",
            "jmeno": "Alchymistický mistr Aurelius",
            "popis": "Odměna za soukromou audience.",
            "pozadovane_charaktery": ["alchymistka"],
            "odmena_zlato": 400,
            "bonus_lektvar": True,
        }]

        with patch("builtins.input", side_effect=["1", "1", ""]), redirect_stdout(io.StringIO()):
            vip_zakazky(hra)

        self.assertEqual(hra.hrac.inventar.pocet_predmetu("elixir_temnoty"), 1)

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

    def test_vsechny_lokace_maji_povest_a_unikatni_akce(self):
        from game.svet import LOKACE, POVESTI_LOKACI

        self.assertEqual(set(POVESTI_LOKACI), set(LOKACE))
        hra = Hra()
        hra.hrac.gold = 10000
        hra.pevnost.drevo = 1000
        hra.hrac.inventar.pridej_predmet("dukazni_listina")
        akce = {
            "hranice": ("1", "2", "3"),
            "ctvrt_remeselniku": ("1", "2", "3"),
            "haj_soumraku": ("1", "2", "3"),
            "observator": ("1", "2"),
            "sklenena_zahrada": ("1", "2", "3"),
            "stribrne_terasy": ("1", "2", "3"),
            "palac_bohatych": ("1", "2", "3"),
            "pristav": ("1", "2"),
            "molo_mesicniho_pristavu": ("1", "2"),
            "tajna_svatyne_stinu": ("1", "2", "3"),
            "akademie": ("1", "2", "3"),
        }

        for lokace, volby in akce.items():
            hra.svet.aktualni_lokace = lokace
            for volba in volby:
                with self.subTest(lokace=lokace, volba=volba):
                    with patch("builtins.input", side_effect=[volba, ""]), redirect_stdout(io.StringIO()):
                        hra.svet.menu_lokacni_akce(hra)

    def test_lokacni_odmeny_respektuji_limity_a_mafie_system(self):
        hra = Hra()
        hra.svet.aktualni_lokace = "tajna_svatyne_stinu"
        hra.mafie.vliv_ve_meste = 99
        with patch("builtins.input", side_effect=["1", ""]), redirect_stdout(io.StringIO()):
            hra.svet.menu_lokacni_akce(hra)
        self.assertEqual(hra.mafie.vliv_ve_meste, 100)

        hra.svet.aktualni_lokace = "katakomby"
        hra.hrac.dark_energy = hra.hrac.max_temno() - 2
        with patch("builtins.input", side_effect=["2", ""]), redirect_stdout(io.StringIO()):
            hra.svet.menu_lokacni_akce(hra)
        self.assertEqual(hra.hrac.dark_energy, hra.hrac.max_temno())

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
        self.assertIn("knezka_temnoty", CHARAKTERY)
        self.assertIn("zlodejka", CHARAKTERY)
        self.assertIn("padla_paladinka", CHARAKTERY)
        self.assertIn("sukuba_hybrid", CHARAKTERY)
        self.assertIn("alchymistka", CHARAKTERY)
        self.assertIn("princezna_ruin", CHARAKTERY)

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

    def test_nevestinec_specializace_a_vypocet(self):
        from game.nevestinec import vypocti_denni_prijem, SPECIALIZACE_POKOJU
        hra = Hra()
        hra.nevestinec.otevreno = True
        hra.hrac.sex_energy = 50
        hra.hrac.dark_energy = 50

        sukuba = Otrokyně(jmeno="Lilith", charakter="sukuba_hybrid")
        sukuba.v_nevestinci = True
        sukuba.pokoj_nevestinec = 1
        hra.harem.pridat(sukuba)
        hra.nevestinec.nastav_specializaci(1, "lazne")

        prijem = vypocti_denni_prijem(hra)
        self.assertGreater(prijem, 30)
        self.assertGreater(hra.hrac.sex_energy, 50)

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

    def test_budovatelska_strategie_produkce_a_pracovnice(self):
        from models.fortress import FortressDevelopment
        hra = Hra()
        pevnost = hra.pevnost
        pevnost.drevo = 100
        pevnost.kamen = 100
        pevnost.zelezo = 50
        pevnost.zasoby = 50
        pevnost.budovy["pila"] = 2
        pevnost.budovy["kamenolom"] = 1
        pevnost.budovy["statek"] = 2

        # Přiřazení dohlížitelky
        otrok = Otrokyně(jmeno="Valeria", charakter="Amazonka (bojovnice)")
        hra.harem.pridat(otrok)
        pevnost.pracovnici["pila"] = "Valeria"

        # Denní produkce
        puvodni_drevo = pevnost.drevo
        vysledky = pevnost.denni_produkce(hra)

        self.assertGreater(pevnost.drevo, puvodni_drevo)
        self.assertIn("drevo", vysledky)
        self.assertIn("dane", vysledky)

    def test_budovatelska_strategie_stavba_a_obrana(self):
        from models.fortress import FortressDevelopment
        pevnost = FortressDevelopment()
        pevnost.drevo = 500
        pevnost.kamen = 500
        pevnost.zelezo = 200

        # Kontrola možnosti stavby a vylepšení
        lze, _ = pevnost.muze_postavit("hradby", zlato_hrace=500)
        self.assertTrue(lze)

        uspelo, _ = pevnost.vylepsi_budovu("hradby", zlato_hrace=500)
        self.assertTrue(uspelo)
        self.assertEqual(pevnost.budovy.get("hradby"), 1)

        obrana = pevnost.celkova_obrana_pevnosti()
        self.assertGreater(obrana, 0)

    def test_souboj_s_bojovou_partnerkou(self):
        from game.souboje import Souboj, Nepritel
        hra = Hra()
        partnerka = Otrokyně(jmeno="Aria", charakter="Amazonka (bojovnice)", poslusnost=90, hp=100, max_hp=100)
        hra.harem.pridat(partnerka)
        hra.pevnost.bojova_partnerka = "Aria"

        nepritel = Nepritel("Tréninkový golem", 1, 1, 0, 10, 5)
        souboj = Souboj(hra.hrac, nepritel, hra=hra)

        # Ověření načtení bojové partnerky
        self.assertIsNotNone(souboj.partnerka)
        self.assertEqual(souboj.partnerka.jmeno, "Aria")

        # Provedení tahu s útokem
        with patch("builtins.input", side_effect=["1", ""]):
            vysledek = souboj.proved_boj()
        self.assertTrue(vysledek)

    def test_mapa_nove_lokace_a_pribeh_npc(self):
        from game.svet import LOKACE, NPC
        self.assertIn("vezeni_inkvizice", LOKACE)
        self.assertIn("zricenina_astralni_veze", LOKACE)
        self.assertIn("paserska_zatoka", LOKACE)
        self.assertIn("krvavy_lom", LOKACE)

        self.assertIn("inkvizitor_malor", NPC)
        self.assertIn("vespera", NPC)
        self.assertIn("selene", NPC)
        self.assertIn("kapitanka_drake", NPC)
        self.assertIn("dozorce_krag", NPC)

        hra = Hra()
        hra.hrac.gold = 100
        hra.hrac.dark_energy = 25
        hra.svet.aktualni_lokace = "vezeni_inkvizice"

        # Test příběhového dialogu s Vesperou - osvobození do harému
        with patch("builtins.input", side_effect=["1", ""]):
            hra.svet.pribehovy_rozhovor("vespera", NPC["vespera"], hra)

        self.assertTrue(any(o.jmeno == "Vespera" for o in hra.harem.otrokyne))

        # Test lokační akce v pevnosti
        hra.svet.aktualni_lokace = "pevnost"
        with patch("builtins.input", side_effect=["2", ""]):
            hra.svet.menu_lokacni_akce(hra)
        self.assertGreaterEqual(hra.pevnost.zasoby, 25)


if __name__ == "__main__":
    unittest.main()
