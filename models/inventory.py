# models/inventory.py
from dataclasses import dataclass, field, asdict, fields

@dataclass
class Zbran:
    nazev: str
    typ: str
    poskozeni: int
    cena: int
    vaha: float = 0.0
    specialni: str = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Inventory:
    predmety: list = field(default_factory=list)
    zbrane: list = field(default_factory=list)
    penize_v_bance: int = 0

    def pridej_zbran(self, zbran: Zbran):
        self.zbrane.append(zbran)

    def odeber_zbran(self, nazev):
        self.zbrane = [z for z in self.zbrane if z.nazev != nazev]

    def to_dict(self):
        return {
            "predmety": self.predmety,
            "zbrane": [z.to_dict() if hasattr(z, 'to_dict') else z for z in self.zbrane],
            "penize_v_bance": self.penize_v_bance
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data inventáře musí být objekt.")
        inv = cls()
        predmety = data.get("predmety", [])
        inv.predmety = predmety if isinstance(predmety, list) else []
        zbrane = data.get("zbrane", [])
        allowed = {f.name for f in fields(Zbran)}
        inv.zbrane = [
            Zbran(**{key: value for key, value in z.items() if key in allowed})
            if isinstance(z, dict) else z
            for z in zbrane
        ] if isinstance(zbrane, list) else []
        inv.penize_v_bance = data.get("penize_v_bance", 0)
        return inv
