#!/usr/bin/env python3
# main.py
import random
from config import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GOLD, BOLD, NC
from game.save_load import Hra, uloz_hru, nacti_hru
from game.interakce import zobraz_interakce, zobraz_hromadne_interakce
from game.ekonomika import najem_otrokyně
from game.mafie import spravovat_mafii
from game.vyvoj import zobraz_vyvoj
from game.diplomacie import Diplomacie
from game.vyzkum import VyzkumSystem, VYZKUM
from game.subky_domestikace import SubkyDomestikace
from game.lov import lov_otrokyn
from game.odpocinek import odpocinek
from game.energie import zobraz_menu as menu_energie
from game.obchod import obchod
from game.questy import QuestSystem
from game.drazba import drazba_otrokyn
from game.budovy import spravovat_budovy
from game.udalosti import spust_nahodnou_udalost
from game.statistiky import zobraz_statistiky
from game.souboje import Souboj
from game.alchymie import AlchymieSystem
from game.crafting import CraftingSystem
from game.harem_interakce import menu_haremu
from utils.vypis import (
    clear, ascii_art, terminalni_obrazek, tisk_ok, tisk_chyba, tisk_info,
    ukazatel,
)
from data.jmena import JMENA
from data.charaktery import CHARAKTERY
from data.degradace import Faze
from models.otrokyne import Otrokyně

def hlavni_menu(hra: Hra):
    diplo = Diplomacie(hra.frakce)
    vyzkum = hra.vyzkum
    subky = SubkyDomestikace()
    souboj = Souboj(hra.hrac, hra.mafie)
    crafting = CraftingSystem()

    while True:
        clear()
        ascii_art()
        terminalni_obrazek("menu")
        print(f"{GOLD}{BOLD}Den: {hra.hrac.den} | {GREEN}Zlato: {hra.hrac.gold} 🪙{NC}")
        print(
            f"{CYAN}Energie {ukazatel(hra.hrac.sex_energy, 100)} | "
            f"Temná energie {ukazatel(hra.hrac.dark_energy, 100)}{NC}"
        )
        print(f"{RED}Reputace: {hra.hrac.reputace_mesta} | {BLUE}Vliv inkvizice: {hra.hrac.vliv_inkvizice}{NC}")
        kapitola = hra.kampan.aktualni()
        kapitola_text = kapitola["nazev"] if kapitola else "Kampaň dokončena"
        print(f"{YELLOW}Harém: {hra.harem.pocet()} | {MAGENTA}Území: {len(hra.mafie.uzemi)} 🏰{NC}")
        print(f"{CYAN}Místo: {hra.svet.aktualni_lokace} | Kampaň: {kapitola_text}{NC}")
        print("\n")
        print(f"{GREEN}1) 👉 Interakce s otrokyněmi")
        print(f"{CYAN}2) 💰 Nájem otrokyně")
        print(f"{MAGENTA}3) 🏢 Mafie / impérium")
        print(f"{YELLOW}4) 📈 Vývoj postavy")
        print(f"{BLUE}5) 🤝 Diplomacie")
        print(f"{GOLD}6) 🔬 Výzkum")
        print(f"{RED}7) 🧠 Subky / Domestikace")
        print(f"{CYAN}8) 🗺️ Mapa a lokace")
        print(f"{GOLD}9) 📖 Příběhová kampaň")
        print(f"{MAGENTA}10) ➕ Přidat otrokyni (test)")
        print(f"{YELLOW}11) 🎯 Lov otrokyň")
        print(f"{BLUE}12) 🛌 Odpočinek")
        print(f"{GOLD}13) 🛒 Obchod")
        print(f"{RED}14) 🎲 Questy")
        print(f"{GREEN}15) 🏛️ Dražba otrokyň")
        print(f"{CYAN}16) 🏗️ Budovy / Harém")
        print(f"{MAGENTA}17) 📊 Statistiky")
        print(f"{YELLOW}18) ⚔️ Souboj")
        print(f"{BLUE}19) 🧪 Alchymie")
        print(f"{CYAN}20) 📋 Rychlý přehled")
        print(f"{GREEN}23) 🤝 Harem: péče, role a osudy")
        print(f"{YELLOW}24) 🛠️ Předměty a crafting")
        print(f"{CYAN}25) ⚡ Dobít energie")
        print(f"{GREEN}21) 💾 Uložit hru")
        print(f"{CYAN}22) 📂 Načíst hru")
        print(f"{RED}0) 🚪 Konec")
        try:
            volba = input("> ").strip().lower()
        except EOFError:
            uloz_hru(hra)
            return

        # Klávesové zkratky usnadňují návrat do menu i práci v terminálu.
        volba = {"s": "21", "l": "22", "q": "0"}.get(volba, volba)

        if volba == "1":
            aktivni = hra.harem.vsechny_aktivni()
            if aktivni:
                print("\nVyber otrokyni:")
                for i, o in enumerate(aktivni, 1):
                    faze_nazev = Faze[o.faze_zkazenosti]["nazev"]
                    char_nazev = CHARAKTERY[o.charakter]["nazev"]
                    print(
                        f"{i}) {o.jmeno} [{char_nazev}, {faze_nazev}, věk {o.vek}] "
                        f"(loajalita:{o.loajalita}% | osud: {o.popis_osudu()})"
                    )
                print("@) Vybrat všechny aktivní otrokyně")
                try:
                    volba_otrokyn = input("> ").strip()
                    if volba_otrokyn == "@":
                        zobraz_hromadne_interakce(aktivni, hra.hrac)
                        continue
                    idx = int(volba_otrokyn) - 1
                    if 0 <= idx < len(aktivni):
                        zobraz_interakce(aktivni[idx], hra.hrac)
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
                input("Enter...")
            else:
                tisk_chyba("Nemáš žádné otrokyně.")
                input("Enter...")

        elif volba == "2":
            aktivni = hra.harem.vsechny_aktivni()
            if aktivni:
                volne = [o for o in aktivni if not o.na_najmu]
                if volne:
                    print("\nVyber otrokyni k pronájmu:")
                    for i, o in enumerate(volne, 1):
                        print(f"{i}) {o.jmeno}")
                    try:
                        idx = int(input("> ")) - 1
                        if 0 <= idx < len(volne):
                            najem_otrokyně(hra.hrac, volne[idx])
                        else:
                            tisk_chyba("Špatná volba.")
                    except ValueError:
                        tisk_chyba("Zadej číslo.")
                else:
                    tisk_chyba("Všechny otrokyně jsou na najmu.")
                input("Enter...")
            else:
                tisk_chyba("Nemáš otrokyně.")
                input("Enter...")

        elif volba == "3":
            spravovat_mafii(hra.hrac, hra.mafie)

        elif volba == "4":
            zobraz_vyvoj(hra.hrac)

        elif volba == "5":
            diplo.zobraz_frakce()
            cil = input("Frakce: ").strip().lower()
            akce = input("Akce (uplatek/spojenectvi/hrozba/obchod): ").strip().lower()
            if akce == "obchod":
                diplo.obchodovat(hra.hrac, cil)
            else:
                diplo.vyjednavat(hra.hrac, cil, akce)
            input("Enter...")

        elif volba == "6":
            vyzkum.zobraz_vyzkum(hra.hrac)
            id_vyzkumu = input("Zadej id výzkumu: ").strip().lower()
            if id_vyzkumu in VYZKUM:
                vyzkum.vyzkoumat(hra.hrac, id_vyzkumu)
            else:
                tisk_chyba("Neznámý výzkum.")
            input("Enter...")

        elif volba == "7":
            aktivni = hra.harem.vsechny_aktivni()
            if aktivni:
                print("\nVyber otrokyni:")
                for i, o in enumerate(aktivni, 1):
                    print(f"{i}) {o.jmeno} (broken:{o.broken} mindbreak:{o.mindbreak})")
                try:
                    idx = int(input("> ")) - 1
                    if 0 <= idx < len(aktivni):
                        subky.zobraz_moznosti(aktivni[idx], hra.hrac)
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
            else:
                tisk_chyba("Nemáš otrokyně.")
                input("Enter...")

        elif volba == "8":
            hra.svet.menu(hra)
            hra.kampan.zkontroluj_postup(hra)

        elif volba == "9":
            hra.kampan.menu(hra)

        elif volba == "21":
            uloz_hru(hra)
            input("Enter...")

        elif volba == "22":
            nova_hra = nacti_hru()
            if nova_hra:
                hra = nova_hra
                diplo = Diplomacie(hra.frakce)
                vyzkum = hra.vyzkum
                subky = SubkyDomestikace()
                souboj = Souboj(hra.hrac, hra.mafie)
                crafting = CraftingSystem()
                tisk_ok("Hra načtena.")
            else:
                tisk_chyba("Nepodařilo se načíst hru.")
            input("Enter...")

        elif volba == "10":
            jmeno = random.choice(JMENA)
            otrok = Otrokyně(jmeno)
            hra.harem.pridat(otrok)
            tisk_ok(f"Přidána otrokyně {jmeno}.")
            input("Enter...")

        elif volba == "11":
            otrok = lov_otrokyn(hra)
            if otrok:
                hra.harem.pridat(otrok)
                tisk_ok(f"Otrokyně {otrok.jmeno} přidána do harému!")
            input("Enter...")

        elif volba == "12":
            odpocinek(hra)
            spust_nahodnou_udalost(hra)

        elif volba == "13":
            obchod(hra)

        elif volba == "14":
            questy = hra.questy
            volba_q = questy.zobraz_questy()
            if volba_q == "1":
                questy.generuj_quest(hra.hrac, hra)
            elif volba_q == "2":
                questy.proved_quest(hra.hrac, hra.harem, hra.mafie, hra)
            input("Enter...")

        elif volba == "15":
            drazba_otrokyn(hra.hrac, hra.harem)

        elif volba == "16":
            spravovat_budovy(hra.hrac, hra.harem)

        elif volba == "17":
            zobraz_statistiky(hra)

        elif volba == "18":
            souboj.generuj_nepritele(hra.hrac.level)
            souboj.proved_boj()

        elif volba == "19":
            hra.alchymie.zobraz_menu(hra.hrac, hra.harem)

        elif volba == "23":
            menu_haremu(hra)

        elif volba == "24":
            crafting.menu(hra)

        elif volba == "25":
            menu_energie(hra)

        elif volba == "0":
            uloz_hru(hra)
            print("Hra uložena. Konec hry.")
            return

        elif volba == "20":
            clear()
            print(f"{GOLD}--- Rychlý přehled dne {hra.hrac.den} ---{NC}\n")
            print(
                f"HP {hra.hrac.hp}/{hra.hrac.max_hp} | "
                f"Energie {hra.hrac.sex_energy}/100 | "
                f"Temno {hra.hrac.dark_energy}/100"
            )
            print(
                f"Místo: {hra.svet.aktualni_lokace} | "
                f"Kampaň: {hra.kampan.kapitola + 1 if hra.kampan.aktualni() else 'hotová'}"
            )
            najmy = [
                f"{o.jmeno} ({o.najem_zbyva_dni} dní)"
                for o in hra.harem.vsechny_aktivni() if o.na_najmu
            ]
            print("Aktivní nájmy: " + (", ".join(najmy) if najmy else "žádné"))
            if hra.questy.aktivni_quest:
                print(
                    f"Quest: {hra.questy.aktivni_quest['nazev']} "
                    f"({hra.questy.dny_zbyva} dní)"
                )
            else:
                print("Quest: žádný aktivní")
            try:
                input("\nEnter...")
            except EOFError:
                pass

        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")

if __name__ == "__main__":
    hra = Hra()
    nactena = nacti_hru()
    if nactena:
        hra = nactena
        print("Načtena uložená hra.")
    else:
        for _ in range(2):
            jmeno = random.choice(JMENA)
            hra.harem.pridat(Otrokyně(jmeno))
        print("Nová hra vytvořena.")
    hlavni_menu(hra)
