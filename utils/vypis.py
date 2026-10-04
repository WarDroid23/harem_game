# utils/vypis.py
import os
import re
import sys
import unicodedata
import logging
from config import (
    NC, GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, GOLD, ORANGE, VIOLET,
    WHITE, GRAY, BOLD, DIM,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def clear():
    """Rychlé smazání – ANSI bez shellu, fallback na cls/clear."""
    try:
        from utils.term_render import clear_fast
        clear_fast()
        return
    except Exception:
        logging.getLogger(__name__).debug(
            "Rychlé vymazání terminálu selhalo; používá se systémový fallback.",
            exc_info=True,
        )
    os.system("cls" if os.name == "nt" else "clear")


def barva(text, barva_kod):
    return f"{barva_kod}{text}{NC}"


def tisk_ok(text):
    print(barva(f"✔ {text}", GREEN))


def tisk_chyba(text):
    print(barva(f"✖ {text}", RED))


def tisk_info(text):
    print(barva(f"◆ {text}", CYAN))


def tisk_zlato(text):
    print(barva(f"💰 {text}", GOLD))


def tisk_magenta(text):
    print(barva(f"🔮 {text}", MAGENTA))


def tisk_cyan(text):
    print(barva(f"💠 {text}", CYAN))


def nacti_volbu(platne: set[str], prompt="> ", chybova_zprava=None):
    """Read a normalized menu choice until it matches the allowed options."""
    platne_normalizovane = {str(volba).strip().lower() for volba in platne}
    while True:
        volba = input(prompt).strip().lower()
        if volba in platne_normalizovane:
            return volba
        if chybova_zprava:
            print(chybova_zprava)
        else:
            print(f"Neplatná volba. Možnosti: {', '.join(sorted(platne_normalizovane))}")


def terminalni_obrazek(scena, hra=None, **kwargs):
    """Vykreslí ASCII ilustraci – dynamicky generovanou."""
    try:
        from utils.ascii_gen import generuj_scenu, generuj_z_hry
        if hra is not None:
            print(generuj_z_hry(hra, scena))
        else:
            print(generuj_scenu(scena or "menu", **kwargs))
        return
    except Exception:
        logging.getLogger(__name__).debug(
            "Generování terminální ilustrace selhalo; používá se textový fallback.",
            exc_info=True,
        )
    from config import GOLD, MAGENTA, CYAN, NC
    print(f"{MAGENTA}     ╔═══ {scena or 'menu'} ═══╗{NC}")
    print(f"{CYAN}     │  TEMNÉ DOMINIUM  │{NC}")
    print(f"{GOLD}     ╚═════════════════╝{NC}")


def ukazatel(hodnota, maximum, sirka=18, barva_plno=GREEN, barva_malo=RED):
    maximum = max(1, maximum)
    hodnota = max(0, min(maximum, hodnota))
    plno = int(sirka * hodnota / maximum)
    pomer = hodnota / maximum
    if pomer > 0.6:
        bv = barva_plno
    elif pomer > 0.3:
        bv = YELLOW
    else:
        bv = barva_malo
    blok_plno = "█" * plno
    blok_prazdno = "░" * (sirka - plno)
    return f"{bv}{blok_plno}{DIM}{blok_prazdno}{NC} {hodnota}/{maximum}"


_IKONY_HLAVICEK = (
    (("souboj", "arén", "boss", "gladi"), "⚔️"),
    (("quest", "úkol", "výpr", "kampa"), "📜"),
    (("map", "cest", "lokac", "npc", "svět"), "🗺️"),
    (("nevěst", "vip", "špion", "mecen"), "🏛️"),
    (("maf", "syndik", "územ"), "🕶️"),
    (("pevnost", "budov", "panstv", "hrad"), "🏰"),
    (("alchym", "lektvar", "dro"), "⚗️"),
    (("craft", "výrob", "předmět"), "🛠️"),
    (("harém", "interak", "otroky", "péč"), "👑"),
    (("manžel", "rodin", "svat"), "💍"),
    (("obchod", "trh", "aukc", "draž"), "🪙"),
    (("diplom", "frak"), "🤝"),
    (("výzkum", "technolog"), "🔬"),
    (("energie", "medit"), "⚡"),
    (("statistik", "rekord"), "📊"),
    (("kronik", "histor"), "📖"),
    (("nastav", "hlavní menu"), "⚙️"),
    (("personál", "dohlíž"), "🧑‍🤝‍🧑"),
    (("odpoč", "nový den"), "🌙"),
)

_IKONY_VOLEB = (
    (("zpět", "návrat", "zrušit"), "↩️"),
    (("ukončit", "konec", "odejít"), "🚪"),
    (("uložit", "ulož"), "💾"),
    (("načíst", "načti"), "📂"),
    (("nastavení", "nastav"), "⚙️"),
    (("boj", "útok", "vyzvat", "arén", "boss"), "⚔️"),
    (("obrana", "bránit"), "🛡️"),
    (("léč", "zdrav"), "🩹"),
    (("quest", "úkol", "výpr"), "📜"),
    (("mapa", "cesta", "cestovat", "lokac"), "🗺️"),
    (("obchod", "koupit", "nákup", "prodat", "prodej"), "🪙"),
    (("harém", "otrokyn", "partner"), "👑"),
    (("diplom", "frak", "vztah"), "🤝"),
    (("výzkum", "technolog"), "🔬"),
    (("energie", "medit"), "⚡"),
    (("trest", "odměn", "péč"), "💝"),
    (("stav", "budov", "pevnost", "panstv"), "🏰"),
    (("karavan", "nájezd"), "🐫"),
    (("nevěst", "vip", "mecen"), "✨"),
    (("špion", "inform"), "🕵️"),
    (("odpoč", "nový den"), "🌙"),
    (("pokrač", "potvr", "přijm"), "✅"),
)

_ANSI_KODY = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def _sirka_zobrazeni(text):
    sirka = 0
    for znak in text:
        if unicodedata.combining(znak) or znak in ("\ufe0e", "\ufe0f", "\u200d"):
            continue
        sirka += 2 if unicodedata.east_asian_width(znak) in ("W", "F") else 1
    return sirka


def banner_lokace(titulek, podtitulek="", ikona="🏙️"):
    """Vykreslí kompaktní banner pro lokaci nebo městskou čtvrť."""
    nadpis = f"{ikona} {titulek}"
    sirka = max(44, _sirka_zobrazeni(nadpis) + 4)
    if podtitulek:
        sirka = max(sirka, _sirka_zobrazeni(podtitulek) + 4)
    print(f"{GOLD}╭{'─' * (sirka - 2)}╮{NC}")
    print(
        f"{GOLD}│{NC} {BOLD}{WHITE}{nadpis}"
        f"{' ' * max(0, sirka - _sirka_zobrazeni(nadpis) - 4)}{NC} "
        f"{GOLD}│{NC}"
    )
    if podtitulek:
        sirka_textu = _sirka_zobrazeni(podtitulek)
        print(f"{GOLD}│{NC} {DIM}{podtitulek}{' ' * (sirka - sirka_textu - 4)}{NC} {GOLD}│{NC}")
    print(f"{GOLD}╰{'─' * (sirka - 2)}╯{NC}")


def _ma_uvodni_ikonu(text):
    viditelny = _ANSI_KODY.sub("", text).lstrip()
    return bool(viditelny) and unicodedata.category(viditelny[0]).startswith("S")


def _ikona_pro(stitek, pravidla):
    nizky = stitek.casefold()
    return next(
        (ikona for klice, ikona in pravidla if any(klic in nizky for klic in klice)),
        "✦",
    )


def hlavicka(stitek, podtitulek=""):
    print()
    # Clean up standard titles from existing hyphens/equals
    stitek = stitek.replace("---", "").replace("===", "").strip()
    if not _ma_uvodni_ikonu(stitek):
        stitek = f"{_ikona_pro(stitek, _IKONY_HLAVICEK)}  {stitek}"
    sirka_titulu = _sirka_zobrazeni(stitek)
    sirka = max(60, sirka_titulu + 4)
    mezera = sirka - 4 - sirka_titulu
    l_mezera = mezera // 2
    p_mezera = mezera - l_mezera

    print(f"{CYAN}{BOLD}╔{'═' * (sirka-2)}╗{NC}")
    print(f"{CYAN}{BOLD}║{NC} {' ' * l_mezera}{BOLD}{WHITE}{stitek}{NC}{' ' * p_mezera} {CYAN}{BOLD}║{NC}")
    print(f"{CYAN}{BOLD}╚{'═' * (sirka-2)}╝{NC}")
    if podtitulek:
        print(f"  {DIM}{podtitulek}{NC}")


def vytiskni_volbu(cislo, text, barva=YELLOW):
    if not _ma_uvodni_ikonu(text):
        text = f"{_ikona_pro(text, _IKONY_VOLEB)} {text}"
    print(f"  {BOLD}{barva}{cislo}){NC} {text}")

def menu_cara():
    print(f"{DIM}────────────────────────────────────────────────────────────{NC}")

def ascii_art():
    print(
        r"""
    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██║██╔═══██╗████╗  ██║
    ██║  ██║███████║██████╔╝█████╔╝     ██║  ██║██║   ██║██╔████╔██║██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║  ██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║██║  ██╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    """
    )
    print(f"{GOLD}{BOLD}               DARK DOMINION – Dark Expansion{NC}")
    print(f"{MAGENTA}  👾 Harém • Loajalita • Odměny • Oblíbenkyně • Témata • Osudy{NC}\n")
