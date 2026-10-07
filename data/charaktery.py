# data/charaktery.py
import random


# Dark Expansion v1.0 – nové archetypy

CHARAKTERY = {
    "subka": {
        "nazev": "Submisivní",
        "popis": "Poslušná a touží po vedení.",
        "modifikatory": {
            "submisivita": 1.3,
            "poslusnost": 1.2,
            "duvera": 1.1,
            "strach": 0.8
        },
        "reakce_na_trest": 1.2,
        "reakce_na_odmenu": 1.0,
        "utek_sance": 0.05
    },
    "odvazna": {
        "nazev": "Odvážná",
        "popis": "Vzdoruje, ale lze ji zlomit.",
        "modifikatory": {
            "submisivita": 0.7,
            "poslusnost": 0.6,
            "strach": 0.9
        },
        "reakce_na_trest": 0.8,
        "reakce_na_odmenu": 0.9,
        "utek_sance": 0.15
    },
    "ustrasena": {
        "nazev": "Ustrašená",
        "popis": "Snadno se bojí, ale je poslušná.",
        "modifikatory": {
            "strach": 1.5,
            "submisivita": 1.1,
            "poslusnost": 1.1,
            "duvera": 0.8
        },
        "reakce_na_trest": 1.1,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.02
    },
    "vzdorna": {
        "nazev": "Vzdorná",
        "popis": "Aktivně vzdoruje, potřebuje silnou ruku.",
        "modifikatory": {
            "submisivita": 0.5,
            "poslusnost": 0.5,
            "strach": 0.7
        },
        "reakce_na_trest": 0.7,
        "reakce_na_odmenu": 0.7,
        "utek_sance": 0.2
    },
    "touha": {
        "nazev": "Toužící",
        "popis": "Sexuálně nadržená, snadno ovlivnitelná.",
        "modifikatory": {
            "touha": 1.4,
            "submisivita": 1.0,
            "poslusnost": 0.9,
            "duvera": 1.0
        },
        "reakce_na_trest": 0.9,
        "reakce_na_odmenu": 1.3,
        "utek_sance": 0.06
    },
    "zlomena": {
        "nazev": "Zlomená",
        "popis": "Už zlomená, téměř bez vůle.",
        "modifikatory": {
            "submisivita": 1.5,
            "poslusnost": 1.5,
            "strach": 0.6
        },
        "reakce_na_trest": 1.4,
        "reakce_na_odmenu": 1.1,
        "utek_sance": 0.0
    },
    "manipulativni": {
        "nazev": "Manipulativní",
        "popis": "Snaží se tě ovlivnit, pozor na ni.",
        "modifikatory": {
            "duvera": 0.6,
            "poslusnost": 0.7,
            "submisivita": 0.8
        },
        "reakce_na_trest": 0.6,
        "reakce_na_odmenu": 1.4,
        "utek_sance": 0.1
    },
    "chladna": {
        "nazev": "Chladná",
        "popis": "Bez emocí, těžko se s ní pracuje.",
        "modifikatory": {
            "duvera": 0.7,
            "touha": 0.8,
            "submisivita": 0.9
        },
        "reakce_na_trest": 0.7,
        "reakce_na_odmenu": 0.8,
        "utek_sance": 0.08
    },
    "hysterialni": {
        "nazev": "Hysteriální",
        "popis": "Nestabilní, rychle mění nálady.",
        "modifikatory": {
            "strach": 1.3,
            "touha": 1.1,
            "submisivita": 0.9
        },
        "reakce_na_trest": 1.3,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.12
    },
    # === DARK EXPANSION – nové archetypy ===
    "slechticna": {
        "nazev": "Zlomená šlechtična",
        "popis": "Bývalá urozená dáma. Hrdost se láme pomalu, ale když praskne, padá hluboko.",
        "modifikatory": {
            "submisivita": 0.6,
            "poslusnost": 0.55,
            "duvera": 0.7,
            "strach": 0.85,
            "humiliation": 1.4
        },
        "reakce_na_trest": 0.75,
        "reakce_na_odmenu": 1.25,
        "utek_sance": 0.12
    },
    "nymfomanka": {
        "nazev": "Nymfomanka",
        "popis": "Tělo ji zrazuje. Touha je silnější než pýcha. Snadno se dostane do závislosti na rozkoši.",
        "modifikatory": {
            "touha": 1.6,
            "vlhkost": 1.4,
            "submisivita": 1.1,
            "poslusnost": 0.95,
            "strach": 0.7
        },
        "reakce_na_trest": 0.85,
        "reakce_na_odmenu": 1.5,
        "utek_sance": 0.04
    },
    "ticha_panenka": {
        "nazev": "Tichá panenka",
        "popis": "Mluví málo. Sleduje. Když se zlomí, stává se dokonalou, tichou hračkou.",
        "modifikatory": {
            "submisivita": 1.2,
            "poslusnost": 1.15,
            "duvera": 0.9,
            "strach": 1.1,
            "mindbreak": 1.2
        },
        "reakce_na_trest": 1.15,
        "reakce_na_odmenu": 1.1,
        "utek_sance": 0.03
    },
    "krvava_subka": {
        "nazev": "Krvavá subka",
        "popis": "Bolest ji vzrušuje. Čím víc krve, tím víc se otevírá. Ideální pro drsné tréninky.",
        "modifikatory": {
            "pain_addiction": 1.5,
            "submisivita": 1.25,
            "touha": 1.15,
            "strach": 0.6,
            "scarred": 1.2
        },
        "reakce_na_trest": 1.4,
        "reakce_na_odmenu": 0.9,
        "utek_sance": 0.02
    },
    "posedla": {
        "nazev": "Posedlá",
        "popis": "Něco v ní se už zlomilo dřív, než jsi ji získal. Teď hledá pána, který ji dokončí.",
        "modifikatory": {
            "broken": 1.3,
            "mindbreak": 1.25,
            "submisivita": 1.3,
            "poslusnost": 1.2,
            "loajalita": 1.15
        },
        "reakce_na_trest": 1.35,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.01
    },
    "kurtizana": {
        "nazev": "Kurtizána",
        "popis": "Vytříbená společnice zvyklá na luxus, svádění a štědré zákazníky v nevěstinci.",
        "modifikatory": {
            "touha": 1.4,
            "vlhkost": 1.3,
            "submisivita": 1.1,
            "poslusnost": 1.1,
            "duvera": 1.1
        },
        "reakce_na_trest": 0.9,
        "reakce_na_odmenu": 1.4,
        "utek_sance": 0.04
    },
    "fanaticka": {
        "nazev": "Fanatička",
        "popis": "Hluboce oddaná temnému kultu. Vnímá pána jako boha na zemi a touží sloužit.",
        "modifikatory": {
            "submisivita": 1.4,
            "poslusnost": 1.3,
            "loajalita": 1.5,
            "strach": 0.5,
            "bloodlust": 1.3
        },
        "reakce_na_trest": 1.2,
        "reakce_na_odmenu": 1.1,
        "utek_sance": 0.01
    },
    "amazonka": {
        "nazev": "Amazonka",
        "popis": "Hrdá a svalnatá válečnice, která odmítá sklonit hlavu bez pořádného boje.",
        "modifikatory": {
            "submisivita": 0.5,
            "poslusnost": 0.5,
            "tolerance_bolesti": 1.4,
            "strach": 0.6,
            "bloodlust": 1.2
        },
        "reakce_na_trest": 0.65,
        "reakce_na_odmenu": 0.85,
        "utek_sance": 0.18
    },
    "carodejka": {
        "nazev": "Čarodějka",
        "popis": "Záhadná žena vládnoucí temným esencím. Její pohled proniká přímo do duše.",
        "modifikatory": {
            "submisivita": 0.75,
            "poslusnost": 0.8,
            "duvera": 0.85,
            "mindbreak": 1.15
        },
        "reakce_na_trest": 0.8,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.09
    },
    "knezka_temnoty": {
        "nazev": "Kněžka temnoty",
        "popis": "Odpadlá duchovní, která své modlitby vyměnila za hříšné rituály a temnou rozkoš.",
        "modifikatory": {
            "submisivita": 1.35,
            "poslusnost": 1.25,
            "loajalita": 1.4,
            "touha": 1.25,
            "strach": 0.5,
            "bloodlust": 1.1
        },
        "reakce_na_trest": 1.25,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.02
    },
    "zlodejka": {
        "nazev": "Stínová zlodějka",
        "popis": "Mrštná a drzá dívka z uliček podsvětí. Ráda provokuje a zkouší pánovy hranice.",
        "modifikatory": {
            "submisivita": 0.7,
            "poslusnost": 0.65,
            "duvera": 0.8,
            "touha": 1.25,
            "strach": 0.85
        },
        "reakce_na_trest": 0.75,
        "reakce_na_odmenu": 1.3,
        "utek_sance": 0.12
    },
    "padla_paladinka": {
        "nazev": "Padlá paladinka",
        "popis": "Bývalá svatá bojovnice. Hrdá, svalnatá a neoblomná, dokud její pevnou víru nezlomí temná vášeň.",
        "modifikatory": {
            "submisivita": 0.55,
            "poslusnost": 0.5,
            "tolerance_bolesti": 1.45,
            "strach": 0.5,
            "bloodlust": 1.35
        },
        "reakce_na_trest": 0.6,
        "reakce_na_odmenu": 0.85,
        "utek_sance": 0.16
    },
    "sukuba_hybrid": {
        "nazev": "Sukuba (démonka)",
        "popis": "Dívka s kapkou démonické krve. Její tělo plane neuhasitelným ohněm a svádění má v krvi.",
        "modifikatory": {
            "touha": 1.7,
            "vlhkost": 1.6,
            "submisivita": 1.05,
            "poslusnost": 0.9,
            "duvera": 1.05,
            "strach": 0.4
        },
        "reakce_na_trest": 0.95,
        "reakce_na_odmenu": 1.5,
        "utek_sance": 0.03
    },
    "alchymistka": {
        "nazev": "Travička / Alchymistka",
        "popis": "Zvrácená učenka fascinovaná afrodiziaky, jedy a zakázanými lektvary tělesné rozkoše.",
        "modifikatory": {
            "submisivita": 0.85,
            "poslusnost": 0.9,
            "duvera": 0.95,
            "mindbreak": 1.2,
            "touha": 1.15
        },
        "reakce_na_trest": 0.85,
        "reakce_na_odmenu": 1.25,
        "utek_sance": 0.07
    },
    "princezna_ruin": {
        "nazev": "Exilová princezna",
        "popis": "Urozená dcera padlé dynastie. Zvyklá poroučet celým armádám, nyní ponížena do role otrokyně.",
        "modifikatory": {
            "submisivita": 0.45,
            "poslusnost": 0.4,
            "duvera": 0.6,
            "strach": 0.9,
            "humiliation": 1.55
        },
        "reakce_na_trest": 0.65,
        "reakce_na_odmenu": 1.35,
        "utek_sance": 0.15
    },
    "kralovska_knezka": {
        "nazev": "Královská kněžka",
        "popis": "Posvátná služebnice pradávných bohů. Vládne léčivou aurou a vysokou důstojností.",
        "modifikatory": {
            "submisivita": 0.8,
            "poslusnost": 0.9,
            "duvera": 1.3,
            "loajalita": 1.25,
            "touha": 1.1
        },
        "reakce_na_trest": 0.7,
        "reakce_na_odmenu": 1.4,
        "utek_sance": 0.04
    },
    "draci_misenka": {
        "nazev": "Dračí míšenka",
        "popis": "Nespoutaná válečnice s dračí krví v žilách. Obrovská síla v boji a žhavá vášeň.",
        "modifikatory": {
            "submisivita": 0.6,
            "poslusnost": 0.7,
            "tolerance_bolesti": 1.6,
            "bloodlust": 1.4,
            "touha": 1.3
        },
        "reakce_na_trest": 1.1,
        "reakce_na_odmenu": 1.1,
        "utek_sance": 0.08
    },
    "temna_elfka": {
        "nazev": "Temná elfka",
        "popis": "Podlá a smyslná vražedkyně z podzemních říší. Mistr stínů, mučení a nebezpečné rozkoše.",
        "modifikatory": {
            "submisivita": 0.7,
            "poslusnost": 0.8,
            "pain_addiction": 1.3,
            "touha": 1.4,
            "humiliation": 0.8
        },
        "reakce_na_trest": 0.9,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.10
    },
    "badatelka": {
        "nazev": "Zvídavá badatelka",
        "popis": "Všímavá a přemýšlivá žena, která si důvěru buduje rozhovorem a poznáním.",
        "modifikatory": {
            "duvera": 1.25,
            "loajalita": 1.1,
            "strach": 0.8,
            "touha": 0.9
        },
        "reakce_na_trest": 0.7,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.07
    },
    "diplomatka": {
        "nazev": "Bystrá diplomatka",
        "popis": "Umí číst nálady lidí, vyjednávat a hledat řešení, která dávají smysl oběma stranám.",
        "modifikatory": {
            "duvera": 1.15,
            "loajalita": 1.2,
            "poslusnost": 0.9,
            "submisivita": 0.8
        },
        "reakce_na_trest": 0.65,
        "reakce_na_odmenu": 1.25,
        "utek_sance": 0.08
    },
    "ochranitelka": {
        "nazev": "Odvážná ochranitelka",
        "popis": "Statečná a spolehlivá; nejvíc si cení bezpečí svých blízkých a férového jednání.",
        "modifikatory": {
            "loajalita": 1.2,
            "duvera": 1.1,
            "tolerance_bolesti": 1.2,
            "strach": 0.7
        },
        "reakce_na_trest": 0.65,
        "reakce_na_odmenu": 1.1,
        "utek_sance": 0.1
    },
    "umelkyne": {
        "nazev": "Citlivá umělkyně",
        "popis": "Vnímavá a tvořivá duše, která se otevírá při sdílení příběhů, hudby a nápadů.",
        "modifikatory": {
            "duvera": 1.2,
            "touha": 1.1,
            "loajalita": 1.05,
            "strach": 0.9
        },
        "reakce_na_trest": 0.75,
        "reakce_na_odmenu": 1.25,
        "utek_sance": 0.08
    },
    "vampirka": {
        "nazev": "Vampýrka",
        "popis": "Mladá upírka s hladovějícími instinkty, která se těší na mlčenlivé samoty a podmanivou tmu.",
        "modifikatory": {
            "touha": 1.5,
            "submisivita": 1.1,
            "duvera": 0.85,
            "loajalita": 1.1,
            "strach": 0.7
        },
        "reakce_na_trest": 0.9,
        "reakce_na_odmenu": 1.35,
        "utek_sance": 0.05
    },
    "templarka": {
        "nazev": "Templářka",
        "popis": "Vytrvalá bojovnice s přísným kodexem, která po zlomení hledá jediného pána a službu věrně zastává.",
        "modifikatory": {
            "loajalita": 1.4,
            "poslusnost": 1.1,
            "tolerance_bolesti": 1.3,
            "strach": 0.8,
            "duvera": 1.15
        },
        "reakce_na_trest": 0.7,
        "reakce_na_odmenu": 1.15,
        "utek_sance": 0.12
    },
    "mecenaska": {
        "nazev": "Mecenáška",
        "popis": "Vysoká dáma, která umí rozkazovat a výhodně vyjednávat; přitom v samotě touží po tichém podřízení.",
        "modifikatory": {
            "duvera": 1.2,
            "poslusnost": 0.85,
            "submisivita": 1.0,
            "loajalita": 1.2,
            "touha": 1.05
        },
        "reakce_na_trest": 0.8,
        "reakce_na_odmenu": 1.3,
        "utek_sance": 0.07
    },
    "cartografka": {
        "nazev": "Kartografka",
        "popis": "Pozorná cestovatelka, která si pamatuje cesty i příběhy lidí, jež na nich potkala.",
        "modifikatory": {
            "duvera": 1.15,
            "loajalita": 1.05,
            "strach": 0.85,
            "vyjednavani": 1.1,
        },
        "reakce_na_trest": 0.65,
        "reakce_na_odmenu": 1.15,
        "utek_sance": 0.08,
    },
    "lekarka": {
        "nazev": "Lékařka",
        "popis": "Praktická léčitelka, která věří v péči, informovaný souhlas a soukromí pacientů.",
        "modifikatory": {
            "duvera": 1.25,
            "loajalita": 1.1,
            "strach": 0.75,
            "poslusnost": 0.9,
        },
        "reakce_na_trest": 0.6,
        "reakce_na_odmenu": 1.2,
        "utek_sance": 0.06,
    },
    "veteranka": {
        "nazev": "Veteránka",
        "popis": "Zkušená obránkyně, která upřednostňuje promyšlenou ochranu před zbytečným střetem.",
        "modifikatory": {
            "duvera": 0.95,
            "loajalita": 1.15,
            "tolerance_bolesti": 1.25,
            "strach": 0.7,
        },
        "reakce_na_trest": 0.7,
        "reakce_na_odmenu": 1.05,
        "utek_sance": 0.1,
    },
}


def normalizuj_charakter(charakter):
    """Vrátí platný klíč charakteru nebo bezpečný fallback."""
    if isinstance(charakter, str):
        klic = charakter.strip().casefold()
        if klic in CHARAKTERY:
            return klic
        aliasy = {
            "amazonka (bojovnice)": "amazonka",
            "amazonka bojovnice": "amazonka",
            "válečnice": "amazonka",
            "čarodějka": "carodejka",
            "kurtizána": "kurtizana",
            "alchymistka": "alchymistka",
            "stínová zlodějka": "zlodejka",
            "svůdnice": "touha",
            "zvrácená": "posedla",
            "zvracena": "posedla",
            "vampýrka": "vampirka",
            "vampirka": "vampirka",
            "templářka": "templarka",
            "mecenáška": "mecenaska",
            "kartografka": "cartografka",
            "lékařka": "lekarka",
            "veteránka": "veteranka",
        }
        if klic in aliasy:
            return aliasy[klic]
    return "subka"


def vyber_charakter():
    """Vybere platný archetyp pro nově získanou postavu."""
    return random.choice(tuple(CHARAKTERY))


def nazev_charakteru(charakter):
    """Vrátí název charakteru i pro neznámé nebo poškozené hodnoty."""
    return CHARAKTERY.get(normalizuj_charakter(charakter), CHARAKTERY["subka"])['nazev']
