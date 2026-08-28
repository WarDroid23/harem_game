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
    },
    {
        "nazev": "Zpráva pro Miru",
        "popis": "Doruč léčitelce zprávu o bezpečné cestě pro její pacienty.",
        "typ": "npc",
        "lokace": "trh",
        "npc_id": "mira",
        "narocnost": 2,
        "odmena_zlato": 90,
        "odmena_predmet": "zdravotni_balicek",
        "riziko": 0.1,
        "doba_trvani": 1
    },
    {
        "nazev": "Pomoc na hranici",
        "popis": "Dovez zásoby do hraniční vesnice dřív, než dorazí další nájezdníci.",
        "typ": "pomoc",
        "lokace": "hranice",
        "narocnost": 5,
        "odmena_zlato": 260,
        "odmena_predmet": "signalni_roh",
        "riziko": 0.25,
        "doba_trvani": 2
    },
    {
        "nazev": "Mapa pro Lyru",
        "popis": "Dones Lyře záznamy z akademie a pomoz jí zakreslit bezpečnou cestu zahradou.",
        "typ": "npc",
        "lokace": "sklenena_zahrada",
        "npc_id": "lyra",
        "narocnost": 4,
        "odmena_zlato": 180,
        "odmena_predmet": "mapa_hvezd",
        "odmena_energie": {"sex": 12, "temna": 8},
        "riziko": 0.15,
        "doba_trvani": 1
    },
    {
        "nazev": "Archiv bez řetězů",
        "popis": "Pomoz Cassianovi zabezpečit archiv tak, aby znalosti sloužily lidem, ne nátlaku.",
        "typ": "pomoc",
        "lokace": "observator",
        "npc_id": "cassian",
        "narocnost": 6,
        "odmena_zlato": 300,
        "odmena_predmet": "klic_observatore",
        "riziko": 0.25,
        "doba_trvani": 2
    },
    {
        "nazev": "Světla na molu",
        "popis": "Pomoz Tereze připravit noční odplutí pro dospělé uprchlíky, kteří si vybrali vlastní cestu.",
        "typ": "pomoc",
        "lokace": "molo_mesicniho_pristavu",
        "npc_id": "tereza",
        "narocnost": 7,
        "odmena_zlato": 420,
        "odmena_predmet": "mesicni_kompas",
        "odmena_energie": {"sex": 8, "temna": 18},
        "riziko": 0.3,
        "doba_trvani": 2
    }
]

class QuestSystem:
    def __init__(self):
        self.aktivni_quest = None
        self.dny_zbyva = 0
        self.dokonceno = 0

    def generuj_quest(self, hrac, hra=None):
        if self.aktivni_quest is not None:
            return
        dostupne = QUESTY
        if hra is not None and hasattr(hra, "svet"):
            dostupne = [
                q for q in QUESTY
                if not q.get("lokace") or q["lokace"] in hra.svet.odhalene_lokace
            ]
        vhodne = [q for q in dostupne if q["narocnost"] <= hrac.level + 1]
        if not vhodne:
            vhodne = dostupne or QUESTY
        quest = random.choice(vhodne)
        self.aktivni_quest = quest
        self.dny_zbyva = quest["doba_trvani"]
        print(f"{GOLD}Nový quest: {quest['nazev']}{NC}")
        print(f"Popis: {quest['popis']}")
        print(f"Odměna: {quest['odmena_zlato']} zlaťáků, riziko: {int(quest['riziko']*100)}%")

    def proved_quest(self, hrac, harem, mafie, hra=None):
        if self.aktivni_quest is None:
            tisk_chyba("Nemáš aktivní quest.")
            return

        quest = self.aktivni_quest
        lokace = quest.get("lokace")
        if lokace and hra is not None and hra.svet.aktualni_lokace != lokace:
            tisk_chyba("Quest musíš plnit v lokaci: " + lokace)
            return
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
            if quest.get("odmena_predmet"):
                hrac.inventar.pridej_predmet(quest["odmena_predmet"])
            energie = quest.get("odmena_energie", {})
            if isinstance(energie, dict):
                hrac.sex_energy = min(100, hrac.sex_energy + max(0, int(energie.get("sex", 0))))
                hrac.dark_energy = min(100, hrac.dark_energy + max(0, int(energie.get("temna", 0))))
            if quest.get("npc_id") and hra is not None and hasattr(hra, "svet"):
                hra.svet.zmen_vztah(quest["npc_id"], 8)
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
        if not isinstance(data, dict):
            return q
        q.aktivni_quest = data.get("aktivni_quest") if isinstance(data.get("aktivni_quest"), dict) else None
        q.dny_zbyva = max(0, int(data.get("dny_zbyva", 0)))
        q.dokonceno = max(0, int(data.get("dokonceno", 0)))
        return q
