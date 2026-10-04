# game/vyvoj.py
from models.hrac import Hrac
from utils.vypis import (
    clear, nacti_volbu, tisk_ok, tisk_chyba, tisk_info, vytiskni_volbu,
)
from data.zbrane import ZBRANE
from models.inventory import Zbran
from config import GREEN, CYAN, GOLD, MAGENTA, NC

CENA_TRENINK = 100
SEX_ZA_VYTRVALOST = 5
TEMNO_ZA_VYTRVALOST = 3


def zobraz_vyvoj(hrac: Hrac):
    clear()
    print(f"{GOLD}--- Vývoj postavy ---{NC}")
    print(f"Level: {hrac.level} (XP: {hrac.xp}/{hrac.xp_next})")
    print(
        f"Zlato: {hrac.gold} | Energie: {hrac.sex_energy}/{hrac.max_sex()} | "
        f"Temná: {hrac.dark_energy}/{hrac.max_temno()}"
    )
    print(f"\n{CYAN}Dovednosti:{NC}")
    for skill, hodnota in hrac.skilly.items():
        extra = ""
        if skill == "vytrvalost":
            extra = f"  → max sex +{hodnota * SEX_ZA_VYTRVALOST}, temno +{hodnota * TEMNO_ZA_VYTRVALOST}"
        print(f"  {skill}: {hodnota}{extra}")
    print(f"\n1) Trénovat dovednost ({CENA_TRENINK} zlaťáků)")
    vytiskni_volbu('2', 'Trénink výdrže (zvyšuje maximum energie)')
    vytiskni_volbu('3', 'Koupit zbraň')
    vytiskni_volbu('0', 'Zpět')
    try:
        volba = nacti_volbu(
            {"0", "1", "2", "3"},
            chybova_zprava="Neplatná volba. Zadej 0, 1, 2 nebo 3.",
        )
    except EOFError:
        return
    if volba == "1":
        print("Dostupné dovednosti:")
        skills = list(hrac.skilly.keys())
        for i, skill in enumerate(skills, 1):
            print(f"{i}) {skill}")
        if not skills:
            tisk_info("Nejsou dostupné žádné dovednosti k tréninku.")
            return
        try:
            vyber = nacti_volbu(
                {"0", *(str(index) for index in range(1, len(skills) + 1))},
                prompt="Vyber dovednost (0 = zpět): ",
                chybova_zprava="Neplatné číslo dovednosti.",
            )
        except EOFError:
            return
        if vyber != "0":
            skill_name = skills[int(vyber) - 1]
            if hrac.gold >= CENA_TRENINK:
                hrac.gold -= CENA_TRENINK
                hrac.skilly[skill_name] += 1
                tisk_ok(f"Dovednost {skill_name} zvýšena na {hrac.skilly[skill_name]}.")
                if skill_name == "vytrvalost":
                    _aplikuj_vytrvalost(hrac)
            else:
                tisk_chyba("Nedostatek zlata.")
    elif volba == "2":
        try:
            _trenink_vytrvalosti(hrac)
        except EOFError:
            return
    elif volba == "3":
        print("Dostupné zbraně:")
        for i, z in enumerate(ZBRANE, 1):
            print(f"{i}) {z['nazev']} (typ: {z['typ']}, cena: {z['cena']}, poškození: {z['poskozeni']})")
        if not ZBRANE:
            tisk_info("Momentálně nejsou dostupné žádné zbraně.")
            return
        try:
            vyber = nacti_volbu(
                {"0", *(str(index) for index in range(1, len(ZBRANE) + 1))},
                prompt="Vyber zbraň (0 = zpět): ",
                chybova_zprava="Neplatné číslo zbraně.",
            )
        except EOFError:
            return
        if vyber != "0":
            z_data = ZBRANE[int(vyber) - 1]
            if hrac.gold >= z_data["cena"]:
                hrac.gold -= z_data["cena"]
                nova_zbran = Zbran(**z_data)
                hrac.inventar.pridej_zbran(nova_zbran)
                tisk_ok(f"Koupena zbraň {nova_zbran.nazev}.")
            else:
                tisk_chyba("Nedostatek zlata.")
    try:
        input("Enter...")
    except EOFError:
        pass


def _aplikuj_vytrvalost(hrac):
    from models.hrac import MAX_SEX_STROPP, MAX_TEMNO_STROPP
    hrac.max_sex_energy = min(MAX_SEX_STROPP, hrac.max_sex() + SEX_ZA_VYTRVALOST)
    hrac.max_dark_energy = min(MAX_TEMNO_STROPP, hrac.max_temno() + TEMNO_ZA_VYTRVALOST)
    tisk_ok(
        f"Výdrž posílila tělo. Max energie: {hrac.max_sex()} sex / {hrac.max_temno()} temno."
    )


def _trenink_vytrvalosti(hrac):
    print(f"\n{MAGENTA}--- Trénink výdrže ---{NC}")
    print(f"Aktuální výdrž: {hrac.skilly.get('vytrvalost', 0)}")
    print(f"Max energie: {hrac.sex_energy}/{hrac.max_sex()} sex | {hrac.dark_energy}/{hrac.max_temno()} temno")
    print(f"Cena: {CENA_TRENINK} zl. → +{SEX_ZA_VYTRVALOST} max sex, +{TEMNO_ZA_VYTRVALOST} max temno")
    vytiskni_volbu('1', 'Trénovat výdrž')
    vytiskni_volbu('0', 'Zpět')
    volba = nacti_volbu(
        {"0", "1"},
        chybova_zprava="Neplatná volba. Zadej 0 nebo 1.",
    )
    if volba != "1":
        return
    if hrac.gold < CENA_TRENINK:
        tisk_chyba("Nedostatek zlata.")
        return
    from models.hrac import MAX_SEX_STROPP
    if hrac.max_sex() >= MAX_SEX_STROPP:
        tisk_info("Dosáhl jsi stropu sexuální výdrže.")
        return
    hrac.gold -= CENA_TRENINK
    hrac.skilly["vytrvalost"] = hrac.skilly.get("vytrvalost", 0) + 1
    _aplikuj_vytrvalost(hrac)
    hrac.pridej_sex_energy(SEX_ZA_VYTRVALOST)
    hrac.pridej_dark_energy(TEMNO_ZA_VYTRVALOST)
    tisk_ok(f"Výdrž: {hrac.skilly['vytrvalost']} | energie doplněna o přírůstek.")
