"""Opakovatelné úkoly NPC s reputačními prahy a odměnami."""

from dataclasses import dataclass, field


NPC_QUESTY = {
    "mira": {"nazev": "Léky pro poutníky", "pozadavek": 10, "odmena": 80, "xp": 25, "reputace": 5},
    "radan": {"nazev": "Tichá zásilka", "pozadavek": 20, "odmena": 110, "xp": 30, "reputace": 4},
    "lyra": {"nazev": "Bezpečná mapa", "pozadavek": 35, "odmena": 150, "xp": 40, "reputace": 6},
    "cassian": {"nazev": "Ochrana archivu", "pozadavek": 50, "odmena": 210, "xp": 55, "reputace": 8},
    "tereza": {"nazev": "Světla v přístavu", "pozadavek": 65, "odmena": 280, "xp": 70, "reputace": 10},
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
        self.aktivni[npc_id] = {"npc_id": npc_id, "pokrok": 0}
        return True

    def dokoncit(self, hra, npc_id):
        if npc_id not in self.aktivni or npc_id not in NPC_QUESTY:
            return False
        quest = NPC_QUESTY[npc_id]
        self.aktivni.pop(npc_id)
        self.dokoncene[npc_id] = self.dokoncene.get(npc_id, 0) + 1
        hra.hrac.gold += quest["odmena"]
        hra.hrac.pridej_xp(quest["xp"])
        hra.svet.zmen_vztah(npc_id, quest["reputace"])
        hra.hrac.reputace_mesta += quest["reputace"] // 2
        return True

    def to_dict(self):
        return {"aktivni": self.aktivni, "dokoncene": self.dokoncene}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            aktivni=data.get("aktivni", {}) if isinstance(data.get("aktivni", {}), dict) else {},
            dokoncene=data.get("dokoncene", {}) if isinstance(data.get("dokoncene", {}), dict) else {},
        )

    def menu(self, hra):
        from utils.vypis import clear, tisk_chyba, tisk_ok
        while True:
            clear()
            print("--- Úkoly NPC ---")
            for ident, quest in NPC_QUESTY.items():
                vztah = hra.svet.vztahy_npc.get(ident, 0)
                stav = "aktivní" if ident in self.aktivni else f"odměna po vztahu {quest['pozadavek']}"
                print(f"{ident}: {quest['nazev']} ({vztah:+d}) — {stav}")
            print("Z) zahájit | D) dokončit | 0) Zpět")
            volba = input("> ").strip().lower()
            if volba == "0":
                return
            npc_id = input("NPC id: ").strip().lower()
            if volba == "z" and self.prijmi(hra, npc_id):
                tisk_ok("Úkol přijat; splň jeho podmínky a vrať se sem.")
            elif volba == "d" and self.dokoncit(hra, npc_id):
                tisk_ok("Úkol dokončen a odměna vyplacena.")
            else:
                tisk_chyba("Úkol není dostupný nebo aktivní.")
            input("Enter...")
