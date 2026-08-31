"""Opakovatelné úkoly NPC (MPC) s reputačními prahy, odměnami a temnými variantami."""

from dataclasses import dataclass, field
import random

NPC_QUESTY = {
    "mira": {
        "nazev": "Léky pro poutníky",
        "popis": "Míra potřebuje vzácné byliny. Můžeš jí je opatřit… nebo ji využít.",
        "pozadavek": 10, "odmena": 80, "xp": 25, "reputace": 5,
        "temna_varianta": {"odmena": 120, "xp": 15, "reputace": -3, "dark": 5}
    },
    "radan": {
        "nazev": "Tichá zásilka",
        "popis": "Radan chce doručit balíček bez otázek.",
        "pozadavek": 20, "odmena": 110, "xp": 30, "reputace": 4,
        "temna_varianta": {"odmena": 160, "xp": 20, "reputace": -5, "dark": 8}
    },
    "lyra": {
        "nazev": "Bezpečná mapa",
        "popis": "Lyra mapuje nebezpečné stezky.",
        "pozadavek": 35, "odmena": 150, "xp": 40, "reputace": 6,
        "temna_varianta": {"odmena": 200, "xp": 25, "reputace": -4, "dark": 6}
    },
    "cassian": {
        "nazev": "Ochrana archivu",
        "popis": "Cassian střeží staré knihy.",
        "pozadavek": 50, "odmena": 210, "xp": 55, "reputace": 8,
        "temna_varianta": {"odmena": 280, "xp": 35, "reputace": -6, "dark": 10}
    },
    "tereza": {
        "nazev": "Světla v přístavu",
        "popis": "Tereza organizuje noční směny.",
        "pozadavek": 65, "odmena": 280, "xp": 70, "reputace": 10,
        "temna_varianta": {"odmena": 350, "xp": 40, "reputace": -8, "dark": 12}
    },
    "selene": {
        "nazev": "Noční hlídka",
        "popis": "Selene hlídá temné uličky. Ví o lidech, kteří mizí.",
        "pozadavek": 25, "odmena": 130, "xp": 35, "reputace": 5,
        "temna_varianta": {"odmena": 190, "xp": 20, "reputace": -7, "dark": 9}
    },
    "vlad": {
        "nazev": "Dluhy a krev",
        "popis": "Vlad vybírá dluhy. Někdy stačí slovo. Jindy je potřeba víc.",
        "pozadavek": 40, "odmena": 180, "xp": 45, "reputace": 3,
        "temna_varianta": {"odmena": 250, "xp": 30, "reputace": -10, "dark": 15}
    },
    "iris": {
        "nazev": "Šepoty z harému",
        "popis": "Iris sbírá informace z jiných pevností. Ví, které otrokyně jsou na prodej.",
        "pozadavek": 55, "odmena": 220, "xp": 50, "reputace": 7,
        "temna_varianta": {"odmena": 300, "xp": 35, "reputace": -5, "dark": 8}
    },
}


@dataclass
class NPCQuestSystem:
    aktivni: dict = field(default_factory=dict)
    dokoncene: dict = field(default_factory=dict)

    def dostupne(self, hra):
        return [
            (ident, quest) for ident, quest in NPC_QUESTY.items()
            if hra.svet.vztahy_npc.get(ident, 0) >= quest["pozadavek"]
            and not self.aktivni.get(ident)
        ]

    def prijmi(self, hra, npc_id):
        if not any(ident == npc_id for ident, _ in self.dostupne(hra)):
            return False
        self.aktivni[npc_id] = {"npc_id": npc_id, "pokrok": 0, "temna": False}
        return True

    def dokoncit(self, hra, npc_id, temna=False):
        if npc_id not in self.aktivni or npc_id not in NPC_QUESTY:
            return False
        quest = NPC_QUESTY[npc_id]
        self.aktivni.pop(npc_id)
        self.dokoncene[npc_id] = self.dokoncene.get(npc_id, 0) + 1

        if temna and "temna_varianta" in quest:
            var = quest["temna_varianta"]
            hra.hrac.gold += var["odmena"]
            hra.hrac.pridej_xp(var["xp"])
            hra.svet.zmen_vztah(npc_id, var["reputace"])
            hra.hrac.reputace_mesta += var["reputace"] // 2
            if hasattr(hra.hrac, "dark_energy"):
                hra.hrac.dark_energy = min(100, hra.hrac.dark_energy + var.get("dark", 0))
            return "temna"
        else:
            hra.hrac.gold += quest["odmena"]
            hra.hrac.pridej_xp(quest["xp"])
            hra.svet.zmen_vztah(npc_id, quest["reputace"])
            hra.hrac.reputace_mesta += quest["reputace"] // 2
            return "normal"

    def to_dict(self):
        return {"aktivni": self.aktivni, "dokoncene": self.dokoncene}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            aktivni=data.get("aktivni", {}),
            dokoncene=data.get("dokoncene", {}),
        )
