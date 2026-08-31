# game/verejny_vykon.py — veřejný výkon na trhu / přístavu
import random
from utils.vypis import clear, tisk_ok, tisk_chyba, tisk_info
from config import GOLD, MAGENTA, RED, CYAN, NC


def menu_verejneho_vykonu(hra):
    clear()
    print(f"{MAGENTA}--- Veřejný výkon ---{NC}\n")
    print("Ukážeš otrokyni městu. Reputace ↑, riziko inkvizice ↑, fáze rychleji.\n")
    try:
        aktivni = [o for o in hra.harem.vsechny_aktivni() if o.hp > 0]
    except Exception:
        aktivni = []
    if not aktivni:
        tisk_chyba("Nemáš otrokyně na výkon.")
        try:
            input("Enter...")
        except EOFError:
            pass
        return
    for i, o in enumerate(aktivni, 1):
        h = "★ " if getattr(o, "oblibena", False) else ""
        print(f"{i}) {h}{o.jmeno} (loajalita {o.loajalita}%, fáze {o.faze_zkazenosti})")
    print("0) Zpět")
    try:
        volba = input("> ").strip()
    except EOFError:
        return
    if volba == "0" or not volba.isdigit():
        return
    idx = int(volba) - 1
    if not (0 <= idx < len(aktivni)):
        tisk_chyba("Špatná volba.")
        return
    o = aktivni[idx]
    _proved(hra, o)
    try:
        input("Enter...")
    except EOFError:
        pass


def _proved(hra, o):
    hrac = hra.hrac
    if getattr(hrac, "sex_energy", 0) < 15:
        tisk_chyba("Málo sexuální energie (potřeba 15).")
        return
    hrac.sex_energy -= 15
    uspech = random.random() < (0.55 + o.loajalita / 200)
    if uspech:
        hrac.reputace_mesta = min(100, hrac.reputace_mesta + random.randint(3, 8))
        o.loajalita = min(100, o.loajalita + random.randint(2, 6))
        if hasattr(o, "faze_zkazenosti"):
            o.faze_zkazenosti = min(16, o.faze_zkazenosti + (1 if random.random() < 0.35 else 0))
        tisk_ok(f"{o.jmeno} zvládla veřejný výkon. Dav jásá. Reputace stoupla.")
    else:
        hrac.vliv_inkvizice = min(100, hrac.vliv_inkvizice + random.randint(4, 10))
        o.loajalita = max(0, o.loajalita - 5)
        tisk_chyba(f"Výkon selhal. Inkvizice si tě všimla. {o.jmeno} se stydí.")
    try:
        from game.kronika import zaznamenej
        zaznamenej(hra, f"Veřejný výkon: {o.jmeno}")
    except Exception:
        pass
    try:
        from game.ai_dialog import vypis_dialog
        vypis_dialog(o, hrac, "veřejný_výkon", nastaveni=getattr(hra, "nastaveni", None))
    except Exception:
        pass
