# utils/vypis.py
import os
import sys
from config import (
    NC, GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, GOLD, ORANGE, VIOLET,
    WHITE, GRAY, BOLD, DIM,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def barva(text, barva_kod):
    return f"{barva_kod}{text}{NC}"


def tisk_ok(text):
    print(barva(f"✔ {text}", GREEN))


def tisk_chyba(text):
    print(barva(f"✖ {text}", RED))


def tisk_info(text):
    print(barva(f"◆ {text}", CYAN))


def tisk_zlato(text):
    print(barva(f"💰 {text}", GOLD))


def tisk_magenta(text):
    print(barva(f"🔮 {text}", MAGENTA))


def tisk_cyan(text):
    print(barva(f"💠 {text}", CYAN))


def terminalni_obrazek(scena):
    obrazky = {
        "menu": (
            f"{VIOLET}       /\\_/\\{NC}\n"
            f"{MAGENTA}      ( o.o ){NC}   {GOLD}╔════════════════════╗{NC}\n"
            f"{CYAN}       > ^ <{NC}    {GOLD}║  TEMNÉ DOMINIUM   ║{NC}\n"
            f"{GRAY}      /|   |\\{NC}   {GOLD}╚════════════════════╝{NC}"
        ),
        "mapa": (
            f"{GREEN}       [PEVNOST]───[TRH]───[PŘÍSTAV]{NC}\n"
            f"{GRAY}          │          │{NC}\n"
            f"{BLUE}       [LES]────[HRANICE]{NC}\n"
            f"{ORANGE}              ✦ CESTA OSUDU{NC}"
        ),
        "souboj": (
            f"{RED}             /\\        /\\{NC}\n"
            f"{WHITE}            /  \\      /  \\{NC}\n"
            f"{YELLOW}           < ⚔  >  VS  <  ⚔ >{NC}\n"
            f"{RED}            \\__/      \\__/{NC}"
        ),
        "osudy": (
            f"{VIOLET}          .-=========-.{NC}\n"
            f"{GOLD}         /  KNIHA OSUDŮ \\{NC}\n"
            f"{CYAN}        |  ✦  ✦  ✦  ✦  |{NC}\n"
            f"{VIOLET}         \\_____________/{NC}"
        ),
        "harem": (
            f"{MAGENTA}     ╔═══ HARÉM ═══╗{NC}\n"
            f"{CYAN}     │ ♀  ♀  ★  ♀  │{NC}\n"
            f"{GOLD}     │   klečí…    │{NC}\n"
            f"{MAGENTA}     ╚═════════════╝{NC}"
        ),
        "odmena": (
            f"{GOLD}        .·´¯`·.¸{NC}\n"
            f"{YELLOW}       ¸.·´¯`·.¸.{NC}\n"
            f"{GREEN}      ODMĚNA PÁNA{NC}\n"
            f"{CYAN}       `·.¸.·´{NC}"
        ),
        "trest": (
            f"{RED}        ╱|、{NC}\n"
            f"{RED}      (˚ˎ 。7{NC}\n"
            f"{GRAY}       |、˜〵{NC}   {RED}TREST{NC}\n"
            f"{GRAY}       じしˍ,)ノ{NC}"
        ),
        "oblibena": (
            f"{GOLD}         ★{NC}\n"
            f"{MAGENTA}      ╱|、  ★{NC}\n"
            f"{CYAN}    (˚ˎ 。7{NC}\n"
            f"{GOLD}     OBLÍBENKYNĚ{NC}"
        ),
        "manzelstvi": (
            f"{MAGENTA}       .·´¯`·.{NC}\n"
            f"{GOLD}      ╱ 💍  ╲{NC}\n"
            f"{CYAN}     │ manžel │{NC}\n"
            f"{MAGENTA}      ╲_____╱{NC}"
        ),
        "lov": (
            f"{GREEN}      /\\_/\\  {ORANGE}╱╲{NC}\n"
            f"{GRAY}     ( o.o ) {ORANGE}╱  ╲  STOPA{NC}\n"
            f"{CYAN}      > ^ <  {ORANGE}╲  ╱{NC}\n"
            f"{GREEN}     LOV OTROKYŇ{NC}"
        ),
        "drazba": (
            f"{GOLD}     ╔══════════╗{NC}\n"
            f"{YELLOW}     ║  DRAŽBA  ║{NC}\n"
            f"{CYAN}     ║  ♀ ???   ║{NC}\n"
            f"{GOLD}     ╚══════════╝{NC}\n"
            f"{GRAY}      kladívko ⇓{NC}"
        ),
        "alchymie": (
            f"{GREEN}       (  (  )  ){NC}\n"
            f"{CYAN}        \\  ||  /{NC}\n"
            f"{VIOLET}         ╲ || ╱{NC}\n"
            f"{GOLD}        ELIXÍR{NC}"
        ),
        "noc": (
            f"{BLUE}      ·  *  .{NC}\n"
            f"{VIOLET}    *   ☽   *{NC}\n"
            f"{GRAY}   .  NOC V HARÉMU  .{NC}\n"
            f"{BLUE}      *  ·  *{NC}"
        ),
        "pevnost": (
            f"{GRAY}        /\\  /\\  /\\{NC}\n"
            f"{WHITE}       |  ||  ||  |{NC}\n"
            f"{GOLD}       | PEVNOST |{NC}\n"
            f"{GRAY}       |__||__||__|{NC}"
        ),
        "inkvizice": (
            f"{RED}      ╱ ═══ ╲{NC}\n"
            f"{YELLOW}     │  ✠  │{NC}\n"
            f"{RED}     │INKVIZICE│{NC}\n"
            f"{GRAY}      ╲_____╱{NC}"
        ),
        "loajalita": (
            f"{GOLD}      ♥─────♥─────♥{NC}\n"
            f"{CYAN}     LOAJALITA HARÉMU{NC}\n"
            f"{GREEN}      [████████░░]{NC}\n"
            f"{MAGENTA}       oddanost{NC}"
        ),
        "partnerka": (
            f"{CYAN}       .·´ ♥ `·.{NC}\n"
            f"{MAGENTA}      ╱ partner ╲{NC}\n"
            f"{GOLD}     │   spolu   │{NC}\n"
            f"{CYAN}      ╲_________╱{NC}"
        ),
        "nastaveni": (
            f"{WHITE}     ⚙️  NASTAVENÍ{NC}\n"
            f"{CYAN}     ├─ barvy{NC}\n"
            f"{MAGENTA}     ├─ téma{NC}\n"
            f"{GOLD}     └─ obtížnost{NC}"
        ),
        "save": (
            f"{GREEN}     ╔═══════╗{NC}\n"
            f"{CYAN}     ║ ULOŽIT ║{NC}\n"
            f"{GREEN}     ╚═══════╝{NC}\n"
            f"{GRAY}      💾 sloty{NC}"
        ),
    }
    print(obrazky.get(scena, obrazky["menu"]))


def ukazatel(hodnota, maximum, sirka=18):
    maximum = max(1, maximum)
    hodnota = max(0, min(maximum, hodnota))
    plno = int(sirka * hodnota / maximum)
    return "[" + "#" * plno + "-" * (sirka - plno) + f"] {hodnota}/{maximum}"


def hlavicka(stitek, podtitulek=""):
    print(f"{BOLD}{GOLD}=== {stitek} ==={NC}")
    if podtitulek:
        print(f"{DIM}{podtitulek}{NC}")


def ascii_art():
    print(
        r"""
    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██║██╔═══██╗████╗  ██║
    ██║  ██║███████║██████╔╝█████╔╝     ██║  ██║██║   ██║██╔████╔██║██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║  ██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║██║  ██╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    """
    )
    print(f"{GOLD}{BOLD}               DARK DOMINION – Dark Expansion{NC}")
    print(f"{MAGENTA}  👾 Harém • Loajalita • Odměny • Oblíbenkyně • Témata • Osudy{NC}\n")
