# game/tresty_odmeny.py
import random
from data.tresty import TRESTY
from data.odmeny import ODMENY
from data.charaktery import CHARAKTERY
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GREEN, RED, CYAN, MAGENTA, GOLD, NC

def proved_trest(otrok, hrac, id_trestu):
    if id_trestu not in TRESTY:
        tisk_chyba("Neplatný trest.")
        return

    trest = TRESTY[id_trestu]

    if hrac.dark_energy < trest.get("dark_cost", 0):
        tisk_chyba("Nedostatek temné energie.")
        return

    hrac.dark_energy -= trest.get("dark_cost", 0)

    charakter_data = CHARAKTERY.get(otrok.charakter, CHARAKTERY["subka"])
    mod_reakce = charakter_data.get("reakce_na_trest", 1.0)

    for stat, hodnota in trest["efekty"].items():
        mod_hodnota = int(hodnota * mod_reakce)
        otrok.zvysit_stat(stat, mod_hodnota)

    hp_dmg = random.randint(*trest["hp_dmg"])
    otrok.zvysit_stat("hp", -hp_dmg)

    if random.random() < trest.get("riziko_smrti", 0.0):
        otrok.hp = 0
        tisk_chyba(f"{otrok.jmeno} zemřela na následky trestu!")

    hrac.vliv_inkvizice = min(100, hrac.vliv_inkvizice + trest.get("vliv_inkvizice", 0))
    hrac.reputace_mesta = max(-100, min(100, hrac.reputace_mesta + trest.get("reputace_mesta", 0)))

    otrok.aktualizuj_fazi()
    tisk_ok(f"Trest {trest['nazev']} aplikován na {otrok.jmeno}.")
    print(f"   HP: {otrok.hp}/{otrok.max_hp} | Strach: {otrok.strach} | Submisivita: {otrok.submisivita}")

def proved_odmenu(otrok, hrac, id_odmeny):
    if id_odmeny not in ODMENY:
        tisk_chyba("Neplatná odměna.")
        return

    odmena = ODMENY[id_odmeny]

    if hrac.gold < odmena.get("cena_gold", 0):
        tisk_chyba("Nedostatek zlata.")
        return
    if hrac.sex_energy < odmena.get("cena_energie", 0):
        tisk_chyba("Nedostatek sexuální energie.")
        return

    hrac.gold -= odmena.get("cena_gold", 0)
    hrac.sex_energy -= odmena.get("cena_energie", 0)

    charakter_data = CHARAKTERY.get(otrok.charakter, CHARAKTERY["subka"])
    mod_reakce = charakter_data.get("reakce_na_odmenu", 1.0)

    for stat, hodnota in odmena["efekty"].items():
        mod_hodnota = int(hodnota * mod_reakce)
        otrok.zvysit_stat(stat, mod_hodnota)

    hrac.vliv_inkvizice = max(0, hrac.vliv_inkvizice + odmena.get("vliv_inkvizice", 0))

    otrok.aktualizuj_fazi()
    tisk_ok(f"Odměna {odmena['nazev']} dána otrokyni {otrok.jmeno}.")
    print(f"   Loajalita: {otrok.loajalita} | Důvěra: {otrok.duvera} | Touha: {otrok.touha}")

def menu_trestu(otrok, hrac):
    clear()
    print(f"{RED}--- Tresty pro {otrok.jmeno} ---{NC}\n")
    seznam = list(TRESTY.keys())
    for i, id_trestu in enumerate(seznam, 1):
        trest = TRESTY[id_trestu]
        print(f"{i}) {trest['nazev']} – {trest['popis']}")
        print(f"   Temná energie: {trest['dark_cost']} | Riziko smrti: {int(trest['riziko_smrti']*100)}% | Vliv inkvizice: +{trest['vliv_inkvizice']}\n")
    print("0) Zpět")
    volba = input("> ").strip()
    if volba == "0":
        return
    try:
        idx = int(volba) - 1
        if 0 <= idx < len(seznam):
            proved_trest(otrok, hrac, seznam[idx])
        else:
            tisk_chyba("Špatná volba.")
    except ValueError:
        tisk_chyba("Zadej číslo.")

def menu_odmen(otrok, hrac):
    clear()
    print(f"{GREEN}--- Odměny pro {otrok.jmeno} ---{NC}\n")
    seznam = list(ODMENY.keys())
    for i, id_odmeny in enumerate(seznam, 1):
        odmena = ODMENY[id_odmeny]
        print(f"{i}) {odmena['nazev']} – {odmena['popis']}")
        print(f"   Zlato: {odmena['cena_gold']} | Energie: {odmena['cena_energie']} | Vliv inkvizice: {odmena['vliv_inkvizice']}\n")
    print("0) Zpět")
    volba = input("> ").strip()
    if volba == "0":
        return
    try:
        idx = int(volba) - 1
        if 0 <= idx < len(seznam):
            proved_odmenu(otrok, hrac, seznam[idx])
        else:
            tisk_chyba("Špatná volba.")
    except ValueError:
        tisk_chyba("Zadej číslo.")
