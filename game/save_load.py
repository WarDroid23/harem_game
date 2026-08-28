# game/save_load.py
import json
import os
import shutil
import tempfile
from pathlib import Path
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
        if not isinstance(data, dict):
            raise ValueError("Uložená hra musí být JSON objekt.")
        hra = cls()
        sekce = {
            nazev: data.get(nazev, {})
            if isinstance(data.get(nazev, {}), dict) else {}
            for nazev in ("hrac", "harem", "frakce", "mafie")
        }
        hra.hrac = Hrac.from_dict(sekce["hrac"])
        hra.harem = Harem.from_dict(sekce["harem"])
        hra.frakce = FrakcniSystem.from_dict(sekce["frakce"])
        hra.mafie = Mafie.from_dict(sekce["mafie"])
        if isinstance(data.get("vyzkum"), dict):
            hra.vyzkum = VyzkumSystem.from_dict(data["vyzkum"])
        if isinstance(data.get("questy"), dict):
            hra.questy = QuestSystem.from_dict(data["questy"])
        if isinstance(data.get("alchymie"), dict):
            hra.alchymie = AlchymieSystem.from_dict(data["alchymie"])
        return hra

def uloz_hru(hra: Hra, soubor=SAVE_FILE):
    """Uloží hru atomicky ve stejné složce a zachová jednu záložní kopii."""
    cesta = Path(soubor).expanduser()
    slozka = cesta.parent if str(cesta.parent) else Path(".")
    docasny = None
    try:
        slozka.mkdir(parents=True, exist_ok=True)
        data = hra.to_dict()
        fd, docasny = tempfile.mkstemp(
            prefix=f".{cesta.name}.", suffix=".tmp", dir=str(slozka)
        )
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        zaloha = cesta.with_name(cesta.name + ".bak")
        if cesta.exists():
            shutil.copy2(cesta, zaloha)
        os.replace(docasny, cesta)
        docasny = None
        print(f"Hra uložena do {cesta}.")
        return True
    except (OSError, TypeError, ValueError) as chyba:
        if docasny:
            try:
                os.unlink(docasny)
            except OSError:
                pass
        print(f"Uložení selhalo: {chyba}")
        return False

def nacti_hru(soubor=SAVE_FILE):
    """Načte hlavní sejv, při poškození zkusí jeho poslední zálohu."""
    cesta = Path(soubor).expanduser()
    if not cesta.exists() and not cesta.with_name(cesta.name + ".bak").exists():
        print("Žádná uložená hra.")
        return None

    cesty = [cesta, cesta.with_name(cesta.name + ".bak")]
    posledni_chyba = None
    for index, kandidát in enumerate(cesty):
        if not kandidát.exists():
            continue
        try:
            with kandidát.open("r", encoding="utf-8") as f:
                data = json.load(f)
            hra = Hra.from_dict(data)
            if index:
                print("Hlavní sejv byl poškozen, načtena záložní kopie.")
            return hra
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as chyba:
            posledni_chyba = chyba

    print(f"Načtení selhalo: {posledni_chyba}")
    return None
