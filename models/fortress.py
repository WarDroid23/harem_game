from dataclasses import dataclass, field


PEVNOSTNI_BUDOVY = {
    "strazni_vez": {"nazev": "Strážní věž", "cena": 220, "bonus_obrana": 5},
    "dilna": {"nazev": "Dílna pevnosti", "cena": 260, "bonus_vybava": 1},
    "archiv": {"nazev": "Archiv", "cena": 300, "bonus_xp": 4},
    "zahrada": {"nazev": "Bezpečná zahrada", "cena": 240, "bonus_duvera": 3},
}


@dataclass
class FortressDevelopment:
    uroven: int = 1
    zasoby: int = 0
    budovy: dict = field(default_factory=lambda: {key: 0 for key in PEVNOSTNI_BUDOVY})
    rozsireni: list = field(default_factory=list)

    def cena_vylepseni(self, budova=None):
        if budova is None:
            return 400 * self.uroven
        if budova not in PEVNOSTNI_BUDOVY:
            return None
        return PEVNOSTNI_BUDOVY[budova]["cena"] * (self.budovy.get(budova, 0) + 1)

    def vylepsi(self, budova=None, zlato=None):
        cena = self.cena_vylepseni(budova)
        if cena is None:
            return False
        if zlato is not None and zlato < cena:
            return False
        if budova is None:
            self.uroven += 1
        else:
            self.budovy[budova] = self.budovy.get(budova, 0) + 1
        return True

    def bonusy(self):
        return {
            "obrana": self.budovy.get("strazni_vez", 0) * 5,
            "vybava": self.budovy.get("dilna", 0),
            "xp": self.budovy.get("archiv", 0) * 4,
            "duvera": self.budovy.get("zahrada", 0) * 3,
        }

    def to_dict(self):
        return {
            "uroven": self.uroven,
            "zasoby": self.zasoby,
            "budovy": self.budovy,
            "rozsireni": self.rozsireni,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        try:
            uroven = max(1, int(data.get("uroven", 1)))
            zasoby = max(0, int(data.get("zasoby", 0)))
        except (TypeError, ValueError):
            uroven, zasoby = 1, 0
        budovy = data.get("budovy", {})
        return cls(
            uroven=uroven,
            zasoby=zasoby,
            budovy={
                key: max(0, int(budovy.get(key, 0)))
                for key in PEVNOSTNI_BUDOVY
            }
            if isinstance(budovy, dict) else {key: 0 for key in PEVNOSTNI_BUDOVY},
            rozsireni=data.get("rozsireni", [])
            if isinstance(data.get("rozsireni", []), list) else [],
        )
