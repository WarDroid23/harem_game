# game/vyzkum.py
from utils.vypis import clear, tisk_ok, tisk_chyba

VYZKUM = {
    "temna_magie": {
        "nazev": "Temná magie",
        "popis": "Zvyšuje maximální temnou energii o 20.",
        "cena": 300,
        "efekt": lambda hrac: setattr(hrac, 'dark_energy', hrac.dark_energy + 20),
        "vyzaduje": []
    },
    "psychologie_zlomeni": {
        "nazev": "Psychologie zlomení",
        "popis": "Zvyšuje účinnost manipulace o 20%.",
        "cena": 400,
        "efekt": lambda hrac: setattr(hrac, 'skilly', {**hrac.skilly, 'temnota': hrac.skilly.get('temnota', 0) + 5}),
        "vyzaduje": ["temna_magie"]
    },
    "obchodni_sit": {
        "nazev": "Obchodní síť",
        "popis": "Pasivní příjem +10 zlaťáků za den.",
        "cena": 500,
        "efekt": lambda hrac: setattr(hrac, 'gold', hrac.gold + 10),
        "vyzaduje": []
    },
    "utajeni": {
        "nazev": "Utajení",
        "popis": "Snižuje vliv inkvizice o 10.",
        "cena": 250,
        "efekt": lambda hrac: setattr(hrac, 'vliv_inkvizice', max(0, hrac.vliv_inkvizice - 10)),
        "vyzaduje": []
    },
    "pokrocile_muceni": {
        "nazev": "Pokročilé mučení",
        "popis": "Zvyšuje efektivitu trestů o 30%.",
        "cena": 700,
        "efekt": lambda hrac: setattr(hrac, 'skilly', {**hrac.skilly, 'dominance': hrac.skilly.get('dominance', 0) + 5}),
        "vyzaduje": ["psychologie_zlomeni"]
    },
}

class VyzkumSystem:
    def __init__(self):
        self.ziskane = set()

    def muzes_vyzkoumat(self, hrac, id_vyzkumu):
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
            return

        vyzkum = VYZKUM[id_vyzkumu]
        hrac.gold -= vyzkum["cena"]
        vyzkum["efekt"](hrac)
        self.ziskane.add(id_vyzkumu)
        tisk_ok(f"Vyzkoumáno: {vyzkum['nazev']}")

    def zobraz_vyzkum(self, hrac):
        clear()
        print("--- Výzkum ---")
        for id_vyzkumu, vyzkum in VYZKUM.items():
            status = "✔" if id_vyzkumu in self.ziskane else "✖"
            print(f"{status} {vyzkum['nazev']} (cena: {vyzkum['cena']})")
            print(f"   {vyzkum['popis']}")
            if vyzkum["vyzaduje"]:
                poz = ", ".join([VYZKUM[p]["nazev"] for p in vyzkum["vyzaduje"]])
                print(f"   Požaduje: {poz}")
        print()

    def to_dict(self):
        return {"ziskane": list(self.ziskane)}

    @classmethod
    def from_dict(cls, data):
        v = cls()
        v.ziskane = set(data.get("ziskane", []))
        return v
