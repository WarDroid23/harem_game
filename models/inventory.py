# models/inventory.py
from dataclasses import dataclass, field, asdict, fields

@dataclass
class Zbran:
    nazev: str
    typ: str
    poskozeni: int
    cena: int
    vaha: float = 0.0
    specialni: str = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Inventory:
    predmety: list = field(default_factory=list)
    zbrane: list = field(default_factory=list)
    penize_v_bance: int = 0
    vybaveni: dict = field(default_factory=dict)

    def pridej_zbran(self, zbran: Zbran):
        self.zbrane.append(zbran)

    def pridej_vybaveni(self, vybaveni_id, vlastnik="hrac"):
        """Přidá trvalé vybavení do loadoutu hráče nebo člena týmu."""
        if not isinstance(vybaveni_id, str) or not vybaveni_id:
            return False
        vlastnik = str(vlastnik)
        self.vybaveni.setdefault(vlastnik, [])
        if vybaveni_id not in self.vybaveni[vlastnik]:
            self.vybaveni[vlastnik].append(vybaveni_id)
        return True

    vybav = pridej_vybaveni

    def odeber_vybaveni(self, vybaveni_id, vlastnik="hrac"):
        vybaveni = self.vybaveni.get(str(vlastnik), [])
        if vybaveni_id not in vybaveni:
            return False
        vybaveni.remove(vybaveni_id)
        if not vybaveni:
            self.vybaveni.pop(str(vlastnik), None)
        return True

    odejmi = odeber_vybaveni

    def bonus_vybaveni(self, vlastnik="hrac"):
        from models.equipment import EQUIPMENT
        return sum(
            int(EQUIPMENT.get(item_id, {}).get("bojovy_bonus", 0))
            for item_id in self.vybaveni.get(str(vlastnik), [])
        )

    def pridej_predmet(self, predmet_id, mnozstvi=1):
        if mnozstvi <= 0:
            return
        for predmet in self.predmety:
            if isinstance(predmet, dict) and predmet.get("id") == predmet_id:
                predmet["mnozstvi"] = max(1, int(predmet.get("mnozstvi", 0))) + mnozstvi
                return
        self.predmety.append({"id": predmet_id, "mnozstvi": mnozstvi})

    def pocet_predmetu(self, predmet_id):
        celkem = 0
        for predmet in self.predmety:
            if isinstance(predmet, str) and predmet == predmet_id:
                celkem += 1
            elif isinstance(predmet, dict) and predmet.get("id") == predmet_id:
                celkem += max(0, int(predmet.get("mnozstvi", 1)))
        return celkem

    def odeber_predmet(self, predmet_id, mnozstvi=1):
        if self.pocet_predmetu(predmet_id) < mnozstvi:
            return False
        nove = []
        zbyva = mnozstvi
        for predmet in self.predmety:
            if zbyva and isinstance(predmet, str) and predmet == predmet_id:
                zbyva -= 1
                continue
            if zbyva and isinstance(predmet, dict) and predmet.get("id") == predmet_id:
                pocet = max(0, int(predmet.get("mnozstvi", 1)))
                odebrat = min(pocet, zbyva)
                zbyva -= odebrat
                pocet -= odebrat
                if pocet:
                    predmet = dict(predmet)
                    predmet["mnozstvi"] = pocet
                else:
                    continue
            nove.append(predmet)
        self.predmety = nove
        return True

    def seznam_predmetu(self):
        from game.predmety import PREDMETY
        seznam = []
        for predmet in self.predmety:
            if isinstance(predmet, str):
                predmet_id, mnozstvi = predmet, 1
            elif isinstance(predmet, dict):
                predmet_id = predmet.get("id")
                mnozstvi = max(1, int(predmet.get("mnozstvi", 1)))
            else:
                continue
            nazev = PREDMETY.get(predmet_id, {}).get("nazev", predmet_id)
            seznam.append(f"{nazev} x{mnozstvi}")
        return seznam

    def odeber_zbran(self, nazev):
        self.zbrane = [z for z in self.zbrane if z.nazev != nazev]

    def to_dict(self):
        return {
            "predmety": self.predmety,
            "zbrane": [z.to_dict() if hasattr(z, 'to_dict') else z for z in self.zbrane],
            "penize_v_bance": self.penize_v_bance,
            "vybaveni": self.vybaveni,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data inventáře musí být objekt.")
        inv = cls()
        predmety = data.get("predmety", [])
        inv.predmety = predmety if isinstance(predmety, list) else []
        zbrane = data.get("zbrane", [])
        allowed = {f.name for f in fields(Zbran)}
        inv.zbrane = [
            Zbran(**{key: value for key, value in z.items() if key in allowed})
            if isinstance(z, dict) else z
            for z in zbrane
        ] if isinstance(zbrane, list) else []
        inv.penize_v_bance = data.get("penize_v_bance", 0)
        vybaveni = data.get("vybaveni", {})
        if isinstance(vybaveni, dict):
            inv.vybaveni = {
                str(vlastnik): [str(item) for item in hodnoty if isinstance(item, str)]
                for vlastnik, hodnoty in vybaveni.items()
                if isinstance(hodnoty, list)
            }
        return inv
