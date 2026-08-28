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
    print("5) Nabídnout romantickou chvíli (8 energie, pouze se souhlasem)")
    print("6) Nabídnout partnerský vztah (po vzájemném sblížení)")
    print("7) Společná mise s partnerkou (+XP a reputace)")
    print("0) Zpět")
    volba = input("> ").strip()
    if volba == "1":
        otrok.zvysit_stat("duvera", 6)
        otrok.zvysit_stat("loajalita", 4)
        otrok.nalada = "soustředěná"
        otrok.zaznamenej_volbu("péče", "Rozhovor o minulosti", hra.hrac.den)
        tisk_ok(f"{otrok.jmeno} ti svěřila část své minulosti.")
    elif volba == "2":
        if not proved_peci(hra, otrok):
            tisk_chyba("Nemáš dost zlata na péči.")
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
            otrok.zaznamenej_volbu("role", nazev, hra.hrac.den)
            otrok.zvysit_stat("loajalita", 4)
            tisk_ok(f"{otrok.jmeno} přijala roli: {nazev}.")
    elif volba == "4":
        from game.osudy import OsudySystem
        OsudySystem().menu(hra, otrok)
    elif volba == "5":
        if otrok.vek < 18:
            tisk_chyba("Romantická linka je dostupná pouze dospělým postavám.")
        elif otrok.na_najmu:
            tisk_chyba("Nejdřív musí skončit pracovní závazek; romantická volba není služba.")
        elif hra.hrac.sex_energy < 8:
            tisk_chyba("Nemáš dost energie na klidný večer.")
        else:
            souhlas = input(
                f"Zeptat se {otrok.jmeno}, zda chce dobrovolně sdílet romantický večer? (a/n): "
            ).strip().lower()
            if souhlas not in ("a", "ano"):
                otrok.romance_stav = "respektovaný odstup"
                otrok.zaznamenej_volbu("romantika", "Respektovaný odstup", hra.hrac.den)
                tisk_info(f"{otrok.jmeno} dnes nechce. Její hranice byly respektovány.")
            else:
                hra.hrac.sex_energy -= 8
                otrok.souhlas_romance = True
                otrok.romance_body = min(100, otrok.romance_body + 12)
                otrok.romance_volby.append({"den": hra.hrac.den, "typ": "společná romantická chvíle"})
                otrok.zaznamenej_volbu("romantika", "Společná romantická chvíle", hra.hrac.den)
                otrok.zvysit_stat("duvera", 8)
                otrok.zvysit_stat("loajalita", 6)
                if otrok.romance_body >= 70:
                    otrok.romance_stav = "oddané partnerství"
                elif otrok.romance_body >= 35:
                    otrok.romance_stav = "blízký vztah"
                else:
                    otrok.romance_stav = "opatrné sbližování"
                tisk_ok(
                    f"Večer proběhl v intimní, ale neexplicitní atmosféře. "
                    f"{otrok.jmeno} zvolila tempo sama; vztah: {otrok.romance_stav}."
                )
    elif volba == "6":
        if otrok.vek < 18:
            tisk_chyba("Partnerský vztah je dostupný pouze dospělým postavám.")
        elif otrok.na_najmu:
            tisk_chyba("Nejdřív musí skončit pracovní závazek.")
        elif otrok.partnerka:
            volba_rozchod = input(
                f"{otrok.jmeno} je tvá partnerka. Ukončit vztah? (a/n): "
            ).strip().lower()
            if volba_rozchod in ("a", "ano"):
                otrok.partnerka = False
                otrok.partner_od_den = 0
                otrok.romance_stav = "bývalé partnerství"
                otrok.zaznamenej_volbu("vztah", "Ukončení partnerského vztahu", hra.hrac.den)
                tisk_info(f"Vztah s {otrok.jmeno} byl ukončen s respektem.")
        elif otrok.romance_body < 70 or otrok.duvera < 55:
            tisk_chyba("Nejdřív je potřeba vybudovat hlubší důvěru a vztah.")
        else:
            souhlas = input(
                f"Nabídnout {otrok.jmeno} dobrovolný partnerský vztah? (a/n): "
            ).strip().lower()
            if souhlas in ("a", "ano"):
                otrok.partnerka = True
                otrok.partner_od_den = hra.hrac.den
                otrok.romance_stav = "partnerský vztah"
                otrok.zaznamenej_volbu("vztah", "Přijetí partnerského vztahu", hra.hrac.den)
                otrok.zvysit_stat("loajalita", 8)
                otrok.zvysit_stat("duvera", 8)
                hra.hrac.reputace_mesta += 2
                tisk_ok(
                    f"{otrok.jmeno} nabídku přijala. Stala se tvou osobní partnerkou "
                    "a NPC společnicí."
                )
            else:
                tisk_info(f"{otrok.jmeno} nabídku odmítla a její rozhodnutí bylo respektováno.")
    elif volba == "7":
        if not otrok.partnerka:
            tisk_chyba("Tato postava není tvou partnerkou.")
        elif hra.hrac.sex_energy < 10:
            tisk_chyba("Na společnou misi nemáš dost energie.")
        else:
            hra.hrac.sex_energy -= 10
            hra.hrac.pridej_xp(20)
            hra.hrac.reputace_mesta += 2
            otrok.zvysit_stat("duvera", 4)
            otrok.zaznamenej_volbu("partnerství", "Společná mise", hra.hrac.den)
            tisk_ok(
                f"Ty a {otrok.jmeno} jste dokončili společnou misi. "
                "Získal jsi 20 XP a reputace +2."
            )
    elif volba != "0":
        tisk_chyba("Neplatná volba.")
    if volba != "4":
        input("Enter...")


def porada_haremu(hra):
    if not proved_poradu(hra):
        tisk_chyba("Nemáš nikoho, kdo by se porady účastnil.")
    input("Enter...")


def proved_peci(hra, otrok, respektuj_najem=False):
    if (
        otrok.hp <= 0
        or hra.hrac.gold < 20
        or (respektuj_najem and otrok.na_najmu)
    ):
        return False
    hra.hrac.gold -= 20
    otrok.zvysit_stat("hp", 25)
    otrok.zaznamenej_volbu("péče", "Péče a zotavení", hra.hrac.den)
    tisk_ok(f"{otrok.jmeno} si odpočinula. HP +25, důvěra +3.")
    otrok.zvysit_stat("duvera", 3)
    return True


def proved_poradu(hra, postavy=None):
    aktivni = (
        hra.harem.vsechny_aktivni()
        if postavy is None
        else [o for o in postavy if o in hra.harem.vsechny_aktivni() and not o.na_najmu]
    )
    if not aktivni:
        return False
    for otrok in aktivni:
        otrok.zvysit_stat("loajalita", 2)
        otrok.zvysit_stat("duvera", 1)
    hra.hrac.reputace_mesta += 1
    tisk_ok("Porada proběhla. Loajalita všech +2, reputace města +1.")
    return True


def zobraz_profil(otrok):
    """Vypíše úplný profil jedné dospělé postavy bez odhalování neplatného věku."""
    print(f"\n--- Profil: {otrok.jmeno} ---")
    print(f"Věk: {max(18, int(otrok.vek))} | Role: {otrok.role}")
    print(f"Charakter: {otrok.charakter} | Osud: {otrok.popis_osudu()}")
    if otrok.partnerka:
        print(f"Partnerský vztah: ano (od dne {otrok.partner_od_den})")
    else:
        print("Partnerský vztah: ne")
    print(
        f"Vztah: {otrok.romance_stav} ({otrok.romance_body}/100) | "
        f"Loajalita: {otrok.loajalita} | Důvěra: {otrok.duvera}"
    )
    print(
        "Statistiky: "
        f"HP {otrok.hp}/{otrok.max_hp}, poslušnost {otrok.poslusnost}, "
        f"submisivita {otrok.submisivita}, touha {otrok.touha}, strach {otrok.strach}"
    )
    historie = list(otrok.historie_voleb)
    if not historie:
        historie = [
            {"typ": "osud", "volba": volba.get("volba", "neznámá")}
            for volba in otrok.osud_volby
            if isinstance(volba, dict)
        ]
    print("Historie voleb:")
    if not historie:
        print("  Zatím žádná zaznamenaná volba.")
    else:
        for zaznam in historie[-12:]:
            den = f" (den {zaznam['den']})" if "den" in zaznam else ""
            print(f"  • {zaznam.get('typ', 'volba')}: {zaznam.get('volba', '')}{den}")


def menu_profily(hra):
    while True:
        clear()
        aktivni = hra.harem.vsechny_aktivni()
        print("--- Profily postav v harému ---\n")
        if not aktivni:
            tisk_chyba("Nemáš žádné aktivní postavy.")
            input("Enter...")
            return
        for index, otrok in enumerate(aktivni, 1):
            print(
                f"{index}) {otrok.jmeno} — {max(18, int(otrok.vek))} let, "
                f"{otrok.role}, vztah {otrok.romance_stav}"
            )
        print("0) Zpět")
        volba = input("> ").strip()
        if volba == "0":
            return
        try:
            index = int(volba) - 1
        except ValueError:
            tisk_chyba("Zadej číslo.")
            input("Enter...")
            continue
        if not 0 <= index < len(aktivni):
            tisk_chyba("Špatná volba.")
            input("Enter...")
            continue
        clear()
        zobraz_profil(aktivni[index])
        input("Enter...")


def menu_haremu(hra):
    while True:
        clear()
        print("--- Harem: péče a vztahy ---\n")
        print(f"Členky: {hra.harem.pocet()} | Úroveň harému: {hra.harem.harem_level}")
        print("1) Osobní rozhovor a osud")
        print("2) Společná porada")
        print("3) Profily postav a historie voleb")
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
            menu_profily(hra)
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
