# game/questy.py
import random
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, GREEN, RED, CYAN, NC

QUESTY = [
    {
        "nazev": "Přepadni karavanu",
        "popis": "Potřebuješ uloupit zboží z obchodní karavany.",
        "typ": "boj",
        "narocnost": 3,
        "odmena_zlato": 200,
        "riziko": 0.3,
        "doba_trvani": 1
    },
    {
        "nazev": "Získej vliv v přístavu",
        "popis": "Podplať přístavní stráž.",
        "typ": "diplomacie",
        "narocnost": 4,
        "odmena_zlato": 150,
        "riziko": 0.2,
        "doba_trvani": 2
    },
    {
        "nazev": "Unes šlechtičnu",
        "popis": "Elitní únos z města.",
        "typ": "lov",
        "narocnost": 6,
        "odmena_zlato": 350,
        "riziko": 0.4,
        "doba_trvani": 2
    },
    {
        "nazev": "Obchod s otroky",
        "popis": "Prodej otrokyň do vzdálených zemí.",
        "typ": "obchod",
        "narocnost": 2,
        "odmena_zlato": 100,
        "riziko": 0.1,
        "doba_trvani": 1
    }
]

class QuestSystem:
    def __init__(self):
        self.aktivni_quest = None
        self.dny_zbyva = 0
        self.dokonceno = 0

    def generuj_quest(self, hrac):
        if self.aktivni_quest is not None:
            return
        vhodne = [q for q in QUESTY if q["narocnost"] <= hrac.level + 1]
        if not vhodne:
            vhodne = QUESTY
        quest = random.choice(vhodne)
        self.aktivni_quest = quest
        self.dny_zbyva = quest["doba_trvani"]
        print(f"{GOLD}Nový quest: {quest['nazev']}{NC}")
        print(f"Popis: {quest['popis']}")
        print(f"Odměna: {quest['odmena_zlato']} zlaťáků, riziko: {int(quest['riziko']*100)}%")

    def proved_quest(self, hrac, harem, mafie):
        if self.aktivni_quest is None:
            tisk_chyba("Nemáš aktivní quest.")
            return

        quest = self.aktivni_quest
        self.dny_zbyva -= 1

        if self.dny_zbyva > 0:
            tisk_info(f"Quest '{quest['nazev']}' pokračuje. Zbývá dní: {self.dny_zbyva}")
            return

        uspech = random.random() > quest["riziko"]

        if uspech:
            hrac.gold += quest["odmena_zlato"]
            hrac.pridej_xp(20 + quest["narocnost"] * 10)
            if quest["typ"] == "lov":
                from models.otrokyne import Otrokyně
                from data.jmena import JMENA
                otrok = Otrokyně(
                    jmeno=random.choice(JMENA),
                    submisivita=random.randint(30, 80),
                    poslusnost=random.randint(20, 70),
                    loajalita=random.randint(10, 50)
                )
                harem.pridat(otrok)
                print(f"{GREEN}Získal jsi otrokyni {otrok.jmeno}!{NC}")
            tisk_ok(f"Quest '{quest['nazev']}' dokončen! Odměna: {quest['odmena_zlato']} zlaťáků, +20 XP.")
        else:
            pokuta = int(quest["odmena_zlato"] * 0.5)
            hrac.gold = max(0, hrac.gold - pokuta)
            hrac.vliv_inkvizice = min(100, hrac.vliv_inkvizice + 5)
            tisk_chyba(f"Quest '{quest['nazev']}' selhal! Ztratil jsi {pokuta} zlaťáků.")

        self.aktivni_quest = None
        self.dokonceno += 1

    def zobraz_questy(self):
        clear()
        print(f"{GOLD}--- Questy ---{NC}")
        if self.aktivni_quest:
            q = self.aktivni_quest
            print(f"Aktivní quest: {q['nazev']}")
            print(f"Popis: {q['popis']}")
            print(f"Zbývá dní: {self.dny_zbyva}")
            print(f"Odměna: {q['odmena_zlato']} zlaťáků, riziko: {int(q['riziko']*100)}%\n")
        else:
            print("Nemáš žádný aktivní quest.\n")
        print(f"Dokončeno questů: {self.dokonceno}")
        print("\n1) Generovat nový quest")
        print("2) Plnit quest")
        print("0) Zpět")
        volba = input("> ").strip()
        return volba

    def to_dict(self):
        return {
            "aktivni_quest": self.aktivni_quest,
            "dny_zbyva": self.dny_zbyva,
            "dokonceno": self.dokonceno
        }

    @classmethod
    def from_dict(cls, data):
        q = cls()
        q.aktivni_quest = data.get("aktivni_quest")
        q.dny_zbyva = data.get("dny_zbyva", 0)
        q.dokonceno = data.get("dokonceno", 0)
        return q
