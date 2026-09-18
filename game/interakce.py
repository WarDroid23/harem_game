# game/interakce.py
import random
from data.interakce import INTERAKCE
from data.charaktery import CHARAKTERY, nazev_charakteru
from utils.vypis import hlavicka, clear, tisk_ok, tisk_chyba, tisk_info, vytiskni_volbu
from models.otrokyne import Otrokyně
from models.hrac import Hrac

def proved_interakci(otrok: Otrokyně, hrac: Hrac, akce_id: str):
    akce = next((a for a in INTERAKCE if a["id"] == akce_id), None)
    if not akce:
        tisk_chyba("Neznámá akce.")
        return False

    if hrac.sex_energy < akce.get("cena_energie", 0):
        tisk_chyba("Nedostatek sexuální energie.")
        return False
    if hrac.dark_energy < akce.get("cena_temnoty", 0):
        tisk_chyba("Nedostatek temné energie.")
        return False

    hrac.sex_energy -= akce.get("cena_energie", 0)
    hrac.dark_energy -= akce.get("cena_temnoty", 0)

    charakter_data = CHARAKTERY.get(otrok.charakter, CHARAKTERY["subka"])
    mod = charakter_data.get("modifikatory", {})

    for stat, hodnota in akce["efekty"].items():
        mod_hodnota = int(hodnota * mod.get(stat, 1.0))
        otrok.zvysit_stat(stat, mod_hodnota)

    if akce.get("typ") == "trest":
        otrok.zvysit_stat("submisivita", int(3 * charakter_data.get("reakce_na_trest", 1.0)))
        otrok.zvysit_stat("strach", int(2 * charakter_data.get("reakce_na_trest", 1.0)))
    elif akce.get("typ") == "odmena":
        otrok.zvysit_stat("loajalita", int(2 * charakter_data.get("reakce_na_odmenu", 1.0)))
        otrok.zvysit_stat("duvera", int(2 * charakter_data.get("reakce_na_odmenu", 1.0)))

    if otrok.charakter in ["vzdorna", "odvazna"]:
        if random.random() < charakter_data.get("utek_sance", 0.1):
            tisk_chyba(f"{otrok.jmeno} se pokusila o útěk!")
            return False

    if "vliv_inkvizice" in akce:
        hrac.vliv_inkvizice = min(100, hrac.vliv_inkvizice + akce["vliv_inkvizice"])

    if random.random() < akce.get("riziko", 0):
        otrok.zvysit_stat("hp", -random.randint(1, 10))
        tisk_chyba("Stala se nepříjemná událost!")

    otrok.aktualizuj_fazi()
    otrok.zaznamenej_volbu("interakce", akce["nazev"])
    tisk_ok(f"Provedeno: {akce['nazev']} (charakter: {nazev_charakteru(getattr(otrok, 'charakter', 'subka'))})")
    try:
        from game.ai_dialog import vypis_dialog, typ_z_akce
        nast = getattr(hrac, "_nastaveni_ref", None)
        vypis_dialog(otrok, hrac, typ_z_akce(akce), nastaveni=nast)
    except Exception:
        pass
    return True

def zobraz_interakce(otrok, hrac, nastaveni=None):
    from game.tresty_odmeny import menu_trestu, menu_odmen
    from game.drogy import menu_drog
    if nastaveni is not None:
        hrac._nastaveni_ref = nastaveni
    while True:
        clear()
        hlavicka(f'Interakce s {otrok.jmeno}')
        print(f"HP: {otrok.hp} | Touha: {otrok.touha} | Submisivita: {otrok.submisivita}")
        print(f"Energie: {hrac.sex_energy} | Temná energie: {hrac.dark_energy}\n")
        for i, akce in enumerate(INTERAKCE, 1):
            print(f"{i}) {akce['nazev']} (E:{akce.get('cena_energie',0)} T:{akce.get('cena_temnoty',0)})")
        vytiskni_volbu('98', 'Drogy')
        vytiskni_volbu('99', 'Tresty/odměny')
        vytiskni_volbu('0', 'Zpět')
        volba = input("> ")
        if volba == "0":
            break
        elif volba == "98":
            menu_drog(otrok, hrac)
        elif volba == "99":
            while True:
                clear()
                hlavicka(f'Tresty / Odměny pro {otrok.jmeno}')
                vytiskni_volbu('1', 'Tresty')
                vytiskni_volbu('2', 'Odměny')
                vytiskni_volbu('0', 'Zpět')
                volba2 = input("> ")
                if volba2 == "1":
                    menu_trestu(otrok, hrac)
                elif volba2 == "2":
                    menu_odmen(otrok, hrac)
                elif volba2 == "0":
                    break
        else:
            try:
                idx = int(volba) - 1
                if 0 <= idx < len(INTERAKCE):
                    proved_interakci(otrok, hrac, INTERAKCE[idx]["id"])
                else:
                    tisk_chyba("Špatná volba.")
            except ValueError:
                tisk_chyba("Zadej číslo.")
        input("Enter...")

def zobraz_hromadne_interakce(otrokyne, hrac):
    """Provede stejnou bezpečnou interakci na všech vybraných postavách."""
    if not otrokyne:
        tisk_chyba("Nemáš žádné aktivní postavy.")
        return

    while True:
        clear()
        hlavicka('Hromadná interakce se všemi otrokyněmi')
        print(f"Počet postav: {len(otrokyne)}")
        for i, akce in enumerate(INTERAKCE, 1):
            print(
                f"{i}) {akce['nazev']} "
                f"(E:{akce.get('cena_energie', 0)} "
                f"T:{akce.get('cena_temnoty', 0)} za osobu)"
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
        if not 0 <= index < len(INTERAKCE):
            tisk_chyba("Špatná volba.")
            input("Enter...")
            continue

        akce = INTERAKCE[index]
        cena_energie = akce.get("cena_energie", 0) * len(otrokyne)
        cena_temnoty = akce.get("cena_temnoty", 0) * len(otrokyne)
        if hrac.sex_energy < cena_energie or hrac.dark_energy < cena_temnoty:
            tisk_chyba(
                f"Nemáš dost energie pro všechny. Potřebuješ "
                f"E:{cena_energie}, T:{cena_temnoty}."
            )
            input("Enter...")
            continue

        for otrok in otrokyne:
            proved_interakci(otrok, hrac, akce["id"])
        tisk_ok(f"Interakce „{akce['nazev']}“ proběhla u všech postav.")
        input("Enter...")
        return
