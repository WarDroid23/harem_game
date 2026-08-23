# models/building.py
from dataclasses import dataclass, asdict

@dataclass
class Building:
    TYPY = {
        "lazne": {"nazev": "Lázně", "cena": 100},
        "cviciste": {"nazev": "Cvičiště", "cena": 120},
        "dungeon": {"nazev": "Mučírna", "cena": 280},
        "dungeon2": {"nazev": "Hluboká mučírna", "cena": 450},
        "oltar": {"nazev": "Oltář temnoty", "cena": 320},
        "oltar_bolesti": {"nazev": "Oltář bolesti", "cena": 500},
        "jama": {"nazev": "Jáma ponížení", "cena": 380},
        "ukryt": {"nazev": "Úkryt", "cena": 280},
        "tunel": {"nazev": "Podzemní chodba", "cena": 300},
    }

    typ: str
    uroven: int = 1

    @property
    def cena(self):
        return int(self.TYPY[self.typ]["cena"] * (1.55 ** (self.uroven - 1)))

    def vylepsi(self):
        self.uroven += 1

    def to_dict(self):
        return {"typ": self.typ, "uroven": self.uroven}

    @classmethod
    def from_dict(cls, data):
        return cls(data["typ"], data["uroven"])
