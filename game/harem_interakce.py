from collections import Counter

from utils.vypis import hlavicka, clear, tisk_chyba, tisk_info, tisk_ok, vytiskni_volbu
from utils.vypis import ukazatel
from config import CYAN, GREEN, MAGENTA, RED, YELLOW, NC
from data.charaktery import CHARAKTERY, nazev_charakteru, normalizuj_charakter
from game.tresty_odmeny import nastav_oblibenou, menu_odmen


def _vyber_otrokyni(hra):
    aktivni = hra.harem.vsechny_aktivni()
    if not aktivni:
        tisk_chyba("Nemáš žádné aktivní členky harému.")
        input("Enter...")
        return None
    print("Vyber postavu:")
    for index, otrok in enumerate(aktivni, 1):
        stav_osudu = "dokončen" if otrok.osud_dokonceno else f"{otrok.osud_krok}/2"
        hvezda = "★ " if getattr(otrok, "oblibena", False) else ""
        znacky = []
        if getattr(otrok, "je_manzelkou", False):
            znacky.append("💍")
        if getattr(otrok, "partnerka", False):
            znacky.append("♥")
        zn = (" " + " ".join(znacky)) if znacky else ""
        print(
            f"{index}) {hvezda}{otrok.jmeno}{zn} — {nazev_charakteru(otrok.charakter)}, "
            f"role: {otrok.role}, "
            f"loajalita {otrok.loajalita}, důvěra {otrok.duvera}, osud {stav_osudu}"
        )
    vytiskni_volbu('0', 'Zpět')
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
    hlavicka(f'Péče o {otrok.jmeno}')
    print(
        f"Osobnost: {nazev_charakteru(otrok.charakter)} — "
        f"{CHARAKTERY[normalizuj_charakter(otrok.charakter)]['popis']}"
    )
    vytiskni_volbu('1', 'Rozhovor o minulosti (+důvěra, +loajalita)')
    vytiskni_volbu('2', 'Péče a zotavení (20 zlata, +HP)')
    vytiskni_volbu('3', 'Přidělit roli v pevnosti')
    vytiskni_volbu('4', 'Otevřít osobní osud')
    vytiskni_volbu('5', 'Nabídnout romantickou chvíli (8 energie, pouze se souhlasem)')
    vytiskni_volbu('6', 'Nabídnout partnerský vztah (po vzájemném sblížení)')
    vytiskni_volbu('7', 'Společná mise s partnerkou (+XP a reputace)')
    vytiskni_volbu('8', 'Jmenovat oblíbenkyní harému')
    vytiskni_volbu('9', 'Odměny (systém odměn)')
    vytiskni_volbu('10', 'Bojová společnice (jmenovat/odvolat z doprovodu v soubojích)')
    vytiskni_volbu('11', 'Poznat její osobnost a promluvit si o jejích přáních')
    vytiskni_volbu('12', 'Pokračovat v jejím osobním příběhu')
    vytiskni_volbu('13', 'Otevřít její osobní deník')
    vytiskni_volbu('14', 'Graf vývoje jejích statistik')
    vytiskni_volbu('0', 'Zpět')
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
    elif volba == "8":
        nastav_oblibenou(hra, otrok)
    elif volba == "9":
        menu_odmen(otrok, hra.hrac)
    elif volba == "10":
        pevnost = getattr(hra, "pevnost", None)
        if pevnost is not None:
            if getattr(pevnost, "bojova_partnerka", "") == otrok.jmeno:
                pevnost.bojova_partnerka = ""
                tisk_ok(f"{otrok.jmeno} již není tvou aktivní bojovou společnicí.")
            else:
                pevnost.bojova_partnerka = otrok.jmeno
                otrok.zvysit_stat("loajalita", 4)
                otrok.zvysit_stat("duvera", 4)
                tisk_ok(f"★ {otrok.jmeno} byla jmenována tvou bojovou společnicí a bude stát po tvém boku v soubojích!")
        else:
            tisk_chyba("Pevnost není k dispozici.")
    elif volba == "11":
        _rozhovor_o_osobnosti(hra, otrok)
    elif volba == "12":
        from game.osobni_pribehy import pokracuj_v_pribehu
        pokracuj_v_pribehu(hra, otrok)
    elif volba == "13":
        from game.osobni_pribehy import zobraz_denik_postavy
        zobraz_denik_postavy(otrok)
    elif volba == "14":
        zobraz_graf_statistik(otrok)
    elif volba != "0":
        tisk_chyba("Neplatná volba.")
    if volba != "4":
        input("Enter...")


def _rozhovor_o_osobnosti(hra, otrok):
    charakter = CHARAKTERY[normalizuj_charakter(otrok.charakter)]
    modifikatory = charakter.get("modifikatory", {})
    print(f"\n{CYAN}Rozhovor s {otrok.jmeno}{NC}")
    print(f"„{charakter['popis']}“")
    vytiskni_volbu("1", "Naslouchat bez přerušování (+7 důvěra, +3 loajalita)")
    vytiskni_volbu("2", "Povzbudit její silnou stránku (+5 vybraný vztahový rys, +3 důvěra)")
    vytiskni_volbu("3", "Domluvit si jasné hranice (+5 důvěra, -5 strach)")
    vytiskni_volbu("0", "Rozhovor odložit")
    volba = input("> ").strip()
    reakce = max(0.5, float(charakter.get("reakce_na_odmenu", 1.0)))

    if volba == "1":
        duvera = max(1, int(7 * modifikatory.get("duvera", 1.0) * reakce))
        loajalita = max(1, int(3 * modifikatory.get("loajalita", 1.0) * reakce))
        otrok.zvysit_stat("duvera", duvera)
        otrok.zvysit_stat("loajalita", loajalita)
        vysledek = f"Důvěra +{duvera}, loajalita +{loajalita}."
    elif volba == "2":
        rysy = ("duvera", "loajalita", "touha")
        rys = max(rysy, key=lambda stat: modifikatory.get(stat, 1.0))
        hodnota = max(1, int(5 * modifikatory.get(rys, 1.0) * reakce))
        duvera = max(1, int(3 * modifikatory.get("duvera", 1.0) * reakce))
        otrok.zvysit_stat(rys, hodnota)
        otrok.zvysit_stat("duvera", duvera)
        popisy = {"duvera": "důvěra", "loajalita": "loajalita", "touha": "nadšení"}
        vysledek = f"{popisy[rys]} +{hodnota}, důvěra +{duvera}."
    elif volba == "3":
        duvera = max(1, int(5 * modifikatory.get("duvera", 1.0) * reakce))
        otrok.zvysit_stat("duvera", duvera)
        otrok.zvysit_stat("strach", -5)
        vysledek = f"Důvěra +{duvera}, strach -5."
    elif volba == "0":
        tisk_info("Rozhovor byl odložen; její rozhodnutí i soukromí respektuješ.")
        return
    else:
        tisk_chyba("Neplatná volba rozhovoru.")
        return

    otrok.nalada = "klidná"
    otrok.zaznamenej_volbu("rozhovor", "Naslouchání osobním přáním", hra.hrac.den)
    tisk_ok(f"{otrok.jmeno} ocenila, že jsi jí věnoval čas. {vysledek}")


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
    hlavicka(f'Profil: {otrok.jmeno}')
    print(f"Věk: {max(18, int(otrok.vek))} | Role: {otrok.role}")
    charakter_id = normalizuj_charakter(otrok.charakter)
    charakter = CHARAKTERY[charakter_id]
    print(f"Charakter: {charakter['nazev']} | Osud: {otrok.popis_osudu()}")
    print(f"  {charakter['popis']}")
    from game.charakter_bonusy import schopnost_postavy
    print(f"Schopnost: {schopnost_postavy(otrok)}")
    krok_pribehu = min(3, int(getattr(otrok, "osobni_pribeh_krok", 0)))
    stav_pribehu = "dokončen" if getattr(otrok, "osobni_pribeh_dokonceno", False) else f"{krok_pribehu}/3"
    print(f"Osobní příběh: {stav_pribehu}")
    if getattr(otrok, "oblibena", False):
        print(f"★ Oblíbenkyně (od dne {getattr(otrok, 'oblibena_od_den', '?')})")
    if otrok.partnerka:
        print(f"Partnerský vztah: ano (od dne {otrok.partner_od_den})")
    else:
        print("Partnerský vztah: ne")
    if getattr(otrok, "je_manzelkou", False):
        print("💍 Manželka")
    print(
        f"Vztah: {otrok.romance_stav} ({otrok.romance_body}/100) | "
        f"Loajalita: {otrok.loajalita} | Důvěra: {otrok.duvera}"
    )
    print(f"\n{CYAN}Přehled postavy{NC}")
    for nazev, hodnota, maximum, barva in (
        ("Zdraví", otrok.hp, otrok.max_hp, GREEN),
        ("Důvěra", otrok.duvera, 100, CYAN),
        ("Loajalita", otrok.loajalita, 100, MAGENTA),
        ("Poslušnost", otrok.poslusnost, 100, YELLOW),
        ("Touha", otrok.touha, 100, MAGENTA),
        ("Strach", otrok.strach, 100, RED),
        ("Romantika", otrok.romance_body, 100, CYAN),
    ):
        print(f"  {nazev:12} {ukazatel(hodnota, maximum, 16, barva)}")
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


def zobraz_graf_statistik(otrok):
    hlavicka(f"Vývoj statistik: {otrok.jmeno}")
    historie = getattr(otrok, "historie_statistik", [])
    if not historie:
        print("Časová řada zatím prázdná. Statistiky se ukládají na konci každého dne.")
        print("Aktuální stav:")
        historie = [{
            "den": 0,
            "duvera": otrok.duvera,
            "loajalita": otrok.loajalita,
            "poslusnost": otrok.poslusnost,
            "touha": otrok.touha,
            "hp": otrok.hp,
        }]
    historie = historie[-14:]
    grafy = (
        ("Důvěra", "duvera", CYAN),
        ("Loajalita", "loajalita", MAGENTA),
        ("Poslušnost", "poslusnost", YELLOW),
        ("Touha", "touha", RED),
        ("Zdraví", "hp", GREEN),
    )
    znaky = "▁▂▃▄▅▆▇█"
    for nazev, klic, barva in grafy:
        hodnoty = [max(0, int(bod.get(klic, 0))) for bod in historie]
        minimum, maximum = min(hodnoty), max(hodnoty)
        if minimum == maximum:
            linka = znaky[3] * len(hodnoty)
        else:
            linka = "".join(
                znaky[round((hodnota - minimum) / (maximum - minimum) * 7)]
                for hodnota in hodnoty
            )
        print(
            f"  {nazev:12} {barva}{linka}{NC} "
            f"{hodnoty[0]} → {hodnoty[-1]}"
        )
    print("  Dny:       " + " ".join(str(bod.get("den", "?")) for bod in historie))


def menu_profily(hra):
    while True:
        clear()
        aktivni = hra.harem.vsechny_aktivni()
        hlavicka("Profily postav v harému")
        if not aktivni:
            tisk_chyba("Nemáš žádné aktivní postavy.")
            input("Enter...")
            return
        for index, otrok in enumerate(aktivni, 1):
            hvezda = "★ " if getattr(otrok, "oblibena", False) else ""
            print(
                f"{index}) {hvezda}{otrok.jmeno} — {max(18, int(otrok.vek))} let, "
                f"{otrok.role}, vztah {otrok.romance_stav}"
            )
        vytiskni_volbu('0', 'Zpět')
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
        aktivni = hra.harem.vsechny_aktivni()
        oblibene = [o for o in aktivni if getattr(o, "oblibena", False)]
        partnerky = [o for o in aktivni if getattr(o, "partnerka", False)]
        manzelky = [o for o in aktivni if getattr(o, "je_manzelkou", False)]

        hlavicka("Harém: péče, vztahy a privilegia")
        print(f"Členky: {hra.harem.pocet()} | Úroveň harému: {getattr(hra.harem, 'harem_level', 1)}")
        if aktivni:
            prumer_duvery = sum(o.duvera for o in aktivni) // len(aktivni)
            prumer_loajality = sum(o.loajalita for o in aktivni) // len(aktivni)
            prumer_zdravi = sum(o.hp for o in aktivni) // len(aktivni)
            print(f"\n{CYAN}Stav harému{NC}")
            for nazev, hodnota, barva in (
                ("Důvěra", prumer_duvery, CYAN),
                ("Loajalita", prumer_loajality, MAGENTA),
                ("Zdraví", prumer_zdravi, GREEN),
            ):
                print(f"  {nazev:10} {ukazatel(hodnota, 100, 18, barva)}")
            pocty_charakteru = Counter(
                normalizuj_charakter(o.charakter) for o in aktivni
            )
            rozdeleni = ", ".join(
                f"{CHARAKTERY[charakter]['nazev']} ×{pocet}"
                for charakter, pocet in pocty_charakteru.most_common(5)
            )
            print(f"  Povahy: {rozdeleni}")
            print(f"\n{YELLOW}Členky harému{NC}")
            for otrok in aktivni[:8]:
                stav_ikona = "💍" if getattr(otrok, "je_manzelkou", False) else (
                    "♥" if getattr(otrok, "partnerka", False) else " "
                )
                print(
                    f"  {stav_ikona} {otrok.jmeno:<14} "
                    f"{nazev_charakteru(otrok.charakter):<22} "
                    f"♥ {ukazatel(otrok.duvera, 100, 10, CYAN)}"
                )
            if len(aktivni) > 8:
                print(f"  … a dalších {len(aktivni) - 8} členek")
        if oblibene:
            print(f"★ Oblíbenkyně: {oblibene[0].jmeno}")
        else:
            print("★ Oblíbenkyně: (zatím žádná)")
        if partnerky:
            print(f"♥ Partnerky: {', '.join(o.jmeno for o in partnerky)}")
        if manzelky:
            print(f"💍 Manželka: {', '.join(o.jmeno for o in manzelky)}")
        print()
        vytiskni_volbu('1', 'Osobní rozhovor, osud, odměny a oblíbenkyně')
        vytiskni_volbu('2', 'Společná porada')
        vytiskni_volbu('3', 'Profily postav a historie voleb')
        vytiskni_volbu('4', 'Rychle jmenovat / změnit oblíbenkyni')
        vytiskni_volbu('5', 'Odměny pro vybranou otrokyni')
        vytiskni_volbu('6', 'Osobní deník vybrané členky')
        vytiskni_volbu('7', 'Graf vývoje statistik vybrané členky')
        vytiskni_volbu('0', 'Zpět')
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
        elif volba == "4":
            otrok = _vyber_otrokyni(hra)
            if otrok:
                nastav_oblibenou(hra, otrok)
                input("Enter...")
        elif volba == "5":
            otrok = _vyber_otrokyni(hra)
            if otrok:
                menu_odmen(otrok, hra.hrac)
                input("Enter...")
        elif volba == "6":
            otrok = _vyber_otrokyni(hra)
            if otrok:
                from game.osobni_pribehy import zobraz_denik_postavy
                zobraz_denik_postavy(otrok)
                input("Enter...")
        elif volba == "7":
            otrok = _vyber_otrokyni(hra)
            if otrok:
                zobraz_graf_statistik(otrok)
                input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
