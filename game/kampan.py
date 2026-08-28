from dataclasses import dataclass, field

from game.svet import LOKACE
from utils.vypis import clear, tisk_chyba, tisk_info, tisk_ok

KAPITOLY = (
    {
        "nazev": "Popel pod branou",
        "popis": "Zjisti, proč se v okolí pevnosti ztrácejí lidé a zásoby.",
        "cil": "navstiv_trh",
        "lokace": "trh",
    },
    {
        "nazev": "Cena spojenectví",
        "popis": "Vyber si spojence, který pomůže udržet pevnost v bezpečí.",
        "cil": "vyber_spojence",
        "lokace": "pristav",
    },
    {
        "nazev": "Noc dlouhých stínů",
        "popis": "Rozhodni, zda odhalíš síť pašeráků, nebo ji využiješ k záchraně města.",
        "cil": "uzavri_kampan",
        "lokace": "hranice",
    },
)


@dataclass
class KampanSystem:
    kapitola: int = 0
    splnene_cile: list = field(default_factory=list)
    volby: list = field(default_factory=list)
    dokonceno: bool = False

    def aktualni(self):
        if self.dokonceno or self.kapitola >= len(KAPITOLY):
            return None
        return KAPITOLY[self.kapitola]

    def zkontroluj_postup(self, hra):
        kapitola = self.aktualni()
        if not kapitola:
            return
        if kapitola["cil"] == "navstiv_trh" and hra.svet.navstiveno.get("trh", 0):
            hra.svet.odhal_lokaci("pristav")
            self.splnene_cile.append(kapitola["cil"])
            hra.hrac.pridej_xp(25)
            tisk_ok("Kapitola dokončena. Přístav je nyní dostupný.")
            self.kapitola += 1

    def zvol(self, hra, index):
        kapitola = self.aktualni()
        if not kapitola:
            tisk_info("Kampaň je dokončena.")
            return False
        if index not in (0, 1):
            tisk_chyba("Neplatná volba.")
            return False
        if kapitola["cil"] == "navstiv_trh":
            if not hra.svet.navstiveno.get("trh", 0):
                tisk_chyba("Nejdřív navštiv Starý trh.")
                return False
            self.splnene_cile.append(kapitola["cil"])
            hra.svet.odhal_lokaci("pristav")
            hra.hrac.pridej_xp(25)
            self.kapitola += 1
            tisk_ok("Kapitola dokončena. Přístav je nyní dostupný.")
            return True
        if kapitola["cil"] == "vyber_spojence":
            npc_id = ("mira", "radan")[index]
            hra.svet.zmen_vztah(npc_id, 15)
            hra.hrac.reputace_mesta += 5 if index == 0 else 0
            hra.hrac.dark_energy = min(100, hra.hrac.dark_energy + (0 if index == 0 else 15))
            hra.svet.odhal_lokaci("hranice")
            self.volby.append({"kapitola": self.kapitola, "volba": npc_id})
            self.splnene_cile.append(kapitola["cil"])
            hra.hrac.pridej_xp(40)
            self.kapitola += 1
            tisk_ok(f"Zvolil jsi spojence: {npc_id}. Hraniční ves je dostupná.")
            return True
        if kapitola["cil"] == "uzavri_kampan":
            if hra.svet.navstiveno.get("hranice", 0) == 0:
                tisk_chyba("Nejdřív navštiv Hraniční ves.")
                return False
            self.volby.append({"kapitola": self.kapitola, "volba": "odhalit" if index == 0 else "vyuzit"})
            self.splnene_cile.append(kapitola["cil"])
            if index == 0:
                hra.hrac.reputace_mesta += 12
                hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 8)
                hra.hrac.inventar.pridej_predmet("dukazni_listina")
            else:
                hra.hrac.gold += 220
                hra.mafie.vliv_ve_meste = min(100, hra.mafie.vliv_ve_meste + 10)
            hra.hrac.pridej_xp(80)
            self.kapitola += 1
            self.dokonceno = True
            tisk_ok("Kampaň dokončena. Tvé rozhodnutí změnilo poměry ve městě.")
            return True
        return False

    def to_dict(self):
        return {
            "kapitola": self.kapitola,
            "splnene_cile": self.splnene_cile,
            "volby": self.volby,
            "dokonceno": self.dokonceno,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            kapitola=max(0, min(len(KAPITOLY), int(data.get("kapitola", 0)))),
            splnene_cile=data.get("splnene_cile", []) if isinstance(data.get("splnene_cile", []), list) else [],
            volby=data.get("volby", []) if isinstance(data.get("volby", []), list) else [],
            dokonceno=bool(data.get("dokonceno", False)),
        )

    def menu(self, hra):
        self.zkontroluj_postup(hra)
        while True:
            clear()
            print("--- Příběhová kampaň ---\n")
            kapitola = self.aktualni()
            if not kapitola:
                print("Kampaň je dokončena.")
                input("Enter...")
                return
            print(f"Kapitola {self.kapitola + 1}/{len(KAPITOLY)}: {kapitola['nazev']}")
            print(kapitola["popis"])
            print(f"Cíl: navštívit {LOKACE[kapitola['lokace']]['nazev']}")
            if kapitola["cil"] == "navstiv_trh":
                print("\nCestuj na trh a prozkoumej okolí.")
                print("1) Zpět na mapu")
            elif kapitola["cil"] == "vyber_spojence":
                print("\n1) Požádat Miru o pomoc (reputace a péče)")
                print("2) Požádat Radana o pomoc (temná energie a zásoby)")
            else:
                print("\n1) Odhalit síť a očistit město")
                print("2) Využít síť a posílit vlastní vliv")
            print("0) Zpět")
            volba = input("> ").strip()
            if volba == "0":
                return
            if kapitola["cil"] == "navstiv_trh":
                tisk_info("Otevři mapu a vydej se na Starý trh.")
                input("Enter...")
            else:
                try:
                    if self.zvol(hra, int(volba) - 1):
                        input("Enter...")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
                    input("Enter...")
