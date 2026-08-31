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


def zobraz_menu(hra):
    clear()
    hrac = hra.hrac
    print(f"{CYAN}--- Dobití energie ---{NC}\n")
    print(
        f"Sex: {hrac.sex_energy}/{_max_pro(hrac, 'sex_energy')} | "
        f"Temno: {hrac.dark_energy}/{_max_pro(hrac, 'dark_energy')} | Zlato: {hrac.gold}"
    )
    print("1) Hostinec (35 zlata)")
    print("2) Lázně (60 zlata)")
    print("3) Meditace (zdarma, 1x denně)")
    print("0) Zpět")
    volba = input("> ").strip()
    if volba == "1":
        hostinec(hra)
    elif volba == "2":
        lazne(hra)
    elif volba == "3":
        meditace(hra)
    try:
        input("Enter...")
    except EOFError:
        pass
