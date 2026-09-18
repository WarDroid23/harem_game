# game/mafie.py
from models.mafie import Mafie, Uzemi
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info, vytiskni_volbu
from config import GOLD, CYAN, MAGENTA, GREEN, RED, NC

DOSTUPNA_UZEMI = (
    ("Přístav", 100, 0, 5),
    ("Tržiště", 80, 0, 3),
    ("Čtvrť bohatých", 150, 0, 10),
    ("Doky", 90, 0, 4),
    ("Staré město", 120, 0, 7),
)


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
    from data.jmena import JMENA

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
                jmeno = random.choice(["Morgana", "Valerie", "Lilith", "Morana", "Kassandra"])
                zajatkyne = Otrokyně(jmeno=jmeno, vek=random.randint(19, 27))
                zajatkyne.charakter = "zvrácená"
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
        elif volba in ("7", "5"):
            valka_uzemi(hrac, mafie, hra)
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

