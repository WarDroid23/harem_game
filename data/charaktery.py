# data/charaktery.py
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
}
