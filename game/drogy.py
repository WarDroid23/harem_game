# game/drogy.py
import random
from data.drogy import DROGY
from data.charaktery import CHARAKTERY
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GREEN, RED, CYAN, MAGENTA, GOLD, NC

def podat_drogu(otrok, hrac, id_drogy):
    if id_drogy not in DROGY:
        tisk_chyba("Neznámá droga.")
        return False

    droga = DROGY[id_drogy]

    if hrac.gold < droga["cena"]:
        tisk_chyba("Nemáš dostatek zlata na nákup drogy.")
        return False

    hrac.gold -= droga["cena"]

    for stat, hodnota in droga["efekty"].items():
        otrok.zvysit_stat(stat, hodnota)

    for stat, hodnota in droga["trvale_nasledky"].items():
        otrok.zvysit_stat(stat, hodnota)

    if otrok.typ_zavislosti is None or otrok.zavislost < 10:
        otrok.typ_zavislosti = id_drogy

    if random.random() < droga["riziko_predavkovani"]:
        otrok.predavkovani = True
        otrok.hp = max(0, otrok.hp - random.randint(20, 50))
        tisk_chyba(f"{otrok.jmeno} se předávkovala! HP: {otrok.hp}.")
        return True

    if otrok.zavislost > 70:
        otrok.abstinenco_priznaky = True
        tisk_chyba(f"{otrok.jmeno} trpí abstinenčními příznaky!")

    otrok.aktualizuj_fazi()
    tisk_ok(f"Droga {droga['nazev']} podána {otrok.jmeno}. Závislost: {otrok.zavislost}%.")
    return True

def spravovat_odvykani(otrok, hrac):
    if otrok.zavislost <= 0:
        tisk_info(f"{otrok.jmeno} není závislá.")
        return

    if hrac.sex_energy < 20:
        tisk_chyba("Nedostatek sexuální energie pro péči o otrokyni.")
        return
    hrac.sex_energy -= 20

    sance_uspech = 0.8 - (otrok.zavislost / 150)
    if otrok.abstinenco_priznaky:
        sance_uspech -= 0.15

    if random.random() < sance_uspech:
        otrok.zavislost = max(0, otrok.zavislost - random.randint(20, 40))
        otrok.abstinenco_priznaky = False
        if otrok.zavislost <= 0:
            otrok.typ_zavislosti = None
        tisk_ok(f"Odvykání úspěšné. Závislost: {otrok.zavislost}%.")
    else:
        otrok.zavislost = min(100, otrok.zavislost + 5)
        otrok.abstinenco_priznaky = True
        tisk_chyba(f"Odvykání selhalo. Závislost stoupla na {otrok.zavislost}%.")

def zobraz_stav(otrok):
    print(f"\n{MAGENTA}Stav drog u {otrok.jmeno}:{NC}")
    if otrok.zavislost > 0:
        nazev = DROGY.get(otrok.typ_zavislosti, {}).get("nazev", "neznámá")
        print(f"  Závislost na: {nazev} ({otrok.zavislost}%)")
        if otrok.abstinenco_priznaky:
            print(f"  {RED}Abstinenční příznaky aktivní{NC}")
        if otrok.predavkovani:
            print(f"  {RED}Předávkování!{NC}")
    else:
        print("  Žádná závislost.")
    print(f"  HP: {otrok.hp}/{otrok.max_hp} | Broken: {otrok.broken} | Mindbreak: {otrok.mindbreak}")

def menu_drog(otrok, hrac):
    while True:
        clear()
        print(f"{MAGENTA}--- Drogy pro {otrok.jmeno} ---{NC}\n")
        zobraz_stav(otrok)
        print("\n1) Podat drogu")
        print("2) Odvykání")
        print("0) Zpět")
        volba = input("> ").strip()
        if volba == "1":
            print("\nDostupné drogy:")
            for id_drogy, droga in DROGY.items():
                print(f"{id_drogy}: {droga['nazev']} – cena {droga['cena']} zlaťáků")
                print(f"   {droga['popis']}")
            volba_droga = input("\nZadej ID drogy: ").strip().lower()
            if volba_droga in DROGY:
                podat_drogu(otrok, hrac, volba_droga)
            else:
                tisk_chyba("Neznámá droga.")
            input("Enter...")
        elif volba == "2":
            spravovat_odvykani(otrok, hrac)
            input("Enter...")
        elif volba == "0":
            break
