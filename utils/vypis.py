# utils/vypis.py
import os
import sys
from config import NC, GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, GOLD, BOLD, DIM

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def barva(text, barva):
    return f"{barva}{text}{NC}"

def tisk_ok(text):
    print(barva(f"✔ {text}", GREEN))

def tisk_chyba(text):
    print(barva(f"✖ {text}", RED))

def tisk_info(text):
    print(barva(text, NC))

def tisk_zlato(text):
    print(barva(f"💰 {text}", GOLD))

def tisk_magenta(text):
    print(barva(f"🔮 {text}", MAGENTA))

def tisk_cyan(text):
    print(barva(f"💠 {text}", CYAN))

def ukazatel(hodnota, maximum, sirka=18):
    """Vrátí krátký ASCII ukazatel použitelný i v terminálu bez barev."""
    maximum = max(1, maximum)
    hodnota = max(0, min(maximum, hodnota))
    plno = int(sirka * hodnota / maximum)
    return "[" + "#" * plno + "-" * (sirka - plno) + f"] {hodnota}/{maximum}"

def hlavicka(stitek, podtitulek=""):
    print(f"{BOLD}{GOLD}=== {stitek} ==={NC}")
    if podtitulek:
        print(f"{DIM}{podtitulek}{NC}")

def ascii_art():
    print(r"""
    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██║██╔═══██╗████╗  ██║
    ██║  ██║███████║██████╔╝█████╔╝     ██║  ██║██║   ██║██╔████╔██║██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║  ██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║██║  ██╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    """)
    print(f"{GOLD}{BOLD}               DARK DOMINION COMPLETE v19.0{NC}")
    print(f"{MAGENTA}  👾 Kampaň • Mapa • Vztahy • Osudy • Crafting • Souboje • Harém{NC}\n")
