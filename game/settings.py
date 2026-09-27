"""Nastavení hry včetně témat, Ironman, AI dialogů a vývojářských pomůcek."""

from dataclasses import dataclass

from config import set_colors_enabled, apply_theme, THEMES, CURRENT_THEME

OBTIZNOSTI = ("lehka", "normalni", "tezka")
VYCHOZI_OBTIZNOST = "normalni"
VYCHOZI_TEMA = "temne_dominium"
STYLY_MENU = ("kategorie", "seznam", "kompaktni", "sekce", "mrizka")
VYCHOZI_STYL_MENU = "kategorie"


@dataclass
class NastaveniHry:
    barvy: bool = True
    obtiznost: str = VYCHOZI_OBTIZNOST
    tema: str = VYCHOZI_TEMA
    styl_menu: str = VYCHOZI_STYL_MENU
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


def aplikuj_nastaveni(nastaveni):
    if not isinstance(nastaveni, NastaveniHry):
        nastaveni = NastaveniHry.from_dict(nastaveni)
    nastaveni.aplikuj()
    return nastaveni
