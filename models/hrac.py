# models/hrac.py
from dataclasses import dataclass, field, asdict
from models.inventory import Inventory
from models.agent import Agent

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
        "vyjednavani": 0
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
    inventar: Inventory = field(default_factory=Inventory)

    def pridej_xp(self, m):
        self.xp += m
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.xp_next = int(self.xp_next * 1.65)
            self.max_hp += 12
            self.hp = self.max_hp
            self.skill_body += 1
            print(f"⭐ LEVEL UP! {self.level}")

    def to_dict(self):
        d = asdict(self)
        d["inventar"] = self.inventar.to_dict()
        d["agenti"] = [a.to_dict() for a in self.agenti]
        return d

    @classmethod
    def from_dict(cls, data):
        inv_data = data.pop("inventar", None)
        agenti_data = data.pop("agenti", [])
        h = cls(**data)
        if inv_data:
            h.inventar = Inventory.from_dict(inv_data)
        h.agenti = [Agent.from_dict(a) for a in agenti_data]
        return h
