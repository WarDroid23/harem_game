# models/mafie.py
from dataclasses import dataclass, field, asdict, fields

BOSSOVE_MAFIE = {"zelezny_baron_vargan", "vevoda_beze_jmena"}
LOKACE_PODLE_UZEMI = {
    "Přístav": "pristav",
    "Tržiště": "trh",
    "Čtvrť bohatých": "palac_bohatych",
    "Doky": "molo_mesicniho_pristavu",
    "Staré město": "katakomby",
    "Černá čtvrť": "cerna_ctvrt",
    "Říční nábřeží": "ricni_nabrezi",
    "Univerzitní okrsek": "univerzitni_okrsek",
    "Dýmová čtvrť": "dymova_ctvrt",
    "Cechovní uličky": "cechovni_ulicky",
    "Půlnoční trh": "pulnocni_trh",
    "Staré katakomby": "stare_katakomby",
    "Kovárenský okrsek": "kovarensky_okrsek",
    "Lucernová čtvrť": "lucernova_ctvrt",
    "Severní hradby": "severni_hradby",
    "Akademické náměstí": "akademicke_namesti",
}

@dataclass
class Uzemi:
    nazev: str
    prijem: int
    kontrola: int = 0
    riziko_inkvizice: int = 0
    obsazeno: bool = False
    opevneni: int = 0
    posadka: int = 0
    podniky: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data území musí být objekt.")
        allowed = {f.name for f in fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in allowed})

@dataclass
class Mafie:
    uzemi: list = field(default_factory=list)
    vojaci: int = 0
    kapitanove: int = 0
    prijem_celkem: int = 0
    informatori: int = 0
    korupce: int = 0
    vliv_ve_meste: int = 0
    bossove_porazeni: list = field(default_factory=list)

    def vypocet_prijmu(self):
        zaklad = sum(u.prijem * u.kontrola // 100 for u in self.uzemi if u.obsazeno)
        podniky_prijem = sum(sum(p.get("prijem", 0) for p in u.podniky.values()) for u in self.uzemi if u.obsazeno and hasattr(u, "podniky"))
        bonus = self.vojaci // 5 + self.kapitanove * 3 + self.vliv_ve_meste // 20 + self.informatori // 2
        self.prijem_celkem = zaklad + podniky_prijem + bonus
        return self.prijem_celkem

    def bojova_sila(self):
        return self.vojaci * 1 + self.kapitanove * 5 + self.vliv_ve_meste // 10

    def to_dict(self):
        return {
            "uzemi": [u.to_dict() for u in self.uzemi],
            "vojaci": self.vojaci,
            "kapitanove": self.kapitanove,
            "prijem_celkem": self.prijem_celkem,
            "informatori": self.informatori,
            "korupce": self.korupce,
            "vliv_ve_meste": self.vliv_ve_meste,
            "bossove_porazeni": list(self.bossove_porazeni),
        }

    @classmethod
    def from_dict(cls, data):
        m = cls()
        m.uzemi = [Uzemi.from_dict(u) if isinstance(u, dict) else u for u in data.get("uzemi", [])]
        m.vojaci = data.get("vojaci", 0)
        m.kapitanove = data.get("kapitanove", 0)
        m.prijem_celkem = data.get("prijem_celkem", 0)
        m.informatori = data.get("informatori", 0)
        m.korupce = data.get("korupce", 0)
        m.vliv_ve_meste = data.get("vliv_ve_meste", 0)
        porazeni = data.get("bossove_porazeni", [])
        if isinstance(porazeni, list):
            m.bossove_porazeni = list(dict.fromkeys(
                boss for boss in porazeni
                if isinstance(boss, str) and boss in BOSSOVE_MAFIE
            ))
        return m
