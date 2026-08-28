# game/odpocinek.py
from utils.vypis import clear, tisk_ok, tisk_chyba
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

    return dokoncene_najmy

def odpocinek(hra):
    hrac = hra.hrac
    clear()
    print(f"{GREEN}--- Odpočinek ---{NC}\n")

    hrac.den += 1
    hrac.sex_energy = min(100, hrac.sex_energy + 30)
    hrac.dark_energy = min(100, hrac.dark_energy + 10)
    hrac.hp = min(hrac.max_hp, hrac.hp + 20)
    dokoncene_najmy = zpracuj_den(hra)

    prijem_harem = hra.harem.pasivni_prijem()
    prijem_mafie = hra.mafie.vypocet_prijmu()
    hrac.gold += prijem_harem + prijem_mafie

    tisk_ok(f"Odpočinul sis. Energie: {hrac.sex_energy} (sex) / {hrac.dark_energy} (temno).")
    tisk_ok(f"Pasivní příjem: {prijem_harem + prijem_mafie} zlaťáků.")
    if dokoncene_najmy:
        tisk_ok("Nájem skončil: " + ", ".join(dokoncene_najmy) + ".")
    if hra.questy.aktivni_quest:
        tisk_info(
            f"Aktivní quest čeká na plnění ({hra.questy.dny_zbyva} "
            "dní do konce)."
        )
    try:
        input("Enter...")
    except EOFError:
        pass
