# models/agent.py
from dataclasses import dataclass, asdict, fields

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
        if not isinstance(data, dict):
            raise ValueError("Data agenta musí být objekt.")
        allowed = {f.name for f in fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in allowed})
