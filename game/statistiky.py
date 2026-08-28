# game/statistiky.py
from utils.vypis import clear, tisk_ok, tisk_info
from config import GOLD, GREEN, CYAN, NC

def zobraz_statistiky(hra):
    clear()
    print(f"{GOLD}--- Statistiky a žebříček ---{NC}\n")

    h = hra.hrac
    print(f"{CYAN}Postava:{NC}")
    print(f"  Jméno: {h.jmeno}")
    print(f"  Level: {h.level} (XP: {h.xp}/{h.xp_next})")
    print(f"  Zlato: {h.gold} 🪙")
    print(f"  Dominance: {h.dominance}")
    print(f"  Dovednosti: {h.skilly}")
    print()

    print(f"{CYAN}Harém:{NC}")
    print(f"  Počet otrokyň: {hra.harem.pocet()}")
    print(f"  Úroveň harému: {hra.harem.harem_level}")
    print(f"  Pasivní příjem: {hra.harem.pasivni_prijem()} zlaťáků/den")
    print()

    print(f"{CYAN}Mafie / Impérium:{NC}")
    print(f"  Území: {len(hra.mafie.uzemi)}")
    print(f"  Vojáci: {hra.mafie.vojaci}")
    print(f"  Vliv ve městě: {hra.mafie.vliv_ve_meste}%")
    print(f"  Příjem: {hra.mafie.vypocet_prijmu()} zlaťáků/den")
    print()

    print(f"{CYAN}Frakce:{NC}")
    for klic, frakce in hra.frakce.frakce.items():
        print(f"  {frakce.nazev}: {frakce.reputace}")
    print()

    print(f"{CYAN}Výzkum:{NC}")
    if hra.vyzkum.ziskane:
        for id_v in hra.vyzkum.ziskane:
            print(f"  ✔ {id_v}")
    else:
        print("  Žádný")
    print()

    print(f"{CYAN}Quest systém:{NC}")
    print(f"  Dokončeno questů: {hra.questy.dokonceno if hasattr(hra, 'questy') else 0}")
    print(f"  Aktivní lokace: {hra.svet.aktualni_lokace}")
    print(
        f"  Kampaň: kapitola {hra.kampan.kapitola + 1}"
        if hra.kampan.aktualni()
        else "  Kampaň: dokončena"
    )
    dokoncene_osudy = sum(
        1 for otrok in hra.harem.otrokyne if otrok.osud_dokonceno
    )
    print(f"  Uzavřené osobní osudy: {dokoncene_osudy}/{len(hra.harem.otrokyne)}")
    print()

    tisk_info("Stiskni Enter...")
    input()
