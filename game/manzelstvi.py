# game/manzelstvi.py
import random
from config import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GOLD, BOLD, WHITE, NC
from models.marriage import Marriage
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from data.jmena import JMENA

def je_mozne_zasnoubeni(otrokyne, hrac):
    if otrokyne.je_manzelkou:
        return False, "Již je vdaná"
    if otrokyne.loajalita < 60:
        return False, f"Loajalita příliš nízká ({otrokyne.loajalita}%)"
    if otrokyne.romance_body < 50:
        return False, f"Romance body příliš nízké ({otrokyne.romance_body}/100)"
    if not otrokyne.souhlas_romance:
        return False, "Neudělila souhlas s romancí"
    return True, "OK"

def je_mozne_svatba(marriage, den):
    if marriage.je_vdana():
        return False, "Již jsou vdaní"
    if den - marriage.den_zasnubin < 10:
        zbyva = 10 - (den - marriage.den_zasnubin)
        return False, f"Čekejte ještě {zbyva} dní"
    return True, "OK"

def je_mozne_potomstvo(marriage, den):
    if not marriage.je_vdana():
        return False, "Nejsou v manželství"
    if marriage.ma_dite():
        if den - (marriage.den_svatby + 60 * (marriage.pocet_deti())) < 60:
            return False, "Musíte čekat min. 60 dní mezi dětmi"
    return True, "OK"

def zasnoubeni(otrokyne, hrac, hra):
    cena = 500 + random.randint(100, 500)
    if hrac.gold < cena:
        tisk_chyba(f"Nemáš dost zlata! (chybí {cena - hrac.gold} 🪙)")
        return False
    hrac.gold -= cena
    marriage = Marriage(
        partner_jmeno=otrokyne.jmeno,
        den_zasnubin=hra.hrac.den,
        stav="zasnubeni",
    )
    hra.marriage_system[otrokyne.jmeno] = marriage
    otrokyne.je_manzelkou = True
    otrokyne.den_zasnubin = hra.hrac.den
    tisk_ok(f"💍 {otrokyne.jmeno} přijala vaši žádost o zasnoubení!")
    tisk_info(f"Utratili jste {cena} 🪙 na ceremoniál.")
    return True

def svatba(otrokyne, hrac, hra):
    if otrokyne.jmeno not in hra.marriage_system:
        tisk_chyba("Nejste zasnoubeni.")
        return False
    marriage = hra.marriage_system[otrokyne.jmeno]
    mozne, zprava = je_mozne_svatba(marriage, hra.hrac.den)
    if not mozne:
        tisk_chyba(f"Svatba není možná: {zprava}")
        return False
    cena = 1500 + random.randint(500, 1500)
    if hrac.gold < cena:
        tisk_chyba(f"Nemáš dost zlata! (chybí {cena - hrac.gold} 🪙)")
        return False
    hrac.gold -= cena
    puvab = random.randint(30, 100)
    marriage.cerem_puvab = puvab
    marriage.stav = "vdana"
    marriage.den_svatby = hra.hrac.den
    otrokyne.loajalita = min(100, otrokyne.loajalita + 20)
    otrokyne.partnerka = True
    otrokyne.partner_od_den = hra.hrac.den
    tisk_ok(f"💒 Sňatek s {otrokyne.jmeno} byl uskutečněn!")
    tisk_info(
        f"Kvalita věnování: {puvab}% | "
        f"Loajalita +20 | Utraceno: {cena} 🪙"
    )
    if hasattr(hrac, "zvys_max_sex"):
        hrac.zvys_max_sex(5)
        hrac.zvys_max_temno(3)
        hrac.dopln_energie_naplno()
        tisk_ok(
            f"Svatba prohloubila tvé síly. Max energie: "
            f"{hrac.max_sex()} sex / {hrac.max_temno()} temno."
        )
    return True

def mat_dite(otrokyne, marriage, hrac, hra):
    mozne, zprava = je_mozne_potomstvo(marriage, hra.hrac.den)
    if not mozne:
        tisk_chyba(f"Dítě není možné: {zprava}")
        return False
    jmeno_ditete = random.choice(JMENA)
    if random.random() < 0.5:
        jmeno_ditete = jmeno_ditete.replace("a", "o")
    dite = marriage.prida_dite(jmeno_ditete)
    if hasattr(hrac, "pridej_sex_energy"):
        hrac.pridej_sex_energy(10)
        hrac.pridej_dark_energy(5)
    else:
        hrac.sex_energy = min(getattr(hrac, "max_sex_energy", 100), hrac.sex_energy + 10)
        hrac.dark_energy = min(getattr(hrac, "max_dark_energy", 100), hrac.dark_energy + 5)
    otrokyne.loajalita = min(100, otrokyne.loajalita + 15)
    tisk_ok(
        f"👶 {otrokyne.jmeno} porodila {dite['pohlavi']} - {dite['jmeno']}!"
    )
    tisk_info(
        f"Talent: {dite['talent']}% | Typ: {dite['typ']} | "
        f"Loajalita +15"
    )
    return True

def rozvod(otrokyne, hrac, hra):
    if otrokyne.jmeno not in hra.marriage_system:
        tisk_chyba("Nejste v manželství.")
        return False
    marriage = hra.marriage_system[otrokyne.jmeno]
    veta = 2000 + random.randint(500, 1500)
    if hrac.gold < veta:
        tisk_chyba(f"Nemáš dost zlata na rozvod! (chybí {veta - hrac.gold} 🪙)")
        return False
    hrac.gold -= veta
    marriage.stav = "rozvedena"
    otrokyne.je_manzelkou = False
    otrokyne.partnerka = False
    otrokyne.loajalita = max(0, otrokyne.loajalita - 40)
    tisk_chyba(f"⚖️ Rozvod s {otrokyne.jmeno} se uskutečnil.")
    tisk_info(f"Zaplatili jste {veta} 🪙 | Loajalita -40%")
    return True

def zobraz_postaveni_partnerstvi(otrokyne, marriage):
    clear()
    print(f"{GOLD}{BOLD}=== Manželství {otrokyne.jmeno} ==={NC}\n")
    if marriage.je_vdana():
        role_txt = " (👑 Hlavní manželka)" if getattr(marriage, "role_manzelky", "") == "hlavni" else ""
        print(f"{GREEN}Stav: Vdaná{role_txt}{NC}")
    elif marriage.je_rozvedena():
        print(f"{RED}Stav: Rozvedena{NC}")
    else:
        print(f"{YELLOW}Stav: Zasnoubená{NC}")
    print(f"Zasnoubeni: Den {marriage.den_zasnubin}")
    if marriage.den_svatby:
        print(f"Svatba: Den {marriage.den_svatby}")
        print(f"Krása ceremonie: {marriage.cerem_puvab}%")
    print(f"Intimita: {marriage.intimita_level}%")
    print(f"Žárlivost na ostatní choti: {getattr(marriage, 'zarlivost', 0)}%")
    print(f"Spokojenost v dominiu: {getattr(marriage, 'spokojenost', 70)}%")
    print(f"Počet dětí: {marriage.pocet_deti()}")
    if marriage.ma_dite():
        print(f"\n{CYAN}Děti:{NC}")
        for i, dite in enumerate(marriage.deti, 1):
            if dite["status"] == "žije":
                print(
                    f"  {i}) {dite['jmeno']} ({dite['pohlavi']}, "
                    f"věk {dite['vek']}, talent {dite['talent']}%, {dite['typ']})"
                )
            else:
                print(f"  {i}) {dite['jmeno']} ({dite['status']})")

def jmenovat_hlavni_manzelku(hra):
    clear()
    print(f"{GOLD}{BOLD}=== Jmenování První manželky (První dáma Dominia) ==={NC}\n")
    aktivni = hra.harem.vsechny_aktivni()
    vdane = [o for o in aktivni if getattr(o, "partnerka", False) and o.je_manzelkou]
    if len(vdane) < 1:
        tisk_chyba("Nemáš žádné vdané manželky.")
        input("Enter...")
        return

    print("První manželka dozírá na chod komnat, zklidňuje žárlivost v harému a zvyšuje prestiž dominia.\n")
    for i, o in enumerate(vdane, 1):
        m = hra.marriage_system.get(o.jmeno)
        je_hlavni = " ★ [AKTUÁLNÍ HLAVNÍ]" if getattr(m, "role_manzelky", "") == "hlavni" else ""
        print(f"{i}) {o.jmeno}{je_hlavni} (loajalita: {o.loajalita}%, spokojenost: {getattr(m, 'spokojenost', 70)}%)")
    print("0) Zpět")

    try:
        idx = int(input("> ")) - 1
        if 0 <= idx < len(vdane):
            vybrana = vdane[idx]
            for o in vdane:
                m = hra.marriage_system.get(o.jmeno)
                if m:
                    m.role_manzelky = "vedlejsi"
            m_vybrana = hra.marriage_system.get(vybrana.jmeno)
            if m_vybrana:
                m_vybrana.role_manzelky = "hlavni"
                m_vybrana.zarlivost = 0
                m_vybrana.spokojenost = 100
            vybrana.loajalita = min(100, vybrana.loajalita + 15)
            tisk_ok(f"👑 {vybrana.jmeno} byla slavnostně korunována První manželkou Dominia!")
            if hasattr(hra, "kronika"):
                from game.kronika import zaznamenej
                zaznamenej(hra, f"{vybrana.jmeno} byla jmenována První manželkou dominia.")
            input("Enter...")
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")

def spolecna_noc_manzelek(hra):
    clear()
    aktivni = hra.harem.vsechny_aktivni()
    vdane = [o for o in aktivni if getattr(o, "partnerka", False) and o.je_manzelkou]
    if len(vdane) < 2:
        tisk_chyba("Ke společné noci manželek potřebuješ mít alespoň 2 vdané choti.")
        input("Enter...")
        return

    cena_energie = 20
    if hra.hrac.sex_energy < cena_energie:
        tisk_chyba(f"Na společnou noc s více manželkami potřebuješ alespoň {cena_energie} sexuální energie.")
        input("Enter...")
        return

    hra.hrac.sex_energy -= cena_energie
    print(f"{MAGENTA}{BOLD}=== Společná noc tvých manželek ==={NC}\n")
    jmena_manzelek = ", ".join(o.jmeno for o in vdane)
    print(f"Pozval jsi do svých velkých komnat své drahé choti: {jmena_manzelek}.")
    print("Zpočátku mezi nimi panuje napětí a měření sil, ale ve tvém náručí a pod tvou rukou")
    print("se žárlivost mění v hluboké vzrušení, sdílenou vášeň a sesterské pouto.")

    for o in vdane:
        m = hra.marriage_system.get(o.jmeno)
        if m:
            m.zmen_zarlivost(-25)
            m.zmen_spokojenost(20)
            m.intimita_level = min(100, m.intimita_level + 10)
        o.loajalita = min(100, o.loajalita + 8)
        o.touha = min(100, o.touha + 10)

    # Obnova sil a temna
    max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
    hra.hrac.dark_energy = min(max_t, hra.hrac.dark_energy + 20)

    tisk_ok("Všechny tvé manželky nalezly soulad. Žárlivost prudce klesla (-25%), loajalita vzrostla!")
    tisk_ok("Získal jsi +20 temné energie ze sdílené harémové extáze.")
    if hasattr(hra, "kronika"):
        from game.kronika import zaznamenej
        zaznamenej(hra, f"Společná noc se všemi manželkami ({jmena_manzelek}) upevnila jednotu dominia.")
    input("Enter...")

def reseni_haremoveho_sporu(hra):
    clear()
    aktivni = hra.harem.vsechny_aktivni()
    vdane = [o for o in aktivni if getattr(o, "partnerka", False) and o.je_manzelkou]
    if len(vdane) < 2:
        tisk_info("Všechny tvé komnaty jsou v klidu – nemáš více manželek pro vznik sporu.")
        input("Enter...")
        return

    m1, m2 = random.sample(vdane, 2)
    mar1 = hra.marriage_system.get(m1.jmeno)
    mar2 = hra.marriage_system.get(m2.jmeno)

    print(f"{RED}{BOLD}=== Spor v komnatách: {m1.jmeno} vs. {m2.jmeno} ==={NC}\n")
    situace = random.choice([
        f"{m1.jmeno} obviňuje {m2.jmeno}, že jí vzala vzácný hedvábný závoj z tvých darů.",
        f"{m2.jmeno} žárlí na čas, který jsi včera v noci strávil o samotě s {m1.jmeno}.",
        f"{m1.jmeno} se dožaduje lepších pokojů s výhledem do zahrady, které dosud obývá {m2.jmeno}."
    ])
    print(situace)
    print("\nJak spor rozhodneš jako pán domu?")
    print(f"1) Dát za pravdu {m1.jmeno} (potěší ji, {m2.jmeno} bude žárlit)")
    print(f"2) Dát za pravdu {m2.jmeno} (potěší ji, {m1.jmeno} bude žárlit)")
    print("3) Oběma darovat šperky a sjednat smír (stojí 60 🪙, zklidní obě)")
    print("4) Pevná panská ruka: obě pokárat a nařídit poslušnost (vyžaduje temno)")

    try:
        v = input("> ").strip()
        if v == "1":
            if mar1: mar1.zmen_spokojenost(15); mar1.zmen_zarlivost(-15)
            if mar2: mar2.zmen_zarlivost(25); mar2.zmen_spokojenost(-15)
            tisk_ok(f"Rozhodl jsi ve prospěch {m1.jmeno}.")
        elif v == "2":
            if mar2: mar2.zmen_spokojenost(15); mar2.zmen_zarlivost(-15)
            if mar1: mar1.zmen_zarlivost(25); mar1.zmen_spokojenost(-15)
            tisk_ok(f"Rozhodl jsi ve prospěch {m2.jmeno}.")
        elif v == "3":
            if hra.hrac.gold >= 60:
                hra.hrac.gold -= 60
                if mar1: mar1.zmen_zarlivost(-15); mar1.zmen_spokojenost(15)
                if mar2: mar2.zmen_zarlivost(-15); mar2.zmen_spokojenost(15)
                tisk_ok("Šperky a vlídné slovo okamžitě urovnaly veškeré spory v harému.")
            else:
                tisk_chyba("Nemáš dostatek zlata na dary pro obě.")
        elif v == "4":
            if hra.hrac.dark_energy >= 10:
                hra.hrac.dark_energy -= 10
                m1.poslusnost = min(100, m1.poslusnost + 10)
                m2.poslusnost = min(100, m2.poslusnost + 10)
                if mar1: mar1.zmen_zarlivost(-10)
                if mar2: mar2.zmen_zarlivost(-10)
                tisk_ok("Tvá autorita a temná aura obě okamžitě srovnaly. V komnatách zavládlo posvátné ticho.")
            else:
                tisk_chyba("Nedostatek temné energie na zastrašení.")
        input("Enter...")
    except Exception as e:
        tisk_chyba(f"Chyba: {e}")
        input("Enter...")

def menu_manzelstvi(hra):
    aktivni = hra.harem.vsechny_aktivni()
    if not aktivni:
        tisk_chyba("Nemáš žádné otrokyně.")
        input("Enter...")
        return
    while True:
        clear()
        print(f"{GOLD}{BOLD}--- Manželství a Rodina ---{NC}\n")
        vdane = [o for o in aktivni if o.je_manzelkou]
        if vdane:
            print(f"{GREEN}Vdané otrokyně:{NC}")
            for o in vdane:
                marriage = hra.marriage_system.get(o.jmeno)
                if marriage:
                    deti_text = f" ({marriage.pocet_deti()} dětí)" if marriage.ma_dite() else ""
                    print(f"  • {o.jmeno}{deti_text}")
        print(f"\n{CYAN}Volby:{NC}")
        print("1) 💍 Zasnoubení")
        print("2) 💒 Svatba")
        print("3) 👶 Mít dítě")
        print("4) 📋 Prohlédnout manželství")
        print("5) ⚖️ Rozvod")
        print("6) 🌙 Společná noc manželek (stmelení chotí, snížení žárlivosti)")
        print("7) ⚡ Řešení harémového sporu (urovnání žárlivosti a intrik)")
        print("8) 👑 Jmenovat První manželku dominia")
        print("0) Zpět")
        try:
            volba = input("> ").strip().lower()
        except EOFError:
            return
        if volba == "0":
            return
        if volba == "1":
            print("\nVyber otrokyni k zasnoubení:")
            for i, o in enumerate(aktivni, 1):
                mozne, _ = je_mozne_zasnoubeni(o, hra.hrac)
                status = "✓" if mozne else "✗"
                print(f"{i}) {o.jmeno} {status}")
            try:
                idx = int(input("> ")) - 1
                if 0 <= idx < len(aktivni):
                    otrok = aktivni[idx]
                    mozne, zprava = je_mozne_zasnoubeni(otrok, hra.hrac)
                    if mozne:
                        zasnoubeni(otrok, hra.hrac, hra)
                    else:
                        tisk_chyba(f"Nemožné: {zprava}")
                else:
                    tisk_chyba("Špatná volba.")
            except ValueError:
                tisk_chyba("Zadej číslo.")
            input("Enter...")
        elif volba == "2":
            zasnoubene = [o for o in aktivni if o.je_manzelkou and not o.partnerka]
            if zasnoubene:
                print("\nVyber zasnoubenu otrokyni pro svatbu:")
                for i, o in enumerate(zasnoubene, 1):
                    print(f"{i}) {o.jmeno}")
                try:
                    idx = int(input("> ")) - 1
                    if 0 <= idx < len(zasnoubene):
                        svatba(zasnoubene[idx], hra.hrac, hra)
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
            else:
                tisk_chyba("Žádné zasnoubené otrokyně.")
            input("Enter...")
        elif volba == "3":
            vdane = [o for o in aktivni if o.partnerka]
            if vdane:
                print("\nVyber vdanou otrokyni pro potomstvo:")
                for i, o in enumerate(vdane, 1):
                    print(f"{i}) {o.jmeno}")
                try:
                    idx = int(input("> ")) - 1
                    if 0 <= idx < len(vdane):
                        marriage = hra.marriage_system.get(vdane[idx].jmeno)
                        if marriage:
                            mat_dite(vdane[idx], marriage, hra.hrac, hra)
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
            else:
                tisk_chyba("Žádné vdané otrokyně.")
            input("Enter...")
        elif volba == "4":
            vdane = [o for o in aktivni if o.je_manzelkou]
            if vdane:
                print("\nVyber manželství k prohlédnutí:")
                for i, o in enumerate(vdane, 1):
                    print(f"{i}) {o.jmeno}")
                try:
                    idx = int(input("> ")) - 1
                    if 0 <= idx < len(vdane):
                        marriage = hra.marriage_system.get(vdane[idx].jmeno)
                        if marriage:
                            zobraz_postaveni_partnerstvi(vdane[idx], marriage)
                            input("Enter...")
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
            else:
                tisk_chyba("Žádné manželství.")
        elif volba == "5":
            vdane = [o for o in aktivni if o.je_manzelkou]
            if vdane:
                print("\nVyber otrokyni pro rozvod:")
                for i, o in enumerate(vdane, 1):
                    print(f"{i}) {o.jmeno}")
                potvrzeni = input("Opravdu chceš rozvod? (ano/ne) ").strip().lower()
                if potvrzeni == "ano":
                    try:
                        idx = int(input("> ")) - 1
                        if 0 <= idx < len(vdane):
                            rozvod(vdane[idx], hra.hrac, hra)
                        else:
                            tisk_chyba("Špatná volba.")
                    except ValueError:
                        tisk_chyba("Zadej číslo.")
                else:
                    tisk_info("Rozvod zrušen.")
            else:
                tisk_chyba("Žádné manželství.")
            input("Enter...")
        elif volba == "6":
            spolecna_noc_manzelek(hra)
        elif volba == "7":
            reseni_haremoveho_sporu(hra)
        elif volba == "8":
            jmenovat_hlavni_manzelku(hra)
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
