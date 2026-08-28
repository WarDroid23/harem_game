"""Mapové a týmové výpravy s deterministickým serializovatelným stavem."""

import random
from dataclasses import dataclass, field

from game.balance import profil_obtiznosti, uprav_odmenu, uprav_xp
from models.equipment import EQUIPMENT
from utils.vypis import clear, tisk_chyba, tisk_info, tisk_ok


EXPEDICE = {
    "mlzne_stopy": {
        "nazev": "Stopy v mlze",
        "lokace": "les",
        "obtiznost": 2,
        "odmena": 120,
        "xp": 35,
        "stages": 2,
        "popis": "Najdi ztracenou karavanu a bezpečně ji doprovoď k hranici.",
    },
    "archivni_vyprava": {
        "nazev": "Výprava do archivu",
        "lokace": "akademie",
        "obtiznost": 3,
        "odmena": 190,
        "xp": 55,
        "stages": 3,
        "popis": "Získej staré mapy bez toho, aby padly do rukou inkvizice.",
    },
    "mesicni_pruzkum": {
        "nazev": "Měsíční průzkum",
        "lokace": "molo_mesicniho_pristavu",
        "obtiznost": 5,
        "odmena": 360,
        "xp": 95,
        "stages": 3,
        "popis": "Prozkoumej pobřeží a vrať se s novou cestou pro spojence.",
    },
    "hvezdny_signal": {
        "nazev": "Hvězdný signál",
        "lokace": "observator",
        "obtiznost": 6,
        "odmena": 500,
        "xp": 130,
        "stages": 4,
        "popis": "Stabilizuj věžní čočky a odhal poslední bezpečnou trasu.",
    },
}


@dataclass
class Expedice:
    id: str
    tym: list = field(default_factory=list)
    krok: int = 0
    stav: str = "aktivni"
    uspech: bool = False
    udalosti: list = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "tym": self.tym,
            "krok": self.krok,
            "stav": self.stav,
            "uspech": self.uspech,
            "udalosti": self.udalosti,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or data.get("id") not in EXPEDICE:
            raise ValueError("Neplatná výprava.")
        try:
            krok = max(0, int(data.get("krok", 0)))
        except (TypeError, ValueError):
            krok = 0
        tym = data.get("tym", [])
        return cls(
            id=data["id"],
            tym=[str(x) for x in tym if isinstance(x, str)] if isinstance(tym, list) else [],
            krok=krok,
            stav=data.get("stav", "aktivni") if data.get("stav") in ("aktivni", "dokoncena", "selhala") else "aktivni",
            uspech=bool(data.get("uspech", False)),
            udalosti=data.get("udalosti", []) if isinstance(data.get("udalosti", []), list) else [],
        )


@dataclass
class ExpeditionSystem:
    aktivni: list = field(default_factory=list)
    dokoncene: int = 0
    objevene: list = field(default_factory=list)

    def dostupne(self, hra):
        odhalene = set(getattr(hra.svet, "odhalene_lokace", []))
        return [
            (ident, data) for ident, data in EXPEDICE.items()
            if data["lokace"] in odhalene
            and ident not in self.objevene
            and not any(v.id == ident and v.stav == "aktivni" for v in self.aktivni)
        ]

    def nahodna(self, hra, rng=None):
        rng = rng or random
        dostupne = self.dostupne(hra)
        if not dostupne:
            return None
        ident, _ = rng.choice(dostupne)
        self.objevene.append(ident)
        return ident

    def sila_tymu(self, hra, jmena):
        postavy = [
            otrok for otrok in hra.harem.vsechny_aktivni()
            if otrok.jmeno in jmena and not otrok.na_najmu
        ]
        if not postavy:
            return 0, []
        sila = sum(
            4 + otrok.poslusnost // 10 + otrok.loajalita // 20
            + sum(int(EQUIPMENT.get(item, {}).get("expedicni_bonus", 0)) for item in otrok.vybaveni)
            for otrok in postavy
        )
        sila += hra.hrac.level * 2 + hra.hrac.bojovy_bonus_vybavy()
        pevnost = getattr(hra, "pevnost", None)
        if pevnost:
            sila += pevnost.bonusy().get("vybava", 0)
        return sila, postavy

    def zahaj(self, hra, expedice_id, jmena):
        data = EXPEDICE.get(expedice_id)
        if data is None:
            return False
        if any(v.stav == "aktivni" for v in self.aktivni):
            return False
        sila, postavy = self.sila_tymu(hra, jmena)
        if not postavy or len(postavy) > 4:
            return False
        if sila < data["obtiznost"] * 4:
            return False
        vyprava = Expedice(expedice_id, [o.jmeno for o in postavy])
        self.aktivni.append(vyprava)
        for otrok in postavy:
            otrok.zaznamenej_volbu("výprava", data["nazev"], hra.hrac.den)
            otrok.unaveny = max(getattr(otrok, "unaveny", 0), 1)
        return True

    def postup(self, hra, expedice_id=None, rng=None):
        rng = rng or random
        vyprava = next(
            (v for v in self.aktivni if v.stav == "aktivni" and (expedice_id is None or v.id == expedice_id)),
            None,
        )
        if vyprava is None:
            return False
        data = EXPEDICE[vyprava.id]
        sila, postavy = self.sila_tymu(hra, vyprava.tym)
        if not postavy:
            vyprava.stav, vyprava.uspech = "selhala", False
            return False
        obtiznost = getattr(getattr(hra, "nastaveni", None), "obtiznost", "normalni")
        profil = profil_obtiznosti(obtiznost)
        sance = max(0.1, min(0.95, 0.55 + (sila - data["obtiznost"] * 5) / 100))
        if hra.kalendar.sezona == "podzim":
            sance -= 0.05
        if rng.random() > sance:
            vyprava.stav, vyprava.uspech = "selhala", False
            hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + data["obtiznost"])
            vyprava.udalosti.append("Výprava selhala a tým se vrátil bez odměny.")
            return False
        vyprava.krok += 1
        vyprava.udalosti.append(f"Etapa {vyprava.krok} proběhla bezpečně.")
        if vyprava.krok < data["stages"]:
            return True
        vyprava.stav, vyprava.uspech = "dokoncena", True
        self.dokoncene += 1
        odmena = uprav_odmenu(data["odmena"], obtiznost)
        xp = uprav_xp(data["xp"], obtiznost)
        if hra.kalendar.sezona == "leto":
            odmena = int(odmena * 1.15)
        hra.hrac.gold += odmena
        hra.hrac.pridej_xp(xp)
        hra.hrac.reputace_mesta += 1 if hra.kalendar.sezona == "zima" else 0
        if hasattr(hra, "achievementy"):
            hra.achievementy.zaznamenej("expedice")
            if len(vyprava.tym) > 1:
                hra.achievementy.zaznamenej("tymova_expedice")
        tisk_ok(f"Výprava {data['nazev']} dokončena: +{odmena} zlata, +{xp} XP.")
        return True

    def to_dict(self):
        return {
            "aktivni": [v.to_dict() for v in self.aktivni],
            "dokoncene": self.dokoncene,
            "objevene": self.objevene,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        aktivni = []
        for item in data.get("aktivni", []):
            if isinstance(item, dict):
                try:
                    aktivni.append(Expedice.from_dict(item))
                except ValueError:
                    continue
        return cls(
            aktivni=aktivni,
            dokoncene=max(0, int(data.get("dokoncene", 0))),
            objevene=[x for x in data.get("objevene", []) if x in EXPEDICE]
            if isinstance(data.get("objevene", []), list) else [],
        )

    def menu(self, hra):
        while True:
            clear()
            print("--- Výpravy mapy a harému ---")
            if self.aktivni:
                for v in self.aktivni:
                    print(f"{v.id}: etapa {v.krok}/{EXPEDICE[v.id]['stages']} ({v.stav})")
            else:
                print("Žádná aktivní výprava.")
            print("\nDostupné:")
            for ident, data in self.dostupne(hra):
                print(f"{ident}) {data['nazev']} — tým do 4 osob, obtížnost {data['obtiznost']}")
            print("P) pokračovat v aktivní výpravě | 0) Zpět")
            volba = input("> ").strip().lower()
            if volba == "0":
                return
            if volba == "p":
                self.postup(hra)
                input("Enter...")
                continue
            if volba not in EXPEDICE:
                tisk_chyba("Neznámá výprava.")
                input("Enter...")
                continue
            jmena = [x.strip() for x in input("Členky týmu (jména oddělená čárkou): ").split(",") if x.strip()]
            if self.zahaj(hra, volba, jmena):
                tisk_info("Tým vyrazil. Proveď další etapy volbou P.")
            else:
                tisk_chyba("Tým není vhodný, výprava už běží nebo je lokace nedostupná.")
            input("Enter...")


Vyprava = Expedice
VypravySystem = ExpeditionSystem
