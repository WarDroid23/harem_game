# game/nevestinec.py
import random
from config import GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, GOLD, NC, BOLD
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from data.charaktery import CHARAKTERY

CENA_OTEVRENI = 300

def otevrit_nevestinec(hra) -> bool:
    clear()
    print(f"{MAGENTA}{BOLD}=== Založení nevěstince v Červené čtvrti ==={NC}\n")
    print("V rušných uličkách Červené čtvrti je k mání stará honosná budova.")
    print("Můžeš ji zrenovovat a vybudovat z ní nejvyhledávanější nevěstinec ve městě.")
    print(f"Cena licence a renovace: {GOLD}{CENA_OTEVRENI} 🪙{NC}")
    print(f"Tvé zlato: {hra.hrac.gold} 🪙\n")
    print("1) Koupit a otevřít nevěstinec")
    print("0) Zpět")

    try:
        volba = input("> ").strip()
    except EOFError:
        return False

    if volba == "1":
        if hra.hrac.gold >= CENA_OTEVRENI:
            hra.hrac.gold -= CENA_OTEVRENI
            hra.nevestinec.otevreno = True
            tisk_ok(f"Gratulujeme! Založil jsi nevěstinec '{hra.nevestinec.nazev}'!")
            if hasattr(hra, "kronika"):
                from game.kronika import zaznamenej
                zaznamenej(hra, f"Otevřen nevěstinec '{hra.nevestinec.nazev}' v Červené čtvrti.")
            if "cech_kurtizan" in hra.frakce.frakce:
                hra.frakce.frakce["cech_kurtizan"].zmenit(15)
            return True
        else:
            tisk_chyba("Nemáš dostatek zlata.")
    return False

def vypocti_cenu_prodeje(otrok) -> int:
    zaklad = 150 + otrok.loajalita * 3 + otrok.poslusnost * 2 + otrok.submisivita * 2
    if getattr(otrok, "charakter", "") == "kurtizana":
        zaklad = int(zaklad * 1.5)
    elif getattr(otrok, "charakter", "") == "slechticna":
        zaklad = int(zaklad * 1.4)
    zkazeny_bonus = getattr(otrok, "faze_zkazenosti", 0) * 80
    cena = max(100, zaklad + zkazeny_bonus)
    return cena

def prodat_otrokyni(hra):
    clear()
    print(f"{GOLD}{BOLD}=== Trvalý prodej otrokyně mecenášům ==={NC}\n")
    aktivni = hra.harem.vsechny_aktivni()
    if not aktivni:
        tisk_chyba("Nemáš žádné otrokyně v harému.")
        input("Enter...")
        return

    # Nelze prodat manželku ani partnerku
    k_prodeji = [o for o in aktivni if not getattr(o, "je_manzelkou", False) and not getattr(o, "partnerka", False)]
    if not k_prodeji:
        tisk_chyba("Všechny tvé otrokyně jsou tvé partnerky či manželky – ty prodat nelze!")
        input("Enter...")
        return

    print("Bohatí šlechtici a mecenáši z Paláce i Červené čtvrti mají zájem o koupi:\n")
    for i, o in enumerate(k_prodeji, 1):
        cena = vypocti_cenu_prodeje(o)
        char = CHARAKTERY.get(o.charakter, {}).get("nazev", o.charakter)
        v_nev = " [V nevěstinci]" if getattr(o, "v_nevestinci", False) else ""
        print(f"{i}) {o.jmeno} ({char}, poslušnost {o.poslusnost}%, zkaženost fáze {o.faze_zkazenosti}){v_nev} -> Nabídka: {GOLD}{cena} 🪙{NC}")
    print("0) Zpět")

    try:
        volba = input("> ").strip()
        if volba == "0":
            return
        idx = int(volba) - 1
        if 0 <= idx < len(k_prodeji):
            vybrana = k_prodeji[idx]
            cena = vypocti_cenu_prodeje(vybrana)
            print(f"\nOpravdu chceš prodat {vybrana.jmeno} za {cena} 🪙? Tato akce je trvalá! (a/n)")
            potvrd = input("> ").strip().lower()
            if potvrd in ("a", "ano", "y"):
                hra.hrac.gold += cena
                hra.harem.odstranit(vybrana.jmeno)
                tisk_ok(f"Otrokyně {vybrana.jmeno} byla prodána bohatému šlechtici za {cena} 🪙!")
                if hasattr(hra, "kronika"):
                    from game.kronika import zaznamenej
                    zaznamenej(hra, f"Otrokyně {vybrana.jmeno} byla prodána mecenáši za {cena} zlata.")
                if "podsveti" in hra.frakce.frakce:
                    hra.frakce.frakce["podsveti"].zmenit(5)
                input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")

def pridat_divku_do_nevestince(hra):
    aktivni = hra.harem.vsechny_aktivni()
    v_nevestinci = [o for o in aktivni if getattr(o, "v_nevestinci", False)]
    if len(v_nevestinci) >= hra.nevestinec.pocet_pokoju:
        tisk_chyba(f"Všechny pokoje ({hra.nevestinec.pocet_pokoju}) jsou již obsazeny. Rozšiř budovu!")
        input("Enter...")
        return

    volne = [o for o in aktivni if not getattr(o, "v_nevestinci", False) and not getattr(o, "na_najmu", False)]
    if not volne:
        tisk_chyba("Nemáš volné otrokyně pro zařazení do nevěstince.")
        input("Enter...")
        return

    clear()
    print(f"{MAGENTA}{BOLD}=== Zařazení otrokyně do pokoje nevěstince ==={NC}\n")
    for i, o in enumerate(volne, 1):
        char = CHARAKTERY.get(o.charakter, {}).get("nazev", o.charakter)
        bonus = " ★ (+40% zisk)" if o.charakter == "kurtizana" else ""
        print(f"{i}) {o.jmeno} [{char}{bonus}] (touha: {o.touha}, loajalita: {o.loajalita}%)")
    print("0) Zpět")

    try:
        idx = int(input("> ")) - 1
        if 0 <= idx < len(volne):
            vybrana = volne[idx]
            vybrana.v_nevestinci = True
            tisk_ok(f"{vybrana.jmeno} byla ubytována v luxusním pokoji nevěstince a obsluhuje hosty!")
            input("Enter...")
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")

def odebrat_divku_z_nevestince(hra):
    aktivni = hra.harem.vsechny_aktivni()
    v_nevestinci = [o for o in aktivni if getattr(o, "v_nevestinci", False)]
    if not v_nevestinci:
        tisk_chyba("V nevěstinci právě nepracuje žádná dívka.")
        input("Enter...")
        return

    clear()
    print(f"{CYAN}{BOLD}=== Stažení otrokyně zpět do Černé pevnosti ==={NC}\n")
    for i, o in enumerate(v_nevestinci, 1):
        print(f"{i}) {o.jmeno}")
    print("0) Zpět")

    try:
        idx = int(input("> ")) - 1
        if 0 <= idx < len(v_nevestinci):
            vybrana = v_nevestinci[idx]
            vybrana.v_nevestinci = False
            tisk_ok(f"{vybrana.jmeno} se vrací do Černé pevnosti.")
            input("Enter...")
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")

def vylepsi_nevestinec(hra):
    clear()
    nev = hra.nevestinec
    print(f"{GOLD}{BOLD}=== Rozvoj nevěstince '{nev.nazev}' ==={NC}\n")
    cena_pokoje = nev.cena_rozsireni_pokoju()
    cena_luxus = nev.cena_luxusu()
    cena_guard = nev.cena_ochranky()

    print(f"1) Přistavět další pokoj ({nev.pocet_pokoju} -> {nev.pocet_pokoju + 1}): {GOLD}{cena_pokoje} 🪙{NC}")
    print(f"2) Zvýšit luxus a výzdobu (úroveň {nev.uroven_luxusu} -> {nev.uroven_luxusu + 1}): {GOLD}{cena_luxus} 🪙{NC} (zvyšuje tržby o 20%)")
    print(f"3) Najmout vyhazovače a ochranku (úroveň {nev.ochranka} -> {nev.ochranka + 1}): {GOLD}{cena_guard} 🪙{NC} (chrání před nájezdy a opilci)")
    print("0) Zpět")

    try:
        v = input("> ").strip()
        if v == "1":
            if hra.hrac.gold >= cena_pokoje:
                hra.hrac.gold -= cena_pokoje
                nev.pocet_pokoju += 1
                tisk_ok(f"Nevěstinec má nyní {nev.pocet_pokoju} pokojů pro dívky!")
            else:
                tisk_chyba("Nedostatek zlata.")
            input("Enter...")
        elif v == "2":
            if hra.hrac.gold >= cena_luxus:
                hra.hrac.gold -= cena_luxus
                nev.uroven_luxusu += 1
                tisk_ok(f"Úroveň luxusu zvýšena na {nev.uroven_luxusu}!")
            else:
                tisk_chyba("Nedostatek zlata.")
            input("Enter...")
        elif v == "3":
            if hra.hrac.gold >= cena_guard:
                hra.hrac.gold -= cena_guard
                nev.ochranka += 1
                tisk_ok(f"Ochranka posílena na úroveň {nev.ochranka}!")
            else:
                tisk_chyba("Nedostatek zlata.")
            input("Enter...")
    except Exception as e:
        tisk_chyba(f"Chyba: {e}")
        input("Enter...")

def menu_nevestinec(hra):
    if not hasattr(hra, "nevestinec"):
        from models.nevestinec import Nevestinec
        hra.nevestinec = Nevestinec()

    if not hra.nevestinec.otevreno:
        if not otevrit_nevestinec(hra):
            return

    while True:
        clear()
        nev = hra.nevestinec
        aktivni = hra.harem.vsechny_aktivni()
        divky_v_nev = [o for o in aktivni if getattr(o, "v_nevestinci", False)]
        odhadovany_zisk = sum(spocitej_denni_vynos_divky(o, nev) for o in divky_v_nev)

        print(f"{MAGENTA}{BOLD}╔══════════════════════════════════════════════════════════╗{NC}")
        print(f"{MAGENTA}{BOLD}║         🏛️  NEVĚSTINEC '{nev.nazev.upper()}'  🏛️           ║{NC}")
        print(f"{MAGENTA}{BOLD}╚══════════════════════════════════════════════════════════╝{NC}\n")

        print(f"{CYAN}Pokoje: {len(divky_v_nev)}/{nev.pocet_pokoju} obsazeno | Luxus: Úroveň {nev.uroven_luxusu} | Ochranka: Úroveň {nev.ochranka}{NC}")
        print(f"{GOLD}Odhadovaný denní příjem: +{odhadovany_zisk} 🪙 | Celkem vyděláno: {nev.celkovy_zisk} 🪙{NC}")
        print(f"{GREEN}Obslouženo mecenášů a hostů: {nev.obslouzeno_zakazniku}{NC}\n")

        print(f"{YELLOW}--- Dívky na pokojích ---{NC}")
        if divky_v_nev:
            for i, d in enumerate(divky_v_nev, 1):
                vynos = spocitej_denni_vynos_divky(d, nev)
                char = CHARAKTERY.get(d.charakter, {}).get("nazev", d.charakter)
                print(f"  {i}. {d.jmeno} [{char}] – Denní tržba: {GOLD}~{vynos} 🪙{NC} | Zkaženost: Fáze {d.faze_zkazenosti}")
        else:
            print("  (Žádná dívka zde zatím nepracuje)")

        print(f"\n{GREEN}1) Přidat dívku na pokoj{NC}")
        print(f"{CYAN}2) Odebrat dívku zpět do harému{NC}")
        print(f"{GOLD}3) Prodat otrokyni mecenáši (trvalý zisk){NC}")
        print(f"{MAGENTA}4) Vylepšit nevěstinec (pokoje, luxus, ochranka){NC}")
        print(f"{RED}0) Odejít zpět{NC}")

        try:
            volba = input("> ").strip()
        except EOFError:
            return

        if volba == "0":
            return
        elif volba == "1":
            pridat_divku_do_nevestince(hra)
        elif volba == "2":
            odebrat_divku_z_nevestince(hra)
        elif volba == "3":
            prodat_otrokyni(hra)
        elif volba == "4":
            vylepsi_nevestinec(hra)

def spocitej_denni_vynos_divky(otrok, nev) -> int:
    zaklad = 20 + int(otrok.touha * 0.3) + int(otrok.vlhkost * 0.2) + int(otrok.faze_zkazenosti * 15)
    if otrok.charakter == "kurtizana":
        zaklad = int(zaklad * 1.4)
    elif otrok.charakter == "nymfomanka":
        zaklad = int(zaklad * 1.25)
    elif otrok.charakter == "slechticna":
        zaklad = int(zaklad * 1.3)
    nasobek_luxusu = 1.0 + (nev.uroven_luxusu - 1) * 0.2
    return max(15, int(zaklad * nasobek_luxusu))

def vypocti_denni_prijem(hra) -> int:
    if not hasattr(hra, "nevestinec") or not hra.nevestinec.otevreno:
        return 0
    nev = hra.nevestinec
    aktivni = hra.harem.vsechny_aktivni()
    divky_v_nev = [o for o in aktivni if getattr(o, "v_nevestinci", False)]
    if not divky_v_nev:
        return 0

    celkem = 0
    for d in divky_v_nev:
        vynos = spocitej_denni_vynos_divky(d, nev)
        celkem += vynos
        # Lehké změny v atributech po noci v nevěstinci
        d.touha = min(100, d.touha + 2)
        d.poslusnost = min(100, d.poslusnost + 1)
        if random.random() < 0.25:
            d.faze_zkazenosti = min(3, d.faze_zkazenosti + 1)

    nev.celkovy_zisk += celkem
    nev.obslouzeno_zakazniku += len(divky_v_nev) * random.randint(2, 4)
    return celkem
