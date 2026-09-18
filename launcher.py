#!/usr/bin/env python3
"""
DARK DOMINION – Launcher
Zkontroluje Python, nainstaluje závislosti a spustí hru.
"""
import sys
import subprocess
import os

# ── Kontrola Python verze ────────────────────────────────────────────────────
if sys.version_info < (3, 8):
    print("❌ Potřebuješ Python 3.8 nebo novější.")
    print(f"   Aktuální verze: {sys.version}")
    input("Enter...")
    sys.exit(1)

print(f"✔ Python {sys.version.split()[0]}")

# ── Volitelné balíčky ────────────────────────────────────────────────────────
OPTIONAL_PACKAGES = ["colorama"]

for pkg in OPTIONAL_PACKAGES:
    try:
        __import__(pkg)
    except ImportError:
        print(f"  Instaluji {pkg}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
            check=False
        )

# ── Spuštění hry ────────────────────────────────────────────────────────────
game_dir = os.path.dirname(os.path.abspath(__file__))
main_py  = os.path.join(game_dir, "main.py")

if not os.path.exists(main_py):
    print(f"❌ Soubor main.py nenalezen v: {game_dir}")
    input("Enter...")
    sys.exit(1)

print("✔ Spouštím hru...\n")
os.chdir(game_dir)

try:
    import main  # noqa: F401 – just run it
except KeyboardInterrupt:
    print("\n\n  Hra přerušena. Nashledanou!")
except Exception as e:
    print(f"\n❌ Neočekávaná chyba: {e}")
    import traceback
    traceback.print_exc()
    input("\nStiskni Enter pro ukončení...")
