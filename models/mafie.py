# models/mafie.py
from dataclasses import dataclass, field, asdict, fields

@dataclass
class Uzemi:
    nazev: str
    prijem: int
    kontrola: int = 0
    riziko_inkvizice: int = 0
    obsazeno: bool = False
    opevneni: int = 0
    posadka: int = 0

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

    def vypocet_prijmu(self):
        self.prijem_celkem = sum(u.prijem * u.kontrola // 100 for u in self.uzemi if u.obsazeno)
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
            "vliv_ve_meste": self.vliv_ve_meste
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
        return m
