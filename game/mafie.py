# game/mafie.py
from models.mafie import Mafie, Uzemi
from utils.vypis import clear, tisk_ok, tisk_chyba

DOSTUPNA_UZEMI = (
    ("Přístav", 100, 0, 5),
    ("Tržiště", 80, 0, 3),
    ("Čtvrť bohatých", 150, 0, 10),
)


def dostupna_uzemi(mafie: Mafie):
    vlastni = {u.nazev for u in mafie.uzemi}
    return [
        Uzemi(nazev, prijem, kontrola, riziko)
        for nazev, prijem, kontrola, riziko in DOSTUPNA_UZEMI
        if nazev not in vlastni
    ]


def koupit_uzemi(hrac, mafie: Mafie, nazev: str):
    """Koupí konkrétní dostupné území bez vstupu z menu."""
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


def spravovat_mafii(hrac, mafie: Mafie):
    clear()
    print("--- Mafie / Sex impérium ---")
    print(f"Vojáci: {mafie.vojaci} | Kapitáni: {mafie.kapitanove}")
    print(f"Celkový příjem: {mafie.vypocet_prijmu()} zlaťáků/den")
    print(f"Korupce: {mafie.korupce} | Vliv ve městě: {mafie.vliv_ve_meste}\n")
    if not mafie.uzemi:
        print("Zatím nemáš žádná území.")
    else:
        for i, u in enumerate(mafie.uzemi, 1):
            stav = "obsazeno" if u.obsazeno else "volné"
            print(f"{i}) {u.nazev} - příjem {u.prijem}, kontrola {u.kontrola}%, stav: {stav}")
    print("\n1) Koupit území")
    print("2) Vylepšit kontrolu")
    print("3) Najímat vojáky")
    print("4) Zvýšit korupci")
    print("0) Zpět")
    volba = input("> ")
    if volba == "1":
        print("Dostupná území:")
        dostupna = dostupna_uzemi(mafie)
        for i, u in enumerate(dostupna, 1):
            print(f"{i}) {u.nazev} - příjem {u.prijem}, riziko {u.riziko_inkvizice}")
        try:
            idx = int(input("Vyber území: ")) - 1
            if 0 <= idx < len(dostupna):
                if not koupit_uzemi(hrac, mafie, dostupna[idx].nazev):
                    tisk_chyba("Nedostatek zlata.")
        except ValueError:
            tisk_chyba("Špatná volba.")
    elif volba == "2":
        if mafie.uzemi:
            for i, u in enumerate(mafie.uzemi, 1):
                print(f"{i}) {u.nazev} (kontrola {u.kontrola}%)")
            try:
                idx = int(input("Vyber území: ")) - 1
                if 0 <= idx < len(mafie.uzemi):
                    cena = 100 + mafie.uzemi[idx].kontrola * 5
                    if hrac.gold >= cena and mafie.uzemi[idx].kontrola < 100:
                        hrac.gold -= cena
                        mafie.uzemi[idx].kontrola += 10
                        if mafie.uzemi[idx].kontrola > 100:
                            mafie.uzemi[idx].kontrola = 100
                        tisk_ok(f"Kontrola zvýšena na {mafie.uzemi[idx].kontrola}%.")
                    else:
                        tisk_chyba("Nelze vylepšit.")
            except ValueError:
                tisk_chyba("Špatná volba.")
    elif volba == "3":
        if not najmout_vojaka(hrac, mafie):
            tisk_chyba("Nedostatek zlata.")
    elif volba == "4":
        cena = 200
        if hrac.gold >= cena:
            hrac.gold -= cena
            mafie.korupce += 5
            if mafie.korupce > 100:
                mafie.korupce = 100
            tisk_ok(f"Korupce zvýšena na {mafie.korupce}.")
        else:
            tisk_chyba("Nedostatek zlata.")
    input("Enter...")
