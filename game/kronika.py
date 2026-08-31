# game/kronika.py — záznam posledních událostí
from collections import deque
from utils.vypis import clear, tisk_info
from config import GOLD, CYAN, NC


class Kronika:
    MAX = 30

    def __init__(self):
        self.zaznamy = deque(maxlen=self.MAX)

    def pridej(self, den, text):
        self.zaznamy.append({"den": den, "text": text})

    def zobraz(self, limit=20):
        clear()
        print(f"{GOLD}--- Kronika dominia ---{NC}\n")
        if not self.zaznamy:
            print("Zatím prázdná. Dny a noci ti teprve začínají.")
            return
        for z in list(self.zaznamy)[-limit:]:
            print(f"{CYAN}Den {z['den']}:{NC} {z['text']}")
        print()

    def to_dict(self):
        return {"zaznamy": list(self.zaznamy)}

    @classmethod
    def from_dict(cls, data):
        k = cls()
        if isinstance(data, dict):
            for z in data.get("zaznamy", [])[-cls.MAX:]:
                if isinstance(z, dict) and "text" in z:
                    k.zaznamy.append({"den": z.get("den", 0), "text": z["text"]})
        return k


def zaznamenej(hra, text):
    if not hasattr(hra, "kronika") or hra.kronika is None:
        hra.kronika = Kronika()
    den = getattr(getattr(hra, "hrac", None), "den", 0)
    hra.kronika.pridej(den, text)
