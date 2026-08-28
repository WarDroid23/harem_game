# game/alchymie.py
import random
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, GREEN, RED, CYAN, MAGENTA, NC
from data.drogy import DROGY

SUROVINY = {
    "bylina_mesicni": {"nazev": "Měsíční bylina", "cena": 10},
    "koren_mandragory": {"nazev": "Kořen mandragory", "cena": 25},
    "esence_temna": {"nazev": "Temná esence", "cena": 40},
    "krystal_sily": {"nazev": "Krystal síly", "cena": 35},
    "vzacna_houba": {"nazev": "Vzácná houba", "cena": 50},
    "pelynek": {"nazev": "Pelyněk", "cena": 15},
    "nocni_stin": {"nazev": "Noční stín", "cena": 30},
    "drací_koren": {"nazev": "Dračí kořen", "cena": 70},
}

RECEPTY = {
    "lektvar_energie": {
        "nazev": "Lektvar energie",
        "popis": "Doplní 30 sexuální energie.",
        "suroviny": {"bylina_mesicni": 2, "koren_mandragory": 1},
        "efekt": lambda h: setattr(h, 'sex_energy', min(100, h.sex_energy + 30)),
        "hodnota": 50
    },
    "lektvar_temne_energie": {
        "nazev": "Lektvar temné energie",
        "popis": "Doplní 20 temné energie.",
        "suroviny": {"esence_temna": 2, "krystal_sily": 1},
        "efekt": lambda h: setattr(h, 'dark_energy', min(100, h.dark_energy + 20)),
        "hodnota": 60
    },
    "lektvar_rovnovahy": {
        "nazev": "Lektvar rovnováhy",
        "popis": "Doplní 18 sexuální i temné energie.",
        "suroviny": {"bylina_mesicni": 1, "esence_temna": 1},
        "efekt": lambda h: (
            setattr(h, 'sex_energy', min(100, h.sex_energy + 18)),
            setattr(h, 'dark_energy', min(100, h.dark_energy + 18))
        ),
        "hodnota": 75
    },
    "lektvar_zdravi": {
        "nazev": "Lektvar zdraví",
        "popis": "Obnoví 50 HP.",
        "suroviny": {"bylina_mesicni": 3, "vzacna_houba": 1},
        "efekt": lambda h: setattr(h, 'hp', min(h.max_hp, h.hp + 50)),
        "hodnota": 40
    },
    "lektvar_dominance": {
        "nazev": "Lektvar dominance",
        "popis": "Zvýší dominanci o 5.",
        "suroviny": {"koren_mandragory": 2, "krystal_sily": 2, "esence_temna": 1},
        "efekt": lambda h: setattr(h, 'dominance', h.dominance + 5),
        "hodnota": 100
    },
    "lektvar_poslusnosti": {
        "nazev": "Lektvar poslušnosti",
        "popis": "Všem otrokyním +10 poslušnosti.",
        "suroviny": {"bylina_mesicni": 2, "vzacna_houba": 2},
        "efekt": lambda h, harem: [o.zvysit_stat('poslusnost', 10) for o in harem.otrokyne],
        "hodnota": 120
    },
}

# Přidání drog do receptů
for id_drogy, droga in DROGY.items():
    RECEPTY[id_drogy] = {
        "nazev": f"Výroba: {droga['nazev']}",
        "popis": droga["popis"],
        "suroviny": droga["suroviny"],
        "efekt": lambda h, id_drogy=id_drogy: None,
        "hodnota": droga["cena"]
    }

class AlchymieSystem:
    def __init__(self):
        self.suroviny = {}
        self.recepty_objevene = set(RECEPTY.keys())

    def pridat_surovinu(self, id_suroviny, mnozstvi=1):
        if id_suroviny not in SUROVINY:
            return False
        if id_suroviny not in self.suroviny:
            self.suroviny[id_suroviny] = 0
        self.suroviny[id_suroviny] += mnozstvi
        return True

    def odeber_surovinu(self, id_suroviny, mnozstvi=1):
        if id_suroviny not in self.suroviny or self.suroviny[id_suroviny] < mnozstvi:
            return False
        self.suroviny[id_suroviny] -= mnozstvi
        return True

    def muzes_vyrobit(self, id_receptu):
        if id_receptu not in RECEPTY:
            return False, "Neznámý recept."
        recept = RECEPTY[id_receptu]
        for surovina, mnozstvi in recept["suroviny"].items():
            if self.suroviny.get(surovina, 0) < mnozstvi:
                return False, f"Nedostatek suroviny: {SUROVINY[surovina]['nazev']} (potřeba {mnozstvi})."
        return True, ""

    def vyrobit(self, hrac, harem, id_receptu):
        mozne, duvod = self.muzes_vyrobit(id_receptu)
        if not mozne:
            tisk_chyba(duvod)
            return False

        recept = RECEPTY[id_receptu]
        for surovina, mnozstvi in recept["suroviny"].items():
            self.odeber_surovinu(surovina, mnozstvi)

        if id_receptu == "lektvar_poslusnosti":
            recept["efekt"](hrac, harem)
        else:
            recept["efekt"](hrac)

        tisk_ok(f"Vyroben lektvar: {recept['nazev']}.")
        return True

    def zobraz_menu(self, hrac, harem):
        clear()
        print(f"{MAGENTA}--- Alchymie ---{NC}\n")
        print("Suroviny:")
        for id_su, nazev in SUROVINY.items():
            pocet = self.suroviny.get(id_su, 0)
            print(f"  {nazev}: {pocet} ks")

        print("\nRecepty:")
        for i, (id_rec, recept) in enumerate(RECEPTY.items(), 1):
            print(f"{i}) {recept['nazev']} – {recept['popis']}")
            suroviny_popis = ", ".join([f"{SUROVINY[s]['nazev']} x{m}" for s, m in recept['suroviny'].items()])
            print(f"   Suroviny: {suroviny_popis}")

        print("\n1) Vyrobit lektvar")
        print("2) Koupit surovinu")
        print("0) Zpět")
        volba = input("> ").strip()

        if volba == "1":
            try:
                idx = int(input("Číslo receptu: ")) - 1
                if 0 <= idx < len(RECEPTY):
                    id_rec = list(RECEPTY.keys())[idx]
                    self.vyrobit(hrac, harem, id_rec)
                else:
                    tisk_chyba("Špatné číslo.")
            except ValueError:
                tisk_chyba("Zadej číslo.")
        elif volba == "2":
            print("\nDostupné suroviny:")
            for i, (id_su, su) in enumerate(SUROVINY.items(), 1):
                print(f"{i}) {su['nazev']} – {su['cena']} zlaťáků")
            try:
                idx = int(input("Vyber surovinu: ")) - 1
                if 0 <= idx < len(SUROVINY):
                    id_su = list(SUROVINY.keys())[idx]
                    cena = SUROVINY[id_su]["cena"]
                    if hrac.gold >= cena:
                        hrac.gold -= cena
                        self.pridat_surovinu(id_su, 1)
                        tisk_ok(f"Koupena surovina {SUROVINY[id_su]['nazev']}.")
                    else:
                        tisk_chyba("Nedostatek zlata.")
            except ValueError:
                tisk_chyba("Zadej číslo.")
        input("Enter...")

    def to_dict(self):
        return {
            "suroviny": self.suroviny,
            "recepty_objevene": list(self.recepty_objevene)
        }

    @classmethod
    def from_dict(cls, data):
        a = cls()
        a.suroviny = data.get("suroviny", {})
        a.recepty_objevene = set(data.get("recepty_objevene", []))
        return a
