"""Nastavení hry včetně barevných témat, Ironman a AI dialogů."""

from dataclasses import dataclass

from config import set_colors_enabled, apply_theme, THEMES, CURRENT_THEME

OBTIZNOSTI = ("lehka", "normalni", "tezka")
VYCHOZI_OBTIZNOST = "normalni"
VYCHOZI_TEMA = "temne_dominium"


@dataclass
class NastaveniHry:
    barvy: bool = True
    obtiznost: str = VYCHOZI_OBTIZNOST
    tema: str = VYCHOZI_TEMA
    ironman: bool = False
    ai_dialogy: bool = False

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
        self.ironman = bool(self.ironman)
        if isinstance(self.ai_dialogy, str):
            self.ai_dialogy = self.ai_dialogy.strip().lower() in {"1", "true", "ano", "on"}
        else:
            self.ai_dialogy = bool(self.ai_dialogy)

    def aplikuj(self):
        set_colors_enabled(self.barvy)
        if self.barvy:
            apply_theme(self.tema)

    def to_dict(self):
        return {
            "barvy": self.barvy,
            "obtiznost": self.obtiznost,
            "tema": self.tema,
            "ironman": self.ironman,
            "ai_dialogy": self.ai_dialogy,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            barvy=data.get("barvy", True),
            obtiznost=data.get("obtiznost", VYCHOZI_OBTIZNOST),
            tema=data.get("tema", VYCHOZI_TEMA),
            ironman=data.get("ironman", False),
            ai_dialogy=data.get("ai_dialogy", False),
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


def aplikuj_nastaveni(nastaveni):
    if not isinstance(nastaveni, NastaveniHry):
        nastaveni = NastaveniHry.from_dict(nastaveni)
    nastaveni.aplikuj()
    return nastaveni
