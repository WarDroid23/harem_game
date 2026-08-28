# game/souboje.py
import random
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, GREEN, RED, CYAN, NC
from game.predmety import PREDMETY

class Nepritel:
    def __init__(self, jmeno, hp, utok, obrana, odmena_zlato, odmena_xp):
        self.jmeno = jmeno
        self.hp = hp
        self.max_hp = hp
        self.utok = utok
        self.obrana = obrana
        self.odmena_zlato = odmena_zlato
        self.odmena_xp = odmena_xp

    def je_nazivu(self):
        return self.hp > 0

class Souboj:
    def __init__(self, hrac, mafie):
        self.hrac = hrac
        self.mafie = mafie
        self.nepritel = None

    def generuj_nepritele(self, uroven):
        typy = [
            {"jmeno": "Bandita", "hp": 30 + uroven * 5, "utok": 5 + uroven, "obrana": 2 + uroven // 2, "zlato": 30 + uroven * 10, "xp": 15 + uroven * 5},
            {"jmeno": "Žoldák", "hp": 50 + uroven * 8, "utok": 8 + uroven * 2, "obrana": 5 + uroven, "zlato": 60 + uroven * 15, "xp": 25 + uroven * 8},
            {"jmeno": "Inkvizitor", "hp": 40 + uroven * 6, "utok": 10 + uroven * 2, "obrana": 8 + uroven, "zlato": 80 + uroven * 20, "xp": 35 + uroven * 10},
            {"jmeno": "Konkurenční otrokář", "hp": 70 + uroven * 10, "utok": 12 + uroven * 3, "obrana": 6 + uroven, "zlato": 120 + uroven * 25, "xp": 45 + uroven * 12},
        ]
        data = random.choice(typy)
        self.nepritel = Nepritel(data["jmeno"], data["hp"], data["utok"], data["obrana"], data["zlato"], data["xp"])
        return self.nepritel

    def hracuv_utok(self, bonus=0):
        zaklad = self.hrac.skill_body * 2 + self.hrac.skilly.get("boj", 0) * 3 + self.hrac.skilly.get("strelba", 0) * 2
        for zbran in self.hrac.inventar.zbrane:
            zaklad += zbran.poskozeni
        return zaklad + bonus

    def hracova_obrana(self):
        zaklad = self.hrac.skill_body + self.hrac.skilly.get("obrana", 0) * 2
        zaklad += self.mafie.vojaci // 2
        return zaklad

    def proved_boj(self):
        if not self.nepritel or not self.nepritel.je_nazivu():
            self.generuj_nepritele(self.hrac.level)

        nepritel = self.nepritel
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
                break

            if preskocit_utok_nepritele:
                continue
            utok_nepr = nepritel.utok
            obrana_hrac = self.hracova_obrana() + obranny_bonus
            poskozeni = max(1, utok_nepr - obrana_hrac + random.randint(-2, 2))
            self.hrac.hp -= poskozeni
            print(f"{RED}Nepřítel útočí: {poskozeni} zranění. Tvé HP: {max(0, self.hrac.hp)}/{self.hrac.max_hp}{NC}")

            if self.hrac.hp <= 0:
                break

        if self.hrac.hp > 0:
            self.hrac.gold += nepritel.odmena_zlato
            self.hrac.pridej_xp(nepritel.odmena_xp)
            self.hrac.kill_count += 1
            tisk_ok(f"Zvítězil jsi! Odměna: {nepritel.odmena_zlato} zlaťáků, +{nepritel.odmena_xp} XP.")
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
