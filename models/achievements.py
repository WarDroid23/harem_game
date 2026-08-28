from dataclasses import dataclass, field


ACHIEVEMENTS = {
    "prvni_vyprava": ("První výprava", "Dokonči první výpravu."),
    "tymova_prace": ("Týmová práce", "Dokonči výpravu se dvěma členkami."),
    "lovec_bossu": ("Lovec bossů", "Poraz příběhového bosse."),
    "stavitel": ("Stavitel", "Vylepši pevnost nebo její budovu."),
    "diplomat": ("Diplomat", "Dosáhni vztahu 75 s NPC."),
    "rok_v_pevnosti": ("Rok v pevnosti", "Přežij 28 herních dní."),
    "tri_osudy": ("Tři uzavřené osudy", "Uzavři tři osobní osudy."),
}


@dataclass
class AchievementSystem:
    odemcene: list = field(default_factory=list)
    statistiky: dict = field(default_factory=dict)

    def zaznamenej(self, udalost, hodnota=1):
        self.statistiky[udalost] = max(0, int(self.statistiky.get(udalost, 0))) + int(hodnota)
        nove = []
        for achievement_id, (_, _) in ACHIEVEMENTS.items():
            if achievement_id in self.odemcene:
                continue
            splneno = {
                "prvni_vyprava": self.statistiky.get("expedice", 0) >= 1,
                "tymova_prace": self.statistiky.get("tymova_expedice", 0) >= 1,
                "lovec_bossu": self.statistiky.get("boss", 0) >= 1,
                "stavitel": self.statistiky.get("stavba", 0) >= 1,
                "diplomat": self.statistiky.get("vztah_75", 0) >= 1,
                "rok_v_pevnosti": self.statistiky.get("dny", 0) >= 28,
                "tri_osudy": self.statistiky.get("osudy", 0) >= 3,
            }[achievement_id]
            if splneno:
                self.odemcene.append(achievement_id)
                nove.append(achievement_id)
        return nove

    def to_dict(self):
        return {"odemcene": self.odemcene, "statistiky": self.statistiky}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        odemcene = data.get("odemcene", [])
        statistiky = data.get("statistiky", {})
        return cls(
            odemcene=[x for x in odemcene if x in ACHIEVEMENTS]
            if isinstance(odemcene, list) else [],
            statistiky={
                str(k): max(0, int(v))
                for k, v in statistiky.items()
                if isinstance(k, str) and isinstance(v, (int, float))
            }
            if isinstance(statistiky, dict) else {},
        )
