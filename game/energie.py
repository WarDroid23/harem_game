"""Doplňkové způsoby obnovy energií hráče."""

from config import CYAN, GOLD, GREEN, MAGENTA, NC
from utils.vypis import clear, tisk_chyba, tisk_info, tisk_ok

MAX_ENERGIE = 100


def _zbyva(hrac, atribut):
    return max(0, MAX_ENERGIE - getattr(hrac, atribut))


def _lze_pouzit(hrac, akce_id):
    if hrac.dobiti_dnes.get(akce_id, 0):
        tisk_info("Tuto možnost jsi dnes už využil. Zkus to znovu po odpočinku.")
        return False
    return True


def _oznac_pouziti(hrac, akce_id):
    hrac.dobiti_dnes[akce_id] = hrac.dobiti_dnes.get(akce_id, 0) + 1


def hostinec(hra):
    """Levné jídlo a pití obnoví hlavně sexuální energii."""
    hrac = hra.hrac
    cena = 35
    if hrac.gold < cena:
        tisk_chyba("Na nocleh v hostinci nemáš dost zlata.")
        return False
    if not _lze_pouzit(hrac, "hostinec"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False

    hrac.gold -= cena
    hrac.sex_energy = min(MAX_ENERGIE, hrac.sex_energy + 28)
    hrac.dark_energy = min(MAX_ENERGIE, hrac.dark_energy + 8)
    hrac.hp = min(hrac.max_hp, hrac.hp + 10)
    _oznac_pouziti(hrac, "hostinec")
    tisk_ok("Hostinský ti naservíroval vydatné jídlo. Sexuální energie +28, temná +8.")
    return True


def lazne(hra):
    """Regenerační procedura v městských lázních."""
    hrac = hra.hrac
    cena = 60
    if hrac.gold < cena:
        tisk_chyba("Na proceduru v lázních nemáš dost zlata.")
        return False
    if not _lze_pouzit(hrac, "lazne"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False

    hrac.gold -= cena
    hrac.sex_energy = min(MAX_ENERGIE, hrac.sex_energy + 20)
    hrac.dark_energy = min(MAX_ENERGIE, hrac.dark_energy + 22)
    hrac.hp = min(hrac.max_hp, hrac.hp + 30)
    _oznac_pouziti(hrac, "lazne")
    tisk_ok("Lázeňská pára uvolnila tělo i mysl. Sexuální energie +20, temná +22, HP +30.")
    return True


def meditace(hra):
    """Jednou za den lze soustředěním získat temnou energii bez zlata."""
    hrac = hra.hrac
    if not _lze_pouzit(hrac, "meditace"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False

    bonus_temna = 28 if hra.svet.aktualni_lokace == "haj_soumraku" else 18
    hrac.sex_energy = min(MAX_ENERGIE, hrac.sex_energy + 5)
    hrac.dark_energy = min(MAX_ENERGIE, hrac.dark_energy + bonus_temna)
    _oznac_pouziti(hrac, "meditace")
    tisk_ok(f"Zklidnil jsi dech. Sexuální energie +5, temná +{bonus_temna}.")
    return True


def zahrada(hra):
    """Klidný rozhovor v zahradě obnoví energii a nevyžaduje zlato."""
    hrac = hra.hrac
    if not _lze_pouzit(hrac, "zahrada"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.sex_energy = min(MAX_ENERGIE, hrac.sex_energy + 24)
    hrac.dark_energy = min(MAX_ENERGIE, hrac.dark_energy + 6)
    hrac.hp = min(hrac.max_hp, hrac.hp + 8)
    _oznac_pouziti(hrac, "zahrada")
    tisk_ok("Ve Skleněné zahradě jste si odpočinuli v bezpečném tichu. Energie +24/+6, HP +8.")
    return True


def observator(hra):
    """Pozorování oblohy v observatoři obnoví soustředění."""
    hrac = hra.hrac
    if not _lze_pouzit(hrac, "observator"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.sex_energy = min(MAX_ENERGIE, hrac.sex_energy + 8)
    hrac.dark_energy = min(MAX_ENERGIE, hrac.dark_energy + 30)
    _oznac_pouziti(hrac, "observator")
    tisk_ok("Čočky observatoře zaostřily tvou mysl. Energie +8/+30.")
    return True


def molo(hra):
    """Krátká směna na molu dá sílu za cenu zásob."""
    hrac = hra.hrac
    cena = 25
    if hrac.gold < cena:
        tisk_chyba("Na čaj a světla pro směnu na molu nemáš dost zlata.")
        return False
    if not _lze_pouzit(hrac, "molo"):
        return False
    if _zbyva(hrac, "sex_energy") == 0 and _zbyva(hrac, "dark_energy") == 0:
        tisk_info("Obě energie už máš plné.")
        return False
    hrac.gold -= cena
    hrac.sex_energy = min(MAX_ENERGIE, hrac.sex_energy + 16)
    hrac.dark_energy = min(MAX_ENERGIE, hrac.dark_energy + 16)
    _oznac_pouziti(hrac, "molo")
    tisk_ok("Směna na Měsíčním molu skončila. Energie +16/+16.")
    return True


def zobraz_menu(hra):
    """Nabídne obnovu dostupnou v aktuální lokaci."""
    while True:
        clear()
        hrac = hra.hrac
        print(f"{MAGENTA}--- Dobití energií ---{NC}\n")
        print(
            f"{CYAN}Sexuální energie: {hrac.sex_energy}/100 | "
            f"Temná energie: {hrac.dark_energy}/100{NC}"
        )
        lokace = hra.svet.aktualni_lokace
        print(f"Místo: {lokace}")
        print("\nDostupné možnosti:")
        moznosti = [("1", "Meditace (zdarma, 1x denně)")]
        if lokace == "hostinec":
            moznosti.append(("2", "Hostinec (35 zlata, energie a HP)"))
        if lokace == "lazne":
            moznosti.append(("3", "Lázně (60 zlata, energie a HP)"))
        moznosti.append(("4", "Alchymie (lektvary z vyrobených surovin)"))
        if lokace == "sklenena_zahrada":
            moznosti.append(("5", "Klidný rozhovor v zahradě (1x denně)"))
        if lokace == "observator":
            moznosti.append(("6", "Pozorování oblohy (1x denně)"))
        if lokace == "molo_mesicniho_pristavu":
            moznosti.append(("7", "Směna na molu (25 zlata, 1x denně)"))
        for cislo, popis in moznosti:
            print(f"{cislo}) {popis}")
        print("0) Zpět")

        volba = input("> ").strip()
        if volba == "0":
            return
        if volba == "1":
            meditace(hra)
        elif volba == "2" and lokace == "hostinec":
            hostinec(hra)
        elif volba == "3" and lokace == "lazne":
            lazne(hra)
        elif volba == "4":
            hra.alchymie.zobraz_menu(hra.hrac, hra.harem)
        elif volba == "5" and lokace == "sklenena_zahrada":
            zahrada(hra)
        elif volba == "6" and lokace == "observator":
            observator(hra)
        elif volba == "7" and lokace == "molo_mesicniho_pristavu":
            molo(hra)
        else:
            tisk_chyba("Tato možnost zde není dostupná.")
        input("Enter...")
