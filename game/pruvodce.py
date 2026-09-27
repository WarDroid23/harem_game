"""Praktický průvodce systémy hry a doporučení pro aktuální uloženou hru."""

from config import CYAN, DIM, GOLD, GREEN, MAGENTA, NC, YELLOW
from game.kampan import KAPITOLY
from game.cile_hry import doporuceni_pro_pruvodce
from utils.vypis import clear, hlavicka, menu_cara


def _doporuceni(hra):
    doporuceni = doporuceni_pro_pruvodce(hra)
    if not hra.mafie.uzemi:
        doporuceni.append("Pro stabilní příjem prozkoumej mafii a území ve volbě 3.")
    return doporuceni


def zobraz_pruvodce(hra):
    """Vypíše nápovědu podle stavu hry; herní data zůstávají beze změny."""
    clear()
    hlavicka("Průvodce dominiem", "Rychlý start a doporučení pro tvou hru")

    print(f"{GOLD}Jak začít{NC}")
    print("  1. Prohlédni si harém a dostupné interakce (volba 1).")
    print("  2. Navštěvuj mapu (8), mluv s NPC a postupuj v kampani (9).")
    print("  3. Přijímej úkoly (14), vylepšuj postavu (4) a buduj své území (3, 16).")
    print("  4. Odpočinek (12) obnoví síly, posune den a může spustit událost.")

    menu_cara()
    print(f"\n{CYAN}Důležité systémy{NC}")
    print("  • Volba 22 shrnuje běžné úkoly, úkoly NPC a hlavní kampaň.")
    print("  • Volba 29 uchovává kroniku rozhodnutí a významných událostí.")
    print("  • Volba 26 otevře ukládání, načítání a nastavení.")
    print("  • Volba 27 zobrazí tohoto průvodce; nápověda nemění stav hry.")

    menu_cara()
    print(f"\n{MAGENTA}Doporučení pro tuto hru{NC}")
    for doporuceni in _doporuceni(hra):
        print(f"  ➜ {doporuceni}")

    kapitola = hra.kampan.aktualni()
    if kapitola:
        cislo = min(hra.kampan.kapitola, len(KAPITOLY) - 1) + 1
        print(
            f"\n{DIM}Aktuální kapitola {cislo}: "
            f"{kapitola.get('nazev', 'Neznámá kapitola')}{NC}"
        )
    else:
        print(f"\n{GREEN}Hlavní kampaň je dokončena. Prozkoumej vedlejší systémy.{NC}")

    print(f"\n{YELLOW}Ovládání{NC}")
    print("  Zadej číslo volby a potvrď Enterem. Zkratky S/L/M otevřou hlavní menu.")
    if hra.nastaveni.vyvojarsky_rezim:
        print(f"  {DIM}Vývojářské volby T a $ jsou zapnuté v nastavení.{NC}")
    else:
        print(f"  {DIM}Vývojářské volby lze zapnout v nastavení (26 → 3 → 6).{NC}")
