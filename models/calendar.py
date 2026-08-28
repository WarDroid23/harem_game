from dataclasses import dataclass, field


ROCNI_OBDOBI = ("jaro", "leto", "podzim", "zima")


@dataclass
class CalendarSystem:
    """Herní kalendář synchronizovaný s historickým atributem Hrac.den."""

    den: int = 1
    udalosti: list = field(default_factory=list)
    posledni_udalost: str = ""

    @property
    def sezona(self):
        return ROCNI_OBDOBI[((max(1, int(self.den)) - 1) // 7) % len(ROCNI_OBDOBI)]

    @property
    def tyden(self):
        return ((max(1, int(self.den)) - 1) // 7) + 1

    def dalsi_den(self, den=None):
        self.den = max(1, int(self.den if den is None else den)) + 1
        self.posledni_udalost = self.sezonni_udalost()
        if self.posledni_udalost:
            self.udalosti.append({"den": self.den, "udalost": self.posledni_udalost})
            self.udalosti = self.udalosti[-30:]
        return self.posledni_udalost

    def sezonni_udalost(self):
        udalosti = {
            "jaro": "Jarní obnova: péče o spojence je účinnější.",
            "leto": "Letní trhy: výpravy přinášejí více zlata.",
            "podzim": "Podzimní mlhy: průzkum je riskantnější, ale odhalí více cest.",
            "zima": "Zimní slavnost: reputace města získá za každý bezpečný návrat.",
        }
        return udalosti.get(self.sezona, "")

    def to_dict(self):
        return {
            "den": self.den,
            "udalosti": self.udalosti,
            "posledni_udalost": self.posledni_udalost,
        }

    @classmethod
    def from_dict(cls, data, fallback_den=1):
        if not isinstance(data, dict):
            return cls(den=max(1, int(fallback_den)))
        try:
            den = max(1, int(data.get("den", fallback_den)))
        except (TypeError, ValueError):
            den = max(1, int(fallback_den))
        udalosti = data.get("udalosti", [])
        return cls(
            den=den,
            udalosti=udalosti[-30:] if isinstance(udalosti, list) else [],
            posledni_udalost=data.get("posledni_udalost", "")
            if isinstance(data.get("posledni_udalost", ""), str) else "",
        )
