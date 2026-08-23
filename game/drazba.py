# game/drazba.py
import random
from utils.vypis import clear, tisk_ok, tisk_chyba
from config import GOLD, GREEN, RED, CYAN, NC

def drazba_otrokyn(hrac, harem):
    clear()
    print(f"{GOLD}--- Dražba otrokyň ---{NC}\n")

    otrokyne = [o for o in harem.otrokyne if o.hp > 0 and not o.na_najmu]
    if not otrokyne:
        tisk_chyba("Nemáš žádné otrokyně na prodej.")
        input("Enter...")
        return

    print("Vyber otrokyni k prodeji:")
    for i, o in enumerate(otrokyne, 1):
        print(f"{i}) {o.jmeno} (subm:{o.submisivita}, broken:{o.broken})")

    try:
        idx = int(input("> ")) - 1
        if idx < 0 or idx >= len(otrokyne):
            tisk_chyba("Špatná volba.")
            input("Enter...")
            return
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")
        return

    otrok = otrokyne[idx]
    zakladni_cena = 50 + otrok.submisivita * 5 + otrok.poslusnost * 3 + otrok.loajalita * 2
    if otrok.broken > 50:
        zakladni_cena += 100
    if otrok.owned_mark:
        zakladni_cena += 150

    zajemci = random.randint(2, 5)
    max_cena = zakladni_cena
    for i in range(zajemci):
        nabidka = zakladni_cena + random.randint(0, 50) * (i + 1)
        if nabidka > max_cena:
            max_cena = nabidka

    print(f"\nVydražil jsi otrokyni {otrok.jmeno} za {max_cena} zlaťáků.")
    hrac.gold += max_cena
    harem.odstranit(otrok.jmeno)
    tisk_ok(f"Otrokyně {otrok.jmeno} prodána.")
    input("Enter...")
