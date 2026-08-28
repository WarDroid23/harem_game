from utils.vypis import clear, tisk_chyba, tisk_ok
from models.fortress import PEVNOSTNI_BUDOVY


def spravovat_pevnost(hra):
    while True:
        clear()
        pevnost = hra.pevnost
        print("--- Rozvoj pevnosti ---")
        print(f"Úroveň: {pevnost.uroven} | Zásoby: {pevnost.zasoby} | Zlato: {hra.hrac.gold}")
        for ident, data in PEVNOSTNI_BUDOVY.items():
            uroven = pevnost.budovy.get(ident, 0)
            print(f"{ident}) {data['nazev']} úroveň {uroven} — {pevnost.cena_vylepseni(ident)} zlata")
        print("U) Vylepšit úroveň pevnosti | 0) Zpět")
        volba = input("> ").strip().lower()
        if volba == "0":
            return
        ident = None if volba == "u" else volba
        cena = pevnost.cena_vylepseni(ident)
        if cena is None:
            tisk_chyba("Neznámá budova.")
        elif hra.hrac.gold < cena:
            tisk_chyba("Nedostatek zlata.")
        elif pevnost.vylepsi(ident, hra.hrac.gold):
            hra.hrac.gold -= cena
            if hasattr(hra, "achievementy"):
                hra.achievementy.zaznamenej("stavba")
            tisk_ok("Pevnost se rozšířila a bonusy jsou aktivní.")
        input("Enter...")
