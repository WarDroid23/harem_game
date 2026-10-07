# game/nocni_eventy.py — scény po odpočinku
import random
from utils.vypis import tisk_ok, tisk_chyba, tisk_info
from config import MAGENTA, RED, GOLD, CYAN, NC
from data.charaktery import CHARAKTERY, normalizuj_charakter


SCENY_OSOBNOSTI = {
    "badatelka": (
        "ti ukáže poznámku, kterou celý den rozvíjela, a zeptá se, co si o ní myslíš.",
        "vysvětluje, proč ji zaujala stará mapa. Několik dalších členek se zastaví a poslouchá.",
        "navrhne malý pokus a sama si připraví seznam bezpečných podmínek.",
    ),
    "diplomatka": (
        "pomáhá dvěma členkám najít společnou řeč a pak se zeptá, zda se obě cítily vyslyšené.",
        "přinese návrh, jak rozdělit společnou práci spravedlivěji.",
        "vypráví veselou historku z jednání, které málem skončilo hádkou.",
    ),
    "ochranitelka": (
        "kontroluje, zda má každá v domě bezpečné místo, a nabídne pomoc bez naléhání.",
        "učí dobrovolnice jednoduchý obranný cvik a nechává každou zvolit si vlastní tempo.",
        "si všimne, že je někdo zamlklý, a nabídne jí klidnou společnost.",
    ),
    "umelkyne": (
        "si v salonku zkouší novou melodii a pozve ostatní, aby přidaly vlastní nápad.",
        "ukáže nedokončenou kresbu a řekne, že ji chce ještě chvíli nechat jen pro sebe.",
        "připraví improvizovanou výstavu drobností, které si členky samy vybraly.",
    ),
    "cartografka": (
        "rozkládá na stole mapu a nechává ostatní doplnit místa, která mají rády.",
        "objevila bezpečnější cestu do města a připíše k ní doporučení od místních.",
        "si zapisuje, kam by každá chtěla jednou vyrazit.",
    ),
    "lekarka": (
        "připravuje bylinkový čaj a připomíná, že odpočinek je stejně důležitý jako práce.",
        "se ptá, zda někoho něco netrápí, a nabídne soukromý rozhovor bez nátlaku.",
        "ukazuje ostatním, jak připravit hojivou mast z běžných bylin.",
    ),
    "veteranka": (
        "vypráví o chvíli, kdy jí nejvíc pomohla spolupráce, ne síla.",
        "vede krátké cvičení a před každou částí se ujistí, že se všichni cítí bezpečně.",
        "navrhne hlídku, která chrání zahradu, ale nikoho zbytečně neomezuje.",
    ),
    "amazonka": (
        "vyzve ostatní na přátelský turnaj, ve kterém si každá sama zvolí disciplínu.",
        "předvádí nové kroky s mečem a trpělivě pomáhá začátečnicím.",
        "s úsměvem přizná, že dnes prohrála v šachu s někým, koho podcenila.",
    ),
    "carodejka": (
        "zkouší drobné světelné kouzlo a nechá ostatní navrhnout jeho barvu.",
        "připravuje ochranný talisman pro společenskou místnost.",
        "vypráví o zvláštním snu a sama rozhodne, které části chce sdílet.",
    ),
    "kurtizana": (
        "učí dobrovolnice, jak se sebejistě představit a slušně odmítnout nepříjemnou nabídku.",
        "vypráví o šatech, které si kdysi navrhla sama, a plánuje nové.",
        "navrhuje večer poezie, kde si každý může vybrat, zda vystoupí, nebo jen poslouchá.",
    ),
    "zlodejka": (
        "předvádí karetní trik a nechává ostatní hádat, jak ho provedla.",
        "vymyslela hru s hledáním drobných předmětů po domě.",
        "se vrací z trhu s příběhem o obchodníkovi, který prodával falešné mapy.",
    ),
    "vampirka": (
        "si v klidné místnosti čte při tlumeném světle a nabídne ostatním společnost.",
        "připravuje noční čajový dýchánek pro ty, kterým se nechce spát.",
        "se svěří, že našla místo, kde se jí dobře přemýšlí.",
    ),
    "templarka": (
        "navrhuje pravidla společné služby, která jsou stejná pro všechny.",
        "opravuje starou výstroj a vypráví, proč ji chce používat jen k ochraně.",
        "připravuje seznam věcí, které by pomohly lidem v nejchudší čtvrti.",
    ),
}


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

    z = _sesterska_rivalita(hra, aktivni)
    if z:
        zpravy.extend(z)

    z = _haremova_intimita_a_lazne(hra, aktivni)
    if z:
        zpravy.extend(z)

    z = _dar_od_oddanych(hra, aktivni)
    if z:
        zpravy.extend(z)

    if random.random() < 0.7:
        z = _scena_osobnosti(hra, aktivni)
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

    if aktivni and getattr(getattr(hra, "nastaveni", None), "ai_dialogy", False):
        try:
            from game.ai_dialog import generuj_dialog
            o = random.choice(aktivni)
            typ = "noční_scéna"
            if any("žárl" in m.lower() for m in zpravy):
                typ = "žárlivost"
            if any("zrád" in m.lower() for m in zpravy):
                typ = "vzdor"
            dialog = generuj_dialog(o, hra.hrac, typ, nastaveni=hra.nastaveni, ticho=True)
            zpravy.append(f"💬 {dialog}")
        except Exception:
            pass
    return zpravy


def _scena_osobnosti(hra, aktivni):
    dostupne = [
        otrok for otrok in aktivni
        if not getattr(otrok, "na_najmu", False)
    ]
    if not dostupne:
        return []

    def posledni_scena_den(otrok):
        for zaznam in reversed(getattr(otrok, "historie_voleb", [])):
            if isinstance(zaznam, dict) and zaznam.get("typ") == "noční_scéna":
                try:
                    return int(zaznam.get("den", 0))
                except (TypeError, ValueError):
                    return 0
        return 0

    nejmene_videne = min(posledni_scena_den(otrok) for otrok in dostupne)
    kandidatky = [
        otrok for otrok in dostupne
        if posledni_scena_den(otrok) == nejmene_videne
    ]
    otrok = random.choice(kandidatky)
    charakter = normalizuj_charakter(getattr(otrok, "charakter", ""))
    sceny = SCENY_OSOBNOSTI.get(charakter)
    if sceny:
        scena = random.choice(sceny)
    else:
        scena = (
            f"si vybere vlastní činnost podle své povahy "
            f"({CHARAKTERY[charakter]['nazev'].lower()}) a pozve ostatní, "
            "aby se přidaly, pokud chtějí."
        )
    otrok.zvysit_stat("duvera", 1)
    otrok.zaznamenej_volbu("noční_scéna", "Spontánní chvíle v harému", hra.hrac.den)
    return [f"🌙 {otrok.jmeno} {scena}"]


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


def _sesterska_rivalita(hra, aktivni):
    if len(aktivni) < 2 or random.random() > 0.30:
        return []
    o1, o2 = random.sample(aktivni, 2)
    sceny = [
        f"⚡ {o1.jmeno} a {o2.jmeno} se přely, která z nich lépe slouží tvé vůli. Rivalita zvyšuje jejich poslušnost!",
        f"👁️ {o1.jmeno} žárlivě sledovala {o2.jmeno}, když jsi kolem ní prošel. Napětí v harému houstne.",
        f"👑 {o1.jmeno} se pokusila předvést před {o2.jmeno}, aby dokázala své prvenství u tvého lože.",
    ]
    o1.zvysit_stat("poslusnost", 3)
    o2.zvysit_stat("poslusnost", 3)
    return [random.choice(sceny)]


def _haremova_intimita_a_lazne(hra, aktivni):
    if len(aktivni) < 2 or random.random() > 0.35:
        return []
    o1, o2 = random.sample(aktivni, 2)
    o1.zvysit_stat("loajalita", 4)
    o2.zvysit_stat("loajalita", 4)
    o1.zvysit_stat("touha", 6)
    o2.zvysit_stat("touha", 6)
    return [
        f"🌸 V nočních lázních panovala harmonie — {o1.jmeno} a {o2.jmeno} se společně koupaly v provoněné vodě. Pouto v harému sílí."
    ]


def _dar_od_oddanych(hra, aktivni):
    oddané = [o for o in aktivni if getattr(o, "loajalita", 0) >= 60 and getattr(o, "duvera", 0) >= 45]
    if not oddané or random.random() > 0.25:
        return []
    o = random.choice(oddané)
    if random.random() < 0.5:
        dar_zl = random.randint(30, 80)
        hra.hrac.gold += dar_zl
        return [f"🎁 {o.jmeno} ti s plachým úsměvem věnovala rodinný klenot ze své skrýše (+{dar_zl} 🪙)!"]
    else:
        hra.hrac.dark_energy = min(100, hra.hrac.dark_energy + 15)
        return [f"✨ {o.jmeno} ti před spaním vděčně vmasírovala vonné oleje do spánků (+15 temné energie, harmonie)!"]
