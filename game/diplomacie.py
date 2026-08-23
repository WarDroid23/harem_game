# game/diplomacie.py
import random
from models.frakce import FrakcniSystem, Frakce
from utils.vypis import clear, tisk_ok, tisk_chyba

class Diplomacie:
    def __init__(self, frakce: FrakcniSystem):
        self.frakce = frakce

    def zobraz_frakce(self):
        clear()
        print("--- Diplomacie ---")
        for klic, frakce in self.frakce.frakce.items():
            print(f"{klic}: {frakce.nazev} (reputace: {frakce.reputace})")
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
        zakladni_cena = 50
        cena = int(zakladni_cena * (1 + frakce.reputace / 100))
        hrac.gold += cena
        frakce.reputace += random.randint(1, 5)
        tisk_ok(f"Obchodoval jsi s {frakce.nazev}. Zisk {cena} zlaťáků.")
