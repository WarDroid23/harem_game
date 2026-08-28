from data.osudy import OSUDY, OSUDY_PORADI
from utils.vypis import clear, terminalni_obrazek, tisk_chyba, tisk_info, tisk_ok


def vyber_osud(otrok):
    """Vybere stabilní výchozí osud; prázdný osud mají jen staré sejvy."""
    index = (sum(ord(znak) for znak in otrok.jmeno) + otrok.vek) % len(OSUDY_PORADI)
    return OSUDY_PORADI[index]


def zajisti_osudy(harem):
    for otrok in harem.otrokyne:
        if not getattr(otrok, "osud_id", "") or otrok.osud_id not in OSUDY:
            otrok.osud_id = vyber_osud(otrok)
        if not isinstance(getattr(otrok, "osud_volby", []), list):
            otrok.osud_volby = []
        if not isinstance(getattr(otrok, "osud_krok", 0), int):
            otrok.osud_krok = 0
        otrok.osud_krok = max(0, min(otrok.osud_krok, len(OSUDY[otrok.osud_id]["kroky"])))
        if otrok.osud_krok >= len(OSUDY[otrok.osud_id]["kroky"]):
            otrok.osud_dokonceno = True


class OsudySystem:
    def _osud(self, otrok):
        if not getattr(otrok, "osud_id", "") or otrok.osud_id not in OSUDY:
            otrok.osud_id = vyber_osud(otrok)
        if not isinstance(getattr(otrok, "osud_volby", []), list):
            otrok.osud_volby = []
        if not isinstance(getattr(otrok, "osud_krok", 0), int):
            otrok.osud_krok = 0
        otrok.osud_krok = max(0, min(otrok.osud_krok, len(OSUDY[otrok.osud_id]["kroky"])))
        if otrok.osud_krok >= len(OSUDY[otrok.osud_id]["kroky"]):
            otrok.osud_dokonceno = True
        return OSUDY[otrok.osud_id]

    def dalsi_krok(self, otrok):
        osud = self._osud(otrok)
        if otrok.osud_krok >= len(osud["kroky"]):
            return None
        return osud["kroky"][otrok.osud_krok]

    def hotovo(self, otrok):
        return self.dalsi_krok(otrok) is None

    def zvol(self, hra, otrok, index):
        krok = self.dalsi_krok(otrok)
        if krok is None:
            tisk_info(f"Osud {otrok.jmeno} je již uzavřen.")
            return False
        volby = krok["volby"]
        if index < 0 or index >= len(volby):
            tisk_chyba("Neplatná volba osudu.")
            return False

        volba = volby[index]
        podminka = volba.get("podminka", {})
        if "gold" in podminka and hra.hrac.gold < podminka["gold"]:
            tisk_chyba(f"Potřebuješ {podminka['gold']} zlaťáků.")
            return False
        if "item" in podminka and hra.hrac.inventar.pocet_predmetu(podminka["item"]) < 1:
            tisk_chyba("Potřebný předmět nemáš v inventáři.")
            return False

        for typ, hodnota in podminka.items():
            if typ == "gold":
                hra.hrac.gold -= hodnota
            elif typ == "item":
                hra.hrac.inventar.odeber_predmet(hodnota, 1)

        efekty = volba.get("efekty", {})
        staty_otrokyn = {
            "srdce", "poslusnost", "vlhkost", "submisivita", "loajalita",
            "duvera", "touha", "strach", "broken", "mindbreak", "hp",
        }
        for typ, hodnota in efekty.items():
            if typ in staty_otrokyn:
                otrok.zvysit_stat(typ, hodnota)
            elif typ == "gold":
                hra.hrac.gold = max(0, hra.hrac.gold + hodnota)
            elif typ == "xp":
                hra.hrac.pridej_xp(hodnota)
            elif typ == "reputace_mesta":
                hra.hrac.reputace_mesta += hodnota
            elif typ == "vliv_inkvizice":
                hra.hrac.vliv_inkvizice = max(0, min(100, hra.hrac.vliv_inkvizice + hodnota))
            elif typ == "obrana":
                hra.hrac.skilly["obrana"] = hra.hrac.skilly.get("obrana", 0) + hodnota
            elif typ == "mafie_vliv":
                hra.mafie.vliv_ve_meste = max(0, min(100, hra.mafie.vliv_ve_meste + hodnota))
            elif typ == "unlock_location":
                hra.svet.odhal_lokaci(hodnota)

        odmena = volba.get("odmena")
        if odmena:
            hra.hrac.inventar.pridej_predmet(odmena["id"], odmena.get("mnozstvi", 1))

        otrok.osud_volby.append({"krok": otrok.osud_krok, "volba": volba["nazev"]})
        otrok.osud_krok += 1
        if self.hotovo(otrok):
            otrok.osud_dokonceno = True
            otrok.loajalita = min(100, otrok.loajalita + 5)
            tisk_ok(f"Osud {otrok.jmeno} je uzavřen. Získala +5 loajality.")
        else:
            tisk_ok(f"Volba u osudu {otrok.jmeno} byla zaznamenána.")
        return True

    def menu(self, hra, otrok):
        while True:
            clear()
            osud = self._osud(otrok)
            krok = self.dalsi_krok(otrok)
            terminalni_obrazek("osudy")
            print(f"--- Osud: {osud['nazev']} ({otrok.jmeno}) ---")
            print(osud["popis"])
            print(f"Stav: {otrok.osud_krok}/{len(osud['kroky'])} rozhodnutí")
            if krok is None:
                print("\nPříběh je uzavřen.")
                input("Enter...")
                return
            print(f"\n{krok['text']}\n")
            for index, volba in enumerate(krok["volby"], 1):
                print(f"{index}) {volba['nazev']} — {volba['popis']}")
            print("0) Zpět")
            volba = input("> ").strip()
            if volba == "0":
                return
            try:
                if self.zvol(hra, otrok, int(volba) - 1):
                    input("Enter...")
            except ValueError:
                tisk_chyba("Zadej číslo.")
                input("Enter...")
