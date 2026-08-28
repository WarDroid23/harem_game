# models/frakce.py
from dataclasses import dataclass, field, asdict, fields

@dataclass
class Frakce:
    nazev: str
    popis: str
    reputace: int = 0

    def zmenit(self, delta):
        self.reputace = max(-100, min(100, self.reputace + delta))
        print(f"{self.nazev}: {delta:+d} → {self.reputace}")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data frakce musí být objekt.")
        allowed = {f.name for f in fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in allowed})

@dataclass
class FrakcniSystem:
    frakce: dict = field(default_factory=lambda: {
        "policie": Frakce("Policie", "Strážci zákona", -20),
        "podsveti": Frakce("Podsvětí", "Otrokáři a sadisté", 20),
        "cirkev": Frakce("Inkvizice", "Svatí muži", -5),
        "obchodnici": Frakce("Obchodníci", "Kupci", 10),
    })

    def to_dict(self):
        return {k: v.to_dict() for k, v in self.frakce.items()}

    @classmethod
    def from_dict(cls, data):
        fs = cls()
        for k, v in data.items():
            fs.frakce[k] = Frakce.from_dict(v)
        return fs
