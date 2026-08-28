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
from models.marriage import Marriage
from game.vyzkum import VyzkumSystem
from game.questy import QuestSystem
from game.alchymie import AlchymieSystem
from game.svet import SvetSystem
from game.kampan import KampanSystem
from game.osudy import zajisti_osudy
from game.settings import NastaveniHry, aplikuj_nastaveni
from game.expedice import ExpeditionSystem
from game.npc_questy import NPCQuestSystem
from models.calendar import CalendarSystem
from models.fortress import FortressDevelopment
from models.achievements import AchievementSystem

POCET_SLOTU = 5
NAZVY_SLOTU = {
    1: "Hlavní save (kompatibilní se starým souborem)",
    2: "Slot 2",
    3: "Slot 3",
    4: "Slot 4",
    5: "Slot 5",
}

class Hra:
    def __init__(self):
        self.nastaveni = NastaveniHry()
        self.nastaveni.aplikuj()
        self.hrac = Hrac()
        self.harem = Harem()
        self.frakce = FrakcniSystem()
        self.mafie = Mafie()
        self.vyzkum = VyzkumSystem()
        self.questy = QuestSystem()
        self.alchymie = AlchymieSystem()
        self.svet = SvetSystem()
        self.kampan = KampanSystem()
        self.expedice = ExpeditionSystem()
        self.npc_questy = NPCQuestSystem()
        self.pevnost = FortressDevelopment()
        self.kalendar = CalendarSystem(self.hrac.den)
        self.achievementy = AchievementSystem()
        self.marriage_system = {}  # slovník {jmeno_otrokyne: Marriage objekt}

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
            "svet": self.svet.to_dict(),
            "kampan": self.kampan.to_dict(),
            "expedice": self.expedice.to_dict(),
            "npc_questy": self.npc_questy.to_dict(),
            "pevnost": self.pevnost.to_dict(),
            "kalendar": self.kalendar.to_dict(),
            "achievementy": self.achievementy.to_dict(),
            "nastaveni": self.nastaveni.to_dict(),
            "marriage_system": {k: v.to_dict() for k, v in self.marriage_system.items()},
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Uložená hra musí být JSON objekt.")
        hra = cls()
        hra.nastaveni = aplikuj_nastaveni(NastaveniHry.from_dict(data.get("nastaveni", {})))
        sekce = {
            nazev: data.get(nazev, {})
            if isinstance(data.get(nazev, {}), dict) else {}
            for nazev in ("hrac", "harem", "frakce", "mafie")
        }
        hra.hrac = Hrac.from_dict(sekce["hrac"])
        hra.harem = Harem.from_dict(sekce["harem"])
        hra.frakce = FrakcniSystem.from_dict(sekce["frakce"])
        hra.mafie = Mafie.from_dict(sekce["mafie"])
        zajisti_osudy(hra.harem)
        if isinstance(data.get("vyzkum"), dict):
            hra.vyzkum = VyzkumSystem.from_dict(data["vyzkum"])
        if isinstance(data.get("questy"), dict):
            hra.questy = QuestSystem.from_dict(data["questy"])
        if isinstance(data.get("alchymie"), dict):
            hra.alchymie = AlchymieSystem.from_dict(data["alchymie"])
        if isinstance(data.get("svet"), dict):
            hra.svet = SvetSystem.from_dict(data["svet"])
        if isinstance(data.get("kampan"), dict):
            hra.kampan = KampanSystem.from_dict(data["kampan"])
        if isinstance(data.get("expedice"), dict):
            hra.expedice = ExpeditionSystem.from_dict(data["expedice"])
        if isinstance(data.get("npc_questy"), dict):
            hra.npc_questy = NPCQuestSystem.from_dict(data["npc_questy"])
        if isinstance(data.get("pevnost"), dict):
            hra.pevnost = FortressDevelopment.from_dict(data["pevnost"])
        hra.kalendar = CalendarSystem.from_dict(
            data.get("kalendar"), fallback_den=hra.hrac.den
        )
        # Hrac.den je autoritativní pro starší sejvy, nový kalendář se s ním
        # srovná při migraci bez ztráty historie událostí.
        hra.kalendar.den = max(hra.kalendar.den, hra.hrac.den)
        hra.hrac.den = hra.kalendar.den
        if isinstance(data.get("achievementy"), dict):
            hra.achievementy = AchievementSystem.from_dict(data["achievementy"])
        # Načtení marriage_system
        if isinstance(data.get("marriage_system"), dict):
            hra.marriage_system = {
                k: Marriage.from_dict(v) 
                for k, v in data["marriage_system"].items()
            }
        # Staré sejvy končily po třetí kapitole; pokračování se odemkne bez
        # přepsání inventáře, harému nebo dosavadních rozhodnutí.
        if hra.kampan.kapitola >= 3 and not hra.kampan.dokonceno:
            hra.svet.odhal_lokaci("sklenena_zahrada")
        return hra


def cesta_slotu(slot, hlavni_soubor=SAVE_FILE):
    """Vrátí cestu slotu; slot 1 zůstává přesně původním hlavním savem."""
    try:
        slot = int(slot)
    except (TypeError, ValueError):
        raise ValueError("Slot musí být číslo 1 až 3.")
    if slot < 1 or slot > POCET_SLOTU:
        raise ValueError(f"Slot musí být číslo 1 až {POCET_SLOTU}.")
    cesta = Path(hlavni_soubor).expanduser()
    if slot == 1:
        return cesta
    return cesta.with_name(f"{cesta.stem}_slot{slot}{cesta.suffix}")


def seznam_slotu(hlavni_soubor=SAVE_FILE):
    """Vrátí stav tří slotů bez vytváření nebo přepisování souborů."""
    return [
        {
            "slot": slot,
            "nazev": NAZVY_SLOTU[slot],
            "cesta": cesta_slotu(slot, hlavni_soubor),
            "existuje": cesta_slotu(slot, hlavni_soubor).exists(),
        }
        for slot in range(1, POCET_SLOTU + 1)
    ]


def uloz_slot(hra, slot, hlavni_soubor=SAVE_FILE):
    return uloz_hru(hra, cesta_slotu(slot, hlavni_soubor))


def nacti_slot(slot, hlavni_soubor=SAVE_FILE):
    return nacti_hru(cesta_slotu(slot, hlavni_soubor))

def uloz_hru(hra: Hra, soubor=SAVE_FILE):
    """Uloží hru atomicky a rotuje tři záložní kopie bez mazání hlavního savu."""
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
        if cesta.exists():
            for index in range(3, 1, -1):
                starsi = cesta.with_name(cesta.name + f".bak{index - 1}")
                novejsi = cesta.with_name(cesta.name + f".bak{index}")
                if starsi.exists():
                    shutil.copy2(starsi, novejsi)
            shutil.copy2(cesta, cesta.with_name(cesta.name + ".bak"))
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
    """Načte hlavní sejv a při poškození zkusí všechny dostupné zálohy."""
    cesta = Path(soubor).expanduser()
    if not cesta.exists() and not cesta.with_name(cesta.name + ".bak").exists():
        print("Žádná uložená hra.")
        return None

    cesty = [
        cesta,
        cesta.with_name(cesta.name + ".bak"),
        cesta.with_name(cesta.name + ".bak2"),
        cesta.with_name(cesta.name + ".bak3"),
    ]
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


def cesta_autosave(hlavni_soubor=SAVE_FILE):
    cesta = Path(hlavni_soubor).expanduser()
    return cesta.with_name(cesta.stem + "_autosave" + cesta.suffix)


def uloz_autosave(hra, hlavni_soubor=SAVE_FILE):
    """Zapíše bezpečný autosave do samostatného souboru, nikdy přes hlavní slot."""
    return uloz_hru(hra, cesta_autosave(hlavni_soubor))
