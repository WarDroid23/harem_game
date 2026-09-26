# game/budovy.py
import random
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info, vytiskni_volbu, hlavicka
from config import GOLD, GREEN, RED, CYAN, MAGENTA, YELLOW, WHITE, NC, BOLD, DIM
from models.fortress import PEVNOSTNI_BUDOVY
from data.charaktery import CHARAKTERY


def vylepsit_budovu(hrac, harem, typ):
    """Vylepší budovu harému bez menu, pokud je typ a cena dostupná."""
    if harem is None or not hasattr(harem, "budovy"):
        return False
    budova = harem.budovy.get(typ)
    if budova is None or hrac.gold < budova.cena:
        return False
    cena = budova.cena
    hrac.gold -= cena
    budova.vylepsi()
    if hasattr(hrac, "_hra_achievementy"):
        hrac._hra_achievementy.zaznamenej("stavba")
    tisk_ok(f"Budova {typ} vylepšena na úroveň {budova.uroven}.")
    return True


def _rozbal_kontext(arg0, arg1=None):
    if hasattr(arg0, "hrac") and hasattr(arg0, "pevnost"):
        return arg0, arg0.hrac, arg0.harem, arg0.pevnost
    # Fallback pro staré volání (hrac, harem)
    hrac = arg0
    harem = arg1
    hra = getattr(hrac, "_hra_ref", None)
    pevnost = getattr(hra, "pevnost", None)
    return hra, hrac, harem, pevnost


def vystavba_budov(hra, hrac, pevnost):
    while True:
        clear()
        hlavicka("Výstavba & Rozvoj budov dominia")
        print(f"\n{CYAN}Suroviny panství:{NC} {GOLD}🪙 {hrac.gold}{NC} | "
              f"{GREEN}🪵 {pevnost.drevo}{NC} | "
              f"{WHITE}🪨 {pevnost.kamen}{NC} | "
              f"{CYAN}⚒️ {pevnost.zelezo}{NC} | "
              f"{YELLOW}🌾 {pevnost.zasoby}{NC} | "
              f"{MAGENTA}🔮 {pevnost.krystaly}{NC}\n")

        kategorie_map = {
            "suroviny": ("⛏️ HOSPODÁŘSTVÍ & TĚŽBA", GREEN),
            "obrana": ("🛡️ VOJENSTVÍ & OBRANA", RED),
            "vyroba": ("🔨 ŘEMESLA & VÝROBA", YELLOW),
            "mystika": ("🔮 MYSTIKA & VÝZKUM", MAGENTA),
            "harem": ("👑 HARÉM & REGENERACE", CYAN),
        }

        seznam = list(PEVNOSTNI_BUDOVY.items())
        posledni_kat = None

        for i, (klic, info) in enumerate(seznam, 1):
            kat = info.get("kategorie", "suroviny")
            if kat != posledni_kat:
                kat_nazev, kat_barva = kategorie_map.get(kat, ("DALŠÍ STAVBY", WHITE))
                print(f"\n{kat_barva}{BOLD}── {kat_nazev} ──{NC}")
                posledni_kat = kat

            lvl = pevnost.budovy.get(klic, 0)
            ceny = pevnost.cena_vylepseni(klic)
            dohled = pevnost.pracovnici.get(klic)
            dohled_txt = f" {MAGENTA}[Dohlíží: {dohled}]{NC}" if dohled else ""

            cena_str = f"{ceny['zlato']} 🪙, {ceny['drevo']} 🪵, {ceny['kamen']} 🪨, {ceny['zelezo']} ⚒️"
            print(f"  {BOLD}{WHITE}{i:2}){NC} {BOLD}{info['nazev']}{NC} (Úroveň {lvl}){dohled_txt}")
            print(f"      {DIM}{info['popis']}{NC}")
            print(f"      {GOLD}Cena vylepšení: {cena_str}{NC}")

        print(f"\n  {BOLD}{MAGENTA}U){NC} 🏰 Vylepšit hlavní citadela dominia ({pevnost.uroven} -> {pevnost.uroven + 1}): {GOLD}{400 * pevnost.uroven} 🪙{NC}")
        vytiskni_volbu('0', 'Zpět', RED)

        try:
            volba = input("> ").strip().lower()
            if volba == "0":
                return
            if volba == "u":
                cena_cit = 400 * pevnost.uroven
                if hrac.gold >= cena_cit:
                    hrac.gold -= cena_cit
                    pevnost.uroven += 1
                    tisk_ok(f"Citadela panství povýšena na úroveň {pevnost.uroven}! Kapacita a prestiž vzrostla.")
                else:
                    tisk_chyba("Nedostatek zlata na vylepšení citadely.")
                input("Enter...")
                continue

            idx = int(volba) - 1
            if 0 <= idx < len(seznam):
                klic_budovy, data_b = seznam[idx]
                uspech, zprava = pevnost.vylepsi_budovu(klic_budovy, hrac)
                if uspech:
                    tisk_ok(zprava)
                    if hra and hasattr(hra, "achievementy"):
                        hra.achievementy.zaznamenej("stavba")
                    if hra and hasattr(hra, "kronika"):
                        from game.kronika import zaznamenej
                        zaznamenej(hra, f"V dominia vylepšena budova {data_b['nazev']} na úroveň {pevnost.budovy[klic_budovy]}.")
                else:
                    tisk_chyba(zprava)
                input("Enter...")
            else:
                tisk_chyba("Neplatné číslo budovy.")
                input("Enter...")
        except ValueError:
            tisk_chyba("Zadej číslo.")
            input("Enter...")


def priradit_pracovnice(hra, hrac, harem, pevnost):
    while True:
        clear()
        hlavicka("Přiřazení otrokyň do budov dominia (Dohlížitelky)")
        print(f"\n{MAGENTA}Dívky jmenované dohlížitelkami budov radikálně zvyšují produkci a odemykají unikátní bonusy!{NC}\n")

        aktivni = harem.vsechny_aktivni()
        prirazene = set(pevnost.pracovnici.values())

        print(f"{YELLOW}--- Aktuální rozdělení dohlížitelek ---{NC}")
        for klic, jmeno in pevnost.pracovnici.items():
            b_nazev = PEVNOSTNI_BUDOVY.get(klic, {}).get("nazev", klic)
            print(f"  • {BOLD}{b_nazev}{NC}: {CYAN}★ {jmeno}{NC}")

        print(f"\n{GREEN}1) Jmenovat dohlížitelku budovy")
        print(f"{CYAN}2) Odvolat dívku z budovy")
        print(f"{RED}0) Zpět{NC}")

        try:
            v = input("> ").strip()
            if v == "0":
                return
            if v == "1":
                volne_divky = [o for o in aktivni if o.jmeno not in prirazene and not o.na_najmu and not getattr(o, "v_nevestinci", False)]
                if not volne_divky:
                    tisk_chyba("Nemáš žádné volné otrokyně (všechny již pracují, jsou v nevěstinci nebo na nájmu).")
                    input("Enter...")
                    continue

                clear()
                hlavicka("Výběr budovy k obsazení")
                seznam_budov = [(k, v) for k, v in PEVNOSTNI_BUDOVY.items() if pevnost.budovy.get(k, 0) > 0]
                if not seznam_budov:
                    tisk_chyba("Zatím nemáš postavené žádné budovy! Nejprve budovu postav.")
                    input("Enter...")
                    continue

                for i, (klic, info) in enumerate(seznam_budov, 1):
                    aktualni = pevnost.pracovnici.get(klic, "nikdo")
                    print(f"  {BOLD}{i}){NC} {info['nazev']} (Nyní dohlíží: {CYAN}{aktualni}{NC})")
                vytiskni_volbu('0', 'Zpět', RED)

                vyber_b = input("> ").strip()
                if vyber_b == "0":
                    continue
                idx_b = int(vyber_b) - 1
                if not (0 <= idx_b < len(seznam_budov)):
                    continue
                vybrany_klic, data_b = seznam_budov[idx_b]

                clear()
                hlavicka(f"Výběr dohlížitelky pro: {data_b['nazev']}")
                for j, o in enumerate(volne_divky, 1):
                    char = CHARAKTERY.get(o.charakter, {}).get("nazev", o.charakter)
                    doporuceni = ""
                    if vybrany_klic == "kasarna" and o.charakter in ("amazonka", "padla_paladinka"):
                        doporuceni = f" {GREEN}★ Ideální velitelka!{NC}"
                    elif vybrany_klic in ("dul", "dilna") and o.charakter == "zlodejka":
                        doporuceni = f" {GOLD}★ Zlatonosný talent!{NC}"
                    elif vybrany_klic == "oltar_stinu" and o.charakter in ("knezka_temnoty", "carodejka", "sukuba_hybrid"):
                        doporuceni = f" {MAGENTA}★ Mystická synergie!{NC}"
                    elif vybrany_klic == "statek" and o.charakter == "subka":
                        doporuceni = f" {CYAN}★ Pracovitá podpora{NC}"
                    print(f"  {BOLD}{j}){NC} {o.jmeno} [{char}]{doporuceni}")
                vytiskni_volbu('0', 'Zpět', RED)

                vyber_d = input("> ").strip()
                if vyber_d == "0":
                    continue
                idx_d = int(vyber_d) - 1
                if 0 <= idx_d < len(volne_divky):
                    vybrana_d = volne_divky[idx_d]
                    pevnost.pracovnici[vybrany_klic] = vybrana_d.jmeno
                    tisk_ok(f"{vybrana_d.jmeno} byla jmenována dohlížitelkou budovy {data_b['nazev']}!")
                    input("Enter...")

            elif v == "2":
                if not pevnost.pracovnici:
                    tisk_info("Žádné budovy nemají přiřazenou dohlížitelku.")
                    input("Enter...")
                    continue
                obsazene = list(pevnost.pracovnici.items())
                for i, (klic, jmeno) in enumerate(obsazene, 1):
                    b_nazev = PEVNOSTNI_BUDOVY.get(klic, {}).get("nazev", klic)
                    print(f"  {i}) {b_nazev}: {jmeno}")
                vytiskni_volbu('0', 'Zpět', RED)
                vyber = input("> ").strip()
                if vyber == "0":
                    continue
                idx = int(vyber) - 1
                if 0 <= idx < len(obsazene):
                    k_odstraneni, jm = obsazene[idx]
                    del pevnost.pracovnici[k_odstraneni]
                    tisk_ok(f"{jm} byla uvolněna z dohledu.")
                    input("Enter...")
        except ValueError:
            tisk_chyba("Zadej číslo.")
            input("Enter...")


def sprava_dani(hrac, pevnost):
    clear()
    hlavicka("Hospodářská & Daňová politika panství")
    print(f"\n{MAGENTA}Nastav výši berně a způsob vlády nad poddanými tvého dominia:{NC}\n")

    politiky = [
        ("laskava", "Laskavá správa (Nízké daně)", "+30–60 🪙/den, +1 reputace města denně, +2 loajalita dívek", GREEN),
        ("vyvazena", "Vyvážená správa (Mírné berně)", "+90–160 🪙/den, stabilní vztahy a běžná spokojenost", GOLD),
        ("kruta", "Kruté vykořisťování (Drakonické desátky)", "+230–370 🪙/den, -1 reputace města, +2% vliv inkvizice!", RED),
    ]

    for klic, nazev, popis, barva in politiky:
        aktivni = " ← AKTIVNÍ" if pevnost.danova_politika == klic else ""
        print(f"  {barva}{BOLD}• {nazev}{aktivni}{NC}")
        print(f"      {DIM}{popis}{NC}\n")

    vytiskni_volbu('1', 'Zvolit laskavou správu', GREEN)
    vytiskni_volbu('2', 'Zvolit vyváženou správu', GOLD)
    vytiskni_volbu('3', 'Zvolit kruté vykořisťování', RED)
    vytiskni_volbu('0', 'Zpět', WHITE)

    try:
        volba = input("> ").strip()
        if volba == "1":
            pevnost.danova_politika = "laskava"
            tisk_ok("Nastavena laskavá správa. Lidé ti žehnají a dívky cítí bezpečí.")
            input("Enter...")
        elif volba == "2":
            pevnost.danova_politika = "vyvazena"
            tisk_ok("Nastavena vyvážená správa. Zlatý střed pro hospodářství.")
            input("Enter...")
        elif volba == "3":
            pevnost.danova_politika = "kruta"
            tisk_ok("Drakonické desátky uvaleny! Tvé truhly budou přetékat zlatem, ale lid skřípe zuby.")
            input("Enter...")
    except ValueError:
        pass


def trznice_surovin(hrac, pevnost):
    while True:
        clear()
        hlavicka("Tržnice surovin dominia")
        print(f"\n{CYAN}Tvé suroviny:{NC} {GOLD}🪙 {hrac.gold}{NC} | "
              f"{GREEN}🪵 {pevnost.drevo}{NC} | "
              f"{WHITE}🪨 {pevnost.kamen}{NC} | "
              f"{CYAN}⚒️ {pevnost.zelezo}{NC} | "
              f"{YELLOW}🌾 {pevnost.zasoby}{NC} | "
              f"{MAGENTA}🔮 {pevnost.krystaly}{NC}\n")

        print(f"{YELLOW}Nakupuj chybějící materiál nebo prodávej přebytky kupcům:{NC}\n")
        print("  1) Koupit 50 dřeva (60 🪙)")
        print("  2) Koupit 40 kamene (65 🪙)")
        print("  3) Koupit 25 železa (75 🪙)")
        print("  4) Koupit 50 zásob jídla (50 🪙)")
        print("  5) Koupit 10 temných krystalů (120 🪙)")
        print(f"{DIM}──────────────────────────────────────────{NC}")
        print("  6) Prodat 50 dřeva (+40 🪙)")
        print("  7) Prodat 40 kamene (+45 🪙)")
        print("  8) Prodat 25 železa (+55 🪙)")
        print("  9) Prodat 50 zásob jídla (+35 🪙)")
        vytiskni_volbu('0', 'Zpět', RED)

        try:
            v = input("> ").strip()
            if v == "0":
                return
            if v == "1":
                if hrac.gold >= 60:
                    hrac.gold -= 60
                    pevnost.drevo += 50
                    tisk_ok("Zakoupeno 50 dřeva.")
                else:
                    tisk_chyba("Nedostatek zlata.")
                input("Enter...")
            elif v == "2":
                if hrac.gold >= 65:
                    hrac.gold -= 65
                    pevnost.kamen += 40
                    tisk_ok("Zakoupeno 40 kamene.")
                else:
                    tisk_chyba("Nedostatek zlata.")
                input("Enter...")
            elif v == "3":
                if hrac.gold >= 75:
                    hrac.gold -= 75
                    pevnost.zelezo += 25
                    tisk_ok("Zakoupeno 25 železa.")
                else:
                    tisk_chyba("Nedostatek zlata.")
                input("Enter...")
            elif v == "4":
                if hrac.gold >= 50:
                    hrac.gold -= 50
                    pevnost.zasoby += 50
                    tisk_ok("Zakoupeno 50 zásob jídla.")
                else:
                    tisk_chyba("Nedostatek zlata.")
                input("Enter...")
            elif v == "5":
                if hrac.gold >= 120:
                    hrac.gold -= 120
                    pevnost.krystaly += 10
                    tisk_ok("Zakoupeno 10 temných krystalů.")
                else:
                    tisk_chyba("Nedostatek zlata.")
                input("Enter...")
            elif v == "6":
                if pevnost.drevo >= 50:
                    pevnost.drevo -= 50
                    hrac.gold += 40
                    tisk_ok("Prodáno 50 dřeva za +40 🪙.")
                else:
                    tisk_chyba("Nemáš 50 dřeva.")
                input("Enter...")
            elif v == "7":
                if pevnost.kamen >= 40:
                    pevnost.kamen -= 40
                    hrac.gold += 45
                    tisk_ok("Prodáno 40 kamene za +45 🪙.")
                else:
                    tisk_chyba("Nemáš 40 kamene.")
                input("Enter...")
            elif v == "8":
                if pevnost.zelezo >= 25:
                    pevnost.zelezo -= 25
                    hrac.gold += 55
                    tisk_ok("Prodáno 25 železa za +55 🪙.")
                else:
                    tisk_chyba("Nemáš 25 železa.")
                input("Enter...")
            elif v == "9":
                if pevnost.zasoby >= 50:
                    pevnost.zasoby -= 50
                    hrac.gold += 35
                    tisk_ok("Prodáno 50 zásob jídla za +35 🪙.")
                else:
                    tisk_chyba("Nemáš 50 zásob jídla.")
                input("Enter...")
        except ValueError:
            pass


def obchodni_karavany(hra, hrac, pevnost):
    clear()
    hlavicka("Obchodní karavany dominia")
    print(f"\n{MAGENTA}Vyprav ozbrojenou obchodní karavanu do okolních měst za velkým ziskem:{NC}\n")

    trasy = [
        ("vesnice", "Zemědělské osady v údolí", 80, "Nízké", "Zisk: 150–220 🪙 + 30 dřeva"),
        ("pristav", "Přímořský cechovní přístav", 160, "Střední", "Zisk: 350–520 🪙 + 25 železa"),
        ("velkomesto", "Císařské velkoměsto Solaria", 300, "Vysoké", "Zisk: 750–1100 🪙 + 15 krystalů a výbava"),
    ]

    for i, (klic, nazev, naklad, riziko, zisk_txt) in enumerate(trasy, 1):
        print(f"  {BOLD}{CYAN}{i}) {nazev}{NC}")
        print(f"      Investice: {GOLD}{naklad} 🪙{NC} | Riziko přepadení: {YELLOW}{riziko}{NC}")
        print(f"      {GREEN}{zisk_txt}{NC}\n")
    vytiskni_volbu('0', 'Zpět', RED)

    try:
        vyber = input("> ").strip()
        if vyber == "0":
            return
        idx = int(vyber) - 1
        if 0 <= idx < len(trasy):
            klic, nazev, naklad, riziko, _ = trasy[idx]
            if hrac.gold < naklad:
                tisk_chyba("Nemáš dostatek zlata na vypravení karavany.")
                input("Enter...")
                return

            hrac.gold -= naklad
            tisk_info(f"Karavana vyrazila na cestu do: {nazev}...")

            # Simulace cesty a obrany
            obrana_bonus = pevnost.budovy.get("kasarna", 0) * 8 + (getattr(hra.mafie, "vojaci", 0) * 2 if hasattr(hra, "mafie") else 0)
            prepadeni = (random.random() < 0.25) if klic == "vesnice" else (random.random() < 0.4) if klic == "pristav" else (random.random() < 0.55)

            if prepadeni:
                tisk_chyba("⚠ Karavana byla na horském průsmyku přepadena bandity a inkvizičními žoldnéři!")
                if obrana_bonus >= random.randint(15, 45):
                    tisk_ok("✔ Stráže z tvých kasáren a mafie útok hrdinně odrazily!")
                    prepadeni = False
                else:
                    tisk_chyba("✖ Karavana utrpěla ztráty a musela část nákladu odhodit.")

            if not prepadeni:
                if klic == "vesnice":
                    zisk_zlato = random.randint(160, 240)
                    pevnost.drevo += 30
                    tisk_ok(f"✔ Karavana se vrátila! Zisk: +{zisk_zlato} 🪙 a +30 🪵 dřeva.")
                elif klic == "pristav":
                    zisk_zlato = random.randint(380, 560)
                    pevnost.zelezo += 25
                    tisk_ok(f"✔ Karavana úspěšně dovezla zámořské zboží! Zisk: +{zisk_zlato} 🪙 a +25 ⚒️ železa.")
                else:
                    zisk_zlato = random.randint(800, 1150)
                    pevnost.krystaly += 15
                    tisk_ok(f"✔ Karavana z císařského velkoměsta přivezla poklady! Zisk: +{zisk_zlato} 🪙 a +15 🔮 krystalů.")
                hrac.gold += zisk_zlato
                if hasattr(hra, "kronika"):
                    from game.kronika import zaznamenej
                    zaznamenej(hra, f"Obchodní karavana se vrátila z {nazev} (+{zisk_zlato} zl).")
            else:
                zachraneno = random.randint(20, naklad // 2)
                hrac.gold += zachraneno
                tisk_info(f"Podařilo se zachránit pouze zbytek nákladu v hodnotě {zachraneno} 🪙.")

            input("Enter...")
    except ValueError:
        pass


def zkouska_obrany(hra, hrac, pevnost):
    clear()
    hlavicka("Zkouška obrany pevnosti & Nájezdy")
    obrana = pevnost.celkova_obrana_pevnosti()
    vojaci = getattr(hra.mafie, "vojaci", 0) if hasattr(hra, "mafie") else 0
    obrana_celkem = obrana + vojaci * 3

    print(f"\n{RED}{BOLD}Pevnostní obrana:{NC} {obrana_celkem} bodů (Hradby: {pevnost.budovy.get('hradby', 0)*35}, Věže: {pevnost.budovy.get('strazni_vez', 0)*25}, Kasárna: {pevnost.budovy.get('kasarna', 0)*20}, Vojáci: {vojaci*3})\n")
    print("Můžeš simulovat střet s nepřátelskými nájezdníky:")
    vytiskni_volbu('1', 'Odmítnout útok loupeživých banditů (nízké riziko)', GREEN)
    vytiskni_volbu('2', 'Odrazit kárnou výpravu inkvizice (střední riziko)', YELLOW)
    vytiskni_volbu('3', 'Čelit obléhání rivalským syndikátem a křižáky (extrémní riziko)', RED)
    vytiskni_volbu('0', 'Zpět', WHITE)

    try:
        vyber = input("> ").strip()
        if vyber == "0":
            return
        cile = {
            "1": {"nazev": "Loupeživí bandité", "sila": 45, "zlato": 180, "suroviny": 25},
            "2": {"nazev": "Kárná výprava inkvizice", "sila": 90, "zlato": 350, "suroviny": 40},
            "3": {"nazev": "Obléhací armáda syndikátu", "sila": 160, "zlato": 650, "suroviny": 80},
        }
        if vyber not in cile:
            return

        cil = cile[vyber]
        print(f"\nNájezdníci: {BOLD}{cil['nazev']}{NC} (Síla útoku: ~{cil['sila']})")
        print(f"Obrana tvé pevnosti: {BOLD}{obrana_celkem}{NC} bodů...")

        if obrana_celkem >= cil["sila"]:
            rozdil = obrana_celkem - cil["sila"]
            zisk_z = cil["zlato"] + rozdil * 2
            pevnost.kamen += cil["suroviny"]
            pevnost.zelezo += cil["suroviny"] // 2
            hrac.gold += zisk_z
            tisk_ok(f"✔ DRTIVÉ VÍTĚZSTVÍ! Hradby a balisty rozstřílely nájezdníky na kusy.")
            tisk_ok(f"Kořist z bojiště: +{zisk_z} 🪙, +{cil['suroviny']} kamene a +{cil['suroviny']//2} železa!")
            if hasattr(hra, "kronika"):
                from game.kronika import zaznamenej
                zaznamenej(hra, f"Obrana pevnosti: odražen nájezd {cil['nazev']} (+{zisk_z} zl).")
        else:
            skoda_zlato = min(hrac.gold, random.randint(60, 150))
            hrac.gold -= skoda_zlato
            pevnost.zasoby = max(0, pevnost.zasoby - 20)
            tisk_chyba(f"✖ PROLOMENÍ OPEVNĚNÍ! Nájezdníci pronikli na nádvoří a vyplenili sýpky.")
            tisk_chyba(f"Ztráta: −{skoda_zlato} 🪙 a −20 zásob jídla. Zesil hradby a věže!")
        input("Enter...")
    except ValueError:
        pass


def spravovat_budovy(arg0, arg1=None):
    """Hlavní strategické rozhraní budovatelské strategie panství."""
    hra, hrac, harem, pevnost = _rozbal_kontext(arg0, arg1)
    if pevnost is None:
        tisk_chyba("Systém pevnosti není dostupný.")
        return

    while True:
        clear()
        hlavicka(f"🏰 STRATEGIE DOMINIA & ROZVOJ PANSTVÍ 🏰")

        obrana_bodu = pevnost.celkova_obrana_pevnosti()
        print(f"\n{GOLD}Citadela panství:{NC} Úroveň {pevnost.uroven} | {RED}Obranná síla:{NC} {obrana_bodu} bodů | {CYAN}Daňová správa:{NC} {pevnost.danova_politika.upper()}")
        print(f"{BOLD}Suroviny skladu:{NC} {GOLD}🪙 {hrac.gold} zlata{NC} | {GREEN}🪵 {pevnost.drevo} dřeva{NC} | {WHITE}🪨 {pevnost.kamen} kamene{NC}")
        print(f"                 {CYAN}⚒️ {pevnost.zelezo} železa{NC} | {YELLOW}🌾 {pevnost.zasoby} zásob jídla{NC} | {MAGENTA}🔮 {pevnost.krystaly} krystalů{NC}\n")

        print(f"{YELLOW}--- Přehled sektorů panství ---{NC}")
        print(f"  • {GREEN}Hospodářství:{NC} Pila úr.{pevnost.budovy.get('pila',0)} | Kamenolom úr.{pevnost.budovy.get('kamenolom',0)} | Důl úr.{pevnost.budovy.get('dul',0)} | Statek úr.{pevnost.budovy.get('statek',0)}")
        print(f"  • {RED}Vojenství:{NC} Hradby úr.{pevnost.budovy.get('hradby',0)} | Věže úr.{pevnost.budovy.get('strazni_vez',0)} | Kasárna úr.{pevnost.budovy.get('kasarna',0)} | Kovárna úr.{pevnost.budovy.get('kovarna',0)}")
        print(f"  • {MAGENTA}Mystika & Harém:{NC} Oltář úr.{pevnost.budovy.get('oltar_stinu',0)} | Archiv úr.{pevnost.budovy.get('archiv',0)} | Zahrada úr.{pevnost.budovy.get('zahrada',0)} | Lázně úr.{pevnost.budovy.get('lazne_dominia',0)}")
        if pevnost.pracovnici:
            prac_txt = ", ".join(f"{PEVNOSTNI_BUDOVY.get(k,{}).get('nazev',k)}: {v}" for k, v in pevnost.pracovnici.items())
            print(f"  • {CYAN}Dohlížitelky:{NC} {prac_txt}")

        print(f"\n{GOLD}{BOLD}╔════ 🏗️ VÝSTAVBA & ROZVOJ ═════════════════╗{NC}   {MAGENTA}{BOLD}╔════ ⚖️ HOSPODÁŘSTVÍ & STRATEGIE ═════════╗{NC}")
        print(f"║ {GREEN} 1){NC} 🔨 Výstavba & vylepšování budov      ║   ║ {YELLOW} 3){NC} ⚖️ Hospodářská & daňová politika   ║")
        print(f"║ {CYAN} 2){NC} 👷 Dohlížitelky (přiřazení otrokyň)  ║   ║ {GREEN} 4){NC} 🛒 Tržnice surovin (nákup / prodej)║")
        print(f"║ {RED} 6){NC} 🛡️ Zkouška obrany & nájezdy          ║   ║ {GOLD} 5){NC} 🐫 Vypravit obchodní karavanu      ║")
        print(f"║                                          ║   ║ {WHITE} 0){NC} 🚪 Odejít zpět do dominia          ║")
        print(f"{GOLD}{BOLD}╚════════════════════════════════════════╝{NC}   {MAGENTA}{BOLD}╚════════════════════════════════════════╝{NC}")

        try:
            volba = input("> ").strip()
        except EOFError:
            return

        if volba == "0":
            return
        elif volba == "1":
            vystavba_budov(hra, hrac, pevnost)
        elif volba == "2":
            priradit_pracovnice(hra, hrac, harem, pevnost)
        elif volba == "3":
            sprava_dani(hrac, pevnost)
        elif volba == "4":
            trznice_surovin(hrac, pevnost)
        elif volba == "5":
            obchodni_karavany(hra, hrac, pevnost)
        elif volba == "6":
            zkouska_obrany(hra, hrac, pevnost)
        else:
            tisk_chyba("Neplatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return
