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
    """Rychlé smazání – ANSI bez shellu, fallback na cls/clear."""
    try:
        from utils.term_render import clear_fast
        clear_fast()
        return
    except Exception:
        pass
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


def terminalni_obrazek(scena, hra=None, **kwargs):
    """Vykreslí ASCII ilustraci – dynamicky generovanou."""
    try:
        from utils.ascii_gen import generuj_scenu, generuj_z_hry
        if hra is not None:
            print(generuj_z_hry(hra, scena))
        else:
            print(generuj_scenu(scena or "menu", **kwargs))
        return
    except Exception:
        pass
    from config import GOLD, MAGENTA, CYAN, NC
    print(f"{MAGENTA}     ╔═══ {scena or 'menu'} ═══╗{NC}")
    print(f"{CYAN}     │  TEMNÉ DOMINIUM  │{NC}")
    print(f"{GOLD}     ╚═════════════════╝{NC}")


def ukazatel(hodnota, maximum, sirka=18, barva_plno=GREEN, barva_malo=RED):
    maximum = max(1, maximum)
    hodnota = max(0, min(maximum, hodnota))
    plno = int(sirka * hodnota / maximum)
    pomer = hodnota / maximum
    if pomer > 0.6:
        bv = barva_plno
    elif pomer > 0.3:
        bv = YELLOW
    else:
        bv = barva_malo
    blok_plno = "█" * plno
    blok_prazdno = "░" * (sirka - plno)
    return f"{bv}{blok_plno}{DIM}{blok_prazdno}{NC} {hodnota}/{maximum}"


def hlavicka(stitek, podtitulek=""):
    print()
    sirka = 60
    # Clean up standard titles from existing hyphens/equals
    stitek = stitek.replace("---", "").replace("===", "").strip()
    mezera = sirka - 4 - len(stitek)
    if mezera < 0:
        mezera = 0
    l_mezera = mezera // 2
    p_mezera = mezera - l_mezera
    
    print(f"{CYAN}{BOLD}╔{'═' * (sirka-2)}╗{NC}")
    print(f"{CYAN}{BOLD}║{NC} {' ' * l_mezera}{BOLD}{WHITE}{stitek}{NC}{' ' * p_mezera} {CYAN}{BOLD}║{NC}")
    print(f"{CYAN}{BOLD}╚{'═' * (sirka-2)}╝{NC}")
    if podtitulek:
        print(f"  {DIM}{podtitulek}{NC}")


def vytiskni_volbu(cislo, text, barva=YELLOW):
    print(f"  {BOLD}{barva}{cislo}){NC} {text}")

def menu_cara():
    print(f"{DIM}────────────────────────────────────────────────────────────{NC}")

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
