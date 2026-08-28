# game/odpocinek.py
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GREEN, CYAN, MAGENTA, NC

def zpracuj_den(hra):
    """Posune stav systémů o jeden den a vrátí krátké shrnutí změn."""
    harem = hra.harem
    dokoncene_najmy = []
    for otrok in harem.otrokyne:
        if otrok.na_najmu:
            otrok.dny_na_najmu += 1
            otrok.najem_zbyva_dni = max(0, otrok.najem_zbyva_dni - 1)
            if otrok.najem_zbyva_dni == 0:
                dokoncene_najmy.append(otrok.jmeno)
                otrok.na_najmu = False
                otrok.klient = None
                otrok.typ_najmu = None
                otrok.dny_na_najmu = 0
        elif otrok.hp > 0:
            lazne = harem.budovy.get("lazne")
            leceni = 10 + (lazne.uroven * 2 if lazne else 0)
            otrok.zvysit_stat("hp", leceni)

        if otrok.tehotna:
            otrok.dny_tehotenstvi += 1
            if otrok.dny_tehotenstvi >= 3:
                otrok.tehotna = False
                otrok.dny_tehotenstvi = 0
                otrok.deti += 1

    for agent in hra.hrac.agenti:
        agent.unaveny = max(0, agent.unaveny - 1)

    # Denní limity doplňkových způsobů dobíjení se obnoví až po posunu dne.
    hra.hrac.dobiti_dnes.clear()
    return dokoncene_najmy


def odpocinek(hra, rezim=None):
    hrac = hra.hrac
    clear()
    print(f"{GREEN}--- Odpočinek ---{NC}\n")

    if rezim is None:
        print("1) Klidný spánek (sexuální energie +30, temná +10)")
        print("2) Meditativní spánek (sexuální energie +15, temná +30)")
        try:
            volba = input("> ").strip()
        except EOFError:
            volba = "1"
        rezim = "meditace" if volba == "2" else "spánek"
    elif rezim not in ("spánek", "meditace"):
        rezim = "spánek"

    hrac.den += 1
    if hasattr(hra, "kalendar"):
        hra.kalendar.dalsi_den(hrac.den - 1)
    if rezim == "meditace":
        hrac.sex_energy = min(100, hrac.sex_energy + 15)
        hrac.dark_energy = min(100, hrac.dark_energy + 30)
        hrac.hp = min(hrac.max_hp, hrac.hp + 15)
        tisk_ok("Meditativní spánek obnovil tělo i temnou energii.")
    else:
        hrac.sex_energy = min(100, hrac.sex_energy + 30)
        hrac.dark_energy = min(100, hrac.dark_energy + 10)
        hrac.hp = min(hrac.max_hp, hrac.hp + 20)
        tisk_ok("Klidný spánek obnovil sexuální energii i zdraví.")
    dokoncene_najmy = zpracuj_den(hra)

    prijem_harem = hra.harem.pasivni_prijem()
    prijem_mafie = hra.mafie.vypocet_prijmu()
    hrac.gold += prijem_harem + prijem_mafie

    # Manželské bonusy
    bonus_marriage_energie = 0
    bonus_marriage_gold = 0
    for jmeno, marriage in hra.marriage_system.items():
        if marriage.je_vdana():
            bonus_marriage_energie += 10
            bonus_marriage_gold += 50
            marriage.intimita_level = min(100, marriage.intimita_level + 5)
            marriage.starne_deti()
    
    if bonus_marriage_energie > 0:
        hrac.sex_energy = min(100, hrac.sex_energy + bonus_marriage_energie)
        hrac.gold += bonus_marriage_gold
        tisk_ok(f"💍 Manželství: energie +{bonus_marriage_energie}, zlato +{bonus_marriage_gold}")

    tisk_ok(f"Energie: {hrac.sex_energy} (sex) / {hrac.dark_energy} (temno).")
    tisk_ok(f"Pasivní příjem: {prijem_harem + prijem_mafie + bonus_marriage_gold} zlaťáků.")
    if dokoncene_najmy:
        tisk_ok("Nájem skončil: " + ", ".join(dokoncene_najmy) + ".")
    if hra.questy.aktivni_quest:
        tisk_info(
            f"Aktivní quest čeká na plnění ({hra.questy.dny_zbyva} "
            "dní do konce)."
        )
    if hasattr(hra, "achievementy"):
        hra.achievementy.zaznamenej("dny", hrac.den)
    if hasattr(hra, "kalendar") and hra.kalendar.posledni_udalost:
        tisk_info(hra.kalendar.posledni_udalost)
    try:
        input("Enter...")
    except EOFError:
        pass
