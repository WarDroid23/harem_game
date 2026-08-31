# game/trailer.py
"""Cinematic trailer pro Harem Dark – Dark Expansion (terminál)."""

from __future__ import annotations

import time

from config import (
    BOLD, BLUE, CYAN, GOLD, GRAY, GREEN, MAGENTA, NC, ORANGE, RED, VIOLET, WHITE, YELLOW,
)
from utils.vypis import clear
from utils.ascii_gen import generuj_harem, hrad, trun


def _pause(sekundy: float = 2.2, rychle: bool = False):
    if rychle:
        time.sleep(min(0.35, sekundy * 0.25))
    else:
        time.sleep(sekundy)


def _radek(text: str, barva: str = WHITE):
    print(f"{barva}{text}{NC}")


def _blok(texty, barva: str = WHITE):
    for t in texty:
        print(f"{barva}{t}{NC}")


SCENA_OKOVY = f"""
{GRAY}           ⛓    ⛓    ⛓
{RED}          ╔═══════════╗
{GOLD}          ║  TVŮJ ZÁKON ║
{RED}          ╚═══════════╝
{MAGENTA}        loajalita • strach • touha
"""

SCENA_FINALE = f"""
{RED}{BOLD}
    ██╗  ██╗ █████╗ ██████╗ ███████╗███╗   ███╗
    ██║  ██║██╔══██╗██╔══██╗██╔════╝████╗ ████║
    ███████║███████║██████╔╝█████╗  ██╔████╔██║
    ██╔══██║██╔══██║██╔══██╗██╔══╝  ██║╚██╔╝██║
    ██║  ██║██║  ██║██║  ██║███████╗██║ ╚═╝ ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝
{NC}{GOLD}              D A R K   E X P A N S I O N
{MAGENTA}     16 fází • loajalita • ★ oblíbenkyně • manželství
{CYAN}              JSON save • výdrž • denní plná energie
"""


def prehraj_trailer(rychle: bool = False, interaktivni: bool = True) -> None:
    sceny = [
        _scena_1_temnota, _scena_2_hrad, _scena_3_harem, _scena_4_zakon,
        _scena_5_moc, _scena_6_svet, _scena_7_finale,
    ]
    for i, fn in enumerate(sceny):
        clear()
        if not fn(rychle):
            clear()
            _radek("Trailer přeskočen.", GRAY)
            _pause(0.8, rychle)
            return
        if interaktivni and i < len(sceny) - 1:
            try:
                odp = input(f"{GRAY}[Enter – dál / Q přeskočit]{NC} ").strip().lower()
            except EOFError:
                odp = ""
            if odp in ("q", "quit", "skip", "0"):
                clear()
                _radek("Trailer přeskočen.", GRAY)
                _pause(0.6, rychle)
                return
        else:
            _pause(2.4 if not rychle else 0.5, rychle)
    if interaktivni:
        try:
            input(f"{GOLD}[Enter – zpět do menu]{NC} ")
        except EOFError:
            pass


def _scena_1_temnota(rychle: bool) -> bool:
    _radek("…", GRAY)
    _pause(0.6, rychle)
    _blok(["", "  V říši, kde se slunce schovává za mraky dýmu,", "  kde inkvizice šeptá a mafie platí zlatem,", ""], CYAN)
    _pause(1.2, rychle)
    _radek(f"  {BOLD}ty držíš klíč od klecí.{NC}", GOLD)
    _pause(1.0, rychle)
    return True


def _scena_2_hrad(rychle: bool) -> bool:
    print("\n".join(hrad(vyska=4, sire=3)))
    print(f"{MAGENTA}           TEMNÉ DOMINIUM{NC}")
    _blok(["  Pevnost. Trůn. Tvé dominium.", "  Za hradbami čeká svět – a uvnitř harém,", "  který se učí tvé jméno šeptem."], WHITE)
    return True


def _scena_3_harem(rychle: bool) -> bool:
    print(generuj_harem(pocet=4, oblibena=True, loajalita_avg=75))
    _blok(["  Každá má charakter. Fázi. Loajalitu.", "  Jedna klečí jako ★ oblíbenkyně.", "  Jiná šeptá o svatbě… nebo o útěku.", "", "  Ty rozhodneš, kdo bude majetek –", "  a kdo absolutní oddanost."], MAGENTA)
    return True


def _scena_4_zakon(rychle: bool) -> bool:
    print(SCENA_OKOVY)
    _blok(["  Odměny. Tresty. 16 fází zkázanosti.", "  Od vzdoru… k prázdné nádobě.", "", "  Harém reaguje. Žárlí. Prosí. Spí u tvých dveří."], RED)
    return True


def _scena_5_moc(rychle: bool) -> bool:
    print("\n".join(trun(True)))
    _blok(["  Každý den se energie vrátí naplno.", "  Výdrž roste. Manželka a ★ tě posilují.", "  Tvé tělo je zbraň – i slib."], GOLD)
    return True


def _scena_6_svet(rychle: bool) -> bool:
    print(f"""
{GREEN}     [PEVNOST]───[TRH]───[PŘÍSTAV]
{GRAY}         │          │
{CYAN}      [LES]────[HRANICE]
{YELLOW}             ✦ CESTA OSUDU
{MAGENTA}     mafie • lov • kampaň • inkvizice
""")
    _blok(["  Lov. Dražba. Questy. Temné NPC.", "  Buduj impérium. Lámej vůli. Piš osudy."], CYAN)
    return True


def _scena_7_finale(rychle: bool) -> bool:
    print(SCENA_FINALE)
    _blok(["", "           Textová RPG • 18+", "         Dark Expansion 22.1", "", f"  {GOLD}Pán. Harém. Trůn. Tvoje pravidla.{NC}", ""], WHITE)
    return True


def menu_trailer():
    clear()
    print(f"{GOLD}{BOLD}--- Trailer / animace ---{NC}\n")
    print("1) Přehrát trailer")
    print("2) Rychlá verze")
    print("3) Animace (ukázky)")
    print("0) Zpět")
    try:
        v = input("> ").strip()
    except EOFError:
        return
    if v == "1":
        prehraj_trailer(rychle=False, interaktivni=True)
    elif v == "2":
        prehraj_trailer(rychle=True, interaktivni=False)
    elif v == "3":
        _menu_animace()


def _menu_animace():
    from utils.term_render import animuj, show_cursor
    from utils.ascii_gen import (
        framy_hvezd_pulz, framy_napln_energie, framy_harem_dych,
        framy_noc, framy_okovy_pulse, framy_trailer_uvod,
    )
    clear()
    print(f"{GOLD}--- Animace ---{NC}\n")
    print("1) Pulz ★ oblíbenkyně")
    print("2) Plnění energie")
    print("3) Harém dýchá")
    print("4) Noční obloha")
    print("5) Okovy / trest")
    print("6) Fade-in úvod")
    print("7) Všechny za sebou")
    print("0) Zpět")
    try:
        v = input("> ").strip()
    except EOFError:
        return
    try:
        if v == "1":
            animuj(framy_hvezd_pulz(8, "Selene"), fps=7, cyklu=2)
        elif v == "2":
            animuj(framy_napln_energie(100, 80, 100, 100, 14), fps=14, cyklu=1)
        elif v == "3":
            animuj(framy_harem_dych(5, True, 8), fps=5, cyklu=2)
        elif v == "4":
            animuj(framy_noc(10), fps=6, cyklu=2)
        elif v == "5":
            animuj(framy_okovy_pulse(8), fps=5, cyklu=2)
        elif v == "6":
            animuj(framy_trailer_uvod(10), fps=8, cyklu=1)
        elif v == "7":
            animuj(framy_trailer_uvod(6), fps=10, cyklu=1)
            animuj(framy_hvezd_pulz(6), fps=8, cyklu=1)
            animuj(framy_napln_energie(kroku=10), fps=14, cyklu=1)
            animuj(framy_harem_dych(4, True, 6), fps=5, cyklu=1)
            animuj(framy_noc(6), fps=7, cyklu=1)
    finally:
        show_cursor()
    try:
        input(f"{GRAY}[Enter]{NC} ")
    except EOFError:
        pass
