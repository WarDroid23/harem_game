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
                 "hp_dmg": (15, 35), "dark_cost": 15, "riziko_smrti": 0.12, "vliv_inkvizice": 9, "reputace_mesta": -7}
}
