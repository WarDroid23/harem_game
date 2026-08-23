# game/lov.py
import random
from models.otrokyne import Otrokyně
from data.jmena import JMENA
from data.charaktery import CHARAKTERY
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import RED, GREEN, CYAN, MAGENTA, GOLD, NC
from game.alchymie import SUROVINY

LOV_OBLASTI = [
    {
        "nazev": "Vesnice",
        "popis": "Poklidná oblast, ale málo kvalitní otrokyně.",
        "sance": 0.7,
        "kvalita": (1, 3),
        "cena_energie": 10,
        "emodži": "🏡",
        "specialni_sance": 0.1
    },
    {
        "nazev": "Přístav",
        "popis": "Různé otrokyně z celého světa.",
        "sance": 0.55,
        "kvalita": (2, 5),
        "cena_energie": 20,
        "emodži": "⚓",
        "specialni_sance": 0.2
    },
    {
        "nazev": "Karavana",
        "popis": "Obchodníci s otroky, dobrá kvalita.",
        "sance": 0.45,
        "kvalita": (3, 6),
        "cena_energie": 30,
        "emodži": "🐪",
        "specialni_sance": 0.25
    },
    {
        "nazev": "Šlechtické sídlo",
        "popis": "Elitní otrokyně, ale vysoké riziko.",
        "sance": 0.3,
        "kvalita": (5, 8),
        "cena_energie": 50,
        "emodži": "🏰",
        "specialni_sance": 0.4
    },
    {
        "nazev": "Banditský tábor",
        "popis": "Nebezpečné, ale otrokyně zdarma.",
        "sance": 0.25,
        "kvalita": (2, 6),
        "cena_energie": 40,
        "emodži": "🏕️",
        "specialni_sance": 0.35
    },
    {
        "nazev": "Otrocký trh",
        "popis": "Legální nákup otrokyň, nízké riziko.",
        "sance": 0.65,
        "kvalita": (3, 7),
        "cena_energie": 35,
        "emodži": "🏪",
        "specialni_sance": 0.15
    },
    {
        "nazev": "Chrám temnoty",
        "popis": "Kultisté nabízejí temné otrokyně.",
        "sance": 0.4,
        "kvalita": (4, 9),
        "cena_energie": 60,
        "emodži": "⛩️",
        "specialni_sance": 0.5
    },
]

SPECIALNI_UDALOSTI_LOV = [
    {
        "nazev": "Poklad",
        "popis": "Našel jsi truhlu se zlaťáky.",
        "efekt": lambda h: setattr(h, 'gold', h.gold + random.randint(20, 80))
    },
    {
        "nazev": "Surovina",
        "popis": "Našel jsi vzácnou surovinu.",
        "efekt": lambda h, alchymie: alchymie.pridat_surovinu(random.choice(list(SUROVINY.keys())), 1) if alchymie else None
    },
    {
        "nazev": "Přepadení",
        "popis": "Byli jste přepadeni!",
        "efekt": lambda h: (setattr(h, 'hp', max(1, h.hp - random.randint(5, 20))), setattr(h, 'gold', max(0, h.gold - random.randint(10, 40))))
    },
    {
        "nazev": "Inkvizice",
        "popis": "Inkvizice vás zahlédla.",
        "efekt": lambda h: setattr(h, 'vliv_inkvizice', min(100, h.vliv_inkvizice + random.randint(2, 8)))
    },
]

def lov_otrokyn(hra):
    hrac = hra.hrac
    clear()
    print(f"{GOLD}{'='*50}{NC}")
    print(f"{MAGENTA}🎯 LOV OTROKYŇ{NC}")
    print(f"{GOLD}{'='*50}{NC}\n")

    if hrac.sex_energy < 10:
        tisk_chyba("Nemáš dostatek energie na lov (min. 10).")
        input("Enter...")
        return None

    print("Vyber oblast lovu:\n")
    for i, oblast in enumerate(LOV_OBLASTI, 1):
        print(f"{i}) {oblast['emodži']} {oblast['nazev']} - {oblast['popis']}")
        print(f"   Šance: {int(oblast['sance']*100)}% | Kvalita: {oblast['kvalita'][0]}-{oblast['kvalita'][1]} | Energie: {oblast['cena_energie']} | Zvláštní událost: {int(oblast['specialni_sance']*100)}%\n")

    volba = input("> ").strip()
    try:
        idx = int(volba) - 1
        if idx < 0 or idx >= len(LOV_OBLASTI):
            tisk_chyba("Špatná volba.")
            input("Enter...")
            return None
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")
        return None

    oblast = LOV_OBLASTI[idx]
    if hrac.sex_energy < oblast["cena_energie"]:
        tisk_chyba(f"Nedostatek energie. Potřebuješ {oblast['cena_energie']}.")
        input("Enter...")
        return None

    hrac.sex_energy -= oblast["cena_energie"]
    print(f"\nVydáváš se do oblasti {oblast['emodži']} {oblast['nazev']}...")

    if random.random() < oblast["specialni_sance"]:
        udalost = random.choice(SPECIALNI_UDALOSTI_LOV)
        print(f"\n⭐ {udalost['popis']}")
        if udalost["nazev"] == "Surovina":
            udalost["efekt"](hrac, hra.alchymie)
        else:
            udalost["efekt"](hrac)
        input("Enter...")

    if random.random() < oblast["sance"]:
        kvalita = random.randint(*oblast["kvalita"])
        jmeno = random.choice(JMENA)
        charakter = random.choice(list(CHARAKTERY.keys()))
        otrok = Otrokyně(
            jmeno=jmeno,
            srdce=min(100, random.randint(40, 90) + kvalita * 5),
            poslusnost=min(100, random.randint(10, 70) + kvalita * 4),
            submisivita=min(100, random.randint(10, 75) + kvalita * 5),
            loajalita=min(100, random.randint(5, 60) + kvalita * 3),
            touha=min(100, random.randint(15, 80) + kvalita * 4),
            broken=random.randint(0, 15),
            hp=random.randint(70, 100),
            charakter=charakter
        )
        hrac.gold += random.randint(10, 50)
        print(f"\n✅ {tisk_ok(f'Úspěch! Chytil jsi otrokyni jménem {jmeno}.')}")
        print(f"   Charakter: {CHARAKTERY[charakter]['nazev']}")
        print(f"   Vlastnosti: submisivita {otrok.submisivita}, poslušnost {otrok.poslusnost}, loajalita {otrok.loajalita}")
        return otrok
    else:
        print(f"\n❌ {tisk_chyba('Lov selhal. Otrokyně utekla.')}")
        return None
