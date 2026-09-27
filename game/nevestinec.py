# game/nevestinec.py
import random
from config import GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, GOLD, NC, BOLD, DIM, WHITE
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info, vytiskni_volbu, hlavicka
from data.charaktery import CHARAKTERY
from models.nevestinec import SPECIALIZACE_POKOJU

CENA_OTEVRENI = 300


def otevrit_nevestinec(hra) -> bool:
    clear()
    hlavicka("Založení nevěstince v Červené čtvrti")
    print(f"\n{MAGENTA}V rušných uličkách Červené čtvrti je k mání stará honosná budova.{NC}")
    print("Můžeš ji zrenovovat a vybudovat z ní nejvyhledávanější nevěstinec ve městě.")
    print(f"Cena licence a renovace: {GOLD}{CENA_OTEVRENI} 🪙{NC}")
    print(f"Tvé zlato: {hra.hrac.gold} 🪙\n")
    vytiskni_volbu('1', 'Koupit a otevřít nevěstinec', GREEN)
    vytiskni_volbu('0', 'Zpět', RED)

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
    char = getattr(otrok, "charakter", "")
    if char == "princezna_ruin":
        zaklad = int(zaklad * 1.8)
    elif char == "sukuba_hybrid":
        zaklad = int(zaklad * 1.6)
    elif char == "kurtizana":
        zaklad = int(zaklad * 1.5)
    elif char == "slechticna":
        zaklad = int(zaklad * 1.4)
    elif char == "knezka_temnoty":
        zaklad = int(zaklad * 1.35)
    zkazeny_bonus = getattr(otrok, "faze_zkazenosti", 0) * 80
    cena = max(100, zaklad + zkazeny_bonus)
    return cena


def prodat_otrokyni(hra):
    clear()
    hlavicka("Trvalý prodej otrokyně mecenášům")
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

    print(f"\n{YELLOW}Bohatí šlechtici a mecenáši z Paláce i Červené čtvrti mají zájem o koupi:{NC}\n")
    for i, o in enumerate(k_prodeji, 1):
        cena = vypocti_cenu_prodeje(o)
        char = CHARAKTERY.get(o.charakter, {}).get("nazev", o.charakter)
        v_nev = " [V nevěstinci]" if getattr(o, "v_nevestinci", False) else ""
        print(f"  {BOLD}{CYAN}{i}){NC} {BOLD}{o.jmeno}{NC} ({char}, poslušnost {o.poslusnost}%, zkaženost fáze {o.faze_zkazenosti}){v_nev} -> Nabídka: {GOLD}{cena} 🪙{NC}")
    vytiskni_volbu('0', 'Zpět', RED)

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


def _prirad_volne_pokojove_cislo(hra, divky_v_nev) -> int:
    obsazene = {getattr(d, "pokoj_nevestinec", 1) for d in divky_v_nev}
    for p in range(1, hra.nevestinec.pocet_pokoju + 1):
        if p not in obsazene:
            return p
    return 1


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
    hlavicka("Zařazení otrokyně do pokoje nevěstince")
    print(f"\n{YELLOW}Volné otrokyně v dominia:{NC}")
    for i, o in enumerate(volne, 1):
        char = CHARAKTERY.get(o.charakter, {}).get("nazev", o.charakter)
        bonusy = []
        if o.charakter in ("kurtizana", "sukuba_hybrid", "princezna_ruin"):
            bonusy.append("★ Luxusní třída")
        if o.charakter in ("knezka_temnoty", "alchymistka", "carodejka"):
            bonusy.append("🌑 Okultní kouzlo")
        if o.charakter == "zlodejka":
            bonusy.append("💰 Kradení hostům")
        b_txt = f" [{', '.join(bonusy)}]" if bonusy else ""
        print(f"  {BOLD}{CYAN}{i}){NC} {o.jmeno} [{char}]{b_txt} (touha: {o.touha}, loajalita: {o.loajalita}%)")
    vytiskni_volbu('0', 'Zpět', RED)

    try:
        volba = input("> ").strip()
        if volba == "0":
            return
        idx = int(volba) - 1
        if 0 <= idx < len(volne):
            vybrana = volne[idx]
            cislo_pokoje = _prirad_volne_pokojove_cislo(hra, v_nevestinci)
            vybrana.v_nevestinci = True
            vybrana.pokoj_nevestinec = cislo_pokoje
            typ_spec = hra.nevestinec.ziskej_specializaci(cislo_pokoje)
            spec_info = SPECIALIZACE_POKOJU.get(typ_spec, SPECIALIZACE_POKOJU["klasicky"])
            tisk_ok(f"{vybrana.jmeno} byla ubytována v pokoji č. {cislo_pokoje} ({spec_info['nazev']})!")
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
    hlavicka("Stažení otrokyně zpět do Černé pevnosti")
    for i, o in enumerate(v_nevestinci, 1):
        p_cislo = getattr(o, "pokoj_nevestinec", i)
        typ_spec = hra.nevestinec.ziskej_specializaci(p_cislo)
        spec_nazev = SPECIALIZACE_POKOJU.get(typ_spec, {}).get("nazev", "Klasický")
        print(f"  {BOLD}{CYAN}{i}){NC} {o.jmeno} (Pokoj {p_cislo} – {spec_nazev})")
    vytiskni_volbu('0', 'Zpět', RED)

    try:
        volba = input("> ").strip()
        if volba == "0":
            return
        idx = int(volba) - 1
        if 0 <= idx < len(v_nevestinci):
            vybrana = v_nevestinci[idx]
            vybrana.v_nevestinci = False
            tisk_ok(f"{vybrana.jmeno} se vrací do Černé pevnosti.")
            input("Enter...")
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")


def specializovat_pokoje(hra):
    clear()
    nev = hra.nevestinec
    hlavicka("Specializace a přestavba pokojů")
    print(f"\n{MAGENTA}Každý pokoj lze zařídit pro konkrétní typ hostů a choutek.{NC}")
    print(f"{YELLOW}Správná kombinace dívky a pokoje výrazně zvyšuje denní zisk a poskytuje bonusy!{NC}\n")

    for p in range(1, nev.pocet_pokoju + 1):
        spec = nev.ziskej_specializaci(p)
        info = SPECIALIZACE_POKOJU.get(spec, SPECIALIZACE_POKOJU["klasicky"])
        print(f"  {BOLD}Pokoj #{p}:{NC} {GOLD}{info['nazev']}{NC} (násobek zisku: x{info['bonus_vynosu']})")
        print(f"      {DIM}{info['popis']}{NC}")

    print("\nVyber číslo pokoje k přestavbě (1 až {}) nebo 0:".format(nev.pocet_pokoju))
    vytiskni_volbu('0', 'Zpět', RED)

    try:
        v_pokoj = input("> ").strip()
        if v_pokoj == "0":
            return
        pokoj_num = int(v_pokoj)
        if not (1 <= pokoj_num <= nev.pocet_pokoju):
            tisk_chyba("Neplatné číslo pokoje.")
            input("Enter...")
            return

        clear()
        hlavicka(f"Přestavba pokoje č. {pokoj_num}")
        print("\nDostupné architektonické styly salonu:\n")
        seznam = list(SPECIALIZACE_POKOJU.items())
        for i, (klic, info) in enumerate(seznam, 1):
            cena_txt = f"{info['cena']} 🪙" if info['cena'] > 0 else "Zdarma"
            print(f"  {BOLD}{CYAN}{i}){NC} {BOLD}{info['nazev']}{NC} — Cena: {GOLD}{cena_txt}{NC}")
            print(f"      {DIM}{info['popis']}{NC}")
            vhodne = ", ".join(info['bonus_charakteru']) if info['bonus_charakteru'] else "všechny"
            print(f"      {GREEN}Ideální pro: {vhodne}{NC}")
        vytiskni_volbu('0', 'Zpět', RED)

        vyber_spec = input("> ").strip()
        if vyber_spec == "0":
            return
        idx_spec = int(vyber_spec) - 1
        if 0 <= idx_spec < len(seznam):
            vybrany_klic, data_spec = seznam[idx_spec]
            cena = data_spec["cena"]
            if hra.hrac.gold >= cena:
                hra.hrac.gold -= cena
                nev.nastav_specializaci(pokoj_num, vybrany_klic)
                tisk_ok(f"Pokoj č. {pokoj_num} byl úspěšně přestavěn na: {data_spec['nazev']}!")
            else:
                tisk_chyba("Nemáš dostatek zlata na přestavbu.")
            input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")


def _generuj_vip_nabidky(hra):
    nev = hra.nevestinec
    if nev.vip_nabidky:
        return nev.vip_nabidky

    pool = [
        {
            "id": "hrabe_cassian",
            "jmeno": "Hrabě Cassian ze Zlatého pahorku",
            "popis": "Bohatý aristokrat hledá společnost urozené dámy. Požaduje královskou eleganci a noblesu.",
            "pozadovane_charaktery": ["slechticna", "princezna_ruin", "kurtizana"],
            "odmena_zlato": random.randint(500, 750),
            "bonus_reputace": 6,
            "frakce": "palac",
        },
        {
            "id": "inkvizitor_malor",
            "jmeno": "Tajný prelát Inkvizice Malor",
            "popis": "Pokrytecký církevní hodnostář touží po zakázaném hříchu se svatou kacířkou.",
            "pozadovane_charaktery": ["knezka_temnoty", "padla_paladinka", "fanaticka"],
            "odmena_zlato": random.randint(380, 520),
            "snizeni_inkvizice": 15,
            "frakce": "cirkev",
        },
        {
            "id": "kapo_syndikatu",
            "jmeno": "Podsvětní kápo Valerio",
            "popis": "Vlivný gangster chce strávit noc s nebezpečnou a divokou ženou podsvětí.",
            "pozadovane_charaktery": ["zlodejka", "sukuba_hybrid", "krvava_subka"],
            "odmena_zlato": random.randint(350, 480),
            "bonus_mafie": 8,
            "frakce": "podsveti",
        },
        {
            "id": "velkokupec_giovanni",
            "jmeno": "Přístavní velkokupec Giovanni",
            "popis": "Marnotratný zámořský kupec lační po nespoutané vášni a exotickém svádění.",
            "pozadovane_charaktery": ["kurtizana", "nymfomanka", "sukuba_hybrid", "touha"],
            "odmena_zlato": random.randint(420, 620),
            "bonus_reputace": 8,
            "frakce": "cech_kurtizan",
        },
        {
            "id": "alchymisticky_mistr",
            "jmeno": "Alchymistický mistr Aurelius",
            "popis": "Učenec hledající ženu obeznámenou s afrodiziaky a zakázanými substancemi.",
            "pozadovane_charaktery": ["alchymistka", "carodejka"],
            "odmena_zlato": random.randint(360, 500),
            "bonus_lektvar": True,
            "frakce": "magove",
        },
    ]
    random.shuffle(pool)
    nev.vip_nabidky = pool[:3]
    return nev.vip_nabidky


def vip_zakazky(hra):
    clear()
    nev = hra.nevestinec
    hlavicka("VIP Mecenáši & Soukromé audience")
    nabidky = _generuj_vip_nabidky(hra)

    aktivni = hra.harem.vsechny_aktivni()
    divky_v_nev = [o for o in aktivni if getattr(o, "v_nevestinci", False)]

    print(f"\n{GOLD}Vlivní mecenáši města nabízejí tučné sumy za soukromou noční seanci s konkrétním typem dívky:{NC}\n")

    if not nabidky:
        print("  Dnes v salonu nečekají žádní další VIP hosté.")
        input("Enter...")
        return

    for i, nab in enumerate(nabidky, 1):
        print(f"  {BOLD}{MAGENTA}{i}) {nab['jmeno']}{NC}")
        print(f"      {DIM}{nab['popis']}{NC}")
        vhodne = ", ".join(CHARAKTERY.get(c, {}).get("nazev", c) for c in nab['pozadovane_charaktery'])
        print(f"      {CYAN}Požadovaný typ: {vhodne}{NC}")
        extra = []
        if nab.get("snizeni_inkvizice"):
            extra.append(f"{GREEN}−{nab['snizeni_inkvizice']} vliv inkvizice{NC}")
        if nab.get("bonus_mafie"):
            extra.append(f"{MAGENTA}+{nab['bonus_mafie']}% vliv mafie{NC}")
        if nab.get("bonus_lektvar"):
            extra.append(f"{BLUE}vzácný elixír{NC}")
        extra_str = f" + {', '.join(extra)}" if extra else ""
        print(f"      {GOLD}Odměna: {nab['odmena_zlato']} 🪙{extra_str}{NC}\n")

    vytiskni_volbu('0', 'Zpět', RED)

    try:
        volba = input("> ").strip()
        if volba == "0":
            return
        idx = int(volba) - 1
        if 0 <= idx < len(nabidky):
            vybrana_nab = nabidky[idx]
            if not divky_v_nev:
                tisk_chyba("Nemáš v nevěstinci žádné dívky k obsloužení mecenáše!")
                input("Enter...")
                return

            clear()
            hlavicka(f"Výběr dívky pro: {vybrana_nab['jmeno']}")
            print("\nDívky pracující v nevěstinci:\n")
            for j, d in enumerate(divky_v_nev, 1):
                char_nazev = CHARAKTERY.get(d.charakter, {}).get("nazev", d.charakter)
                hodi_se = " ✔ (Perfektní volba!)" if d.charakter in vybrana_nab["pozadovane_charaktery"] else " ✖ (Nesplňuje požadavky)"
                barva_v = GREEN if d.charakter in vybrana_nab["pozadovane_charaktery"] else RED
                print(f"  {BOLD}{CYAN}{j}){NC} {d.jmeno} [{char_nazev}] {barva_v}{hodi_se}{NC}")
            vytiskni_volbu('0', 'Zpět', RED)

            volba_d = input("> ").strip()
            if volba_d == "0":
                return
            idx_d = int(volba_d) - 1
            if 0 <= idx_d < len(divky_v_nev):
                divka = divky_v_nev[idx_d]
                if divka.charakter not in vybrana_nab["pozadovane_charaktery"] and divka.poslusnost < 80:
                    tisk_chyba(f"{vybrana_nab['jmeno']} byl zklamán! {divka.jmeno} neodpovídá jeho vytříbenému vkusu.")
                    input("Enter...")
                    return

                # Úspěch seance
                zlato = vybrana_nab["odmena_zlato"]
                hra.hrac.gold += zlato
                nev.celkovy_zisk += zlato
                nev.obslouzeno_zakazniku += 1
                nev.reputace_podniku = min(100, nev.reputace_podniku + 4)
                divka.loajalita = min(100, divka.loajalita + 5)
                divka.touha = min(100, divka.touha + 5)

                tisk_ok(f"★ Soukromá seance měla obrovský úspěch! {vybrana_nab['jmeno']} byl nadšen.")
                tisk_ok(f"Získáno: +{zlato} 🪙 a prestiž nevěstince vzrostla!")

                if vybrana_nab.get("snizeni_inkvizice"):
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - vybrana_nab["snizeni_inkvizice"])
                    tisk_info(f"Prelát zařídil stažení církevních hlídek: Inkvizice klesla na {hra.hrac.vliv_inkvizice}%!")
                if vybrana_nab.get("bonus_mafie") and hasattr(hra, "mafie"):
                    hra.mafie.vliv_ve_meste = min(100, getattr(hra.mafie, "vliv_ve_meste", 0) + vybrana_nab["bonus_mafie"])
                    tisk_info(f"Podsvětí ti vyjadřuje respekt: Vliv mafie stoupl o +{vybrana_nab['bonus_mafie']}%!")
                if vybrana_nab.get("bonus_lektvar") and hasattr(hra.hrac, "inventar"):
                    hra.hrac.inventar.pridej_predmet("elixir_temnoty")
                    tisk_info("Obdržel jsi vzácný Elixír temnoty!")

                if hasattr(hra, "kronika"):
                    from game.kronika import zaznamenej
                    zaznamenej(hra, f"VIP seance: {divka.jmeno} obsloužila hosta {vybrana_nab['jmeno']} (+{zlato} zl).")

                # Odstranění splněné zakázky
                nev.vip_nabidky.pop(idx)
                input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
    except ValueError:
        tisk_chyba("Zadej číslo.")
        input("Enter...")


def spionaz_a_kompro(hra):
    clear()
    nev = hra.nevestinec
    hlavicka("Špionáž v polštářích & Kompromitující materiály")
    print(f"\n{MAGENTA}V opojení vína a tělesné rozkoše prozradí i nejopatrnější šlechtici svá tajemství.{NC}")
    print(f"{CYAN}Tvé dívky (zejména zlodějky, kurtizány a manipulativní dívky) sbírají cenné kompro.{NC}\n")

    print(f"Nalezené kompromitující svazky a tajemství: {GOLD}{nev.kompro_materialy}{NC}\n")

    vytiskni_volbu('1', 'Vydírat městskou radu (+8% vliv mafie, +180 🪙, spotřebuje 1 kompro)', GOLD)
    vytiskni_volbu('2', 'Zdiskreditovat inkvizici (-15 vliv inkvizice před lidem, spotřebuje 1 kompro)', CYAN)
    vytiskni_volbu('3', 'Prodat kompro mecenášům na černém trhu (+220 🪙, spotřebuje 1 kompro)', GREEN)
    vytiskni_volbu('0', 'Zpět', RED)

    try:
        v = input("> ").strip()
        if v == "0":
            return
        if nev.kompro_materialy <= 0:
            tisk_chyba("Nemáš žádné nasbírané kompromitující materiály. Dívky je sbírají během nocí.")
            input("Enter...")
            return

        if v == "1":
            nev.kompro_materialy -= 1
            zisk = 180
            hra.hrac.gold += zisk
            if hasattr(hra, "mafie"):
                hra.mafie.vliv_ve_meste = min(100, getattr(hra.mafie, "vliv_ve_meste", 0) + 8)
            tisk_ok(f"Radní se podvolili vydírání! Získáno +{zisk} 🪙 a vliv mafie ve městě posílil.")
            input("Enter...")
        elif v == "2":
            nev.kompro_materialy -= 1
            hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 15)
            tisk_ok(f"Dopisy o hříších inkvizitorů byly rozvěšeny po náměstí! Inkvizice oslabena na {hra.hrac.vliv_inkvizice}%.")
            input("Enter...")
        elif v == "3":
            nev.kompro_materialy -= 1
            zisk = 220
            hra.hrac.gold += zisk
            tisk_ok(f"Tajné svazky prodány na černém trhu za +{zisk} 🪙!")
            input("Enter...")
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
    except ValueError:
        pass


def noc_neresti_festival(hra):
    clear()
    nev = hra.nevestinec
    hlavicka("Velkolepá Noc neřesti (Maškarní bál)")
    aktivni = hra.harem.vsechny_aktivni()
    divky_v_nev = [o for o in aktivni if getattr(o, "v_nevestinci", False)]

    CENA_FESTIVALU = 200
    print(f"\n{MAGENTA}Uspořádání velkolepé slavnosti v Červené čtvrti. Šampaňské teče proudem,{NC}")
    print(f"{MAGENTA}hudebníci hrají a tvé dívky tančí před nejbohatšími mecenáši a šlechtici.{NC}\n")
    print(f"Cena příprav a vína: {GOLD}{CENA_FESTIVALU} 🪙{NC}")
    print(f"Počet dívek v nevěstinci: {len(divky_v_nev)}")
    print(f"Tvé zlato: {hra.hrac.gold} 🪙\n")

    if not divky_v_nev:
        tisk_chyba("V nevěstinci nemáš žádné dívky! Festival bez nich nelze uspořádat.")
        input("Enter...")
        return

    vytiskni_volbu('1', 'Zahájit Noc neřesti!', GOLD)
    vytiskni_volbu('0', 'Zpět', RED)

    try:
        volba = input("> ").strip()
        if volba == "1":
            if hra.hrac.gold < CENA_FESTIVALU:
                tisk_chyba("Nemáš dostatek zlata na organizaci slavnosti.")
                input("Enter...")
                return

            den = getattr(hra.hrac, "den", 1)
            if getattr(nev, "posledni_den_akce", 0) == den:
                tisk_info("Dnes už byl festival uspořádán. Nech hosty a dívky vydechnout do zítřka.")
                input("Enter...")
                return

            hra.hrac.gold -= CENA_FESTIVALU
            nev.posledni_den_akce = den
            nev.pocet_festivalu += 1

            hoste = len(divky_v_nev) * random.randint(18, 30) + nev.uroven_luxusu * 15
            trzba = len(divky_v_nev) * random.randint(120, 220) + nev.uroven_luxusu * 100
            hra.hrac.gold += trzba
            nev.celkovy_zisk += trzba
            nev.obslouzeno_zakazniku += hoste
            nev.reputace_podniku = min(100, nev.reputace_podniku + 8)
            nev.kompro_materialy += random.randint(1, 2)

            for d in divky_v_nev:
                d.touha = min(100, d.touha + 15)
                d.loajalita = min(100, d.loajalita + 5)
                if random.random() < 0.4:
                    d.faze_zkazenosti = min(12, d.faze_zkazenosti + 1)

            tisk_ok(f"🎉 Noc neřesti byla legendární! Do nevěstince dorazilo {hoste} hostů.")
            tisk_ok(f"Hrubá tržba večera: +{trzba} 🪙! Prestiž podniku vzrostla na {nev.reputace_podniku}%.")
            tisk_info("V opilosti hosté vyžvanili tajné informace (+kompro materiál).")

            if hasattr(hra, "kronika"):
                from game.kronika import zaznamenej
                zaznamenej(hra, f"Festival v nevěstinci '{nev.nazev}': tržba +{trzba} zl, {hoste} hostů.")

            input("Enter...")
    except ValueError:
        pass


def pece_o_divky(hra):
    clear()
    nev = hra.nevestinec
    hlavicka("Wellness & Výcvik kurtizán")
    aktivni = hra.harem.vsechny_aktivni()
    divky_v_nev = [o for o in aktivni if getattr(o, "v_nevestinci", False)]

    if not divky_v_nev:
        tisk_chyba("V nevěstinci právě nepracují žádné dívky.")
        input("Enter...")
        return

    print(f"\n{CYAN}Investuj do péče o dívky – odpočaté a zručné kurtizány vydělávají mnohem víc!{NC}\n")
    vytiskni_volbu('1', 'Koupel v kozím mléce a vonných olejích (60 🪙) — plné HP, +12 touha, +6 loajalita všem dívkám', CYAN)
    vytiskni_volbu('2', 'Lekce svádění a erotických doteků (120 🪙) — +10 poslušnost, +15 submisivita, trvalý růst výnosů', GOLD)
    vytiskni_volbu('0', 'Zpět', RED)

    try:
        volba = input("> ").strip()
        if volba == "1":
            if hra.hrac.gold >= 60:
                hra.hrac.gold -= 60
                for d in divky_v_nev:
                    d.hp = d.max_hp
                    d.touha = min(100, d.touha + 12)
                    d.loajalita = min(100, d.loajalita + 6)
                tisk_ok("Dívky si užily horkou lázeň a vonné masáže. Jsou svěží a plné touhy!")
            else:
                tisk_chyba("Nedostatek zlata.")
            input("Enter...")
        elif volba == "2":
            if hra.hrac.gold >= 120:
                hra.hrac.gold -= 120
                for d in divky_v_nev:
                    d.poslusnost = min(100, d.poslusnost + 10)
                    d.submisivita = min(100, d.submisivita + 15)
                tisk_ok("Mistr kurtizán naučil dívky tajům poddajnosti a rafinovaného svádění!")
            else:
                tisk_chyba("Nedostatek zlata.")
            input("Enter...")
    except ValueError:
        pass


def vylepsi_nevestinec(hra):
    clear()
    nev = hra.nevestinec
    hlavicka(f"Rozvoj nevěstince '{nev.nazev}'")
    cena_pokoje = nev.cena_rozsireni_pokoju()
    cena_luxus = nev.cena_luxusu()
    cena_guard = nev.cena_ochranky()

    print(f"\n{YELLOW}Zlepšuj zázemí, rozšiřuj kapacitu a chraň podnik před inkvizicí:{NC}\n")
    vytiskni_volbu('1', f'Přistavět další pokoj ({nev.pocet_pokoju} -> {nev.pocet_pokoju + 1}): {GOLD}{cena_pokoje} 🪙{NC}', GREEN)
    vytiskni_volbu('2', f'Zvýšit luxus a výzdobu (úroveň {nev.uroven_luxusu} -> {nev.uroven_luxusu + 1}): {GOLD}{cena_luxus} 🪙{NC} (+20% k tržbám)', GOLD)
    vytiskni_volbu('3', f'Posílit ochranku a vyhazovače (úroveň {nev.ochranka} -> {nev.ochranka + 1}): {GOLD}{cena_guard} 🪙{NC} (ochrana před raziemi)', RED)
    vytiskni_volbu('0', 'Zpět', WHITE)

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

        hlavicka(f"🏛️  NEVĚSTINEC '{nev.nazev.upper()}'  🏛️")

        print(f"\n{CYAN}Pokoje: {len(divky_v_nev)}/{nev.pocet_pokoju} obsazeno | Luxus: Úr. {nev.uroven_luxusu} | Ochranka: Úr. {nev.ochranka} | Reputace: {nev.reputace_podniku}%{NC}")
        print(f"{GOLD}Odhadovaný denní příjem: +{odhadovany_zisk} 🪙 | Celkem vyděláno: {nev.celkovy_zisk} 🪙{NC}")
        print(f"{GREEN}Obslouženo hostů: {nev.obslouzeno_zakazniku} | Tajné kompro materiály: {nev.kompro_materialy} 📜{NC}\n")

        print(f"{YELLOW}--- Dívky na pokojích ---{NC}")
        if divky_v_nev:
            for i, d in enumerate(divky_v_nev, 1):
                p_num = getattr(d, "pokoj_nevestinec", i)
                spec_klic = nev.ziskej_specializaci(p_num)
                spec_info = SPECIALIZACE_POKOJU.get(spec_klic, SPECIALIZACE_POKOJU["klasicky"])
                vynos = spocitej_denni_vynos_divky(d, nev)
                char = CHARAKTERY.get(d.charakter, {}).get("nazev", d.charakter)
                shoda = " ★ (Specializace ladí!)" if d.charakter in spec_info.get("bonus_charakteru", []) else ""
                print(f"  {BOLD}Pokoj #{p_num}{NC} [{spec_info['nazev']}]: {BOLD}{d.jmeno}{NC} [{char}] – Denní tržba: {GOLD}~{vynos} 🪙{NC}{GREEN}{shoda}{NC}")
        else:
            print("  (Žádná dívka zde právě nepracuje)")

        print(f"\n{GOLD}{BOLD}╔════ 🛎️ OBSLUHA & HOSTÉ ══════════════════╗{NC}   {MAGENTA}{BOLD}╔════ 🏰 BUDOVA & MANAGEMENT ════════════╗{NC}")
        print(f"║ {GREEN} 1){NC} ➕ Přidat dívku na pokoj             ║   ║ {MAGENTA} 4){NC} 🏗️ Vylepšit budovu a ochranku      ║")
        print(f"║ {CYAN} 2){NC} ➖ Vrátit dívku do Černé pevnosti    ║   ║ {YELLOW} 5){NC} 🎨 Přestavba & specializace pokojů ║")
        print(f"║ {GOLD} 3){NC} 👑 VIP Mecenáši & Exkluzivní audience ║   ║ {CYAN} 6){NC} 📜 Špionáž & vydírání z kompra     ║")
        print(f"║ {RED} 7){NC} 🎭 Noční festival (Noc neřesti)      ║   ║ {GREEN} 8){NC} 🛁 Wellness lázeň a výcvik dívek   ║")
        print(f"║ {GOLD} 9){NC} 💰 Prodat otrokyni mecenáši (trvalé) ║   ║ {WHITE} 0){NC} 🚪 Odejít zpět                      ║")
        print(f"{GOLD}{BOLD}╚════════════════════════════════════════╝{NC}   {MAGENTA}{BOLD}╚════════════════════════════════════════╝{NC}")

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
            vip_zakazky(hra)
        elif volba == "4":
            vylepsi_nevestinec(hra)
        elif volba == "5":
            specializovat_pokoje(hra)
        elif volba == "6":
            spionaz_a_kompro(hra)
        elif volba == "7":
            noc_neresti_festival(hra)
        elif volba == "8":
            pece_o_divky(hra)
        elif volba == "9":
            prodat_otrokyni(hra)


def spocitej_denni_vynos_divky(otrok, nev) -> int:
    zaklad = 20 + int(otrok.touha * 0.35) + int(otrok.vlhkost * 0.25) + int(otrok.faze_zkazenosti * 15)
    char = getattr(otrok, "charakter", "")

    # Archetypální násobky
    if char == "sukuba_hybrid":
        zaklad = int(zaklad * 1.55)
    elif char == "princezna_ruin":
        zaklad = int(zaklad * 1.5)
    elif char == "kurtizana":
        zaklad = int(zaklad * 1.4)
    elif char == "slechticna":
        zaklad = int(zaklad * 1.35)
    elif char == "knezka_temnoty":
        zaklad = int(zaklad * 1.3)
    elif char == "nymfomanka":
        zaklad = int(zaklad * 1.25)
    elif char == "zlodejka":
        zaklad = int(zaklad * 1.2)

    # Specializace pokoje dívky
    p_num = getattr(otrok, "pokoj_nevestinec", 1)
    spec_typ = nev.ziskej_specializaci(p_num)
    spec_data = SPECIALIZACE_POKOJU.get(spec_typ, SPECIALIZACE_POKOJU["klasicky"])
    nasobek_pokoje = spec_data.get("bonus_vynosu", 1.0)

    # Bonus za perfektní shodu charakteru s pokojem
    if char in spec_data.get("bonus_charakteru", []):
        nasobek_pokoje += 0.35

    nasobek_luxusu = 1.0 + (nev.uroven_luxusu - 1) * 0.2
    return max(15, int(zaklad * nasobek_pokoje * nasobek_luxusu))


def vypocti_denni_prijem(hra) -> int:
    if not hasattr(hra, "nevestinec") or not hra.nevestinec.otevreno:
        return 0
    nev = hra.nevestinec
    aktivni = hra.harem.vsechny_aktivni()
    divky_v_nev = [o for o in aktivni if getattr(o, "v_nevestinci", False)]
    if not divky_v_nev:
        return 0

    celkem = 0
    extra_temno = 0
    extra_sex = 0
    extra_zlato_zlodejky = 0

    for d in divky_v_nev:
        vynos = spocitej_denni_vynos_divky(d, nev)
        celkem += vynos

        p_num = getattr(d, "pokoj_nevestinec", 1)
        spec_typ = nev.ziskej_specializaci(p_num)

        # Generování esencí z tematických pokojů a charakterů
        if spec_typ == "bdsm" or d.charakter == "knezka_temnoty":
            extra_temno += 3
        if spec_typ == "krypta" or d.charakter == "carodejka":
            extra_temno += 4
        if d.charakter == "sukuba_hybrid":
            extra_sex += 5

        # Zlodějka krade opilým hostům
        if d.charakter == "zlodejka":
            extra_zlato_zlodejky += random.randint(20, 50)

        # Špionáž a sběr kompra
        if d.charakter in ("zlodejka", "kurtizana", "manipulativni"):
            if random.random() < 0.35:
                nev.kompro_materialy += 1

        # Vývoj dívky po noci
        d.touha = min(100, d.touha + 2)
        d.poslusnost = min(100, d.poslusnost + 1)
        if random.random() < 0.25:
            d.faze_zkazenosti = min(4, d.faze_zkazenosti + 1)

    # Připsání extra bonusů
    if extra_temno > 0:
        hra.hrac.dark_energy = min(hra.hrac.max_temno(), hra.hrac.dark_energy + extra_temno)
        tisk_info(f"🌑 Pokoje neřesti a temné kněžky ti v noci přinesly +{extra_temno} temné energie!")
    if extra_sex > 0:
        hra.hrac.sex_energy = min(hra.hrac.max_sex(), hra.hrac.sex_energy + extra_sex)
        tisk_info(f"⚡ Sukuba v nevěstinci přelila sexuální rozkoš přímo do tebe (+{extra_sex} sexuální energie)!")
    if extra_zlato_zlodejky > 0:
        celkem += extra_zlato_zlodejky
        tisk_ok(f"💰 Tvé stínové zlodějky v noci obraly opilé šlechtice o extra +{extra_zlato_zlodejky} 🪙!")

    nev.celkovy_zisk += celkem
    nev.obslouzeno_zakazniku += len(divky_v_nev) * random.randint(3, 5)

    # Obnova VIP nabídek pro další den
    nev.vip_nabidky = []
    _generuj_vip_nabidky(hra)

    return celkem
