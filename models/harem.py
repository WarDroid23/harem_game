# models/harem.py
from dataclasses import dataclass, field, asdict
from models.otrokyne import Otrokyně
from models.building import Building

@dataclass
class Harem:
    otrokyne: list = field(default_factory=list)
    harem_level: int = 1
    harem_exp: int = 0
    harem_max_exp: int = 100
    budovy: dict = field(default_factory=lambda: {t: Building(t) for t in Building.TYPY})

    def pocet(self):
        return len([o for o in self.otrokyne if o.hp > 0])

    def pridat(self, otrokyne):
        self.otrokyne.append(otrokyne)
        self.harem_exp += 12
        if self.harem_exp >= self.harem_max_exp:
            self.harem_exp = 0
            self.harem_level += 1
            self.harem_max_exp = int(self.harem_max_exp * 1.8)

    def odstranit(self, jmeno):
        self.otrokyne = [o for o in self.otrokyne if o.jmeno != jmeno]

    def vsechny_aktivni(self):
        return [o for o in self.otrokyne if o.hp > 0]

    def pasivni_prijem(self):
        return 10 * self.harem_level + sum(b.uroven * 3 for b in self.budovy.values())

    def to_dict(self):
        return {
            "otrokyne": [o.to_dict() for o in self.otrokyne],
            "harem_level": self.harem_level,
            "harem_exp": self.harem_exp,
            "harem_max_exp": self.harem_max_exp,
            "budovy": {k: v.to_dict() for k, v in self.budovy.items()}
        }

    @classmethod
    def from_dict(cls, data):
        h = cls()
        h.otrokyne = [Otrokyně.from_dict(o) for o in data.get("otrokyne", [])]
        h.harem_level = data.get("harem_level", 1)
        h.harem_exp = data.get("harem_exp", 0)
        h.harem_max_exp = data.get("harem_max_exp", 100)
        for k, v in data.get("budovy", {}).items():
            h.budovy[k] = Building.from_dict(v)
        return h
