# models/agent.py
from dataclasses import dataclass, asdict

@dataclass
class Agent:
    jmeno: str
    specializace: str = "obecny"
    level: int = 1
    xp: int = 0
    odhaleny: bool = False
    unaveny: int = 0

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
