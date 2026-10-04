"""Opakovatelné úkoly NPC (MPC) s reputačními prahy, odměnami a temnými variantami."""

from dataclasses import dataclass, field

from game.balance import uprav_odmenu, uprav_xp

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
    "maren_prevoznik": {
        "nazev": "Zásilka proti proudu",
        "popis": "Maren potřebuje dopravit léky do nábřežní osady dřív, než stoupne řeka.",
        "pozadavek": 8, "odmena": 140, "xp": 35, "reputace": 7,
        "temna_varianta": {
            "odmena": 210, "xp": 25, "reputace": -5, "dark": 8,
            "frakce_dopad": {"obchodnici": -3, "syndikat_stinu": 3},
            "kontrola_uzemi": {"Říční nábřeží": 4},
        },
        "navazujici": {
            "nazev": "Most pro dvě čtvrti",
            "popis": "Zajisti průchod přes řeku a rozhodni, zda bude sloužit všem, nebo jen tvé síti.",
            "pozadavek": 18, "odmena": 300, "xp": 75, "reputace": 12,
            "odmena_predmet": "mesicni_kompas",
            "frakce_dopad": {"obchodnici": 6, "policie": 2},
            "kontrola_uzemi": {"Říční nábřeží": 8},
            "temna_varianta": {
                "odmena": 430, "xp": 50, "reputace": -10, "dark": 15,
                "frakce_dopad": {"syndikat_stinu": 8, "obchodnici": -5},
                "kontrola_uzemi": {"Říční nábřeží": 12},
                "vliv_mafie": 6,
            },
        },
        "jednorazovy": True,
    },
    "oren_mistr_cechu": {
        "nazev": "Znamení na cechovních dveřích",
        "popis": "Oren hledá autora značek, které rozhádaly řemeslnické cechy.",
        "pozadavek": 8, "odmena": 130, "xp": 35, "reputace": 6,
        "frakce_dopad": {"obchodnici": 3},
        "temna_varianta": {
            "odmena": 200, "xp": 25, "reputace": -5, "dark": 8,
            "frakce_dopad": {"podsveti": 4, "obchodnici": -4},
            "kontrola_uzemi": {"Cechovní uličky": 5},
        },
        "navazujici": {
            "nazev": "Cechovní přísaha",
            "popis": "Rozhodni, zda nové smlouvy ochrání malé dílny, nebo podřídí cechy tvým lidem.",
            "pozadavek": 18, "odmena": 280, "xp": 70, "reputace": 11,
            "odmena_predmet": "opravarenska_sada",
            "frakce_dopad": {"obchodnici": 7, "policie": 2},
            "kontrola_uzemi": {"Cechovní uličky": 6},
            "temna_varianta": {
                "odmena": 420, "xp": 45, "reputace": -9, "dark": 14,
                "frakce_dopad": {"podsveti": 7, "obchodnici": -6},
                "kontrola_uzemi": {"Cechovní uličky": 12},
                "vliv_mafie": 5,
            },
        },
        "jednorazovy": True,
    },
    "livia_archivarka": {
        "nazev": "Kniha bez katalogového čísla",
        "popis": "Livia potřebuje najít knihu, která se objevila v knihovně bez záznamu o původu.",
        "pozadavek": 8, "odmena": 150, "xp": 40, "reputace": 7,
        "odmena_vyzkum": 3,
        "frakce_dopad": {"obchodnici": 2, "cirkev": 1},
        "temna_varianta": {
            "odmena": 230, "xp": 25, "reputace": -6, "dark": 9,
            "odmena_vyzkum": 2,
            "frakce_dopad": {"syndikat_stinu": 4, "cirkev": -4},
        },
        "navazujici": {
            "nazev": "Otevřený archiv",
            "popis": "Rozhodni, zda zpřístupníš nalezené poznámky učencům, nebo je prodáš zájemcům z podsvětí.",
            "pozadavek": 18, "odmena": 310, "xp": 80, "reputace": 12,
            "odmena_predmet": "mapa_hvezd",
            "odmena_vyzkum": 8,
            "frakce_dopad": {"obchodnici": 6, "cirkev": 3},
            "kontrola_uzemi": {"Akademické náměstí": 5},
            "temna_varianta": {
                "odmena": 470, "xp": 50, "reputace": -10, "dark": 16,
                "odmena_predmet": "tajny_vzkaz",
                "odmena_vyzkum": 5,
                "frakce_dopad": {"syndikat_stinu": 8, "obchodnici": -5},
                "kontrola_uzemi": {"Akademické náměstí": 10},
                "vliv_mafie": 5,
            },
        },
        "jednorazovy": True,
    },
    "nera_dymova": {
        "nazev": "Ztracená směna",
        "popis": "Nera hledá dělníky, kteří se nevrátili z noční směny v Dýmové čtvrti.",
        "pozadavek": 8, "odmena": 160, "xp": 40, "reputace": 7,
        "frakce_dopad": {"podsveti": 2, "policie": 2},
        "temna_varianta": {
            "odmena": 240, "xp": 30, "reputace": -6, "dark": 10,
            "frakce_dopad": {"podsveti": 5, "policie": -4},
            "kontrola_uzemi": {"Dýmová čtvrť": 5},
        },
        "navazujici": {
            "nazev": "Světlo nad komíny",
            "popis": "Rozhodni, zda předáš důkazy městské hlídce, nebo převezmeš noční směny pod svou ochranu.",
            "pozadavek": 18, "odmena": 330, "xp": 85, "reputace": 13,
            "frakce_dopad": {"policie": 6, "obchodnici": 3},
            "kontrola_uzemi": {"Dýmová čtvrť": 6},
            "odhal_lokace": "severni_hradby",
            "temna_varianta": {
                "odmena": 500, "xp": 55, "reputace": -11, "dark": 18,
                "frakce_dopad": {"podsveti": 8, "policie": -7},
                "kontrola_uzemi": {"Dýmová čtvrť": 14},
                "vliv_mafie": 7,
                "odhal_lokace": "severni_hradby",
            },
        },
        "jednorazovy": True,
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
            if zaklad.get("jednorazovy") and pocet >= 2:
                continue
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
            zaklad = NPC_QUESTY[npc_id]
            quest = (
                zaklad.get("navazujici")
                if int(self.dokoncene.get(npc_id, 0)) >= 1
                else zaklad
            )
            quest = quest or zaklad
        je_retezec = int(self.dokoncene.get(npc_id, 0)) >= 1
        self.aktivni.pop(npc_id)
        self.dokoncene[npc_id] = self.dokoncene.get(npc_id, 0) + 1

        if temna and "temna_varianta" in quest:
            var = quest["temna_varianta"]
            obtiznost = getattr(
                getattr(hra, "nastaveni", None), "obtiznost", "normalni"
            )
            hra.hrac.gold += uprav_odmenu(var["odmena"], obtiznost)
            hra.hrac.pridej_xp(uprav_xp(var["xp"], obtiznost))
            hra.svet.zmen_vztah(npc_id, var["reputace"])
            hra.hrac.reputace_mesta += var["reputace"] // 2
            if hasattr(hra.hrac, "dark_energy"):
                hra.hrac.dark_energy = min(100, hra.hrac.dark_energy + var.get("dark", 0))
            self._udelej_extra_odmenu(hra, var)
            self._udelej_nasledky(hra, var)
            self._zaznamenej_achievementy(hra, je_retezec)
            self._zapis_vysledek(hra, quest, npc_id, "temná")
            return "temna"
        else:
            obtiznost = getattr(
                getattr(hra, "nastaveni", None), "obtiznost", "normalni"
            )
            hra.hrac.gold += uprav_odmenu(quest["odmena"], obtiznost)
            hra.hrac.pridej_xp(uprav_xp(quest["xp"], obtiznost))
            hra.svet.zmen_vztah(npc_id, quest["reputace"])
            hra.hrac.reputace_mesta += quest["reputace"] // 2
            self._udelej_extra_odmenu(hra, quest)
            self._udelej_nasledky(hra, quest)
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
    def _udelej_nasledky(hra, data):
        vyzkumne_body = max(0, int(data.get("odmena_vyzkum", 0)))
        if vyzkumne_body:
            hra.vyzkum.pridej_body(vyzkumne_body)

        zmenena_frakce = False
        for frakce_id, delta in data.get("frakce_dopad", {}).items():
            frakce = hra.frakce.frakce.get(frakce_id)
            if frakce:
                frakce.zmenit(int(delta))
                zmenena_frakce = True

        kontrola = data.get("kontrola_uzemi", {})
        zmenena_kontrola = False
        for uzemi in hra.mafie.uzemi:
            delta = kontrola.get(uzemi.nazev)
            if delta is not None and uzemi.obsazeno:
                nova_kontrola = max(0, min(100, uzemi.kontrola + int(delta)))
                zmenena_kontrola = zmenena_kontrola or nova_kontrola != uzemi.kontrola
                uzemi.kontrola = nova_kontrola

        vliv = int(data.get("vliv_mafie", 0))
        zmeneny_vliv = False
        if vliv:
            puvodni_vliv = hra.mafie.vliv_ve_meste
            hra.mafie.vliv_ve_meste = max(
                0, min(100, puvodni_vliv + vliv)
            )
            zmeneny_vliv = hra.mafie.vliv_ve_meste != puvodni_vliv

        if vyzkumne_body or zmenena_frakce or zmenena_kontrola or zmeneny_vliv:
            from game.kronika import zaznamenej
            dusledky = []
            if vyzkumne_body:
                dusledky.append(f"+{vyzkumne_body} výzkumných bodů")
            if zmenena_frakce:
                dusledky.append("změna reputace frakcí")
            if zmenena_kontrola:
                dusledky.append("změna kontroly území")
            if zmeneny_vliv:
                dusledky.append(f"vliv mafie {vliv:+d}")
            zaznamenej(hra, "Důsledky úkolu: " + "; ".join(dusledky) + ".")

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
