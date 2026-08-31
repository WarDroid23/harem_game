# game/vyzkum.py
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, CYAN, GREEN, RED, NC

VYZKUM = {
    "temna_magie": {
        "nazev": "Temná magie",
        "popis": "Zvyšuje maximální temnou energii o 20.",
        "cena": 300,
        "efekt": lambda hrac: _efekt_temna_magie(hrac),
        "vyzaduje": [],
    },
    "psychologie_zlomeni": {
        "nazev": "Psychologie zlomení",
        "popis": "Zvyšuje účinnost manipulace o 20%.",
        "cena": 400,
        "efekt": lambda hrac: _skill_plus(hrac, "temnota", 5),
        "vyzaduje": ["temna_magie"],
    },
    "obchodni_sit": {
        "nazev": "Obchodní síť",
        "popis": "Okamžitý bonus +50 zlata (pasivní síť).",
        "cena": 500,
        "efekt": lambda hrac: setattr(hrac, "gold", hrac.gold + 50),
        "vyzaduje": [],
    },
    "utajeni": {
        "nazev": "Utajení",
        "popis": "Snižuje vliv inkvizice o 10.",
        "cena": 250,
        "efekt": lambda hrac: setattr(
            hrac, "vliv_inkvizice", max(0, getattr(hrac, "vliv_inkvizice", 0) - 10)
        ),
        "vyzaduje": [],
    },
    "pokrocile_muceni": {
        "nazev": "Pokročilé mučení",
        "popis": "Zvyšuje efektivitu trestů o 30%.",
        "cena": 700,
        "efekt": lambda hrac: _skill_plus(hrac, "dominance", 5),
        "vyzaduje": ["psychologie_zlomeni"],
    },
}


def _skill_plus(hrac, skill, o_kolik):
    if not isinstance(getattr(hrac, "skilly", None), dict):
        hrac.skilly = {}
    hrac.skilly[skill] = hrac.skilly.get(skill, 0) + o_kolik


def _efekt_temna_magie(hrac):
    if hasattr(hrac, "zvys_max_temno"):
        hrac.zvys_max_temno(20)
        hrac.pridej_dark_energy(20)
    else:
        if hasattr(hrac, "max_dark_energy"):
            hrac.max_dark_energy = getattr(hrac, "max_dark_energy", 100) + 20
        hrac.dark_energy = min(
            getattr(hrac, "max_dark_energy", 120), hrac.dark_energy + 20
        )


class VyzkumSystem:
    def __init__(self):
        self.ziskane = set()

    def muzes_vyzkoumat(self, hrac, id_vyzkumu):
        if id_vyzkumu not in VYZKUM:
            return False, "Neznámý výzkum."
        vyzkum = VYZKUM[id_vyzkumu]
        if id_vyzkumu in self.ziskane:
            return False, "Již vyzkoumáno."
        for pozadavek in vyzkum["vyzaduje"]:
            if pozadavek not in self.ziskane:
                return False, f"Chybí požadavek: {VYZKUM[pozadavek]['nazev']}"
        if hrac.gold < vyzkum["cena"]:
            return False, "Nedostatek zlata."
        return True, ""

    def vyzkoumat(self, hrac, id_vyzkumu):
        mozne, duvod = self.muzes_vyzkoumat(hrac, id_vyzkumu)
        if not mozne:
            tisk_chyba(duvod)
            return False
        vyzkum = VYZKUM[id_vyzkumu]
        hrac.gold -= vyzkum["cena"]
        try:
            vyzkum["efekt"](hrac)
        except Exception as e:
            tisk_chyba(f"Efekt výzkumu selhal: {e}")
            hrac.gold += vyzkum["cena"]
            return False
        self.ziskane.add(id_vyzkumu)
        tisk_ok(f"Vyzkoumáno: {vyzkum['nazev']}")
        return True

    def zobraz_vyzkum(self, hrac):
        clear()
        print(f"{GOLD}--- Výzkum ---{NC}")
        print(f"Zlato: {hrac.gold} 🪙\n")
        for i, (id_vyzkumu, vyzkum) in enumerate(VYZKUM.items(), 1):
            status = f"{GREEN}✔{NC}" if id_vyzkumu in self.ziskane else f"{RED}✖{NC}"
            print(f"{i}) {status} {vyzkum['nazev']} (id: {id_vyzkumu}, cena: {vyzkum['cena']})")
            print(f"   {vyzkum['popis']}")
            if vyzkum["vyzaduje"]:
                poz = ", ".join(VYZKUM[p]["nazev"] for p in vyzkum["vyzaduje"])
                print(f"   Požaduje: {poz}")
        print()

    def menu(self, hra):
        hrac = hra.hrac if hasattr(hra, "hrac") else hra
        ids = list(VYZKUM.keys())
        while True:
            self.zobraz_vyzkum(hrac)
            print("Zadej číslo nebo id výzkumu (0 = zpět)")
            try:
                volba = input("> ").strip().lower()
            except EOFError:
                return
            if volba in ("0", "q", ""):
                return
            if volba.isdigit():
                idx = int(volba) - 1
                if 0 <= idx < len(ids):
                    id_v = ids[idx]
                else:
                    tisk_chyba("Špatné číslo.")
                    try:
                        input("Enter...")
                    except EOFError:
                        return
                    continue
            elif volba in VYZKUM:
                id_v = volba
            else:
                tisk_chyba("Neznámý výzkum.")
                try:
                    input("Enter...")
                except EOFError:
                    return
                continue
            self.vyzkoumat(hrac, id_v)
            try:
                input("Enter...")
            except EOFError:
                return

    def to_dict(self):
        return {"ziskane": list(self.ziskane)}

    @classmethod
    def from_dict(cls, data):
        v = cls()
        if isinstance(data, dict):
            v.ziskane = set(data.get("ziskane", []))
        return v
