"""Statická data pro propojená města a rozhodovací profily NPC."""

MESTA = {
    "stare_mesto": {
        "nazev": "Staré město",
        "popis": "Původní sídlo dominia, jeho cechů a městských frakcí.",
        "lokace": (
            "pevnost", "trh", "pristav", "hostinec", "akademie",
            "cervena_ctvrt", "palac_bohatych", "cechovni_ulicky",
            "pulnocni_trh", "ricni_nabrezi", "univerzitni_okrsek",
            "akademicke_namesti", "tekno_party",
        ),
        "prosperita": 58,
        "bezpeci": 62,
        "stabilita": 60,
    },
    "vychodni_brod": {
        "nazev": "Východní Brod",
        "popis": "Říční město karavan, lodníků a pohraničních osad.",
        "lokace": (
            "vychodni_pristav", "vychodni_trziste", "rada_vychodniho_brodu",
            "vychodni_kasarna", "vychodni_zahrady",
        ),
        "prosperita": 44,
        "bezpeci": 38,
        "stabilita": 46,
    },
}

FRAKCNI_ZONY = {
    "policie": (
        "pevnost", "hranice", "hostinec", "severni_hradby",
        "rada_vychodniho_brodu", "vychodni_kasarna",
    ),
    "obchodnici": (
        "trh", "ctvrt_remeselniku", "pristav", "molo_mesicniho_pristavu", "ricni_nabrezi",
        "cechovni_ulicky", "kupecke_ulice", "vychodni_pristav",
        "vychodni_trziste", "vychodni_zahrady",
    ),
    "podsveti": (
        "katakomby", "tajna_svatyne_stinu", "paserska_zatoka",
        "dymova_ctvrt", "pulnocni_trh", "cerna_ctvrt",
        "podzemni_arena", "stare_katakomby", "kanalove_pruplavy",
    ),
    "cirkev": ("chram_cistoty", "vezeni_inkvizice"),
    "kult_krve": (
        "les", "svatyne_krvaveho_mesice", "observator",
        "zricenina_astralni_veze", "krvavy_lom",
    ),
    "syndikat_stinu": ("lucernova_ctvrt", "univerzitni_okrsek"),
    "cech_kurtizan": (
        "cervena_ctvrt", "palac_bohatych", "lazne", "stribrne_terasy",
        "zahradni_altan",
    ),
    "narkomani": ("haj_soumraku", "sklenena_zahrada"),
    "cyberpunkaci": (
        "akademie", "akademicke_namesti", "kovarensky_okrsek",
    ),
    "nymfomanky": ("botanicke_zahrady",),
    "gembleri": ("cervena_ctvrt", "pulnocni_trh", "podzemni_arena"),
    "systemaci": ("tekno_party", "dymova_ctvrt", "akademie"),
}

LOKACE_VYCHODNIHO_BRODU = {
    "vychodni_pristav": {
        "nazev": "Východní přístav",
        "kratky": "Východní přístav",
        "ikona": "⛵",
        "typ_ctvrti": "vodní",
        "mesto": "vychodni_brod",
        "popis": "Říční molo Východního Brodu propojuje Staré město s obchodními cestami na východ.",
        "sousedni": ["pristav", "molo_mesicniho_pristavu", "vychodni_trziste"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "vychodni_trziste": {
        "nazev": "Východní tržiště",
        "kratky": "Východní trh",
        "ikona": "🧺",
        "typ_ctvrti": "kupecká",
        "mesto": "vychodni_brod",
        "popis": "Karavany zde mění zboží za říční přepravu a zprávy z okolních osad.",
        "sousedni": [
            "vychodni_pristav", "rada_vychodniho_brodu", "vychodni_kasarna",
        ],
        "uroven": 2,
        "nebezpeci": "nízké",
    },
    "rada_vychodniho_brodu": {
        "nazev": "Radnice Východního Brodu",
        "kratky": "Radnice",
        "ikona": "🏛️",
        "typ_ctvrti": "politická",
        "mesto": "vychodni_brod",
        "popis": "Městská rada hledá spojence, kteří dokážou obnovit důvěru obyvatel.",
        "sousedni": ["vychodni_trziste", "vychodni_zahrady"],
        "uroven": 2,
        "nebezpeci": "nízké",
    },
    "vychodni_kasarna": {
        "nazev": "Kasárna na východní cestě",
        "kratky": "Východní kasárna",
        "ikona": "🛡️",
        "typ_ctvrti": "vojenská",
        "mesto": "vychodni_brod",
        "popis": "Pohraniční vojáci střeží mosty i rozptýlené osady za městskými hradbami.",
        "sousedni": ["vychodni_trziste", "vychodni_zahrady"],
        "uroven": 3,
        "nebezpeci": "střední",
    },
    "vychodni_zahrady": {
        "nazev": "Zahrady za řekou",
        "kratky": "Zahrady",
        "ikona": "🌱",
        "typ_ctvrti": "zahradní",
        "mesto": "vychodni_brod",
        "popis": "Úrodné zahrady zásobují město, ale jejich zavlažovací kanály potřebují opravu.",
        "sousedni": ["rada_vychodniho_brodu", "vychodni_kasarna"],
        "uroven": 1,
        "nebezpeci": "bezpečno",
    },
}

PROFILY_AI_NPC = {
    "mira_lecitelka": {"metrika": "bezpeci", "smer": "minimum"},
    "radan_paserak": {"metrika": "stabilita", "smer": "minimum"},
    "elian_informator": {"metrika": "stabilita", "smer": "minimum"},
    "selene_vedma": {"metrika": "prosperita", "smer": "minimum"},
    "talia_kupkyne": {"metrika": "prosperita", "smer": "minimum"},
    "vespera_kuryrka": {"metrika": "bezpeci", "smer": "minimum"},
    "nela_umelkyne": {"metrika": "prosperita", "smer": "minimum"},
    "nora_kartografka": {"metrika": "stabilita", "smer": "minimum"},
    "zora_bylinkarka": {"metrika": "bezpeci", "smer": "minimum"},
    "mira_vychodni": {"metrika": "bezpeci", "smer": "minimum"},
    "rovan_kapitan": {"metrika": "bezpeci", "smer": "minimum"},
    "vesna_radni": {"metrika": "stabilita", "smer": "minimum"},
}

DOPADY_AI_NPC = {
    "mira_lecitelka": ("bezpeci", 2),
    "radan_paserak": ("prosperita", 1),
    "elian_informator": ("stabilita", 1),
    "selene_vedma": ("stabilita", 1),
    "talia_kupkyne": ("prosperita", 2),
    "vespera_kuryrka": ("bezpeci", 1),
    "nela_umelkyne": ("prosperita", 1),
    "nora_kartografka": ("stabilita", 1),
    "zora_bylinkarka": ("bezpeci", 1),
    "mira_vychodni": ("bezpeci", 2),
    "rovan_kapitan": ("bezpeci", 1),
    "vesna_radni": ("stabilita", 2),
}

AKCE_VYCHODNIHO_BRODU = {
    "vychodni_pristav": {
        "pruzkum": "Zkontrolovat říční náklad",
        "kontakt": "Domluvit bezpečný lodní průjezd",
        "frakce": "obchodnici",
        "odmena": "zlato",
    },
    "vychodni_trziste": {
        "pruzkum": "Prověřit ceny karavan",
        "kontakt": "Podpořit místní obchodníky",
        "frakce": "obchodnici",
        "odmena": "drevo",
    },
    "rada_vychodniho_brodu": {
        "pruzkum": "Prostudovat městské záznamy",
        "kontakt": "Zprostředkovat dohodu s radou",
        "frakce": "policie",
        "odmena": "vyzkum",
    },
    "vychodni_kasarna": {
        "pruzkum": "Prověřit pohraniční hlídky",
        "kontakt": "Nabídnout výcvikovou spolupráci",
        "frakce": "policie",
        "odmena": "zelezo",
    },
    "vychodni_zahrady": {
        "pruzkum": "Prohledat zavlažovací kanály",
        "kontakt": "Zajistit zahradám ochranu",
        "frakce": "obchodnici",
        "odmena": "krystaly",
    },
}
