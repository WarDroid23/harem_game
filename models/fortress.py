# models/fortress.py
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
import random

PEVNOSTNI_BUDOVY = {
    # Původní klíče pro plnou zpětnou kompatibilitu
    "strazni_vez": {
        "nazev": "Strážní věž s balistami",
        "kategorie": "obrana",
        "cena_zlato": 220,
        "cena_drevo": 40,
        "cena_kamen": 60,
        "cena_zelezo": 15,
        "popis": "Automaticky ostřeluje nájezdníky a dává +5 k obraně hráče v soubojích za úroveň.",
    },
    "dilna": {
        "nazev": "Dílna pevnosti",
        "kategorie": "vyroba",
        "cena_zlato": 260,
        "cena_drevo": 50,
        "cena_kamen": 40,
        "cena_zelezo": 25,
        "popis": "Zvyšuje kvalitu vybavení a zlevňuje opravy výzbroje.",
    },
    "archiv": {
        "nazev": "Temný archiv & Knihovna",
        "kategorie": "mystika",
        "cena_zlato": 300,
        "cena_drevo": 60,
        "cena_kamen": 50,
        "cena_zelezo": 10,
        "popis": "Uchovává zakázané spisy. Přidává zkušenosti a vyrábí 3 výzkumné body denně za úroveň.",
    },
    "zahrada": {
        "nazev": "Zahrada rozkoše a klidu",
        "kategorie": "harem",
        "cena_zlato": 240,
        "cena_drevo": 70,
        "cena_kamen": 30,
        "cena_zelezo": 0,
        "popis": "Ráj květin a altánů. Každý den zvyšuje loajalitu a důvěru všech otrokyň v pevnosti.",
    },
    # Nové budovy pro plnohodnotnou budovatelskou strategii
    "pila": {
        "nazev": "Pila & Lesní tábor",
        "kategorie": "suroviny",
        "cena_zlato": 150,
        "cena_drevo": 20,
        "cena_kamen": 30,
        "cena_zelezo": 5,
        "popis": "Těží dřevo v okolních hvozdech. Denní produkce: +25 dřeva za úroveň.",
    },
    "kamenolom": {
        "nazev": "Žulový kamenolom",
        "kategorie": "suroviny",
        "cena_zlato": 180,
        "cena_drevo": 40,
        "cena_kamen": 20,
        "cena_zelezo": 10,
        "popis": "Láme pevný stavební kámen. Denní produkce: +20 kamene za úroveň.",
    },
    "dul": {
        "nazev": "Hluboký železný důl",
        "kategorie": "suroviny",
        "cena_zlato": 250,
        "cena_drevo": 60,
        "cena_kamen": 50,
        "cena_zelezo": 10,
        "popis": "Těží železnou rudu a drahé kovy. Denní produkce: +15 železa za úroveň.",
    },
    "statek": {
        "nazev": "Panský statek & Sýpky",
        "kategorie": "suroviny",
        "cena_zlato": 160,
        "cena_drevo": 50,
        "cena_kamen": 30,
        "cena_zelezo": 5,
        "popis": "Pěstuje obilí a chová dobytek. Denní produkce: +30 zásob jídla za úroveň.",
    },
    "hradby": {
        "nazev": "Masivní kamenné hradby",
        "kategorie": "obrana",
        "cena_zlato": 280,
        "cena_drevo": 30,
        "cena_kamen": 90,
        "cena_zelezo": 25,
        "popis": "Základní štít dominia. Zvyšuje obranu pevnosti před nájezdy o +35 za úroveň.",
    },
    "kasarna": {
        "nazev": "Kasárna & Cvičiště gardy",
        "kategorie": "obrana",
        "cena_zlato": 260,
        "cena_drevo": 60,
        "cena_kamen": 60,
        "cena_zelezo": 35,
        "popis": "Trénuje elitní stráže dominia. Dává hráči +4 k útoku v soubojích za úroveň.",
    },
    "kovarna": {
        "nazev": "Mistrovská kovárna",
        "kategorie": "vyroba",
        "cena_zlato": 240,
        "cena_drevo": 30,
        "cena_kamen": 50,
        "cena_zelezo": 40,
        "popis": "Kove prvotřídní ostří a brnění. Zvyšuje útočné poškození hráče a snižuje ceny výbavy.",
    },
    "oltar_stinu": {
        "nazev": "Oltář temných stínů",
        "kategorie": "mystika",
        "cena_zlato": 320,
        "cena_drevo": 30,
        "cena_kamen": 70,
        "cena_zelezo": 20,
        "popis": "Shromažďuje temné esence. Denně přináší +4 temnou energii a +2 mana krystaly za úroveň.",
    },
    "lazne_dominia": {
        "nazev": "Lázeňský pavilon dominia",
        "kategorie": "harem",
        "cena_zlato": 200,
        "cena_drevo": 50,
        "cena_kamen": 50,
        "cena_zelezo": 5,
        "popis": "Mramorové lázně pro regeneraci a potěšení harému. Léčí +5 HP a +3 loajalitu dívkám denně.",
    },
    "bylinkovy_sklenik": {
        "nazev": "Bylinkový skleník & Sušárna",
        "kategorie": "mystika",
        "cena_zlato": 210,
        "cena_drevo": 60,
        "cena_kamen": 30,
        "cena_zelezo": 5,
        "popis": "Pěstuje alchymistické byliny a houby. Denně dodává zásoby pro alchymii a výrobu drog.",
    },
    "alchymisticka_laborator": {
        "nazev": "Alchymistická laboratoř & Syntéza",
        "kategorie": "vyroba",
        "cena_zlato": 270,
        "cena_drevo": 40,
        "cena_kamen": 50,
        "cena_zelezo": 20,
        "popis": "Automatizuje syntézu lektvarů. Přináší +45 🪙, +3 temné energie a +1 výzkumný bod denně za úroveň.",
    },
}


@dataclass
class FortressDevelopment:
    uroven: int = 1
    zasoby: int = 80       # Jídlo a proviant
    drevo: int = 120       # Dřevo na stavby
    kamen: int = 90        # Kámen na zdivo
    zelezo: int = 40       # Železo na výzbroj
    krystaly: int = 15     # Magické krystaly
    budovy: Dict[str, int] = field(default_factory=lambda: {key: 0 for key in PEVNOSTNI_BUDOVY})
    rozsireni: List[str] = field(default_factory=list)
    pracovnici: Dict[str, str] = field(default_factory=dict)  # budova_id -> jmeno_otrokine
    danova_politika: str = "vyvazena"               # "laskava", "vyvazena", "kruta"
    karavany_aktivni: List[Dict[str, Any]] = field(default_factory=list)
    arena_rank: int = 0                            # 0: Rekrut, 1: Rváč, 2: Gladiátor, 3: Šampion, 4: Bůh arény
    bojova_partnerka: str = ""                     # jméno zvolené otrokyně do soubojů
    personal: Dict[str, Any] = field(default_factory=dict)   # personál dominia: spravce, vyhazovac, alchymista

    def cena_vylepseni(self, budova=None):
        if budova is None:
            return 400 * self.uroven
        if budova not in PEVNOSTNI_BUDOVY:
            return None
        lvl = self.budovy.get(budova, 0)
        multi = 1.0 + lvl * 0.45
        info = PEVNOSTNI_BUDOVY[budova]
        return {
            "zlato": int(info.get("cena_zlato", info.get("cena", 200)) * multi),
            "drevo": int(info.get("cena_drevo", 20) * multi),
            "kamen": int(info.get("cena_kamen", 20) * multi),
            "zelezo": int(info.get("cena_zelezo", 10) * multi),
        }

    def muze_postavit(self, budova, hrac=None, zlato_hrace=None):
        ceny = self.cena_vylepseni(budova)
        if not ceny:
            return False, "Neznámá budova."
        zlato = zlato_hrace if zlato_hrace is not None else (getattr(hrac, "gold", hrac) if hrac is not None else 0)
        if zlato < ceny["zlato"]:
            return False, f"Nedostatek zlata (potřebuješ {ceny['zlato']} 🪙)."
        if self.drevo < ceny["drevo"]:
            return False, f"Nedostatek dřeva (potřebuješ {ceny['drevo']} 🪵)."
        if self.kamen < ceny["kamen"]:
            return False, f"Nedostatek kamene (potřebuješ {ceny['kamen']} 🪨)."
        if self.zelezo < ceny["zelezo"]:
            return False, f"Nedostatek železa (potřebuješ {ceny['zelezo']} ⚒️)."
        return True, "Lze postavit."

    def vylepsi_budovu(self, budova, hrac=None, zlato_hrace=None):
        muze, duvod = self.muze_postavit(budova, hrac=hrac, zlato_hrace=zlato_hrace)
        if not muze:
            return False, duvod
        ceny = self.cena_vylepseni(budova)
        if hrac is not None and hasattr(hrac, "gold"):
            hrac.gold -= ceny["zlato"]
        self.drevo -= ceny["drevo"]
        self.kamen -= ceny["kamen"]
        self.zelezo -= ceny["zelezo"]
        self.budovy[budova] = self.budovy.get(budova, 0) + 1
        return True, f"Budova {PEVNOSTNI_BUDOVY[budova]['nazev']} vylepšena na úroveň {self.budovy[budova]}!"

    def vylepsi(self, budova=None, zlato=None):
        """Zpětná kompatibilita pro testy a staré volání."""
        if budova is None:
            cena = 400 * self.uroven
            if zlato is not None and zlato < cena:
                return False
            self.uroven += 1
            return True
        ceny = self.cena_vylepseni(budova)
        if not ceny:
            return False
        cena_zlato = ceny["zlato"] if isinstance(ceny, dict) else ceny
        if zlato is not None and zlato < cena_zlato:
            return False
        self.budovy[budova] = self.budovy.get(budova, 0) + 1
        return True

    def celkova_obrana_pevnosti(self):
        obrana = self.budovy.get("hradby", 0) * 35
        obrana += self.budovy.get("strazni_vez", 0) * 25
        obrana += self.budovy.get("kasarna", 0) * 20
        obrana += self.uroven * 15
        return obrana

    def bonusy(self):
        return {
            "obrana": self.budovy.get("strazni_vez", 0) * 5 + self.budovy.get("hradby", 0) * 3,
            "utok": self.budovy.get("kasarna", 0) * 4 + self.budovy.get("kovarna", 0) * 3,
            "vybava": self.budovy.get("dilna", 0) + self.budovy.get("kovarna", 0),
            "xp": self.budovy.get("archiv", 0) * 4,
            "duvera": self.budovy.get("zahrada", 0) * 3,
        }

    def denni_produkce(self, hra):
        """Vypočítá denní produkci surovin, spotřebu jídla a efekt daní."""
        zpravy = []

        # Produkce ze surovinových budov
        drevo_zisk = self.budovy.get("pila", 0) * 25
        kamen_zisk = self.budovy.get("kamenolom", 0) * 20
        zelezo_zisk = self.budovy.get("dul", 0) * 15
        jidlo_zisk = self.budovy.get("statek", 0) * 30
        temno_zisk = self.budovy.get("oltar_stinu", 0) * 4
        krystaly_zisk = self.budovy.get("oltar_stinu", 0) * 2

        # Produkce ze skleníku a alchymistické laboratoře
        sklenik_lvl = self.budovy.get("bylinkovy_sklenik", 0)
        if sklenik_lvl > 0 and hasattr(hra, "alchymie"):
            hra.alchymie.pridat_surovinu("bylina_mesicni", sklenik_lvl * 2)
            hra.alchymie.pridat_surovinu("vzacna_houba", sklenik_lvl * 1)
            zpravy.append(f"🌿 Skleník sklidil {sklenik_lvl * 2}x Měsíční bylina a {sklenik_lvl}x Vzácná houba pro alchymii!")

        lab_lvl = self.budovy.get("alchymisticka_laborator", 0)
        if lab_lvl > 0:
            hra.hrac.gold += lab_lvl * 45
            temno_zisk += lab_lvl * 3
            zpravy.append(f"🧪 Alchymistická laboratoř vygenerovala +{lab_lvl * 45} 🪙 a +{lab_lvl * 3} temné energie!")

        body_vyzkumu = 0
        if hasattr(hra, "vyzkum"):
            body_vyzkumu = hra.vyzkum.produkce_bodu_za_den(hra)
            if body_vyzkumu:
                hra.vyzkum.pridej_body(body_vyzkumu)
                zpravy.append(f"🔬 Laboratoře vytvořily +{body_vyzkumu} výzkumných bodů.")

        # Efekty najatého personálu
        if getattr(self, "personal", {}).get("spravce_nevestince", False):
            bonus_nev = 75
            hra.hrac.gold += bonus_nev
            zpravy.append(f"💼 Správce nevěstince zorganizoval provoz a zvýšil tržby o +{bonus_nev} 🪙!")

        if getattr(self, "personal", {}).get("vrchni_vyhazovac", False):
            hra.hrac.vliv_inkvizice = max(0, getattr(hra.hrac, "vliv_inkvizice", 0) - 2)
            zpravy.append("🛡️ Vrchní vyhazovač zajistil naprostý pořádek v dominia a odradil zvědy.")

        if getattr(self, "personal", {}).get("alchymista_tovarys", False):
            if hasattr(hra, "alchymie"):
                hra.alchymie.pridat_surovinu("bylina_mesicni", 1)
                hra.alchymie.pridat_surovinu("esence_temna", 1)
            zpravy.append("⚗️ Alchymistický tovaryš syntetizoval čisté esence pro tvé lektvary.")

        # Bonusy z přiřazených dívek
        for b_id, jmeno in self.pracovnici.items():
            otrok = next((o for o in hra.harem.vsechny_aktivni() if o.jmeno == jmeno), None)
            if not otrok:
                continue
            char = getattr(otrok, "charakter", "")
            if b_id == "pila":
                drevo_zisk += 15
            elif b_id == "kamenolom":
                kamen_zisk += 12
            elif b_id == "dul":
                zelezo_zisk += 10
                if char == "zlodejka" and random.random() < 0.4:
                    hra.hrac.gold += 35
                    zpravy.append(f"Zlodějka {otrok.jmeno} našla v dole zlatou žílu (+35 🪙)!")
            elif b_id == "statek":
                jidlo_zisk += 20
            elif b_id == "oltar_stinu":
                temno_zisk += 6
                krystaly_zisk += 3
            elif b_id == "kasarna":
                if char in ("amazonka", "padla_paladinka"):
                    zpravy.append(f"{otrok.jmeno} vycvičila stráže v tvrdém boji (+bonus k obraně).")

        self.drevo += drevo_zisk
        self.kamen += kamen_zisk
        self.zelezo += zelezo_zisk
        self.zasoby += jidlo_zisk
        self.krystaly += krystaly_zisk

        if temno_zisk > 0:
            hra.hrac.dark_energy = min(hra.hrac.max_temno(), hra.hrac.dark_energy + temno_zisk)

        # Spotřeba jídla harémem a obránci
        pocet_lidí = len(hra.harem.vsechny_aktivni()) + self.budovy.get("kasarna", 0) * 2
        spotreba_jidla = max(5, pocet_lidí * 2)

        if self.zasoby >= spotreba_jidla:
            self.zasoby -= spotreba_jidla
            # Dostatek jídla zvyšuje morálku
            for o in hra.harem.vsechny_aktivni():
                o.loajalita = min(100, o.loajalita + 1)
        else:
            chybi = spotreba_jidla - self.zasoby
            self.zasoby = 0
            nakup_cena = chybi * 3
            if hra.hrac.gold >= nakup_cena:
                hra.hrac.gold -= nakup_cena
                zpravy.append(f"Nedostatek jídla! Muselo být dokoupeno obilí z trhu za −{nakup_cena} 🪙.")
            else:
                for o in hra.harem.vsechny_aktivni():
                    o.loajalita = max(0, o.loajalita - 4)
                zpravy.append("Hladomor v panství! Loajalita otrokyň klesá.")

        # Daňová politika panství
        zisk_dani = 0
        if self.danova_politika == "laskava":
            zisk_dani = 30 + self.uroven * 15
            hra.hrac.reputace_mesta += 1
            for o in hra.harem.vsechny_aktivni():
                o.loajalita = min(100, o.loajalita + 1)
        elif self.danova_politika == "vyvazena":
            zisk_dani = 90 + self.uroven * 35
        elif self.danova_politika == "kruta":
            zisk_dani = 230 + self.uroven * 70
            hra.hrac.reputace_mesta = max(-50, hra.hrac.reputace_mesta - 1)
            hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + 2)
            zpravy.append("Kruté desátky přinesly bohatství, ale vzbudily hněv poddaných a inkvizice.")

        hra.hrac.gold += zisk_dani

        # Regenerace z lázní a zahrady
        lazne_lvl = self.budovy.get("lazne_dominia", 0)
        zahrada_lvl = self.budovy.get("zahrada", 0)
        if lazne_lvl > 0 or zahrada_lvl > 0:
            for o in hra.harem.vsechny_aktivni():
                if lazne_lvl > 0:
                    o.hp = min(o.max_hp, o.hp + lazne_lvl * 5)
                if zahrada_lvl > 0:
                    o.duvera = min(100, o.duvera + zahrada_lvl * 2)
                    o.loajalita = min(100, o.loajalita + zahrada_lvl * 1)

        return {
            "drevo": drevo_zisk,
            "kamen": kamen_zisk,
            "zelezo": zelezo_zisk,
            "jidlo": jidlo_zisk,
            "krystaly": krystaly_zisk,
            "dane": zisk_dani,
            "vyzkum": body_vyzkumu,
            "zpravy": zpravy,
        }

    def to_dict(self):
        return {
            "uroven": self.uroven,
            "zasoby": self.zasoby,
            "drevo": self.drevo,
            "kamen": self.kamen,
            "zelezo": self.zelezo,
            "krystaly": self.krystaly,
            "budovy": self.budovy,
            "rozsireni": self.rozsireni,
            "pracovnici": self.pracovnici,
            "danova_politika": self.danova_politika,
            "karavany_aktivni": self.karavany_aktivni,
            "arena_rank": self.arena_rank,
            "bojova_partnerka": self.bojova_partnerka,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        inst = cls()
        inst.uroven = max(1, int(data.get("uroven", 1)))
        inst.zasoby = max(0, int(data.get("zasoby", 80)))
        inst.drevo = max(0, int(data.get("drevo", 120)))
        inst.kamen = max(0, int(data.get("kamen", 90)))
        inst.zelezo = max(0, int(data.get("zelezo", 40)))
        inst.krystaly = max(0, int(data.get("krystaly", 15)))
        inst.danova_politika = data.get("danova_politika", "vyvazena")
        inst.arena_rank = max(0, int(data.get("arena_rank", 0)))
        inst.bojova_partnerka = str(data.get("bojova_partnerka", ""))
        inst.rozsireni = data.get("rozsireni", []) if isinstance(data.get("rozsireni"), list) else []
        inst.pracovnici = data.get("pracovnici", {}) if isinstance(data.get("pracovnici"), dict) else {}
        inst.karavany_aktivni = data.get("karavany_aktivni", []) if isinstance(data.get("karavany_aktivni"), list) else []

        budovy_raw = data.get("budovy", {})
        inst.budovy = {
            key: max(0, int(budovy_raw.get(key, 0)))
            for key in PEVNOSTNI_BUDOVY
        } if isinstance(budovy_raw, dict) else {key: 0 for key in PEVNOSTNI_BUDOVY}

        return inst
