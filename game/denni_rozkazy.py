# game/denni_rozkazy.py — ranní režim harému
from utils.vypis import clear, tisk_ok, tisk_info, tisk_chyba
from config import GOLD, GREEN, RED, CYAN, MAGENTA, NC

REZIMY = {
    "tvrdy": {
        "nazev": "Tvrdý režim",
        "popis": "Disciplína, tresty, rychlejší fáze zkázanosti, −loajalita slabším.",
        "mod": -2,
        "faze_bonus": 1,
    },
    "laskavy": {
        "nazev": "Laskavý režim",
        "popis": "Péče, odměny, +loajalita, pomalejší temnota.",
        "mod": 3,
        "faze_bonus": 0,
    },
    "vystavni": {
        "nazev": "Výstavní režim",
        "popis": "Krása a výkon. +reputace města, vyšší riziko inkvizice.",
        "mod": 1,
        "faze_bonus": 0,
        "reputace": 2,
        "inkvizice": 1,
    },
}


def aktualni_rezim(hra):
    return getattr(hra, "denni_rezim", "laskavy")


def nastav_rezim(hra, klic):
    if klic not in REZIMY:
        return False
    hra.denni_rezim = klic
    return True


def aplikuj_rezim_na_den(hra):
    klic = aktualni_rezim(hra)
    info = REZIMY.get(klic, REZIMY["laskavy"])
    zpravy = []
    try:
        aktivni = hra.harem.vsechny_aktivni()
    except Exception:
        return zpravy
    for o in aktivni:
        if o.hp <= 0:
            continue
        mod = info.get("mod", 0)
        if mod:
            stara = getattr(o, "loajalita", 50)
            o.loajalita = max(0, min(100, stara + mod))
    if info.get("reputace"):
        hra.hrac.reputace_mesta = min(100, hra.hrac.reputace_mesta + info["reputace"])
        zpravy.append(f"Výstavní den: reputace +{info['reputace']}")
    if info.get("inkvizice"):
        hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + info["inkvizice"])
        zpravy.append(f"Inkvizice si všimla výstavního harému (+{info['inkvizice']})")
    zpravy.append(f"Režim harému: {info['nazev']}")
    return zpravy


def menu_rozkazu(hra):
    clear()
    print(f"{GOLD}--- Denní rozkazy harému ---{NC}\n")
    akt = aktualni_rezim(hra)
    for i, (k, v) in enumerate(REZIMY.items(), 1):
        mark = " ← aktivní" if k == akt else ""
        print(f"{i}) {v['nazev']}{mark}")
        print(f"   {v['popis']}")
    print("0) Zpět")
    try:
        volba = input("> ").strip()
    except EOFError:
        return
    mapa = {str(i): k for i, k in enumerate(REZIMY.keys(), 1)}
    if volba in mapa:
        nastav_rezim(hra, mapa[volba])
        tisk_ok(f"Rozkaz nastaven: {REZIMY[mapa[volba]]['nazev']}")
        try:
            from game.kronika import zaznamenej
            zaznamenej(hra, f"Denní rozkaz: {REZIMY[mapa[volba]]['nazev']}")
        except Exception:
            pass
    try:
        input("Enter...")
    except EOFError:
        pass
