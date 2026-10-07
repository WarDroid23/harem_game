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
        "typ": "ekonomicka",
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

    def zkontroluj_aktivitu(self, hra):
        den = int(getattr(getattr(hra, "hrac", None), "den", 1) or 1)
        if self.aktivni is None or (den - self.posledni_den) >= 3:
            self.nova_krize(hra)
        return self.aktivni

    def nova_krize(self, hra):
        den = int(getattr(getattr(hra, "hrac", None), "den", 1) or 1)
        mesicni_index = (den // 30) % len(MESTSKA_KRIZE)
        kriz = MESTSKA_KRIZE[mesicni_index].copy()
        if getattr(hra, "mafie", None) is not None:
            kriz["frakce"] = kriz.get("frakce", "obchodnici")
        kriz["typ"] = kriz.get("typ", random.choice(["politicka", "ekonomicka", "bezpecnostni", "spolecenska"]))
        kriz["den"] = den
        kriz["zivot"] = 3
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
        })
        self.historie = self.historie[-12:]
        return kriz

    def vyresit(self, hra, zpusob: str = "silny"):
        kriz = self.aktivni or self.nova_krize(hra)
        hrac = getattr(hra, "hrac", None)
        if hrac is None:
            return False
        typ = kriz.get("typ", "politicka")
        zlaty_bonus = 0
        vliv_bonus = kriz.get("vliv", 0)
        loajalita_bonus = kriz.get("loajalita", 0)
        if typ == "ekonomicka":
            zlaty_bonus = max(20, kriz.get("zlatek", 0) // 3)
            vliv_bonus += 2
        elif typ == "bezpecnostni":
            loajalita_bonus += 3
            vliv_bonus += 3
        elif typ == "spolecenska":
            loajalita_bonus += 4
        if zpusob == "silny":
            cena = min(200, kriz["zlatek"])
            if hrac.gold < cena:
                tisk_chyba("Na tvrdé řešení krize nemáš dost zlata.")
                return False
            hrac.gold -= cena
            hra.mafie.vliv_ve_meste = min(100, getattr(hra.mafie, "vliv_ve_meste", 0) + vliv_bonus)
            for otrok in hra.harem.vsechny_aktivni():
                otrok.loajalita = min(100, otrok.loajalita + loajalita_bonus)
            hrac.gold += zlaty_bonus
            tisk_ok(f"Rozhodl jsi se tvrdě: {kriz['nazev']} byla utlumena. Zlato -{cena}, vliv +{vliv_bonus}, bonus +{zlaty_bonus} zl.")
        else:
            hra.mafie.vliv_ve_meste = max(0, getattr(hra.mafie, "vliv_ve_meste", 0) + max(1, vliv_bonus // 2))
            for otrok in hra.harem.vsechny_aktivni():
                otrok.duvera = min(100, otrok.duvera + max(4, loajalita_bonus // 2))
            hrac.gold += max(10, zlaty_bonus // 2)
            tisk_ok(f"Použil jsi diplomatický přístup: {kriz['nazev']} byla urovnána, ale město si teprve zvyká na tvůj styl vlády.")
        self.aktivni = None
        return True

    def menu(self, hra):
        clear()
        kriz = self.zkontroluj_aktivitu(hra)
        print("🏙️ Městské krize a drama")
        print(f"Akční událost: {kriz['nazev']}")
        print(kriz["popis"])
        print(f"Doba působení: {kriz['zivot']} dny | Vliv města: +{kriz['vliv']}% | Náklady: {kriz['zlatek']} zl.")
        vytiskni_volbu("1", "Silná zásahová akce (zlatem a tvrdou rukou)")
        vytiskni_volbu("2", "Diplomatické uklidnění (měkké řešení)")
        vytiskni_volbu("0", "Zpět")
        volba = input("> ").strip()
        if volba == "1":
            self.vyresit(hra, "silny")
        elif volba == "2":
            self.vyresit(hra, "mily")
        try:
            input("Enter...")
        except EOFError:
            pass

    def to_dict(self):
        return {"aktivni": self.aktivni, "historie": self.historie, "posledni_den": self.posledni_den}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        if isinstance(data, dict):
            obj.aktivni = data.get("aktivni") if isinstance(data.get("aktivni"), dict) else None
            obj.historie = data.get("historie", []) if isinstance(data.get("historie", []), list) else []
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
        archetyp = getattr(otrok, "charakter", "subka")
        quest = random.choice(HAREM_STORY_QUESTS).copy()
        if archetyp in {"amazonka", "padla_paladinka"}:
            quest["nazev"] = "Bojový hlas z venku"
        elif archetyp in {"carodejka", "knezka_temnoty"}:
            quest["nazev"] = "Noční liturgie"
        elif archetyp in {"badatelka", "diplomatka"}:
            quest["nazev"] = "Zvěsti a důvěra"
        quest["faze"] = 1
        quest["stav"] = "aktivni"
        quest["faze_texty"] = [
            "Nastala první zkouška důvěry.",
            "Vztah se prohloubil a mění se v pouto.",
            "Příběh dosáhl vrcholu a odhalil pravou cenu přátelství.",
        ]
        return quest

    def vyrob_quest(self, otrok):
        quest = self._quest_pro_otrokyni(otrok)
        active = getattr(otrok, "rozsireni_questy", [])
        if not isinstance(active, list):
            active = []
        if not any(q.get("id") == quest["id"] for q in active):
            active.append({
                "id": quest["id"],
                "nazev": quest["nazev"],
                "stav": "aktivni",
                "faze": 1,
                "faze_text": quest["faze_texty"][0],
            })
            otrok.rozsireni_questy = active
        return quest

    def dokonci_quest(self, hra, otrok, quest):
        active = getattr(otrok, "rozsireni_questy", []) or []
        if not isinstance(active, list):
            active = []
        for item in active:
            if isinstance(item, dict) and item.get("id") == quest["id"]:
                item["stav"] = "dokonceno"
                item["faze"] = 2
                item["faze_text"] = quest["faze_texty"][-1]
        otrok.duvera = min(100, otrok.duvera + quest["bonus_duvera"])
        otrok.loajalita = min(100, otrok.loajalita + quest["bonus_loajalita"])
        if hasattr(otrok, "strach"):
            otrok.strach = max(0, otrok.strach - max(2, quest["bonus_duvera"] // 4))
        hra.hrac.gold += quest["bonus_gold"]
        otrok.rozsireni_questy = active
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
                        stav = q.get("stav", "aktivni")
                        quest_nazvy.append(f"{q.get('nazev', 'osobní výzva')} ({stav})")
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
                print(f"\n{otrok.jmeno}: {quest['nazev']}")
                print(quest['popis'])
                print(f"Odměna: +{quest['bonus_gold']} zl., +{quest['bonus_duvera']} důvěra, +{quest['bonus_loajalita']} loajalita")
                vytiskni_volbu("1", "Přijmout výzvu")
                vytiskni_volbu("2", "Nepřijímat")
                rozhodnuti = input("> ").strip()
                if rozhodnuti == "1":
                    self.dokonci_quest(hra, otrok, quest)
                    tisk_ok(f"{otrok.jmeno} se otevřela novému vztahu s tebou. Přidány odměny a v harému se rozbřesklo nové pouto.")
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
