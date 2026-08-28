from utils.vypis import clear, tisk_chyba, tisk_info, tisk_ok


def _vyber_otrokyni(hra):
    aktivni = hra.harem.vsechny_aktivni()
    if not aktivni:
        tisk_chyba("Nemáš žádné aktivní členky harému.")
        input("Enter...")
        return None
    print("Vyber postavu:")
    for index, otrok in enumerate(aktivni, 1):
        stav_osudu = "dokončen" if otrok.osud_dokonceno else f"{otrok.osud_krok}/2"
        print(
            f"{index}) {otrok.jmeno} — role: {otrok.role}, "
            f"loajalita {otrok.loajalita}, důvěra {otrok.duvera}, osud {stav_osudu}"
        )
    print("0) Zpět")
    try:
        index = int(input("> ")) - 1
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")
        return None
    if index < 0:
        return None
    if index >= len(aktivni):
        tisk_chyba("Špatná volba.")
        input("Enter...")
        return None
    return aktivni[index]


def _osobni_akce(hra, otrok):
    print(f"\n--- Péče o {otrok.jmeno} ---")
    print("1) Rozhovor o minulosti (+důvěra, +loajalita)")
    print("2) Péče a zotavení (20 zlata, +HP)")
    print("3) Přidělit roli v pevnosti")
    print("4) Otevřít osobní osud")
    print("0) Zpět")
    volba = input("> ").strip()
    if volba == "1":
        otrok.zvysit_stat("duvera", 6)
        otrok.zvysit_stat("loajalita", 4)
        otrok.nalada = "soustředěná"
        tisk_ok(f"{otrok.jmeno} ti svěřila část své minulosti.")
    elif volba == "2":
        if hra.hrac.gold < 20:
            tisk_chyba("Nemáš dost zlata na péči.")
        else:
            hra.hrac.gold -= 20
            otrok.zvysit_stat("hp", 25)
            otrok.zvysit_stat("duvera", 3)
            tisk_ok(f"{otrok.jmeno} si odpočinula. HP +25, důvěra +3.")
    elif volba == "3":
        role = input("Role (stráž/řemesla/vyjednávání/zpravodajství): ").strip().lower()
        role_map = {
            "stráž": ("strážkyně", "obrana", 2),
            "řemesla": ("správkyně dílny", "obchod", 2),
            "vyjednávání": ("vyjednavačka", "vyjednavani", 2),
            "zpravodajství": ("zpravodajka", "temnota", 2),
        }
        if role not in role_map:
            tisk_chyba("Neznámá role.")
        else:
            nazev, dovednost, bonus = role_map[role]
            stara_role = otrok.role
            otrok.role = nazev
            if stara_role != nazev:
                hra.hrac.skilly[dovednost] = hra.hrac.skilly.get(dovednost, 0) + bonus
            otrok.zvysit_stat("loajalita", 4)
            tisk_ok(f"{otrok.jmeno} přijala roli: {nazev}.")
    elif volba == "4":
        from game.osudy import OsudySystem
        OsudySystem().menu(hra, otrok)
    elif volba != "0":
        tisk_chyba("Neplatná volba.")
    if volba != "4":
        input("Enter...")


def porada_haremu(hra):
    aktivni = hra.harem.vsechny_aktivni()
    if not aktivni:
        tisk_chyba("Nemáš nikoho, kdo by se porady účastnil.")
        input("Enter...")
        return
    for otrok in aktivni:
        otrok.zvysit_stat("loajalita", 2)
        otrok.zvysit_stat("duvera", 1)
    hra.hrac.reputace_mesta += 1
    tisk_ok(f"Porada proběhla. Loajalita všech +2, reputace města +1.")
    input("Enter...")


def menu_haremu(hra):
    while True:
        clear()
        print("--- Harem: péče a vztahy ---\n")
        print(f"Členky: {hra.harem.pocet()} | Úroveň harému: {hra.harem.harem_level}")
        print("1) Osobní rozhovor a osud")
        print("2) Společná porada")
        print("3) Přehled rolí a osudů")
        print("0) Zpět")
        volba = input("> ").strip()
        if volba == "0":
            return
        if volba == "1":
            otrok = _vyber_otrokyni(hra)
            if otrok:
                _osobni_akce(hra, otrok)
        elif volba == "2":
            porada_haremu(hra)
        elif volba == "3":
            clear()
            for otrok in hra.harem.vsechny_aktivni():
                print(
                    f"{otrok.jmeno}: {otrok.role}, nálada {otrok.nalada}, "
                    f"loajalita {otrok.loajalita}, důvěra {otrok.duvera}, "
                    f"osud {otrok.popis_osudu()}"
                )
            input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
