# game/vyvoj.py
from models.hrac import Hrac
from utils.vypis import clear, tisk_ok, tisk_chyba
from data.zbrane import ZBRANE
from models.inventory import Zbran

def zobraz_vyvoj(hrac: Hrac):
    clear()
    print("--- Vývoj postavy ---")
    print(f"Level: {hrac.level} (XP: {hrac.xp}/{hrac.xp_next})")
    print(f"Zlato: {hrac.gold} | Energie: {hrac.sex_energy} | Temná energie: {hrac.dark_energy}")
    print("\nDovednosti:")
    for skill, hodnota in hrac.skilly.items():
        print(f"{skill}: {hodnota}")
    print("\n1) Trénovat dovednost (1 bod za 100 zlaťáků)")
    print("2) Koupit zbraň")
    print("0) Zpět")
    volba = input("> ")
    if volba == "1":
        print("Dostupné dovednosti:")
        for i, skill in enumerate(hrac.skilly, 1):
            print(f"{i}) {skill}")
        try:
            idx = int(input("Vyber dovednost: ")) - 1
            if 0 <= idx < len(hrac.skilly):
                if hrac.gold >= 100:
                    hrac.gold -= 100
                    skill_name = list(hrac.skilly.keys())[idx]
                    hrac.skilly[skill_name] += 1
                    tisk_ok(f"Dovednost {skill_name} zvýšena na {hrac.skilly[skill_name]}.")
                else:
                    tisk_chyba("Nedostatek zlata.")
        except ValueError:
            tisk_chyba("Špatná volba.")
    elif volba == "2":
        print("Dostupné zbraně:")
        for i, z in enumerate(ZBRANE, 1):
            print(f"{i}) {z['nazev']} (typ: {z['typ']}, cena: {z['cena']}, poškození: {z['poskozeni']})")
        try:
            idx = int(input("Vyber zbraň: ")) - 1
            if 0 <= idx < len(ZBRANE):
                z_data = ZBRANE[idx]
                if hrac.gold >= z_data["cena"]:
                    hrac.gold -= z_data["cena"]
                    nova_zbran = Zbran(**z_data)
                    hrac.inventar.pridej_zbran(nova_zbran)
                    tisk_ok(f"Koupena zbraň {nova_zbran.nazev}.")
                else:
                    tisk_chyba("Nedostatek zlata.")
        except ValueError:
            tisk_chyba("Špatná volba.")
    input("Enter...")
