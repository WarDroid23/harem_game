# data/tresty.py
TRESTY = {
    "lehky": {"nazev": "Lehký trest", "popis": "Facka, spoutání, ponižování",
              "efekty": {"strach": 8, "submisivita": 6, "humiliation": 5}, "hp_dmg": (0, 3),
              "dark_cost": 0, "riziko_smrti": 0.0, "vliv_inkvizice": 0, "reputace_mesta": 0},
    "stredni": {"nazev": "Střední trest", "popis": "Výprask, veřejné ponížení",
                "efekty": {"strach": 14, "submisivita": 12, "humiliation": 12, "pain_addiction": 6, "broken": 3},
                "hp_dmg": (3, 8), "dark_cost": 3, "riziko_smrti": 0.01, "vliv_inkvizice": 1, "reputace_mesta": -1},
    "tvrdy": {"nazev": "Tvrdý trest", "popis": "Bičování, izolace, značení",
              "efekty": {"strach": 20, "submisivita": 18, "humiliation": 16, "pain_addiction": 12, "broken": 8, "scarred": 6},
              "hp_dmg": (8, 18), "dark_cost": 8, "riziko_smrti": 0.04, "vliv_inkvizice": 4, "reputace_mesta": -3},
    "extremni": {"nazev": "Extrémní trest", "popis": "Krev, asfyxie, mindbreak prvky",
                 "efekty": {"strach": 28, "submisivita": 22, "humiliation": 20, "pain_addiction": 18, "broken": 15, "scarred": 12, "mindbreak": 8},
                 "hp_dmg": (15, 35), "dark_cost": 15, "riziko_smrti": 0.12, "vliv_inkvizice": 9, "reputace_mesta": -7},
    "solna_komora": {
        "nazev": "Uvěznění v solné cele",
        "popis": "Tmavá kamenná kobka posypaná solí. Dny samotky zlomí i nejpyšnější vzdor.",
        "efekty": {"strach": 18, "submisivita": 25, "poslusnost": 20, "broken": 10},
        "hp_dmg": (2, 6), "dark_cost": 5, "riziko_smrti": 0.0, "vliv_inkvizice": 0, "reputace_mesta": 0
    },
    "verejny_pranyr": {
        "nazev": "Veřejný pranýř na trhu",
        "popis": "Připoutána v poutech před davem na Starém trhu. Hluboké pokoření a ztráta cti.",
        "efekty": {"strach": 16, "humiliation": 30, "submisivita": 18, "poslusnost": 15},
        "hp_dmg": (3, 8), "dark_cost": 4, "riziko_smrti": 0.01, "vliv_inkvizice": 3, "reputace_mesta": -4
    },
    "krvave_znackovani": {
        "nazev": "Krvavé rituální značkování",
        "popis": "Vypálení runy dominia rozžhaveným železem přímo do kůže. Věčný znak tvého vlastnictví.",
        "efekty": {"loajalita": 15, "strach": 22, "scarred": 20, "pain_addiction": 15, "submisivita": 20},
        "hp_dmg": (10, 20), "dark_cost": 10, "riziko_smrti": 0.03, "vliv_inkvizice": 2, "reputace_mesta": -2
    },
    "senzoricka_deprivace": {
        "nazev": "Senzorická deprivace a pouta",
        "popis": "Zavázané oči, roubík v ústech a naprosté ticho. Mysl ztrácí pojem o čase i sobě samé.",
        "efekty": {"mindbreak": 14, "submisivita": 22, "broken": 12, "strach": 14, "poslusnost": 18},
        "hp_dmg": (1, 4), "dark_cost": 6, "riziko_smrti": 0.0, "vliv_inkvizice": 0, "reputace_mesta": 0
    },
}
