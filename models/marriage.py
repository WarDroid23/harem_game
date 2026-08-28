# models/marriage.py
from dataclasses import dataclass, field, asdict
import random

@dataclass
class Marriage:
    """Reprezentuje manželství mezi hráčem a jednou z otrokyň."""
    partner_jmeno: str
    den_zasnubin: int
    den_svatby: int = None
    stav: str = "zasnubeni"  # zasnubeni, vdana, rozvedena
    deti: list = field(default_factory=list)
    cerem_puvab: int = 50  # Jak poutavá byla svatba (0-100)
    intimita_level: int = 0  # 0-100, roste s každou interakcí
    
    def je_vdana(self):
        """Vrátí True pokud je již vdaná (ne jen zasnoubená)."""
        return self.stav == "vdana"
    
    def je_rozvedena(self):
        """Vrátí True pokud byla sňatek rozdělen."""
        return self.stav == "rozvedena"
    
    def dny_spolecne_zite(self):
        """Počet dní, kdy spolu žijí."""
        if self.den_svatby is None:
            return 0
        return max(0, self.den_svatby - self.den_zasnubin)
    
    def ma_dite(self):
        """Vrátí True pokud mají dítě/děti."""
        return len(self.deti) > 0
    
    def pocet_deti(self):
        """Vrátí počet dětí."""
        return len(self.deti)
    
    def prida_dite(self, jmeno: str, pohlavi: str = None):
        """Přidá dítě do rodiny."""
        if pohlavi is None:
            pohlavi = random.choice(["kluk", "holka"])
        
        dite = {
            "jmeno": jmeno,
            "pohlavi": pohlavi,
            "vek": 0,
            "loajalita": 70,
            "talent": random.randint(30, 100),
            "typ": random.choice(["bojovník", "kouzelník", "průzkumník"]),
            "status": "žije"
        }
        self.deti.append(dite)
        return dite
    
    def starne_deti(self):
        """Postárne všechna dítka o rok."""
        for dite in self.deti:
            if dite["status"] == "žije":
                dite["vek"] += 1
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data manželství musí být objekt.")
        return cls(**data)
