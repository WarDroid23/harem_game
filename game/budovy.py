# game/budovy.py
from utils.vypis import clear, tisk_ok, tisk_chyba
from config import GOLD, GREEN, RED, NC
from models.building import Building


def vylepsit_budovu(hrac, harem, typ):
    """Vylepší budovu bez menu, pokud je typ a cena dostupná."""
    budova = harem.budovy.get(typ)
    if budova is None or hrac.gold < budova.cena:
        return False
    cena = budova.cena
    hrac.gold -= cena
    budova.vylepsi()
    tisk_ok(f"Budova {typ} vylepšena na úroveň {budova.uroven}.")
    return True


def spravovat_budovy(hrac, harem):
    clear()
    print(f"{GOLD}--- Vylepšení harému ---{NC}\n")
    print(f"Úroveň harému: {harem.harem_level}")
    print(f"Zlato: {hrac.gold} 🪙\n")

    for typ, budova in harem.budovy.items():
        info = Building.TYPY[typ]
        print(f"{typ}: {info['nazev']} (úroveň {budova.uroven}) - cena vylepšení: {budova.cena} zlaťáků")
        if typ == "lazne":
            efekt = f"+{budova.uroven * 2} HP denně pro otrokyně"
        elif typ == "cviciste":
            efekt = f"+{budova.uroven * 1} poslušnost trénink"
        elif typ == "dungeon":
            efekt = f"+{budova.uroven * 3} efektivita trestů"
        elif typ == "dungeon2":
            efekt = f"+{budova.uroven * 5} efektivita extrémních trestů"
        elif typ == "oltar":
            efekt = f"+{budova.uroven * 2} temná energie denně"
        elif typ == "oltar_bolesti":
            efekt = f"+{budova.uroven * 4} broken přírůstek"
        elif typ == "jama":
            efekt = f"+{budova.uroven * 2} humiliation přírůstek"
        elif typ == "ukryt":
            efekt = f"-{budova.uroven * 5}% riziko inkvizice"
        elif typ == "tunel":
            efekt = f"+{budova.uroven * 3} pasivní příjem"
        else:
            efekt = "žádný"
        print(f"   Efekt: {efekt}")

    print("\n1) Vylepšit budovu")
    print("0) Zpět")
    volba = input("> ").strip()

    if volba == "1":
        typ = input("Zadej typ budovy: ").strip().lower()
        if typ in harem.budovy:
            budova = harem.budovy[typ]
            if not vylepsit_budovu(hrac, harem, typ):
                tisk_chyba("Nedostatek zlata.")
        else:
            tisk_chyba("Neplatný typ budovy.")
    input("Enter...")
