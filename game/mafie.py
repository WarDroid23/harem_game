# game/mafie.py
from models.mafie import Mafie, Uzemi
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info, vytiskni_volbu
from config import GOLD, CYAN, MAGENTA, GREEN, RED, YELLOW, WHITE, BOLD, DIM, NC

DOSTUPNA_UZEMI = (
    ("Přístav", 100, 0, 5),
    ("Tržiště", 80, 0, 3),
    ("Čtvrť bohatých", 150, 0, 10),
    ("Doky", 90, 0, 4),
    ("Staré město", 120, 0, 7),
    ("Černá čtvrť", 130, 0, 9),
    ("Říční nábřeží", 110, 0, 6),
    ("Univerzitní okrsek", 140, 0, 8),
)

KATALOG_PODNIKU = {
    "tajne_doupe": {
        "nazev": "Tajné drogové doupě", "cena": 200, "prijem": 45,
        "popis": "Zvyšuje odbyt drog a přináší stálý černý zisk.",
    },
    "tajny_nevestinec": {
        "nazev": "Podsvětní nevěstinec", "cena": 300, "prijem": 65,
        "popis": "Diskrétní podnik pro bohatou klientelu podsvětí.",
    },
    "nelegalni_herna": {
        "nazev": "Podzemní herna & Kostky", "cena": 250, "prijem": 50,
        "popis": "Láká hazardní hráče a pašeráky z celého města.",
    },
    "vypalne_cech": {
        "nazev": "Síť výpalného od cechů", "cena": 150, "prijem": 35,
        "popis": "Pravidelné poplatky za ochranu od místních obchodníků.",
    },
    "paseracky_sklad": {
        "nazev": "Pašerácký sklad", "cena": 350, "prijem": 75,
        "popis": "Ukryje kontraband a vynáší z každé tajné dodávky.",
    },
    "padelatelska_dilna": {
        "nazev": "Padělatelská dílna", "cena": 300, "prijem": 60,
        "popis": "Vyrábí falešné listiny a přináší příjem z jejich prodeje.",
    },
    "tajna_arena": {
        "nazev": "Tajná zápasnická aréna", "cena": 450, "prijem": 85,
        "popis": "Pořádá nelegální zápasy pro bohaté sázkaře.",
    },
}


def dostupna_uzemi(mafie: Mafie):
    vlastni = {u.nazev for u in mafie.uzemi}
    return [
        Uzemi(nazev, prijem, kontrola, riziko)
        for nazev, prijem, kontrola, riziko in DOSTUPNA_UZEMI
        if nazev not in vlastni
    ]


def koupit_uzemi(hrac, mafie: Mafie, nazev: str):
    uzemi = next((u for u in dostupna_uzemi(mafie) if u.nazev == nazev), None)
    cena = 500 + len(mafie.uzemi) * 200
    if uzemi is None or hrac.gold < cena:
        return False
    hrac.gold -= cena
    uzemi.obsazeno = True
    uzemi.kontrola = 50
    mafie.uzemi.append(uzemi)
    tisk_ok(f"Koupeno území {uzemi.nazev}. Výchozí kontrola: 50%.")
    return True


def najmout_vojaka(hrac, mafie: Mafie, cena=50):
    if hrac.gold < cena:
        return False
    hrac.gold -= cena
    mafie.vojaci += 1
    tisk_ok("Najat voják do podsvětní gardy.")
    return True


def najmout_kapitana(hrac, mafie: Mafie, cena=250):
    if hrac.gold < cena:
        return False
    hrac.gold -= cena
    mafie.kapitanove = getattr(mafie, "kapitanove", 0) + 1
    tisk_ok("Najat podsvětní kapitán (+5 bojová síla, vedení oddílů).")
    return True


def najmout_informatora(hrac, mafie: Mafie, cena=100):
    if hrac.gold < cena:
        return False
    hrac.gold -= cena
    mafie.informatori = getattr(mafie, "informatori", 0) + 1
    tisk_ok("Získán nový pouliční informátor (+špionáž, odhalení slabin rivalů).")
    return True


def _rozbal_args(arg0, arg1=None):
    if arg1 is not None:
        return arg0, arg1, None
    if hasattr(arg0, "hrac") and hasattr(arg0, "mafie"):
        return arg0.hrac, arg0.mafie, arg0
    raise TypeError("spravovat_mafii očekává (hra) nebo (hrac, mafie)")


def valka_uzemi(hrac, mafie, hra=None):
    import random
    from game.kronika import zaznamenej
    from models.otrokyne import Otrokyně
    from data.jmena import vyber_nove_jmeno

    if not mafie.uzemi:
        tisk_chyba("Bez vlastních území nemá smysl vést válku syndikátů.")
        return

    clear()
    print(f"{MAGENTA}--- Válka o území a podsvětní syndikáty ---{NC}\n")
    print("Vyber soupeřící syndikát k útoku:")
    vytiskni_volbu('1', 'Přístavní cech pašeráků (snadný cíl, nízké ztráty)')
    vytiskni_volbu('2', 'Syndikát Nočních stínů (střední cíl, boj o vliv a kontrolu)')
    vytiskni_volbu('3', 'Krvavý kult podsvětí (těžký cíl, vysoká kořist a temné rituály)')
    vytiskni_volbu('4', 'Inkviziční represivní garda (extrémní riziko, oslabení církve)')
    vytiskni_volbu('0', 'Zpět')

    try:
        vyber = input("> ").strip()
    except EOFError:
        return

    cile = {
        "1": {"nazev": "Přístavní cech pašeráků", "zaklad_obrana": 25, "obtiznost": "snadná", "risk_vojaci": 1},
        "2": {"nazev": "Syndikát Nočních stínů", "zaklad_obrana": 50, "obtiznost": "střední", "risk_vojaci": 2},
        "3": {"nazev": "Krvavý kult podsvětí", "zaklad_obrana": 80, "obtiznost": "těžká", "risk_vojaci": 3},
        "4": {"nazev": "Inkviziční represivní garda", "zaklad_obrana": 120, "obtiznost": "extrémní", "risk_vojaci": 4},
    }

    if vyber not in cile:
        return

    cil = cile[vyber]
    nepritel_sila = cil["zaklad_obrana"] + random.randint(-5, 15) + (getattr(hrac, "den", 1) // 3)

    print(f"\nCíl: {GOLD}{cil['nazev']}{NC} (předpokládaná síla: ~{nepritel_sila})")
    print("Zvol strategii útoku:")
    vytiskni_volbu('1', 'Frontální nápor armády (vojáci a kapitáni v plné síle)')
    vytiskni_volbu('2', 'Skrytá sabotáž a úplatky (vyžaduje informátory a korupci)')
    vytiskni_volbu('3', 'Temný úder dominia (spotřebuje 15 temné energie hráče pro bonus k síle)')

    try:
        taktika = input("Strategie [1/2/3]: ").strip()
    except EOFError:
        taktika = "1"

    bonus_taktika = 0
    taktika_popis = "Přímý nápor"
    if taktika == "2":
        taktika_popis = "Skrytá sabotáž"
        bonus_taktika = getattr(mafie, "informatori", 0) * 8 + (mafie.korupce // 3)
        tisk_info(f"Informátoři podkopali nepřátelskou obranu (+{bonus_taktika} taktická síla).")
    elif taktika == "3":
        taktika_popis = "Temný úder"
        if getattr(hrac, "dark_energy", 0) >= 15:
            hrac.dark_energy -= 15
            bonus_taktika = 25 + (getattr(hrac, "level", 1) * 3)
            tisk_info(f"Temná aura zasáhla nepřátelské řady hrůzou (+{bonus_taktika} mystická síla).")
        else:
            tisk_chyba("Nemáš 15 temné energie – útok probíhá bez magie.")

    zakladni_sila = (
        mafie.vojaci * 3 +
        getattr(mafie, "kapitanove", 0) * 12 +
        len(mafie.uzemi) * 4 +
        getattr(mafie, "vliv_ve_meste", 0) // 5 +
        bonus_taktika
    )

    tisk_info(f"\nTvá celková útočná síla: {zakladni_sila}  vs  Obrana rivala: {nepritel_sila}")

    if zakladni_sila >= nepritel_sila:
        rozdil = zakladni_sila - nepritel_sila
        zisk_zlata = random.randint(120, 260) + rozdil * 2
        hrac.gold += zisk_zlata
        mafie.vliv_ve_meste = min(100, getattr(mafie, "vliv_ve_meste", 0) + random.randint(4, 9))
        for u in mafie.uzemi:
            u.kontrola = min(100, u.kontrola + random.randint(3, 8))

        tisk_ok(f"✔ VÍTĚZSTVÍ nad {cil['nazev']}! Kořist: +{zisk_zlata} 🪙, vliv ve městě stoupl na {mafie.vliv_ve_meste}%.")

        # Speciální odměna u Krvavého kultu nebo drtivého vítězství
        if vyber == "3" and rozdil >= 15 and hra is not None:
            if random.random() < 0.65:
                from data.charaktery import vyber_charakter
                jmeno = vyber_nove_jmeno(hra.harem.otrokyne)
                zajatkyne = Otrokyně(
                    jmeno=jmeno,
                    vek=random.randint(19, 27),
                    charakter=vyber_charakter(),
                )
                zajatkyne.faze_zkazenosti = 4
                zajatkyne.poslusnost = 45
                zajatkyne.loajalita = 40
                zajatkyne.touha = 60
                hra.harem.pridat(zajatkyne)
                tisk_ok(f"★ Mezi troskami svatyně kultu byla zajata kněžka {jmeno} a uvržena do tvého harému!")
                if hra:
                    zaznamenej(hra, f"Válka syndikátů: zajata temná kněžka {jmeno}.")

        zprava = f"Vítězství ve válce o území nad {cil['nazev']} ({taktika_popis}, +{zisk_zlata} zl)."
        if hra:
            zaznamenej(hra, zprava)
    else:
        ztrata_zlata = min(hrac.gold, random.randint(50, 150))
        padli_vojaci = min(mafie.vojaci, random.randint(1, cil["risk_vojaci"]))
        hrac.gold -= ztrata_zlata
        mafie.vojaci = max(0, mafie.vojaci - padli_vojaci)
        tisk_chyba(f"✖ PORÁŽKA! Tvé síly byly odraženy. Ztráta: −{ztrata_zlata} 🪙, padlo {padli_vojaci} vojáků.")
        if hra:
            zaznamenej(hra, f"Porážka ve válce o území proti {cil['nazev']} (−{ztrata_zlata} zl, −{padli_vojaci} vojáků).")


def spravovat_mafii(arg0, arg1=None):
    try:
        hrac, mafie, hra = _rozbal_args(arg0, arg1)
    except TypeError as e:
        tisk_chyba(str(e))
        try:
            input("Enter...")
        except EOFError:
            pass
        return

    while True:
        clear()
        print(f"{MAGENTA}--- Mafie / Sex impérium ---{NC}")
        print(f"Zlato: {hrac.gold} 🪙")
        print(
            f"Vojáci: {mafie.vojaci} | Kapitáni: {getattr(mafie, 'kapitanove', 0)} | "
            f"Informátoři: {getattr(mafie, 'informatori', 0)}"
        )
        print(f"Celkový pasivní příjem: {mafie.vypocet_prijmu()} zlaťáků/den")
        print(f"Korupce: {mafie.korupce} | Vliv ve městě: {getattr(mafie, 'vliv_ve_meste', 0)}%\n")

        if not mafie.uzemi:
            print("Zatím nemáš žádná území.")
        else:
            for i, u in enumerate(mafie.uzemi, 1):
                stav = "obsazeno" if getattr(u, "obsazeno", False) else "volné"
                prijem_aktualni = u.prijem * u.kontrola // 100 if getattr(u, "obsazeno", False) else 0
                print(
                    f"{i}) {u.nazev} – základ {u.prijem} (nyní {prijem_aktualni} zl), "
                    f"kontrola {u.kontrola}%, stav: {stav}"
                )

        print(f"\n{GREEN}1) Koupit nové území")
        print(f"{CYAN}2) Vylepšit kontrolu nad územím")
        print(f"{GOLD}3) Najímat vojáky (50 zl)")
        print(f"{YELLOW}4) Najmout kapitána (250 zl)")
        print(f"{WHITE}5) Získat informátora (100 zl)")
        print(f"{RED}6) Zvýšit korupci (200 zl)")
        print(f"{MAGENTA}7) Válka o území / syndikáty")
        print(f"{CYAN}8) Nelegální podniky v územích (doupata, nevěstince, herny)")
        print(f"{YELLOW}9) Vydírání hodnostářů & podplácení stráží")
        print(f"{NC}0) Zpět")

        try:
            volba = input("> ").strip()
        except EOFError:
            return
        if volba == "0":
            return
        if volba == "1":
            dostupna = dostupna_uzemi(mafie)
            if not dostupna:
                tisk_info("Žádná další území k nákupu.")
            else:
                for i, u in enumerate(dostupna, 1):
                    cena = 500 + len(mafie.uzemi) * 200
                    print(f"{i}) {u.nazev} – příjem {u.prijem}, riziko {u.riziko_inkvizice}, cena {cena} 🪙")
                try:
                    idx = int(input("Vyber území: ")) - 1
                    if 0 <= idx < len(dostupna):
                        if koupit_uzemi(hrac, mafie, dostupna[idx].nazev):
                            if hra:
                                from game.kronika import zaznamenej
                                zaznamenej(hra, f"Koupeno nové území {dostupna[idx].nazev}")
                        else:
                            tisk_chyba("Nedostatek zlata nebo území není dostupné.")
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Špatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "2":
            if not mafie.uzemi:
                tisk_chyba("Nemáš žádná území.")
            else:
                for i, u in enumerate(mafie.uzemi, 1):
                    print(f"{i}) {u.nazev} (kontrola {u.kontrola}%)")
                try:
                    idx = int(input("Vyber území: ")) - 1
                    if 0 <= idx < len(mafie.uzemi):
                        cena = 100 + mafie.uzemi[idx].kontrola * 5
                        if hrac.gold >= cena and mafie.uzemi[idx].kontrola < 100:
                            hrac.gold -= cena
                            mafie.uzemi[idx].kontrola = min(100, mafie.uzemi[idx].kontrola + 10)
                            tisk_ok(f"Kontrola zvýšena na {mafie.uzemi[idx].kontrola}%.")
                        else:
                            tisk_chyba("Nelze vylepšit (nedostatek zlata nebo max 100%).")
                    else:
                        tisk_chyba("Špatná volba.")
                except ValueError:
                    tisk_chyba("Špatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "3":
            if not najmout_vojaka(hrac, mafie):
                tisk_chyba("Nedostatek zlata na vojáka.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "4":
            if not najmout_kapitana(hrac, mafie):
                tisk_chyba("Nedostatek zlata na kapitána.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "5":
            if not najmout_informatora(hrac, mafie):
                tisk_chyba("Nedostatek zlata na informátora.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "6":
            cena = 200
            if hrac.gold >= cena:
                hrac.gold -= cena
                mafie.korupce = min(100, mafie.korupce + 5)
                tisk_ok(f"Korupce zvýšena na {mafie.korupce}%.")
            else:
                tisk_chyba("Nedostatek zlata.")
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "7":
            valka_uzemi(hrac, mafie, hra)
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "8":
            spravovat_podniky_uzemi(hrac, mafie)
            try:
                input("Enter...")
            except EOFError:
                return
        elif volba == "9":
            vydirani_a_korupce(hrac, mafie, hra)
            try:
                input("Enter...")
            except EOFError:
                return
        else:
            tisk_chyba("Neplatná volba.")
            try:
                input("Enter...")
            except EOFError:
                return


def spravovat_podniky_uzemi(hrac, mafie):
    if not mafie.uzemi:
        tisk_chyba("Nejprve musíš ovládat alespoň jedno území.")
        return

    clear()
    print(f"{MAGENTA}--- Nelegální podniky & Výpalné v městských čtvrtích ---{NC}\n")
    for i, u in enumerate(mafie.uzemi, 1):
        pocet_p = len(getattr(u, "podniky", {}))
        print(f"  {i}) {BOLD}{u.nazev}{NC} (Podniky: {pocet_p}, Kontrola: {u.kontrola}%)")
    vytiskni_volbu('0', 'Zpět')

    try:
        vyber = input("\nVyber území pro správu podniků: ").strip()
        if vyber == "0" or not vyber:
            return
        idx = int(vyber) - 1
        if not (0 <= idx < len(mafie.uzemi)):
            tisk_chyba("Špatné číslo území.")
            return
    except ValueError:
        tisk_chyba("Zadej platné číslo.")
        return

    u = mafie.uzemi[idx]
    if not hasattr(u, "podniky"):
        u.podniky = {}

    clear()
    print(f"{CYAN}Správa podniků v území: {BOLD}{u.nazev}{NC}\n")
    print("Aktivní podniky:")
    if not u.podniky:
        print("  (Žádný vybudovaný podnik)")
    else:
        for p_id, p_data in u.podniky.items():
            print(f"  ✔ {BOLD}{p_data['nazev']}{NC} (+{p_data['prijem']} zl/den)")

    print(f"\nDostupné investice (Tvé zlato: {GOLD}{hrac.gold} 🪙{NC}):")
    mozne = [k for k in KATALOG_PODNIKU if k not in u.podniky]
    for j, k_id in enumerate(mozne, 1):
        info = KATALOG_PODNIKU[k_id]
        print(f"  {j}) {BOLD}{info['nazev']}{NC} — Cena: {GOLD}{info['cena']} 🪙{NC} (+{info['prijem']} zl/den)")
        print(f"      {DIM}{info['popis']}{NC}")
    vytiskni_volbu('0', 'Zpět')

    volba_p = input("\nVyber podnik k vybudování: ").strip()
    if volba_p == "0" or not volba_p:
        return
    try:
        p_idx = int(volba_p) - 1
        if 0 <= p_idx < len(mozne):
            vybrany_klic = mozne[p_idx]
            vybrany_p = KATALOG_PODNIKU[vybrany_klic]
            if hrac.gold >= vybrany_p["cena"]:
                hrac.gold -= vybrany_p["cena"]
                u.podniky[vybrany_klic] = {"nazev": vybrany_p["nazev"], "prijem": vybrany_p["prijem"]}
                mafie.vliv_ve_meste = min(100, getattr(mafie, "vliv_ve_meste", 0) + 3)
                tisk_ok(f"Podnik '{vybrany_p['nazev']}' byl úspěšně otevřen v čtvrti {u.nazev}!")
            else:
                tisk_chyba("Nemáš dostatek zlata na tuto investici.")
        else:
            tisk_chyba("Neplatná volba.")
    except ValueError:
        tisk_chyba("Zadej číslo.")


def vydirani_a_korupce(hrac, mafie, hra=None):
    clear()
    print(f"{RED}--- Vydírání hodnostářů & Podplácení městských stráží ---{NC}\n")
    print(f"Informátoři: {getattr(mafie, 'informatori', 0)} | Korupce: {mafie.korupce}% | Vliv: {getattr(mafie, 'vliv_ve_meste', 0)}%\n")
    vytiskni_volbu('1', 'Vydírat zkorumpovaného radního (Vyžaduje 1 informátora, zisk 150-300 zl)')
    vytiskni_volbu('2', 'Uplatit velitele hlídky (Cena 120 zl, sníží vliv inkvizice o 10%)')
    vytiskni_volbu('3', 'Kompromitovat církevního soudce (Vyžaduje 2 informátory a 30% korupce)')
    vytiskni_volbu('0', 'Zpět')

    volba = input("> ").strip()
    if volba == "1":
        if getattr(mafie, "informatori", 0) < 1:
            tisk_chyba("Potřebuješ alespoň 1 informátora ke shromáždění kompromateriálů.")
        else:
            import random
            mafie.informatori -= 1
            zisk = random.randint(150, 320)
            hrac.gold += zisk
            mafie.vliv_ve_meste = min(100, getattr(mafie, "vliv_ve_meste", 0) + 4)
            tisk_ok(f"Radní zaplatil {zisk} 🪙 ze strachu ze zveřejnění svých hříchů!")
    elif volba == "2":
        if hrac.gold < 120:
            tisk_chyba("Nemáš dost zlata na úplatek.")
        else:
            hrac.gold -= 120
            hrac.vliv_inkvizice = max(0, getattr(hrac, "vliv_inkvizice", 0) - 10)
            mafie.korupce = min(100, mafie.korupce + 4)
            tisk_ok("Velitel hlídky přijal měšec. Inkviziční tlak na tvé impérium klesl o 10%.")
    elif volba == "3":
        if getattr(mafie, "informatori", 0) < 2 or mafie.korupce < 30:
            tisk_chyba("Nedostatek informátorů (potřeba 2) nebo nízká korupce (potřeba 30%).")
        else:
            mafie.informatori -= 2
            hrac.vliv_inkvizice = max(0, getattr(hrac, "vliv_inkvizice", 0) - 25)
            hrac.dark_energy = min(100, hrac.dark_energy + 20)
            mafie.vliv_ve_meste = min(100, getattr(mafie, "vliv_ve_meste", 0) + 8)
            tisk_ok("Církevní soudce je plně ve tvé moci! Tlak inkvizice drasticky klesl (-25%).")
