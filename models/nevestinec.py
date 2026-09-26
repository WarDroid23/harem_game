# models/nevestinec.py
from dataclasses import dataclass, field, asdict, fields

SPECIALIZACE_POKOJU = {
    "klasicky": {
        "nazev": "Klasický budoár",
        "popis": "Univerzální pokoj pro hosty všech stavů.",
        "cena": 0,
        "bonus_vynosu": 1.0,
        "bonus_charakteru": [],
    },
    "bdsm": {
        "nazev": "Mučírna rozkoše (BDSM)",
        "popis": "Černá kůže, pouta a biče. Vhodné pro drsné praktiky. Generuje temnou energii a vysoký zisk od zvrhlíků.",
        "cena": 200,
        "bonus_vynosu": 1.35,
        "bonus_charakteru": ["subka", "krvava_subka", "posedla", "zlomena"],
    },
    "kralovsky": {
        "nazev": "Královský salon",
        "popis": "Hedvábí, zlato a vybraná vína. Přitahuje nejbohatší šlechtu, mecenáše a diplomaty.",
        "cena": 300,
        "bonus_vynosu": 1.5,
        "bonus_charakteru": ["kurtizana", "slechticna", "princezna_ruin"],
    },
    "lazne": {
        "nazev": "Hříšné parní lázně",
        "popis": "Vonné oleje, teplé prameny a erotické masáže. Rychle zvyšuje touhu a vlhkost dívek.",
        "cena": 220,
        "bonus_vynosu": 1.25,
        "bonus_charakteru": ["nymfomanka", "touha", "sukuba_hybrid"],
    },
    "krypta": {
        "nazev": "Okultní krypta vášně",
        "popis": "Temné rituální lože ozářené černými svícemi. Přitahuje kultisty krve a mágy podsvětí.",
        "cena": 280,
        "bonus_vynosu": 1.4,
        "bonus_charakteru": ["knezka_temnoty", "carodejka", "fanaticka", "sukuba_hybrid"],
    },
    "zrcadla": {
        "nazev": "Zrcadlový palác rozkoše",
        "popis": "Stěny i stropy pokryté křišťálovými zrcadly. Hosté sledují každý detail extáze ze všech úhlů.",
        "cena": 350,
        "bonus_vynosu": 1.6,
        "bonus_charakteru": ["kurtizana", "draci_misenka", "temna_elfka", "nymfomanka"],
    },
    "astralni_komnata": {
        "nazev": "Astrální komnata snů",
        "popis": "Zářící mlžné zřídlo a iluze hvězdné oblohy. Poskytuje transcendentální sexuální zážitky.",
        "cena": 320,
        "bonus_vynosu": 1.45,
        "bonus_charakteru": ["kralovska_knezka", "carodejka", "sukuba_hybrid", "princezna_ruin"],
    },
}

@dataclass
class Nevestinec:
    otevreno: bool = False
    nazev: str = "Rudý samet"
    pocet_pokoju: int = 3
    uroven_luxusu: int = 1
    ochranka: int = 1
    celkovy_zisk: int = 0
    obslouzeno_zakazniku: int = 0
    reputace_podniku: int = 10
    specializace_pokoju: dict = field(default_factory=dict)
    vip_nabidky: list = field(default_factory=list)
    kompro_materialy: int = 0
    pocet_festivalu: int = 0
    posledni_den_akce: int = 0

    def cena_rozsireni_pokoju(self) -> int:
        return self.pocet_pokoju * 120

    def cena_luxusu(self) -> int:
        return self.uroven_luxusu * 150

    def cena_ochranky(self) -> int:
        return self.ochranka * 100

    def ziskej_specializaci(self, pokoj_cislo: int) -> str:
        return self.specializace_pokoju.get(str(pokoj_cislo), "klasicky")

    def nastav_specializaci(self, pokoj_cislo: int, typ: str) -> None:
        self.specializace_pokoju[str(pokoj_cislo)] = typ

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict):
            return cls()
        allowed = {f.name for f in fields(cls)}
        clean = {k: v for k, v in data.items() if k in allowed}
        return cls(**clean)
