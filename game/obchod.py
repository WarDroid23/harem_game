# game/obchod.py — zjednodušený obchod + černý trh
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, CYAN, MAGENTA, NC


def obchod(hra):
    clear()
    print(f"{GOLD}--- Obchod ---{NC}\n")
    print("1) Léčivý elixír (30 zl) — +20 HP")
    print("2) Stimulant (40 zl) — +15 sex energie")
    print("3) Temný katalyzátor (60 zl) — +15 temná energie")
    print("9) Černý trh")
    print("0) Zpět")
    try:
        volba = input("> ").strip()
    except EOFError:
        return
    if volba == "9":
        cerny_trh(hra)
        return
    if volba == "0":
        return
    hrac = hra.hrac
    if volba == "1" and hrac.gold >= 30:
        hrac.gold -= 30
        hrac.hp = min(hrac.max_hp, hrac.hp + 20)
        tisk_ok("Elixír vypit. HP +20.")
    elif volba == "2" and hrac.gold >= 40:
        hrac.gold -= 40
        max_s = hrac.max_sex() if hasattr(hrac, "max_sex") else 100
        hrac.sex_energy = min(max_s, hrac.sex_energy + 15)
        tisk_ok("Stimulant. Sex energie +15.")
    elif volba == "3" and hrac.gold >= 60:
        hrac.gold -= 60
        max_t = hrac.max_temno() if hasattr(hrac, "max_temno") else 100
        hrac.dark_energy = min(max_t, hrac.dark_energy + 15)
        tisk_ok("Temný katalyzátor. Temná energie +15.")
    else:
        tisk_chyba("Nelze koupit (zlato nebo volba).")
    try:
        input("Enter...")
    except EOFError:
        pass


def cerny_trh(hra):
    clear()
    print(f"{MAGENTA}--- Černý trh ---{NC}")
    kor = getattr(hra.mafie, "korupce", 0)
    if kor < 20 and getattr(hra.hrac, "dark_energy", 0) < 40:
        tisk_chyba("Ještě nemáš dost temného vlivu (korupce ≥20 nebo temná energie ≥40).")
        try:
            input("Enter...")
        except EOFError:
            pass
        return
    print("1) Elixír temnoty (80 zl) — +20 temná energie")
    print("2) Okovy luxusu (120 zl) — +5 loajalita všem aktivním")
    print("0) Zpět")
    try:
        v = input("> ").strip()
    except EOFError:
        return
    if v == "1" and hra.hrac.gold >= 80:
        hra.hrac.gold -= 80
        if hasattr(hra.hrac, "pridej_dark_energy"):
            hra.hrac.pridej_dark_energy(20)
        else:
            hra.hrac.dark_energy = min(
                getattr(hra.hrac, "max_dark_energy", 120), hra.hrac.dark_energy + 20
            )
        tisk_ok("Elixír temnoty vypit.")
    elif v == "2" and hra.hrac.gold >= 120:
        hra.hrac.gold -= 120
        for o in hra.harem.vsechny_aktivni():
            o.loajalita = min(100, o.loajalita + 5)
        tisk_ok("Okovy luxusu nasazeny. Harém je vděčný… a spoutaný.")
    elif v != "0":
        tisk_chyba("Nelze koupit.")
    try:
        input("Enter...")
    except EOFError:
        pass
