# data/charaktery.py
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
}
