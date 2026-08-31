# utils/ascii_gen.py
"""Dynamické generování ASCII ilustrací pro Harem Dark."""

from __future__ import annotations

import random
from typing import List, Optional

from config import (
    BLUE, CYAN, GOLD, GRAY, GREEN, MAGENTA, NC, ORANGE, RED, VIOLET, WHITE, YELLOW,
)


def ramecek(sirka: int, vyska: int, nadpis: str = "", barva: str = GOLD) -> List[str]:
    sirka = max(sirka, len(nadpis) + 4)
    top = f"{barva}╔{'═' * (sirka - 2)}╗{NC}"
    bot = f"{barva}╚{'═' * (sirka - 2)}╝{NC}"
    lines = [top]
    if nadpis:
        pad = sirka - 2 - len(nadpis)
        left = pad // 2
        right = pad - left
        lines.append(f"{barva}║{' ' * left}{nadpis}{' ' * right}║{NC}")
    for _ in range(max(0, vyska - (2 if nadpis else 1))):
        lines.append(f"{barva}║{' ' * (sirka - 2)}║{NC}")
    lines.append(bot)
    return lines


def progress_bar(hodnota: int, maximum: int, sirka: int = 12, plny: str = "█", prazdny: str = "░") -> str:
    maximum = max(1, int(maximum))
    hodnota = max(0, min(maximum, int(hodnota)))
    plno = int(sirka * hodnota / maximum)
    return plny * plno + prazdny * (sirka - plno)


def hvezdy(sirka: int = 28) -> str:
    znaky = ["·", "*", "✦", "✧", " "]
    radky = []
    for _ in range(2):
        radek = "".join(random.choice(znaky) if random.random() < 0.35 else " " for _ in range(sirka))
        radky.append(f"{BLUE}{radek}{NC}")
    return "\n".join(radky)


def silueta_zeny(styl: str = "kleci", barva: str = CYAN) -> List[str]:
    styly = {
        "kleci": ["  ╱|、", "(˚ˎ 。7", " |、˜〵", " じしˍ,)ノ"],
        "stoji": ["  ╱╲", " (••)", " /||\\", "  /\\"],
        "hvezda": ["   ★", "  ╱|、", " (˚ˎ 。7", "  OBL"],
        "okovy": ["  ⛓", " ╱|、", "(˚ˎ 。7", " |、˜〵"],
    }
    body = styly.get(styl, styly["kleci"])
    return [f"{barva}{r}{NC}" for r in body]


def rada_figurek(pocet: int, oblibena_idx: Optional[int] = None, max_zobrazeni: int = 7) -> str:
    pocet = max(0, pocet)
    if pocet == 0:
        return f"{GRAY}(prázdný harém){NC}"
    zobraz = min(pocet, max_zobrazeni)
    casti = []
    for i in range(zobraz):
        if oblibena_idx is not None and i == min(oblibena_idx, zobraz - 1):
            casti.append(f"{GOLD}★{NC}")
        else:
            casti.append(f"{CYAN}♀{NC}")
    extra = f" {GRAY}+{pocet - zobraz}{NC}" if pocet > zobraz else ""
    return "  ".join(casti) + extra


def hrad(vyska: int = 4, sire: int = 3) -> List[str]:
    sire = max(2, min(6, sire))
    lines = []
    cim = "".join("/\\" for _ in range(sire))
    lines.append(f"{GRAY}        {cim}{NC}")
    for i in range(vyska - 2):
        okna = "".join("||" if j % 2 == 0 else "  " for j in range(sire))
        lines.append(f"{WHITE}       |{okna}|{NC}")
    mid = sire * 2
    lines.append(f"{GOLD}       |{'PEVN':^{mid}}|{NC}")
    lines.append(f"{GRAY}       |{'_' * mid}|{NC}")
    return lines


def trun(s_hvezdou: bool = True) -> List[str]:
    star = "★" if s_hvezdou else " "
    return [
        f"{GOLD}          .--.{NC}",
        f"{GOLD}         | {star}  |{NC}",
        f"{YELLOW}      ___/____\\___{NC}",
        f"{GRAY}     |  TRŮN PÁNA  |{NC}",
        f"{VIOLET}     |_____________|{NC}",
    ]


def mesic_a_noci() -> List[str]:
    return [
        hvezdy(sirka=24),
        f"{VIOLET}         *   ☽   *{NC}",
        f"{GRAY}      .  NOC V HARÉMU  .{NC}",
    ]


def generuj_harem(pocet: int = 3, oblibena: bool = False, loajalita_avg: int = 50, nadpis: str = "HARÉM") -> str:
    oblib_idx = 1 if oblibena and pocet > 0 else None
    fig = rada_figurek(pocet, oblib_idx)
    bar = progress_bar(loajalita_avg, 100, 14)
    barva_bar = GREEN if loajalita_avg >= 70 else (YELLOW if loajalita_avg >= 40 else RED)
    lines = [
        f"{MAGENTA}     ╔═══ {nadpis} ═══╗{NC}",
        f"     │ {fig} │",
        f"{GOLD}     │  klečí u trůnu… │{NC}" if pocet else f"{GRAY}     │   ticho…        │{NC}",
        f"     │ {barva_bar}[{bar}]{NC} │",
        f"{MAGENTA}     ╚═════════════════╝{NC}",
    ]
    return "\n".join(lines)


def generuj_energie(sex: int, max_sex: int, temno: int, max_temno: int) -> str:
    bs = progress_bar(sex, max_sex, 16)
    bt = progress_bar(temno, max_temno, 16)
    return "\n".join([
        f"{CYAN}  SEX  [{bs}] {sex}/{max_sex}{NC}",
        f"{MAGENTA}  TEMNO[{bt}] {temno}/{max_temno}{NC}",
    ])


def generuj_menu(tema: str = "temne_dominium") -> str:
    o = random.choice(["✦", "✧", "·", "★"])
    return "\n".join([
        f"{VIOLET}       /\\_/\\{NC}",
        f"{MAGENTA}      ( o.o ){NC}   {GOLD}╔════════════════════╗{NC}",
        f"{CYAN}       > ^ <{NC}    {GOLD}║  TEMNÉ DOMINIUM   ║{NC}",
        f"{GRAY}      /|   |\\{NC}   {GOLD}╚════════════════════╝{NC}",
        f"{VIOLET}        {o}  {o}  {o}{NC}",
    ])


def generuj_lov(uspech: Optional[bool] = None) -> str:
    stopa = random.choice(["╱╲", "╱  ╲", " ╲╱ "])
    stav = ""
    if uspech is True:
        stav = f"\n{GREEN}     STOPA ČERSTVÁ – KOŘIST BLÍZKO{NC}"
    elif uspech is False:
        stav = f"\n{RED}     STOPA VYHASLA{NC}"
    return "\n".join([
        f"{GREEN}      /\\_/\\  {ORANGE}{stopa}{NC}",
        f"{GRAY}     ( o.o ) {ORANGE} STOPA{NC}",
        f"{CYAN}      > ^ <{NC}",
        f"{GREEN}     LOV OTROKYŇ{NC}",
    ]) + stav


def generuj_souboj(nepritel: str = "BOSS") -> str:
    n = (nepritel or "BOSS")[:8]
    return "\n".join([
        f"{RED}             /\\        /\\{NC}",
        f"{WHITE}            /  \\      /  \\{NC}",
        f"{YELLOW}           < ⚔  >  VS  <{n:^5}>{NC}",
        f"{RED}            \\__/      \\__/{NC}",
    ])


def generuj_odmenu(uroven: int = 1) -> str:
    hvezdy_txt = "★" * max(1, min(5, uroven))
    return "\n".join([
        f"{GOLD}        .·´¯`·.¸{NC}",
        f"{YELLOW}       ¸.·´¯`·.¸.{NC}",
        f"{GREEN}      ODMĚNA PÁNA{NC}",
        f"{CYAN}       {hvezdy_txt}{NC}",
    ])


def generuj_trest() -> str:
    return "\n".join(silueta_zeny("okovy", RED) + [f"{RED}      TREST{NC}"])


def generuj_oblibenou(jmeno: str = "") -> str:
    jm = (jmeno or "OBLÍBENKYNĚ")[:12]
    return "\n".join([
        f"{GOLD}         ★{NC}",
        f"{MAGENTA}      ╱|、  ★{NC}",
        f"{CYAN}    (˚ˎ 。7{NC}",
        f"{GOLD}     {jm}{NC}",
    ])


def generuj_loajalitu(avg: int = 50) -> str:
    bar = progress_bar(avg, 100, 12)
    col = GREEN if avg >= 70 else (YELLOW if avg >= 40 else RED)
    return "\n".join([
        f"{GOLD}      ♥─────♥─────♥{NC}",
        f"{CYAN}     LOAJALITA HARÉMU{NC}",
        f"{col}      [{bar}] {avg}%{NC}",
        f"{MAGENTA}       oddanost{NC}",
    ])


def generuj_pevnost() -> str:
    return "\n".join(hrad(vyska=4, sire=random.randint(2, 4)))


def generuj_noc() -> str:
    return "\n".join(mesic_a_noci())


def generuj_mapu(aktualni: str = "pevnost") -> str:
    uzly = {
        "pevnost": "PEVNOST", "trh": "TRH", "pristav": "PŘÍSTAV",
        "les": "LES", "hranice": "HRANICE",
    }
    def z(k):
        nazev = uzly.get(k, k.upper())
        if k == aktualni.lower() or nazev.lower() == aktualni.lower():
            return f"{GOLD}[{nazev}]{NC}"
        return f"{GREEN}[{nazev}]{NC}"
    return "\n".join([
        f"     {z('pevnost')}───{z('trh')}───{z('pristav')}",
        f"{GRAY}         │          │{NC}",
        f"      {z('les')}────{z('hranice')}",
        f"{ORANGE}              ✦ CESTA OSUDU{NC}",
    ])


def generuj_scenu(scena: str, **kwargs) -> str:
    scena = (scena or "menu").lower()
    generatory = {
        "menu": generuj_menu,
        "harem": lambda: generuj_harem(
            kwargs.get("pocet", 3), kwargs.get("oblibena", False), kwargs.get("loajalita", 50),
        ),
        "mapa": lambda: generuj_mapu(kwargs.get("aktualni", "pevnost")),
        "souboj": lambda: generuj_souboj(kwargs.get("nepritel", "BOSS")),
        "osudy": lambda: "\n".join([
            f"{VIOLET}          .-=========-.{NC}",
            f"{GOLD}         /  KNIHA OSUDŮ \\{NC}",
            f"{CYAN}        |  {'✦ ' * random.randint(2, 4)} |{NC}",
            f"{VIOLET}         \\_____________/{NC}",
        ]),
        "odmena": lambda: generuj_odmenu(kwargs.get("uroven", 1)),
        "trest": generuj_trest,
        "oblibena": lambda: generuj_oblibenou(kwargs.get("jmeno", "")),
        "manzelstvi": lambda: "\n".join([
            f"{MAGENTA}       .·´¯`·.{NC}", f"{GOLD}      ╱ 💍  ╲{NC}",
            f"{CYAN}     │ manžel │{NC}", f"{MAGENTA}      ╲_____╱{NC}",
        ]),
        "lov": lambda: generuj_lov(kwargs.get("uspech")),
        "drazba": lambda: "\n".join([
            f"{GOLD}     ╔══════════╗{NC}", f"{YELLOW}     ║  DRAŽBA  ║{NC}",
            f"{CYAN}     ║  ♀ {random.choice(['???', 'nová', 'vzácná']):^5} ║{NC}",
            f"{GOLD}     ╚══════════╝{NC}", f"{GRAY}      kladívko ⇓{NC}",
        ]),
        "alchymie": lambda: "\n".join([
            f"{GREEN}       (  (  )  ){NC}", f"{CYAN}        \\  ||  /{NC}",
            f"{VIOLET}         ╲ || ╱{NC}", f"{GOLD}        ELIXÍR{NC}",
        ]),
        "noc": generuj_noc,
        "pevnost": generuj_pevnost,
        "inkvizice": lambda: "\n".join([
            f"{RED}      ╱ ═══ ╲{NC}", f"{YELLOW}     │  ✠  │{NC}",
            f"{RED}     │INKVIZICE│{NC}", f"{GRAY}      ╲_____╱{NC}",
        ]),
        "loajalita": lambda: generuj_loajalitu(kwargs.get("loajalita", 50)),
        "partnerka": lambda: "\n".join([
            f"{CYAN}       .·´ ♥ `·.{NC}", f"{MAGENTA}      ╱ partner ╲{NC}",
            f"{GOLD}     │   spolu   │{NC}", f"{CYAN}      ╲_________╱{NC}",
        ]),
        "nastaveni": lambda: "\n".join([
            f"{WHITE}     ⚙️  NASTAVENÍ{NC}", f"{CYAN}     ├─ barvy{NC}",
            f"{MAGENTA}     ├─ téma{NC}", f"{GOLD}     └─ obtížnost{NC}",
        ]),
        "save": lambda: "\n".join([
            f"{GREEN}     ╔═══════╗{NC}", f"{CYAN}     ║ ULOŽIT ║{NC}",
            f"{GREEN}     ╚═══════╝{NC}", f"{GRAY}      💾 sloty{NC}",
        ]),
        "energie": lambda: generuj_energie(
            kwargs.get("sex", 70), kwargs.get("max_sex", 100),
            kwargs.get("temno", 20), kwargs.get("max_temno", 100),
        ),
        "trun": lambda: "\n".join(trun(True)),
        "hrad": generuj_pevnost,
    }
    fn = generatory.get(scena, generatory["menu"])
    return fn()


def generuj_z_hry(hra, scena: str = "harem") -> str:
    try:
        aktivni = hra.harem.vsechny_aktivni()
        pocet = len(aktivni)
        oblib = any(getattr(o, "oblibena", False) for o in aktivni)
        loaj = int(sum(getattr(o, "loajalita", 50) for o in aktivni) / pocet) if pocet else 50
        jmeno_oblib = next((o.jmeno for o in aktivni if getattr(o, "oblibena", False)), "")
        lokace = getattr(getattr(hra, "svet", None), "aktualni_lokace", "pevnost") or "pevnost"
        hrac = hra.hrac
        max_s = hrac.max_sex() if hasattr(hrac, "max_sex") else getattr(hrac, "max_sex_energy", 100)
        max_t = hrac.max_temno() if hasattr(hrac, "max_temno") else getattr(hrac, "max_dark_energy", 100)
        return generuj_scenu(
            scena, pocet=pocet, oblibena=oblib, loajalita=loaj, jmeno=jmeno_oblib,
            aktualni=lokace, sex=hrac.sex_energy, max_sex=max_s,
            temno=hrac.dark_energy, max_temno=max_t,
        )
    except Exception:
        return generuj_scenu(scena)
