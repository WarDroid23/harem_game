# game/tresty_odmeny.py
# Dark Expansion – vylepšený systém trestů a odměn

import random
from data.tresty import TRESTY
from data.odmeny import ODMENY
from data.charaktery import CHARAKTERY
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GREEN, RED, CYAN, MAGENTA, GOLD, YELLOW, NC


def proved_trest(otrok, hrac, id_trestu):
    if id_trestu not in TRESTY:
        tisk_chyba("Neplatný trest.")
        return False

    trest = TRESTY[id_trestu]

    if hrac.dark_energy < trest.get("dark_cost", 0):
        tisk_chyba("Nedostatek temné energie.")
        return False

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
        return True

    hrac.vliv_inkvizice = min(100, hrac.vliv_inkvizice + trest.get("vliv_inkvizice", 0))
    hrac.reputace_mesta = max(-100, min(100, hrac.reputace_mesta + trest.get("reputace_mesta", 0)))

    otrok.aktualizuj_fazi()
    tisk_ok(f"Trest «{trest['nazev']}» byl aplikován na {otrok.jmeno}.")
    print(f"   {RED}Strach: {otrok.strach} | Submisivita: {otrok.submisivita} | Broken: {otrok.broken}{NC}")
    return True


def proved_odmenu(otrok, hrac, id_odmeny):
    if id_odmeny not in ODMENY:
        tisk_chyba("Neplatná odměna.")
        return False

    odmena = ODMENY[id_odmeny]

    # Speciální požadavky
    if odmena.get("vyzaduje_partnerku") and not getattr(otrok, "partnerka", False):
        tisk_chyba(f"{otrok.jmeno} není tvá partnerka. Tuto odměnu jí zatím nemůžeš dát.")
        return False

    if hrac.gold < odmena.get("cena_gold", 0):
        tisk_chyba("Nedostatek zlata.")
        return False
    if hrac.sex_energy < odmena.get("cena_energie", 0):
        tisk_chyba("Nedostatek sexuální energie.")
        return False

    hrac.gold -= odmena.get("cena_gold", 0)
    hrac.sex_energy -= odmena.get("cena_energie", 0)

    charakter_data = CHARAKTERY.get(otrok.charakter, CHARAKTERY["subka"])
    mod_reakce = charakter_data.get("reakce_na_odmenu", 1.0)

    for stat, hodnota in odmena["efekty"].items():
        # Speciální handlování pro owned_mark a romance_body
        if stat == "owned_mark":
            otrok.owned_mark = True
            continue
        if stat == "romance_body":
            if hasattr(otrok, "romance_body"):
                otrok.romance_body = min(100, getattr(otrok, "romance_body", 0) + hodnota)
            continue
        mod_hodnota = int(hodnota * mod_reakce)
        otrok.zvysit_stat(stat, mod_hodnota)

    hrac.vliv_inkvizice = max(0, hrac.vliv_inkvizice + odmena.get("vliv_inkvizice", 0))

    otrok.aktualizuj_fazi()

    # Flavored výpis podle typu odměny
    typ = odmena.get("typ", "zakladni")
    if typ == "eroticka":
        tisk_ok(f"Odměna «{odmena['nazev']}»… {otrok.jmeno} se chvěje vděčností.")
    elif typ == "ritual":
        tisk_ok(f"Rituál dokončen. {otrok.jmeno} klečí a šeptá tvé jméno.")
    elif typ == "partnerska":
        tisk_ok(f"Noc s partnerkou. {otrok.jmeno} usíná s úsměvem a tvým jménem na rtech.")
    elif typ == "vlastnictvi":
        tisk_ok(f"Značka je hotová. {otrok.jmeno} se dívá na své tělo a ví, komu patří.")
    else:
        tisk_ok(f"Odměna «{odmena['nazev']}» dána otrokyni {otrok.jmeno}.")

    print(f"   {GREEN}Loajalita: {otrok.loajalita} | Důvěra: {otrok.duvera} | Touha: {otrok.touha} | Submisivita: {otrok.submisivita}{NC}")
    return True


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
    print(f"{GREEN}--- Odměny pro {otrok.jmeno} ---{NC}")
    print(f"{CYAN}Loajalita: {otrok.loajalita} | Důvěra: {otrok.duvera} | Touha: {otrok.touha}{NC}\n")

    seznam = list(ODMENY.keys())
    for i, id_odmeny in enumerate(seznam, 1):
        odmena = ODMENY[id_odmeny]
        dostupna = True
        omezeni = ""

        if odmena.get("vyzaduje_partnerku") and not getattr(otrok, "partnerka", False):
            dostupna = False
            omezeni = f" {YELLOW}(pouze partnerka){NC}"

        barva = GREEN if dostupna else YELLOW
        print(f"{barva}{i}) {odmena['nazev']}{NC} – {odmena['popis']}{omezeni}")
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
