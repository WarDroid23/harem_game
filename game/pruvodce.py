"""Praktický průvodce systémy hry a doporučení pro aktuální uloženou hru."""

from config import CYAN, DIM, GOLD, GREEN, MAGENTA, NC, YELLOW
from game.kampan import KAPITOLY
from game.cile_hry import _cislo_volby, doporuceni_pro_pruvodce
from utils.vypis import clear, hlavicka, menu_cara


def _rychly_start(hra):
    """Vrátí stavové kroky úvodu bez změny uložené hry."""
    prozkoumal_lokaci = bool(hra.svet.prozkoumane_lokace)
    vybral_spojence = any(
        isinstance(volba, dict)
        and volba.get("kapitola") == 1
        and volba.get("volba") in ("mira", "radan")
        for volba in hra.kampan.volby
    )
    posunul_den = hra.hrac.den > 1
    return (
        (
            prozkoumal_lokaci,
            "Prozkoumej první lokaci",
            f"Mapa ({_cislo_volby('8')}) → vyber odhalenou lokaci a prozkoumej ji.",
        ),
        (
            vybral_spojence,
            "Získej prvního spojence",
            f"Kampaň ({_cislo_volby('9')}) → v kapitole „Cena spojenectví“ si vyber Miru nebo Radana.",
        ),
        (
            posunul_den,
            "Poprvé posuň herní den",
            f"Odpočinek ({_cislo_volby('12')}) obnoví síly a posune svět o den; hra se při tom automaticky uloží.",
        ),
    )


def _doporuceni(hra):
    doporuceni = doporuceni_pro_pruvodce(hra)
    if not hra.mafie.uzemi:
        doporuceni.append(
            f"Pro stabilní příjem prozkoumej mafii a území "
            f"(ve volbě {_cislo_volby('3')})."
        )
    return doporuceni


def zobraz_pruvodce(hra):
    """Vypíše nápovědu podle stavu hry; herní data zůstávají beze změny."""
    clear()
    hlavicka("Průvodce dominiem", "Rychlý start a doporučení pro tvou hru")

    kroky = _rychly_start(hra)
    hotovo = sum(dokonceno for dokonceno, _, _ in kroky)
    print(f"{GOLD}Rychlý start — {hotovo}/{len(kroky)} kroků{NC}")
    for dokonceno, nazev, instrukce in kroky:
        stav = f"{GREEN}✓{NC}" if dokonceno else f"{YELLOW}○{NC}"
        print(f"  {stav} {nazev}: {instrukce}")

    menu_cara()
    print(f"\n{CYAN}Důležité systémy{NC}")
    print(
        f"  • Deník úkolů (volba {_cislo_volby('22')}) shrnuje běžné "
        "úkoly, úkoly NPC a hlavní kampaň."
    )
    print(
        f"  • Kronika dominia (volba {_cislo_volby('29')}) uchovává "
        "rozhodnutí a významné události."
    )
    print(f"  • Volba {_cislo_volby('26')} otevře ukládání a nastavení.")
    print(
        f"  • Volba {_cislo_volby('27')} zobrazí tohoto průvodce; "
        "nápověda nemění stav hry."
    )

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
    print("  Zadej číslo zobrazené v menu a potvrď Enterem. S/L/M otevřou ukládání.")
    if hra.nastaveni.vyvojarsky_rezim:
        print(f"  {DIM}Vývojářské volby T a $ jsou zapnuté v nastavení.{NC}")
    else:
        print(
            f"  {DIM}Vývojářské volby lze zapnout v nastavení "
            f"(volba {_cislo_volby('26')}).{NC}"
        )
