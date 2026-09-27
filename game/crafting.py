from game.predmety import PREDMETY
from utils.vypis import clear, hlavicka, tisk_chyba, tisk_ok, vytiskni_volbu

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
    "balzam_stinu": {
        "nazev": "Balzám stínů",
        "suroviny": {"bylina_mesicni": 1, "esence_temna": 1, "pelynek": 1},
    },
    "ocelovy_zamek": {
        "nazev": "Ocelový zámek",
        "suroviny": {"krystal_sily": 2, "drací_koren": 1},
    },
    "lucerna_soumraku": {
        "nazev": "Lucerna soumraku",
        "suroviny": {"nocni_stin": 2, "esence_temna": 1},
    },
}


class CraftingSystem:
    def pouzit_predmet(self, hra, predmet_id):
        """Použije podpůrný předmět mimo souboj."""
        predmet = PREDMETY.get(predmet_id)
        if not predmet or not hra.hrac.inventar.odeber_predmet(predmet_id):
            tisk_chyba("Tento předmět nemáš v inventáři.")
            return False
        if predmet.get("boj") == "leceni_temnota":
            hra.hrac.hp = min(hra.hrac.max_hp, hra.hrac.hp + predmet["hodnota"])
            hra.hrac.dark_energy = min(
                hra.hrac.max_temno(), hra.hrac.dark_energy + 8
            )
            tisk_ok(f"Použil jsi {predmet['nazev']}. HP: {hra.hrac.hp}, temná energie: {hra.hrac.dark_energy}.")
        elif predmet_id == "lucerna_soumraku":
            hra.hrac.reputace_mesta = min(100, hra.hrac.reputace_mesta + 2)
            tisk_ok("Lucerna odhalila bezpečné stopy. Reputace města +2.")
        else:
            hra.hrac.inventar.pridej_predmet(predmet_id)
            tisk_chyba("Tento předmět lze použít pouze v odpovídající herní situaci.")
            return False
        return True

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
            hlavicka("Předměty a výroba")
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
            print("\nUžitečné předměty:")
            pouzitelne = [
                predmet_id for predmet_id, predmet in PREDMETY.items()
                if hra.hrac.inventar.pocet_predmetu(predmet_id)
                and (
                    predmet.get("boj") == "leceni_temnota"
                    or predmet_id == "lucerna_soumraku"
                )
            ]
            for index, predmet_id in enumerate(pouzitelne, 1):
                predmet = PREDMETY[predmet_id]
                print(
                    f"U{index}) {predmet['nazev']} "
                    f"x{hra.hrac.inventar.pocet_predmetu(predmet_id)} — {predmet['popis']}"
                )
            vytiskni_volbu('0', 'Zpět')
            volba = input("> ").strip()
            if volba == "0":
                return
            if volba.upper().startswith("U"):
                try:
                    index = int(volba[1:]) - 1
                    if 0 <= index < len(pouzitelne):
                        self.pouzit_predmet(hra, pouzitelne[index])
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Použij například U1.")
                input("Enter...")
                continue
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
