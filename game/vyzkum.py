"""Větvený technologický strom dominia."""

from utils.vypis import clear, nacti_volbu, tisk_ok, tisk_chyba
from config import GOLD, CYAN, GREEN, RED, YELLOW, NC


def _zvys_schopnost(hrac, schopnost, hodnota):
    if not isinstance(getattr(hrac, "skilly", None), dict):
        hrac.skilly = {}
    hrac.skilly[schopnost] = hrac.skilly.get(schopnost, 0) + hodnota


def _temna_magie(hrac):
    if hasattr(hrac, "zvys_max_temno"):
        hrac.zvys_max_temno(20)
        hrac.pridej_dark_energy(20)
    else:
        hrac.max_dark_energy = getattr(hrac, "max_dark_energy", 100) + 20
        hrac.dark_energy = min(hrac.max_dark_energy, hrac.dark_energy + 20)


def _sniz_inkvizici(hrac, hodnota):
    hrac.vliv_inkvizice = max(
        0, getattr(hrac, "vliv_inkvizice", 0) - hodnota
    )


def _pridej_zlato(hrac, hodnota):
    hrac.gold += hodnota


def _vycvik_legie(hrac):
    _zvys_schopnost(hrac, "boj", 2)
    _zvys_schopnost(hrac, "obrana", 2)


def _technologie(vetev, uroven, nazev, popis, cena, efekt, vyzaduje=(),
                 body=10, denni_prijem=0, sleva_vyzkumu=0,
                 bonus_bodu_za_uzemi=0, bonus_prijmu_za_uzemi=0):
    return {
        "vetev": vetev,
        "uroven": uroven,
        "nazev": nazev,
        "popis": popis,
        "cena": cena,
        "body": body,
        "efekt": efekt,
        "vyzaduje": list(vyzaduje),
        "denni_prijem": denni_prijem,
        "sleva_vyzkumu": sleva_vyzkumu,
        "bonus_bodu_za_uzemi": bonus_bodu_za_uzemi,
        "bonus_prijmu_za_uzemi": bonus_prijmu_za_uzemi,
    }


VYZKUM = {
    "temna_magie": _technologie(
        "🌑 Magie", 0, "Temná magie",
        "Zvýší maximální i aktuální temnou energii o 20.",
        300, _temna_magie, body=10,
    ),
    "psychologie_zlomeni": _technologie(
        "🌑 Magie", 1, "Psychologie zlomení",
        "Posílí temné útoky: +5 k dovednosti Temnota.",
        400, lambda h: _zvys_schopnost(h, "temnota", 5),
        ("temna_magie",), body=15,
    ),
    "pokrocile_muceni": _technologie(
        "🌑 Magie", 2, "Pokročilé mučení",
        "Zesílí temné útoky o dalších +5 k dovednosti Temnota.",
        700, lambda h: _zvys_schopnost(h, "temnota", 5),
        ("psychologie_zlomeni",), body=25,
    ),
    "ritualni_rezonance": _technologie(
        "🌑 Magie", 3, "Rituální rezonance",
        "Trvale zvýší maximální temnou energii o 15.",
        950, lambda h: h.zvys_max_temno(15),
        ("pokrocile_muceni",), body=35,
    ),
    "obchodni_sit": _technologie(
        "🪙 Hospodářství", 0, "Obchodní síť",
        "Získáš 50 zlata ihned a síť bude vynášet +15 zlata za každý den.",
        500, lambda h: _pridej_zlato(h, 50), body=10, denni_prijem=15,
    ),
    "investicni_kruh": _technologie(
        "🪙 Hospodářství", 1, "Investiční kruh",
        "Rozšíří pravidelný výnos dominia o +25 zlata za den.",
        650, None, ("obchodni_sit",), body=15, denni_prijem=25,
    ),
    "monopolni_smlouvy": _technologie(
        "🪙 Hospodářství", 2, "Monopolní smlouvy",
        "Uzavře výnosné smlouvy: dalších +40 zlata za každý den.",
        900, None, ("investicni_kruh",), body=25, denni_prijem=40,
    ),
    "ucty_podsveti": _technologie(
        "🪙 Hospodářství", 3, "Účetní knihy podsvětí",
        "Každé ovládané městské území přidá +10 zlata k dennímu výnosu.",
        1250, None, ("monopolni_smlouvy",), body=35,
        bonus_prijmu_za_uzemi=10,
    ),
    "utajeni": _technologie(
        "🕯️ Infiltrace", 0, "Utajení",
        "Zmate vyšetřovatele a okamžitě sníží vliv Inkvizice o 10.",
        250, lambda h: _sniz_inkvizici(h, 10), body=8,
    ),
    "tajne_archivy": _technologie(
        "🕯️ Infiltrace", 1, "Tajné archivy",
        "Získáš přístup ke znalostem; další výzkumy budou stát o 5 % méně zlata.",
        500, None, ("utajeni",), body=12, sleva_vyzkumu=5,
    ),
    "dvojiti_agent": _technologie(
        "🕯️ Infiltrace", 2, "Síť dvojitých agentů",
        "Rozšíří tajné zdroje a sníží zlatou cenu dalších výzkumů o dalších 5 %.",
        800, None, ("tajne_archivy",), body=18, sleva_vyzkumu=5,
    ),
    "sit_informatoru": _technologie(
        "🕯️ Infiltrace", 3, "Síť informátorů",
        "Každé ovládané městské území přidá +1 výzkumný bod za den.",
        1100, None, ("dvojiti_agent",), body=30,
        bonus_bodu_za_uzemi=1,
    ),
    "vojenska_taktika": _technologie(
        "⚔️ Válečnictví", 0, "Vojenská taktika",
        "Zlepší útočné schopnosti: +2 k dovednosti Boj.",
        300, lambda h: _zvys_schopnost(h, "boj", 2), body=10,
    ),
    "disciplinovana_legie": _technologie(
        "⚔️ Válečnictví", 1, "Disciplinovaná legie",
        "Zlepší útok (+2 Boj) i obranu (+2 Obrana).",
        550, _vycvik_legie,
        ("vojenska_taktika",), body=15,
    ),
    "ocelova_elita": _technologie(
        "⚔️ Válečnictví", 2, "Ocelová elita",
        "Vyškolí elitní útočníky: +4 k dovednosti Boj.",
        850, lambda h: _zvys_schopnost(h, "boj", 4),
        ("disciplinovana_legie",), body=25,
    ),
}


class VyzkumSystem:
    def __init__(self):
        self.ziskane = set()
        self.body = 0
        self._hra_ref = None

    def produkce_bodu_za_den(self, hra):
        pevnost = getattr(hra, "pevnost", None)
        budovy = getattr(pevnost, "budovy", {})
        if not isinstance(budovy, dict):
            return 0
        zaklad = (
            max(0, int(budovy.get("archiv", 0))) * 3
            + max(0, int(budovy.get("alchymisticka_laborator", 0)))
        )
        bonus_za_uzemi = sum(
            VYZKUM[id_v]["bonus_bodu_za_uzemi"]
            for id_v in self.ziskane
            if id_v in VYZKUM
        )
        pocet_uzemi = len(getattr(getattr(hra, "mafie", None), "uzemi", []))
        return zaklad + bonus_za_uzemi * pocet_uzemi

    def pridej_body(self, pocet):
        pocet = max(0, int(pocet))
        self.body += pocet
        return pocet

    def sleva_vyzkumu(self, hrac, hra=None):
        hra = hra or self._hra_ref or getattr(hrac, "_hra_ref", None)
        sleva = sum(
            VYZKUM[id_v]["sleva_vyzkumu"]
            for id_v in self.ziskane
            if id_v in VYZKUM
        )
        if hra is not None:
            from game.charakter_bonusy import bonus_vyzkumu
            sleva += bonus_vyzkumu(hra)
        return min(50, sleva)

    def cena_vyzkumu(self, hrac, id_vyzkumu, hra=None):
        if id_vyzkumu not in VYZKUM:
            return 0
        sleva = self.sleva_vyzkumu(hrac, hra)
        return max(1, int(VYZKUM[id_vyzkumu]["cena"] * (100 - sleva) / 100))

    def cena_bodu_vyzkumu(self, id_vyzkumu):
        if id_vyzkumu not in VYZKUM:
            return 0
        return VYZKUM[id_vyzkumu]["body"]

    def bonus_denniho_prijmu(self, hra=None):
        bonus = sum(
            VYZKUM[id_v]["denni_prijem"]
            for id_v in self.ziskane
            if id_v in VYZKUM
        )
        bonus_za_uzemi = sum(
            VYZKUM[id_v]["bonus_prijmu_za_uzemi"]
            for id_v in self.ziskane
            if id_v in VYZKUM
        )
        pocet_uzemi = len(getattr(getattr(hra, "mafie", None), "uzemi", []))
        return bonus + bonus_za_uzemi * pocet_uzemi

    def muzes_vyzkoumat(self, hrac, id_vyzkumu, hra=None):
        if id_vyzkumu not in VYZKUM:
            return False, "Neznámý výzkum."
        if id_vyzkumu in self.ziskane:
            return False, "Již vyzkoumáno."
        vyzkum = VYZKUM[id_vyzkumu]
        for pozadavek in vyzkum["vyzaduje"]:
            if pozadavek not in self.ziskane:
                return False, f"Chybí požadavek: {VYZKUM[pozadavek]['nazev']}"
        cena = self.cena_vyzkumu(hrac, id_vyzkumu, hra)
        cena_body = self.cena_bodu_vyzkumu(id_vyzkumu)
        if self.body < cena_body:
            return False, f"Nedostatek výzkumných bodů (potřeba {cena_body}, máš {self.body})."
        if hrac.gold < cena:
            return False, f"Nedostatek zlata (potřeba {cena})."
        return True, ""

    def vyzkoumat(self, hrac, id_vyzkumu, hra=None):
        mozne, duvod = self.muzes_vyzkoumat(hrac, id_vyzkumu, hra)
        if not mozne:
            tisk_chyba(duvod)
            return False
        vyzkum = VYZKUM[id_vyzkumu]
        cena = self.cena_vyzkumu(hrac, id_vyzkumu, hra)
        cena_body = self.cena_bodu_vyzkumu(id_vyzkumu)
        try:
            if vyzkum["efekt"] is not None:
                vyzkum["efekt"](hrac)
        except Exception as e:
            tisk_chyba(f"Efekt výzkumu selhal: {e}")
            return False
        hrac.gold -= cena
        self.body -= cena_body
        self.ziskane.add(id_vyzkumu)
        tisk_ok(f"Vyzkoumáno: {vyzkum['nazev']}")
        return True

    def _stav(self, id_vyzkumu):
        if id_vyzkumu in self.ziskane:
            return f"{GREEN}✔ Vyzkoumáno{NC}"
        if all(p in self.ziskane for p in VYZKUM[id_vyzkumu]["vyzaduje"]):
            return f"{YELLOW}◆ Dostupné{NC}"
        return f"{RED}🔒 Uzamčeno{NC}"

    def zobraz_vyzkum(self, hrac, hra=None):
        clear()
        print(f"{GOLD}--- Technologický strom dominia ---{NC}")
        print(
            f"Zlato: {hrac.gold} 🪙 | "
            f"Výzkumné body: {self.body} 🔬 | "
            f"Pokrok: {len(self.ziskane & VYZKUM.keys())}/{len(VYZKUM)}"
        )
        if hra is not None:
            produkce = self.produkce_bodu_za_den(hra)
            print(f"Produkce: +{produkce} výzkumných bodů za den (archiv, laboratoř a případné bonusy čtvrtí)")
        sleva = self.sleva_vyzkumu(hrac, hra)
        if sleva:
            print(f"🔬 Sleva na výzkum: {sleva} %")
        print(
            f"{GREEN}✔ Vyzkoumáno{NC}  "
            f"{YELLOW}◆ Dostupné{NC}  "
            f"{RED}🔒 Uzamčeno{NC}\n"
        )
        poradi = list(VYZKUM)
        vetev_predchozi = None
        for index, id_vyzkumu in enumerate(poradi, 1):
            vyzkum = VYZKUM[id_vyzkumu]
            if vyzkum["vetev"] != vetev_predchozi:
                vetev_predchozi = vyzkum["vetev"]
                print(f"\n{CYAN}{vyzkum['vetev']}{NC}")
            odsazeni = "   " * vyzkum["uroven"]
            spojka = "└─ " if vyzkum["uroven"] else ""
            cena = self.cena_vyzkumu(hrac, id_vyzkumu, hra)
            print(
                f"{odsazeni}{spojka}{index:>2}) {self._stav(id_vyzkumu)} "
                f"{vyzkum['nazev']} ({self.cena_bodu_vyzkumu(id_vyzkumu)} 🔬 + {cena} 🪙)"
            )
            print(f"{odsazeni}   {vyzkum['popis']}")
            if vyzkum["vyzaduje"] and id_vyzkumu not in self.ziskane:
                chybi = [
                    VYZKUM[p]["nazev"] for p in vyzkum["vyzaduje"]
                    if p not in self.ziskane
                ]
                if chybi:
                    print(f"{odsazeni}   Předpoklad: {', '.join(chybi)}")
        print()

    def menu(self, hra):
        hrac = hra.hrac if hasattr(hra, "hrac") else hra
        if hasattr(hra, "hrac"):
            self._hra_ref = hra
        ids = list(VYZKUM)
        while True:
            self.zobraz_vyzkum(hrac, hra if hasattr(hra, "hrac") else None)
            print("Zadej číslo nebo id technologie (0 = zpět)")
            platne_volby = {
                "", "0", "q", *VYZKUM,
                *(str(index) for index in range(1, len(ids) + 1)),
            }
            try:
                volba = nacti_volbu(
                    platne_volby,
                    chybova_zprava="Neznámý výzkum nebo špatné číslo.",
                )
            except EOFError:
                return
            if volba in ("0", "q", ""):
                return
            if volba.isdigit():
                idx = int(volba) - 1
                id_v = ids[idx]
            elif volba in VYZKUM:
                id_v = volba
            self.vyzkoumat(hrac, id_v, hra if hasattr(hra, "hrac") else None)
            try:
                input("Enter...")
            except EOFError:
                return

    def to_dict(self):
        return {"ziskane": sorted(self.ziskane), "body": self.body}

    @classmethod
    def from_dict(cls, data):
        vyzkum = cls()
        if isinstance(data, dict) and isinstance(data.get("ziskane"), list):
            vyzkum.ziskane = {
                id_v for id_v in data["ziskane"]
                if isinstance(id_v, str) and id_v in VYZKUM
            }
        if isinstance(data, dict):
            try:
                vyzkum.body = max(0, int(data.get("body", 0)))
            except (TypeError, ValueError):
                vyzkum.body = 0
        return vyzkum
