"""Denní simulace frakcí, NPC a rozhodovacích situací."""

import random
from copy import deepcopy
from dataclasses import dataclass, field

from data.mesta import DOPADY_AI_NPC, FRAKCNI_ZONY, MESTA, PROFILY_AI_NPC
from data.frakcni_kroniky import (
    FRAKCNI_PROFILY,
    MESTSKE_STAROSTI,
    TRZNI_ZBOZI,
    VYCHOZI_SKLADY,
)
from game.svet import LOKACE
from models.mesto import StavMesta
from utils.decision_ai import vyber_nejlepsi_uzitek, vzdalenosti_od_cilu
from utils.vypis import tisk_chyba, tisk_info, tisk_ok, vytiskni_volbu


FRAKCNI_CILE = {
    "policie": ("Udržet pořádek ve čtvrtích", "Stráž posiluje hlídky a hledá podporu obyvatel."),
    "podsveti": ("Rozšířit vliv v podzemí", "Gangy budují nové kontakty a soupeří o kontrolu uliček."),
    "cirkev": ("Odhalit zakázané aktivity", "Inkvizice sbírá svědectví a hledá stopy po dominiu."),
    "obchodnici": ("Zajistit bezpečné obchodní trasy", "Kupci připravují karavany a vyjednávají výhodnější průchod."),
    "kult_krve": ("Shromáždit suroviny pro rituál", "Kult pátrá po vzácných přísadách a příznivcích."),
    "syndikat_stinu": ("Získat převahu v informační síti", "Špehové vyměňují zprávy a mapují slabá místa rivalů."),
    "cech_kurtizan": ("Získat nové mecenáše", "Cech pořádá společenská setkání a rozšiřuje své kontakty."),
    "narkomani": ("Omezit pouliční krize", "Dobrovolníci hledají bezpečnější pomoc pro lidi v nouzi."),
    "cyberpunkaci": ("Ovládnout městskou datovou síť", "Technici opravují uzly a obchodují s ověřenými informacemi."),
    "nymfomanky": ("Uspořádat dobrovolný slavnostní večer", "Organizátorky připravují společenskou akci s jasnými pravidly účasti."),
    "gembleri": ("Rozšířit vliv heren", "Gamblerů lákají další návštěvníky ke stolům a zároveň řeší rostoucí dluhy svých členů."),
    "systemaci": ("Udržet SoundSystem bezpečný a přístupný", "Zvukaři a pořadatelé opravují aparaturu a spolupracují s dobrovolníky."),
}

FRAKCNI_AKCE = {
    "policie": (
        "posílila hlídky",
        "bezpeci",
        {"bezpeci": 1, "stabilita": 1},
    ),
    "podsveti": (
        "rozšířilo noční obchod",
        "prosperita",
        {"prosperita": 1, "bezpeci": -1},
    ),
    "cirkev": (
        "zprostředkovala veřejné smírčí jednání",
        "stabilita",
        {"stabilita": 1, "bezpeci": 1},
    ),
    "obchodnici": (
        "otevřeli novou obchodní trasu",
        "prosperita",
        {"prosperita": 1, "bezpeci": 1},
    ),
    "kult_krve": (
        "vyvolal neklid kolem tajného rituálu",
        "stabilita",
        {"stabilita": -1, "bezpeci": -1},
    ),
    "syndikat_stinu": (
        "rozšířil síť ověřených zpráv",
        "stabilita",
        {"stabilita": 1},
    ),
    "cech_kurtizan": (
        "uspořádal dobrovolný společenský večer",
        "prosperita",
        {"prosperita": 1, "stabilita": 1},
    ),
    "narkomani": (
        "zajistili bezpečnější pouliční pomoc",
        "bezpeci",
        {"bezpeci": 1, "stabilita": 1},
    ),
    "cyberpunkaci": (
        "opravili městské komunikační uzly",
        "stabilita",
        {"stabilita": 1, "prosperita": 1},
    ),
    "nymfomanky": (
        "uspořádaly slavnost s jasnými pravidly účasti",
        "prosperita",
        {"prosperita": 1, "stabilita": 1},
    ),
    "gembleri": (
        "uspořádali noční turnaj v kostkách",
        "prosperita",
        {"prosperita": 1, "stabilita": -1},
    ),
    "systemaci": (
        "uspořádali bezpečný SoundSystem večer",
        "stabilita",
        {"stabilita": 1, "prosperita": 1},
    ),
}

FRAKCNI_TRZNI_DOPADY = {
    "policie": {"zasoby": -1, "zelezo": -1},
    "podsveti": {"zelezo": -1, "krystaly": 1},
    "cirkev": {"zasoby": 1, "krystaly": -1},
    "obchodnici": {"zasoby": 2, "drevo": 1, "zelezo": 1},
    "kult_krve": {"krystaly": -2, "kamen": -1},
    "syndikat_stinu": {"krystaly": -1, "zasoby": 1},
    "cech_kurtizan": {"zasoby": -1, "drevo": 1},
    "narkomani": {"zasoby": -1, "krystaly": 1},
    "cyberpunkaci": {"zelezo": -2, "krystaly": 1},
    "nymfomanky": {"zasoby": -1, "drevo": 1},
    "gembleri": {"zasoby": -1, "zelezo": 1},
    "systemaci": {"krystaly": -1, "zasoby": 1},
}

NPC_POMOC = {
    "mira_lecitelka": {
        "zadost": "potřebuje zásoby pro ošetřovnu a bezpečnější cestu",
        "cena": 10,
        "mesto": {"bezpeci": 3, "stabilita": 1},
    },
    "radan_paserak": {
        "zadost": "shání pomoc s dodávkou pro přístavní dělníky",
        "cena": 10,
        "mesto": {"prosperita": 2},
        "trziste": {"zasoby": 1},
    },
    "elian_informator": {
        "zadost": "ověřuje zprávu, která může uklidnit městskou radu",
        "cena": 10,
        "mesto": {"stabilita": 2},
        "vyzkum": 1,
    },
    "selene_vedma": {
        "zadost": "potřebuje pomoc s bezpečným průzkumem zvláštního úkazu",
        "cena": 10,
        "mesto": {"stabilita": 1},
        "vyzkum": 2,
    },
    "talia_kupkyne": {
        "zadost": "vyjednává o zásobách pro tržiště",
        "cena": 10,
        "mesto": {"prosperita": 3},
        "trziste": {"zasoby": 2, "drevo": 1},
    },
    "vespera_kuryrka": {
        "zadost": "hledá svědky pro klidné jednání s chrámem",
        "cena": 10,
        "mesto": {"stabilita": 2},
        "inkvizice": -1,
    },
    "nela_umelkyne": {
        "zadost": "připravuje bezpečné setkání pro místní umělce",
        "cena": 10,
        "mesto": {"prosperita": 2, "stabilita": 1},
    },
    "nora_kartografka": {
        "zadost": "potřebuje ověřit bezpečnou trasu mezi akademií a tržištěm",
        "cena": 10,
        "mesto": {"stabilita": 2},
        "vyzkum": 1,
    },
    "zora_bylinkarka": {
        "zadost": "shání pomoc se semeny pro komunitní léčivou zahradu",
        "cena": 10,
        "mesto": {"bezpeci": 1, "prosperita": 1},
        "trziste": {"zasoby": 1},
    },
    "mira_vychodni": {
        "zadost": "zajišťuje první pomoc pro říční osadu",
        "cena": 10,
        "mesto": {"bezpeci": 2, "stabilita": 1},
    },
    "rovan_kapitan": {
        "zadost": "posiluje hlídku u východního mostu",
        "cena": 10,
        "mesto": {"bezpeci": 3},
    },
    "vesna_radni": {
        "zadost": "vyjednává pravidelné zásoby pro Východní Brod",
        "cena": 10,
        "mesto": {"prosperita": 2, "stabilita": 1},
        "trziste": {"zasoby": 1, "zelezo": 1},
    },
}

FRAKCNI_RIVALOVE = (
    ("policie", "podsveti"),
    ("obchodnici", "syndikat_stinu"),
    ("cirkev", "kult_krve"),
    ("cech_kurtizan", "nymfomanky"),
    ("narkomani", "cyberpunkaci"),
    ("gembleri", "policie"),
    ("systemaci", "narkomani"),
)

FRAKCNI_SPOJENCI = {frozenset(("systemaci", "narkomani"))}

TRASA_KARAVANY = (
    "trh",
    "pristav",
    "vychodni_pristav",
    "vychodni_trziste",
)

VYCHOZI_POSTAVY = (
    {
        "id": "mira_lecitelka", "jmeno": "Mira", "role": "Potulná léčitelka",
        "frakce": "policie", "lokace": "hostinec", "duvera": 0,
        "akce": (
            "Objíždí čtvrti a nabízí první pomoc.",
            "Připravuje zásoby pro městskou ošetřovnu.",
            "Vyslechla obyvatele a předala zprávu stráži.",
        ),
    },
    {
        "id": "radan_paserak", "jmeno": "Radan", "role": "Pašerák",
        "frakce": "podsveti", "lokace": "pristav", "duvera": 0,
        "akce": (
            "Vyjednává o průchodu zboží městem.",
            "Hledá bezpečnější cestu pro noční zásilku.",
            "Vyměnil zprávy s přístavními kontakty.",
        ),
    },
    {
        "id": "elian_informator", "jmeno": "Elian", "role": "Informátor",
        "frakce": "syndikat_stinu", "lokace": "trh", "duvera": 0,
        "akce": (
            "Ověřuje zprávy mezi městskými čtvrtěmi.",
            "Předává radě ověřené informace z tržiště.",
            "Sleduje, kdo se vyptává na městské plány.",
        ),
    },
    {
        "id": "selene_vedma", "jmeno": "Selene", "role": "Vědma",
        "frakce": "kult_krve", "lokace": "akademie", "duvera": 0,
        "akce": (
            "Studuje změny v magických proudech.",
            "Sbírá svědectví o zvláštních světlech nad městem.",
            "Vyměnila s akademiky poznámky o starých runách.",
        ),
    },
    {
        "id": "talia_kupkyne", "jmeno": "Talia", "role": "Kupecká vyjednavačka",
        "frakce": "obchodnici", "lokace": "cechovni_ulicky", "duvera": 0,
        "akce": (
            "Sjednává bezpečný průjezd pro karavanu.",
            "Kontroluje ceny a dostupnost zásob.",
            "Vyjednala s cechem nový obchodní termín.",
        ),
    },
    {
        "id": "vespera_kuryrka", "jmeno": "Vespera", "role": "Kurýrka",
        "frakce": "cirkev", "lokace": "chram_cistoty", "duvera": 0,
        "akce": (
            "Předává zprávy mezi chrámem a městskou radou.",
            "Vyslýchá svědky a ověřuje jejich výpovědi.",
            "Dohlíží na hlídky u městských bran.",
        ),
    },
    {
        "id": "nela_umelkyne", "jmeno": "Nela", "role": "Městská umělkyně",
        "frakce": "cech_kurtizan", "lokace": "cervena_ctvrt", "duvera": 0,
        "akce": (
            "Připravuje večerní vystoupení pro dobrovolné hosty.",
            "Domlouvá se s mecenáši na podmínkách večerní akce.",
            "Rozšiřuje síť bezpečných a dobrovolných společenských setkání.",
        ),
    },
    {
        "id": "nora_kartografka", "jmeno": "Nora", "role": "Městská kartografka",
        "frakce": "cyberpunkaci", "lokace": "akademicke_namesti", "duvera": 0,
        "akce": (
            "Ověřuje pěší cesty mezi akademickým náměstím a tržištěm.",
            "Vyznačuje na mapě místa, kde mohou cestovatelé požádat o pomoc.",
        ),
    },
    {
        "id": "zora_bylinkarka", "jmeno": "Zora", "role": "Bylinkářka komunitní zahrady",
        "frakce": "nymfomanky", "lokace": "botanicke_zahrady", "duvera": 0,
        "akce": (
            "Pěstuje léčivé byliny pro místní ošetřovnu.",
            "Učí zahradníky, jak bezpečně uchovávat semena.",
        ),
    },
    {
        "id": "mira_vychodni", "jmeno": "Mira z Brodu",
        "role": "Léčitelka říčních osad", "frakce": "policie",
        "lokace": "vychodni_zahrady", "duvera": 0,
        "akce": (
            "Zřídila ošetřovnu pro karavanové dělníky.",
            "Pomohla obyvatelům opravit zavlažovací kanál.",
        ),
    },
    {
        "id": "rovan_kapitan", "jmeno": "Kapitán Rovan",
        "role": "Velitel pohraniční hlídky", "frakce": "policie",
        "lokace": "vychodni_kasarna", "duvera": 0,
        "akce": (
            "Zkontroloval hlídky u východního mostu.",
            "Doprovodil karavanu přes nebezpečný úsek cesty.",
        ),
    },
    {
        "id": "vesna_radni", "jmeno": "Vesna z městské rady",
        "role": "Vyjednavačka Východního Brodu", "frakce": "obchodnici",
        "lokace": "rada_vychodniho_brodu", "duvera": 0,
        "akce": (
            "Zprostředkovala jednání mezi radou a cechy.",
            "Vyjednala zásoby pro čtvrti za řekou.",
        ),
    },
    {
        "id": "dj_runa", "jmeno": "Runa", "role": "DJ SoundSystemu",
        "frakce": "systemaci", "lokace": "tekno_party", "duvera": 0,
        "akce": (
            "Zkouší aparaturu před večerním programem.",
            "Domlouvá vystoupení místních hudebníků.",
            "Připravila klidné místo pro návštěvníky, kteří potřebují pauzu.",
        ),
    },
    {
        "id": "ivo_systemak", "jmeno": "Ivo", "role": "Zvukař Systemáků",
        "frakce": "systemaci", "lokace": "tekno_party", "duvera": 0,
        "akce": (
            "Opravuje světelný uzel SoundSystemu.",
            "Koordinuje dobrovolný doprovod s místními pomocníky.",
        ),
    },
    {
        "id": "lexa_party", "jmeno": "Lexa", "role": "Klubová organizátorka",
        "frakce": "systemaci", "lokace": "tekno_party", "duvera": 0,
        "akce": (
            "Zajišťuje bezpečné zázemí pro účastníky večera.",
            "Spojuje umělce s komunitními dobrovolníky.",
        ),
    },
    {
        "id": "sara_signalistka", "jmeno": "Sára", "role": "Výpravčí říčních tras",
        "frakce": "obchodnici", "lokace": "vychodni_pristav", "duvera": 0,
        "akce": (
            "Kontroluje světelné značky pro karavany.",
            "Domlouvá s hlídkami bezpečný příjezd do přístavu.",
        ),
    },
)

MOZNOSTI_ZASAHU = (
    {"text": "Podpořit cíl a získat přízeň frakce (25 zlata)", "cena": 25, "frakce": 8, "mesto": 1},
    {"text": "Vyjednat kompromis (10 zlata)", "cena": 10, "frakce": 3, "mesto": 2},
    {"text": "Postavit se plánu a oslabit vliv frakce", "cena": 0, "frakce": -6, "mesto": -1},
)

UDALOSTI_MESTA = {
    "karavana": {
        "frakce": "obchodnici",
        "nazev": "Karavana žádá o bezpečný průjezd",
        "text": "Kupecká karavana čeká na zajištění trasy a zásob.",
        "volby": (
            ("Zajistit průjezd (25 zl.)", 25, {"prosperita": 5, "stabilita": 1}, 5),
            ("Vyjednat pomoc místních (bez nákladů)", 0, {"prosperita": 2, "stabilita": 1}, 2),
        ),
        "zanik": {"prosperita": -2, "bezpeci": -1},
    },
    "most": {
        "frakce": "obchodnici",
        "nazev": "Městský most potřebuje opravu",
        "text": "Poškozený most brzdí dopravu mezi čtvrtěmi a okolními osadami.",
        "volby": (
            ("Zaplatit opravu (30 zl.)", 30, {"prosperita": 2, "bezpeci": 5}, 4),
            ("Povolat dobrovolníky (10 zl.)", 10, {"bezpeci": 2, "stabilita": 1}, 2),
        ),
        "zanik": {"prosperita": -2, "bezpeci": -2},
    },
    "hlidky": {
        "frakce": "policie",
        "nazev": "Obyvatelé žádají posílit hlídky",
        "text": "Obchodníci a rodiny hlásí neklid na cestách a v okrajových čtvrtích.",
        "volby": (
            ("Zaplatit posílené hlídky (20 zl.)", 20, {"bezpeci": 5, "stabilita": 2}, 5),
            ("Požádat místní o spolupráci", 0, {"bezpeci": 2, "stabilita": 1}, 2),
        ),
        "zanik": {"bezpeci": -3, "stabilita": -1},
    },
    "trzni_oziveni": {
        "frakce": "obchodnici",
        "nazev": "Noví klienti dorazili na tržiště",
        "text": "Dobrá pověst trasy přivedla do města nové kupce.",
        "volby": (
            ("Podpořit místní stánky (10 zl.)", 10, {"prosperita": 3}, 3),
            ("Ponechat trh samostatně", 0, {"prosperita": 1}, 1),
        ),
        "zanik": {"prosperita": -1},
    },
    "bezpecna_ctvrt": {
        "frakce": "policie",
        "nazev": "Obyvatelé chtějí udržet klid",
        "text": "Po úspěšné hlídce se místní domlouvají, jak udržet pořádek.",
        "volby": (
            ("Zajistit komunitní hlídku (15 zl.)", 15, {"bezpeci": 3, "stabilita": 2}, 3),
            ("Pověřit místní radu", 0, {"stabilita": 2}, 2),
        ),
        "zanik": {"bezpeci": -2},
    },
    "trzni_nepokoj": {
        "frakce": "obchodnici",
        "nazev": "Tržiště řeší následky zdržení",
        "text": "Zpožděné zásoby zvedly ceny a obchodníci žádají pomoc.",
        "volby": (
            ("Doplnit zásoby (15 zl.)", 15, {"prosperita": 2, "stabilita": 1}, 2),
            ("Nechat ceny trhu volně", 0, {"stabilita": 1}, 1),
        ),
        "zanik": {"prosperita": -2, "stabilita": -1},
    },
    "frakcni_iniciativa": {
        "frakce": "policie",
        "nazev": "Městská iniciativa",
        "text": "Místní postava žádá o podporu pro svou čtvrť.",
        "volby": (),
        "zanik": {"stabilita": -1},
    },
}

MISTA_UDALOSTI = {
    "karavana": {"stare_mesto": "trh", "vychodni_brod": "vychodni_trziste"},
    "most": {"stare_mesto": "pristav", "vychodni_brod": "vychodni_pristav"},
    "hlidky": {"stare_mesto": "hranice", "vychodni_brod": "vychodni_kasarna"},
    "trzni_oziveni": {"stare_mesto": "trh", "vychodni_brod": "vychodni_trziste"},
    "trzni_nepokoj": {"stare_mesto": "trh", "vychodni_brod": "vychodni_trziste"},
    "bezpecna_ctvrt": {"stare_mesto": "hostinec", "vychodni_brod": "vychodni_kasarna"},
    "frakcni_iniciativa": {"stare_mesto": "trh", "vychodni_brod": "vychodni_trziste"},
}


@dataclass
class ZivySvetSystem:
    posledni_den: int = 0
    frakcni_cile: dict = field(default_factory=dict)
    postavy: list = field(default_factory=lambda: deepcopy(VYCHOZI_POSTAVY))
    nabidky: list = field(default_factory=list)
    historie: list = field(default_factory=list)
    mesta: dict = field(default_factory=dict)
    kontrola_lokaci: dict = field(default_factory=dict)
    udalosti_mesta: list = field(default_factory=list)
    navazujici_udalosti: list = field(default_factory=list)
    vztahy_frakci: dict = field(default_factory=dict)
    karavany: list = field(default_factory=list)
    trziste_sklady: dict = field(default_factory=dict)
    dalsi_frakce: int = 0
    dalsi_postava: int = 0
    posledni_slavnosti: dict = field(default_factory=dict)

    def __post_init__(self):
        for frakce_id, (nazev, popis) in FRAKCNI_CILE.items():
            cil = self.frakcni_cile.get(frakce_id)
            if not isinstance(cil, dict):
                cil = {}
                self.frakcni_cile[frakce_id] = cil
            cil.setdefault("nazev", nazev)
            cil.setdefault("popis", popis)
            cil.setdefault("nazev_zakladni", nazev)
            cil.setdefault("popis_zakladni", popis)
            cil["cil"] = max(1, min(10, _kladne_cislo(cil.get("cil", 3))))
            cil["postup"] = min(cil["cil"], _kladne_cislo(cil.get("postup", 0)))
            cil["uroven"] = max(1, min(5, _kladne_cislo(cil.get("uroven", 1))))
            cil["evoluce"] = _kladne_cislo(cil.get("evoluce", 0))
            mesto_id = cil.get("mesto_id")
            if mesto_id not in MESTA:
                mesto_id = _prvni_mesto_frakce(frakce_id)
            cil["mesto_id"] = mesto_id
            cil["posledni_akce"] = (
                cil.get("posledni_akce")
                if isinstance(cil.get("posledni_akce"), str)
                else ""
            )
        self.postavy = [p for p in self.postavy if isinstance(p, dict)]
        for index, postava in enumerate(self.postavy):
            postava.setdefault("id", f"npc_{index}")
            postava.setdefault("jmeno", "Neznámá postava")
            postava.setdefault("role", "Obyvatel města")
            postava.setdefault("frakce", "")
            postava.setdefault("lokace", "trh")
            postava.setdefault("duvera", 0)
            postava.setdefault("pribeh", 0)
            postava.setdefault("vztah_hraci", 0)
            postava.setdefault("posledni_rozhovor", "")
            postava.setdefault("posledni_akce", "")
            postava.setdefault("posledni_pomoc_den", 0)
            if postava.get("lokace") not in LOKACE:
                postava["lokace"] = "trh"
            if postava.get("frakce") not in FRAKCNI_CILE:
                postava["frakce"] = ""
            if not isinstance(postava.get("akce"), (str, tuple, list)):
                postava["akce"] = ("Prochází městem a vyřizuje své záležitosti.",)
            postava["pribeh"] = max(0, min(3, _kladne_cislo(postava["pribeh"])))
            postava["vztah_hraci"] = max(
                -100, min(100, _signed_cislo(postava["vztah_hraci"]))
            )
            if not isinstance(postava["posledni_rozhovor"], str):
                postava["posledni_rozhovor"] = ""
            if not isinstance(postava["posledni_akce"], str):
                postava["posledni_akce"] = ""
            postava["posledni_pomoc_den"] = _kladne_cislo(
                postava["posledni_pomoc_den"]
            )
        for definice in VYCHOZI_POSTAVY:
            if not any(p.get("id") == definice["id"] for p in self.postavy):
                self.postavy.append(deepcopy(definice))
            else:
                postava = next(p for p in self.postavy if p.get("id") == definice["id"])
                for klic, hodnota in definice.items():
                    postava.setdefault(klic, hodnota)
        ulozena_mesta = self.mesta if isinstance(self.mesta, dict) else {}
        self.mesta = {
            mesto_id: StavMesta.from_dict(
                ulozena_mesta.get(mesto_id),
                {
                    "ident": mesto_id,
                    "nazev": definice["nazev"],
                    "prosperita": definice["prosperita"],
                    "bezpeci": definice["bezpeci"],
                    "stabilita": definice["stabilita"],
                },
            )
            for mesto_id, definice in MESTA.items()
        }
        ulozene_sklady = (
            self.trziste_sklady if isinstance(self.trziste_sklady, dict) else {}
        )
        self.trziste_sklady = {}
        for mesto_id, vychozi_sklad in VYCHOZI_SKLADY.items():
            sklad = ulozene_sklady.get(mesto_id)
            sklad = sklad if isinstance(sklad, dict) else {}
            self.trziste_sklady[mesto_id] = {
                zbozi_id: max(
                    0,
                    min(60, _kladne_cislo(sklad.get(zbozi_id, mnozstvi))),
                )
                for zbozi_id, mnozstvi in vychozi_sklad.items()
                if zbozi_id in TRZNI_ZBOZI
            }
        ulozena_kontrola = (
            self.kontrola_lokaci if isinstance(self.kontrola_lokaci, dict) else {}
        )
        self.kontrola_lokaci = {}
        for lokace_id in LOKACE:
            vliv = ulozena_kontrola.get(lokace_id)
            if not isinstance(vliv, dict):
                vlastnik = _vychozi_frakce_lokace(lokace_id)
                vliv = {vlastnik: 55}
                rival = next(
                    (frakce for frakce in FRAKCNI_CILE if frakce != vlastnik),
                    vlastnik,
                )
                vliv[rival] = 30
            ocisteny = {
                frakce_id: max(0, min(100, _kladne_cislo(hodnota)))
                for frakce_id, hodnota in vliv.items()
                if frakce_id in FRAKCNI_CILE
            }
            if not ocisteny:
                ocisteny[_vychozi_frakce_lokace(lokace_id)] = 55
            self.kontrola_lokaci[lokace_id] = ocisteny
        udalosti = []
        if isinstance(self.udalosti_mesta, list):
            for udalost in self.udalosti_mesta:
                if (
                    not isinstance(udalost, dict)
                    or udalost.get("mesto_id") not in MESTA
                    or udalost.get("typ") not in UDALOSTI_MESTA
                    or not isinstance(udalost.get("den"), int)
                ):
                    continue
                udalost = deepcopy(udalost)
                udalost["den"] = max(0, udalost["den"])
                if udalost["typ"] == "frakcni_iniciativa":
                    frakce_id = udalost.get("frakce_id")
                    if frakce_id not in FRAKCNI_CILE:
                        frakce_id = "policie"
                    udalost["frakce_id"] = frakce_id
                    npc_id = udalost.get("npc_id")
                    if not isinstance(npc_id, str) or not any(
                        postava.get("id") == npc_id for postava in self.postavy
                    ):
                        npc_id = next(
                            (
                                postava.get("id") for postava in self.postavy
                                if postava.get("frakce") == frakce_id
                            ),
                            "",
                        )
                    udalost["npc_id"] = npc_id
                    metrika = udalost.get("metrika")
                    if metrika not in ("prosperita", "bezpeci", "stabilita"):
                        metrika = "stabilita"
                    udalost["metrika"] = metrika
                    udalost["nazev"] = f"Iniciativa: {FRAKCNI_CILE[frakce_id][0]}"
                    npc = next(
                        (
                            postava for postava in self.postavy
                            if postava.get("id") == npc_id
                        ),
                        None,
                    )
                    profil = FRAKCNI_PROFILY.get(frakce_id, {})
                    starost = profil.get("starost", "Místní obyvatelé žádají o pomoc.")
                    akce = npc.get("posledni_akce", "") if npc else ""
                    akce_text = f" Její poslední krok: {akce}" if akce else ""
                    ulozeny_text = udalost.get("text")
                    udalost["text"] = (
                        ulozeny_text
                        if isinstance(ulozeny_text, str) and ulozeny_text
                        else (
                            f"{npc['jmeno']} ({npc['role']}) žádá o pomoc. "
                            f"{starost}{akce_text}"
                            if npc else starost
                        )
                    )
                else:
                    udalost["nazev"] = UDALOSTI_MESTA[udalost["typ"]]["nazev"]
                    udalost["text"] = UDALOSTI_MESTA[udalost["typ"]]["text"]
                udalost["lokace_id"] = _lokace_udalosti(
                    udalost["typ"], udalost["mesto_id"]
                )
                if udalost["typ"] == "frakcni_iniciativa":
                    npc = next(
                        (
                            postava for postava in self.postavy
                            if postava.get("id") == udalost["npc_id"]
                        ),
                        None,
                    )
                    if npc and _mesto_lokace(npc.get("lokace", "")) == udalost["mesto_id"]:
                        udalost["lokace_id"] = npc["lokace"]
                udalosti.append(udalost)
        self.udalosti_mesta = udalosti[-3:]
        ulozene_vztahy = (
            self.vztahy_frakci if isinstance(self.vztahy_frakci, dict) else {}
        )
        self.vztahy_frakci = {
            _klic_vztahu(*dvojice): max(
                -100,
                min(
                    100,
                    _signed_cislo(
                        ulozene_vztahy.get(
                            _klic_vztahu(*dvojice),
                            40 if frozenset(dvojice) in FRAKCNI_SPOJENCI else -20,
                        )
                    ),
                ),
            )
            for dvojice in FRAKCNI_RIVALOVE
        }
        if not isinstance(self.karavany, list):
            self.karavany = []
        platne_karavany = []
        for karavana in self.karavany:
            if not isinstance(karavana, dict):
                continue
            cesta = karavana.get("cesta")
            pozice = karavana.get("pozice")
            if (
                not isinstance(cesta, list)
                or len(cesta) < 2
                or not all(isinstance(lokace, str) and lokace in LOKACE for lokace in cesta)
                or not all(
                    dalsi in LOKACE[lokace]["sousedni"]
                    for lokace, dalsi in zip(cesta, cesta[1:])
                )
                or not isinstance(pozice, int)
                or isinstance(pozice, bool)
                or not 0 <= pozice < len(cesta)
                or karavana.get("stav") != "na_ceste"
            ):
                continue
            platne_karavany.append({
                "id": (
                    karavana.get("id")
                    if isinstance(karavana.get("id"), str)
                    else f"karavana-{_kladne_cislo(karavana.get('odeslano'))}"
                ),
                "cesta": list(cesta),
                "pozice": pozice,
                "stav": "na_ceste",
                "odeslano": _kladne_cislo(karavana.get("odeslano")),
                "doprovod": karavana.get("doprovod") is True,
            })
        self.karavany = platne_karavany[:3]
        if not isinstance(self.navazujici_udalosti, list):
            self.navazujici_udalosti = []
        navazujici = []
        for udalost in self.navazujici_udalosti:
            if (
                not isinstance(udalost, dict)
                or udalost.get("mesto_id") not in MESTA
                or udalost.get("typ") not in UDALOSTI_MESTA
                or not isinstance(udalost.get("den"), int)
            ):
                continue
            navazujici.append({
                "den": max(0, udalost["den"]),
                "mesto_id": udalost["mesto_id"],
                "typ": udalost["typ"],
                "retizec": (
                    udalost.get("retizec")
                    if isinstance(udalost.get("retizec"), str) else ""
                ),
            })
        self.navazujici_udalosti = navazujici[-5:]
        self.nabidky = [
            nabidka for nabidka in self.nabidky
            if isinstance(nabidka, dict)
            and all(
                isinstance(nabidka.get(klic), str)
                for klic in ("frakce_id", "frakce_nazev", "cilek", "text", "postava")
            )
        ]
        self.historie = [
            zaznam for zaznam in self.historie
            if isinstance(zaznam, dict)
            and "den" in zaznam
            and isinstance(zaznam.get("text"), str)
        ][-30:]
        self.dalsi_frakce %= len(FRAKCNI_CILE)
        self.dalsi_postava %= max(1, len(self.postavy))
        ulozene_slavnosti = (
            self.posledni_slavnosti
            if isinstance(self.posledni_slavnosti, dict) else {}
        )
        self.posledni_slavnosti = {
            mesto_id: _kladne_cislo(ulozene_slavnosti.get(mesto_id, 0))
            for mesto_id in MESTA
        }

    def to_dict(self):
        return {
            "posledni_den": self.posledni_den,
            "frakcni_cile": deepcopy(self.frakcni_cile),
            "postavy": deepcopy(self.postavy),
            "nabidky": deepcopy(self.nabidky),
            "historie": deepcopy(self.historie[-30:]),
            "mesta": {
                mesto_id: mesto.to_dict()
                for mesto_id, mesto in self.mesta.items()
            },
            "kontrola_lokaci": deepcopy(self.kontrola_lokaci),
            "udalosti_mesta": deepcopy(self.udalosti_mesta),
            "navazujici_udalosti": deepcopy(self.navazujici_udalosti),
            "vztahy_frakci": deepcopy(self.vztahy_frakci),
            "karavany": deepcopy(self.karavany),
            "trziste_sklady": deepcopy(self.trziste_sklady),
            "dalsi_frakce": self.dalsi_frakce,
            "dalsi_postava": self.dalsi_postava,
            "posledni_slavnosti": deepcopy(self.posledni_slavnosti),
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data živého světa musí být objekt.")
        cile = data.get("frakcni_cile", {})
        postavy = data.get("postavy", [])
        nabidky = data.get("nabidky", [])
        historie = data.get("historie", [])
        mesta = data.get("mesta", {})
        kontrola_lokaci = data.get("kontrola_lokaci", {})
        udalosti_mesta = data.get("udalosti_mesta", [])
        navazujici_udalosti = data.get("navazujici_udalosti", [])
        vztahy_frakci = data.get("vztahy_frakci", {})
        karavany = data.get("karavany", [])
        trziste_sklady = data.get("trziste_sklady", {})
        posledni_slavnosti = data.get("posledni_slavnosti", {})
        if not isinstance(cile, dict) or not isinstance(postavy, list):
            raise ValueError("Uložený živý svět má neplatný formát.")
        if (
            not isinstance(nabidky, list)
            or not isinstance(historie, list)
            or not isinstance(mesta, dict)
            or not isinstance(kontrola_lokaci, dict)
            or not isinstance(udalosti_mesta, list)
            or not isinstance(navazujici_udalosti, list)
            or not isinstance(vztahy_frakci, dict)
            or not isinstance(karavany, list)
            or not isinstance(trziste_sklady, dict)
            or not isinstance(posledni_slavnosti, dict)
        ):
            raise ValueError("Uložené události živého světa mají neplatný formát.")
        return cls(
            posledni_den=_kladne_cislo(data.get("posledni_den", 0)),
            frakcni_cile=deepcopy(cile),
            postavy=deepcopy(postavy),
            nabidky=deepcopy(nabidky),
            historie=deepcopy(historie[-30:]),
            mesta=deepcopy(mesta),
            kontrola_lokaci=deepcopy(kontrola_lokaci),
            udalosti_mesta=deepcopy(udalosti_mesta[-3:]),
            navazujici_udalosti=deepcopy(navazujici_udalosti[-5:]),
            vztahy_frakci=deepcopy(vztahy_frakci),
            karavany=deepcopy(karavany[-3:]),
            trziste_sklady=deepcopy(trziste_sklady),
            dalsi_frakce=_kladne_cislo(data.get("dalsi_frakce", 0)),
            dalsi_postava=_kladne_cislo(data.get("dalsi_postava", 0)),
            posledni_slavnosti=deepcopy(posledni_slavnosti),
        )

    def posun_den(self, hra):
        """Simuluje jeden den; opakované volání ve stejný den stav nemění."""
        den = max(1, int(hra.hrac.den))
        if self.posledni_den >= den:
            return []
        self.posledni_den = den
        zpravy = []
        for mesto in self.mesta.values():
            mesto.posun_den()
        self._doplnit_trziste()
        self._vyres_expirovane_udalosti(den, zpravy)
        self._aktivuj_nasledne_udalosti(den, zpravy)

        frakce_ids = tuple(FRAKCNI_CILE)
        vedlejsi_frakce = random.choice(
            tuple(
                frakce_id for frakce_id in frakce_ids
                if frakce_id != frakce_ids[self.dalsi_frakce % len(frakce_ids)]
            )
        )
        dnesni_frakce = (
            frakce_ids[self.dalsi_frakce % len(frakce_ids)],
            vedlejsi_frakce,
        )
        for frakce_id in dnesni_frakce:
            zprava_cile = self._vykonej_cil_fakce(frakce_id)
            if zprava_cile:
                zpravy.append(zprava_cile)
            zmena_kontroly = self._rozsir_vliv_fakce(frakce_id, den)
            if zmena_kontroly:
                zpravy.append(zmena_kontroly)
            cil = self.frakcni_cile[frakce_id]
            postup_pred = cil["postup"]
            cil["postup"] = min(cil["cil"], int(cil.get("postup", 0)) + 1)
            if cil["postup"] >= cil["cil"]:
                if len(self.nabidky) < 10:
                    cil["postup"] = 0
                    vyvoj = self._vyvin_cil_fakce(frakce_id)
                    nabidka = self._vytvor_nabidku(frakce_id, den)
                    self.nabidky.append(nabidka)
                    zpravy.append(
                        f"{nabidka['frakce_nazev']} pokročila ve svém cíli: "
                        f"{nabidka['cilek']}. Na rozhodnutí čeká nová situace."
                    )
                    zpravy.append(vyvoj)
                elif postup_pred < cil["cil"]:
                    zpravy.append(
                        f"{FRAKCNI_CILE[frakce_id][0]} dokončila cíl, ale "
                        "čeká na uvolnění fronty rozhodnutí."
                    )
        self.dalsi_frakce = (self.dalsi_frakce + 1) % len(frakce_ids)
        zprava_sporu = self._vyhodnot_soupereni(den)
        if zprava_sporu:
            zpravy.append(zprava_sporu)

        if den % 4 == 0 and len(self.udalosti_mesta) < 3:
            if den % 12 == 0:
                udalost = self._vytvor_frakcni_iniciativu(den)
            else:
                udalost = self._vytvor_udalost_mesta(den)
            self.udalosti_mesta.append(udalost)
            zpravy.append(
                f"{self.mesta[udalost['mesto_id']].nazev}: "
                f"{udalost['nazev'].lower()}. Ve městě čeká rozhodnutí."
            )
        zpravy.extend(self._posun_karavany(hra, den))

        postava = self.postavy[self.dalsi_postava % len(self.postavy)]
        self.dalsi_postava = (self.dalsi_postava + 1) % len(self.postavy)
        nova_lokace = self._rozhodni_pohyb_npc(postava)
        if not nova_lokace:
            nova_lokace = postava.get("lokace", "trh")
        postava["lokace"] = nova_lokace
        if hasattr(hra, "svet"):
            hra.svet.odhal_lokaci(nova_lokace)
        mesto_id = _mesto_lokace(nova_lokace)
        dopad = DOPADY_AI_NPC.get(postava.get("id"))
        if dopad and mesto_id in self.mesta:
            self.mesta[mesto_id].uprav_akci(*dopad)
        akce = postava["akce"]
        if isinstance(akce, (tuple, list)):
            akce = random.choice(akce)
        postava["posledni_akce"] = akce
        zpravy.append(
            f"{postava['jmeno']} ({postava['role']}) se přesunula do lokace "
            f"{nova_lokace.replace('_', ' ')}. {akce}"
        )
        self.historie.extend({"den": den, "text": zprava} for zprava in zpravy)
        self.historie = self.historie[-30:]
        return zpravy

    def _vyhodnot_soupereni(self, den):
        """Spor či aliance se projeví pravidelně a jen v jednom městě."""
        if den % 3:
            return ""
        dvojice = FRAKCNI_RIVALOVE[(den // 3 - 1) % len(FRAKCNI_RIVALOVE)]
        vztah = self.vztahy_frakci[_klic_vztahu(*dvojice)]
        if vztah <= -25:
            mesto_id = self._mesto_pro_frakci(dvojice[0])
            mesto = self.mesta[mesto_id]
            mesto.uprav(bezpeci=-1, stabilita=-1)
            return (
                f"Napětí mezi {FRAKCNI_CILE[dvojice[0]][0]} a "
                f"{FRAKCNI_CILE[dvojice[1]][0]} vyvolalo spor ve městě "
                f"{mesto.nazev} (bezpečí −1, stabilita −1)."
            )
        if vztah >= 25:
            mesto_id = self._mesto_pro_frakci(dvojice[0])
            mesto = self.mesta[mesto_id]
            mesto.uprav(stabilita=1)
            return (
                f"Dohoda frakcí {FRAKCNI_CILE[dvojice[0]][0]} a "
                f"{FRAKCNI_CILE[dvojice[1]][0]} posílila stabilitu "
                f"ve městě {mesto.nazev}."
            )
        return ""

    def _mesto_pro_frakci(self, frakce_id):
        mesto_id = self.frakcni_cile.get(frakce_id, {}).get("mesto_id")
        return mesto_id if mesto_id in self.mesta else _prvni_mesto_frakce(frakce_id)

    def zmen_vztah_frakci(self, frakce_a, frakce_b, zmena):
        klic = _klic_vztahu(frakce_a, frakce_b)
        if klic not in self.vztahy_frakci:
            return False
        self.vztahy_frakci[klic] = max(
            -100, min(100, self.vztahy_frakci[klic] + _signed_cislo(zmena))
        )
        return True

    def _posun_karavany(self, hra, den):
        zpravy = []
        if den % 5 == 0 and len(self.karavany) < 3:
            cesta = list(TRASA_KARAVANY)
            if (den // 5) % 2 == 0:
                cesta.reverse()
            karavana = {
                "id": f"karavana-{den}",
                "cesta": cesta,
                "pozice": 0,
                "stav": "na_ceste",
                "odeslano": den,
                "doprovod": False,
            }
            self.karavany.append(karavana)
            zpravy.append(
                f"Karavana vyrazila z lokace {cesta[0].replace('_', ' ')} "
                f"směrem do {LOKACE[cesta[-1]]['nazev']}."
            )
        pokracujici = []
        for karavana in self.karavany:
            karavana["pozice"] = min(
                len(karavana["cesta"]) - 1,
                karavana["pozice"] + 1,
            )
            lokace_id = karavana["cesta"][karavana["pozice"]]
            mesto_id = _mesto_lokace(lokace_id)
            if hasattr(hra, "svet"):
                hra.svet.odhal_lokaci(lokace_id)
            if karavana["pozice"] < len(karavana["cesta"]) - 1:
                pokracujici.append(karavana)
                continue
            mesto = self.mesta[mesto_id]
            doprovod = karavana.get("doprovod", False) is True
            if (mesto.bezpeci >= 20 and mesto.stabilita >= 20) or doprovod:
                prijem = 12 + mesto.prosperita // 5 + (25 if doprovod else 0)
                hra.hrac.gold += prijem
                mesto.uprav(
                    prosperita=1,
                    stabilita=2 if doprovod else 1,
                    bezpeci=1 if doprovod else 0,
                )
                self._uprav_vliv_lokace(lokace_id, "obchodnici", 3)
                zpravy.append(
                    f"Karavana bezpečně dorazila do města {mesto.nazev}: "
                    f"+{prijem} zl., prosperita +1"
                    f"{', doprovod posílil bezpečí a stabilitu' if doprovod else ''}."
                )
            else:
                mesto.uprav(stabilita=-1)
                zpravy.append(
                    f"Karavana nedorazila bezpečně do města {mesto.nazev}; "
                    "obchodníci odklonili zásilku."
                )
        self.karavany = pokracujici
        return zpravy

    def zajisti_doprovod_karavany(self, hra):
        """Zaplatí doprovod pro jednu dosud nechráněnou karavanu."""
        if hra.npc_questy.dokoncene.get("sara_signalistka", 0) < 1:
            tisk_info("Nejdřív dokonči Sářin první úkol, aby ti svěřila karavany.")
            return False
        karavana = next(
            (
                polozka for polozka in self.karavany
                if polozka.get("stav") == "na_ceste"
                and polozka.get("doprovod") is not True
            ),
            None,
        )
        if karavana is None:
            tisk_info("Není tu žádná karavana, která by potřebovala doprovod.")
            return False
        cena = 25
        if hra.hrac.gold < cena:
            tisk_chyba("Na zajištění doprovodu potřebuješ 25 zlata.")
            return False
        hra.hrac.gold -= cena
        karavana["doprovod"] = True
        tisk_ok(
            f"Karavana {karavana.get('id', '')} dostala říční doprovod "
            "a při příjezdu přiveze bezpečnější zásilku."
        )
        return True

    def _vykonej_cil_fakce(self, frakce_id):
        """Nechá frakci vykonat malý, průběžný krok jejího městského cíle."""
        akce = FRAKCNI_AKCE.get(frakce_id)
        if not akce:
            return ""
        popis, metrika, dopady = akce
        mesta_vlivu = {
            _mesto_lokace(lokace_id)
            for lokace_id in FRAKCNI_ZONY.get(frakce_id, ())
            if lokace_id in LOKACE
        }
        kandidati = [
            mesto_id for mesto_id in MESTA
            if not mesta_vlivu or mesto_id in mesta_vlivu
        ]
        mesto_id = vyber_nejlepsi_uzitek(
            (klic, 100 - getattr(self.mesta[klic], metrika))
            for klic in kandidati
        )
        if not mesto_id:
            return ""
        mesto = self.mesta[mesto_id]
        mesto.uprav(**dopady)
        cil = self.frakcni_cile[frakce_id]
        cil["mesto_id"] = mesto_id
        cil["posledni_akce"] = popis
        dopad_trhu = self._aplikuj_dopad_frakce_na_trh(frakce_id, mesto_id)
        return (
            f"{mesto.nazev}: {cil['nazev']} — {popis}"
            f"{dopad_trhu}"
        )

    def _vyvin_cil_fakce(self, frakce_id):
        """Přizpůsobí další cíl frakce opakovaným výsledkům a místní krizi."""
        cil = self.frakcni_cile[frakce_id]
        cil["uroven"] = min(5, cil["uroven"] + 1)
        cil["evoluce"] += 1
        cil["cil"] = min(10, 3 + cil["uroven"] // 2)
        mesto = self.mesta[cil["mesto_id"]]
        metrika = min(
            ("bezpeci", "prosperita", "stabilita"),
            key=lambda polozka: getattr(mesto, polozka),
        )
        if getattr(mesto, metrika) <= 55:
            adaptivni_cile = {
                "bezpeci": (
                    "Zajistit bezpečné trasy",
                    "Frakce přesouvá své úsilí k hlídkám, doprovodu a pomoci v rizikových čtvrtích.",
                ),
                "prosperita": (
                    "Obnovit místní zásoby",
                    "Frakce upravuje svůj plán podle nedostatku zboží a potřeb městského trhu.",
                ),
                "stabilita": (
                    "Urovnat napětí ve městě",
                    "Frakce hledá spojence a mění své kroky podle sporů mezi místními skupinami.",
                ),
            }
            cil["nazev"], cil["popis"] = adaptivni_cile[metrika]
        else:
            cil["nazev"] = (
                f"{cil['nazev_zakladni']} — etapa {cil['uroven']}"
            )
            cil["popis"] = (
                f"{cil['popis_zakladni']} Další etapa rozšiřuje její síť "
                f"v oblasti města {mesto.nazev}."
            )
        return (
            f"Adaptivní AI: {FRAKCNI_CILE[frakce_id][0]} přizpůsobila "
            f"svůj plán místní situaci (etapa {cil['uroven']})."
        )

    def _aplikuj_dopad_frakce_na_trh(self, frakce_id, mesto_id):
        """Promítne každodenní práci frakce do lokálního trhu."""
        dopady = FRAKCNI_TRZNI_DOPADY.get(frakce_id, {})
        sklad = self.trziste_sklady.get(mesto_id)
        if not isinstance(sklad, dict):
            return ""
        zmeny = []
        for zbozi_id, zmena in dopady.items():
            if zbozi_id not in sklad:
                continue
            pred = sklad[zbozi_id]
            sklad[zbozi_id] = max(0, min(60, pred + zmena))
            skutecna_zmena = sklad[zbozi_id] - pred
            if skutecna_zmena:
                smer = "+" if skutecna_zmena > 0 else "−"
                zmeny.append(f"{smer}{abs(skutecna_zmena)} {zbozi_id}")
        if not zmeny:
            return ""
        return " Tržiště: " + ", ".join(zmeny) + "."

    def _rozsir_vliv_fakce(self, frakce_id, den):
        lokace = tuple(
            lokace_id for lokace_id in FRAKCNI_ZONY.get(frakce_id, ())
            if lokace_id in self.kontrola_lokaci
        )
        if not lokace:
            return ""
        index_fakce = tuple(FRAKCNI_CILE).index(frakce_id)
        lokace_id = lokace[(den + index_fakce) % len(lokace)]
        vliv = self.kontrola_lokaci[lokace_id]
        puvodni = self.frakce_lokace(lokace_id)
        vliv[frakce_id] = min(100, vliv.get(frakce_id, 0) + 2)
        if puvodni != frakce_id:
            vliv[puvodni] = max(0, vliv.get(puvodni, 0) - 1)
        novy = self.frakce_lokace(lokace_id)
        if novy != puvodni:
            return (
                f"{FRAKCNI_CILE[novy][0]} získala převahu v lokaci "
                f"{lokace_id.replace('_', ' ')}."
            )
        return ""

    def frakce_lokace(self, lokace_id):
        """Vrátí frakci s nejvyšším uloženým vlivem v lokaci."""
        vliv = self.kontrola_lokaci.get(lokace_id, {})
        return max(
            vliv,
            key=lambda frakce: (vliv[frakce], -tuple(FRAKCNI_CILE).index(frakce)),
            default=_vychozi_frakce_lokace(lokace_id),
        )

    def _uprav_vliv_lokace(self, lokace_id, frakce_id, zmena):
        if lokace_id not in self.kontrola_lokaci or frakce_id not in FRAKCNI_CILE:
            return
        vliv = self.kontrola_lokaci[lokace_id]
        vliv[frakce_id] = max(0, min(100, vliv.get(frakce_id, 0) + zmena))

    def _vytvor_udalost_mesta(self, den):
        typy = tuple(UDALOSTI_MESTA)
        mesta = tuple(MESTA)
        typ = typy[(den // 4 - 1) % len(typy)]
        mesto_id = mesta[(den // 4 - 1) % len(mesta)]
        nejhorsi_mesto = min(
            self.mesta,
            key=lambda ident: min(
                getattr(self.mesta[ident], metrika)
                for metrika in ("prosperita", "bezpeci", "stabilita")
            ),
        )
        nejhorsi = self.mesta[nejhorsi_mesto]
        metrika = min(
            ("prosperita", "bezpeci", "stabilita"),
            key=lambda atribut: getattr(nejhorsi, atribut),
        )
        if getattr(nejhorsi, metrika) <= 30:
            mesto_id = nejhorsi_mesto
            if metrika == "bezpeci":
                typ = "hlidky"
            elif metrika == "stabilita":
                return self._vytvor_frakcni_iniciativu(den, mesto_id)
            else:
                sklad = self.trziste_sklady.get(mesto_id, {})
                typ = (
                    "trzni_nepokoj"
                    if any(sklad.get(zbozi, 0) <= 5 for zbozi in (
                        "zasoby", "drevo", "kamen",
                    ))
                    else "karavana"
                )
        definice = UDALOSTI_MESTA[typ]
        return {
            "id": f"{mesto_id}-{typ}-{den}",
            "den": den,
            "mesto_id": mesto_id,
            "typ": typ,
            "nazev": definice["nazev"],
            "text": definice["text"],
            "lokace_id": _lokace_udalosti(typ, mesto_id),
        }

    def _vytvor_frakcni_iniciativu(self, den, mesto_id=None):
        if mesto_id not in self.mesta:
            mesto_id = min(
                self.mesta,
                key=lambda ident: sum(
                    getattr(self.mesta[ident], metrika)
                    for metrika in ("prosperita", "bezpeci", "stabilita")
                ),
            )
        mesto = self.mesta[mesto_id]
        metrika = min(
            ("prosperita", "bezpeci", "stabilita"),
            key=lambda atribut: getattr(mesto, atribut),
        )
        frakce_v_meste = [
            frakce_id for frakce_id, cil in self.frakcni_cile.items()
            if cil.get("mesto_id") == mesto_id
        ]
        if not frakce_v_meste:
            frakce_v_meste = list(FRAKCNI_CILE)
        frakce_id = random.choice(frakce_v_meste)
        zastupci = [
            postava for postava in self.postavy
            if postava.get("frakce") == frakce_id
        ]
        npc = (
            random.choice(zastupci)
            if zastupci
            else random.choice(self.postavy)
            if self.postavy
            else {"id": "", "jmeno": "Místní obyvatelé", "role": "rada"}
        )
        profil = FRAKCNI_PROFILY.get(frakce_id, {})
        starost = profil.get("starost", "Místní obyvatelé žádají o pomoc.")
        akce = npc.get("posledni_akce", "")
        akce_text = f" Její poslední krok: {akce}" if akce else ""
        nazev = f"Iniciativa: {FRAKCNI_CILE[frakce_id][0]}"
        return {
            "id": f"{mesto_id}-iniciativa-{frakce_id}-{den}",
            "den": den,
            "mesto_id": mesto_id,
            "typ": "frakcni_iniciativa",
            "frakce_id": frakce_id,
            "npc_id": npc.get("id", ""),
            "metrika": metrika,
            "nazev": nazev,
            "text": (
                f"{npc['jmeno']} ({npc['role']}) žádá o pomoc. "
                f"{starost}{akce_text}"
            ),
            "lokace_id": (
                npc["lokace"]
                if _mesto_lokace(npc.get("lokace", "")) == mesto_id
                else _lokace_udalosti("frakcni_iniciativa", mesto_id)
            ),
        }

    def _vyres_expirovane_udalosti(self, den, zpravy):
        cekajici = []
        for udalost in self.udalosti_mesta:
            if den < udalost.get("k_dispozici_od", udalost["den"]):
                cekajici.append(udalost)
                continue
            if den - udalost["den"] < 4:
                cekajici.append(udalost)
                continue
            mesto = self.mesta[udalost["mesto_id"]]
            mesto.uprav(**UDALOSTI_MESTA[udalost["typ"]]["zanik"])
            zpravy.append(
                f"Neřešená situace «{udalost['nazev']}» ve městě "
                f"{mesto.nazev} skončila zhoršením místních poměrů."
            )
            self.historie.append({
                "den": den,
                "text": f"{mesto.nazev}: nevyřešeno — {udalost['nazev']}.",
            })
        self.udalosti_mesta = cekajici[-3:]

    def _aktivuj_nasledne_udalosti(self, den, zpravy):
        cekajici = []
        for udalost in sorted(self.navazujici_udalosti, key=lambda polozka: polozka["den"]):
            if udalost["den"] > den or len(self.udalosti_mesta) >= 3:
                cekajici.append(udalost)
                continue
            definice = UDALOSTI_MESTA[udalost["typ"]]
            lokace_id = _lokace_udalosti(udalost["typ"], udalost["mesto_id"])
            self.udalosti_mesta.append({
                "id": f"{udalost['mesto_id']}-{udalost['typ']}-{den}",
                "den": den,
                "k_dispozici_od": den,
                "mesto_id": udalost["mesto_id"],
                "typ": udalost["typ"],
                "nazev": definice["nazev"],
                "text": definice["text"],
                "lokace_id": lokace_id,
                "retizec": udalost.get("retizec", ""),
            })
            zpravy.append(
                f"Pokračuje městská linka: {definice['nazev']} "
                f"ve městě {self.mesta[udalost['mesto_id']].nazev}."
            )
        self.navazujici_udalosti = cekajici[-5:]

    def _prijem_karavan(self):
        prijem = 0
        for mesto in self.mesta.values():
            if mesto.bezpeci < 20 or mesto.stabilita < 20:
                continue
            prijem += min(
                8,
                (mesto.prosperita + mesto.bezpeci + mesto.stabilita) // 60,
            )
        return prijem

    def _vyres_udalost_mesta(self, hra, udalost):
        definice = UDALOSTI_MESTA[udalost["typ"]]
        mesto = self.mesta[udalost["mesto_id"]]
        volby = definice["volby"]
        zanik = definice["zanik"]
        frakce_id = udalost.get("frakce_id", definice["frakce"])
        if udalost["typ"] == "frakcni_iniciativa":
            metrika = udalost["metrika"]
            dopad_podpora = {metrika: 4, "stabilita": 2}
            dopad_dohoda = {metrika: 2, "stabilita": 1}
            if metrika == "stabilita":
                dopad_podpora["stabilita"] = 6
                dopad_dohoda["stabilita"] = 3
            volby = (
                (
                    "Podpořit iniciativu (25 zl.)",
                    25,
                    dopad_podpora,
                    5,
                ),
                (
                    "Domluvit dobrovolné řešení",
                    0,
                    dopad_dohoda,
                    2,
                ),
            )
            zanik = {metrika: -2}
            zanik["stabilita"] = zanik.get("stabilita", 0) - 1
        print(f"\n{mesto.nazev}: {udalost['nazev']}\n{udalost['text']}")
        for index, (text, cena, _, _) in enumerate(volby, 1):
            oznaceni = " — nedostatek zlata" if hra.hrac.gold < cena else ""
            vytiskni_volbu(str(index), text + oznaceni)
        vytiskni_volbu("0", "Nechat situaci bez zásahu")
        try:
            volba = input("> ").strip()
        except EOFError:
            return False
        if volba == "0":
            mesto.uprav(**zanik)
            if udalost["typ"] == "frakcni_iniciativa":
                frakce = hra.frakce.frakce.get(frakce_id)
                if frakce:
                    frakce.zmenit(-2)
                self._uprav_vztah_npc(udalost.get("npc_id"), -1)
            tisk_info("Situaci ponecháváš bez zásahu; městské poměry se zhorší.")
            self._zapis_udalost(udalost, "bez zásahu")
            self._naplanuj_pokracovani(udalost, uspesne=False)
            return True
        try:
            index = int(volba) - 1
            text, cena, dopady, vliv = volby[index]
        except (ValueError, IndexError):
            tisk_chyba("Zadej číslo dostupné možnosti.")
            return False
        if hra.hrac.gold < cena:
            tisk_chyba("Na tuto možnost nemáš dost zlata.")
            return False
        hra.hrac.gold -= cena
        mesto.uprav(**dopady)
        frakce = hra.frakce.frakce.get(frakce_id)
        if frakce:
            frakce.zmenit(vliv)
        self._uprav_vliv_lokace(
            udalost["lokace_id"], frakce_id, vliv
        )
        if udalost["typ"] == "frakcni_iniciativa":
            self._uprav_vztah_npc(udalost.get("npc_id"), 4)
        tisk_ok(f"Rozhodl ses: {text}.")
        self._zapis_udalost(udalost, text)
        self._naplanuj_pokracovani(udalost, uspesne=True)
        return True

    def _uprav_vztah_npc(self, npc_id, zmena):
        if not isinstance(npc_id, str):
            return
        npc = next(
            (postava for postava in self.postavy if postava.get("id") == npc_id),
            None,
        )
        if npc:
            vztah = _signed_cislo(npc.get("vztah_hraci", 0))
            npc["vztah_hraci"] = max(-100, min(100, vztah + zmena))

    def _naplanuj_pokracovani(self, udalost, uspesne):
        if udalost.get("retizec") or len(self.navazujici_udalosti) >= 5:
            return
        dalsi_typ = {
            ("karavana", True): "trzni_oziveni",
            ("most", True): "trzni_oziveni",
            ("hlidky", True): "bezpecna_ctvrt",
            ("karavana", False): "trzni_nepokoj",
        }.get((udalost["typ"], uspesne))
        if not dalsi_typ:
            return
        self.navazujici_udalosti.append({
            "den": udalost["den"] + 2,
            "mesto_id": udalost["mesto_id"],
            "typ": dalsi_typ,
            "retizec": udalost.get("id", udalost["typ"]),
        })

    def _zapis_udalost(self, udalost, rozhodnuti):
        mesto = self.mesta[udalost["mesto_id"]]
        self.historie.append({
            "den": udalost["den"],
            "text": f"{mesto.nazev}: {rozhodnuti} — {udalost['nazev']}.",
        })
        self.historie = self.historie[-30:]

    def _rozhodni_pohyb_npc(self, postava):
        """NPC volí trasu k městu, kde jeho specializace nejvíc pomůže."""
        aktualni = postava.get("lokace", "trh")
        if aktualni not in LOKACE:
            aktualni = "trh"
        profil = PROFILY_AI_NPC.get(postava.get("id"))
        sousedi = LOKACE[aktualni]["sousedni"]
        if not sousedi:
            return aktualni
        if not profil:
            return sousedi[0]

        metrika = profil["metrika"]
        smer = profil["smer"]
        mesto_cil = vyber_nejlepsi_uzitek(
            (
                mesto_id,
                (
                    100 - getattr(mesto, metrika)
                    if smer == "minimum"
                    else getattr(mesto, metrika)
                ),
            )
            for mesto_id, mesto in self.mesta.items()
        )
        lokace_cile = MESTA[mesto_cil]["lokace"]
        vzdalenosti = vzdalenosti_od_cilu(
            {lokace_id: data["sousedni"] for lokace_id, data in LOKACE.items()},
            lokace_cile,
        )
        kandidati = [lokace for lokace in sousedi if lokace in vzdalenosti]
        if aktualni in lokace_cile:
            kandidati = [
                lokace for lokace in kandidati
                if lokace in lokace_cile
            ] or kandidati
        vybrany = vyber_nejlepsi_uzitek(
            (lokace, -vzdalenosti[lokace]) for lokace in kandidati
        )
        return vybrany or aktualni

    def _vytvor_nabidku(self, frakce_id, den):
        definice = self.frakcni_cile[frakce_id]
        frakce_nazev = FRAKCNI_CILE[frakce_id][0]
        postava = next(
            (p for p in self.postavy if p.get("frakce") == frakce_id),
            self.postavy[den % len(self.postavy)],
        )
        return {
            "id": f"{frakce_id}-{den}",
            "den": den,
            "frakce_id": frakce_id,
            "frakce_nazev": frakce_nazev,
            "cilek": definice["nazev"],
            "text": definice["popis"],
            "postava": postava["jmeno"],
            "mesto_id": _mesto_lokace(postava.get("lokace", "trh")),
            "lokace_id": postava.get("lokace", "trh"),
        }

    def _doplnit_trziste(self):
        for mesto_id, sklad in self.trziste_sklady.items():
            prosperita = self.mesta[mesto_id].prosperita
            doplneni = 2 if prosperita >= 60 else 1
            for zbozi_id in sklad:
                sklad[zbozi_id] = min(60, sklad[zbozi_id] + doplneni)

    def _cena_na_trzisti(self, mesto_id, zbozi_id):
        zbozi = TRZNI_ZBOZI[zbozi_id]
        sklad = self.trziste_sklady[mesto_id][zbozi_id]
        mesto = self.mesta[mesto_id]
        nedostatek = max(0.65, min(1.8, 1.45 - sklad / 60))
        stav_mesta = 0.75 + (mesto.prosperita + mesto.stabilita) / 400
        nakup = max(1, int(zbozi["cena"] * nedostatek * stav_mesta + 0.5))
        prodej = max(1, int(nakup * 0.55))
        return nakup, prodej

    def _menu_trziste(self, hra):
        lokace = getattr(getattr(hra, "svet", None), "aktualni_lokace", "trh")
        mesto_id = _mesto_lokace(lokace)
        mesto = self.mesta[mesto_id]
        sklad = self.trziste_sklady[mesto_id]
        dodavatel_id = self.frakce_lokace(lokace)
        profil_dodavatele = FRAKCNI_PROFILY.get(dodavatel_id)
        dodavatel = hra.frakce.frakce.get(dodavatel_id)
        print(
            f"\n=== TRŽIŠTĚ: {mesto.nazev} ===\n"
            f"Prosperita {mesto.prosperita} | stabilita {mesto.stabilita} | "
            f"tvoje zlato {hra.hrac.gold}"
        )
        if profil_dodavatele:
            nazev_dodavatele = dodavatel.nazev if dodavatel else dodavatel_id
            print(
                f"Dodavatel: {nazev_dodavatele} — "
                f"{', '.join(profil_dodavatele['zbozi'])}"
            )
        dostupne = tuple(sklad)
        for index, zbozi_id in enumerate(dostupne, 1):
            info = TRZNI_ZBOZI[zbozi_id]
            nakup, prodej = self._cena_na_trzisti(mesto_id, zbozi_id)
            print(
                f"  {index}) {info['nazev']}: {sklad[zbozi_id]} {info['jednotka']} "
                f"| nákup {nakup} zl. | prodej {prodej} zl."
            )
        print("  0) Zpět")
        try:
            volba = input("Zboží: ").strip()
            if volba == "0":
                return
            index = int(volba) - 1
            if not 0 <= index < len(dostupne):
                raise ValueError
            zbozi_id = dostupne[index]
            smer = input("Koupit (k) / prodat (p): ").strip().lower()
            if smer not in ("k", "koupit", "p", "prodat"):
                tisk_chyba("Zvol k pro nákup nebo p prodej.")
                return
            mnozstvi = int(input("Množství (1–20): ").strip())
        except EOFError:
            return
        except ValueError:
            tisk_chyba("Neplatný výběr nebo množství.")
            return
        if not 1 <= mnozstvi <= 20:
            tisk_chyba("V jednom obchodu lze převést 1 až 20 jednotek.")
            return

        nakup, prodej = self._cena_na_trzisti(mesto_id, zbozi_id)
        sklad = self.trziste_sklady[mesto_id]
        if smer in ("k", "koupit"):
            cena = nakup * mnozstvi
            if sklad[zbozi_id] < mnozstvi:
                tisk_chyba("Místní sklad nemá požadované množství.")
                return
            if hra.hrac.gold < cena:
                tisk_chyba(f"Na nákup potřebuješ {cena} zlata.")
                return
            hra.hrac.gold -= cena
            setattr(hra.pevnost, zbozi_id, getattr(hra.pevnost, zbozi_id) + mnozstvi)
            sklad[zbozi_id] -= mnozstvi
            tisk_ok(f"Koupeno {mnozstvi} {TRZNI_ZBOZI[zbozi_id]['jednotka']} za {cena} zlata.")
        else:
            dostupne_mnozstvi = getattr(hra.pevnost, zbozi_id)
            cena = prodej * mnozstvi
            if dostupne_mnozstvi < mnozstvi:
                tisk_chyba("Panství nemá tolik zboží na prodej.")
                return
            if sklad[zbozi_id] + mnozstvi > 60:
                tisk_chyba("Místní sklad nemá prostor pro tak velkou dodávku.")
                return
            setattr(hra.pevnost, zbozi_id, dostupne_mnozstvi - mnozstvi)
            hra.hrac.gold += cena
            sklad[zbozi_id] += mnozstvi
            tisk_ok(f"Prodáno {mnozstvi} {TRZNI_ZBOZI[zbozi_id]['jednotka']} za {cena} zlata.")

    def _prehled_frakci_a_mest(self, hra):
        print("\n=== FRAKCE, MĚSTSKÉ STAROSTI A ZBOŽÍ ===")
        for mesto_id, mesto in self.mesta.items():
            metrika = min(
                ("prosperita", "bezpeci", "stabilita"),
                key=lambda klic: getattr(mesto, klic),
            )
            print(
                f"\n{mesto.nazev} — {MESTSKE_STAROSTI[mesto_id][metrika]} "
                f"({metrika}: {getattr(mesto, metrika)})"
            )
        for frakce_id, profil in FRAKCNI_PROFILY.items():
            frakce = hra.frakce.frakce.get(frakce_id)
            nazev = frakce.nazev if frakce else FRAKCNI_CILE[frakce_id][0]
            mesto = self.mesta[self.frakcni_cile[frakce_id]["mesto_id"]]
            postava = next(
                (p for p in self.postavy if p.get("frakce") == frakce_id),
                None,
            )
            kapitola = postava.get("pribeh", 0) if postava else 0
            dalsi_pribeh = (
                profil["kapitoly"][kapitola][0]
                if kapitola < len(profil["kapitoly"])
                else "příběhová linka uzavřena"
            )
            reputace = frakce.reputace if frakce else 0
            print(
                f"\n• {nazev} | {mesto.nazev} | reputace {reputace:+d}\n"
                f"  Starost: {profil['starost']}\n"
                f"  Nabídka: {', '.join(profil['zbozi'])}\n"
                f"  Příběh: {dalsi_pribeh}"
            )

    def menu(self, hra):
        while True:
            print("\n=== ŽIVÝ SVĚT ===")
            print("Denní cíle frakcí:")
            for frakce_id, cil in self.frakcni_cile.items():
                frakce = hra.frakce.frakce.get(frakce_id)
                jmeno = frakce.nazev if frakce else frakce_id
                mesto = self.mesta[cil["mesto_id"]].nazev
                akce = f" — {cil['posledni_akce']}" if cil["posledni_akce"] else ""
                print(
                    f"  {jmeno}: {cil['nazev']} [{cil['postup']}/{cil['cil']}] "
                    f"→ {mesto}{akce}"
                )
            print("\nPostavy ve městě:")
            for postava in self.postavy:
                print(
                    f"  {postava['jmeno']} — {postava['role']}, "
                    f"{postava['lokace'].replace('_', ' ')}"
                )
            print("\nStav měst:")
            for mesto_id, mesto in self.mesta.items():
                print(
                    f"  {mesto.nazev}: prosperita {mesto.prosperita}, "
                    f"bezpečí {mesto.bezpeci}, stabilita {mesto.stabilita}"
                )
            if self.nabidky:
                nabidka = self.nabidky[0]
                print(
                    f"\nSituace: {nabidka['frakce_nazev']} — {nabidka['cilek']}\n"
                    f"{nabidka['text']} {nabidka['postava']} přináší zprávu."
                )
                if not self._vyres_nabidku(hra, nabidka):
                    return
                self.nabidky.pop(0)
                if self.nabidky:
                    try:
                        dalsi = input("Vyřešit také další situaci? (a/n): ").strip().lower()
                    except EOFError:
                        return
                    if dalsi not in ("a", "ano"):
                        return
                continue
            if self.udalosti_mesta:
                index = next(
                    (
                        index for index, udalost in enumerate(self.udalosti_mesta)
                        if udalost.get("k_dispozici_od", udalost["den"]) <= hra.hrac.den
                    ),
                    None,
                )
                if index is None:
                    self._menu_nabidky_svet(hra)
                    return
                udalost = self.udalosti_mesta[index]
                if not self._vyres_udalost_mesta(hra, udalost):
                    return
                self.udalosti_mesta.pop(index)
                continue
            if self.historie:
                print("\nPoslední dění:")
                for zaznam in self.historie[-5:]:
                    print(f"  Den {zaznam['den']}: {zaznam['text']}")
            vytiskni_volbu("1", "Přehled změn, karavan a vztahů frakcí")
            vytiskni_volbu("2", "Dlouhodobé příběhy NPC")
            vytiskni_volbu("3", "Vyjednávat mezi frakcemi")
            vytiskni_volbu("4", "Místní tržiště — koupit nebo prodat suroviny")
            vytiskni_volbu("5", "Kronika frakcí, jejich starosti a zboží")
            pobliz = self._postavy_v_lokaci(hra)
            vytiskni_volbu(
                "6",
                f"Setkat se s NPC v této lokaci ({len(pobliz)})",
            )
            vytiskni_volbu("7", "Uspořádat městskou slavnost")
            vytiskni_volbu("0", "Zpět")
            try:
                volba = input("> ").strip()
                if volba == "0":
                    return
                if volba == "1":
                    self._menu_nabidky_svet(hra)
                elif volba == "2":
                    self._menu_pribehu_npc(hra)
                elif volba == "3":
                    self._menu_diplomacie_frakci(hra)
                elif volba == "4":
                    self._menu_trziste(hra)
                elif volba == "5":
                    self._prehled_frakci_a_mest(hra)
                    input("Enter pro návrat...")
                elif volba == "6":
                    self._menu_setkani_npc(hra)
                elif volba == "7":
                    self._menu_slavnosti(hra)
            except EOFError:
                return

    def _dostupne_slavnosti(self, hra):
        den = max(1, int(hra.hrac.den))
        nabidky = []
        for mesto_id, mesto in self.mesta.items():
            posledni_den = self.posledni_slavnosti.get(mesto_id, 0)
            if posledni_den and den - posledni_den < 7:
                continue
            if mesto.prosperita >= 55:
                nabidky.append((mesto_id, "trh"))
            if mesto.stabilita >= 50:
                nabidky.append((mesto_id, "slavnost"))
        return nabidky

    def _menu_slavnosti(self, hra):
        print("\n=== MĚSTSKÉ SLAVNOSTI ===")
        nabidky = self._dostupne_slavnosti(hra)
        if not nabidky:
            tisk_info(
                "Žádné město zatím nesplňuje podmínky nebo ještě trvá "
                "sedmidenní odpočinek po poslední slavnosti."
            )
            return

        print("Vyber město a událost:")
        for index, (mesto_id, typ) in enumerate(nabidky, 1):
            mesto = self.mesta[mesto_id]
            nazev = "Kupecký trh" if typ == "trh" else "Městský festival"
            podminka = (
                f"prosperita {mesto.prosperita}"
                if typ == "trh" else f"stabilita {mesto.stabilita}"
            )
            print(f"  {index}) {mesto.nazev} — {nazev} ({podminka})")
        vytiskni_volbu("0", "Zpět")
        try:
            volba = input("> ").strip()
            if volba == "0":
                return
            index = int(volba) - 1
            if not 0 <= index < len(nabidky):
                raise ValueError
        except (EOFError, ValueError):
            tisk_chyba("Neplatná slavnost.")
            return

        mesto_id, typ = nabidky[index]
        mesto = self.mesta[mesto_id]
        print("Rozpočet: 1) Skromný (30 zl.)  2) Velkolepý (70 zl.)")
        print("Zajištění: 1) Dobrovolníci (zdarma)  2) Městská hlídka (25 zl.)")
        try:
            rozpocet_volba = input("Rozpočet: ").strip()
            zajisteni_volba = input("Zajištění: ").strip()
        except EOFError:
            return
        if rozpocet_volba not in ("1", "2") or zajisteni_volba not in ("1", "2"):
            tisk_chyba("Neplatná volba rozpočtu nebo zajištění.")
            return

        velkolepa = rozpocet_volba == "2"
        hlidka = zajisteni_volba == "2"
        naklady = (70 if velkolepa else 30) + (25 if hlidka else 0)
        if hra.hrac.gold < naklady:
            tisk_chyba(f"Na tuto slavnost potřebuješ {naklady} zlata.")
            return
        hra.hrac.gold -= naklady

        if typ == "trh":
            vydelek = 100 if velkolepa else 60
            mesto.uprav(prosperita=5 if velkolepa else 3)
            sklad = self.trziste_sklady[mesto_id]
            sklad["zasoby"] = min(
                60, sklad["zasoby"] + (5 if velkolepa else 2)
            )
            frakce_id = "obchodnici"
            typ_nazev = "kupecký trh"
        else:
            vydelek = 65 if velkolepa else 35
            mesto.uprav(stabilita=6 if velkolepa else 4)
            frakce_id = (
                "cech_kurtizan" if mesto_id == "stare_mesto" else "policie"
            )
            typ_nazev = "městský festival"

        mesto.uprav(bezpeci=3 if hlidka else 0)
        incident = not hlidka and mesto.bezpeci < 30
        if incident:
            vydelek = max(0, vydelek - 25)
            mesto.uprav(stabilita=-2)
            tisk_info("Slabé hlídky způsobily během slavnosti menší nepokoj.")

        hra.hrac.gold += vydelek
        frakce = hra.frakce.frakce.get(frakce_id)
        if frakce:
            frakce.zmenit(6 if velkolepa else 3)
        mesto_id_postav = [
            postava for postava in self.postavy
            if _mesto_lokace(postava.get("lokace", "")) == mesto_id
        ]
        if mesto_id_postav:
            vztah = 5 if velkolepa else 3
            for postava in mesto_id_postav:
                postava["vztah_hraci"] = min(
                    100, postava.get("vztah_hraci", 0) + vztah
                )
                hra.svet.zmen_vztah(postava.get("id"), vztah)

        den = max(1, int(hra.hrac.den))
        self.posledni_slavnosti[mesto_id] = den
        typ_pokracovani = (
            "trzni_oziveni" if typ == "trh" else "bezpecna_ctvrt"
        )
        naplanovano = len(self.navazujici_udalosti) < 5
        if naplanovano:
            self.navazujici_udalosti.append({
                "den": den + 2,
                "mesto_id": mesto_id,
                "typ": typ_pokracovani,
                "retizec": f"slavnost-{mesto_id}-{den}",
            })
        zaznam = {
            "den": den,
            "text": (
                f"{mesto.nazev}: uspořádán {typ_nazev}; "
                f"příjem +{vydelek} zl."
            ),
        }
        self.historie.append(zaznam)
        self.historie = self.historie[-30:]
        from game.kronika import zaznamenej
        zaznamenej(hra, f"Živý svět: {zaznam['text']}")
        tisk_ok(
            f"{typ_nazev.capitalize()} v {mesto.nazev} přilákal návštěvníky: "
            f"+{vydelek} zl., přízeň frakce +{6 if velkolepa else 3}."
        )
        if naplanovano:
            tisk_info(
                "Za dva dny naváže další událost: "
                + UDALOSTI_MESTA[typ_pokracovani]["nazev"]
                + "."
            )

    def _postavy_v_lokaci(self, hra):
        lokace = getattr(getattr(hra, "svet", None), "aktualni_lokace", "")
        return [
            postava for postava in self.postavy
            if postava.get("lokace") == lokace
        ]

    def _menu_setkani_npc(self, hra):
        """Nabídne zprávu nebo jednorázovou denní pomoc přítomnému NPC."""
        postavy = self._postavy_v_lokaci(hra)
        if not postavy:
            tisk_info("V této lokaci teď není žádná známá postava.")
            return
        print("\n=== SETKÁNÍ V LOKACI ===")
        for index, postava in enumerate(postavy, 1):
            print(
                f"  {index}) {postava['jmeno']} — {postava['role']} "
                f"(vztah {postava['vztah_hraci']:+d})"
            )
        try:
            vyber = input("Postava (0 zpět): ").strip()
            if vyber == "0":
                return
            index = int(vyber) - 1
            if not 0 <= index < len(postavy):
                raise ValueError
        except (EOFError, ValueError):
            tisk_chyba("Neplatný výběr postavy.")
            return

        postava = postavy[index]
        frakce_id = postava.get("frakce")
        profil = FRAKCNI_PROFILY.get(frakce_id, {})
        mesto = self.mesta[_mesto_lokace(postava.get("lokace", ""))]
        posledni_akce = postava.get("posledni_akce")
        if not posledni_akce:
            posledni_akce = (
                postava["akce"][0]
                if isinstance(postava.get("akce"), (tuple, list))
                and postava["akce"]
                else str(postava.get("akce", "Prochází městem."))
            )
        print(
            f"\n{postava['jmeno']}: „{posledni_akce}“\n"
            f"Starost frakce: {profil.get('starost', 'Místní dění se mění.')}\n"
            f"{mesto.nazev}: prosperita {mesto.prosperita}, "
            f"bezpečí {mesto.bezpeci}, stabilita {mesto.stabilita}."
        )
        pomoc = NPC_POMOC.get(postava.get("id"), {
            "zadost": "potřebuje pomoc s místním úkolem",
            "cena": 10,
            "mesto": {"stabilita": 1},
        })
        print(f"Prosba: {pomoc['zadost']}.")
        vytiskni_volbu("1", "Poděkovat za zprávu a rozloučit se")
        vytiskni_volbu(
            "2",
            f"Pomoci ( {pomoc['cena']} zl., 1× denně)",
        )
        vytiskni_volbu("0", "Ukončit setkání")
        try:
            volba = input("> ").strip()
        except EOFError:
            return
        if volba == "0":
            return
        if volba == "1":
            tisk_info("Získal jsi aktuální zprávu z této čtvrti.")
            return
        if volba != "2":
            tisk_chyba("Neplatná volba.")
            return

        den = max(1, int(hra.hrac.den))
        if postava["posledni_pomoc_den"] == den:
            tisk_info("Dnes už jsi této postavě pomohl.")
            return
        cena = pomoc["cena"]
        if hra.hrac.gold < cena:
            tisk_chyba(f"Na pomoc potřebuješ {cena} zlata.")
            return
        hra.hrac.gold -= cena
        postava["posledni_pomoc_den"] = den
        self._uprav_vztah_npc(postava.get("id"), 4)
        mesto.uprav(**pomoc["mesto"])
        zmeny_mesta = ", ".join(
            f"{atribut} {hodnota:+d}"
            for atribut, hodnota in pomoc["mesto"].items()
        )
        for zbozi_id, mnozstvi in pomoc.get("trziste", {}).items():
            sklad = self.trziste_sklady.get(mesto.ident, {})
            if zbozi_id in sklad:
                sklad[zbozi_id] = max(0, min(60, sklad[zbozi_id] + mnozstvi))
        if pomoc.get("vyzkum"):
            hra.vyzkum.pridej_body(pomoc["vyzkum"])
        if pomoc.get("inkvizice"):
            hra.hrac.vliv_inkvizice = max(
                0,
                min(100, hra.hrac.vliv_inkvizice + pomoc["inkvizice"]),
            )
        frakce = hra.frakce.frakce.get(frakce_id)
        if frakce:
            frakce.zmenit(2)
        zaznam = {
            "den": den,
            "text": (
                f"{postava['jmeno']}: místní pomoc v lokaci "
                f"{postava['lokace'].replace('_', ' ')}."
            ),
        }
        self.historie.append(zaznam)
        self.historie = self.historie[-30:]
        from game.kronika import zaznamenej
        zaznamenej(hra, f"Živý svět: {zaznam['text']}")
        odmeny = [f"vztah +4", f"přízeň frakce +2", zmeny_mesta]
        if pomoc.get("vyzkum"):
            odmeny.append(f"výzkum +{pomoc['vyzkum']}")
        if pomoc.get("inkvizice"):
            odmeny.append(f"vliv inkvizice {pomoc['inkvizice']:+d}")
        if pomoc.get("trziste"):
            odmeny.append("doplnění místního trhu")
        tisk_ok(f"Pomohl jsi {postava['jmeno']}; " + ", ".join(odmeny) + ".")

    def _menu_nabidky_svet(self, hra):
        print("\n=== PŘEHLED ZMĚN SVĚTA ===")
        for mesto in self.mesta.values():
            print(
                f"  {mesto.nazev}: prosperita {mesto.prosperita}, "
                f"bezpečí {mesto.bezpeci}, stabilita {mesto.stabilita}"
            )
        print("\nVztahy frakcí:")
        for dvojice in FRAKCNI_RIVALOVE:
            hodnota = self.vztahy_frakci[_klic_vztahu(*dvojice)]
            stav = "spojenectví" if hodnota >= 25 else "napětí" if hodnota <= -25 else "křehké příměří"
            print(
                f"  {FRAKCNI_CILE[dvojice[0]][0]} ↔ "
                f"{FRAKCNI_CILE[dvojice[1]][0]}: {stav} ({hodnota:+d})"
            )
        print("\nKaravany:")
        if self.karavany:
            for karavana in self.karavany:
                cesta = karavana["cesta"]
                poloha = cesta[karavana["pozice"]]
                cil = cesta[-1]
                print(
                    f"  {karavana['id']}: {LOKACE[poloha]['nazev']} → "
                    f"{LOKACE[cil]['nazev']} "
                    f"({karavana['pozice'] + 1}/{len(cesta)})"
                )
        else:
            print("  Žádná karavana právě není na cestě.")
        print("\nNadcházející události:")
        for udalost in self.navazujici_udalosti:
            print(
                f"  Den {udalost['den']}: {udalost['typ'].replace('_', ' ')} — "
                f"{self.mesta[udalost['mesto_id']].nazev}"
            )
        print("\nPoslední změny:")
        for zaznam in self.historie[-10:]:
            print(f"  Den {zaznam['den']}: {zaznam['text']}")
        try:
            input("\nEnter pro návrat...")
        except EOFError:
            return

    def _menu_pribehu_npc(self, hra):
        print("\n=== PŘÍBĚHY POSTAV ===")
        for index, postava in enumerate(self.postavy, 1):
            print(
                f"  {index}) {postava['jmeno']} — "
                f"{postava['role']}, příběh {postava['pribeh']}/3, "
                f"vztah {postava['vztah_hraci']:+d}"
            )
        try:
            volba = input("Postava (0 zpět): ").strip()
            if volba == "0":
                return
            index = int(volba) - 1
            if not 0 <= index < len(self.postavy):
                raise IndexError
            postava = self.postavy[index]
        except (EOFError, ValueError, IndexError):
            tisk_chyba("Neplatný výběr postavy.")
            return
        mesto_id = _mesto_lokace(postava["lokace"])
        mesto = self.mesta[mesto_id]
        kapitoly = (
            "Sdílí, co ji přivedlo do města, a poslouchá tvé otázky.",
            "Ukazuje, jak její práce mění životy místních obyvatel.",
            "Rozhoduje se, jakou budoucnost chce pro sebe i své město.",
        )
        pribehy_sary = (
            (
                "Světlo, které nikdo neviděl",
                "Sára vypráví o karavaně, která minula přístav, protože staré signální lampy zhasly.",
            ),
            (
                "Mapa na obou březích",
                "Kupci a hlídky používají různé značky. Sára hledá způsob, jak je přimět sdílet jednu mapu.",
            ),
            (
                "Bezpečná cesta domů",
                "Sára chce, aby se přístav stal místem, kam se karavany vracejí bez strachu i bez výpalného.",
            ),
        )
        if postava["pribeh"] >= 3:
            print(
                f"{postava['jmeno']} už uzavřela svůj příběh. "
                f"Vztah s tebou: {postava['vztah_hraci']:+d}."
            )
            try:
                input("Enter pro návrat...")
            except EOFError:
                pass
            return
        kapitola = postava["pribeh"]
        profil = FRAKCNI_PROFILY.get(postava.get("frakce"))
        if postava.get("id") == "sara_signalistka":
            pribehova_kapitola = pribehy_sary[kapitola]
        else:
            pribehova_kapitola = (
                profil["kapitoly"][kapitola]
                if profil and kapitola < len(profil["kapitoly"])
                else (f"Kapitola {kapitola + 1}", kapitoly[kapitola])
            )
        starosti_mesta = MESTSKE_STAROSTI[mesto_id]
        nejpalcivejsi = min(
            ("prosperita", "bezpeci", "stabilita"),
            key=lambda klic: getattr(mesto, klic),
        )
        print(
            f"\n{postava['jmeno']} — {pribehova_kapitola[0]}\n"
            f"{pribehova_kapitola[1]}\n"
            f"Městská starost: {starosti_mesta[nejpalcivejsi]}\n"
            f"Vztah {postava['vztah_hraci']:+d} | město {mesto.nazev}: "
            f"stabilita {mesto.stabilita}"
        )
        vytiskni_volbu("1", "Nabídnout praktickou pomoc (10 zl.)")
        vytiskni_volbu("2", "Podpořit její vlastní rozhodnutí (zdarma)")
        vytiskni_volbu("0", "Ukončit rozhovor")
        try:
            volba = input("> ").strip()
        except EOFError:
            return
        if volba == "0":
            return
        if volba not in ("1", "2"):
            tisk_chyba("Neplatná volba.")
            return
        if volba == "1" and hra.hrac.gold < 10:
            tisk_chyba("Na praktickou pomoc potřebuješ 10 zlata.")
            return
        if volba == "1":
            hra.hrac.gold -= 10
            postava["vztah_hraci"] = min(100, postava["vztah_hraci"] + 8)
            mesto.uprav(stabilita=2)
            vysledek = "pomohl jsi jí s místním úkolem"
        else:
            postava["vztah_hraci"] = min(100, postava["vztah_hraci"] + 4)
            mesto.uprav(stabilita=1)
            vysledek = "podpořil jsi její vlastní rozhodnutí"
        postava["pribeh"] += 1
        postava["posledni_rozhovor"] = vysledek
        if postava["pribeh"] == 3:
            frakce = hra.frakce.frakce.get(postava.get("frakce"))
            if frakce:
                frakce.zmenit(4)
            mesto.uprav(prosperita=1, stabilita=1)
            tisk_ok(
                f"Příběh {postava['jmeno']} dospěl k závěru; "
                "místní frakce získala přízeň +4."
            )
        self.historie.append({
            "den": max(1, int(hra.hrac.den)),
            "text": (
                f"{postava['jmeno']}: {vysledek}; "
                f"příběh {postava['pribeh']}/3."
            ),
        })
        self.historie = self.historie[-30:]
        tisk_ok(
            f"{postava['jmeno']} — příběh {postava['pribeh']}/3, "
            f"vztah {postava['vztah_hraci']:+d}; stabilita "
            f"{mesto.nazev} +{2 if volba == '1' else 1}."
        )

    def _menu_diplomacie_frakci(self, hra):
        print("\n=== VZTAHY MEZI FRAKCEMI ===")
        for index, dvojice in enumerate(FRAKCNI_RIVALOVE, 1):
            hodnota = self.vztahy_frakci[_klic_vztahu(*dvojice)]
            print(
                f"  {index}) {FRAKCNI_CILE[dvojice[0]][0]} ↔ "
                f"{FRAKCNI_CILE[dvojice[1]][0]} ({hodnota:+d})"
            )
        try:
            vyber = input("Vyber dvojici (0 zpět): ").strip()
            if vyber == "0":
                return
            index = int(vyber) - 1
            if not 0 <= index < len(FRAKCNI_RIVALOVE):
                raise IndexError
            dvojice = FRAKCNI_RIVALOVE[index]
        except (EOFError, ValueError, IndexError):
            tisk_chyba("Neplatná dvojice.")
            return
        vytiskni_volbu("1", "Zprostředkovat smír (25 zl., vztahy +15)")
        vytiskni_volbu("2", "Podpořit soupeření (vztahy −15, stabilita −2)")
        try:
            rozhodnuti = input("> ").strip()
        except EOFError:
            return
        if rozhodnuti == "1":
            if hra.hrac.gold < 25:
                tisk_chyba("Na zprostředkování smíru potřebuješ 25 zlata.")
                return
            hra.hrac.gold -= 25
            self.zmen_vztah_frakci(*dvojice, 15)
            for frakce_id in dvojice:
                frakce = hra.frakce.frakce.get(frakce_id)
                if frakce:
                    frakce.zmenit(2)
            mesto = self.mesta[self._mesto_pro_frakci(dvojice[0])]
            mesto.uprav(stabilita=2)
            vysledek = "zprostředkoval jsi smír"
        elif rozhodnuti == "2":
            self.zmen_vztah_frakci(*dvojice, -15)
            mesto = self.mesta[self._mesto_pro_frakci(dvojice[0])]
            mesto.uprav(stabilita=-2)
            vysledek = "podpořil jsi soupeření"
        else:
            tisk_chyba("Neplatná volba.")
            return
        self.historie.append({
            "den": max(1, int(hra.hrac.den)),
            "text": (
                f"{FRAKCNI_CILE[dvojice[0]][0]} a "
                f"{FRAKCNI_CILE[dvojice[1]][0]}: {vysledek}."
            ),
        })
        self.historie = self.historie[-30:]
        tisk_ok(f"Rozhodnutí změnilo vztahy mezi frakcemi: {vysledek}.")

    def _vyres_nabidku(self, hra, nabidka):
        while True:
            for index, moznost in enumerate(MOZNOSTI_ZASAHU, 1):
                oznaceni = (
                    " — nedostatek zlata"
                    if hra.hrac.gold < moznost["cena"] else ""
                )
                vytiskni_volbu(str(index), moznost["text"] + oznaceni)
            vytiskni_volbu("0", "Nechat situaci bez zásahu")
            try:
                volba = input("> ").strip()
            except EOFError:
                return False
            if volba == "0":
                tisk_info("Situaci ponecháváš jejímu vývoji.")
                self._zapis(hra, nabidka, "bez zásahu")
                return True
            try:
                index = int(volba) - 1
            except ValueError:
                index = -1
            if not 0 <= index < len(MOZNOSTI_ZASAHU):
                tisk_chyba("Zadej číslo dostupné možnosti.")
                continue
            moznost = MOZNOSTI_ZASAHU[index]
            if hra.hrac.gold < moznost["cena"]:
                tisk_chyba("Na tuto možnost nemáš dost zlata.")
                continue
            hra.hrac.gold -= moznost["cena"]
            frakce = hra.frakce.frakce.get(nabidka["frakce_id"])
            if frakce:
                frakce.zmenit(moznost["frakce"])
            mesto_id = nabidka.get("mesto_id", "stare_mesto")
            lokace_id = nabidka.get("lokace_id")
            if lokace_id not in self.kontrola_lokaci:
                lokace_id = MESTA.get(mesto_id, MESTA["stare_mesto"])["lokace"][0]
            self._uprav_vliv_lokace(
                lokace_id, nabidka["frakce_id"], moznost["frakce"]
            )
            hra.hrac.reputace_mesta = max(
                -100,
                min(100, hra.hrac.reputace_mesta + moznost["mesto"]),
            )
            mesto = self.mesta.get(nabidka.get("mesto_id", "stare_mesto"))
            if mesto:
                dopady = (
                    {"prosperita": 2, "stabilita": 1},
                    {"bezpeci": 1, "stabilita": 2},
                    {"bezpeci": -1, "stabilita": -2},
                )
                mesto.uprav(**dopady[index])
            tisk_ok(f"Rozhodl ses: {moznost['text']}.")
            self._zapis(hra, nabidka, moznost["text"])
            return True

    def _zapis(self, hra, nabidka, rozhodnuti):
        zaznam = {
            "den": max(1, int(hra.hrac.den)),
            "text": f"{nabidka['frakce_nazev']}: {rozhodnuti}.",
        }
        self.historie.append(zaznam)
        self.historie = self.historie[-30:]
        from game.kronika import zaznamenej
        zaznamenej(hra, f"Živý svět: {zaznam['text']}")


def _kladne_cislo(hodnota):
    if isinstance(hodnota, bool):
        return 0
    try:
        return max(0, int(hodnota))
    except (TypeError, ValueError):
        return 0


def _signed_cislo(hodnota):
    if isinstance(hodnota, bool):
        return 0
    try:
        return int(hodnota)
    except (TypeError, ValueError):
        return 0


def _klic_vztahu(frakce_a, frakce_b):
    return "|".join(sorted((frakce_a, frakce_b)))


def _lokace_udalosti(typ, mesto_id):
    return MISTA_UDALOSTI.get(typ, {}).get(
        mesto_id, MESTA[mesto_id]["lokace"][0]
    )


def _mesto_lokace(lokace_id):
    return LOKACE.get(lokace_id, {}).get("mesto", "stare_mesto")


def _vychozi_frakce_lokace(lokace_id):
    for frakce_id, lokace in FRAKCNI_ZONY.items():
        if lokace_id in lokace:
            return frakce_id
    return "policie"


def _prvni_mesto_frakce(frakce_id):
    for lokace_id in FRAKCNI_ZONY.get(frakce_id, ()):
        if lokace_id in LOKACE:
            return _mesto_lokace(lokace_id)
    return "stare_mesto"
