# game/odpocinek.py
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GREEN, CYAN, MAGENTA, NC

def zpracuj_den(hra):
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
    hra.hrac.dobiti_dnes.clear()
    return dokoncene_najmy


def odpocinek(hra, rezim=None):
    hrac = hra.hrac
    clear()
    print(f"{GREEN}--- Odpočinek / nový den ---{NC}\n")
    if rezim is None:
        print("1) Klidný spánek (plná energie + HP)")
        print("2) Meditativní spánek (plná energie, více temna v duchu)")
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

    hrac.dopln_energie_naplno()
    if rezim == "meditace":
        hrac.hp = min(hrac.max_hp, hrac.hp + 15)
        tisk_ok("Meditativní spánek. Probudil ses s plnou energií.")
    else:
        hrac.hp = min(hrac.max_hp, hrac.hp + 20)
        tisk_ok("Klidný spánek. Probudil ses s plnou energií.")

    dokoncene_najmy = zpracuj_den(hra)
    prijem_harem = hra.harem.pasivni_prijem()
    prijem_mafie = hra.mafie.vypocet_prijmu()
    hrac.gold += prijem_harem + prijem_mafie

    bonus_marriage_gold = 0
    for jmeno, marriage in hra.marriage_system.items():
        if marriage.je_vdana():
            bonus_marriage_gold += 50
            marriage.intimita_level = min(100, marriage.intimita_level + 5)
            marriage.starne_deti()
    if bonus_marriage_gold:
        hrac.gold += bonus_marriage_gold
        tisk_ok(f"💍 Manželství: zlato +{bonus_marriage_gold}")

    tisk_ok(
        f"Energie naplněna: {hrac.sex_energy}/{hrac.max_sex()} (sex) | "
        f"{hrac.dark_energy}/{hrac.max_temno()} (temno)."
    )
    tisk_ok(f"Pasivní příjem: {prijem_harem + prijem_mafie + bonus_marriage_gold} zlaťáků.")
    if dokoncene_najmy:
        tisk_ok("Nájem skončil: " + ", ".join(dokoncene_najmy) + ".")
    if hra.questy.aktivni_quest:
        tisk_info(f"Aktivní quest čeká na plnění ({hra.questy.dny_zbyva} dní do konce).")
    if hasattr(hra, "achievementy"):
        hra.achievementy.zaznamenej("dny", hrac.den)
    if hasattr(hra, "kalendar") and hra.kalendar.posledni_udalost:
        tisk_info(hra.kalendar.posledni_udalost)

    try:
        from game.save_load import uloz_autosave
        if uloz_autosave(hra):
            tisk_info("Autosave uložen (JSON).")
    except Exception as e:
        tisk_chyba(f"Autosave selhal: {e}")

    try:
        input("Enter...")
    except EOFError:
        pass
