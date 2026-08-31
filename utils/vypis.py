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
