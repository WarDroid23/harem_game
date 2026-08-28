"""Nastavení hry a jejich bezpečná normalizace při načtení."""

from dataclasses import dataclass

from config import set_colors_enabled

OBTIZNOSTI = ("lehka", "normalni", "tezka")
VYCHOZI_OBTIZNOST = "normalni"


@dataclass
class NastaveniHry:
    barvy: bool = True
    obtiznost: str = VYCHOZI_OBTIZNOST

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

    def aplikuj(self):
        set_colors_enabled(self.barvy)

    def to_dict(self):
        return {"barvy": self.barvy, "obtiznost": self.obtiznost}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            barvy=data.get("barvy", True),
            obtiznost=data.get("obtiznost", VYCHOZI_OBTIZNOST),
        )

    @property
    def obtiznost_text(self):
        return {
            "lehka": "Lehká",
            "normalni": "Normální",
            "tezka": "Těžká",
        }[self.obtiznost]


def aplikuj_nastaveni(nastaveni):
    """Aplikuje barvy a vrátí normalizované nastavení."""
    if not isinstance(nastaveni, NastaveniHry):
        nastaveni = NastaveniHry.from_dict(nastaveni)
    nastaveni.aplikuj()
    return nastaveni
