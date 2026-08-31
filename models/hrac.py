# models/hrac.py
from dataclasses import dataclass, field, asdict, fields
from models.inventory import Inventory
from models.agent import Agent

ZAKLAD_MAX_SEX = 100
ZAKLAD_MAX_TEMNO = 100
MAX_SEX_STROPP = 250
MAX_TEMNO_STROPP = 200


@dataclass
class Hrac:
    jmeno: str = "LordRusty23"
    level: int = 1
    xp: int = 0
    xp_next: int = 100
    hp: int = 100
    max_hp: int = 100
    gold: int = 500
    sex_energy: int = 70
    dark_energy: int = 20
    max_sex_energy: int = ZAKLAD_MAX_SEX
    max_dark_energy: int = ZAKLAD_MAX_TEMNO
    dominance: int = 5
    kill_count: int = 0
    den: int = 1
    skill_body: int = 2
    skilly: dict = field(default_factory=lambda: {
        "svadeni": 0,
        "obchod": 0,
        "veleni": 0,
        "temnota": 0,
        "obrana": 0,
        "dominance": 0,
        "strelba": 0,
        "boj": 0,
        "vyjednavani": 0,
        "vytrvalost": 0,
    })
    reputace_mesta: int = 0
    titul_mesta: str = "Neznámý"
    vliv_inkvizice: int = 15
    spioni_inkvizice: int = 0
    klient_vernost: dict = field(default_factory=dict)
    agenti: list = field(default_factory=list)
    max_agentu: int = 1
    zpravodajska_uroven: int = 1
    aukcni_bonus: int = 0
    dobiti_dnes: dict = field(default_factory=dict)
    inventar: Inventory = field(default_factory=Inventory)

    def bojovy_bonus_vybavy(self):
        return self.inventar.bonus_vybaveni("hrac")

    def max_sex(self):
        return max(ZAKLAD_MAX_SEX, int(getattr(self, "max_sex_energy", ZAKLAD_MAX_SEX) or ZAKLAD_MAX_SEX))

    def max_temno(self):
        return max(ZAKLAD_MAX_TEMNO, int(getattr(self, "max_dark_energy", ZAKLAD_MAX_TEMNO) or ZAKLAD_MAX_TEMNO))

    def dopln_energie_naplno(self):
        self.sex_energy = self.max_sex()
        self.dark_energy = self.max_temno()

    def omez_energie(self):
        self.sex_energy = max(0, min(self.max_sex(), int(self.sex_energy)))
        self.dark_energy = max(0, min(self.max_temno(), int(self.dark_energy)))

    def pridej_sex_energy(self, kolik):
        self.sex_energy = min(self.max_sex(), self.sex_energy + int(kolik))

    def pridej_dark_energy(self, kolik):
        self.dark_energy = min(self.max_temno(), self.dark_energy + int(kolik))

    def zvys_max_sex(self, o_kolik=5):
        pred = self.max_sex()
        self.max_sex_energy = min(MAX_SEX_STROPP, pred + int(o_kolik))
        return self.max_sex_energy - pred

    def zvys_max_temno(self, o_kolik=3):
        pred = self.max_temno()
        self.max_dark_energy = min(MAX_TEMNO_STROPP, pred + int(o_kolik))
        return self.max_dark_energy - pred

    def pridej_xp(self, m):
        self.xp += m
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.xp_next = int(self.xp_next * 1.65)
            self.max_hp += 12
            self.hp = self.max_hp
            self.skill_body += 1
            self.zvys_max_sex(3)
            self.zvys_max_temno(2)
            self.dopln_energie_naplno()
            print(f"⭐ LEVEL UP! {self.level} | max energie {self.max_sex()}/{self.max_temno()}")

    def to_dict(self):
        d = asdict(self)
        d["inventar"] = self.inventar.to_dict()
        d["agenti"] = [a.to_dict() for a in self.agenti]
        return d

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data hráče musí být objekt.")
        values = dict(data)
        inv_data = values.pop("inventar", None)
        agenti_data = values.pop("agenti", [])
        allowed = {f.name for f in fields(cls)}
        values = {key: value for key, value in values.items() if key in allowed}
        h = cls(**values)
        if isinstance(inv_data, dict):
            h.inventar = Inventory.from_dict(inv_data)
        if isinstance(agenti_data, list):
            h.agenti = [Agent.from_dict(a) for a in agenti_data if isinstance(a, dict)]
        if not isinstance(h.skilly, dict):
            h.skilly = cls().skilly
        if "vytrvalost" not in h.skilly:
            h.skilly["vytrvalost"] = 0
        if not getattr(h, "max_sex_energy", None):
            h.max_sex_energy = ZAKLAD_MAX_SEX + h.skilly.get("vytrvalost", 0) * 5
        if not getattr(h, "max_dark_energy", None):
            h.max_dark_energy = ZAKLAD_MAX_TEMNO + h.skilly.get("vytrvalost", 0) * 3
        if not isinstance(h.dobiti_dnes, dict):
            h.dobiti_dnes = {}
        h.omez_energie()
        return h
