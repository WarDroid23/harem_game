from dataclasses import dataclass, field

from utils.vypis import clear, tisk_chyba, tisk_info, tisk_ok

LOKACE = {
    "pevnost": {
        "nazev": "Černá pevnost",
        "popis": "Bezpečné zázemí tvého harému a výchozí bod výprav.",
        "sousedni": ["trh", "les"],
        "uroven": 1,
    },
    "trh": {
        "nazev": "Starý trh",
        "popis": "Obchodníci, překupníci a lidé, kteří slyší víc, než říkají.",
        "sousedni": ["pevnost", "pristav", "ctvrt_remeselniku"],
        "uroven": 1,
    },
    "les": {
        "nazev": "Mlžný les",
        "popis": "Zkratka k hranici, kde se ztrácejí karavany.",
        "sousedni": ["pevnost", "hranice"],
        "uroven": 2,
    },
    "pristav": {
        "nazev": "Černý přístav",
        "popis": "Místo pašeráků, lodí a zpráv z dalekých zemí.",
        "sousedni": ["trh"],
        "uroven": 2,
    },
    "hranice": {
        "nazev": "Hraniční ves",
        "popis": "Vesničané potřebují ochranu před nájezdy.",
        "sousedni": ["les"],
        "uroven": 3,
    },
    "ctvrt_remeselniku": {
        "nazev": "Čtvrť řemeslníků",
        "popis": "Dílny, cechy a lidé, kteří umí proměnit suroviny v užitečné vybavení.",
        "sousedni": ["trh"],
        "uroven": 2,
    },
}

NPC = {
    "mira": {
        "jmeno": "Mira, potulná léčitelka",
        "popis": "Pomáhá zraněným bez ohledu na jejich minulost.",
        "lokace": "trh",
    },
    "radan": {
        "jmeno": "Radan, pašerák",
        "popis": "Zná tajné stezky a shání vzácné suroviny.",
        "lokace": "pristav",
    },
    "elian": {
        "jmeno": "Elian, městský informátor",
        "popis": "Vyměňuje zprávy za laskavosti a opatrnost.",
        "lokace": "trh",
    },
}


@dataclass
class SvetSystem:
    aktualni_lokace: str = "pevnost"
    odhalene_lokace: list = field(default_factory=lambda: ["pevnost", "trh", "les"])
    navstiveno: dict = field(default_factory=dict)
    vztahy_npc: dict = field(default_factory=lambda: {k: 0 for k in NPC})

    def __post_init__(self):
        if self.aktualni_lokace not in LOKACE:
            self.aktualni_lokace = "pevnost"
        self.odhalene_lokace = [
            k for k in self.odhalene_lokace if k in LOKACE
        ] or ["pevnost"]
        if "pevnost" not in self.odhalene_lokace:
            self.odhalene_lokace.insert(0, "pevnost")
        self.vztahy_npc = {
            k: max(-100, min(100, int(self.vztahy_npc.get(k, 0))))
            for k in NPC
        }

    def odhal_lokaci(self, lokace):
        if lokace in LOKACE and lokace not in self.odhalene_lokace:
            self.odhalene_lokace.append(lokace)
            return True
        return False

    def zmen_vztah(self, npc_id, delta):
        if npc_id not in NPC:
            return False
        self.vztahy_npc[npc_id] = max(-100, min(100, self.vztahy_npc[npc_id] + delta))
        return True

    def cestuj(self, cil):
        if cil not in LOKACE or cil not in self.odhalene_lokace:
            tisk_chyba("Tato lokace zatím není dostupná.")
            return False
        if cil != self.aktualni_lokace and cil not in LOKACE[self.aktualni_lokace]["sousedni"]:
            tisk_chyba("Z této lokace tam nevede bezpečná cesta.")
            return False
        self.aktualni_lokace = cil
        self.navstiveno[cil] = self.navstiveno.get(cil, 0) + 1
        tisk_ok(f"Dorazil jsi do lokace: {LOKACE[cil]['nazev']}.")
        return True

    def npc_v_lokaci(self):
        return [
            (npc_id, data) for npc_id, data in NPC.items()
            if data["lokace"] == self.aktualni_lokace
        ]

    def to_dict(self):
        return {
            "aktualni_lokace": self.aktualni_lokace,
            "odhalene_lokace": self.odhalene_lokace,
            "navstiveno": self.navstiveno,
            "vztahy_npc": self.vztahy_npc,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            aktualni_lokace=data.get("aktualni_lokace", "pevnost"),
            odhalene_lokace=data.get("odhalene_lokace", ["pevnost", "trh", "les"]),
            navstiveno=data.get("navstiveno", {}) if isinstance(data.get("navstiveno", {}), dict) else {},
            vztahy_npc=data.get("vztahy_npc", {}) if isinstance(data.get("vztahy_npc", {}), dict) else {},
        )

    def menu(self, hra):
        while True:
            clear()
            lokace = LOKACE[self.aktualni_lokace]
            print(f"--- Mapa a vztahy ---\n")
            print(f"Pozice: {lokace['nazev']}")
            print(lokace["popis"])
            print("\nDostupné lokace:")
            dostupne = [
                cil for cil in lokace["sousedni"]
                if cil in self.odhalene_lokace
            ]
            for index, cil in enumerate(dostupne, 1):
                print(f"{index}) {LOKACE[cil]['nazev']}")
            print("\nNPC v okolí:")
            npc_v_lokaci = self.npc_v_lokaci()
            if npc_v_lokaci:
                for npc_id, npc in npc_v_lokaci:
                    print(f"  {npc['jmeno']} (vztah {self.vztahy_npc[npc_id]:+d})")
            else:
                print("  Nikdo známý.")
            print("\n1-9) Cestovat  |  N) setkat se s NPC  |  0) Zpět")
            volba = input("> ").strip().lower()
            if volba == "0":
                return
            if volba == "n":
                self.menu_npc(hra)
                continue
            try:
                index = int(volba) - 1
                if 0 <= index < len(dostupne):
                    self.cestuj(dostupne[index])
                    input("Enter...")
                else:
                    tisk_chyba("Špatná volba.")
                    input("Enter...")
            except ValueError:
                tisk_chyba("Zadej číslo nebo N.")
                input("Enter...")

    def menu_npc(self, hra):
        npc_v_lokaci = self.npc_v_lokaci()
        if not npc_v_lokaci:
            tisk_info("V této lokaci nikoho známého nenajdeš.")
            input("Enter...")
            return
        print()
        for index, (npc_id, npc) in enumerate(npc_v_lokaci, 1):
            print(f"{index}) {npc['jmeno']} (vztah {self.vztahy_npc[npc_id]:+d})")
        print("0) Zpět")
        try:
            index = int(input("> ")) - 1
        except ValueError:
            tisk_chyba("Zadej číslo.")
            input("Enter...")
            return
        if index < 0:
            return
        if index >= len(npc_v_lokaci):
            tisk_chyba("Špatná volba.")
            input("Enter...")
            return
        npc_id, npc = npc_v_lokaci[index]
        print(f"\n{npc['jmeno']}: {npc['popis']}")
        print("1) Přátelsky si promluvit  2) Požádat o službu  3) Nabídnout pomoc")
        akce = input("> ").strip()
        vztah = self.vztahy_npc[npc_id]
        if akce == "1":
            self.zmen_vztah(npc_id, 4)
            hra.hrac.reputace_mesta += 1
            tisk_ok(f"{npc['jmeno']} si tě zapamatoval. Vztah +4.")
        elif akce == "2":
            if npc_id == "mira":
                hra.hrac.hp = min(hra.hrac.max_hp, hra.hrac.hp + 25)
                self.zmen_vztah(npc_id, 3)
                tisk_ok("Mira tě ošetřila. HP +25, vztah +3.")
            elif npc_id == "radan":
                hra.alchymie.pridat_surovinu("nocni_stin", 1)
                self.zmen_vztah(npc_id, 3)
                tisk_ok("Radan ti předal Noční stín. Vztah +3.")
            else:
                hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 3)
                self.zmen_vztah(npc_id, 3)
                tisk_ok("Elian odvedl pozornost stráží. Vliv inkvizice -3.")
        elif akce == "3":
            if vztah < -20:
                self.zmen_vztah(npc_id, -4)
                tisk_chyba("NPC ti nevěří a nabídku odmítl.")
            else:
                hra.hrac.gold += 30
                self.zmen_vztah(npc_id, 6)
                tisk_ok("Pomohl jsi NPC s její prací. Získal jsi 30 zlata, vztah +6.")
        else:
            tisk_chyba("Neplatná volba.")
        input("Enter...")
