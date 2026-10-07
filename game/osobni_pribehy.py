"""Krátké, větvené osobní příběhy členek harému."""

from data.charaktery import CHARAKTERY, normalizuj_charakter
from utils.vypis import hlavicka, tisk_chyba, tisk_info, tisk_ok, vytiskni_volbu

PRIBEHY = {
    "subka": {
        "cil": "Najít odvahu říct, co jí vyhovuje a kde potřebuje zpomalit.",
        "sceny": (
            "Přizná, že často souhlasí dřív, než si stačí promyslet vlastní odpověď.",
            "Zkouší vyslovit své přání nahlas a čeká, zda ho vezmeš vážně.",
            "Sepíše si vlastní pravidla a chce, aby se jimi vaše domluvy řídily.",
        ),
    },
    "odvazna": {
        "cil": "Proměnit svou odvahu v samostatný projekt, na který bude hrdá.",
        "sceny": (
            "Vzpomene na riskantní útěk z minulosti a na člověka, který jí tehdy pomohl.",
            "Chce prověřit svůj plán, ale tentokrát bez zbytečného hazardu.",
            "Dokončila výpravu a rozhoduje, jak naloží s nově získanou jistotou.",
        ),
    },
    "ustrasena": {
        "cil": "Vybudovat si bezpečné zázemí a rozhodovat o svém denním režimu.",
        "sceny": (
            "Požádá o klidné místo, kde se může vyspat bez vyrušování.",
            "Sama navrhne, kdo smí vstoupit do jejího pokoje a kdy.",
            "Připravila si svůj bezpečný koutek a chce jeho pravidla oznámit ostatním.",
        ),
    },
    "vzdorna": {
        "cil": "Prosadit vlastní pravidla férové spolupráce.",
        "sceny": (
            "Řekne ti, že nedůvěřuje slibům bez činů a konkrétních hranic.",
            "Sepíše podmínky, které by podle ní měly platit pro každého.",
            "Předloží návrh společné dohody a čeká, zda jej přijmeš jako rovnocenný hlas.",
        ),
    },
    "touha": {
        "cil": "Najít rovnováhu mezi silnými emocemi, odpočinkem a vlastními cíli.",
        "sceny": (
            "Popíše, jak ji někdy vlastní nadšení zahltí a proč potřebuje čas na rozmyšlenou.",
            "Zkouší si naplánovat chvíle radosti i klidný čas jen pro sebe.",
            "Vytvořila si režim, který jí pomáhá držet se vlastních rozhodnutí.",
        ),
    },
    "zlomena": {
        "cil": "Obnovit ztracené zájmy malými kroky, které si sama zvolí.",
        "sceny": (
            "Jen tiše přizná, že si už dlouho nepamatuje, co ji dříve těšilo.",
            "Vybere si jednu drobnou činnost, kterou chce zkusit bez tlaku na výsledek.",
            "Našla činnost, ke které se chce vracet, a stanoví si vlastní tempo.",
        ),
    },
    "manipulativni": {
        "cil": "Vybudovat vztah založený na otevřených kartách a vzájemné důvěře.",
        "sceny": (
            "Přizná, že se naučila zkoušet lidi oklikou, protože přímá žádost dříve selhala.",
            "Zkusí říct, co potřebuje, bez skrytých podmínek.",
            "Navrhne dohodu, v níž oba víte, co nabízíte a co očekáváte.",
        ),
    },
    "chladna": {
        "cil": "Najít způsob, jak sdílet své myšlenky bez předstírání emocí.",
        "sceny": (
            "Řekne, že málokdy cítí potřebu mluvit, ale nechce být považována za lhostejnou.",
            "Vybere si téma, o kterém je ochotná vést věcný rozhovor.",
            "Sepíše stručný dopis, kterým vyjádří to, co se jí říká obtížně.",
        ),
    },
    "hysterialni": {
        "cil": "Vytvořit si plán, který jí pomůže zvládat náhlé změny nálad.",
        "sceny": (
            "Popíše, jak rychle se jí někdy změní nálada, a co jí v takovou chvíli pomáhá.",
            "Zkouší několik klidových postupů a vybírá si ty, které jí vyhovují.",
            "Sestavila si vlastní plán pro těžké chvíle a chce, abyste ho respektovali.",
        ),
    },
    "slechticna": {
        "cil": "Rozhodnout, které tradice si chce ponechat a které opustit.",
        "sceny": (
            "Vzpomene na rodinný erb a na povinnosti, které jí nikdy nedávaly smysl.",
            "Zvažuje, které části svého původu chce dál nést jako vlastní volbu.",
            "Navrhne nový erb, který vystihuje její budoucnost, ne jen minulost.",
        ),
    },
    "nymfomanka": {
        "cil": "Sama si nastavit rovnováhu mezi odpočinkem, zdravím a potěšením.",
        "sceny": (
            "Otevřeně mluví o tom, že silné impulzy někdy předběhnou její potřeby.",
            "Vybírá si způsoby, jak dát přednost zdraví a odpočinku, když je potřebuje.",
            "Sestavila si osobní plán péče a rozhodla, které hranice jsou pro ni důležité.",
        ),
    },
    "ticha_panenka": {
        "cil": "Najít vlastní hlas, i kdyby ho chtěla používat jen občas.",
        "sceny": (
            "Místo odpovědi ti podá lístek s jedinou otázkou, na kterou by chtěla znát názor.",
            "Napíše několik věcí, které jí dělají dobře, a které naopak nechce.",
            "Rozhodne se, komu svůj seznam ukáže a co si ponechá jen pro sebe.",
        ),
    },
    "krvava_subka": {
        "cil": "Zvolit si bezpečnou podobu tréninku a jasné signály pro přestávku.",
        "sceny": (
            "Navrhne náročný trénink, ale chce nejdřív společně domluvit bezpečné hranice.",
            "Vytvoří pravidla, signály a kontrolu po každém cvičení.",
            "Trénink proběhne podle její dohody a ona vyhodnotí, co příště změnit.",
        ),
    },
    "posedla": {
        "cil": "Oddělit vlastní přání od očekávání, která si přinesla z minulosti.",
        "sceny": (
            "Přizná, že někdy hledá jistotu v tom, že za ni rozhodnou druzí.",
            "Sepíše si několik rozhodnutí, která chce tentokrát udělat sama.",
            "Vybere si jeden vlastní cíl a požádá jen o podporu, kterou skutečně chce.",
        ),
    },
    "kurtizana": {
        "cil": "Najít vlastní profesní směr a podmínky, za kterých chce pracovat.",
        "sceny": (
            "Vzpomíná na dobu, kdy si mohla sama vybírat, komu věnuje svůj čas.",
            "Předloží seznam podmínek, které potřebuje pro bezpečnou a férovou práci.",
            "Rozhodne, zda chce učit, vystupovat, nebo se věnovat úplně jiné činnosti.",
        ),
    },
    "fanaticka": {
        "cil": "Znovu prozkoumat své přesvědčení a svobodně si vybrat, čemu věří.",
        "sceny": (
            "Připustí, že některé naučené odpovědi už v ní vyvolávají otázky.",
            "Prostuduje různé pohledy a sama si určí, kterým chce věnovat pozornost.",
            "Pojmenuje zásady, které přijímá z vlastní vůle, a ty, které odmítá.",
        ),
    },
    "amazonka": {
        "cil": "Založit výcvikový kruh, kde se síla měří i schopností chránit.",
        "sceny": (
            "Vypráví o svém prvním turnaji a o soupeřce, která si získala její respekt.",
            "Navrhne výcvik, v němž si každý může zvolit obtížnost a bezpečné tempo.",
            "První lekce skončila; ona sama rozhodne, koho chce příště učit.",
        ),
    },
    "carodejka": {
        "cil": "Bezpečně prozkoumat své magické schopnosti bez cizího dozoru.",
        "sceny": (
            "Ukáže ti drobný trik, který se bála před ostatními zopakovat.",
            "Připraví bezpečný pokus a sama určí, kdo smí být přítomen.",
            "Pokus se vydařil. Rozhodne se, jak a komu své poznatky předá.",
        ),
    },
    "knezka_temnoty": {
        "cil": "Vytvořit osobní rituál, který vyjadřuje její přesvědčení, ne cizí příkazy.",
        "sceny": (
            "Přizná, že její staré modlitby někdo používal k ovládání druhých.",
            "Navrhne nový obřad, v němž každý účastník může svobodně odmítnout.",
            "Rituál je připraven; sama určí, zda ho chce sdílet, nebo ponechat soukromý.",
        ),
    },
    "zlodejka": {
        "cil": "Proměnit své znalosti uliček v legální síť pomoci a varování.",
        "sceny": (
            "Ukáže ti značky, kterými si dříve předávali varování lidé z ulic.",
            "Navrhne bezpečnou síť zpráv, která nebude sledovat ani vydírat její známé.",
            "Síť funguje a ona rozhoduje, komu chce dál pomáhat.",
        ),
    },
    "padla_paladinka": {
        "cil": "Najít nový smysl služby, který nevyžaduje zradu vlastního svědomí.",
        "sceny": (
            "Vzpomene na přísahu, kterou kdysi složila, a na důvod, proč ji opustila.",
            "Rozhoduje se, které části svého slibu chce znovu přijmout po svém.",
            "Sepíše nový kodex ochrany slabších podle vlastního svědomí.",
        ),
    },
    "sukuba_hybrid": {
        "cil": "Poznat svou démonickou stránku a sama určit, jak s ní naloží.",
        "sceny": (
            "Přizná, že se celý život snažila skrývat zvláštní sílu, které nerozuměla.",
            "Experimentuje s jejími projevy v bezpečných podmínkách a může kdykoli přestat.",
            "Rozhodne, zda své schopnosti využije, bude je dál studovat, nebo je nechá odpočívat.",
        ),
    },
    "alchymistka": {
        "cil": "Dokončit bezpečný výzkum a zveřejnit výsledky pod vlastním jménem.",
        "sceny": (
            "Přizná, že její dřívější výzkum někdo vydával za svůj.",
            "Připraví protokol, který jasně popisuje rizika a bezpečné zacházení.",
            "Výsledky jsou hotové a ona sama rozhodne, komu je předá.",
        ),
    },
    "princezna_ruin": {
        "cil": "Rozhodnout, zda chce obnovit rodový odkaz, nebo začít úplně znovu.",
        "sceny": (
            "Vzpomene na své království a na lidi, jejichž osud jí stále leží na srdci.",
            "Zvažuje plán obnovy, ale chce nejdřív znát přání těch, kterých se týká.",
            "Rozhodne, zda bude usilovat o návrat, nebo vytvoří nový domov.",
        ),
    },
    "kralovska_knezka": {
        "cil": "Obnovit léčebnou svatyni, která pomáhá všem bez rozdílu.",
        "sceny": (
            "Vypráví o staré svatyni, kde se kdysi léčilo bez otázek na původ.",
            "Připraví seznam potřeb a pravidla, která zajistí dostupnou péči.",
            "Svatyně se otevírá a ona sama si vybere, jakou roli v ní chce mít.",
        ),
    },
    "draci_misenka": {
        "cil": "Naučit se bezpečně ovládat dračí sílu a sama určit její využití.",
        "sceny": (
            "Popíše první chvíli, kdy v sobě ucítila žár, který nedokázala vysvětlit.",
            "Vymyslí cvičení, které jí pomůže sílu poznat bez ohrožení okolí.",
            "Získala jistotu a rozhoduje, zda chce schopnost ukázat, nebo dál trénovat v soukromí.",
        ),
    },
    "temna_elfka": {
        "cil": "Najít vlastní místo mezi dvěma kulturami bez nutnosti cokoli předstírat.",
        "sceny": (
            "Vypráví o domově pod zemí a o zvycích, které jí v novém prostředí chybí.",
            "Navrhne večer, na kterém představí jen ty tradice, které chce sdílet.",
            "Rozhodne, které části své kultury chce zachovat pro sebe a které předat dál.",
        ),
    },
    "badatelka": {
        "cil": "Najít místo, kde může bádat bez strachu z cenzury.",
        "sceny": (
            "Z jejího zápisníku vypadne nedokončená mapa starých ruin. „Někdo mi kdysi zakázal klást otázky.“",
            "Objevila stopu k chybějícímu svazku, ale nechce se vydat do archivu sama.",
            "Položí před tebe hotovou mapu. Rozhoduje se, komu své poznání zpřístupní.",
        ),
    },
    "diplomatka": {
        "cil": "Vyjednat bezpečnou dohodu, ve které budou její přání vyslyšena.",
        "sceny": (
            "Přizná, že kdysi urovnávala spory mezi znepřátelenými rody.",
            "Nabídne vlastní plán jednání a trvá na tom, že se bude moci kdykoli stáhnout.",
            "Dohoda je připravena. Zbývá vybrat, jaké podmínky budou pro ni nepřekročitelné.",
        ),
    },
    "ochranitelka": {
        "cil": "Založit hlídku, která chrání lidi a respektuje jejich rozhodnutí.",
        "sceny": (
            "Vypráví o vesnici, kterou kdysi nedokázala ochránit, a ptá se, zda jí pomůžeš začít znovu.",
            "Sestavila plán obrany a žádá, aby pravidla hlídky platila pro všechny stejně.",
            "Nová hlídka čeká na svůj první rozkaz. Ona chce, aby jejím cílem byla ochrana, ne zastrašování.",
        ),
    },
    "umelkyne": {
        "cil": "Dokončit vlastní dílo a sama rozhodnout, komu ho ukáže.",
        "sceny": (
            "Ukáže ti pár tahů v náčrtníku, ale zatím si nechává zbytek pro sebe.",
            "Našla inspiraci pro nové dílo a vybírá si, zda chce společnost, nebo klid.",
            "Dílo je hotové. Sama určí, zda zůstane soukromé, nebo bude vystaveno.",
        ),
    },
    "vampirka": {
        "cil": "Naučit se ovládat vlastní hlad a chránit si místo, které si sama zvolila.",
        "sceny": (
            "Přizná, že její hlad ji někdy přiměje jednat bez přemýšlení.",
            "Vybírá si bezpečný režim, který ji pomůže zůstat v klidu i po setmění.",
            "Rozhoduje se, kdo smí vidět její skutečnou tvář a kdo zůstane jen ve stínu.",
        ),
    },
    "templarka": {
        "cil": "Najít nový cíl služby, který neporušuje její vlastní svědomí.",
        "sceny": (
            "Vzpomene na vlastní přísahu a na okamžik, kdy jí zničila vrcholná jistota.",
            "Zkouší rozdíl mezi poslušností a skutečnou ochranou těch, které má chránit.",
            "Sestaví nový kodex, podle kterého bude sloužit i bez cizích rozkazů.",
        ),
    },
    "mecenaska": {
        "cil": "Vytvořit si vlastní standard lásky a síly bez výčitek z minulého života.",
        "sceny": (
            "Vypráví o předchozím světě výhod, přízně a závazků, které jí nikdy nepřinesly klid.",
            "Rozhoduje, co od vztahů skutečně chce a čeho se nehodlá vzdát.",
            "Pořádá si vlastní pravidla pro rovnost, důstojnost a laskavost ve vztahu.",
        ),
    },
    "cartografka": {
        "cil": "Vytvořit mapu města, která zachová i místních obyvatel známost o bezpečných cestách.",
        "sceny": (
            "Našla starý plánek, na kterém někdo pečlivě označil zapomenuté studny a průchody.",
            "Vyslechne místní průvodce a rozhodne, které informace smějí být veřejné.",
            "Dokončí mapu a sama zvolí, komu ji předá a které části ponechá soukromé.",
        ),
    },
    "lekarka": {
        "cil": "Otevřít léčebnu s péčí založenou na důvěrnosti a svobodném rozhodování pacientů.",
        "sceny": (
            "Vzpomene na svou první lékařskou praxi a na pacienta, kterému nemohla pomoci.",
            "Sepíše pravidla soukromí a zjišťuje, jaké vybavení lidé skutečně potřebují.",
            "Léčebna je připravena; sama určí její provozní dobu i vlastní roli.",
        ),
    },
    "veteranka": {
        "cil": "Předat své zkušenosti nové hlídce, aniž by opakovala chyby starého velení.",
        "sceny": (
            "Vypráví o těžké službě, která ji naučila, že rozkaz bez vysvětlení může uškodit.",
            "Navrhne výcvik, kde se ochrana civilistů a možnost odmítnout nebezpečný úkol berou vážně.",
            "Hlídka je připravena; sama se rozhodne, zda chce vést, radit, nebo odejít do klidu.",
        ),
    },
}

BRANY = ((0, 0), (30, 20), (50, 40))


def dej_pro_clenku(otrok):
    archetyp = normalizuj_charakter(getattr(otrok, "charakter", ""))
    pribeh = PRIBEHY.get(archetyp)
    if pribeh:
        return pribeh
    povaha = CHARAKTERY[archetyp]["nazev"].lower()
    return {
        "cil": f"Najít vlastní cestu, která odpovídá její povaze ({povaha}).",
        "sceny": (
            "Opatrně začne vyprávět o svém životě před příchodem do dominia.",
            "Přemýšlí, co by chtěla změnit, kdyby měla podporu a možnost volby.",
            "Je připravena učinit vlastní rozhodnutí o tom, co pro ni bude dál důležité.",
        ),
    }


def zobraz_denik_postavy(otrok):
    pribeh = dej_pro_clenku(otrok)
    krok = max(0, min(3, int(getattr(otrok, "osobni_pribeh_krok", 0))))
    dokoncen = bool(getattr(otrok, "osobni_pribeh_dokonceno", False)) or krok >= 3
    hlavicka(f"Osobní deník: {otrok.jmeno}")
    print(f"Povaha: {CHARAKTERY[normalizuj_charakter(otrok.charakter)]['nazev']}")
    print(f"Přání: {pribeh['cil']}")
    stav = "uzavřený příběh" if dokoncen else f"kapitola {krok + 1}/3"
    print(f"Postup: {krok}/3 — {stav}")
    if getattr(otrok, "osobni_pribeh_zaver", ""):
        print(f"Závěr: {otrok.osobni_pribeh_zaver}")
    if not dokoncen:
        duvera, loajalita = BRANY[krok]
        print(
            f"Další kapitola: důvěra {duvera}+ a loajalita {loajalita}+ "
            f"(aktuálně {otrok.duvera}/{otrok.loajalita})."
        )
    print("\nDůležité okamžiky:")
    historie = getattr(otrok, "historie_voleb", [])
    zaznamy = [
        zaznam for zaznam in historie
        if isinstance(zaznam, dict)
        and zaznam.get("typ") in {"osobní příběh", "rozhovor", "osud", "vztah"}
    ]
    if not zaznamy:
        print("  Zatím tu není žádný zapsaný okamžik.")
    for zaznam in zaznamy[-10:]:
        den = f" — den {zaznam['den']}" if "den" in zaznam else ""
        print(f"  • {zaznam.get('volba', '')}{den}")


def pokracuj_v_pribehu(hra, otrok):
    krok = max(0, min(3, int(getattr(otrok, "osobni_pribeh_krok", 0))))
    if getattr(otrok, "osobni_pribeh_dokonceno", False) or krok >= 3:
        otrok.osobni_pribeh_dokonceno = True
        tisk_info(f"Příběh {otrok.jmeno} je uzavřen. Její deník si můžeš znovu pročíst.")
        return False

    pozadovana_duvera, pozadovana_loajalita = BRANY[krok]
    if otrok.duvera < pozadovana_duvera or otrok.loajalita < pozadovana_loajalita:
        tisk_info(
            f"Nejdřív je potřeba více důvěry a společných zkušeností "
            f"(důvěra {pozadovana_duvera}, loajalita {pozadovana_loajalita})."
        )
        return False

    pribeh = dej_pro_clenku(otrok)
    hlavicka(f"Kapitola {krok + 1}: {otrok.jmeno}")
    print(pribeh["sceny"][krok])
    vytiskni_volbu("1", "Naslouchat a nechat ji určit další krok")
    vytiskni_volbu("2", "Nabídnout pomoc a společně připravit plán")
    vytiskni_volbu("0", "Vrátit se později")
    try:
        volba = input("> ").strip()
    except EOFError:
        return False
    if volba == "0":
        return False
    if volba not in ("1", "2"):
        tisk_chyba("Neplatná volba příběhu.")
        return False

    if volba == "1":
        otrok.zvysit_stat("duvera", 8)
        otrok.zvysit_stat("loajalita", 3)
        rozhodnuti = "Naslouchal jsi a nechal ji zvolit další krok."
    else:
        otrok.zvysit_stat("duvera", 5)
        otrok.zvysit_stat("loajalita", 6)
        rozhodnuti = "Společně jste připravili plán podle jejích podmínek."
    otrok.osobni_pribeh_volby.append(
        {"kapitola": krok + 1, "volba": int(volba), "den": hra.hrac.den}
    )
    otrok.osobni_pribeh_krok = krok + 1
    otrok.zaznamenej_volbu("osobní příběh", rozhodnuti, hra.hrac.den)
    hra.hrac.pridej_xp(10 + krok * 5)
    if krok == 2:
        otrok.osobni_pribeh_dokonceno = True
        volby = getattr(otrok, "osobni_pribeh_volby", [])
        samostatne = sum(zaznam.get("volba") == 1 for zaznam in volby if isinstance(zaznam, dict))
        spolecne = sum(zaznam.get("volba") == 2 for zaznam in volby if isinstance(zaznam, dict))
        if samostatne == 3:
            otrok.osobni_pribeh_zaver = f"Vlastní cesta: {pribeh['cil']}"
        elif spolecne >= 2:
            otrok.osobni_pribeh_zaver = f"Společný plán: {pribeh['cil']}"
        else:
            otrok.osobni_pribeh_zaver = f"Nový začátek: {pribeh['cil']}"
        tisk_ok(f"Příběh {otrok.jmeno} je dokončen. Získáváš {10 + krok * 5} XP.")
    else:
        tisk_ok(f"Posun v příběhu {otrok.jmeno}. Získáváš {10 + krok * 5} XP.")
    return True
