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
        "kult_krve": Frakce("Kult Krvavého Měsíce", "Fanatičtí uctívači temných sil a rituálů", 0),
        "syndikat_stinu": Frakce("Syndikát Nočních stínů", "Cech zlodějů, špehů a nájemných vrahů", 5),
        "cech_kurtizan": Frakce("Cech kurtizán", "Vlivná síť nevěstinců, společnic a šlechty", 15),
    })

    def to_dict(self):
        return {k: v.to_dict() for k, v in self.frakce.items()}

    @classmethod
    def from_dict(cls, data):
        fs = cls()
        for k, v in data.items():
            fs.frakce[k] = Frakce.from_dict(v)
        # Zajištění nových výchozích frakcí i pro starší savy
        vychozi = cls().frakce
        for k, v in vychozi.items():
            if k not in fs.frakce:
                fs.frakce[k] = v
        return fs
