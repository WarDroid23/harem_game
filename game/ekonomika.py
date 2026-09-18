# game/ekonomika.py
import random
from data.klienti import KLIENTI, AUKCNI_DOBA
from models.hrac import Hrac
from models.otrokyne import Otrokyně
from utils.vypis import clear, tisk_ok, tisk_chyba
from game.balance import uprav_odmenu

def vernostni_bonus(hrac, klient_id):
    if klient_id not in hrac.klient_vernost:
        return 1.0, 0
    v = hrac.klient_vernost[klient_id]
    level = v.get("level", 0)
    multi = {0: 1.0, 1: 1.08, 2: 1.15, 3: 1.25, 4: 1.40, 5: 1.60}.get(level, 1.0)
    sleva = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20, 5: 30}.get(level, 0)
    return multi, sleva

def pridej_vernost_xp(hrac, klient_id, xp=15):
    if klient_id not in hrac.klient_vernost:
        hrac.klient_vernost[klient_id] = {"level": 0, "xp": 0, "rentals": 0}
    v = hrac.klient_vernost[klient_id]
    v["xp"] += xp
    v["rentals"] += 1
    while v["xp"] >= (v["level"] + 1) * 40 and v["level"] < 5:
        v["xp"] -= (v["level"] + 1) * 40
        v["level"] += 1
        print(f"★ Věrnost klienta vzrostla na úroveň {v['level']}!")


def spocitej_cenu_najmu(hrac: Hrac, otrok: Otrokyně, klient_id: str, obtiznost="normalni"):
    """Vrátí odměnu za jeden den nájmu bez změny herního stavu."""
    klient = KLIENTI.get(klient_id)
    if klient is None:
        return None
    zaklad = 20 + otrok.submisivita + otrok.poslusnost
    cena = int(zaklad * klient["multi"] * (1 + hrac.aukcni_bonus / 100))
    if hrac.reputace_mesta < 0:
        cena = int(cena * 0.9)
    multi, sleva = vernostni_bonus(hrac, klient_id)
    cena = int(cena * multi * (1 - sleva / 100))
    return uprav_odmenu(cena, obtiznost)


def proved_najem_otrokyně(
    hrac: Hrac,
    otrok: Otrokyně,
    klient_id: str,
    doba_volba: str = "kratka",
    obtiznost="normalni",
):
    """Provede nájem bez menu; určeno pro automatiku a další systémové akce."""
    klient = KLIENTI.get(klient_id)
    if klient is None or doba_volba not in AUKCNI_DOBA:
        return False
    if otrok.hp <= 0 or otrok.na_najmu:
        return False

    cena = spocitej_cenu_najmu(hrac, otrok, klient_id, obtiznost)
    dny = random.randint(*AUKCNI_DOBA[doba_volba])
    otrok.na_najmu = True
    otrok.klient = klient_id
    otrok.typ_najmu = doba_volba
    otrok.dny_na_najmu = 0
    otrok.najem_zbyva_dni = dny
    otrok.najem_prijem_celkem = cena * dny
    hrac.gold += otrok.najem_prijem_celkem

    for stat, hodnota in klient["efekty"].items():
        otrok.zvysit_stat(stat, hodnota)
    hrac.reputace_mesta += 1
    pridej_vernost_xp(hrac, klient_id)
    if random.random() < klient.get("riziko", 0):
        hrac.vliv_inkvizice = min(100, hrac.vliv_inkvizice + 2)
        tisk_chyba("Rizikový klient přitáhl pozornost inkvizice (+2 vliv).")
    tisk_ok(
        f"Otrokyně {otrok.jmeno} pronajata klientovi {klient['jmeno']} "
        f"na {dny} dní za {otrok.najem_prijem_celkem} zlaťáků."
    )
    return True


def najem_otrokyně(hrac: Hrac, otrok: Otrokyně, obtiznost="normalni"):
    clear()
    print("Dostupní klienti:")
    for klic, klient in KLIENTI.items():
        print(f"{klic}: {klient['jmeno']} (multi x{klient['multi']})")
    volba = input("Vyber klienta (id): ").strip().lower()
    if volba not in KLIENTI:
        tisk_chyba("Neplatný klient.")
        return

    klient = KLIENTI[volba]
    if otrok.hp <= 0:
        tisk_chyba("Tato otrokyně není v dostatečném stavu pro nájem.")
        return False
    if otrok.na_najmu:
        tisk_chyba("Otrokyně je již na najmu.")
        return False

    doba_volba = input("Doba najmu (kratka/stredni/dlouha): ").strip().lower()
    if doba_volba not in AUKCNI_DOBA:
        tisk_chyba("Neplatná doba.")
        return
    uspech = proved_najem_otrokyně(
        hrac, otrok, volba, doba_volba, obtiznost
    )
    try:
        input("Enter...")
    except EOFError:
        pass
    return uspech


proved_najem_otrokyn = proved_najem_otrokyně
