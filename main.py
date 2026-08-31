#!/usr/bin/env python3
# main.py
import random
from config import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GOLD, BOLD, WHITE, NC
from game.save_load import (
    Hra, uloz_hru, uloz_slot, nacti_slot, seznam_slotu,
)
from game.trailer import prehraj_trailer, menu_trailer
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
from game.souboje import Souboj, dostupni_bossove
from game.alchymie import AlchymieSystem
from game.crafting import CraftingSystem
from game.harem_interakce import menu_haremu
from game.settings import NastaveniHry, aplikuj_nastaveni
from game.automaticky_tah import obsluz_automaticky_tah
from game.manzelstvi import menu_manzelstvi
from utils.vypis import (
    clear, ascii_art, terminalni_obrazek, tisk_ok, tisk_chyba, tisk_info,
    ukazatel,
)
from data.jmena import JMENA
from data.charaktery import CHARAKTERY
from data.degradace import Faze
from models.otrokyne import Otrokyně


def _vykresli_sloty(hlavni_soubor=None):
    for slot in seznam_slotu(hlavni_soubor) if hlavni_soubor else seznam_slotu():
        if not slot["existuje"]:
            print(f"{slot['slot']}) {slot['nazev']} — prázdný")
            continue
        meta = slot.get("meta") or {}
        den = meta.get("den", "?")
        zlato = meta.get("zlato", "?")
        harem = meta.get("pocet_haremu", "?")
        kdy = meta.get("ulozene", "?")
        oblib = meta.get("oblibenkyně")
        oblib_txt = f" | ★ {oblib}" if oblib else ""
        print(
            f"{slot['slot']}) {slot['nazev']} — den {den}, zlato {zlato}, "
            f"harém {harem}{oblib_txt}"
        )
        print(f"    uloženo: {kdy} (JSON)")


def menu_ulozeni(hra):
    clear()
    print("--- Uložení hry (JSON) ---\n")
    _vykresli_sloty()
    print("0) Zpět")
    try:
        volba = input("> ").strip()
        if volba == "0":
            return False
        slot = int(volba)
        uspech = uloz_slot(hra, slot)
        if uspech:
            tisk_ok(f"Hra byla uložena do JSON slotu {slot}.")
        return uspech
    except (ValueError, EOFError):
        tisk_chyba("Zadej číslo slotu 1 až 5.")
        return False


def menu_nacteni():
    clear()
    print("--- Načtení hry (JSON) ---\n")
    _vykresli_sloty()
    print("0) Zpět")
    try:
        volba = input("> ").strip()
        if volba == "0":
            return None
        slot = int(volba)
        hra = nacti_slot(slot)
        if hra:
            tisk_ok(f"Načten JSON slot {slot}.")
        return hra
    except (ValueError, EOFError):
        tisk_chyba("Zadej číslo slotu 1 až 5.")
        return None


def menu_nastaveni(hra):
    from config import THEMES, apply_theme
    while True:
        clear()
        nastaveni = hra.nastaveni
        terminalni_obrazek("nastaveni")
        print("--- Nastavení hry ---\n")
        print(f"1) Barvy terminálu: {'zapnuté' if nastaveni.barvy else 'vypnuté'}")
        print(f"2) Obtížnost: {nastaveni.obtiznost_text}")
        print(f"3) Barevné téma: {getattr(nastaveni, 'tema_text', 'Temné dominium')}")
        print("0) Zpět")
        try:
            volba = input("> ").strip().lower()
        except EOFError:
            return
        if volba == "0":
            return
        if volba == "1":
            nastaveni.barvy = not nastaveni.barvy
            aplikuj_nastaveni(nastaveni)
            tisk_ok("Nastavení barev změněno.")
            input("Enter...")
        elif volba == "2":
            print("\n1) Lehká  2) Normální  3) Těžká")
            vyber = input("> ").strip()
            mapa = {"1": "lehka", "2": "normalni", "3": "tezka"}
            if vyber in mapa:
                nastaveni.obtiznost = mapa[vyber]
                aplikuj_nastaveni(nastaveni)
                tisk_ok(f"Obtížnost nastavena na {nastaveni.obtiznost_text}.")
            else:
                tisk_chyba("Neplatná obtížnost.")
            input("Enter...")
        elif volba == "3":
            print("\n--- Barevná témata ---\n")
            seznam = list(THEMES.items())
            for i, (tid, info) in enumerate(seznam, 1):
                aktivni = " ← aktivní" if tid == getattr(nastaveni, "tema", "") else ""
                print(f"{i}) {info['nazev']}{aktivni}")
                print(f"   {info['popis']}")
            print("0) Zpět")
            vyber = input("> ").strip()
            if vyber == "0":
                continue
            try:
                idx = int(vyber) - 1
                if 0 <= idx < len(seznam):
                    tid = seznam[idx][0]
                    nastaveni.tema = tid
                    nastaveni.barvy = True
                    aplikuj_nastaveni(nastaveni)
                    nazev = apply_theme(tid)
                    tisk_ok(f"Téma nastaveno: {nazev}")
                    terminalni_obrazek("menu")
                else:
                    tisk_chyba("Špatná volba.")
            except ValueError:
                tisk_chyba("Zadej číslo.")
            input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")


def menu_meta_hlavni(hra):
    while True:
        clear()
        terminalni_obrazek("nastaveni")
        print(f"{GOLD}{BOLD}--- Hlavní menu ---{NC}\n")
        print(f"{GREEN}1) 💾 Uložit hru")
        print(f"{CYAN}2) 📂 Načíst hru")
        print(f"{WHITE}3) ⚙️ Nastavení hry")
        print(f"{YELLOW}4) 🏠 Zpět do hry")
        print(f"{RED}0) 🚪 Ukončit hru (s uložením)")
        try:
            volba = input("> ").strip().lower()
        except EOFError:
            uloz_hru(hra)
            return "quit"
        if volba in ("1", "s"):
            menu_ulozeni(hra)
            input("Enter...")
        elif volba in ("2", "l"):
            nova = menu_nacteni()
            if nova:
                tisk_ok("Hra načtena.")
                input("Enter...")
                return nova
            input("Enter...")
        elif volba == "3":
            menu_nastaveni(hra)
        elif volba in ("4", ""):
            return None
        elif volba in ("0", "q"):
            uloz_hru(hra)
            print("Hra uložena. Konec hry.")
            return "quit"
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")


def hlavni_menu(hra: Hra):
    diplo = Diplomacie(hra.frakce)
    vyzkum = hra.vyzkum
    subky = SubkyDomestikace()
    souboj = Souboj(hra.hrac, hra.mafie, hra)
    crafting = CraftingSystem()

    while True:
        clear()
        ascii_art()
        terminalni_obrazek("menu")
        print(f"{GOLD}{BOLD}Den: {hra.hrac.den} | {GREEN}Zlato: {hra.hrac.gold} 🪙{NC}")
        max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
        max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
        print(
            f"{CYAN}Energie {ukazatel(hra.hrac.sex_energy, max_s)} | "
            f"Temná energie {ukazatel(hra.hrac.dark_energy, max_t)}{NC}"
        )
        print(f"{RED}Reputace: {hra.hrac.reputace_mesta} | {BLUE}Vliv inkvizice: {hra.hrac.vliv_inkvizice}{NC}")
        kapitola = hra.kampan.aktualni()
        kapitola_text = kapitola["nazev"] if kapitola else "Kampaň dokončena"
        aktivni_harem = hra.harem.vsechny_aktivni()
        pocet_partnerek = sum(1 for o in aktivni_harem if getattr(o, "partnerka", False))
        oblibena = next((o for o in aktivni_harem if getattr(o, "oblibena", False)), None)
        oblib_txt = f" | ★ {oblibena.jmeno}" if oblibena else ""
        print(
            f"{YELLOW}Harém: {hra.harem.pocet()} "
            f"(partnerky: {pocet_partnerek}{oblib_txt}) | "
            f"{MAGENTA}Území: {len(hra.mafie.uzemi)} 🏰{NC}"
        )
        print(
            f"{CYAN}Místo: {hra.svet.aktualni_lokace} | "
            f"Kampaň: {kapitola_text} | Obtížnost: {hra.nastaveni.obtiznost_text}{NC}"
        )
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
        print(f"{GREEN}23) 🤝 Harem: péče, odměny, oblíbenkyně a osudy")
        print(f"{YELLOW}24) 🛠️ Předměty a crafting")
        print(f"{CYAN}25) ⚡ Dobít energie")
        print(f"{MAGENTA}28) 💍 Manželství a rodina")
        print(f"{GREEN}A) 🤖 Automatický bezpečný tah")
        print(f"{YELLOW}26) 🏠 Hlavní menu (uložit / načíst / nastavení)")
        print(f"{RED}0) 🚪 Konec")
        try:
            volba = input("> ").strip().lower()
        except EOFError:
            uloz_hru(hra)
            return

        volba = {"s": "26", "l": "26", "q": "0", "a": "auto", "m": "26"}.get(volba, volba)

        if volba == "auto":
            obsluz_automaticky_tah(hra)
            try:
                input("Enter...")
            except EOFError:
                pass
        elif volba == "1":
            aktivni = hra.harem.vsechny_aktivni()
            if aktivni:
                print("\nVyber otrokyni:")
                for i, o in enumerate(aktivni, 1):
                    faze_nazev = Faze[o.faze_zkazenosti]["nazev"]
                    char_nazev = CHARAKTERY[o.charakter]["nazev"]
                    hvezda = "★ " if getattr(o, "oblibena", False) else ""
                    print(
                        f"{i}) {hvezda}{o.jmeno} [{char_nazev}, {faze_nazev}, věk {o.vek}] "
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
                            najem_otrokyně(hra.hrac, volne[idx], hra.nastaveni.obtiznost)
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
            try:
                spravovat_mafii(hra)
            except Exception as e:
                tisk_chyba(f"Mafie selhala: {e}")
                try:
                    input("Enter...")
                except EOFError:
                    pass
        elif volba == "4":
            zobraz_vyvoj(hra.hrac)
        elif volba == "5":
            try:
                diplo.menu(hra)
            except Exception as e:
                tisk_chyba(f"Diplomacie selhala: {e}")
                try:
                    input("Enter...")
                except EOFError:
                    pass
        elif volba == "6":
            try:
                vyzkum.menu(hra)
            except Exception as e:
                tisk_chyba(f"Výzkum selhal: {e}")
                try:
                    input("Enter...")
                except EOFError:
                    pass
        elif volba == "7":
            aktivni = hra.harem.vsechny_aktivni()
            if aktivni:
                subky.menu(hra, aktivni)
            else:
                tisk_chyba("Nemáš otrokyně pro domestikaci.")
                input("Enter...")
        elif volba == "8":
            hra.svet.menu(hra)
        elif volba == "9":
            hra.kampan.menu(hra)
        elif volba == "10":
            jmeno = random.choice(JMENA)
            otrok = Otrokyně(jmeno=jmeno)
            hra.harem.pridat(otrok)
            tisk_ok(f"Přidána testovací otrokyně: {jmeno}")
            input("Enter...")
        elif volba == "11":
            otrok = lov_otrokyn(hra)
            if otrok:
                hra.harem.pridat(otrok)
            input("Enter...")
        elif volba == "12":
            odpocinek(hra)
            input("Enter...")
        elif volba == "13":
            obchod(hra)
        elif volba == "14":
            QuestSystem().menu(hra)
        elif volba == "15":
            drazba_otrokyn(hra.hrac, hra.harem)
            input("Enter...")
        elif volba == "16":
            spravovat_budovy(hra.hrac, hra.harem)
        elif volba == "17":
            zobraz_statistiky(hra)
            input("Enter...")
        elif volba == "18":
            souboj.menu()
        elif volba == "19":
            hra.alchymie.zobraz_menu(hra.hrac, hra.harem)
        elif volba == "23":
            menu_haremu(hra)
        elif volba == "24":
            crafting.menu(hra)
        elif volba == "25":
            menu_energie(hra)
        elif volba == "28":
            menu_manzelstvi(hra)
        elif volba == "26":
            vysledek = menu_meta_hlavni(hra)
            if vysledek == "quit":
                return
            if vysledek is not None:
                hra = vysledek
                diplo = Diplomacie(hra.frakce)
                vyzkum = hra.vyzkum
                subky = SubkyDomestikace()
                souboj = Souboj(hra.hrac, hra.mafie, hra)
                crafting = CraftingSystem()
        elif volba == "0":
            uloz_hru(hra)
            print("Hra uložena. Konec hry.")
            return
        elif volba == "20":
            clear()
            print(f"{GOLD}--- Rychlý přehled dne {hra.hrac.den} ---{NC}\n")
            max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
            max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
            print(
                f"HP {hra.hrac.hp}/{hra.hrac.max_hp} | "
                f"Energie {hra.hrac.sex_energy}/{max_s} | "
                f"Temno {hra.hrac.dark_energy}/{max_t}"
            )
            print(
                f"Místo: {hra.svet.aktualni_lokace} | "
                f"Kampaň: {hra.kampan.kapitola + 1 if hra.kampan.aktualni() else 'hotová'}"
            )
            najmy = [
                f"{o.jmeno} ({o.najem_zbyva_dni} dní)"
                for o in hra.harem.vsechny_aktivni() if o.na_najmu
            ]
            if najmy:
                print("Na najmu: " + ", ".join(najmy))
            oblib = next((o for o in hra.harem.vsechny_aktivni() if getattr(o, "oblibena", False)), None)
            if oblib:
                print(f"★ Oblíbenkyně: {oblib.jmeno}")
            input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            try:
                input("Enter...")
            except EOFError:
                pass


def start():
    while True:
        clear()
        ascii_art()
        print(f"{GOLD}{BOLD}HAREM DARK – Dark Expansion{NC}\n")
        print(f"{GREEN}1) Nová hra")
        print(f"{CYAN}2) Načíst hru")
        print(f"{WHITE}3) Nastavení")
        print(f"{MAGENTA}4) 🎬 Trailer")
        print(f"{RED}0) Konec")
        try:
            volba = input("> ").strip()
        except EOFError:
            return
        if volba == "1":
            try:
                prehraj_trailer(rychle=True, interaktivni=True)
            except Exception:
                pass
            hra = Hra()
            hlavni_menu(hra)
        elif volba == "2":
            hra = menu_nacteni()
            if hra:
                hlavni_menu(hra)
        elif volba == "3":
            h = Hra()
            menu_nastaveni(h)
        elif volba == "4":
            menu_trailer()
        else:
            print("Konec.")
            return


if __name__ == "__main__":
    start()
