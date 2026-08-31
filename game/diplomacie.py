# game/diplomacie.py
import random
from models.frakce import FrakcniSystem, Frakce
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, CYAN, MAGENTA, GREEN, RED, YELLOW, NC


class Diplomacie:
    def __init__(self, frakce: FrakcniSystem):
        self.frakce = frakce

    def zobraz_frakce(self):
        clear()
        print(f"{GOLD}--- Diplomacie ---{NC}")
        if not getattr(self.frakce, "frakce", None):
            print("Žádné frakce.")
            return
        for klic, frakce in self.frakce.frakce.items():
            rep = frakce.reputace
            barva = GREEN if rep >= 40 else (RED if rep <= -20 else CYAN)
            print(f"  {klic}: {frakce.nazev} ({barva}reputace: {rep}{NC})")
            if getattr(frakce, "popis", None):
                print(f"      {frakce.popis}")
        print()

    def vyjednavat(self, hrac, cilova_frakce, akce):
        if cilova_frakce not in self.frakce.frakce:
            tisk_chyba("Neplatná frakce.")
            return
        frakce = self.frakce.frakce[cilova_frakce]
        if akce == "uplatek":
            cena = 100
            if hrac.gold >= cena:
                hrac.gold -= cena
                delta = random.randint(5, 15)
                frakce.reputace += delta
                tisk_ok(f"Podplatil jsi {frakce.nazev}. Reputace +{delta} (aktuálně {frakce.reputace})")
            else:
                tisk_chyba("Nedostatek zlata.")
        elif akce == "spojenectvi":
            if frakce.reputace >= 50:
                frakce.reputace += 10
                tisk_ok(f"Uzavřeno spojenectví s {frakce.nazev}.")
            else:
                tisk_chyba("Reputace je příliš nízká pro spojenectví (potřeba 50).")
        elif akce == "hrozba":
            if frakce.reputace <= -30:
                delta = random.randint(-10, -5)
                frakce.reputace += delta
                tisk_ok(f"Pohrozil jsi frakci {frakce.nazev}. Reputace {delta:+d}")
            else:
                tisk_chyba("Nelze vyhrožovat, dokud nejsou vztahy dost špatné.")
        else:
            tisk_chyba("Neznámá akce.")

    def obchodovat(self, hrac, cilova_frakce, typ_zbozi="bezny"):
        if cilova_frakce not in self.frakce.frakce:
            tisk_chyba("Neplatná frakce.")
            return
        frakce = self.frakce.frakce[cilova_frakce]
        cena = int(50 * (1 + frakce.reputace / 100))
        hrac.gold += max(10, cena)
        frakce.reputace += random.randint(1, 5)
        tisk_ok(f"Obchodoval jsi s {frakce.nazev}. Zisk {max(10, cena)} zlaťáků.")

    def menu(self, hra):
        hrac = hra.hrac if hasattr(hra, "hrac") else hra
        while True:
            self.zobraz_frakce()
            print(f"{GREEN}1) Úplatek (100 zl)")
            print(f"{CYAN}2) Spojenectví (reputace ≥ 50)")
            print(f"{RED}3) Hrozba (reputace ≤ -30)")
            print(f"{YELLOW}4) Obchod")
            print(f"{NC}0) Zpět")
            try:
                volba = input("> ").strip().lower()
            except EOFError:
                return
            if volba in ("0", "q", ""):
                return
            klice = list(self.frakce.frakce.keys())
            print("Frakce:")
            for i, k in enumerate(klice, 1):
                print(f"  {i}) {k} – {self.frakce.frakce[k].nazev}")
            try:
                vyber = input("Vyber frakci (číslo nebo id): ").strip().lower()
            except EOFError:
                return
            if vyber.isdigit():
                idx = int(vyber) - 1
                if 0 <= idx < len(klice):
                    cil = klice[idx]
                else:
                    tisk_chyba("Špatná volba.")
                    try:
                        input("Enter...")
                    except EOFError:
                        return
                    continue
            elif vyber in self.frakce.frakce:
                cil = vyber
            else:
                tisk_chyba("Neplatná frakce.")
                try:
                    input("Enter...")
                except EOFError:
                    return
                continue
            if volba == "1":
                self.vyjednavat(hrac, cil, "uplatek")
            elif volba == "2":
                self.vyjednavat(hrac, cil, "spojenectvi")
            elif volba == "3":
                self.vyjednavat(hrac, cil, "hrozba")
            elif volba == "4":
                self.obchodovat(hrac, cil)
            else:
                tisk_chyba("Neplatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return
