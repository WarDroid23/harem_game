"""Doplňkové způsoby obnovy energií hráče."""

from config import CYAN, GOLD, GREEN, MAGENTA, NC
from utils.vypis import clear, tisk_chyba, tisk_info, tisk_ok


def _max_pro(hrac, atribut):
    if atribut == "sex_energy":
        return hrac.max_sex() if hasattr(hrac, "max_sex") else getattr(hrac, "max_sex_energy", 100)
    if atribut == "dark_energy":
        return hrac.max_temno() if hasattr(hrac, "max_temno") else getattr(hrac, "max_dark_energy", 100)
    return 100


def _zbyva(hrac, atribut):
    return max(0, _max_pro(hrac, atribut) - getattr(hrac, atribut))


def _lze_pouzit(hrac, akce_id):
    if hrac.dobiti_dnes.get(akce_id, 0):
        tisk_info("Tuto možnost jsi dnes už využil. Zkus to znovu po odpočinku.")
        return False
    return True


def _oznac_pouziti(hrac, akce_id):
    hrac.dobiti_dnes[akce_id] = hrac.dobiti_dnes.get(akce_id, 0) + 1


def hostinec(hra):
    hrac = hra.hrac
    cena = 35
    if hrac.gold < cena:
        tisk_chyba("Na nocleh v hostinci nemáš dost zlata.")
        return False
    if not _lze_pouzit(hrac, "hostinec"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.gold -= cena
    hrac.sex_energy = min(_max_pro(hrac, "sex_energy"), hrac.sex_energy + 28)
    hrac.dark_energy = min(_max_pro(hrac, "dark_energy"), hrac.dark_energy + 8)
    hrac.hp = min(hrac.max_hp, hrac.hp + 10)
    _oznac_pouziti(hrac, "hostinec")
    tisk_ok("Hostinský ti naservíroval vydatné jídlo. Sexuální energie +28, temná +8.")
    return True


def lazne(hra):
    hrac = hra.hrac
    cena = 60
    if hrac.gold < cena:
        tisk_chyba("Lázně jsou teď mimo tvůj rozpočet.")
        return False
    if not _lze_pouzit(hrac, "lazne"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.gold -= cena
    hrac.sex_energy = min(_max_pro(hrac, "sex_energy"), hrac.sex_energy + 20)
    hrac.dark_energy = min(_max_pro(hrac, "dark_energy"), hrac.dark_energy + 22)
    hrac.hp = min(hrac.max_hp, hrac.hp + 15)
    _oznac_pouziti(hrac, "lazne")
    tisk_ok("Lázně uvolnily tělo. Sexuální +20, temná +22.")
    return True


def meditace(hra):
    hrac = hra.hrac
    if not _lze_pouzit(hrac, "meditace"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.sex_energy = min(_max_pro(hrac, "sex_energy"), hrac.sex_energy + 5)
    hrac.dark_energy = min(_max_pro(hrac, "dark_energy"), hrac.dark_energy + 12)
    _oznac_pouziti(hrac, "meditace")
    tisk_ok("Meditace. Temná energie +12, sexuální +5.")
    return True


def zahrada(hra):
    hrac = hra.hrac
    if not _lze_pouzit(hrac, "zahrada"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.sex_energy = min(_max_pro(hrac, "sex_energy"), hrac.sex_energy + 12)
    hrac.dark_energy = min(_max_pro(hrac, "dark_energy"), hrac.dark_energy + 6)
    _oznac_pouziti(hrac, "zahrada")
    tisk_ok("Klidný rozhovor v zahradě. Sex +12, temno +6.")
    return True


def observator(hra):
    hrac = hra.hrac
    if not _lze_pouzit(hrac, "observator"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.sex_energy = min(_max_pro(hrac, "sex_energy"), hrac.sex_energy + 4)
    hrac.dark_energy = min(_max_pro(hrac, "dark_energy"), hrac.dark_energy + 16)
    _oznac_pouziti(hrac, "observator")
    tisk_ok("Pozorování oblohy. Temno +16, sex +4.")
    return True


def molo(hra):
    hrac = hra.hrac
    cena = 25
    if hrac.gold < cena:
        tisk_chyba("Na směnu na molu nemáš dost zlata.")
        return False
    if not _lze_pouzit(hrac, "molo"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.gold -= cena
    hrac.sex_energy = min(_max_pro(hrac, "sex_energy"), hrac.sex_energy + 18)
    hrac.dark_energy = min(_max_pro(hrac, "dark_energy"), hrac.dark_energy + 10)
    _oznac_pouziti(hrac, "molo")
    tisk_ok("Směna na molu. Sex +18, temno +10.")
    return True


def zobraz_menu(hra):
    clear()
    hrac = hra.hrac
    lokace = getattr(getattr(hra, "svet", None), "aktualni_lokace", "")
    print(f"{CYAN}--- Dobití energie ---{NC}\n")
    print(
        f"Sex: {hrac.sex_energy}/{_max_pro(hrac, 'sex_energy')} | "
        f"Temno: {hrac.dark_energy}/{_max_pro(hrac, 'dark_energy')} | Zlato: {hrac.gold}"
    )
    moznosti = [("1", "Meditace (zdarma, 1x denně)")]
    if True:
        moznosti.append(("2", "Hostinec (35 zlata, energie a HP)"))
        moznosti.append(("3", "Lázně (60 zlata, energie a HP)"))
    moznosti.append(("4", "Alchymie (lektvary z vyrobených surovin)"))
    if lokace in ("pevnost", "zahrada", "") or True:
        moznosti.append(("5", "Klidný rozhovor v zahradě (1x denně)"))
    if lokace in ("haj_soumraku", "") or True:
        moznosti.append(("6", "Pozorování oblohy (1x denně)"))
    if lokace in ("pristav", "molo", "") or True:
        moznosti.append(("7", "Směna na molu (25 zlata, 1x denně)"))
    for cislo, popis in moznosti:
        print(f"{cislo}) {popis}")
    print("0) Zpět")
    volba = input("> ").strip()
    if volba == "1":
        meditace(hra)
    elif volba == "2":
        hostinec(hra)
    elif volba == "3":
        lazne(hra)
    elif volba == "4":
        if hasattr(hra, "alchymie"):
            hra.alchymie.zobraz_menu(hra.hrac, hra.harem)
        else:
            tisk_chyba("Alchymie není dostupná.")
    elif volba == "5":
        zahrada(hra)
    elif volba == "6":
        observator(hra)
    elif volba == "7":
        molo(hra)
    try:
        input("Enter...")
    except EOFError:
        pass
