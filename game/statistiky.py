# game/statistiky.py
from utils.vypis import clear, tisk_info
from utils.vypis import hlavicka, ukazatel
from config import GREEN, CYAN, MAGENTA, RED, YELLOW, NC
from collections import Counter
from data.charaktery import CHARAKTERY, normalizuj_charakter


def _graf_historie_haremu(clenky):
    dny = sorted({
        int(bod["den"])
        for otrok in clenky
        for bod in getattr(otrok, "historie_statistik", [])
        if isinstance(bod, dict) and isinstance(bod.get("den"), int)
    })[-14:]
    if not dny:
        return
    print(f"\n{CYAN}📈 Vývoj harému v čase{NC}")
    znaky = "▁▂▃▄▅▆▇█"
    for nazev, klic, barva in (
        ("Důvěra", "duvera", CYAN),
        ("Loajalita", "loajalita", MAGENTA),
    ):
        hodnoty = []
        for den in dny:
            posledni = [
                max(
                    (
                        bod for bod in getattr(otrok, "historie_statistik", [])
                        if isinstance(bod, dict) and bod.get("den", -1) <= den
                    ),
                    key=lambda bod: bod.get("den", -1),
                    default=None,
                )
                for otrok in clenky
            ]
            dostupne = [bod[klic] for bod in posledni if bod is not None and klic in bod]
            hodnoty.append(sum(dostupne) // len(dostupne) if dostupne else 0)
        minimum, maximum = min(hodnoty), max(hodnoty)
        if minimum == maximum:
            linka = znaky[3] * len(hodnoty)
        else:
            linka = "".join(
                znaky[round((hodnota - minimum) / (maximum - minimum) * 7)]
                for hodnota in hodnoty
            )
        print(f"  {nazev:10} {barva}{linka}{NC} {hodnoty[0]} → {hodnoty[-1]}")
    print("  Dny:      " + " ".join(map(str, dny)))


def zobraz_statistiky(hra):
    clear()
    hlavicka("Statistiky a přehled dominia")

    h = hra.hrac
    print(f"{CYAN}👤 Postava:{NC}")
    print(f"  Jméno: {h.jmeno}")
    print(f"  Level: {h.level} (XP: {h.xp}/{h.xp_next})")
    print(f"  Dominance: {h.dominance}")
    print(f"  Zlato: {h.gold} 🪙")
    for nazev, hodnota, maximum, barva in (
        ("Životy", h.hp, h.max_hp, GREEN),
        ("Sexuální energie", h.sex_energy, h.max_sex(), MAGENTA),
        ("Temná energie", h.dark_energy, h.max_temno(), RED),
        ("Postup XP", h.xp, h.xp_next, YELLOW),
    ):
        print(f"  {nazev:20} {ukazatel(hodnota, maximum, 20, barva)}")
    skilly = sorted(h.skilly.items())
    max_dovednost = max((hodnota for _, hodnota in skilly), default=1) or 1
    print(f"\n{CYAN}⚔️ Dovednosti{NC}")
    for nazev, hodnota in skilly:
        print(f"  {nazev.replace('_', ' ').capitalize():16} {ukazatel(hodnota, max_dovednost, 14, CYAN)}")
    print()

    aktivni_harem = hra.harem.vsechny_aktivni()
    print(f"{CYAN}👑 Harém:{NC}")
    print(f"  Aktivní členky: {len(aktivni_harem)} | Celkem získáno: {len(hra.harem.otrokyne)}")
    print(f"  Úroveň harému: {hra.harem.harem_level}")
    print(f"  Pasivní příjem: {hra.harem.pasivni_prijem()} zlaťáků/den")
    if aktivni_harem:
        prumer_duvery = sum(o.duvera for o in aktivni_harem) // len(aktivni_harem)
        prumer_loajality = sum(o.loajalita for o in aktivni_harem) // len(aktivni_harem)
        for nazev, hodnota, barva in (
            ("Průměrná důvěra", prumer_duvery, CYAN),
            ("Průměrná loajalita", prumer_loajality, MAGENTA),
        ):
            print(f"  {nazev:20} {ukazatel(hodnota, 100, 20, barva)}")
        pocty_charakteru = Counter(
            normalizuj_charakter(o.charakter) for o in aktivni_harem
        )
        print("  Povahy:")
        for charakter, pocet in pocty_charakteru.most_common():
            print(
                f"    {CHARAKTERY[charakter]['nazev']:<24} "
                f"{ukazatel(pocet, len(aktivni_harem), 12, YELLOW)}"
            )
        _graf_historie_haremu(aktivni_harem)
    else:
        tisk_info("Harém zatím nemá žádné aktivní členky.")
    print()

    print(f"{CYAN}🕶️ Mafie / Impérium:{NC}")
    print(f"  Území: {len(hra.mafie.uzemi)}")
    print(f"  Vojáci: {hra.mafie.vojaci}")
    print(f"  Vliv ve městě   {ukazatel(hra.mafie.vliv_ve_meste, 100, 20, MAGENTA)}")
    print(f"  Příjem: {hra.mafie.vypocet_prijmu()} zlaťáků/den")
    print()

    print(f"{CYAN}🤝 Frakce:{NC}")
    for klic, frakce in hra.frakce.frakce.items():
        print(
            f"  {frakce.nazev:<24} {frakce.reputace:+4} "
            f"{ukazatel(frakce.reputace + 100, 200, 14, GREEN, RED)}"
        )
    print()

    print(f"{CYAN}Výzkum:{NC}")
    if hra.vyzkum.ziskane:
        for id_v in hra.vyzkum.ziskane:
            print(f"  ✔ {id_v}")
    else:
        print("  Žádný")
    print()

    print(f"{CYAN}Quest systém:{NC}")
    print(f"  Dokončeno questů: {hra.questy.dokonceno if hasattr(hra, 'questy') else 0}")
    print(f"  Aktivní lokace: {hra.svet.aktualni_lokace}")
    print(
        f"  Kampaň: kapitola {hra.kampan.kapitola + 1}"
        if hra.kampan.aktualni()
        else "  Kampaň: dokončena"
    )
    dokoncene_osudy = sum(
        1 for otrok in hra.harem.otrokyne if otrok.osud_dokonceno
    )
    print(f"  Uzavřené osobní osudy: {dokoncene_osudy}/{len(hra.harem.otrokyne)}")
    if hasattr(hra, "expedice"):
        print(f"  Dokončené výpravy: {hra.expedice.dokoncene}")
    if hasattr(hra, "pevnost"):
        print(f"  Pevnost: úroveň {hra.pevnost.uroven}, bonusy {hra.pevnost.bonusy()}")
    if hasattr(hra, "achievementy"):
        from models.achievements import ACHIEVEMENTS
        print(f"  Achievementy: {len(hra.achievementy.odemcene)}/{len(ACHIEVEMENTS)}")
        for ident in hra.achievementy.odemcene:
            nazev = ACHIEVEMENTS.get(ident, (ident, ""))[0]
            print(f"    ✔ {nazev}")
    if hasattr(hra, "npc_questy"):
        aktivni = len(hra.npc_questy.aktivni)
        dokoncene = sum(
            int(pocet) for pocet in hra.npc_questy.dokoncene.values()
            if isinstance(pocet, (int, float))
        )
        print(f"  NPC síť: {dokoncene} dokončených, {aktivni} aktivních úkolů")
    print()

    tisk_info("Stiskni Enter...")
    input()
