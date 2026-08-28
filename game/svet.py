from dataclasses import dataclass, field

from utils.vypis import clear, terminalni_obrazek, tisk_chyba, tisk_info, tisk_ok

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
        "sousedni": [
            "pevnost", "pristav", "ctvrt_remeselniku", "hostinec", "lazne",
            "akademie"
        ],
        "uroven": 1,
    },
    "les": {
        "nazev": "Mlžný les",
        "popis": "Zkratka k hranici, kde se ztrácejí karavany.",
        "sousedni": ["pevnost", "hranice", "haj_soumraku"],
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
        "sousedni": ["trh", "akademie"],
        "uroven": 2,
    },
    "hostinec": {
        "nazev": "Hostinec U Tří svící",
        "popis": "Rušný hostinec, kde se najíš, vyspíš a zaslechneš nové zvěsti.",
        "sousedni": ["trh", "lazne"],
        "uroven": 1,
    },
    "lazne": {
        "nazev": "Městské lázně",
        "popis": "Teplé prameny obnovují sílu poutníkům i vládcům.",
        "sousedni": ["trh", "hostinec", "haj_soumraku"],
        "uroven": 1,
    },
    "haj_soumraku": {
        "nazev": "Háj soumraku",
        "popis": "Tiché místo mezi lesem a prameny, vhodné k meditaci a temným rituálům.",
        "sousedni": ["les", "lazne"],
        "uroven": 2,
    },
    "akademie": {
        "nazev": "Alchymistická akademie",
        "popis": "Učenci zde zkoumají esence a vyměňují je za vzácné suroviny.",
        "sousedni": ["ctvrt_remeselniku", "trh"],
        "uroven": 2,
    },
    "sklenena_zahrada": {
        "nazev": "Skleněná zahrada",
        "popis": "Zastřešená zahrada plná světla, kde se dá mluvit bez publika a beze spěchu.",
        "sousedni": ["lazne", "akademie", "observator"],
        "uroven": 2,
    },
    "observator": {
        "nazev": "Observatoř severní věže",
        "popis": "Staré čočky ukazují cesty, které město raději zapomnělo.",
        "sousedni": ["sklenena_zahrada", "hranice"],
        "uroven": 3,
    },
    "molo_mesicniho_pristavu": {
        "nazev": "Molo Měsíčního přístavu",
        "popis": "Tiché molo na okraji přístavu, kde se uzavírají dohody a loučí se s minulostí.",
        "sousedni": ["pristav", "observator"],
        "uroven": 3,
    },
}

VYCHOZI_ODHALENE = [
    "pevnost", "trh", "les", "hostinec", "lazne", "haj_soumraku", "akademie"
]

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
    "borin": {
        "jmeno": "Borin, hostinský",
        "popis": "Dobrosrdečný hostinský, který pozná poutníka podle kroku.",
        "lokace": "hostinec",
    },
    "velena": {
        "jmeno": "Velena, správkyně lázní",
        "popis": "Pečuje o prameny a nabízí léčivou proceduru za rozumnou cenu.",
        "lokace": "lazne",
    },
    "sava": {
        "jmeno": "Sava, strážkyně háje",
        "popis": "Mlčenlivá strážkyně, která učí soustředění a zná sílu nočního stínu.",
        "lokace": "haj_soumraku",
    },
    "nela": {
        "jmeno": "Nela, mladá alchymistka",
        "popis": "Hledá pomocníky pro své pokusy a odměňuje je užitečnými esencemi.",
        "lokace": "akademie",
    },
    "lyra": {
        "jmeno": "Lyra, kartografka hvězd",
        "popis": "Dospělá kartografka, která kreslí bezpečné cesty i mapy lidské důvěry.",
        "lokace": "sklenena_zahrada",
        "vek": 29,
        "dialogy": [
            "Když člověk zná svou cestu, nemusí nikoho vlastnit, aby nebyl sám.",
            "Můžeme mluvit o tom, co chceme, až když stejně dobře umíme říct ne.",
        ],
    },
    "cassian": {
        "jmeno": "Cassian, správce observatoře",
        "popis": "Dospělý správce věže, který chrání její archiv před lidmi toužícími po moci.",
        "lokace": "observator",
        "vek": 34,
        "dialogy": [
            "Hvězdy nejsou věštba. Jsou připomínka, že i dlouhá noc jednou skončí.",
            "Archiv otevřu jen těm, kdo unesou pravdu bez toho, aby ji použili proti druhým.",
        ],
    },
    "tereza": {
        "jmeno": "Tereza, kapitánka měsíčního mola",
        "popis": "Dospělá kapitánka, která dává posádce druhou šanci a jasné hranice.",
        "lokace": "molo_mesicniho_pristavu",
        "vek": 31,
        "dialogy": [
            "Důvěra se nevyžaduje rozkazem. Staví se z malých rozhodnutí, která platí i zítra.",
            "Pokud chceš plout se mnou, řekni mi nejdřív, kam skutečně míříš.",
        ],
    },
}


@dataclass
class SvetSystem:
    aktualni_lokace: str = "pevnost"
    odhalene_lokace: list = field(default_factory=lambda: list(VYCHOZI_ODHALENE))
    navstiveno: dict = field(default_factory=dict)
    vztahy_npc: dict = field(default_factory=lambda: {k: 0 for k in NPC})

    def __post_init__(self):
        if not isinstance(self.aktualni_lokace, str) or self.aktualni_lokace not in LOKACE:
            self.aktualni_lokace = "pevnost"
        puvodni_lokace = self.odhalene_lokace
        if not isinstance(puvodni_lokace, list):
            puvodni_lokace = []
        self.odhalene_lokace = [
            k for k in puvodni_lokace if k in LOKACE
        ]
        # Nové lokace se přidají i do starších savů, které mapu ještě neměly.
        for lokace in VYCHOZI_ODHALENE:
            if lokace not in self.odhalene_lokace:
                self.odhalene_lokace.append(lokace)
        if not self.odhalene_lokace:
            self.odhalene_lokace = ["pevnost"]
        if "pevnost" not in self.odhalene_lokace:
            self.odhalene_lokace.insert(0, "pevnost")
        puvodni_vztahy = self.vztahy_npc if isinstance(self.vztahy_npc, dict) else {}
        vztahy = {}
        for npc_id in NPC:
            try:
                hodnota = int(puvodni_vztahy.get(npc_id, 0))
            except (TypeError, ValueError):
                hodnota = 0
            vztahy[npc_id] = max(-100, min(100, hodnota))
        self.vztahy_npc = vztahy

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
            odhalene_lokace=data.get("odhalene_lokace", VYCHOZI_ODHALENE),
            navstiveno=data.get("navstiveno", {}) if isinstance(data.get("navstiveno", {}), dict) else {},
            vztahy_npc=data.get("vztahy_npc", {}) if isinstance(data.get("vztahy_npc", {}), dict) else {},
        )

    def menu(self, hra):
        while True:
            clear()
            lokace = LOKACE[self.aktualni_lokace]
            terminalni_obrazek("mapa")
            print("\n--- Mapa a vztahy ---\n")
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
                    vek = f", {npc['vek']} let" if npc.get("vek") else ""
                    print(f"  {npc['jmeno']} ({self.vztahy_npc[npc_id]:+d}{vek})")
            else:
                print("  Nikdo známý.")
            print("\n1-9) Cestovat  |  N) setkat se s NPC  |  E) dobít energii  |  0) Zpět")
            volba = input("> ").strip().lower()
            if volba == "0":
                return
            if volba == "n":
                self.menu_npc(hra)
                continue
            if volba == "e":
                from game.energie import zobraz_menu as menu_energie
                menu_energie(hra)
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
            vek = f", {npc['vek']} let" if npc.get("vek") else ""
            print(f"{index}) {npc['jmeno']} (vztah {self.vztahy_npc[npc_id]:+d}{vek})")
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
            dialogy = npc.get("dialogy", [])
            if dialogy:
                index_dialogu = 0 if vztah < 35 else min(len(dialogy) - 1, 1)
                print(f"{npc['jmeno']}: „{dialogy[index_dialogu]}“")
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
            elif npc_id == "elian":
                hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 3)
                self.zmen_vztah(npc_id, 3)
                tisk_ok("Elian odvedl pozornost stráží. Vliv inkvizice -3.")
            elif npc_id == "borin":
                from game.energie import hostinec
                if hostinec(hra):
                    self.zmen_vztah(npc_id, 3)
            elif npc_id == "velena":
                from game.energie import lazne
                if lazne(hra):
                    self.zmen_vztah(npc_id, 3)
            elif npc_id == "sava":
                from game.energie import meditace
                if meditace(hra):
                    self.zmen_vztah(npc_id, 3)
            elif npc_id == "nela":
                if hra.alchymie.pridat_surovinu("esence_temna", 1):
                    self.zmen_vztah(npc_id, 3)
                    tisk_ok("Nela ti svěřila lahvičku temné esence. Vztah +3.")
                else:
                    tisk_chyba("Nela dnes nemá vhodnou surovinu.")
            elif npc_id == "lyra":
                from game.energie import zahrada
                if zahrada(hra):
                    self.zmen_vztah(npc_id, 4)
            elif npc_id == "cassian":
                if hra.hrac.dark_energy < 10:
                    tisk_chyba("Cassian žádá nejdřív důkaz, že zvládneš soustředění.")
                else:
                    hra.hrac.dark_energy -= 10
                    self.odhal_lokaci("molo_mesicniho_pristavu")
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Cassian ti otevřel hvězdný archiv. Molo Měsíčního přístavu je na mapě.")
            elif npc_id == "tereza":
                hra.hrac.sex_energy = min(100, hra.hrac.sex_energy + 12)
                hra.hrac.reputace_mesta += 2
                self.zmen_vztah(npc_id, 4)
                tisk_ok("Tereza s tebou sdílela klidnou směnu na molu. Energie +12, reputace +2.")
        elif akce == "3":
            if vztah < -20:
                self.zmen_vztah(npc_id, -4)
                tisk_chyba("NPC ti nevěří a nabídku odmítl.")
            else:
                if npc_id == "sava":
                    hra.alchymie.pridat_surovinu("nocni_stin", 1)
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi Savě očistit háj. Získal jsi Noční stín, vztah +6.")
                elif npc_id == "nela":
                    hra.hrac.gold += 35
                    hra.alchymie.pridat_surovinu("koren_mandragory", 1)
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi Nele s destilací. Získal jsi 35 zlata a kořen mandragory.")
                else:
                    hra.hrac.gold += 30
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi NPC s její prací. Získal jsi 30 zlata, vztah +6.")
        else:
            tisk_chyba("Neplatná volba.")
        input("Enter...")
