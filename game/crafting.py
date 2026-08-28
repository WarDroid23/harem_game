from game.predmety import PREDMETY
from utils.vypis import clear, tisk_chyba, tisk_ok

RECEPTY_PREDMETU = {
    "zdravotni_balicek": {
        "nazev": "Zdravotní balíček",
        "suroviny": {"bylina_mesicni": 2, "vzacna_houba": 1},
    },
    "elixir_temnoty": {
        "nazev": "Elixír temnoty",
        "suroviny": {"esence_temna": 2, "pelynek": 1},
    },
    "dymovnice": {
        "nazev": "Dýmovnice",
        "suroviny": {"nocni_stin": 1, "pelynek": 2},
    },
    "opravarenska_sada": {
        "nazev": "Opravárenská sada",
        "suroviny": {"krystal_sily": 1, "drací_koren": 1},
    },
}


class CraftingSystem:
    def vyrobit(self, hra, predmet_id):
        recept = RECEPTY_PREDMETU.get(predmet_id)
        if not recept:
            tisk_chyba("Neznámý recept.")
            return False
        for surovina, mnozstvi in recept["suroviny"].items():
            if hra.alchymie.suroviny.get(surovina, 0) < mnozstvi:
                tisk_chyba(f"Nedostatek suroviny: {surovina} (potřeba {mnozstvi}).")
                return False
        for surovina, mnozstvi in recept["suroviny"].items():
            hra.alchymie.odeber_surovinu(surovina, mnozstvi)
        hra.hrac.inventar.pridej_predmet(predmet_id)
        tisk_ok(f"Vyrobeno: {PREDMETY[predmet_id]['nazev']}.")
        return True

    def menu(self, hra):
        while True:
            clear()
            print("--- Předměty a výroba ---\n")
            print("Inventář:")
            inventar = hra.hrac.inventar.seznam_predmetu()
            if inventar:
                for polozka in inventar:
                    print(f"  {polozka}")
            else:
                print("  (prázdný)")
            print("\nRecepty:")
            ids = list(RECEPTY_PREDMETU)
            for index, predmet_id in enumerate(ids, 1):
                recept = RECEPTY_PREDMETU[predmet_id]
                suroviny = ", ".join(f"{s} x{m}" for s, m in recept["suroviny"].items())
                print(f"{index}) {recept['nazev']} — {suroviny}")
            print("0) Zpět")
            volba = input("> ").strip()
            if volba == "0":
                return
            try:
                index = int(volba) - 1
                if 0 <= index < len(ids):
                    self.vyrobit(hra, ids[index])
                    input("Enter...")
                else:
                    tisk_chyba("Špatná volba.")
                    input("Enter...")
            except ValueError:
                tisk_chyba("Zadej číslo.")
                input("Enter...")
