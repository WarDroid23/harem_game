"""Zobrazení hlavního herního menu a zpracování jeho textových zkratek."""

from config import (
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GOLD, BOLD, NC, DIM,
)
from utils.vypis import ascii_art, terminalni_obrazek, ukazatel


ZKRATKY_HLAVNIHO_MENU = {
    "s": "26",
    "l": "26",
    "m": "26",
    "q": "0",
    "a": "auto",
    "t": "test",
    "10": "test",
    "$": "cheat",
    "&": "cheat_suroviny",
    "#": "cheat_dovednosti",
    "*": "cheat_budovy",
}


def normalizuj_volbu(volba):
    """Převede zkratky menu na kanonické hodnoty; 10 zůstává zpětně kompatibilní."""
    return ZKRATKY_HLAVNIHO_MENU.get(volba, volba)


def vykresli_hlavni_menu(hra):
    ascii_art()
    terminalni_obrazek("menu")
    max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
    max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
    aktivni_harem = hra.harem.vsechny_aktivni()
    pocet_partnerek = sum(1 for o in aktivni_harem if getattr(o, "partnerka", False))
    oblibena = next((o for o in aktivni_harem if getattr(o, "oblibena", False)), None)
    oblib_txt = f" ★{oblibena.jmeno}" if oblibena else ""

    print(f"{GOLD}{BOLD}╔{'═'*76}╗{NC}")
    print(
        f"{GOLD}{BOLD}║{NC} {BOLD}Den {hra.hrac.den:>3}{NC}  "
        f"{GREEN}🪙 {hra.hrac.gold:<6}{NC}  "
        f"{YELLOW}👑 Harém {hra.harem.pocet()} (partnerek {pocet_partnerek}{oblib_txt}){NC}  "
        f"{MAGENTA}🏰 Území {len(hra.mafie.uzemi)}{NC}"
        f"{GOLD}{BOLD}{'':>2}║{NC}"
    )
    bar_s = ukazatel(hra.hrac.sex_energy, max_s, sirka=16)
    bar_t = ukazatel(
        hra.hrac.dark_energy, max_t, sirka=16,
        barva_plno=MAGENTA, barva_malo=RED,
    )
    print(
        f"{GOLD}{BOLD}║{NC} ⚡ Energie   {bar_s}   🌑 Temno  {bar_t}  "
        f"{RED}☩Inkvizice {hra.hrac.vliv_inkvizice:<3}{NC}  "
        f"{CYAN}📍{hra.svet.aktualni_lokace}{NC}"
        f"{GOLD}{BOLD}{'':>1}║{NC}"
    )
    print(f"{GOLD}{BOLD}╚{'═'*76}╝{NC}")
    print()

    print(f"{GOLD}{BOLD}╔════ 👑 HARÉM & DÍVKY ══════════════════╗{NC}   {MAGENTA}{BOLD}╔════ 🏰 PANSTVÍ & IMPÉRIUM ═════════════╗{NC}")
    print(f"║ {GREEN} 1){NC} 👉 Interakce s otrokyněmi            ║   ║ {MAGENTA} 3){NC} 🏢 Mafie / gangy & území        ║")
    print(f"║ {GREEN}23){NC} 🤝 Profily, osobnost, vztahy        ║   ║ {CYAN}16){NC} 🏗️ Budovy dominia               ║")
    print(f"║ {MAGENTA}28){NC} 💍 Manželství, žárlivost & rodina   ║   ║ {MAGENTA}21){NC} 🏛️ Nevěstinec & prodej dívek    ║")
    print(f"║ {RED} 7){NC} 🧠 Subky & Domestikace             ║   ║ {CYAN} 2){NC} 💰 Nájem otrokyně               ║")
    print(f"║ {YELLOW}11){NC} 🎯 Lov otrokyň                      ║   ║ {BLUE} 5){NC} 🤝 Diplomacie & frakce          ║")
    print(f"║ {GREEN}15){NC} 🏛️ Dražba otrokyň                    ║   ║ {GOLD} 6){NC} 🔬 Výzkum dominia               ║")
    print(f"║ {GOLD}30){NC} 📋 Denní rozkazy harému             ║   ║ {RED}31){NC} 🎭 Veřejný výkon                 ║")
    print(f"{GOLD}{BOLD}╚════════════════════════════════════════╝{NC}   {MAGENTA}{BOLD}╚════════════════════════════════════════╝{NC}")
    print(f"{CYAN}{BOLD}╔════ 🗺️ SVĚT & DOBRODRUŽSTVÍ ═══════════╗{NC}   {YELLOW}{BOLD}╔════ ⚙️ POSTAVA & PROVOZ ═══════════════╗{NC}")
    print(f"║ {CYAN} 8){NC} 🗺️ Mapa světa & lokace             ║   ║ {YELLOW} 4){NC} 📈 Vývoj postavy                ║")
    print(f"║ {GOLD} 9){NC} 📖 Příběhová kampaň                ║   ║ {YELLOW}18){NC} ⚔️ Souboj & aréna                ║")
    print(f"║ {RED}14){NC} 🎲 Questy & úkoly                  ║   ║ {BLUE}19){NC} 🧪 Alchymie & lektvary          ║")
    print(f"║ {GOLD}13){NC} 🛒 Obchod města                    ║   ║ {YELLOW}24){NC} 🛠️ Crafting & předměty          ║")
    print(f"║ {CYAN}22){NC} 📜 Deník úkolů                      ║   ║ {CYAN}25){NC} ⚡ Dobít energii                ║")
    print(f"║ {CYAN}29){NC} 📖 Kronika dominia                  ║   ║ {BLUE}12){NC} 🛌 Odpočinek (nový den)         ║")
    print(f"║ {CYAN}20){NC} 📋 Rychlý přehled dne              ║   ║ {MAGENTA}17){NC} 📊 Grafy & statistiky         ║")
    print(f"║ {YELLOW}27){NC} 🧭 Průvodce dominiem               ║   ║ {GREEN} A){NC} 🤖 Bezpečný automatický tah     ║")
    print(f"{CYAN}{BOLD}╚════════════════════════════════════════╝{NC}   {YELLOW}{BOLD}╚════════════════════════════════════════╝{NC}")
    print(f"{DIM}──────────────────────────────────────────────────────────────────────────────────{NC}")
    menu_spodek = (
        f"  {YELLOW}26) 🏠 Hlavní menu (uložit / načíst / nastavení){NC}   │   "
    )
    if hra.nastaveni.vyvojarsky_rezim:
        menu_spodek += (
            f"{MAGENTA}T) 🧪 Testovací otrokyně{NC}   │   "
            f"{RED}0) 🚪 Konec hry{NC}"
        )
    else:
        menu_spodek += f"{RED}0) 🚪 Konec hry{NC}"
    print(menu_spodek)
    print(f"  {CYAN}32) 📅 Kalendář a události{NC}")
    if hra.nastaveni.vyvojarsky_rezim:
        print(f"  {GOLD}$) 💰 Cheat: +10 000 zl. a doplnění všech energií{NC}")
        print(f"  {CYAN}&) 🧪 Cheat: +1 000 od všech surovin a zásob pevnosti{NC}")
        print(f"  {MAGENTA}#) 📈 Cheat: +10 ke každé dovednosti{NC}")
        print(f"  {YELLOW}*) 🏗️ Cheat: vylepšit všechny budovy{NC}")
    if getattr(hra.hrac, "bonus_za_questy", 0):
        print(f"  {GREEN}✨ Quest bonus získaný celkem: {hra.hrac.bonus_za_questy} zl.{NC}")
    if getattr(hra.hrac, "bonus_za_souboje", 0):
        print(f"  {RED}⚔️ Soubojové bonusy získané celkem: {hra.hrac.bonus_za_souboje} zl.{NC}")
