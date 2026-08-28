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
    {
        "nazev": "Zahrada tichých slibů",
        "popis": "Najdi místo, kde mohou spojenci mluvit otevřeně a bez nátlaku.",
        "cil": "navstiv_zahradu",
        "lokace": "sklenena_zahrada",
    },
    {
        "nazev": "Hvězdný tribunál",
        "popis": "Poraz Strážce hvězdné brány a rozhodni, jakou budoucnost nabídneš svým spojencům.",
        "cil": "uzavri_hvezdny_slib",
        "lokace": "observator",
    },
)


@dataclass
class KampanSystem:
    kapitola: int = 0
    splnene_cile: list = field(default_factory=list)
    volby: list = field(default_factory=list)
    boss_porazeni: list = field(default_factory=list)
    dokonceno: bool = False
    zaver: str = ""

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
        elif kapitola["cil"] == "navstiv_zahradu" and hra.svet.navstiveno.get("sklenena_zahrada", 0):
            hra.svet.odhal_lokaci("observator")
            self.splnene_cile.append(kapitola["cil"])
            hra.hrac.pridej_xp(55)
            tisk_ok("Zahrada odhalila cestu k observatoři. Nová kapitola začíná.")
            self.kapitola += 1

    def urci_zaver(self, hra):
        """Vyhodnotí reputaci, vztahy a zásadní rozhodnutí kampaně."""
        npc_vztahy = list(hra.svet.vztahy_npc.values())
        prumer_npc = sum(npc_vztahy) / len(npc_vztahy) if npc_vztahy else 0
        aktivni = hra.harem.vsechny_aktivni()
        prumer_harem = (
            sum(o.loajalita + o.duvera + o.romance_body for o in aktivni)
            / (3 * len(aktivni))
            if aktivni else 0
        )
        volby = {volba.get("volba") for volba in self.volby if isinstance(volba, dict)}
        if (
            hra.hrac.reputace_mesta >= 25
            and prumer_npc >= 20
            and prumer_harem >= 35
            and "spolecna_cesta" in volby
        ):
            return "Sjednocené město"
        if (
            hra.hrac.reputace_mesta <= -10
            or hra.mafie.vliv_ve_meste >= 65
            or "vyuzit" in volby
        ):
            return "Vláda stínů"
        return "Křehký mír"
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
            hra.svet.odhal_lokaci("sklenena_zahrada")
            self.kapitola += 1
            self.dokonceno = False
            tisk_ok("Síť je uzavřena, ale příběh pokračuje. Na mapě se objevila Skleněná zahrada.")
            return True
        if kapitola["cil"] == "navstiv_zahradu":
            if not hra.svet.navstiveno.get("sklenena_zahrada", 0):
                tisk_chyba("Nejdřív navštiv Skleněnou zahradu.")
                return False
            hra.svet.odhal_lokaci("observator")
            self.splnene_cile.append(kapitola["cil"])
            hra.hrac.pridej_xp(55)
            self.kapitola += 1
            tisk_ok("Cesta k observatoři je otevřená.")
            return True
        if kapitola["cil"] == "uzavri_hvezdny_slib":
            if hra.svet.aktualni_lokace != "observator":
                tisk_chyba("Rozhodnutí můžeš učinit až v observatoři.")
                return False
            if "strazce_hvezdne_brany" not in self.boss_porazeni:
                tisk_chyba("Nejdřív poraz Strážce hvězdné brány.")
                return False
            volba_id = ("spolecna_cesta", "samostatne_cesty")[index]
            self.volby.append({"kapitola": self.kapitola, "volba": volba_id})
            self.splnene_cile.append(kapitola["cil"])
            if index == 0:
                hra.hrac.reputace_mesta += 10
                hra.hrac.sex_energy = min(100, hra.hrac.sex_energy + 20)
                tisk_ok("Zvolil jsi společnou cestu založenou na důvěře a vzájemném souhlasu.")
            else:
                hra.hrac.reputace_mesta += 6
                hra.hrac.dark_energy = min(100, hra.hrac.dark_energy + 25)
                tisk_ok("Podpořil jsi samostatnost spojenců; návraty budou mít větší váhu.")
            hra.hrac.pridej_xp(120)
            self.kapitola += 1
            self.dokonceno = True
            self.zaver = self.urci_zaver(hra)
            popisy = {
                "Sjednocené město": "Spojenci vytvořili městskou alianci založenou na důvěře.",
                "Vláda stínů": "Město se uklonilo síti vlivu a pevnost ovládá podsvětí.",
                "Křehký mír": "Podařilo se odvrátit nejhorší, ale důvěra se bude teprve stavět.",
            }
            tisk_ok(f"Hvězdný tribunál je uzavřen. Konec: {self.zaver}.")
            tisk_info(popisy[self.zaver])
            return True
        return False

    def to_dict(self):
        return {
            "kapitola": self.kapitola,
            "splnene_cile": self.splnene_cile,
            "volby": self.volby,
            "boss_porazeni": self.boss_porazeni,
            "dokonceno": self.dokonceno,
            "zaver": self.zaver,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        try:
            kapitola = int(data.get("kapitola", 0))
        except (TypeError, ValueError):
            kapitola = 0
        kapitola = max(0, min(len(KAPITOLY), kapitola))
        dokonceno = bool(data.get("dokonceno", False))
        # Starší verze končily po kapitole 3; jejich save dostane pokračování.
        if dokonceno and kapitola < len(KAPITOLY):
            dokonceno = False
        return cls(
            kapitola=kapitola,
            splnene_cile=data.get("splnene_cile", []) if isinstance(data.get("splnene_cile", []), list) else [],
            volby=data.get("volby", []) if isinstance(data.get("volby", []), list) else [],
            boss_porazeni=data.get("boss_porazeni", []) if isinstance(data.get("boss_porazeni", []), list) else [],
            dokonceno=dokonceno,
            zaver=data.get("zaver", "") if isinstance(data.get("zaver", ""), str) else "",
        )

    def menu(self, hra):
        self.zkontroluj_postup(hra)
        while True:
            clear()
            print("--- Příběhová kampaň ---\n")
            kapitola = self.aktualni()
            if not kapitola:
                print(f"Kampaň je dokončena. Konec: {self.zaver or 'nevyhodnocen'}")
                input("Enter...")
                return
            print(f"Kapitola {self.kapitola + 1}/{len(KAPITOLY)}: {kapitola['nazev']}")
            print(kapitola["popis"])
            print(f"Cíl: navštívit {LOKACE[kapitola['lokace']]['nazev']}")
            if kapitola["cil"] in ("navstiv_trh", "navstiv_zahradu"):
                print(f"\nCestuj do lokace {LOKACE[kapitola['lokace']]['nazev']} a prozkoumej okolí.")
                print("1) Zpět na mapu")
            elif kapitola["cil"] == "vyber_spojence":
                print("\n1) Požádat Miru o pomoc (reputace a péče)")
                print("2) Požádat Radana o pomoc (temná energie a zásoby)")
            elif kapitola["cil"] == "uzavri_hvezdny_slib":
                print("\n1) Pokračovat společně, s jasnými hranicemi a vzájemnou volbou")
                print("2) Podpořit samostatné cesty a setkávat se bez vlastnění")
            else:
                print("\n1) Odhalit síť a očistit město")
                print("2) Využít síť a posílit vlastní vliv")
            print("0) Zpět")
            volba = input("> ").strip()
            if volba == "0":
                return
            if kapitola["cil"] in ("navstiv_trh", "navstiv_zahradu"):
                tisk_info(f"Otevři mapu a vydej se do lokace: {LOKACE[kapitola['lokace']]['nazev']}.")
                input("Enter...")
            elif kapitola["cil"] == "uzavri_hvezdny_slib":
                print("\n1) Pokračovat společně, s jasnými hranicemi a vzájemnou volbou")
                print("2) Podpořit samostatné cesty a setkávat se bez vlastnění")
                try:
                    if self.zvol(hra, int(volba) - 1):
                        input("Enter...")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
                    input("Enter...")
            else:
                try:
                    if self.zvol(hra, int(volba) - 1):
                        input("Enter...")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
                    input("Enter...")
