# game/souboje.py
import random
from utils.vypis import clear, terminalni_obrazek, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, GREEN, RED, CYAN, NC
from game.predmety import PREDMETY
from game.balance import profil_obtiznosti, uprav_odmenu, uprav_xp

BOSSOVE = {
    "strazce_hvezdne_brany": {
        "jmeno": "Strážce hvězdné brány",
        "lokace": "observator",
        "hp": 145,
        "utok": 15,
        "obrana": 10,
        "zlato": 420,
        "xp": 140,
        "faze": [
            {"nazev": "Světelný štít", "hp": 145, "utok": 15, "obrana": 10},
            {"nazev": "Praskající brána", "hp": 95, "utok": 22, "obrana": 7},
        ],
    },
    "kapitan_zeleznich_flotily": {
        "jmeno": "Kapitán železné flotily",
        "lokace": "molo_mesicniho_pristavu",
        "hp": 185,
        "utok": 19,
        "obrana": 13,
        "zlato": 560,
        "xp": 190,
        "faze": [
            {"nazev": "Paluba flotily", "hp": 185, "utok": 19, "obrana": 13},
            {"nazev": "Nouzový manévr", "hp": 125, "utok": 27, "obrana": 9},
        ],
    },
    "inkvizitor_cerne_peceti": {
        "jmeno": "Inkvizitor Černé pečeti",
        "lokace": "hranice",
        "hp": 165,
        "utok": 22,
        "obrana": 15,
        "zlato": 600,
        "xp": 210,
        "faze": [
            {"nazev": "Černá pečeť", "hp": 165, "utok": 22, "obrana": 15},
            {"nazev": "Rozbitá pečeť", "hp": 110, "utok": 30, "obrana": 10},
        ],
    },
}


def dostupni_bossove(hra):
    """Vrátí bossy dostupné v aktuální lokaci a podle postupu kampaně."""
    porazeni = set(getattr(hra.kampan, "boss_porazeni", []))
    kapitola = getattr(hra.kampan, "kapitola", 0)
    lokace = hra.svet.aktualni_lokace
    dostupni = []
    for boss_id, data in BOSSOVE.items():
        if data["lokace"] != lokace or boss_id in porazeni:
            continue
        if boss_id == "kapitan_zeleznich_flotily" and "strazce_hvezdne_brany" not in porazeni:
            continue
        if boss_id == "inkvizitor_cerne_peceti" and kapitola < 2:
            continue
        dostupni.append((boss_id, data))
    return dostupni

class Nepritel:
    def __init__(self, jmeno, hp, utok, obrana, odmena_zlato, odmena_xp, boss=False, boss_id="", faze=None, faze_index=0):
        self.jmeno = jmeno
        self.hp = hp
        self.max_hp = hp
        self.utok = utok
        self.obrana = obrana
        self.odmena_zlato = odmena_zlato
        self.odmena_xp = odmena_xp
        self.boss = boss
        self.boss_id = boss_id
        self.faze = faze or []
        self.faze_index = faze_index

    def je_nazivu(self):
        return self.hp > 0

class Souboj:
    def __init__(self, hrac, mafie, hra=None):
        self.hrac = hrac
        self.mafie = mafie
        self.hra = hra
        self.nepritel = None

    def generuj_nepritele(self, uroven):
        typy = [
            {"jmeno": "Bandita", "hp": 30 + uroven * 5, "utok": 5 + uroven, "obrana": 2 + uroven // 2, "zlato": 30 + uroven * 10, "xp": 15 + uroven * 5},
            {"jmeno": "Žoldák", "hp": 50 + uroven * 8, "utok": 8 + uroven * 2, "obrana": 5 + uroven, "zlato": 60 + uroven * 15, "xp": 25 + uroven * 8},
            {"jmeno": "Inkvizitor", "hp": 40 + uroven * 6, "utok": 10 + uroven * 2, "obrana": 8 + uroven, "zlato": 80 + uroven * 20, "xp": 35 + uroven * 10},
            {"jmeno": "Konkurenční otrokář", "hp": 70 + uroven * 10, "utok": 12 + uroven * 3, "obrana": 6 + uroven, "zlato": 120 + uroven * 25, "xp": 45 + uroven * 12},
        ]
        data = random.choice(typy)
        obtiznost = self._obtiznost()
        koeficient = profil_obtiznosti(obtiznost)["nepritel"]
        self.nepritel = Nepritel(
            data["jmeno"],
            max(1, int(data["hp"] * koeficient)),
            max(1, int(data["utok"] * koeficient)),
            max(0, int(data["obrana"] * koeficient)),
            uprav_odmenu(data["zlato"], obtiznost),
            uprav_xp(data["xp"], obtiznost),
        )
        return self.nepritel

    def _obtiznost(self):
        nastaveni = getattr(self.hra, "nastaveni", None)
        return getattr(nastaveni, "obtiznost", "normalni")

    def generuj_bosse(self, uroven, boss_id="strazce_hvezdne_brany"):
        """Vytvoří konkrétního příběhového bosse, zpětně kompatibilně s původním voláním."""
        if boss_id not in BOSSOVE:
            raise ValueError("Neznámý boss.")
        data = BOSSOVE[boss_id]
        sila = max(1, uroven)
        obtiznost = self._obtiznost()
        koeficient = profil_obtiznosti(obtiznost)["nepritel"]
        faze = data.get("faze", [])
        prvni = faze[0] if faze else data
        self.nepritel = Nepritel(
            data["jmeno"],
            max(1, int((prvni["hp"] + sila * 18) * koeficient)),
            max(1, int((prvni["utok"] + sila * 2) * koeficient)),
            max(0, int((prvni["obrana"] + sila) * koeficient)),
            uprav_odmenu(data["zlato"] + sila * 35, obtiznost),
            uprav_xp(data["xp"] + sila * 18, obtiznost),
            boss=True,
            boss_id=boss_id,
            faze=faze,
        )
        return self.nepritel

    def dalsi_faze(self):
        """Přepne vícestupňového bosse; vrací False, pokud už byl poslední."""
        if not self.nepritel or not self.nepritel.boss:
            return False
        nepritel = self.nepritel
        if nepritel.faze_index + 1 >= len(nepritel.faze):
            return False
        nepritel.faze_index += 1
        faze = nepritel.faze[nepritel.faze_index]
        koeficient = profil_obtiznosti(self._obtiznost())["nepritel"]
        nepritel.jmeno = f"{BOSSOVE[nepritel.boss_id]['jmeno']} — {faze['nazev']}"
        nepritel.max_hp = max(1, int(faze["hp"] * koeficient))
        nepritel.hp = nepritel.max_hp
        nepritel.utok = max(1, int(faze["utok"] * koeficient))
        nepritel.obrana = max(0, int(faze["obrana"] * koeficient))
        tisk_info(f"Boss vstoupil do další fáze: {faze['nazev']}.")
        return True

    def hracuv_utok(self, bonus=0):
        zaklad = self.hrac.skill_body * 2 + self.hrac.skilly.get("boj", 0) * 3 + self.hrac.skilly.get("strelba", 0) * 2
        for zbran in self.hrac.inventar.zbrane:
            zaklad += zbran.poskozeni
        return zaklad + self.hrac.bojovy_bonus_vybavy() + bonus

    def hracova_obrana(self):
        zaklad = self.hrac.skill_body + self.hrac.skilly.get("obrana", 0) * 2
        zaklad += self.mafie.vojaci // 2
        if self.hra is not None and getattr(self.hra, "pevnost", None):
            zaklad += self.hra.pevnost.bonusy().get("obrana", 0)
        return zaklad

    def proved_boj(self):
        if not self.nepritel or not self.nepritel.je_nazivu():
            self.generuj_nepritele(self.hrac.level)

        nepritel = self.nepritel
        terminalni_obrazek("souboj")
        print(f"\n{NC}⚔️  Boj proti: {nepritel.jmeno} (HP {nepritel.hp}/{nepritel.max_hp})")
        print(f"Tvé HP: {self.hrac.hp}/{self.hrac.max_hp}\n")

        bonus_uteku = 0
        while self.hrac.hp > 0 and nepritel.je_nazivu():
            print(
                "1) Útok  2) Přesný útok  3) Obrana  "
                "4) Temný úder (10 temné energie) 5) Předmět  "
                "6) Zastrašení  7) Útěk"
            )
            try:
                volba = input("> ").strip()
            except EOFError:
                volba = "1"

            obranny_bonus = 0
            preskocit_utok_nepritele = False
            if volba == "7":
                if random.random() < 0.65 + bonus_uteku:
                    tisk_info("Útěk se podařil.")
                    self.nepritel = None
                    return False
                tisk_chyba("Útěk se nepodařil; nepřítel útočí.")
                utok_hrac = 0
            elif volba == "3":
                obranny_bonus = 8 + self.hrac.skilly.get("obrana", 0)
                tisk_info("Zaujal jsi obranný postoj.")
                utok_hrac = 0
            elif volba == "4":
                if self.hrac.dark_energy < 10:
                    tisk_chyba("Nemáš dost temné energie, provede se běžný útok.")
                    utok_hrac = self.hracuv_utok()
                else:
                    self.hrac.dark_energy -= 10
                    utok_hrac = self.hracuv_utok(
                        8 + self.hrac.skilly.get("temnota", 0) * 3
                    )
            elif volba == "2":
                utok_hrac = self.hracuv_utok(5 + self.hrac.skilly.get("strelba", 0) * 2)
                tisk_info("Zamířil jsi na slabé místo.")
            elif volba == "5":
                utok_hrac = 0
                self._bonus_uteku = 0
                self._bonus_obrany = 0
                pouzito = self._pouzij_predmet()
                bonus_uteku = getattr(self, "_bonus_uteku", 0)
                obranny_bonus += getattr(self, "_bonus_obrany", 0)
                if not pouzito:
                    tisk_info("Bez použitého předmětu provedeš běžný útok.")
                    utok_hrac = self.hracuv_utok()
            elif volba == "6":
                sance = min(0.9, 0.25 + self.hrac.dominance / 200 + self.hrac.skilly.get("vyjednavani", 0) / 100)
                if random.random() < sance:
                    preskocit_utok_nepritele = True
                    nepritel.hp -= max(1, nepritel.max_hp // 8)
                    tisk_ok(f"Nepřítel zaváhal. Zastrašení mu ubralo {max(1, nepritel.max_hp // 8)} HP.")
                else:
                    tisk_chyba("Zastrašení selhalo.")
                utok_hrac = 0
            else:
                utok_hrac = self.hracuv_utok()

            obrana_nepr = nepritel.obrana
            if utok_hrac:
                poskozeni = max(1, utok_hrac - obrana_nepr + random.randint(-2, 2))
                nepritel.hp -= poskozeni
                print(f"{GREEN}Tvůj útok: {poskozeni} zranění. {nepritel.jmeno} HP: {max(0, nepritel.hp)}/{nepritel.max_hp}{NC}")

            if not nepritel.je_nazivu():
                if self.dalsi_faze():
                    continue
                break

            if preskocit_utok_nepritele:
                continue
            utok_nepr = nepritel.utok
            obrana_hrac = self.hracova_obrana() + obranny_bonus
            poskozeni = max(1, utok_nepr - obrana_hrac + random.randint(-2, 2))
            poskozeni = max(
                1,
                int(poskozeni * profil_obtiznosti(self._obtiznost())["poskozeni"]),
            )
            self.hrac.hp -= poskozeni
            print(f"{RED}Nepřítel útočí: {poskozeni} zranění. Tvé HP: {max(0, self.hrac.hp)}/{self.hrac.max_hp}{NC}")

            if self.hrac.hp <= 0:
                break

        if self.hrac.hp > 0:
            self.hrac.gold += nepritel.odmena_zlato
            self.hrac.pridej_xp(nepritel.odmena_xp)
            self.hrac.kill_count += 1
            tisk_ok(f"Zvítězil jsi! Odměna: {nepritel.odmena_zlato} zlaťáků, +{nepritel.odmena_xp} XP.")
            if nepritel.boss and self.hra is not None:
                if hasattr(self.hra, "achievementy"):
                    self.hra.achievementy.zaznamenej("boss")
                porazeni = self.hra.kampan.boss_porazeni
                if nepritel.boss_id not in porazeni:
                    porazeni.append(nepritel.boss_id)
                    if nepritel.boss_id == "strazce_hvezdne_brany":
                        self.hra.svet.odhal_lokaci("molo_mesicniho_pristavu")
                        tisk_ok("Strážce padl. Na mapě se objevilo Molo Měsíčního přístavu.")
                    elif nepritel.boss_id == "kapitan_zeleznich_flotily":
                        self.hra.svet.zmen_vztah("tereza", 12)
                        self.hra.hrac.reputace_mesta += 5
                        tisk_ok("Kapitán padl. Tereza uznala tvou pomoc a reputace vzrostla.")
                    elif nepritel.boss_id == "inkvizitor_cerne_peceti":
                        self.hra.hrac.vliv_inkvizice = max(
                            0, self.hra.hrac.vliv_inkvizice - 15
                        )
                        self.hra.hrac.reputace_mesta += 8
                        tisk_ok("Inkvizitor padl. Jeho pečeť oslabila vliv inkvizice.")
            self.nepritel = None
            vysledek = True
        else:
            ztrata = nepritel.odmena_zlato // 2
            self.hrac.gold = max(0, self.hrac.gold - ztrata)
            self.hrac.hp = 1
            tisk_chyba(f"Prohrál jsi! Ztratil jsi {ztrata} zlaťáků a přežíváš s 1 HP.")
            self.nepritel = None
            vysledek = False
        try:
            input("Enter...")
        except EOFError:
            pass
        return vysledek

    def _pouzij_predmet(self):
        dostupne = []
        for predmet_id, data in PREDMETY.items():
            pocet = self.hrac.inventar.pocet_predmetu(predmet_id)
            if pocet and data.get("boj"):
                dostupne.append((predmet_id, data, pocet))
        if not dostupne:
            tisk_chyba("Nemáš žádný bojový předmět.")
            return False
        print("Předměty:")
        for index, (_, data, pocet) in enumerate(dostupne, 1):
            print(f"{index}) {data['nazev']} x{pocet} — {data['popis']}")
        print("0) Zpět")
        try:
            index = int(input("> ")) - 1
        except ValueError:
            tisk_chyba("Zadej číslo.")
            return False
        if index < 0:
            return False
        if index >= len(dostupne):
            tisk_chyba("Špatná volba.")
            return False
        predmet_id, data, _ = dostupne[index]
        if not self.hrac.inventar.odeber_predmet(predmet_id):
            tisk_chyba("Předmět už není v inventáři.")
            return False
        if data["boj"] == "leceni":
            self.hrac.hp = min(self.hrac.max_hp, self.hrac.hp + data["hodnota"])
            tisk_ok(f"Použil jsi {data['nazev']}. HP: {self.hrac.hp}.")
        elif data["boj"] == "temnota":
            self.hrac.dark_energy = min(100, self.hrac.dark_energy + data["hodnota"])
            tisk_ok(f"Použil jsi {data['nazev']}. Temná energie: {self.hrac.dark_energy}.")
        elif data["boj"] == "utek":
            bonus_uteku = 0.2
            self._bonus_uteku = bonus_uteku
            tisk_ok("Dýmovnice naplnila bojiště kouřem.")
        elif data["boj"] == "obrana":
            self._bonus_obrany = data["hodnota"]
            tisk_ok("Opravárenská sada zpevňuje vybavení.")
        return True
