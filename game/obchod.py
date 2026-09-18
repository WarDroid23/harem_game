# game/obchod.py — zjednodušený obchod + černý trh
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info, vytiskni_volbu
from config import GOLD, CYAN, MAGENTA, NC


def obchod(hra):
    clear()
    print(f"{GOLD}--- Obchod ---{NC}\n")
    vytiskni_volbu('1', 'Léčivý elixír (30 zl) — +20 HP')
    vytiskni_volbu('2', 'Stimulant (40 zl) — +15 sex energie')
    vytiskni_volbu('3', 'Temný katalyzátor (60 zl) — +15 temná energie')
    vytiskni_volbu('9', 'Černý trh')
    vytiskni_volbu('0', 'Zpět')
    try:
        volba = input("> ").strip()
    except EOFError:
        return
    if volba == "9":
        cerny_trh(hra)
        return
    if volba == "0":
        return
    hrac = hra.hrac
    if volba == "1" and hrac.gold >= 30:
        hrac.gold -= 30
        hrac.hp = min(hrac.max_hp, hrac.hp + 20)
        tisk_ok("Elixír vypit. HP +20.")
    elif volba == "2" and hrac.gold >= 40:
        hrac.gold -= 40
        max_s = hrac.max_sex() if hasattr(hrac, "max_sex") else 100
        hrac.sex_energy = min(max_s, hrac.sex_energy + 15)
        tisk_ok("Stimulant. Sex energie +15.")
    elif volba == "3" and hrac.gold >= 60:
        hrac.gold -= 60
        max_t = hrac.max_temno() if hasattr(hrac, "max_temno") else 100
        hrac.dark_energy = min(max_t, hrac.dark_energy + 15)
        tisk_ok("Temný katalyzátor. Temná energie +15.")
    else:
        tisk_chyba("Nelze koupit (zlato nebo volba).")
    try:
        input("Enter...")
    except EOFError:
        pass


def cerny_trh(hra):
    import random
    from game.kronika import zaznamenej
    from models.otrokyne import Otrokyně

    clear()
    print(f"{MAGENTA}--- Černý trh podsvětí ---{NC}")
    kor = getattr(hra.mafie, "korupce", 0)
    temno = getattr(hra.hrac, "dark_energy", 0)

    if kor < 20 and temno < 40:
        tisk_chyba("Podsvětí ti zatím nevěří (požadováno: korupce mafie ≥ 20% nebo temná energie ≥ 40).")
        try:
            input("Enter...")
        except EOFError:
            pass
        return

    print(f"Zlato: {hra.hrac.gold} 🪙 | Temná energie: {temno} | Korupce: {kor}%\n")
    vytiskni_volbu('1', 'Elixír temnoty (80 zl) — +20 temná energie')
    vytiskni_volbu('2', 'Okovy luxusu (120 zl) — +5 loajalita všem otrokyním')
    vytiskni_volbu('3', 'Sérum zlomené vůle (160 zl) — +25 poslušnost a +15 submisivita vybrané otrokyně')
    vytiskni_volbu('4', 'Inkviziční falešný odpustek (180 zl) — zahlazení stop před církví a inkvizicí')
    vytiskni_volbu('5', 'Pašerácká úmluva (220 zl) — dodávka kontrabandu (+300 🪙 okamžitě, +8 vliv ve městě)')
    vytiskni_volbu('6', 'Krvavý ametyst (350 zl) — krystal podsvětí: trvale +10 k max temné energii')
    vytiskni_volbu('7', 'Tajemná dražba z podsvětí (400 zl) — odkup vzácné exotické otrokyně')
    vytiskni_volbu('0', 'Zpět')

    try:
        v = input("> ").strip()
    except EOFError:
        return

    hrac = hra.hrac
    if v == "0":
        return

    if v == "1":
        if hrac.gold >= 80:
            hrac.gold -= 80
            if hasattr(hrac, "pridej_dark_energy"):
                hrac.pridej_dark_energy(20)
            else:
                max_t = hrac.max_temno() if hasattr(hrac, "max_temno") else 120
                hrac.dark_energy = min(max_t, hrac.dark_energy + 20)
            tisk_ok("Elixír temnoty vypit. Temná síla proudí v žilách (+20 temno).")
            zaznamenej(hra, "Černý trh: zakoupen Elixír temnoty.")
        else:
            tisk_chyba("Nedostatek zlata.")

    elif v == "2":
        if hrac.gold >= 120:
            hrac.gold -= 120
            aktivni = hra.harem.vsechny_aktivni()
            for o in aktivni:
                o.loajalita = min(100, o.loajalita + 5)
                o.poslusnost = min(100, getattr(o, "poslusnost", 30) + 5)
            tisk_ok(f"Okovy luxusu nasazeny. Harém ({len(aktivni)} dívek) je spoután vděkem i řetězy.")
            zaznamenej(hra, "Černý trh: nasazeny Okovy luxusu harému.")
        else:
            tisk_chyba("Nedostatek zlata.")

    elif v == "3":
        if hrac.gold >= 160:
            aktivni = hra.harem.vsechny_aktivni()
            if not aktivni:
                tisk_chyba("V harému nemáš žádné otrokyně.")
            else:
                print("\nVyber otrokyni pro aplikaci séra:")
                for i, o in enumerate(aktivni, 1):
                    print(f"{i}) {o.jmeno} (poslušnost: {o.poslusnost}, submisivita: {o.submisivita})")
                try:
                    vybrana_idx = int(input("> ")) - 1
                    if 0 <= vybrana_idx < len(aktivni):
                        hrac.gold -= 160
                        cil = aktivni[vybrana_idx]
                        cil.poslusnost = min(100, cil.poslusnost + 25)
                        cil.submisivita = min(100, cil.submisivita + 15)
                        cil.strach = max(0, getattr(cil, "strach", 30) - 10)
                        tisk_ok(f"Sérum aplikováno na {cil.jmeno}. Vůle se podlamuje, poslušnost stoupla na {cil.poslusnost}.")
                        zaznamenej(hra, f"Černý trh: sérum zlomené vůle podáno {cil.jmeno}.")
                    else:
                        tisk_chyba("Neplatná volba.")
                except ValueError:
                    tisk_chyba("Zadej číslo.")
        else:
            tisk_chyba("Nedostatek zlata.")

    elif v == "4":
        if hrac.gold >= 180:
            hrac.gold -= 180
            for u in getattr(hra.mafie, "uzemi", []):
                u.riziko_inkvizice = max(0, getattr(u, "riziko_inkvizice", 0) - 5)
            if hasattr(hra.mafie, "korupce"):
                hra.mafie.korupce = min(100, hra.mafie.korupce + 4)
            tisk_ok("Falešný církevní odpustek získán. Riziko inkvizice na územích kleslo, korupce stoupla.")
            zaznamenej(hra, "Černý trh: zakoupen falešný inkviziční odpustek.")
        else:
            tisk_chyba("Nedostatek zlata.")

    elif v == "5":
        if hrac.gold >= 220:
            hrac.gold -= 220
            hrac.gold += 300
            hra.mafie.vliv_ve_meste = min(100, getattr(hra.mafie, "vliv_ve_meste", 0) + 8)
            tisk_ok("Pašerácká dohoda uzavřena! Čistý zisk +80 🪙 a vliv mafie ve městě stoupl o +8%.")
            zaznamenej(hra, "Černý trh: uzavřena lukrativní pašerácká úmluva.")
        else:
            tisk_chyba("Nedostatek zlata.")

    elif v == "6":
        if hrac.gold >= 350:
            hrac.gold -= 350
            if hasattr(hrac, "zvys_max_temno"):
                hrac.zvys_max_temno(10)
            else:
                hrac.max_dark_energy = getattr(hrac, "max_dark_energy", 100) + 10
            hrac.dark_energy = getattr(hrac, "dark_energy", 0) + 10
            tisk_ok(f"Krvavý ametyst byl vstřebán tvou duší. Max temná energie trvale vzrostla (+10)!")
            zaznamenej(hra, "Černý trh: absorbován Krvavý ametyst (+10 max temno).")
        else:
            tisk_chyba("Nedostatek zlata.")

    elif v == "7":
        if hrac.gold >= 400:
            hrac.gold -= 400
            jmena_exoticka = ["Shae", "Azira", "Nefret", "Salma", "Kailani", "Sora"]
            jmeno = random.choice(jmena_exoticka)
            otrok = Otrokyně(jmeno=jmeno, vek=random.randint(20, 26))
            otrok.charakter = random.choice(["svůdnice", "subka", "zvrácená"])
            otrok.faze_zkazenosti = 3
            otrok.poslusnost = 55
            otrok.loajalita = 45
            otrok.touha = 70
            otrok.vlhkost = 65
            hra.harem.pridat(otrok)
            tisk_ok(f"★ Úspěšný příhoz v dražbě! Exotická otrokyně {jmeno} ({otrok.charakter}) byla doručena do tvé pevnosti.")
            zaznamenej(hra, f"Černý trh: z podsvětní dražby získána otrokyně {jmeno}.")
        else:
            tisk_chyba("Nedostatek zlata.")
    else:
        tisk_chyba("Neplatná volba.")

    try:
        input("Enter...")
    except EOFError:
        pass

