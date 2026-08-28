# game/manzelstvi.py
import random
from config import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GOLD, BOLD, WHITE, NC
from models.marriage import Marriage
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from data.jmena import JMENA

def je_mozne_zasnoubeni(otrokyne, hrac):
    """Kontrola, zda lze zasnoubení uskutečnit."""
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
    """Kontrola, zda lze uskutečnit svatbu (min. 10 dní od zasnoubení)."""
    if marriage.je_vdana():
        return False, "Již jsou vdaní"
    if den - marriage.den_zasnubin < 10:
        zbyva = 10 - (den - marriage.den_zasnubin)
        return False, f"Čekejte ještě {zbyva} dní"
    return True, "OK"

def je_mozne_potomstvo(marriage, den):
    """Kontrola možnosti mít dítě."""
    if not marriage.je_vdana():
        return False, "Nejsou v manželství"
    if marriage.ma_dite():
        # Max jedno dítě za 2 roky (60 dní)
        if den - (marriage.den_svatby + 60 * (marriage.pocet_deti())) < 60:
            return False, "Musíte čekat min. 60 dní mezi dětmi"
    return True, "OK"

def zasnoubeni(otrokyne, hrac, hra):
    """Provedení zasnoubení."""
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
    """Uskutečnění svatby."""
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
    
    # Generování krásy svatby (0-100)
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
    
    return True

def mat_dite(otrokyne, marriage, hrac, hra):
    """Generování dítěte."""
    mozne, zprava = je_mozne_potomstvo(marriage, hra.hrac.den)
    if not mozne:
        tisk_chyba(f"Dítě není možné: {zprava}")
        return False
    
    jmeno_ditete = random.choice(JMENA)
    if random.random() < 0.5:
        jmeno_ditete = jmeno_ditete.replace("a", "o")  # Zjednodušené "mužské" jméno
    
    dite = marriage.prida_dite(jmeno_ditete)
    
    # Bonusy za potomstvo
    hrac.sex_energy = min(100, hrac.sex_energy + 10)
    hrac.dark_energy = min(100, hrac.dark_energy + 5)
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
    """Rozvedení."""
    if otrokyne.jmeno not in hra.marriage_system:
        tisk_chyba("Nejste v manželství.")
        return False
    
    marriage = hra.marriage_system[otrokyne.jmeno]
    
    # Veta za rozvod
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
    tisk_info(
        f"Zaplatili jste {veta} 🪙 | "
        f"Loajalita -{40}%"
    )
    return True

def zobraz_postaveni_partnerstvi(otrokyne, marriage):
    """Zobrazí status manželství."""
    clear()
    print(f"{GOLD}{BOLD}=== Manželství {otrokyne.jmeno} ==={NC}\n")
    
    if marriage.je_vdana():
        print(f"{GREEN}Stav: Vdaná{NC}")
    elif marriage.je_rozvedena():
        print(f"{RED}Stav: Rozvedena{NC}")
    else:
        print(f"{YELLOW}Stav: Zasnoubená{NC}")
    
    print(f"Zasnoubeni: Den {marriage.den_zasnubin}")
    if marriage.den_svatby:
        print(f"Svatba: Den {marriage.den_svatby}")
        print(f"Krása ceremonie: {marriage.cerem_puvab}%")
    
    print(f"Intimita: {marriage.intimita_level}%")
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

def menu_manzelstvi(hra):
    """Hlavní menu pro manželství."""
    aktivni = hra.harem.vsechny_aktivni()
    
    if not aktivni:
        tisk_chyba("Nemáš žádné otrokyně.")
        input("Enter...")
        return
    
    while True:
        clear()
        print(f"{GOLD}{BOLD}--- Manželství a Rodina ---{NC}\n")
        
        # Zobrazení současných partnerek
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
        
        else:
            tisk_chyba("Neplatná volba.")
            input("Enter...")
