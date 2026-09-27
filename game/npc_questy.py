"""Opakovatelné úkoly NPC (MPC) s reputačními prahy, odměnami a temnými variantami."""

from dataclasses import dataclass, field
import random

NPC_QUESTY = {
    "mira": {
        "nazev": "Léky pro poutníky",
        "popis": "Míra potřebuje vzácné byliny. Můžeš jí je opatřit… nebo ji využít.",
        "pozadavek": 10, "odmena": 80, "xp": 25, "reputace": 5,
        "temna_varianta": {"odmena": 120, "xp": 15, "reputace": -3, "dark": 5},
        "navazujici": {
            "nazev": "Dům bez řetězů",
            "popis": "Míra tě požádá o ochranu léčebny před lidmi, kteří chtějí její pacienty znovu prodat.",
            "pozadavek": 15, "odmena": 260, "xp": 70, "reputace": 12,
            "odmena_predmet": "zdravotni_balicek",
            "temna_varianta": {"odmena": 340, "xp": 45, "reputace": -10, "dark": 12,
                               "odmena_predmet": "balzam_stinu"}
        }
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
        "temna_varianta": {"odmena": 200, "xp": 25, "reputace": -4, "dark": 6},
        "navazujici": {
            "nazev": "Hvězdná cesta",
            "popis": "Doprovoď Lyru k observatoři a rozhodni, zda její mapy zpřístupníš cestovatelům, nebo je prodáš podsvětí.",
            "pozadavek": 50, "odmena": 300, "xp": 75, "reputace": 10,
            "odmena_predmet": "mapa_hvezd",
            "temna_varianta": {"odmena": 430, "xp": 45, "reputace": -9, "dark": 15,
                               "odmena_predmet": "tajny_vzkaz"}
        }
    },
    "cassian": {
        "nazev": "Ochrana archivu",
        "popis": "Cassian střeží staré knihy.",
        "pozadavek": 50, "odmena": 210, "xp": 55, "reputace": 8,
        "temna_varianta": {"odmena": 280, "xp": 35, "reputace": -6, "dark": 10},
        "navazujici": {
            "nazev": "Klíč k zapomenuté observatoři",
            "popis": "Po záchraně archivu musíš rozhodnout, komu svěříš klíč od uzamčené věže.",
            "pozadavek": 65, "odmena": 420, "xp": 90, "reputace": 14,
            "odmena_predmet": "lucerna_soumraku",
            "odhal_lokace": "zricenina_astralni_veze",
            "temna_varianta": {"odmena": 560, "xp": 55, "reputace": -12, "dark": 20,
                               "odmena_predmet": "krvavy_ametyst"}
        }
    },
    "tereza": {
        "nazev": "Světla v přístavu",
        "popis": "Tereza organizuje noční směny.",
        "pozadavek": 65, "odmena": 280, "xp": 70, "reputace": 10,
        "temna_varianta": {"odmena": 350, "xp": 40, "reputace": -8, "dark": 12},
        "navazujici": {
            "nazev": "Příliv bez světel",
            "popis": "Ochraň uprchlíky na nočním molu a rozhodni, komu připadne jejich tajná zásilka.",
            "pozadavek": 78, "odmena": 520, "xp": 110, "reputace": 16,
            "odmena_predmet": "mesicni_kompas",
            "temna_varianta": {"odmena": 680, "xp": 65, "reputace": -14, "dark": 25,
                               "odmena_predmet": "pecet_svedka"}
        }
    },
    "selene": {
        "nazev": "Noční hlídka",
        "popis": "Selene hlídá temné uličky. Ví o lidech, kteří mizí.",
        "pozadavek": 25, "odmena": 130, "xp": 35, "reputace": 5,
        "temna_varianta": {"odmena": 190, "xp": 20, "reputace": -7, "dark": 9},
        "navazujici": {
            "nazev": "Zrcadla astrální citadely",
            "popis": "Pomoz Selene obnovit zrcadlovou síť citadely, nebo ji využij k odposlechu cestovatelů.",
            "pozadavek": 40, "odmena": 360, "xp": 80, "reputace": 12,
            "odmena_predmet": "klic_observatore",
            "temna_varianta": {
                "odmena": 470, "xp": 50, "reputace": -9, "dark": 16,
                "odmena_predmet": "tajny_vzkaz",
            },
        },
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
    "madame_scarlett": {
        "nazev": "Hedvábí a tajemství",
        "popis": "Madame Scarlett potřebuje zajistit luxusní parfémy a uklidnit zdivočelého hosta.",
        "pozadavek": 30, "odmena": 160, "xp": 35, "reputace": 6,
        "temna_varianta": {"odmena": 240, "xp": 25, "reputace": -4, "dark": 8}
    },
    "baron_archibald": {
        "nazev": "Šlechtické choutky",
        "popis": "Baron shání vzácný nápoj lásky a diskrétní společnost pro svůj večírek.",
        "pozadavek": 45, "odmena": 210, "xp": 45, "reputace": 5,
        "temna_varianta": {"odmena": 310, "xp": 30, "reputace": -7, "dark": 12}
    },
    "gladiator_gor": {
        "nazev": "Krev v aréně",
        "popis": "Gor hledá sparring partnera a dodávku hojivých mastí pro gladiátory.",
        "pozadavek": 40, "odmena": 190, "xp": 50, "reputace": 4,
        "temna_varianta": {"odmena": 270, "xp": 35, "reputace": -6, "dark": 10}
    },
    "lady_eleanor": {
        "nazev": "Pavučina na terasách",
        "popis": "Lady Eleanor potřebuje zcizit kompromitující dopis z paláce guvernéra.",
        "pozadavek": 60, "odmena": 260, "xp": 60, "reputace": 8,
        "temna_varianta": {"odmena": 360, "xp": 40, "reputace": -8, "dark": 14},
        "navazujici": {
            "nazev": "Dopis bez podpisu",
            "popis": "Rozhodni, zda zveřejníš důkaz o korupci městské rady, nebo dopis prodáš nejvyšší nabídce.",
            "pozadavek": 75, "odmena": 440, "xp": 95, "reputace": 14,
            "odmena_predmet": "dukazni_listina",
            "temna_varianta": {
                "odmena": 590, "xp": 55, "reputace": -12, "dark": 18,
                "odmena_predmet": "krvavy_ametyst",
            },
        },
    },
}


@dataclass
class NPCQuestSystem:
    aktivni: dict = field(default_factory=dict)
    dokoncene: dict = field(default_factory=dict)

    def dostupne(self, hra):
        dostupne = []
        for ident, zaklad in NPC_QUESTY.items():
            if self.aktivni.get(ident):
                continue
            pocet = int(self.dokoncene.get(ident, 0))
            quest = zaklad.get("navazujici") if pocet == 1 else zaklad
            if not quest:
                continue
            if hra.svet.vztahy_npc.get(ident, 0) >= quest["pozadavek"]:
                dostupne.append((ident, quest))
        return dostupne

    def prijmi(self, hra, npc_id):
        nalezeny = next(
            ((ident, quest) for ident, quest in self.dostupne(hra) if ident == npc_id),
            None,
        )
        if nalezeny is None:
            return False
        self.aktivni[npc_id] = {
            "npc_id": npc_id,
            "quest": nalezeny[1],
            "pokrok": 0,
            "temna": False,
        }
        return True

    def dokoncit(self, hra, npc_id, temna=False):
        if npc_id not in self.aktivni or npc_id not in NPC_QUESTY:
            return False
        aktivni = self.aktivni[npc_id]
        quest = aktivni.get("quest") if isinstance(aktivni, dict) else None
        if not isinstance(quest, dict):
            quest = NPC_QUESTY[npc_id]
        je_retezec = int(self.dokoncene.get(npc_id, 0)) >= 1
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
            self._udelej_extra_odmenu(hra, var)
            self._zaznamenej_achievementy(hra, je_retezec)
            self._zapis_vysledek(hra, quest, npc_id, "temná")
            return "temna"
        else:
            hra.hrac.gold += quest["odmena"]
            hra.hrac.pridej_xp(quest["xp"])
            hra.svet.zmen_vztah(npc_id, quest["reputace"])
            hra.hrac.reputace_mesta += quest["reputace"] // 2
            self._udelej_extra_odmenu(hra, quest)
            self._zaznamenej_achievementy(hra, je_retezec)
            self._zapis_vysledek(hra, quest, npc_id, "čestná")
            return "normal"

    @staticmethod
    def _udelej_extra_odmenu(hra, data):
        predmet = data.get("odmena_predmet")
        if predmet:
            hra.hrac.inventar.pridej_predmet(predmet)
        lokace = data.get("odhal_lokace")
        if lokace and hra.svet.odhal_lokaci(lokace):
            from game.kronika import zaznamenej
            zaznamenej(hra, f"Odhalena nová lokace: {lokace}.")

    @staticmethod
    def _zaznamenej_achievementy(hra, je_retezec):
        achievementy = getattr(hra, "achievementy", None)
        if achievementy is None:
            return
        achievementy.zaznamenej("npc_questy")
        if je_retezec:
            achievementy.zaznamenej("npc_retezce")

    def stav_pro_npc(self, hra, npc_id):
        """Vrátí stav úkolu pro zobrazení v NPC menu."""
        aktivni = self.aktivni.get(npc_id)
        if aktivni:
            quest = aktivni.get("quest", {})
            return "aktivni", quest
        for ident, quest in self.dostupne(hra):
            if ident == npc_id:
                return "dostupny", quest
        return "zamceny", None

    @staticmethod
    def _zapis_vysledek(hra, quest, npc_id, vetev):
        """Zachová volbu hráče v kronice a připraví půdu pro návazné systémy."""
        from game.kronika import zaznamenej
        zaznamenej(
            hra,
            f"NPC úkol «{quest['nazev']}» ({npc_id}): zvolena {vetev} větev."
        )

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
