# models/nevestinec.py
from dataclasses import dataclass, field, asdict, fields

@dataclass
class Nevestinec:
    otevreno: bool = False
    nazev: str = "Rudý samet"
    pocet_pokoju: int = 3
    uroven_luxusu: int = 1
    ochranka: int = 1
    celkovy_zisk: int = 0
    obslouzeno_zakazniku: int = 0
    reputace_podniku: int = 10

    def cena_rozsireni_pokoju(self) -> int:
        return self.pocet_pokoju * 120

    def cena_luxusu(self) -> int:
        return self.uroven_luxusu * 150

    def cena_ochranky(self) -> int:
        return self.ochranka * 100

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict):
            return cls()
        allowed = {f.name for f in fields(cls)}
        clean = {k: v for k, v in data.items() if k in allowed}
        return cls(**clean)
