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
        if not isinstance(otrokyne, Otrokyně):
            raise TypeError("Do harému lze přidat pouze otrokyni.")
        if not getattr(otrokyne, "osud_id", ""):
            from game.osudy import vyber_osud
            otrokyne.osud_id = vyber_osud(otrokyne)
        self.otrokyne.append(otrokyne)
        self.harem_exp += 12
        while self.harem_exp >= self.harem_max_exp:
            self.harem_exp -= self.harem_max_exp
            self.harem_level += 1
            self.harem_max_exp = int(self.harem_max_exp * 1.8)

    def odstranit(self, jmeno):
        for index, otrok in enumerate(self.otrokyne):
            if otrok.jmeno == jmeno:
                del self.otrokyne[index]
                break

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
        if not isinstance(data, dict):
            raise ValueError("Data harému musí být objekt.")
        h = cls()
        otrokyne = data.get("otrokyne", [])
        h.otrokyne = [
            Otrokyně.from_dict(o) for o in otrokyne if isinstance(o, dict)
        ] if isinstance(otrokyne, list) else []
        from game.osudy import zajisti_osudy
        zajisti_osudy(h)
        h.harem_level = max(1, int(data.get("harem_level", 1)))
        h.harem_exp = max(0, int(data.get("harem_exp", 0)))
        h.harem_max_exp = max(1, int(data.get("harem_max_exp", 100)))
        budovy = data.get("budovy", {})
        if isinstance(budovy, dict):
            for k, v in budovy.items():
                if (
                    k in h.budovy
                    and isinstance(v, dict)
                    and v.get("typ", k) in Building.TYPY
                ):
                    h.budovy[k] = Building.from_dict(v)
        return h
