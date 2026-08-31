# game/nocni_eventy.py — scény po odpočinku
import random
from utils.vypis import tisk_ok, tisk_chyba, tisk_info
from config import MAGENTA, RED, GOLD, CYAN, NC


def _aktivni(hra):
    try:
        return [o for o in hra.harem.vsechny_aktivni() if o.hp > 0]
    except Exception:
        return []


def spust_nocni_eventy(hra):
    zpravy = []
    aktivni = _aktivni(hra)
    if not aktivni:
        return zpravy

    z = _zarlivost_star_manzelka(hra, aktivni)
    if z:
        zpravy.extend(z)

    z = _zradkyne(hra, aktivni)
    if z:
        zpravy.extend(z)

    if random.random() < 0.45:
        z = _nahodna_scena(hra, aktivni)
        if z:
            zpravy.extend(z)

    if getattr(hra.hrac, "vliv_inkvizice", 0) >= 55 and random.random() < 0.35:
        zpravy.extend(_razie_inkvizice(hra, aktivni))

    try:
        from game.kronika import zaznamenej
        for msg in zpravy:
            zaznamenej(hra, msg)
    except Exception:
        pass
    return zpravy


def _zarlivost_star_manzelka(hra, aktivni):
    star = next((o for o in aktivni if getattr(o, "oblibena", False)), None)
    manz = next(
        (o for o in aktivni if getattr(o, "je_manzelkou", False) or getattr(o, "partnerka", False)),
        None,
    )
    if not star or not manz or star is manz:
        return []
    if random.random() > 0.4:
        return []
    volby = [
        f"★ {star.jmeno} žárlí na manželku {manz.jmeno}. Napětí v komnatách.",
        f"{manz.jmeno} ti šeptá, že ★ {star.jmeno} je jen hračka — ne partnerka.",
        f"★ {star.jmeno} a {manz.jmeno} se v noci střetly. Krev nebyla, ale hrdost ano.",
    ]
    msg = random.choice(volby)
    star.loajalita = max(0, min(100, star.loajalita + random.randint(-5, 5)))
    manz.loajalita = max(0, min(100, manz.loajalita + random.randint(-5, 5)))
    return [msg]


def _zradkyne(hra, aktivni):
    kandidatky = [
        o for o in aktivni
        if getattr(o, "loajalita", 50) < 25
        and getattr(o, "faze_zkazenosti", 0) >= 8
        and not getattr(o, "oblibena", False)
        and not getattr(o, "je_manzelkou", False)
    ]
    if not kandidatky or random.random() > 0.25:
        return []
    o = random.choice(kandidatky)
    hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + random.randint(5, 12))
    o.loajalita = max(0, o.loajalita - 10)
    return [
        f"{RED}Zrádkyně:{NC} {o.jmeno} se pokusila prozradit tvé impérium inkvizici. "
        f"Vliv inkvizice stoupl. Zvaž trest."
    ]


def _nahodna_scena(hra, aktivni):
    o = random.choice(aktivni)
    sceny = [
        f"V noci cítíš dech u postele — {o.jmeno} přišla bez dovolení. Čeká na rozkaz.",
        f"{o.jmeno} šeptá ve spánku tvé jméno. Loajalita se chvěje.",
        f"Slyšíš sténání z harému. {o.jmeno} se „cvičí“ na tebe.",
        f"★ stín ve dveřích: {o.jmeno} drží lucernu a ptá se, jestli smí zůstat.",
    ]
    if getattr(o, "oblibena", False):
        sceny.append(f"★ {o.jmeno} spí u tebe. Ráno je energie o něco sladší.")
        hra.hrac.sex_energy = min(
            hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100,
            hra.hrac.sex_energy + 5,
        )
    return [random.choice(sceny)]


def _razie_inkvizice(hra, aktivni):
    msg = [f"{RED}Inkviziční razie!{NC} Hlídky prohledávají okolí dominia."]
    if hra.hrac.gold >= 150 and random.random() < 0.5:
        hra.hrac.gold -= 150
        hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 8)
        msg.append("Zaplatil jsi úplatek strážím (−150 zl). Krize zažehnána.")
    else:
        zranene = random.sample(aktivni, k=min(2, len(aktivni)))
        for o in zranene:
            o.hp = max(1, o.hp - random.randint(10, 25))
        jmena = ", ".join(o.jmeno for o in zranene)
        msg.append(f"Několik otrokyň utrpělo při razie: {jmena}.")
        hra.hrac.reputace_mesta = max(-100, hra.hrac.reputace_mesta - 5)
    return msg
