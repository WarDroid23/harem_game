# game/souboje.py
import random
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, GREEN, RED, CYAN, NC

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

    def hracuv_utok(self):
        zaklad = self.hrac.skill_body * 2 + self.hrac.skilly.get("boj", 0) * 3 + self.hrac.skilly.get("strelba", 0) * 2
        for zbran in self.hrac.inventar.zbrane:
            zaklad += zbran.poskozeni
        return zaklad

    def hracova_obrana(self):
        zaklad = self.hrac.skill_body + self.hrac.skilly.get("obrana", 0) * 2
        zaklad += self.mafie.vojaci // 2
        return zaklad

    def proved_boj(self):
        if not self.nepritel:
            self.generuj_nepritele(self.hrac.level)

        nepritel = self.nepritel
        print(f"\n{NC}⚔️  Boj proti: {nepritel.jmeno} (HP {nepritel.hp}/{nepritel.max_hp})")
        print(f"Tvé HP: {self.hrac.hp}/{self.hrac.max_hp}\n")

        while self.hrac.hp > 0 and nepritel.je_nazivu():
            utok_hrac = self.hracuv_utok()
            obrana_nepr = nepritel.obrana
            poskozeni = max(1, utok_hrac - obrana_nepr + random.randint(-2, 2))
            nepritel.hp -= poskozeni
            print(f"{GREEN}Tvůj útok: {poskozeni} zranění. {nepritel.jmeno} HP: {max(0, nepritel.hp)}/{nepritel.max_hp}{NC}")

            if not nepritel.je_nazivu():
                break

            utok_nepr = nepritel.utok
            obrana_hrac = self.hracova_obrana()
            poskozeni = max(1, utok_nepr - obrana_hrac + random.randint(-2, 2))
            self.hrac.hp -= poskozeni
            print(f"{RED}Nepřítel útočí: {poskozeni} zranění. Tvé HP: {max(0, self.hrac.hp)}/{self.hrac.max_hp}{NC}")

            if self.hrac.hp <= 0:
                break

        if self.hrac.hp > 0:
            self.hrac.gold += nepritel.odmena_zlato
            self.hrac.pridej_xp(nepritel.odmena_xp)
            tisk_ok(f"Zvítězil jsi! Odměna: {nepritel.odmena_zlato} zlaťáků, +{nepritel.odmena_xp} XP.")
        else:
            ztrata = nepritel.odmena_zlato // 2
            self.hrac.gold = max(0, self.hrac.gold - ztrata)
            self.hrac.hp = 1
            tisk_chyba(f"Prohrál jsi! Ztratil jsi {ztrata} zlaťáků a přežíváš s 1 HP.")
        input("Enter...")
