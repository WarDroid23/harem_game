"""Bezpečný plánovač automatického tahu bez použití herních menu."""

from dataclasses import dataclass, field

from config import BOLD, CYAN, GOLD, GREEN, MAGENTA, NC, RED, YELLOW
from data.interakce import INTERAKCE
from data.klienti import AUKCNI_DOBA, KLIENTI
from game.budovy import vylepsit_budovu
from game.ekonomika import proved_najem_otrokyně, spocitej_cenu_najmu
from game.energie import hostinec, lazne, meditace, molo, observator, zahrada
from game.harem_interakce import proved_peci, proved_poradu
from game.interakce import proved_interakci
from game.mafie import dostupna_uzemi, koupit_uzemi, najmout_vojaka


MIN_ZLATO_REZERVA = 200
MIN_SEX_ENERGIE_REZERVA = 10
MIN_TEMNA_ENERGIE_REZERVA = 5
NIZKA_SEX_ENERGIE = 35
NIZKA_TEMNA_ENERGIE = 25

_BEZPECNE_INTERAKCE = {
    a["id"]: a
    for a in INTERAKCE
    if a.get("typ") == "odmena" and a.get("riziko", 1) == 0
}
_DOBIJECE = {
    "hostinec": (hostinec, 35, 28, 8, "Hostinec"),
    "lazne": (lazne, 60, 20, 22, "Lázně"),
    "molo": (molo, 25, 16, 16, "Směna na molu"),
    "zahrada": (zahrada, 0, 24, 6, "Klidný rozhovor v zahradě"),
    "observator": (observator, 0, 8, 30, "Pozorování oblohy"),
}
_LOKACNI_DOBIJECE = {
    "hostinec": "hostinec",
    "lazne": "lazne",
    "molo_mesicniho_pristavu": "molo",
    "sklenena_zahrada": "zahrada",
    "observator": "observator",
}


@dataclass(frozen=True)
class AutomatickaAkce:
    typ: str
    nazev: str
    popis: str
    cil: str = ""
    klient_id: str = ""
    doba: str = ""
    cena_zlato: int = 0
    cena_sex: int = 0
    cena_temna: int = 0


@dataclass
class PlanAutomatickehoTahu:
    akce: list = field(default_factory=list)
    poznamky: list = field(default_factory=list)
    rezerva_zlata: int = MIN_ZLATO_REZERVA

    @property
    def je_prazdny(self):
        return not self.akce


@dataclass
class VysledekAutomatickehoTahu:
    provedene: list = field(default_factory=list)
    preskocene: list = field(default_factory=list)
    chyby: list = field(default_factory=list)
    zlato_pred: int = 0
    zlato_po: int = 0
    sex_energie_pred: int = 0
    sex_energie_po: int = 0
    temna_energie_pred: int = 0
    temna_energie_po: int = 0


def _aktivni_postavy(hra):
    return hra.harem.vsechny_aktivni()


def _volna_postava(hra, preferuj_zranenou=False):
    postavy = [o for o in _aktivni_postavy(hra) if not o.na_najmu]
    if preferuj_zranenou:
        postavy.sort(key=lambda o: (o.hp >= o.max_hp, o.hp, o.jmeno))
    else:
        postavy.sort(key=lambda o: (-o.hp, o.jmeno))
    return postavy[0] if postavy else None


def _pridej_dobiti(plan, hra, sex, temna, zlato):
    """Naplánuje nejvýše jednu bezplatnou a jednu placenou obnovu."""
    hrac = hra.hrac
    if (
        hrac.sex_energy >= NIZKA_SEX_ENERGIE
        and hrac.dark_energy >= NIZKA_TEMNA_ENERGIE
    ):
        return sex, temna, zlato

    if not hrac.dobiti_dnes.get("meditace", 0):
        plan.akce.append(
            AutomatickaAkce(
                "energie", "Meditace", "bezplatné dobití dostupné jednou denně"
            )
        )
        sex = min(100, sex + 5)
        temna = min(100, temna + (28 if hra.svet.aktualni_lokace == "haj_soumraku" else 18))

    typ = _LOKACNI_DOBIJECE.get(hra.svet.aktualni_lokace)
    if typ and typ in _DOBIJECE:
        _, cena, bonus_sex, bonus_temna, nazev = _DOBIJECE[typ]
        if (
            not hrac.dobiti_dnes.get(typ, 0)
            and (sex < NIZKA_SEX_ENERGIE or temna < NIZKA_TEMNA_ENERGIE)
            and zlato - cena >= plan.rezerva_zlata
            and (bonus_sex > 0 or bonus_temna > 0)
        ):
            plan.akce.append(
                AutomatickaAkce(
                    "energie",
                    nazev,
                    f"{cena} zlata, energie +{bonus_sex}/+{bonus_temna}",
                    cena_zlato=cena,
                )
            )
            zlato -= cena
            sex = min(100, sex + bonus_sex)
            temna = min(100, temna + bonus_temna)
    return sex, temna, zlato


def naplanuj_automaticky_tah(hra):
    """Sestaví plán pouze z aktuálního stavu; funkce nic nemění a nečte vstup."""
    plan = PlanAutomatickehoTahu()
    hrac = hra.hrac
    zlato = max(0, int(hrac.gold))
    sex = max(0, int(hrac.sex_energy))
    temna = max(0, int(hrac.dark_energy))

    aktivni_najmy = [
        o for o in _aktivni_postavy(hra) if o.na_najmu
    ]
    if aktivni_najmy:
        koncici = [o.jmeno for o in aktivni_najmy if o.najem_zbyva_dni <= 1]
        if koncici:
            plan.poznamky.append(
                "Nájem brzy skončí (" + ", ".join(koncici) + "); automatika ho neruší."
            )
        else:
            plan.poznamky.append(
                f"Aktivní nájmy jsou chráněny ({len(aktivni_najmy)}); "
                "automatika vybírá jen volné postavy."
            )

    sex, temna, zlato = _pridej_dobiti(plan, hra, sex, temna, zlato)

    dostupna = dostupna_uzemi(hra.mafie)
    if dostupna:
        nejlevnejsi_uzemi = min(dostupna, key=lambda u: u.riziko_inkvizice)
        cena = 500 + len(hra.mafie.uzemi) * 200
        if zlato - cena >= plan.rezerva_zlata:
            plan.akce.append(
                AutomatickaAkce(
                    "uzemi",
                    "Nákup území",
                    f"{nejlevnejsi_uzemi.nazev} za {cena} zlata "
                    f"(riziko {nejlevnejsi_uzemi.riziko_inkvizice})",
                    cil=nejlevnejsi_uzemi.nazev,
                    cena_zlato=cena,
                )
            )
            zlato -= cena

    lazne_budova = hra.harem.budovy.get("lazne")
    zranena = any(o.hp < o.max_hp for o in _aktivni_postavy(hra))
    if lazne_budova and zranena and zlato - lazne_budova.cena >= plan.rezerva_zlata:
        plan.akce.append(
            AutomatickaAkce(
                "budova",
                "Vylepšení lázní",
                f"{lazne_budova.cena} zlata, lepší denní péče",
                cil="lazne",
                cena_zlato=lazne_budova.cena,
            )
        )
        zlato -= lazne_budova.cena

    volna = _volna_postava(hra)
    if volna and "neznost" in _BEZPECNE_INTERAKCE:
        akce = _BEZPECNE_INTERAKCE["neznost"]
        cena_sex = akce.get("cena_energie", 0)
        cena_temna = akce.get("cena_temnoty", 0)
        if (
            sex - cena_sex >= MIN_SEX_ENERGIE_REZERVA
            and temna - cena_temna >= MIN_TEMNA_ENERGIE_REZERVA
        ):
            plan.akce.append(
                AutomatickaAkce(
                    "interakce",
                    akce["nazev"],
                    "bezpečná interakce bez rizika",
                    cil=volna.jmeno,
                    cena_sex=cena_sex,
                    cena_temna=cena_temna,
                )
            )
            sex -= cena_sex
            temna -= cena_temna

    zranena_volna = _volna_postava(hra, preferuj_zranenou=True)
    if (
        zranena_volna
        and zranena_volna.hp < zranena_volna.max_hp
        and zlato - 20 >= plan.rezerva_zlata
    ):
        plan.akce.append(
            AutomatickaAkce(
                "pece",
                "Péče a zotavení",
                "20 zlata, +25 HP a +3 důvěra",
                cil=zranena_volna.jmeno,
                cena_zlato=20,
            )
        )
        zlato -= 20

    volne_postavy = [o for o in _aktivni_postavy(hra) if not o.na_najmu]
    if len(volne_postavy) > 1:
        plan.akce.append(
            AutomatickaAkce(
                "porada",
                "Porada harému",
                "bezplatná porada, loajalita +2 a důvěra +1 všem aktivním"
            )
        )

    volna = _volna_postava(hra)
    if volna:
        klient_id = "slechtic"
        cena_za_den = spocitej_cenu_najmu(
            hrac, volna, klient_id, getattr(hra.nastaveni, "obtiznost", "normalni")
        )
        dny_min, dny_max = AUKCNI_DOBA["kratka"]
        plan.akce.append(
            AutomatickaAkce(
                "najem",
                "Nabídka krátkého nájmu",
                f"klient {KLIENTI[klient_id]['jmeno']}, "
                f"{dny_min}-{dny_max} dní, přibližně {cena_za_den} zlata/den",
                cil=volna.jmeno,
                klient_id=klient_id,
                doba="kratka",
            )
        )

    return plan


def _ma_rezervu_zlata(hra, cena, rezerva):
    return hra.hrac.gold - cena >= rezerva


def _najdi_postavu(hra, jmeno):
    return next(
        (o for o in _aktivni_postavy(hra) if o.jmeno == jmeno and not o.na_najmu),
        None,
    )


def proved_automaticky_tah(hra, plan):
    """Provede plán s kontrolou podmínek znovu před každou akcí."""
    vysledek = VysledekAutomatickehoTahu(
        zlato_pred=hra.hrac.gold,
        zlato_po=hra.hrac.gold,
        sex_energie_pred=hra.hrac.sex_energy,
        sex_energie_po=hra.hrac.sex_energy,
        temna_energie_pred=hra.hrac.dark_energy,
        temna_energie_po=hra.hrac.dark_energy,
    )
    if not isinstance(plan, PlanAutomatickehoTahu):
        vysledek.chyby.append("Neplatný plán automatického tahu.")
        return vysledek

    for akce in plan.akce:
        uspech = False
        duvod = ""
        if akce.typ == "energie":
            energie = next(
                (data for data in _DOBIJECE.values() if data[4] == akce.nazev), None
            )
            if akce.nazev == "Meditace":
                if hra.hrac.dobiti_dnes.get("meditace", 0):
                    duvod = "meditace už byla dnes použita"
                else:
                    uspech = meditace(hra)
            elif energie is None:
                duvod = "dobití není dostupné"
            elif not _ma_rezervu_zlata(hra, energie[1], plan.rezerva_zlata):
                duvod = "po akci by nezůstala zlatá rezerva"
            else:
                uspech = energie[0](hra)
        elif akce.typ == "uzemi":
            if not _ma_rezervu_zlata(hra, akce.cena_zlato, plan.rezerva_zlata):
                duvod = "po nákupu by nezůstala zlatá rezerva"
            else:
                uspech = koupit_uzemi(hra.hrac, hra.mafie, akce.cil)
        elif akce.typ == "budova":
            if not _ma_rezervu_zlata(hra, akce.cena_zlato, plan.rezerva_zlata):
                duvod = "po nákupu by nezůstala zlatá rezerva"
            else:
                uspech = vylepsit_budovu(hra.hrac, hra.harem, akce.cil)
        elif akce.typ == "interakce":
            otrok = _najdi_postavu(hra, akce.cil)
            if otrok is None:
                duvod = "postava není aktivní nebo je na nájmu"
            elif (
                hra.hrac.sex_energy - akce.cena_sex < MIN_SEX_ENERGIE_REZERVA
                or hra.hrac.dark_energy - akce.cena_temna < MIN_TEMNA_ENERGIE_REZERVA
            ):
                duvod = "po interakci by nezůstala energetická rezerva"
            else:
                uspech = proved_interakci(otrok, hra.hrac, "neznost")
        elif akce.typ == "pece":
            otrok = _najdi_postavu(hra, akce.cil)
            if otrok is None:
                duvod = "postava není aktivní nebo je na nájmu"
            elif not _ma_rezervu_zlata(hra, 20, plan.rezerva_zlata):
                duvod = "po péči by nezůstala zlatá rezerva"
            else:
                uspech = proved_peci(hra, otrok, respektuj_najem=True)
        elif akce.typ == "porada":
            uspech = proved_poradu(
                hra,
                [o for o in _aktivni_postavy(hra) if not o.na_najmu],
            )
            if not uspech:
                duvod = "není aktivní postava"
        elif akce.typ == "najem":
            otrok = _najdi_postavu(hra, akce.cil)
            if otrok is None:
                duvod = "postava není volná"
            else:
                uspech = proved_najem_otrokyně(
                    hra.hrac,
                    otrok,
                    akce.klient_id,
                    akce.doba,
                    getattr(hra.nastaveni, "obtiznost", "normalni"),
                )
        elif akce.typ == "vojak":
            if not _ma_rezervu_zlata(hra, akce.cena_zlato, plan.rezerva_zlata):
                duvod = "po nákupu by nezůstala zlatá rezerva"
            else:
                uspech = najmout_vojaka(hra.hrac, hra.mafie, akce.cena_zlato)
        else:
            duvod = "neznámý typ akce"

        if uspech:
            vysledek.provedene.append(akce.nazev)
        else:
            vysledek.preskocene.append(
                f"{akce.nazev}" + (f" ({duvod})" if duvod else "")
            )

    vysledek.zlato_po = hra.hrac.gold
    vysledek.sex_energie_po = hra.hrac.sex_energy
    vysledek.temna_energie_po = hra.hrac.dark_energy
    return vysledek


def zobraz_plan(plan):
    print(f"{GOLD}{BOLD}╔══════════ AUTOMATICKÝ TAH ══════════╗{NC}")
    if plan.je_prazdny:
        print(f"{YELLOW}║ Nejsou dostupné bezpečné akce.        ║{NC}")
    else:
        for index, akce in enumerate(plan.akce, 1):
            print(f"{CYAN}║ {index:>2}. {akce.nazev}: {akce.popis}{NC}")
        print(f"{GOLD}║ Rezerva zlata po akcích: {plan.rezerva_zlata}         ║{NC}")
    for poznamka in plan.poznamky:
        print(f"{MAGENTA}║ Poznámka: {poznamka}{NC}")
    print(f"{GOLD}╚══════════════════════════════════════╝{NC}")


def zobraz_vysledky(vysledek):
    print(f"{GREEN}{BOLD}--- Výsledky automatického tahu ---{NC}")
    if vysledek.provedene:
        for akce in vysledek.provedene:
            print(f"{GREEN}✔ {akce}{NC}")
    else:
        print(f"{YELLOW}Žádná akce nebyla provedena.{NC}")
    for akce in vysledek.preskocene:
        print(f"{YELLOW}• Přeskočeno: {akce}{NC}")
    for chyba in vysledek.chyby:
        print(f"{RED}✖ {chyba}{NC}")
    print(
        f"{CYAN}Stav: zlato {vysledek.zlato_pred} → {vysledek.zlato_po}, "
        f"energie {vysledek.sex_energie_pred}/{vysledek.temna_energie_pred} "
        f"→ {vysledek.sex_energie_po}/{vysledek.temna_energie_po}{NC}"
    )


def obsluz_automaticky_tah(hra, vstup=None):
    """Zobrazí plán, vyžádá potvrzení a vrátí výsledek; jediný vstup je potvrzení."""
    plan = naplanuj_automaticky_tah(hra)
    zobraz_plan(plan)
    if plan.je_prazdny:
        return None
    if vstup is None:
        vstup = input
    try:
        potvrzeni = vstup("Provést tento plán? (a/n): ").strip().lower()
    except EOFError:
        potvrzeni = "n"
    if potvrzeni not in ("a", "ano", "y", "yes"):
        print(f"{CYAN}Automatický tah byl zrušen.{NC}")
        return None
    vysledek = proved_automaticky_tah(hra, plan)
    zobraz_vysledky(vysledek)
    return vysledek


naplanuj_tah = naplanuj_automaticky_tah
proved_tah = proved_automaticky_tah
