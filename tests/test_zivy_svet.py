import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from game.menu_hlavni import normalizuj_volbu
from game.save_load import Hra, migrate_save
from game.zivy_svet import FRAKCNI_AKCE, ZivySvetSystem
from game.svet import LOKACE
from data.mesta import MESTA
from data.frakcni_kroniky import FRAKCNI_PROFILY
from config import YELLOW
from models.frakce import FrakcniSystem
from utils.decision_ai import vzdalenosti_od_cilu, vyber_nejlepsi_uzitek


class ZivySvetTesty(unittest.TestCase):
    def test_vsechny_frakce_maji_unikatni_starost_pribeh_a_zbozi(self):
        hra = Hra()
        self.assertEqual(set(FRAKCNI_PROFILY), set(hra.frakce.frakce))
        for profil in FRAKCNI_PROFILY.values():
            self.assertTrue(profil["starost"])
            self.assertEqual(len(profil["kapitoly"]), 3)
            self.assertTrue(all(nazev and text for nazev, text in profil["kapitoly"]))
            self.assertGreaterEqual(len(profil["zbozi"]), 2)

        vystup = io.StringIO()
        with redirect_stdout(vystup):
            hra.zivy_svet._prehled_frakci_a_mest(hra)
        for frakce in hra.frakce.frakce.values():
            self.assertIn(frakce.nazev, vystup.getvalue())
        self.assertIn("Staré město", vystup.getvalue())
        self.assertIn("Východní Brod", vystup.getvalue())

    def test_pribeh_npc_zobrazi_fakcni_kapitolu_a_mestskou_starost(self):
        hra = Hra()
        with patch("builtins.input", side_effect=["7", "2"]), redirect_stdout(
            io.StringIO()
        ) as vystup:
            hra.zivy_svet._menu_pribehu_npc(hra)

        self.assertIn("Večer pro mecenáše", vystup.getvalue())
        self.assertIn("Městská starost:", vystup.getvalue())
        self.assertEqual(hra.zivy_svet.postavy[6]["pribeh"], 1)

    def test_nove_dospele_npc_maji_osobni_ukoly_a_ulozitelny_postup(self):
        from game.svet import NPC

        hra = Hra()
        for npc_id, prvni_ukol, dalsi_ukol in (
            (
                "nora_kartografka",
                "Mapa bezpečných cest",
                "Atlas otevřených cest",
            ),
            (
                "zora_bylinkarka",
                "Semena pro komunitní zahradu",
                "Ošetřovna pod širým nebem",
            ),
        ):
            with self.subTest(npc=npc_id):
                self.assertIn(npc_id, NPC)
                self.assertIn(npc_id, hra.svet.vztahy_npc)
                self.assertGreaterEqual(NPC[npc_id]["vek"], 18)
                hra.svet.vztahy_npc[npc_id] = 8
                self.assertEqual(
                    dict(hra.npc_questy.dostupne(hra))[npc_id]["nazev"],
                    prvni_ukol,
                )
                self.assertTrue(hra.npc_questy.prijmi(hra, npc_id))
                self.assertEqual(hra.npc_questy.dokoncit(hra, npc_id), "normal")

                obnovena = Hra.from_dict(hra.to_dict())
                self.assertEqual(
                    dict(obnovena.npc_questy.dostupne(obnovena))[npc_id]["nazev"],
                    dalsi_ukol,
                )

    def test_setkani_npc_zobrazi_postavy_pouze_v_aktualni_lokaci(self):
        hra = Hra()
        sveta = hra.zivy_svet
        hra.svet.aktualni_lokace = "hostinec"
        mira = next(p for p in sveta.postavy if p["id"] == "mira_lecitelka")
        mira["lokace"] = "hostinec"
        videny = sveta._postavy_v_lokaci(hra)

        self.assertEqual([p["id"] for p in videny], ["mira_lecitelka"])
        with patch("builtins.input", side_effect=["1", "1"]), redirect_stdout(
            io.StringIO()
        ) as vystup:
            sveta._menu_setkani_npc(hra)
        self.assertIn("Mira", vystup.getvalue())
        self.assertIn("aktuální zprávu", vystup.getvalue())
        self.assertEqual(mira["vztah_hraci"], 0)

    def test_pomoc_pritomnemu_npc_ma_denni_limit_a_uklada_se(self):
        hra = Hra()
        sveta = hra.zivy_svet
        hra.hrac.den = 3
        hra.svet.aktualni_lokace = "hostinec"
        mira = next(p for p in sveta.postavy if p["id"] == "mira_lecitelka")
        mira["lokace"] = "hostinec"
        mesto = sveta.mesta["stare_mesto"]
        zlato_pred = hra.hrac.gold
        reputace_pred = hra.frakce.frakce["policie"].reputace
        stabilita_pred = mesto.stabilita
        bezpeci_pred = mesto.bezpeci

        with patch("builtins.input", side_effect=["1", "2"]), redirect_stdout(
            io.StringIO()
        ):
            sveta._menu_setkani_npc(hra)

        self.assertEqual(hra.hrac.gold, zlato_pred - 10)
        self.assertEqual(mira["vztah_hraci"], 4)
        self.assertEqual(mira["posledni_pomoc_den"], 3)
        self.assertEqual(hra.frakce.frakce["policie"].reputace, reputace_pred + 2)
        self.assertEqual(mesto.stabilita, stabilita_pred + 1)
        self.assertEqual(mesto.bezpeci, bezpeci_pred + 3)

        ulozena = Hra.from_dict(hra.to_dict())
        ulozena_mira = next(
            p for p in ulozena.zivy_svet.postavy
            if p["id"] == "mira_lecitelka"
        )
        self.assertEqual(ulozena_mira["posledni_pomoc_den"], 3)
        zlato_po_prvni_pomoci = hra.hrac.gold
        with patch("builtins.input", side_effect=["1", "2"]), redirect_stdout(
            io.StringIO()
        ) as vystup:
            sveta._menu_setkani_npc(hra)
        self.assertIn("Dnes už jsi této postavě pomohl", vystup.getvalue())
        self.assertEqual(hra.hrac.gold, zlato_po_prvni_pomoci)
        self.assertEqual(mira["vztah_hraci"], 4)

    def test_pomoc_npc_ma_dopad_podle_role_a_mistni_zadosti(self):
        hra = Hra()
        svet = hra.zivy_svet
        hra.hrac.den = 4
        talia = next(p for p in svet.postavy if p["id"] == "talia_kupkyne")
        talia["lokace"] = hra.svet.aktualni_lokace
        mesto = svet.mesta["stare_mesto"]
        prosperita_pred = mesto.prosperita
        zasoby_pred = svet.trziste_sklady["stare_mesto"]["zasoby"]
        drevo_pred = svet.trziste_sklady["stare_mesto"]["drevo"]

        with patch("builtins.input", side_effect=["1", "2"]), redirect_stdout(
            io.StringIO()
        ) as vystup:
            svet._menu_setkani_npc(hra)

        self.assertIn("vyjednává o zásobách pro tržiště", vystup.getvalue())
        self.assertEqual(mesto.prosperita, prosperita_pred + 3)
        self.assertEqual(
            svet.trziste_sklady["stare_mesto"]["zasoby"],
            zasoby_pred + 2,
        )
        self.assertEqual(
            svet.trziste_sklady["stare_mesto"]["drevo"],
            drevo_pred + 1,
        )

        hra.hrac.den = 5
        elian = next(p for p in svet.postavy if p["id"] == "elian_informator")
        elian["lokace"] = hra.svet.aktualni_lokace
        body_pred = hra.vyzkum.body
        stabilita_pred = mesto.stabilita
        with patch("builtins.input", side_effect=["1", "2"]), redirect_stdout(
            io.StringIO()
        ):
            svet._menu_setkani_npc(hra)
        self.assertEqual(hra.vyzkum.body, body_pred + 1)
        self.assertEqual(mesto.stabilita, stabilita_pred + 2)

    def test_trziste_ma_zasoby_v_obou_mestech_a_denne_se_doplni(self):
        svet = ZivySvetSystem()
        stare_mesto_pred = svet.trziste_sklady["stare_mesto"]["zasoby"]
        brod_pred = svet.trziste_sklady["vychodni_brod"]["zelezo"]

        svet._doplnit_trziste()

        self.assertEqual(svet.trziste_sklady["stare_mesto"]["zasoby"], stare_mesto_pred + 1)
        self.assertEqual(svet.trziste_sklady["vychodni_brod"]["zelezo"], brod_pred + 1)

    def test_vsechny_frakce_maji_cil_a_stav_se_uklada(self):
        svet = ZivySvetSystem()

        self.assertEqual(set(svet.frakcni_cile), set(FrakcniSystem().frakce))
        self.assertEqual(set(FRAKCNI_AKCE), set(svet.frakcni_cile))
        obnoveno = ZivySvetSystem.from_dict(svet.to_dict())
        self.assertEqual(obnoveno.frakcni_cile, svet.frakcni_cile)
        self.assertEqual(
            {postava["id"] for postava in obnoveno.postavy},
            {postava["id"] for postava in svet.postavy},
        )
        for frakce_id in svet.frakcni_cile:
            self.assertEqual(
                obnoveno.frakcni_cile[frakce_id]["mesto_id"],
                svet.frakcni_cile[frakce_id]["mesto_id"],
            )

    def test_denni_tah_pohybuje_npc_a_neopakuje_se(self):
        hra = Hra()
        hra.hrac.den = 2
        postava = hra.zivy_svet.postavy[0]
        postava_pred = postava["lokace"]
        vzdalenosti = vzdalenosti_od_cilu(
            {lokace: data["sousedni"] for lokace, data in LOKACE.items()},
            MESTA["vychodni_brod"]["lokace"],
        )

        zpravy = hra.zivy_svet.posun_den(hra)
        druhy_vysledek = hra.zivy_svet.posun_den(hra)

        self.assertTrue(zpravy)
        self.assertEqual(druhy_vysledek, [])
        self.assertNotEqual(hra.zivy_svet.postavy[0]["lokace"], postava_pred)
        self.assertLess(
            vzdalenosti[postava["lokace"]],
            vzdalenosti[postava_pred],
        )
        self.assertEqual(hra.zivy_svet.posledni_den, 2)

    def test_dokonceny_frakcni_cil_vytvori_nabidku_s_rozhodnutim(self):
        hra = Hra()
        hra.hrac.den = 1
        hra.zivy_svet.frakcni_cile["policie"]["cil"] = 1

        hra.zivy_svet.posun_den(hra)

        self.assertEqual(len(hra.zivy_svet.nabidky), 1)
        self.assertEqual(
            hra.zivy_svet.nabidky[0]["frakce_id"],
            "policie",
        )
        self.assertIn("postava", hra.zivy_svet.nabidky[0])

    def test_volba_nabidky_zmeni_zlato_frakci_a_reputaci(self):
        hra = Hra()
        nabidka = {
            "frakce_id": "policie",
            "frakce_nazev": "Policie",
            "cilek": "hlídky",
        }
        zlato_pred = hra.hrac.gold
        reputace_pred = hra.frakce.frakce["policie"].reputace
        mesto_pred = hra.hrac.reputace_mesta

        with patch("builtins.input", return_value="1"), redirect_stdout(io.StringIO()):
            self.assertTrue(hra.zivy_svet._vyres_nabidku(hra, nabidka))

        self.assertEqual(hra.hrac.gold, zlato_pred - 25)
        self.assertEqual(hra.frakce.frakce["policie"].reputace, reputace_pred + 8)
        self.assertEqual(hra.hrac.reputace_mesta, mesto_pred + 1)

    def test_rozhodnuti_frakcni_situace_meni_stav_prislusneho_mesta(self):
        hra = Hra()
        mesto = hra.zivy_svet.mesta["vychodni_brod"]
        bezpeci_pred = mesto.bezpeci
        stabilita_pred = mesto.stabilita
        nabidka = {
            "frakce_id": "policie",
            "frakce_nazev": "Policie",
            "cilek": "hlídky",
            "mesto_id": "vychodni_brod",
        }

        with patch("builtins.input", return_value="2"), redirect_stdout(io.StringIO()):
            self.assertTrue(hra.zivy_svet._vyres_nabidku(hra, nabidka))

        self.assertEqual(mesto.bezpeci, bezpeci_pred + 1)
        self.assertEqual(mesto.stabilita, stabilita_pred + 2)

    def test_menu_a_migrace_starych_savu(self):
        hra = Hra()
        data = hra.to_dict()
        data["save_version"] = 1

        migrovano = migrate_save(data)

        self.assertEqual(migrovano["save_version"], 2)
        self.assertEqual(normalizuj_volbu("35"), "36")
        self.assertEqual(normalizuj_volbu("36"), "37")
        obnoveno = Hra.from_dict(migrovano)
        self.assertIsInstance(obnoveno.zivy_svet, ZivySvetSystem)

    def test_vychodni_mesto_je_propojene_a_cestovatelne(self):
        hra = Hra()
        hra.svet.aktualni_lokace = "pristav"
        hra.svet.odhal_lokaci("vychodni_pristav")
        hra.svet.odhal_lokaci("vychodni_trziste")
        hra.svet.odhal_lokaci("pristav")

        with patch("random.random", return_value=0.99):
            self.assertTrue(hra.svet.cestuj("vychodni_pristav", hra))
            self.assertTrue(hra.svet.cestuj("vychodni_trziste", hra))

        self.assertIn("vychodni_pristav", LOKACE["pristav"]["sousedni"])
        self.assertIn("vychodni_pristav", hra.svet.odhalene_lokace)

    def test_prichod_do_lokace_upozorni_na_pritomne_npc(self):
        hra = Hra()
        hra.zivy_svet.postavy[0]["lokace"] = "trh"
        vystup = io.StringIO()

        with patch("random.random", return_value=0.99), redirect_stdout(vystup):
            self.assertTrue(hra.svet.cestuj("trh", hra))

        self.assertIn("Na místě potkáváš: Mira", vystup.getvalue())
        self.assertIn("Setkat se s NPC", vystup.getvalue())

    def test_prichod_neupozorni_na_npc_v_jine_lokaci(self):
        hra = Hra()
        for postava in hra.zivy_svet.postavy:
            postava["lokace"] = "hostinec"
        vystup = io.StringIO()

        with patch("random.random", return_value=0.99), redirect_stdout(vystup):
            self.assertTrue(hra.svet.cestuj("trh", hra))

        self.assertNotIn("Na místě potkáváš:", vystup.getvalue())

    def test_ai_najde_nejkratsi_cestu_k_cili_a_zvazuje_uzitek(self):
        graf = {
            "pevnost": ("trh", "les"),
            "trh": ("pevnost", "pristav"),
            "pristav": ("trh", "vychodni_pristav"),
            "vychodni_pristav": ("pristav", "vychodni_trziste"),
            "vychodni_trziste": ("vychodni_pristav",),
            "les": ("pevnost",),
        }

        vzdalenosti = vzdalenosti_od_cilu(graf, ("vychodni_trziste",))

        self.assertEqual(vzdalenosti["pevnost"], 4)
        self.assertEqual(
            vyber_nejlepsi_uzitek((("bezpecna", 1), ("rizikova", 3))),
            "rizikova",
        )

    def test_zivy_svet_ulozi_stav_druheho_mesta_a_ai_cil(self):
        hra = Hra()
        hra.zivy_svet.mesta["vychodni_brod"].uprav(bezpeci=-8, prosperita=12)
        hra.hrac.den = 2
        hra.zivy_svet.posun_den(hra)

        obnovena = Hra.from_dict(hra.to_dict())

        self.assertEqual(
            obnovena.zivy_svet.mesta["vychodni_brod"].prosperita,
            hra.zivy_svet.mesta["vychodni_brod"].prosperita,
        )
        self.assertIn(
            hra.zivy_svet.postavy[0]["lokace"],
            hra.svet.odhalene_lokace,
        )

    def test_mapa_barvi_lokace_podle_frakcni_kontroly(self):
        hra = Hra()
        hra.svet.aktualni_lokace = "pevnost"
        hra.svet.odhal_lokaci("trh")

        uzel = hra.svet._format_uzel("trh", hra)

        self.assertIn(str(YELLOW), uzel)
        self.assertEqual(hra.zivy_svet.frakce_lokace("trh"), "obchodnici")

    def test_frakcni_vliv_a_mestske_udalosti_se_ukladaji(self):
        hra = Hra()
        hra.hrac.den = 4
        hra.zivy_svet.posun_den(hra)

        obnovena = Hra.from_dict(hra.to_dict())

        self.assertEqual(
            obnovena.zivy_svet.kontrola_lokaci,
            hra.zivy_svet.kontrola_lokaci,
        )
        self.assertEqual(
            obnovena.zivy_svet.udalosti_mesta,
            hra.zivy_svet.udalosti_mesta,
        )
        self.assertEqual(len(obnovena.zivy_svet.udalosti_mesta), 1)

    def test_rozhodnuti_mestske_udalosti_maji_cenu_a_dopad(self):
        hra = Hra()
        hra.hrac.den = 4
        hra.zivy_svet.posun_den(hra)
        udalost = hra.zivy_svet.udalosti_mesta[0]
        mesto = hra.zivy_svet.mesta[udalost["mesto_id"]]
        prosperita_pred = mesto.prosperita
        zlato_pred = hra.hrac.gold

        with patch("builtins.input", return_value="1"), redirect_stdout(io.StringIO()):
            self.assertTrue(hra.zivy_svet._vyres_udalost_mesta(hra, udalost))

        self.assertEqual(hra.hrac.gold, zlato_pred - 25)
        self.assertEqual(mesto.prosperita, prosperita_pred + 5)

    def test_karavanni_prijem_respektuje_bezpeci_mest(self):
        hra = Hra()
        prijem_bezpecnych_mest = hra.zivy_svet._prijem_karavan()
        hra.zivy_svet.mesta["vychodni_brod"].uprav(bezpeci=-100)

        self.assertLess(
            hra.zivy_svet._prijem_karavan(),
            prijem_bezpecnych_mest,
        )

    def test_plna_fronta_nezahodi_dokonceny_frakcni_cil(self):
        hra = Hra()
        hra.zivy_svet.nabidky = [
            {
                "frakce_id": "policie",
                "frakce_nazev": "Policie",
                "cilek": "hlídky",
                "text": "Situace",
                "postava": "Mira",
            }
            for _ in range(10)
        ]
        hra.zivy_svet.frakcni_cile["policie"]["cil"] = 1
        hra.hrac.den = 1

        hra.zivy_svet.posun_den(hra)
        obnovena = Hra.from_dict(hra.to_dict())

        self.assertEqual(len(hra.zivy_svet.nabidky), 10)
        self.assertEqual(
            obnovena.zivy_svet.frakcni_cile["policie"]["postup"],
            1,
        )

    def test_ignorovana_mestska_udalost_ma_trvaly_dusledek(self):
        hra = Hra()
        hra.hrac.den = 4
        hra.zivy_svet.posun_den(hra)
        udalost = hra.zivy_svet.udalosti_mesta[0]
        mesto = hra.zivy_svet.mesta[udalost["mesto_id"]]
        prosperita_pred = mesto.prosperita

        with patch("builtins.input", return_value="0"), redirect_stdout(io.StringIO()):
            self.assertTrue(hra.zivy_svet._vyres_udalost_mesta(hra, udalost))

        self.assertEqual(mesto.prosperita, prosperita_pred - 2)
        self.assertIn("bez zásahu", hra.zivy_svet.historie[-1]["text"])

    def test_fakcni_cil_pusobi_na_mesto_kde_ma_fakce_vliv(self):
        hra = Hra()
        mesto = hra.zivy_svet.mesta["vychodni_brod"]
        bezpeci_pred = mesto.bezpeci
        stabilita_pred = mesto.stabilita

        zprava = hra.zivy_svet._vykonej_cil_fakce("policie")

        self.assertEqual(mesto.bezpeci, bezpeci_pred + 1)
        self.assertEqual(mesto.stabilita, stabilita_pred + 1)
        self.assertEqual(
            hra.zivy_svet.frakcni_cile["policie"]["mesto_id"],
            "vychodni_brod",
        )
        self.assertIn("Východní Brod", zprava)

    def test_fakcni_akce_maji_omezeny_a_odlisny_dopad(self):
        hra = Hra()
        stare_mesto = hra.zivy_svet.mesta["stare_mesto"]
        bezpeci_pred = stare_mesto.bezpeci
        prosperita_pred = stare_mesto.prosperita

        hra.zivy_svet._vykonej_cil_fakce("podsveti")

        self.assertEqual(stare_mesto.prosperita, prosperita_pred + 1)
        self.assertEqual(stare_mesto.bezpeci, bezpeci_pred - 1)

    def test_denni_cinnost_frakci_meni_zasoby_mistniho_trziste(self):
        hra = Hra()
        svet = hra.zivy_svet
        frakce_id = "obchodnici"
        sklady_pred = {
            mesto_id: sklad.copy()
            for mesto_id, sklad in svet.trziste_sklady.items()
        }

        zprava = svet._vykonej_cil_fakce(frakce_id)

        mesto_id = svet.frakcni_cile[frakce_id]["mesto_id"]
        sklad = svet.trziste_sklady[mesto_id]
        self.assertEqual(
            sklad["zasoby"],
            min(60, sklady_pred[mesto_id]["zasoby"] + 2),
        )
        self.assertEqual(
            sklad["drevo"],
            min(60, sklady_pred[mesto_id]["drevo"] + 1),
        )
        self.assertIn("Tržiště:", zprava)
        self.assertIn("zasoby", zprava)

    def test_fakcni_trzni_dopady_respektuji_skladove_limity(self):
        hra = Hra()
        svet = hra.zivy_svet
        mesto_id = svet.frakcni_cile["obchodnici"]["mesto_id"]
        svet.trziste_sklady[mesto_id]["zasoby"] = 60
        svet.trziste_sklady[mesto_id]["drevo"] = 0

        zprava = svet._aplikuj_dopad_frakce_na_trh("obchodnici", mesto_id)

        self.assertEqual(svet.trziste_sklady[mesto_id]["zasoby"], 60)
        self.assertEqual(svet.trziste_sklady[mesto_id]["drevo"], 1)
        self.assertNotIn("zasoby", zprava)
        self.assertIn("+1 drevo", zprava)

    def test_automaticky_vyvoj_zustava_v_rozsahu_po_ctyriceti_dnech(self):
        hra = Hra()
        for den in range(1, 41):
            hra.hrac.den = den
            hra.zivy_svet.posun_den(hra)

        for mesto in hra.zivy_svet.mesta.values():
            for atribut in ("prosperita", "bezpeci", "stabilita"):
                self.assertGreaterEqual(getattr(mesto, atribut), 0)
                self.assertLessEqual(getattr(mesto, atribut), 100)
        self.assertLessEqual(len(hra.zivy_svet.udalosti_mesta), 3)
        self.assertLessEqual(len(hra.zivy_svet.nabidky), 10)
        self.assertLessEqual(len(hra.zivy_svet.historie), 30)

    def test_diplomacie_meni_vztah_a_stabilitu_mesta(self):
        hra = Hra()
        vztah_pred = hra.zivy_svet.vztahy_frakci["podsveti|policie"]
        stabilita_pred = hra.zivy_svet.mesta["stare_mesto"].stabilita
        zlato_pred = hra.hrac.gold

        with patch("builtins.input", side_effect=["1", "1"]), \
             redirect_stdout(io.StringIO()):
            hra.zivy_svet._menu_diplomacie_frakci(hra)

        self.assertEqual(hra.hrac.gold, zlato_pred - 25)
        self.assertEqual(
            hra.zivy_svet.vztahy_frakci["podsveti|policie"],
            vztah_pred + 15,
        )
        self.assertEqual(
            hra.zivy_svet.mesta["stare_mesto"].stabilita,
            stabilita_pred + 2,
        )

    def test_pribeh_npc_uklada_postup_a_odmenu_dokoncenim(self):
        hra = Hra()
        postava = hra.zivy_svet.postavy[0]
        reputace_pred = hra.frakce.frakce["policie"].reputace
        with patch("builtins.input", side_effect=["1", "1", "1", "2", "1", "2"]):
            with redirect_stdout(io.StringIO()):
                for _ in range(3):
                    hra.zivy_svet._menu_pribehu_npc(hra)

        self.assertEqual(postava["pribeh"], 3)
        self.assertEqual(postava["vztah_hraci"], 16)
        self.assertEqual(hra.frakce.frakce["policie"].reputace, reputace_pred + 4)
        self.assertEqual(
            Hra.from_dict(hra.to_dict()).zivy_svet.postavy[0]["pribeh"],
            3,
        )

    def test_sara_ma_vlastni_pribehovou_linku(self):
        hra = Hra()
        sara = next(
            postava for postava in hra.zivy_svet.postavy
            if postava["id"] == "sara_signalistka"
        )
        index = hra.zivy_svet.postavy.index(sara) + 1
        vystup = io.StringIO()
        with patch("builtins.input", side_effect=[str(index), "2"]), redirect_stdout(
            vystup
        ):
            hra.zivy_svet._menu_pribehu_npc(hra)

        self.assertIn("Světlo, které nikdo neviděl", vystup.getvalue())
        self.assertEqual(sara["pribeh"], 1)

    def test_doprovod_karavany_persistuje_a_zachrani_nejistou_zasilku(self):
        hra = Hra()
        hra.hrac.gold = 100
        hra.npc_questy.dokoncene["sara_signalistka"] = 1
        hra.zivy_svet.karavany = [{
            "id": "testovaci-karavana",
            "cesta": ["trh", "pristav", "vychodni_pristav", "vychodni_trziste"],
            "pozice": 2,
            "stav": "na_ceste",
            "odeslano": 1,
            "doprovod": False,
        }]

        with redirect_stdout(io.StringIO()):
            self.assertTrue(hra.zivy_svet.zajisti_doprovod_karavany(hra))
        self.assertEqual(hra.hrac.gold, 75)
        obnovena = Hra.from_dict(hra.to_dict())
        self.assertTrue(obnovena.zivy_svet.karavany[0]["doprovod"])

        mesto = obnovena.zivy_svet.mesta["vychodni_brod"]
        mesto.bezpeci = 10
        mesto.stabilita = 10
        zlato_pred = obnovena.hrac.gold
        with redirect_stdout(io.StringIO()):
            zpravy = obnovena.zivy_svet._posun_karavany(
                obnovena, obnovena.hrac.den
            )

        self.assertFalse(obnovena.zivy_svet.karavany)
        self.assertGreater(obnovena.hrac.gold, zlato_pred)
        self.assertGreater(mesto.bezpeci, 10)
        self.assertTrue(any("bezpečně dorazila" in zprava for zprava in zpravy))

    def test_slavnost_zohledni_rozpocet_bezpecnost_npc_a_ochlazeni(self):
        hra = Hra()
        hra.hrac.gold = 200
        svet = hra.zivy_svet
        mesto = svet.mesta["stare_mesto"]
        stabilita_pred = mesto.stabilita
        bezpeci_pred = mesto.bezpeci
        reputace_pred = hra.frakce.frakce["cech_kurtizan"].reputace
        npc_pred = next(
            postava for postava in svet.postavy
            if postava["id"] == "mira_lecitelka"
        )["vztah_hraci"]

        with patch("builtins.input", side_effect=["2", "2", "2"]), redirect_stdout(
            io.StringIO()
        ):
            svet._menu_slavnosti(hra)

        self.assertEqual(hra.hrac.gold, 170)
        self.assertEqual(mesto.stabilita, stabilita_pred + 6)
        self.assertEqual(mesto.bezpeci, bezpeci_pred + 3)
        self.assertEqual(
            hra.frakce.frakce["cech_kurtizan"].reputace,
            reputace_pred + 6,
        )
        self.assertEqual(
            next(
                postava for postava in svet.postavy
                if postava["id"] == "mira_lecitelka"
            )["vztah_hraci"],
            npc_pred + 5,
        )
        self.assertEqual(svet.posledni_slavnosti["stare_mesto"], 1)
        obnovena = Hra.from_dict(hra.to_dict()).zivy_svet
        self.assertEqual(obnovena.posledni_slavnosti["stare_mesto"], 1)
        self.assertEqual(len(obnovena.navazujici_udalosti), 1)
        self.assertEqual(
            obnovena.navazujici_udalosti[0]["typ"], "bezpecna_ctvrt"
        )
        self.assertEqual(obnovena.navazujici_udalosti[0]["den"], 3)
        self.assertFalse(any(
            mesto_id == "stare_mesto"
            for mesto_id, _ in obnovena._dostupne_slavnosti(
                Hra.from_dict(hra.to_dict())
            )
        ))

        zpravy = []
        obnovena._aktivuj_nasledne_udalosti(3, zpravy)
        self.assertEqual(
            obnovena.udalosti_mesta[-1]["typ"], "bezpecna_ctvrt"
        )
        self.assertIn("Pokračuje městská linka", zpravy[0])

    def test_slavnost_zustane_zamcena_pro_mesto_v_krizi(self):
        hra = Hra()
        for mesto in hra.zivy_svet.mesta.values():
            mesto.prosperita = 30
            mesto.stabilita = 30

        self.assertEqual(hra.zivy_svet._dostupne_slavnosti(hra), [])
        vystup = io.StringIO()
        with redirect_stdout(vystup):
            hra.zivy_svet._menu_slavnosti(hra)
        self.assertIn("Žádné město", vystup.getvalue())

    def test_navazujici_udalost_se_aktivuje_a_ulozi(self):
        hra = Hra()
        hra.zivy_svet.navazujici_udalosti.append({
            "den": 5,
            "mesto_id": "vychodni_brod",
            "typ": "trzni_oziveni",
            "retizec": "test-linky",
        })
        zpravy = []

        hra.zivy_svet._aktivuj_nasledne_udalosti(5, zpravy)

        self.assertEqual(len(hra.zivy_svet.navazujici_udalosti), 0)
        self.assertEqual(hra.zivy_svet.udalosti_mesta[-1]["lokace_id"], "vychodni_trziste")
        obnoveno = Hra.from_dict(hra.to_dict())
        self.assertEqual(
            obnoveno.zivy_svet.udalosti_mesta[-1]["retizec"],
            "test-linky",
        )

    def test_frakcni_iniciativa_reaguje_na_mesto_a_zapoji_npc(self):
        hra = Hra()
        mesto = hra.zivy_svet.mesta["vychodni_brod"]
        mesto.uprav(prosperita=-20, bezpeci=-30, stabilita=-10)
        hra.hrac.den = 12

        zpravy = hra.zivy_svet.posun_den(hra)

        udalost = next(
            udalost for udalost in hra.zivy_svet.udalosti_mesta
            if udalost["typ"] == "frakcni_iniciativa"
        )
        self.assertEqual(udalost["mesto_id"], "vychodni_brod")
        self.assertEqual(udalost["metrika"], "bezpeci")
        self.assertTrue(udalost["npc_id"])
        self.assertTrue(any("iniciativa:" in zprava for zprava in zpravy))
        self.assertIn("žádá o pomoc", udalost["text"])

        obnovena = Hra.from_dict(hra.to_dict())
        ulozena = next(
            udalost for udalost in obnovena.zivy_svet.udalosti_mesta
            if udalost["typ"] == "frakcni_iniciativa"
        )
        self.assertEqual(ulozena["npc_id"], udalost["npc_id"])
        self.assertEqual(ulozena["metrika"], "bezpeci")
        self.assertEqual(ulozena["text"], udalost["text"])

    def test_mestske_udalosti_se_prizpusobi_nejvetsi_krizi(self):
        hra = Hra()
        svet = hra.zivy_svet
        brod = svet.mesta["vychodni_brod"]
        brod.prosperita = 50
        brod.bezpeci = 50
        brod.stabilita = 20

        udalost = svet._vytvor_udalost_mesta(4)

        self.assertEqual(udalost["mesto_id"], "vychodni_brod")
        self.assertEqual(udalost["typ"], "frakcni_iniciativa")
        self.assertEqual(udalost["metrika"], "stabilita")

        brod.prosperita = 50
        brod.bezpeci = 20
        brod.stabilita = 50
        udalost = svet._vytvor_udalost_mesta(8)
        self.assertEqual(udalost["typ"], "hlidky")
        self.assertEqual(udalost["mesto_id"], "vychodni_brod")

        brod.bezpeci = 50
        brod.prosperita = 20
        svet.trziste_sklady["vychodni_brod"]["zasoby"] = 2
        udalost = svet._vytvor_udalost_mesta(16)
        self.assertEqual(udalost["typ"], "trzni_nepokoj")
        self.assertEqual(udalost["mesto_id"], "vychodni_brod")

        svet.trziste_sklady["vychodni_brod"]["zasoby"] = 20
        udalost = svet._vytvor_udalost_mesta(16)
        self.assertEqual(udalost["typ"], "karavana")

    def test_podpora_frakcni_iniciativy_zmeni_mesto_frakci_i_vztah_npc(self):
        hra = Hra()
        svet = hra.zivy_svet
        udalost = svet._vytvor_frakcni_iniciativu(12)
        mesto = svet.mesta[udalost["mesto_id"]]
        npc = next(
            postava for postava in svet.postavy
            if postava["id"] == udalost["npc_id"]
        )
        metrika_pred = getattr(mesto, udalost["metrika"])
        reputace_pred = hra.frakce.frakce[udalost["frakce_id"]].reputace
        vztah_pred = npc["vztah_hraci"]
        zlato_pred = hra.hrac.gold

        with patch("builtins.input", return_value="1"), redirect_stdout(io.StringIO()):
            self.assertTrue(svet._vyres_udalost_mesta(hra, udalost))

        self.assertEqual(getattr(mesto, udalost["metrika"]), metrika_pred + 4)
        self.assertEqual(hra.hrac.gold, zlato_pred - 25)
        self.assertEqual(
            hra.frakce.frakce[udalost["frakce_id"]].reputace,
            reputace_pred + 5,
        )
        self.assertEqual(npc["vztah_hraci"], vztah_pred + 4)

    def test_ignorovana_frakcni_iniciativa_ma_dusledek(self):
        hra = Hra()
        svet = hra.zivy_svet
        udalost = svet._vytvor_frakcni_iniciativu(12)
        mesto = svet.mesta[udalost["mesto_id"]]
        npc = next(
            postava for postava in svet.postavy
            if postava["id"] == udalost["npc_id"]
        )
        metrika_pred = getattr(mesto, udalost["metrika"])
        reputace_pred = hra.frakce.frakce[udalost["frakce_id"]].reputace

        with patch("builtins.input", return_value="0"), redirect_stdout(io.StringIO()):
            self.assertTrue(svet._vyres_udalost_mesta(hra, udalost))

        ocekavany_pokles = 3 if udalost["metrika"] == "stabilita" else 2
        self.assertEqual(
            getattr(mesto, udalost["metrika"]),
            metrika_pred - ocekavany_pokles,
        )
        self.assertEqual(
            hra.frakce.frakce[udalost["frakce_id"]].reputace,
            reputace_pred - 2,
        )
        self.assertEqual(npc["vztah_hraci"], -1)

    def test_karavana_postupuje_po_propojene_trase_a_je_ulozitelna(self):
        hra = Hra()
        hra.hrac.den = 5
        hra.zivy_svet.posun_den(hra)

        self.assertEqual(len(hra.zivy_svet.karavany), 1)
        cesta = hra.zivy_svet.karavany[0]["cesta"]
        self.assertTrue(all(
            b in LOKACE[a]["sousedni"] for a, b in zip(cesta, cesta[1:])
        ))
        self.assertEqual(len(Hra.from_dict(hra.to_dict()).zivy_svet.karavany), 1)


if __name__ == "__main__":
    unittest.main()
