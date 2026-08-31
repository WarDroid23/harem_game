# game/mafie.py
from models.mafie import Mafie, Uzemi
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, CYAN, MAGENTA, GREEN, RED, NC

DOSTUPNA_UZEMI = (
    ("Přístav", 100, 0, 5),
    ("Tržiště", 80, 0, 3),
    ("Čtvrť bohatých", 150, 0, 10),
    ("Doky", 90, 0, 4),
    ("Staré město", 120, 0, 7),
)


def dostupna_uzemi(mafie: Mafie):
    vlastni = {u.nazev for u in mafie.uzemi}
    return [
        Uzemi(nazev, prijem, kontrola, riziko)
        for nazev, prijem, kontrola, riziko in DOSTUPNA_UZEMI
        if nazev not in vlastni
    ]


def koupit_uzemi(hrac, mafie: Mafie, nazev: str):
    uzemi = next((u for u in dostupna_uzemi(mafie) if u.nazev == nazev), None)
    cena = 500 + len(mafie.uzemi) * 200
    if uzemi is None or hrac.gold < cena:
        return False
    hrac.gold -= cena
    mafie.uzemi.append(uzemi)
    tisk_ok(f"Koupeno území {uzemi.nazev}.")
    return True


def najmout_vojaka(hrac, mafie: Mafie, cena=50):
    if hrac.gold < cena:
        return False
    hrac.gold -= cena
    mafie.vojaci += 1
    tisk_ok("Najat voják.")
    return True


def _rozbal_args(arg0, arg1=None):
    """Podporuje spravovat_mafii(hra) i spravovat_mafii(hrac, mafie)."""
    if arg1 is not None:
        return arg0, arg1
    if hasattr(arg0, "hrac") and hasattr(arg0, "mafie"):
        return arg0.hrac, arg0.mafie
    raise TypeError("spravovat_mafii očekává (hra) nebo (hrac, mafie)")


def spravovat_mafii(arg0, arg1=None):
    """Menu mafie. Volání: spravovat_mafii(hra) nebo (hrac, mafie)."""
    try:
        hrac, mafie = _rozbal_args(arg0, arg1)
    except TypeError as e:
        tisk_chyba(str(e))
        try:
            input("Enter...")
        except EOFError:
            pass
        return

    while True:
        clear()
        print(f"{MAGENTA}--- Mafie / Sex impérium ---{NC}")
        print(f"Zlato: {hrac.gold} 🪙")
        print(f"Vojáci: {mafie.vojaci} | Kapitáni: {getattr(mafie, 'kapitanove', 0)}")
        print(f"Celkový příjem: {mafie.vypocet_prijmu()} zlaťáků/den")
        print(f"Korupce: {mafie.korupce} | Vliv ve městě: {getattr(mafie, 'vliv_ve_meste', 0)}\n")
        if not mafie.uzemi:
            print("Zatím nemáš žádná území.")
        else:
            for i, u in enumerate(mafie.uzemi, 1):
                stav = "obsazeno" if getattr(u, "obsazeno", False) else "volné"
                print(
                    f"{i}) {u.nazev} – příjem {u.prijem}, "
                    f"kontrola {u.kontrola}%, stav: {stav}"
                )
        print(f"\n{GREEN}1) Koupit území")
        print(f"{CYAN}2) Vylepšit kontrolu")
        print(f"{GOLD}3) Najímat vojáky (50 zl)")
        print(f"{RED}4) Zvýšit korupci (200 zl)")
        print(f"{NC}0) Zpět")
        try:
            volba = input("> ").strip()
        except EOFError:
            return

        if volba == "0":
            return
        if volba == "1":
            print("Dostupná území:")
            dostupna = dostupna_uzemi(mafie)
            if not dostupna:
                tisk_info("Žádná další území k nákupu.")
            else:
                for i, u in enumerate(dostupna, 1):
                    cena = 500 + len(mafie.uzemi) * 200
                    print(
                        f"{i}) {u.nazev} – příjem {u.prijem}, "
                        f"riziko {u.riziko_inkvizice}, cena {cena}"
                    )
                try:
                    idx = int(input("Vyber území: ")) - 1
                    if 0 <= idx < len(dostupna):
                        if not koupit_uzemi(hrac, mafie, dostupna[idx].nazev):
                            tisk_chyba("Nedostatek zlata nebo území není dostupné.")
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Špatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "2":
            if not mafie.uzemi:
                tisk_chyba("Nemáš žádná území.")
            else:
                for i, u in enumerate(mafie.uzemi, 1):
                    print(f"{i}) {u.nazev} (kontrola {u.kontrola}%)")
                try:
                    idx = int(input("Vyber území: ")) - 1
                    if 0 <= idx < len(mafie.uzemi):
                        cena = 100 + mafie.uzemi[idx].kontrola * 5
                        if hrac.gold >= cena and mafie.uzemi[idx].kontrola < 100:
                            hrac.gold -= cena
                            mafie.uzemi[idx].kontrola = min(100, mafie.uzemi[idx].kontrola + 10)
                            tisk_ok(f"Kontrola zvýšena na {mafie.uzemi[idx].kontrola}%.")
                        else:
                            tisk_chyba("Nelze vylepšit (zlato nebo max kontrola).")
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Špatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "3":
            if not najmout_vojaka(hrac, mafie):
                tisk_chyba("Nedostatek zlata.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "4":
            cena = 200
            if hrac.gold >= cena:
                hrac.gold -= cena
                mafie.korupce = min(100, mafie.korupce + 5)
                tisk_ok(f"Korupce zvýšena na {mafie.korupce}.")
            else:
                tisk_chyba("Nedostatek zlata.")
            try:
                input("Enter...")
            except EOFError:
                return
        else:
            tisk_chyba("Neplatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return
