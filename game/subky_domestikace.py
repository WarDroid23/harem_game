# game/subky_domestikace.py
import random
from models.otrokyne import Otrokyně
from models.hrac import Hrac
from utils.vypis import clear, tisk_ok, tisk_chyba

class SubkyDomestikace:
    def __init__(self):
        pass

    def trenink_poslusnosti(self, otrok: Otrokyně, hrac: Hrac):
        if hrac.sex_energy < 10:
            tisk_chyba("Nedostatek energie.")
            return
        hrac.sex_energy -= 10

        otrok.poslusnost = min(100, otrok.poslusnost + random.randint(3, 8))
        otrok.submisivita = min(100, otrok.submisivita + random.randint(2, 5))
        otrok.duvera = max(0, otrok.duvera - random.randint(1, 3))
        otrok.strach = min(100, otrok.strach + random.randint(1, 4))
        otrok.aktualizuj_fazi()
        tisk_ok(f"Trénink poslušnosti: {otrok.jmeno} poslušnost {otrok.poslusnost}, submisivita {otrok.submisivita}.")

    def podminovani(self, otrok: Otrokyně, hrac: Hrac):
        if hrac.dark_energy < 5:
            tisk_chyba("Nedostatek temné energie.")
            return
        hrac.dark_energy -= 5

        otrok.broken = min(100, otrok.broken + random.randint(2, 6))
        otrok.mindbreak = min(100, otrok.mindbreak + random.randint(1, 4))
        otrok.duvera = max(0, otrok.duvera - random.randint(3, 6))
        otrok.strach = min(100, otrok.strach + random.randint(2, 5))
        otrok.aktualizuj_fazi()
        tisk_ok(f"Podminování: {otrok.jmeno} broken {otrok.broken}, mindbreak {otrok.mindbreak}.")

    def domestikace(self, otrok: Otrokyně, hrac: Hrac):
        if otrok.broken < 70 or otrok.mindbreak < 50:
            tisk_chyba("Otrokyně ještě není dostatečně zlomená.")
            return

        otrok.loajalita = min(100, otrok.loajalita + 20)
        otrok.submisivita = min(100, otrok.submisivita + 15)
        otrok.duvera = 0
        otrok.owned_mark = True
        otrok.aktualizuj_fazi()
        tisk_ok(f"{otrok.jmeno} byla domestikována. Loajalita: {otrok.loajalita}, submisivita: {otrok.submisivita}.")

    def dehumanizace(self, otrok: Otrokyně, hrac: Hrac):
        if otrok.broken < 90 or otrok.mindbreak < 80:
            tisk_chyba("Otrokyně není připravena na dehumanizaci.")
            return

        otrok.mindbreak = 100
        otrok.broken = 100
        otrok.loajalita = 100
        otrok.submisivita = 100
        otrok.duvera = 0
        otrok.nalada = "zlomená"
        otrok.aktualizuj_fazi()
        tisk_ok(f"{otrok.jmeno} byla plně dehumanizována.")

    def zobraz_moznosti(self, otrok, hrac):
        clear()
        print(f"--- Subky / Domestikace: {otrok.jmeno} ---")
        print(f"Poslušnost: {otrok.poslusnost} | Submisivita: {otrok.submisivita}")
        print(f"Broken: {otrok.broken} | Mindbreak: {otrok.mindbreak} | Loajalita: {otrok.loajalita}")
        print(f"Energie: {hrac.sex_energy} | Temná energie: {hrac.dark_energy}")
        print()
        print("1) Trénink poslušnosti (10 energie)")
        print("2) Podminování (5 temné energie)")
        print("3) Domestikace (vyžaduje broken 70, mindbreak 50)")
        print("4) Dehumanizace (vyžaduje broken 90, mindbreak 80)")
        print("0) Zpět")
        volba = input("> ")
        if volba == "1":
            self.trenink_poslusnosti(otrok, hrac)
        elif volba == "2":
            self.podminovani(otrok, hrac)
        elif volba == "3":
            self.domestikace(otrok, hrac)
        elif volba == "4":
            self.dehumanizace(otrok, hrac)
