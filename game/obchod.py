# game/obchod.py
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, GREEN, CYAN, MAGENTA, RED, NC
from models.agent import Agent
from data.jmena import JMENA_AGENTU
from game.balance import uprav_cenu
import random

def obchod(hra):
    hrac = hra.hrac
    clear()
    print(f"{GOLD}--- Obchod ---{NC}\n")
    print(f"{GREEN}Zlato: {hrac.gold} 🪙{NC}\n")

    polozky = [
        {"id": "lektvar_sex", "nazev": "Lektvar sexuální energie", "cena": 50,
         "popis": "Doplní 30 sexuální energie.",
         "efekt": lambda h: setattr(h, 'sex_energy', min(100, h.sex_energy + 30))},
        {"id": "lektvar_temno", "nazev": "Lektvar temné energie", "cena": 60,
         "popis": "Doplní 20 temné energie.",
         "efekt": lambda h: setattr(h, 'dark_energy', min(100, h.dark_energy + 20))},
        {"id": "lektvar_hp", "nazev": "Lektvar zdraví", "cena": 40,
         "popis": "Obnoví 50 HP.",
         "efekt": lambda h: setattr(h, 'hp', min(h.max_hp, h.hp + 50))},
        {"id": "lektvar_dom", "nazev": "Lektvar dominance", "cena": 100,
         "popis": "Zvýší dominanci o 5.",
         "efekt": lambda h: setattr(h, 'dominance', h.dominance + 5)},
        {"id": "obojky", "nazev": "Obojky poslušnosti", "cena": 300,
         "popis": "Všem otrokyním +10 poslušnosti.",
         "efekt": lambda h, harem: [o.zvysit_stat('poslusnost', 10) for o in harem.otrokyne]},
        {"id": "vycvik_sub", "nazev": "Výcvik submisivity", "cena": 400,
         "popis": "Všem otrokyním +8 submisivity.",
         "efekt": lambda h, harem: [o.zvysit_stat('submisivita', 8) for o in harem.otrokyne]},
        {"id": "psycho_prirucka", "nazev": "Psychologická příručka", "cena": 500,
         "popis": "Všem otrokyním +5 broken.",
         "efekt": lambda h, harem: [o.zvysit_stat('broken', 5) for o in harem.otrokyne]},
        {"id": "uplatek_inkvizici", "nazev": "Úplatek inkvizici", "cena": 200,
         "popis": "Sníží vliv inkvizice o 10.",
         "efekt": lambda h: setattr(h, 'vliv_inkvizice', max(0, h.vliv_inkvizice - 10))},
        {"id": "najem_spiona", "nazev": "Najmout špiona", "cena": 150,
         "popis": "Přidá nového agenta (pokud je místo).",
         "efekt": lambda h: pridat_agenta(h)},
        {"id": "mapa_podsveti", "nazev": "Mapa podsvětí", "cena": 250,
         "popis": "Zvýší vliv ve městě o 5.",
         "efekt": lambda h, mafie: setattr(mafie, 'vliv_ve_meste', min(100, mafie.vliv_ve_meste + 5))},
        {"id": "trenink_boje", "nazev": "Trénink boje", "cena": 200,
         "popis": "Zvýší dovednost boj o 3.",
         "efekt": lambda h: h.skilly.update({'boj': h.skilly.get('boj', 0) + 3})},
    ]

    obtiznost = getattr(getattr(hra, "nastaveni", None), "obtiznost", "normalni")
    ceny = [uprav_cenu(p["cena"], obtiznost) for p in polozky]
    for i, (p, cena) in enumerate(zip(polozky, ceny), 1):
        print(f"{i}) {p['nazev']} – {p['popis']} ({cena} 🪙)")

    print("\n0) Zpět")
    volba = input("> ").strip()

    if volba == "0":
        return

    try:
        idx = int(volba) - 1
        if idx < 0 or idx >= len(polozky):
            tisk_chyba("Špatná volba.")
            input("Enter...")
            return
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")
        return

    polozka = polozky[idx]
    if polozka["id"] == "najem_spiona" and len(hrac.agenti) >= hrac.max_agentu:
        tisk_chyba("Nemáš volné místo pro agenta.")
        input("Enter...")
        return
    cena = ceny[idx]
    if hrac.gold < cena:
        tisk_chyba("Nedostatek zlata.")
        input("Enter...")
        return

    hrac.gold -= cena

    if polozka["id"] in ["obojky", "vycvik_sub", "psycho_prirucka"]:
        polozka["efekt"](hrac, hra.harem)
    elif polozka["id"] == "mapa_podsveti":
        polozka["efekt"](hrac, hra.mafie)
    elif polozka["id"] == "najem_spiona":
        polozka["efekt"](hrac)
    else:
        polozka["efekt"](hrac)

    tisk_ok(f"Koupeno: {polozka['nazev']}.")
    input("Enter...")

def pridat_agenta(hrac):
    if len(hrac.agenti) >= hrac.max_agentu:
        return False
    jmeno = random.choice(JMENA_AGENTU)
    agent = Agent(jmeno, specializace="spion")
    hrac.agenti.append(agent)
    return True
