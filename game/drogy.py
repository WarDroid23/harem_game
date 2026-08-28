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

def podpora_zotaveni(otrok, hrac):
    """Nabídne několik neinvazivních cest zotavení bez podávání další drogy."""
    if otrok.zavislost <= 0:
        tisk_info(f"{otrok.jmeno} nyní nepotřebuje léčbu závislosti.")
        return
    print("\nMožnosti podpory zotavení:")
    print("1) Léčitel a bezpečný detox (50 zlata, -25 závislosti)")
    print("2) Klidový program (zdarma, -10 závislosti, +důvěra)")
    print("3) Podpůrná skupina (20 zlata, -15 závislosti, +loajalita)")
    volba = input("> ").strip()
    ceny = {"1": 50, "2": 0, "3": 20}
    snizeni = {"1": 25, "2": 10, "3": 15}
    if volba not in ceny:
        tisk_chyba("Neplatná volba.")
        return
    if hrac.gold < ceny[volba]:
        tisk_chyba("Nemáš dost zlata na tuto formu podpory.")
        return
    hrac.gold -= ceny[volba]
    otrok.zavislost = max(0, otrok.zavislost - snizeni[volba])
    otrok.lecba_zavislosti = min(100, otrok.lecba_zavislosti + snizeni[volba])
    otrok.abstinenco_priznaky = otrok.zavislost > 0
    if volba == "1":
        otrok.zvysit_stat("hp", 15)
        tisk_ok(f"Léčitel provedl bezpečný detox. Závislost: {otrok.zavislost}%.")
    elif volba == "2":
        otrok.zvysit_stat("duvera", 5)
        tisk_ok(f"{otrok.jmeno} dostala prostor k zotavení. Závislost: {otrok.zavislost}%.")
    else:
        otrok.zvysit_stat("loajalita", 4)
        tisk_ok(f"Podpůrná skupina pomohla. Závislost: {otrok.zavislost}%.")
    if otrok.zavislost == 0:
        otrok.typ_zavislosti = None
        otrok.abstinenco_priznaky = False
        tisk_ok("Závislost je překonána; další péče pomáhá udržet zotavení.")

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
        print("3) Podpora zotavení")
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
        elif volba == "3":
            podpora_zotaveni(otrok, hrac)
            input("Enter...")
        elif volba == "0":
            break
