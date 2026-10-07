from __future__ import annotations

import random
from dataclasses import dataclass, field

from utils.vypis import clear, tisk_chyba, tisk_info, tisk_ok, vytiskni_volbu


MESTSKA_KRIZE = [
    {
        "nazev": "Městský požár ve skladištích",
        "popis": "V přístavní části hoří zásoby, které by měly udržet město v klidu. Lidé čekají, zda se postavíš do čela záchranných prací nebo vyděláš na chaosu.",
        "zlatek": 140,
        "vliv": 6,
        "loajalita": 8,
        "frakce": "obchodnici",
        "typ": "pozar",
    },
    {
        "nazev": "Povstání v cechovních uličkách",
        "popis": "Řemeslníci a cechovní mistři se bouří proti zvýšení daní. Rozhodnutí může posílit tvůj vliv nebo otevřít nové zisky pro nájemné vrahy.",
        "zlatek": 110,
        "vliv": 8,
        "loajalita": 10,
        "frakce": "cechy",
        "typ": "politicka",
    },
    {
        "nazev": "Noční sabotáž v paláci",
        "popis": "Stínoví agenti přerušili zásilky a záměrně rozházeli kompromitující dopisy. Pokud to nevyřešíš rychle, celá městská elita tě bude považovat za slabého pána.",
        "zlatek": 160,
        "vliv": 10,
        "loajalita": 6,
        "frakce": "sylvestrova_elita",
        "typ": "bezpecnostni",
    },
    {
        "nazev": "Vysoké hladomorné ceny",
        "popis": "Tři trhy hlásí nedostatek zásob. Zatímco měšťané zuří, jsi jedním krokem od toho, aby se rozhodli, zda jsi přítel či vládcem jejich strachu.",
        "zlatek": 100,
        "vliv": 7,
        "loajalita": 9,
        "frakce": "obchodnici",
        "typ": "spolecenska",
    },
    {
        "nazev": "Vstup inkvizice do uliček",
        "popis": "Inkvizice rozšiřuje kontroly a hledá hříšníky v každém domě. Pokud se nezachytíš, město se otočí proti tobě i tvému harému.",
        "zlatek": 130,
        "vliv": 9,
        "loajalita": 7,
        "frakce": "inkvizice",
        "typ": "politicka",
    },
    {
        "nazev": "Prasklá hráz na říčním nábřeží",
        "popis": "Voda zaplavuje dílny a sklady u řeky. Obyvatelé potřebují pomoc dřív, než se spor o bezpečné útočiště změní v paniku.",
        "zlatek": 150,
        "vliv": 8,
        "loajalita": 9,
        "frakce": "cechy",
        "typ": "bezpecnostni",
    },
    {
        "nazev": "Ztracený seznam svědků",
        "popis": "Z archivu zmizel seznam lidí, kteří mohou objasnit spor mezi městskými rody. Každá frakce tvrdí, že jej chce jen ochránit.",
        "zlatek": 125,
        "vliv": 9,
        "loajalita": 7,
        "frakce": "sylvestrova_elita",
        "typ": "politicka",
    },
    {
        "nazev": "Zadržená karavana s léky",
        "popis": "Zásilka léčiv uvízla na hranici čtvrtí. Kupecký cech žádá náhradu, zatímco léčebny potřebují zásoby.",
        "zlatek": 135,
        "vliv": 7,
        "loajalita": 10,
        "frakce": "obchodnici",
        "typ": "ekonomicka",
    },
]


HAREM_STORY_QUESTS = [
    {
        "id": "prizek_mesta",
        "nazev": "Noc pro město",
        "popis": "Přesvědčíš svou otrokyně, aby se stala tvou reprezentantkou při klidnění davu a zlepšení pověsti dominia.",
        "bonus_gold": 80,
        "bonus_duvera": 12,
        "bonus_loajalita": 8,
    },
    {
        "id": "ztraceny_znak",
        "nazev": "Ztracený znak rodu",
        "popis": "Vyřešíš osobní konflikt, který narušuje důvěru mezi tebou a tvou otrokyní. Odměna je hlubší důvěra a méně žárlivosti v harému.",
        "bonus_gold": 70,
        "bonus_duvera": 14,
        "bonus_loajalita": 6,
    },
    {
        "id": "tajna_cesta",
        "nazev": "Tajná cesta k úniku",
        "popis": "Pomůžeš otrokyni překonat její strach z cizích ulic tak, aby se pro tebe stala ještě odhodlanější spojenkyní.",
        "bonus_gold": 90,
        "bonus_duvera": 10,
        "bonus_loajalita": 10,
    },
]


@dataclass
class MestskaKrizeSystem:
    aktivni: dict | None = None
    historie: list = field(default_factory=list)
    posledni_den: int = 0
    mesic: int = 1

    def _vytvor_moznosti(self, typ: str):
        typ = (typ or "politicka").lower()
        if typ == "hlad":
            return [
                {
                    "id": "distribuce",
                    "text": "Rozdělíš zásoby a uklidníš město",
                    "dopady": {"penize": -25, "reputace": 5, "frakce": {"obchodnici": 7, "cechy": 4}},
                },
                {
                    "id": "natalak",
                    "text": "Ovládneš tržní cenu a zatlačíš obchodníky k poslušnosti",
                    "dopady": {"penize": -10, "reputace": 2, "frakce": {"obchodnici": -8, "policie": 6}},
                },
                {
                    "id": "ticho",
                    "text": "Necháš chaos vyhořet a počkáš, až se dav unaví",
                    "dopady": {"penize": 0, "reputace": -4, "frakce": {"cechy": -6, "podsveti": 5}},
                },
            ]
        if typ == "pozar":
            return [
                {
                    "id": "haseni",
                    "text": "Požár uhasíš vlastními silami a zachráníš prestiž",
                    "dopady": {"penize": -40, "reputace": 8, "frakce": {"policie": 5, "obchodnici": 3}, "duvera": 3},
                },
                {
                    "id": "sabotaz",
                    "text": "Využiješ zmatek a zvedneš vliv podsvětí",
                    "dopady": {"penize": 25, "reputace": -7, "frakce": {"podsveti": 12, "obchodnici": -6}},
                },
                {
                    "id": "kryti",
                    "text": "Dáš záchranářům pokyn k tichému potlačení záznamů",
                    "dopady": {"penize": -15, "reputace": -2, "frakce": {"inkvizice": 6, "policie": 3}},
                },
            ]
        if typ == "razie":
            return [
                {
                    "id": "zastav",
                    "text": "Zastavíš razii a vyjednáš si podporu policie",
                    "dopady": {"penize": -20, "reputace": 6, "frakce": {"policie": 8, "podsveti": -10}},
                },
                {
                    "id": "podporit",
                    "text": "Skrze policejní razii posílíš vlastní autoritu",
                    "dopady": {"penize": -30, "reputace": 3, "frakce": {"policie": 12, "cechy": -8}},
                },
                {
                    "id": "utajit",
                    "text": "První průšvih se tichými prostředky zahodíš a odložíš stopu",
                    "dopady": {"penize": 15, "reputace": -5, "frakce": {"podsveti": 7, "inkvizice": 3}},
                },
            ]
        if typ == "mafia":
            return [
                {
                    "id": "sankce",
                    "text": "Vytáhneš černé karty a pošleš syndikát do ústupu",
                    "dopady": {"penize": -35, "reputace": 7, "frakce": {"syndikat_stinu": -16, "policie": 6}},
                },
                {
                    "id": "vyjednavat",
                    "text": "Přijmeš výhody ze smlouvy se stínovou sítí",
                    "dopady": {"penize": 25, "reputace": -3, "frakce": {"syndikat_stinu": 12, "obchodnici": 4}},
                },
                {
                    "id": "mlcet",
                    "text": "Dáše příměří bez veřejného rozruchu",
                    "dopady": {"penize": 5, "reputace": -1, "frakce": {"syndikat_stinu": 5, "cechy": -2}},
                },
            ]
        if typ == "ekonomicka":
            return [
                {
                    "id": "investice",
                    "text": "Podpoříš trh a obnovíš zásobování (−40 zl.)",
                    "dopady": {"penize": -40, "reputace": 7, "frakce": {"obchodnici": 8, "cechy": 3}, "duvera": 3},
                },
                {
                    "id": "smlouvy",
                    "text": "Vyjednáš dohodu s obchodníky (+25 zl.)",
                    "dopady": {"penize": 25, "reputace": 2, "frakce": {"obchodnici": 4, "cechy": -2}, "loajalita": 3},
                },
                {
                    "id": "solidarita",
                    "text": "Zorganizuješ společnou pomoc (−15 zl.)",
                    "dopady": {"penize": -15, "reputace": 5, "frakce": {"cechy": 6, "obchodnici": 2}, "duvera": 5},
                },
            ]
        if typ == "bezpecnostni":
            return [
                {
                    "id": "ochrana",
                    "text": "Zajistíš bezpečné hlídky pro obyvatele (−30 zl.)",
                    "dopady": {"penize": -30, "reputace": 6, "frakce": {"policie": 7, "podsveti": -5}, "duvera": 4},
                },
                {
                    "id": "jednani",
                    "text": "Vyjednáš příměří mezi znesvářenými stranami",
                    "dopady": {"penize": 0, "reputace": 4, "frakce": {"cechy": 5, "policie": 2}, "loajalita": 3},
                },
                {
                    "id": "informace",
                    "text": "Zaplatíš za informace a zabráníš dalšímu střetu (−20 zl.)",
                    "dopady": {"penize": -20, "reputace": 1, "frakce": {"podsveti": 4, "policie": -2}, "duvera": 2},
                },
            ]
        if typ == "spolecenska":
            return [
                {
                    "id": "pomoc",
                    "text": "Otevřeš veřejné zásobovací místo (−25 zl.)",
                    "dopady": {"penize": -25, "reputace": 8, "frakce": {"cechy": 5, "obchodnici": 3}, "duvera": 5},
                },
                {
                    "id": "shromazdeni",
                    "text": "Svoláš zástupce čtvrtí a vyslechneš jejich požadavky",
                    "dopady": {"penize": 0, "reputace": 5, "frakce": {"cechy": 7, "policie": 1}, "loajalita": 4},
                },
                {
                    "id": "vyhlaska",
                    "text": "Vydáš dočasnou vyhlášku a získáš čas (+15 zl.)",
                    "dopady": {"penize": 15, "reputace": -2, "frakce": {"policie": 3, "cechy": -4}, "loajalita": 1},
                },
            ]
        if typ == "politicka":
            return [
                {
                    "id": "dohoda",
                    "text": "Uzavřeš veřejnou dohodu a přijmeš dohled",
                    "dopady": {"penize": -10, "reputace": 7, "frakce": {"cechy": 5, "inkvizice": 3}, "duvera": 4},
                },
                {
                    "id": "ustupky",
                    "text": "Přijmeš omezené ústupky výměnou za klid (+20 zl.)",
                    "dopady": {"penize": 20, "reputace": 1, "frakce": {"obchodnici": 3, "cechy": 2}, "loajalita": 2},
                },
                {
                    "id": "odmitnuti",
                    "text": "Odmítneš tlak a veřejně obhájíš své rozhodnutí",
                    "dopady": {"penize": 0, "reputace": -3, "frakce": {"podsveti": 4, "inkvizice": -5}, "duvera": 1},
                },
            ]
        return [
            {
                "id": "silny",
                "text": "Tvrdý zásah a rázný příklad",
                "dopady": {"penize": -20, "reputace": 5, "frakce": {"policie": 7, "obchodnici": 2}},
            },
            {
                "id": "diplomaticky",
                "text": "Měkké urovnání přes dialog a výměnu ústupků",
                "dopady": {"penize": 10, "reputace": 2, "frakce": {"cechy": 6, "inkvizice": -4}},
            },
        ]

    def zkontroluj_aktivitu(self, hra):
        den = int(getattr(getattr(hra, "hrac", None), "den", 1) or 1)
        if self.aktivni is None and (not self.posledni_den or den - self.posledni_den >= 3):
            self.nova_krize(hra)
        return self.aktivni

    def posun_den(self, hra):
        """Zkrátí dobu krize a vyřeší její veřejné následky, pokud ji hráč ignoruje."""
        kriz = self.aktivni
        if not isinstance(kriz, dict):
            return None
        try:
            kriz["zivot"] = max(0, int(kriz.get("zivot", 3)) - 1)
        except (TypeError, ValueError):
            kriz["zivot"] = 0
        if kriz["zivot"] > 0:
            return None

        hrac = getattr(hra, "hrac", None)
        if hrac is not None:
            hrac.reputace_mesta = max(-100, min(100, getattr(hrac, "reputace_mesta", 0) - 5))
        if getattr(hra, "mestske_frakce", None) is not None and kriz.get("frakce"):
            hra.mestske_frakce.uprav(str(kriz["frakce"]), -8, "nevyřešená městská krize")
        zaznam = {
            "den": int(getattr(hrac, "den", self.posledni_den)),
            "nazev": kriz.get("nazev", "Městská krize"),
            "typ": kriz.get("typ", "politicka"),
            "vysledek": "bez zásahu",
            "reputace": -5,
        }
        self.historie.append(zaznam)
        self.historie = self.historie[-12:]
        self.aktivni = None
        return zaznam

    def nova_krize(self, hra):
        den = int(getattr(getattr(hra, "hrac", None), "den", 1) or 1)
        pocet_predchozich = sum(
            1 for zaznam in self.historie
            if isinstance(zaznam, dict) and "faze" in zaznam
        )
        kriz = MESTSKA_KRIZE[pocet_predchozich % len(MESTSKA_KRIZE)].copy()
        typ = (kriz.get("typ") or random.choice(["politicka", "ekonomicka", "bezpecnostni", "spolecenska"])).lower()
        kriz["typ"] = typ
        kriz["frakce"] = kriz.get("frakce", "obchodnici")
        kriz["den"] = den
        kriz["zivot"] = 3
        kriz["faze"] = 1
        kriz["sila"] = max(1, min(5, int(kriz.get("vliv", 5)) // 2))
        kriz["moznosti"] = self._vytvor_moznosti(typ)
        kriz["reseni"] = {
            "silny": "tvrdá intervence",
            "diplomaticky": "měkké urovnání",
        }
        kriz["mesicni_faze"] = max(1, (den // 30) + 1)
        self.aktivni = kriz
        self.posledni_den = den
        self.historie.append({
            "den": den,
            "nazev": kriz["nazev"],
            "typ": kriz["typ"],
            "frakce": kriz.get("frakce", "neurceno"),
            "popis": kriz["popis"],
            "faze": kriz["faze"],
        })
        self.historie = self.historie[-12:]
        return kriz

    def zvyrazni_krizi(self, hra, bonus: int = 1):
        kriz = self.aktivni or self.nova_krize(hra)
        if not isinstance(kriz, dict):
            return kriz
        faze = int(kriz.get("faze", 1)) + int(bonus)
        kriz["faze"] = min(3, max(1, faze))
        kriz["sila"] = max(1, int(kriz.get("sila", 1)) + int(bonus))
        kriz["popis"] = f"{kriz.get('popis', '')} V okolí narůstá tlak a město očekává jasné rozhodnutí."
        return kriz

    def vyresit(self, hra, zpusob: str = "silny", volba: str | None = None):
        kriz = self.aktivni or self.nova_krize(hra)
        hrac = getattr(hra, "hrac", None)
        if hrac is None:
            return False
        volby = kriz.get("moznosti", [])
        if volba is None:
            if isinstance(zpusob, str) and zpusob.lower() in {"silny", "tvrdy", "hard"}:
                volba = "silny" if any(item.get("id") == "silny" for item in volby) else (volby[0].get("id") if volby else "silny")
            elif isinstance(zpusob, str) and zpusob.lower() in {"diplomaticky", "mily", "soft"}:
                volba = "diplomaticky" if any(item.get("id") == "diplomaticky" for item in volby) else (volby[-1].get("id") if volby else "diplomaticky")
            else:
                volba = volby[0].get("id") if volby else "silny"
        vybrana = next((item for item in volby if item.get("id") == volba), None)
        if vybrana is None:
            tisk_chyba("Toto řešení krize není dostupné.")
            return False
        dopady = vybrana.get("dopady", {})
        typ = kriz.get("typ", "politicka")
        zlaty_bonus = max(10, int(kriz.get("zlatek", 0)) // 5)
        vliv_bonus = int(kriz.get("vliv", 0))
        loajalita_bonus = int(kriz.get("loajalita", 0))
        if typ == "ekonomicka":
            zlaty_bonus += 20
        elif typ == "bezpecnostni":
            loajalita_bonus += 3
            vliv_bonus += 2
        elif typ == "spolecenska":
            loajalita_bonus += 4

        zmena_penez = int(dopady.get("penize", 0))
        if zmena_penez < 0 and hrac.gold < -zmena_penez:
            tisk_chyba("Na toto řešení krize nemáš dost zlata.")
            return False
        hrac.gold += zmena_penez
        if volba == "diplomaticky":
            zlaty_bonus = max(5, zlaty_bonus // 2)
            if getattr(hra, "mafie", None) is not None:
                hra.mafie.vliv_ve_meste = max(0, getattr(hra.mafie, "vliv_ve_meste", 0) + max(1, vliv_bonus // 3))
        if getattr(hra, "mafie", None) is not None:
            hra.mafie.vliv_ve_meste = min(100, getattr(hra.mafie, "vliv_ve_meste", 0) + max(0, vliv_bonus // 2))
        if getattr(hra, "mestske_frakce", None) is not None:
            for frakce_id, delta in dopady.get("frakce", {}).items():
                hra.mestske_frakce.uprav(str(frakce_id), int(delta), f"krize:{kriz.get('typ', 'politicka')}")
            if kriz.get("frakce"):
                hra.mestske_frakce.uprav(str(kriz.get("frakce")), 6, f"krize:{kriz.get('typ', 'politicka')}")
        if getattr(hra, "frakce", None) is not None and kriz.get("frakce") in hra.frakce.frakce:
            hra.frakce.frakce[kriz["frakce"]].reputace = max(-100, min(100, hra.frakce.frakce[kriz["frakce"]].reputace + max(1, vliv_bonus // 2)))
        if hasattr(hrac, "reputace_mesta"):
            hrac.reputace_mesta = max(-100, min(100, hrac.reputace_mesta + int(dopady.get("reputace", 0))))
        for otrok in hra.harem.vsechny_aktivni():
            otrok.duvera = min(100, otrok.duvera + int(dopady.get("duvera", 0)))
            otrok.loajalita = min(100, otrok.loajalita + int(dopady.get("loajalita", 0)))
        hrac.gold += zlaty_bonus
        self.historie.append({
            "den": int(getattr(hrac, "den", self.posledni_den)),
            "nazev": kriz.get("nazev", "Městská krize"),
            "typ": typ,
            "vysledek": str(volba),
            "reputace": int(dopady.get("reputace", 0)),
        })
        self.historie = self.historie[-12:]
        self.aktivni = None
        self.mesic += 1
        return True

    def menu(self, hra):
        clear()
        kriz = self.zkontroluj_aktivitu(hra)
        if kriz is None:
            tisk_info("Město je po nedávném zásahu zatím klidné. Další událost se objeví za několik dní.")
            return
        print("🏙️ Městské krize a drama")
        print(f"Akční událost: {kriz['nazev']}")
        print(f"Fáze: {kriz.get('faze', 1)} / 3 | Síla: {kriz.get('sila', 1)} | Frakce: {kriz.get('frakce', 'neurčeno')}")
        print(kriz["popis"])
        print(f"Čas na řešení: {kriz.get('zivot', 3)} dny | Vliv města: +{kriz.get('vliv', 0)}%")
        for index, moznost in enumerate(kriz.get("moznosti", []), 1):
            vytiskni_volbu(str(index), moznost.get("text", "Vyber řešení"))
        vytiskni_volbu("0", "Zpět")
        try:
            volba = input("> ").strip()
        except EOFError:
            return
        if volba == "0":
            return
        if volba.isdigit():
            idx = int(volba) - 1
            moznosti = kriz.get("moznosti", [])
            if 0 <= idx < len(moznosti):
                self.vyresit(hra, zpusob=moznosti[idx].get("id"), volba=moznosti[idx].get("id"))
                return
        tisk_chyba("Neplatná volba.")
        try:
            input("Enter...")
        except EOFError:
            pass

    def to_dict(self):
        return {"aktivni": self.aktivni, "historie": self.historie, "posledni_den": self.posledni_den, "mesic": self.mesic}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        if isinstance(data, dict):
            obj.aktivni = data.get("aktivni") if isinstance(data.get("aktivni"), dict) else None
            obj.historie = data.get("historie", []) if isinstance(data.get("historie", []), list) else []
            obj.mesic = int(data.get("mesic", obj.mesic)) if str(data.get("mesic", obj.mesic)).isdigit() else obj.mesic
            try:
                obj.posledni_den = max(1, int(data.get("posledni_den", 1)))
            except (TypeError, ValueError):
                obj.posledni_den = 1
        return obj


@dataclass
class MestskeFrakceSystem:
    vztahy: dict = field(default_factory=dict)
    kronika: list = field(default_factory=list)

    PREDVOLENE = {
        "policie": 20,
        "podsveti": 10,
        "obchodnici": 15,
        "inkvizice": -10,
        "syndikat_stinu": 12,
        "cech_kurtizan": 18,
        "cechy": 10,
        "elitni_rod": 8,
    }

    def __post_init__(self):
        if not isinstance(self.vztahy, dict):
            self.vztahy = {}
        for frakce_id, hodnota in self.PREDVOLENE.items():
            if frakce_id not in self.vztahy:
                self.vztahy[frakce_id] = int(hodnota)

    def stav(self, frakce_id):
        hodnota = self.vztahy.get(frakce_id, 0)
        if hodnota >= 35:
            return "přátelský"
        if hodnota <= -35:
            return "nepřátelský"
        return "neutrální"

    def uprav(self, frakce_id, delta, zdroj=""):
        if frakce_id not in self.vztahy:
            self.vztahy[frakce_id] = 0
        self.vztahy[frakce_id] = max(-100, min(100, self.vztahy[frakce_id] + int(delta)))
        if zdroj:
            self.kronika.append({
                "frakce": frakce_id,
                "delta": int(delta),
                "zdroj": zdroj,
                "hodnota": self.vztahy[frakce_id],
            })
        self.kronika = self.kronika[-24:]
        return self.vztahy[frakce_id]

    def aplikuj_krizovy_dopad(self, frakce_id, delta, zdroj="krize"):
        return self.uprav(str(frakce_id), int(delta), zdroj)

    def menu(self, hra):
        clear()
        print("🏛️ Městské frakce a skrytá moc")
        ids = list(self.vztahy.keys())
        for idx, frakce_id in enumerate(ids, 1):
            hodnota = self.vztahy.get(frakce_id, 0)
            print(f"{idx}) {frakce_id}: {hodnota:+d} ({self.stav(frakce_id)})")
        print("0) Zpět")
        try:
            volba = input("> ").strip()
        except EOFError:
            return
        if not volba or volba == "0":
            return
        try:
            idx = int(volba) - 1
            if idx < 0 or idx >= len(ids):
                tisk_chyba("Neplatná volba.")
                input("Enter...")
                return
            frakce_id = ids[idx]
            print(f"\nFrakce: {frakce_id}")
            print("1) Uspokojit diplomacií")
            print("2) Vynutit loajalitu")
            print("3) Zajistit příměří")
            print("0) Zpět")
            akce = input("> ").strip()
            if akce == "1":
                self.uprav(frakce_id, 8, "diplomacie")
                if getattr(hra, "frakce", None) and frakce_id in hra.frakce.frakce:
                    hra.frakce.frakce[frakce_id].reputace = max(-100, min(100, hra.frakce.frakce[frakce_id].reputace + 8))
                tisk_ok(f"Diplomatická cesta posílila vztahy s {frakce_id}.")
            elif akce == "2":
                self.uprav(frakce_id, -12, "nátlak")
                if getattr(hra, "frakce", None) and frakce_id in hra.frakce.frakce:
                    hra.frakce.frakce[frakce_id].reputace = max(-100, min(100, hra.frakce.frakce[frakce_id].reputace - 12))
                tisk_ok(f"Nátlak zvyšuje tvou kontrolu, ale u {frakce_id} to zvyšuje napětí.")
            elif akce == "3":
                self.uprav(frakce_id, 5, "príměří")
                if getattr(hra, "frakce", None) and frakce_id in hra.frakce.frakce:
                    hra.frakce.frakce[frakce_id].reputace = max(-100, min(100, hra.frakce.frakce[frakce_id].reputace + 5))
                tisk_ok(f"Příměří s {frakce_id} bylo dočasně potvrzeno.")
        except ValueError:
            tisk_chyba("Neplatná volba.")
        try:
            input("Enter...")
        except EOFError:
            pass

    def to_dict(self):
        return {"vztahy": dict(self.vztahy), "kronika": list(self.kronika)}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        if isinstance(data, dict):
            vztahy = data.get("vztahy", {})
            if isinstance(vztahy, dict):
                obj.vztahy = {str(k): int(v) for k, v in vztahy.items() if isinstance(v, (int, float))}
            kronika = data.get("kronika", [])
            if isinstance(kronika, list):
                obj.kronika = kronika
        return obj


@dataclass
class RozsireniHarlemuSystem:
    aktivity: dict = field(default_factory=dict)

    def _quest_pro_otrokyni(self, otrok):
        from data.charaktery import normalizuj_charakter

        archetyp = normalizuj_charakter(getattr(otrok, "charakter", "subka"))
        quest = random.choice(HAREM_STORY_QUESTS).copy()
        if archetyp in {"amazonka", "padla_paladinka"}:
            quest["nazev"] = "Bojový hlas z venku"
            quest["popis"] = "Společně připravíte otevřený výcvikový kruh, jehož pravidla určí jeho účastníci."
            quest["faze_texty"] = [
                "Na nádvoří se scházejí první zájemci; ona chce nejdřív vyslechnout jejich očekávání.",
                "Účastníci sestavují pravidla bezpečného tréninku a volí si vlastní tempo.",
                "Výcvikový kruh zahajuje činnost a ona rozhoduje, jakou roli v něm chce mít.",
            ]
        elif archetyp in {"carodejka", "knezka_temnoty"}:
            quest["nazev"] = "Noční liturgie"
            quest["popis"] = "Připraví osobní obřad, který může sdílet, upravit, nebo si ponechat jen pro sebe."
            quest["faze_texty"] = [
                "Při přípravě obřadu narazí na symbol, který jí připomíná její minulost.",
                "Zkouší nové bezpečné postupy a sama rozhoduje, kdo smí být přítomen.",
                "Obřad je připraven; jeho podobu i účastníky určí ona.",
            ]
        elif archetyp in {"badatelka", "diplomatka"}:
            quest["nazev"] = "Zvěsti a důvěra"
            quest["popis"] = "Prověří znepokojivou městskou zprávu a rozhodne, jak naložit s výsledkem."
            quest["faze_texty"] = [
                "Získala první stopu, ale nechce stavět závěry na pouhé pověsti.",
                "Porovnává svědectví a připravuje otázky pro další zdroje.",
                "Zná celý příběh a rozhoduje, zda jej zveřejní, nebo ochrání své zdroje.",
            ]
        elif archetyp == "cartografka":
            quest["nazev"] = "Mapa bezpečných cest"
            quest["popis"] = "Zmapuje průchody městem a rozhodne, komu svou mapu zpřístupní."
            quest["faze_texty"] = [
                "Našla starý plánek a vyznačuje místa, která je třeba ověřit.",
                "Prochází čtvrti s místními průvodci a zaznamenává jejich připomínky.",
                "Mapa je hotová; sama volí, zda ji zveřejní, nebo předá jen důvěryhodným lidem.",
            ]
        elif archetyp == "lekarka":
            quest["nazev"] = "Léčebna pro každého"
            quest["popis"] = "Pomůže připravit léčebnou místnost s jasnými pravidly soukromí a péče."
            quest["faze_texty"] = [
                "Sepisuje potřeby pacientů a trvá na tom, že každý musí znát možnosti péče.",
                "Dobrovolníci připravují prostor a ona nastavuje pravidla důvěrnosti.",
                "Léčebna otevírá; sama si zvolí, kolik času a energie jí chce věnovat.",
            ]
        elif archetyp == "veteranka":
            quest["nazev"] = "Hlídka bez rozkazů"
            quest["popis"] = "Pomůže vytvořit obrannou hlídku, která jedná podle společně přijatých pravidel."
            quest["faze_texty"] = [
                "Navrhuje hlídky, ale nechce opakovat chyby starých velitelů.",
                "Členové hlídky společně schvalují zásady ochrany a odpovědnosti.",
                "Hlídka je připravena; ona sama určí, zda jí chce velet, nebo jen radit.",
            ]
        quest["faze"] = 1
        quest["stav"] = "aktivni"
        quest["max_faze"] = 3
        quest.setdefault("faze_texty", [
            "Nastala první zkouška důvěry.",
            "Vztah se prohloubil a mění se v pouto.",
            "Příběh dosáhl vrcholu a odhalil pravou cenu přátelství.",
        ])
        quest["volby"] = [
            {"id": "naslouchat", "text": "Vyslechneš její přání a necháš jí určit tempo", "bonus": {"duvera": 8, "loajalita": 2}},
            {"id": "spolupracovat", "text": "Rozdělíte si úkoly a připravíte společný plán", "bonus": {"duvera": 5, "loajalita": 5}},
            {"id": "samostatne", "text": "Podpoříš její samostatné rozhodnutí a nabídneš pomoc na vyžádání", "bonus": {"duvera": 6, "loajalita": 3}},
        ]
        return quest

    def _normalizuj_quest(self, quest):
        if not isinstance(quest, dict):
            return None
        q = quest.copy()
        q["id"] = str(q.get("id", "osobni_vyzva"))
        q["nazev"] = str(q.get("nazev", "Osobní výzva"))
        q["stav"] = str(q.get("stav", "aktivni"))
        try:
            q["faze"] = max(1, min(3, int(q.get("faze", 1))))
        except (TypeError, ValueError):
            q["faze"] = 1
        q["max_faze"] = max(3, int(q.get("max_faze", 3)))
        if not isinstance(q.get("faze_texty"), list):
            q["faze_texty"] = [
                "Nastala první zkouška důvěry.",
                "Vztah se prohloubil a mění se v pouto.",
                "Příběh dosáhl vrcholu a odhalil pravou cenu přátelství.",
            ]
        if not isinstance(q.get("volby"), list):
            q["volby"] = [
                {"id": "naslouchat", "text": "Vyslechneš její přání a necháš jí určit tempo", "bonus": {"duvera": 8, "loajalita": 2}},
                {"id": "spolupracovat", "text": "Rozdělíte si úkoly a připravíte společný plán", "bonus": {"duvera": 5, "loajalita": 5}},
            ]
        if not isinstance(q.get("volby_zvolene"), list):
            q["volby_zvolene"] = [None] * max(0, q["faze"] - 1)
        return q

    def _pridej_quest(self, otrok, quest):
        active = getattr(otrok, "rozsireni_questy", []) or []
        if not isinstance(active, list):
            active = []
        q = self._normalizuj_quest(quest)
        if q is None:
            return None
        for existing in active:
            if isinstance(existing, dict) and str(existing.get("id")) == q["id"]:
                return existing
        active.append({
            "id": q["id"],
            "nazev": q["nazev"],
            "popis": q.get("popis", ""),
            "stav": q["stav"],
            "faze": q["faze"],
            "max_faze": q.get("max_faze", 3),
            "faze_text": q["faze_texty"][min(q["faze"] - 1, len(q["faze_texty"]) - 1)],
            "bonus_gold": q.get("bonus_gold", 60),
            "bonus_duvera": q.get("bonus_duvera", 10),
            "bonus_loajalita": q.get("bonus_loajalita", 8),
            "faze_texty": q["faze_texty"],
            "volby": q["volby"],
            "volby_zvolene": [],
            "odmena_vyplacena": False,
        })
        otrok.rozsireni_questy = active
        return active[-1]

    def vyrob_quest(self, otrok):
        active = getattr(otrok, "rozsireni_questy", []) or []
        if isinstance(active, list):
            for item in active:
                if isinstance(item, dict) and item.get("stav") == "aktivni":
                    return item
        quest = self._quest_pro_otrokyni(otrok)
        active = active if isinstance(active, list) else []
        quest["id"] = f"{quest['id']}_{len(active) + 1}"
        return self._pridej_quest(otrok, quest) or quest

    def _uplatni_odmenu(self, hra, otrok, quest):
        q = self._normalizuj_quest(quest)
        if q is None:
            return
        if q.get("odmena_vyplacena"):
            return
        otrok.duvera = min(100, int(otrok.duvera) + int(q.get("bonus_duvera", 0)))
        otrok.loajalita = min(100, int(otrok.loajalita) + int(q.get("bonus_loajalita", 0)))
        if hasattr(otrok, "strach"):
            otrok.strach = max(0, int(otrok.strach) - max(2, int(q.get("bonus_duvera", 0)) // 4))
        if hasattr(hra, "hrac") and getattr(hra.hrac, "gold", 0) is not None:
            hra.hrac.gold += int(q.get("bonus_gold", 0))
        q["odmena_vyplacena"] = True
        if isinstance(quest, dict):
            quest["odmena_vyplacena"] = True

    def postup_quest(self, hra, otrok, quest, volba_id: str = "soucit"):
        active = getattr(otrok, "rozsireni_questy", []) or []
        if not isinstance(active, list):
            active = []
        q = self._normalizuj_quest(quest)
        if q is None:
            return None
        for index, item in enumerate(active):
            if not isinstance(item, dict):
                continue
            if str(item.get("id")) != q["id"]:
                continue
            item = self._normalizuj_quest(item)
            if item is None:
                continue
            if item.get("stav") != "aktivni":
                return None
            moznost = next(
                (volba for volba in item["volby"] if volba.get("id") == volba_id),
                None,
            )
            if moznost is None:
                legacy_aliases = {
                    "soucit": "naslouchat",
                    "vydrz": "spolupracovat",
                    "ticho": "samostatne",
                }
                alias = legacy_aliases.get(volba_id)
                moznost = next(
                    (volba for volba in item["volby"] if volba.get("id") == alias),
                    None,
                )
            if moznost is None:
                return None
            for stat, hodnota in moznost.get("bonus", {}).items():
                if stat in {"duvera", "loajalita", "touha"} and hasattr(otrok, stat):
                    setattr(otrok, stat, min(100, max(0, int(getattr(otrok, stat)) + int(hodnota))))
            item.setdefault("volby_zvolene", []).append(str(volba_id))
            item["faze"] = min(int(item.get("faze", 1)) + 1, int(item.get("max_faze", 3)))
            item["stav"] = (
                "dokonceno"
                if len(item["volby_zvolene"]) >= int(item.get("max_faze", 3))
                else "aktivni"
            )
            if "faze_texty" in item and isinstance(item["faze_texty"], list):
                item["faze_text"] = item["faze_texty"][min(item["faze"] - 1, len(item["faze_texty"]) - 1)]
            active[index] = item
            otrok.rozsireni_questy = active
            if item["stav"] == "dokonceno":
                volby = item["volby_zvolene"]
                if volby and all(volba == "naslouchat" for volba in volby):
                    item["zaver"] = "Její vlastní plán"
                elif volby.count("spolupracovat") >= 2:
                    item["zaver"] = "Společné dílo"
                else:
                    item["zaver"] = "Otevřená cesta"
                item["faze_text"] = f"{item['faze_texty'][-1]} Závěr: {item['zaver']}."
                self._uplatni_odmenu(hra, otrok, item)
            return item
        return None

    def dokonci_quest(self, hra, otrok, quest):
        q = self._normalizuj_quest(quest)
        if q is None:
            return False
        active = getattr(otrok, "rozsireni_questy", []) or []
        if not isinstance(active, list):
            active = []
        for index, item in enumerate(active):
            if isinstance(item, dict) and str(item.get("id")) == q["id"]:
                item = self._normalizuj_quest(item)
                if item.get("stav") == "dokonceno":
                    return False
                item["stav"] = "dokonceno"
                item["faze"] = int(item.get("max_faze", 3))
                item["faze_text"] = item["faze_texty"][-1]
                active[index] = item
                break
        else:
            active.append({
                "id": q["id"],
                "nazev": q["nazev"],
                "stav": "dokonceno",
                "faze": int(q.get("max_faze", 3)),
                "max_faze": int(q.get("max_faze", 3)),
                "faze_text": q["faze_texty"][-1],
                "faze_texty": q["faze_texty"],
                "bonus_gold": q.get("bonus_gold", 60),
                "bonus_duvera": q.get("bonus_duvera", 10),
                "bonus_loajalita": q.get("bonus_loajalita", 8),
            })
            item = active[-1]
        otrok.rozsireni_questy = active
        self._uplatni_odmenu(hra, otrok, item)
        return True

    def zobraz_menu(self, hra):
        clear()
        print("💬 Rozšíření harému: osobní příběhy a story questy")
        aktivni = [o for o in hra.harem.vsechny_aktivni() if getattr(o, "hp", 0) > 0]
        if not aktivni:
            tisk_info("V harému zatím není nikdo, koho bys mohl znovu poznat.")
            input("Enter...")
            return
        for index, otrok in enumerate(aktivni, 1):
            print(f"{index}) {otrok.jmeno} — důvěra {otrok.duvera}, loajalita {otrok.loajalita}")
            questy = getattr(otrok, "rozsireni_questy", []) or []
            if questy:
                quest_nazvy = []
                for q in questy:
                    if isinstance(q, dict):
                        q = self._normalizuj_quest(q)
                        if q is None:
                            continue
                        stav = q.get("stav", "aktivni")
                        quest_nazvy.append(f"{q.get('nazev', 'osobní výzva')} ({stav} {q.get('faze', 1)}/{q.get('max_faze', 3)})")
                if quest_nazvy:
                    print(f"   Story questy: {', '.join(quest_nazvy)}")
        print("0) Zpět")
        try:
            volba = input("> ").strip()
        except EOFError:
            return
        if not volba or volba == "0":
            return
        try:
            idx = int(volba) - 1
            if 0 <= idx < len(aktivni):
                otrok = aktivni[idx]
                quest = self.vyrob_quest(otrok)
                q = self._normalizuj_quest(quest)
                if q is None:
                    tisk_chyba("Tato výzva se nepodařilo načíst.")
                    input("Enter...")
                    return
                print(f"\n{otrok.jmeno}: {q['nazev']}")
                print(q['faze_texty'][min(q['faze'] - 1, len(q['faze_texty']) - 1)])
                print(q.get('popis', ''))
                print(f"Odměna: +{q.get('bonus_gold', 60)} zl., +{q.get('bonus_duvera', 10)} důvěra, +{q.get('bonus_loajalita', 8)} loajalita")
                for v in q.get('volby', []):
                    vytiskni_volbu(v['id'], v.get('text', 'Vybrat volbu'))
                rozhodnuti = input("> ").strip()
                if rozhodnuti in {v['id'] for v in q.get('volby', [])}:
                    aktualni = self.postup_quest(hra, otrok, q, rozhodnuti)
                    if aktualni is not None and aktualni.get("stav") == "dokonceno":
                        tisk_ok(f"{otrok.jmeno} dokončila osobní výzvu. Pouto mezi vámi je pevnější a harém získal odměnu.")
                    elif aktualni is not None:
                        tisk_ok(f"{otrok.jmeno} postoupila v příběhu o další fázi. Pouto se prohlubuje.")
                else:
                    tisk_chyba("Neplatná volba pro osobní výzvu.")
        except ValueError:
            tisk_chyba("Neplatná volba.")
        try:
            input("Enter...")
        except EOFError:
            pass

    def to_dict(self):
        return {k: v for k, v in self.aktivity.items() if isinstance(v, dict)}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        if isinstance(data, dict):
            obj.aktivity = {k: v for k, v in data.items() if isinstance(v, dict)}
        return obj


@dataclass
class MestskyMesicSystem:
    mesic: int = 1
    prehled: dict = field(default_factory=dict)

    def _specializacni_bonusy(self, hra):
        specializace = getattr(getattr(hra, "svet", None), "specializace_ctvrti", None)
        if specializace is None:
            return {}
        bonusy = {}
        for lokace_id, typ in getattr(specializace, "specializace", {}).items():
            for kluc, hodnota in specializace.popis_typu(typ).get("bonus", {}).items():
                bonusy[kluc] = bonusy.get(kluc, 0) + int(hodnota)
        return bonusy

    def vyhodnot_mesic(self, hra):
        bonusy = self._specializacni_bonusy(hra)
        frakce = getattr(hra, "mestske_frakce", None)
        vztahy = {}
        if frakce is not None:
            vztahy = dict(getattr(frakce, "vztahy", {}))
        kriz = getattr(getattr(hra, "mestska_krize", None), "aktivni", None)
        if kriz is None:
            stav_krize = "klid"
        else:
            stav_krize = kriz.get("typ", "politicka")

        soucet_vliv = sum(v for v in vztahy.values()) if vztahy else 0
        zisk = max(0, int(bonusy.get("gold", 0))) + max(0, int(soucet_vliv // 12))
        if stav_krize in {"ekonomicka", "spolecenska"}:
            zisk = max(0, zisk - 20)
        elif stav_krize in {"politicka", "bezpecnostni"}:
            zisk = max(0, zisk - 10)

        prehled = {
            "mesic": self.mesic,
            "stav_krize": stav_krize,
            "bonusy": bonusy,
            "ekonomika": {
                "prijem": zisk,
                "vetrh": int(bonusy.get("gold", 0)) // 2,
                "vliv": max(0, int(bonusy.get("vliv", 0))),
            },
            "frakce": vztahy,
        }
        self.prehled = prehled
        if zisk > 0:
            hra.hrac.gold += zisk
        if getattr(hra, "harem", None) is not None:
            for otrok in hra.harem.vsechny_aktivni():
                if bonusy.get("duvera"):
                    otrok.duvera = min(100, otrok.duvera + max(1, int(bonusy.get("duvera", 0)) // 4))
                if bonusy.get("loajalita"):
                    otrok.loajalita = min(100, otrok.loajalita + max(1, int(bonusy.get("loajalita", 0)) // 4))
        self.mesic += 1
        return prehled

    def zobraz_prehled(self, hra):
        clear()
        prehled = self.vyhodnot_mesic(hra)
        print("📊 Měsíční přehled města")
        print(f"Měsíc: {prehled['mesic']}")
        print(f"Stav města: {prehled['stav_krize']}")
        print(f"Příjem: +{prehled['ekonomika']['prijem']} zl")
        print(f"Vliv: +{prehled['ekonomika']['vliv']}")
        if prehled["bonusy"]:
            print("Bonusy čtvrtí:")
            for klic, hodnota in prehled["bonusy"].items():
                print(f"  - {klic}: {hodnota:+d}")
        if prehled["frakce"]:
            print("Vztahy k frakcím:")
            for frakce_id, hodnota in sorted(prehled["frakce"].items()):
                print(f"  - {frakce_id}: {hodnota:+d}")
        try:
            input("Enter...")
        except EOFError:
            pass
        return prehled

    def to_dict(self):
        return {"mesic": self.mesic, "prehled": self.prehled}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        if isinstance(data, dict):
            try:
                obj.mesic = max(1, int(data.get("mesic", 1)))
            except (TypeError, ValueError):
                obj.mesic = 1
            obj.prehled = data.get("prehled", {}) if isinstance(data.get("prehled", {}), dict) else {}
        return obj


def menu_specializace_ctvrti(hra):
    from utils.vypis import clear, tisk_chyba, tisk_ok
    from game.svet import LOKACE

    clear()
    lokace_id = getattr(getattr(hra, "svet", None), "aktualni_lokace", "pevnost")
    print("🏭 Specializace čtvrtí")
    print(f"Současná lokace: {LOKACE.get(lokace_id, {}).get('nazev', lokace_id)}")
    print("Vyber typ: ")
    print("1) Obecná čtvrť")
    print("2) Zahradní specializace")
    print("3) Vodní specializace")
    print("4) Kupecká specializace")
    print("0) Zpět")
    volba = input("> ").strip()
    if volba == "0":
        return
    mapa = {
        "1": "obecna",
        "2": "zahradni",
        "3": "vodni",
        "4": "kupecká",
    }
    typ = mapa.get(volba)
    if typ is None:
        tisk_chyba("Neplatná volba.")
        input("Enter...")
        return
    if lokace_id not in LOKACE:
        tisk_chyba("Tato lokace není ve světě mapy.")
        input("Enter...")
        return
    hra.svet.nastav_specializaci(lokace_id, typ)
    bonus = hra.svet.bonus_specializace(lokace_id)
    popis = hra.svet.specializace_ctvrti.popis_typu(typ)
    tisk_ok(f"Čtvrt {LOKACE[lokace_id]['nazev']} má nyní specializaci: {popis['nazev']}.")
    print(popis['popis'])
    if bonus:
        print(f"Bonus: {bonus}")
    input("Enter...")
