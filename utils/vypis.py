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

def ascii_art():
    print(r"""
    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██║██╔═══██╗████╗  ██║
    ██║  ██║███████║██████╔╝█████╔╝     ██║  ██║██║   ██║██╔████╔██║██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║  ██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║██║  ██╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    """)
    print(f"{GOLD}{BOLD}               DARK DOMINION COMPLETE v18.0{NC}")
    print(f"{MAGENTA}  👾 Nájmy • Aukce • Věrnost • Inkvizice • Špióni • Manipulace • Tresty • Odměny 🍓{NC}\n")
