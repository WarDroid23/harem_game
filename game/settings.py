"""Nastavení hry včetně témat, Ironman, AI dialogů a vývojářských pomůcek."""

from dataclasses import dataclass

from config import set_colors_enabled, apply_theme, THEMES, CURRENT_THEME

OBTIZNOSTI = ("lehka", "normalni", "tezka")
VYCHOZI_OBTIZNOST = "normalni"
VYCHOZI_TEMA = "temne_dominium"
VYCHOZI_DEKORACE_MESTA = "trh"
STYLY_MENU = ("kategorie", "seznam", "kompaktni", "sekce", "mrizka")
VYCHOZI_STYL_MENU = "kategorie"

MESTSKA_DEKORACE = {
    "trh": {
        "nazev": "Křivolaké tržiště",
        "popis": "Světelné lampy, kožené stánky a živé strážce u každé uličky.",
        "atmosfera": "Ulice jsou živé, plné pachu koření, zvuku obchodníků a křiků z válek o cenu.",
    },
    "palac": {
        "nazev": "Královský palác",
        "popis": "Mramorové schodiště, zlaté lamely a slavnostní dvůr pro temnou šlechtu.",
        "atmosfera": "Město působí vznešeně, s kovově znějícími schody, šepotem sluhů a leskem zlata.",
    },
    "podsveti": {
        "nazev": "Krvavé podsvětí",
        "popis": "Přepych, černé lampy a nevěstinské světlo v ulicích plných stínů.",
        "atmosfera": "Ve tmě se rozsvěcují rudé lucerny a každý roh působí jako místo tajné dohody.",
    },
    "pevnost": {
        "nazev": "Pevnostní citadela",
        "popis": "Hradby, ohně a brusinkově červené ocelové brány jako symbol moci.",
        "atmosfera": "Město zastává obraz hradního žalu: těžké brány, stráže a odlesky pochodní na kameni.",
    },
    "sypka": {
        "nazev": "Lunární salon",
        "popis": "Nakloněné výlohy, měkké fialové světlo a intriky bohatých patronů.",
        "atmosfera": "Z uliček se linou fialové stíny a šepot tajných schůzek, jako by noc sama poslouchala.",
    },
}


@dataclass
class NastaveniHry:
    barvy: bool = True
    obtiznost: str = VYCHOZI_OBTIZNOST
    tema: str = VYCHOZI_TEMA
    styl_menu: str = VYCHOZI_STYL_MENU
    dekorace_mesta: str = VYCHOZI_DEKORACE_MESTA
    ironman: bool = False
    ai_dialogy: bool = False
    vyvojarsky_rezim: bool = False

    def __post_init__(self):
        if isinstance(self.barvy, str):
            self.barvy = self.barvy.strip().lower() in {"1", "true", "ano", "on"}
        else:
            self.barvy = bool(self.barvy)
        aliases = {"easy": "lehka", "normal": "normalni", "hard": "tezka"}
        if isinstance(self.obtiznost, str):
            klic = self.obtiznost.strip().lower()
            self.obtiznost = aliases.get(klic, klic)
        else:
            self.obtiznost = VYCHOZI_OBTIZNOST
        if self.obtiznost not in OBTIZNOSTI:
            self.obtiznost = VYCHOZI_OBTIZNOST
        if not isinstance(self.tema, str) or self.tema not in THEMES:
            self.tema = VYCHOZI_TEMA
        if not isinstance(self.styl_menu, str) or self.styl_menu not in STYLY_MENU:
            self.styl_menu = VYCHOZI_STYL_MENU
        if not isinstance(self.dekorace_mesta, str) or self.dekorace_mesta not in MESTSKA_DEKORACE:
            self.dekorace_mesta = VYCHOZI_DEKORACE_MESTA
        self.ironman = bool(self.ironman)
        if isinstance(self.ai_dialogy, str):
            self.ai_dialogy = self.ai_dialogy.strip().lower() in {"1", "true", "ano", "on"}
        else:
            self.ai_dialogy = bool(self.ai_dialogy)
        if isinstance(self.vyvojarsky_rezim, str):
            self.vyvojarsky_rezim = self.vyvojarsky_rezim.strip().lower() in {
                "1", "true", "ano", "on",
            }
        else:
            self.vyvojarsky_rezim = bool(self.vyvojarsky_rezim)

    def aplikuj(self):
        set_colors_enabled(self.barvy)
        if self.barvy:
            apply_theme(self.tema)

    def to_dict(self):
        return {
            "barvy": self.barvy,
            "obtiznost": self.obtiznost,
            "tema": self.tema,
            "styl_menu": self.styl_menu,
            "dekorace_mesta": self.dekorace_mesta,
            "ironman": self.ironman,
            "ai_dialogy": self.ai_dialogy,
            "vyvojarsky_rezim": self.vyvojarsky_rezim,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            barvy=data.get("barvy", True),
            obtiznost=data.get("obtiznost", VYCHOZI_OBTIZNOST),
            tema=data.get("tema", VYCHOZI_TEMA),
            styl_menu=data.get("styl_menu", VYCHOZI_STYL_MENU),
            dekorace_mesta=data.get("dekorace_mesta", VYCHOZI_DEKORACE_MESTA),
            ironman=data.get("ironman", False),
            ai_dialogy=data.get("ai_dialogy", False),
            vyvojarsky_rezim=data.get("vyvojarsky_rezim", False),
        )

    @property
    def obtiznost_text(self):
        base = {
            "lehka": "Lehká",
            "normalni": "Normální",
            "tezka": "Těžká",
        }[self.obtiznost]
        if self.ironman:
            return base + " [Ironman]"
        return base

    @property
    def tema_text(self):
        return THEMES.get(self.tema, THEMES[VYCHOZI_TEMA])["nazev"]

    @property
    def styl_menu_text(self):
        return {
            "kategorie": "Čtyři kategorie v rámečcích",
            "seznam": "Jednoduchý seznam bez kategorií",
            "kompaktni": "Kompaktní dvousloupcové menu",
            "sekce": "Čtyři přehledné sekce bez rámečků",
            "mrizka": "Hustá mřížka ve třech sloupcích",
        }[self.styl_menu]

    @property
    def dekorace_mesta_text(self):
        return MESTSKA_DEKORACE.get(self.dekorace_mesta, MESTSKA_DEKORACE[VYCHOZI_DEKORACE_MESTA])["nazev"]


def aplikuj_nastaveni(nastaveni):
    if not isinstance(nastaveni, NastaveniHry):
        nastaveni = NastaveniHry.from_dict(nastaveni)
    nastaveni.aplikuj()
    return nastaveni
