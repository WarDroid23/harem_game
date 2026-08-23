# game/save_load.py
import json
import os
import tempfile
from config import SAVE_FILE, VERSION
from models.hrac import Hrac
from models.harem import Harem
from models.frakce import FrakcniSystem
from models.mafie import Mafie
from game.vyzkum import VyzkumSystem
from game.questy import QuestSystem
from game.alchymie import AlchymieSystem

class Hra:
    def __init__(self):
        self.hrac = Hrac()
        self.harem = Harem()
        self.frakce = FrakcniSystem()
        self.mafie = Mafie()
        self.vyzkum = VyzkumSystem()
        self.questy = QuestSystem()
        self.alchymie = AlchymieSystem()

    def to_dict(self):
        return {
            "verze": VERSION,
            "hrac": self.hrac.to_dict(),
            "harem": self.harem.to_dict(),
            "frakce": self.frakce.to_dict(),
            "mafie": self.mafie.to_dict(),
            "vyzkum": self.vyzkum.to_dict(),
            "questy": self.questy.to_dict(),
            "alchymie": self.alchymie.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        hra = cls()
        hra.hrac = Hrac.from_dict(data["hrac"])
        hra.harem = Harem.from_dict(data["harem"])
        hra.frakce = FrakcniSystem.from_dict(data["frakce"])
        hra.mafie = Mafie.from_dict(data["mafie"])
        if "vyzkum" in data:
            hra.vyzkum = VyzkumSystem.from_dict(data["vyzkum"])
        if "questy" in data:
            hra.questy = QuestSystem.from_dict(data["questy"])
        if "alchymie" in data:
            hra.alchymie = AlchymieSystem.from_dict(data["alchymie"])
        return hra

def uloz_hru(hra: Hra, soubor=SAVE_FILE):
    data = hra.to_dict()
    fd, tmp = tempfile.mkstemp()
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, soubor)
    print("Hra uložena.")

def nacti_hru(soubor=SAVE_FILE):
    if not os.path.exists(soubor):
        print("Žádná uložená hra.")
        return None
    with open(soubor, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Hra.from_dict(data)
