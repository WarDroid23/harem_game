# data/odmeny.py
ODMENY = {
    "drobna": {"nazev": "Drobná náklonnost", "popis": "Pohladění, pochválení",
               "efekty": {"loajalita": 5, "duvera": 4, "touha": 3, "strach": -3},
               "cena_gold": 0, "cena_energie": 0, "vliv_inkvizice": 0},
    "dar": {"nazev": "Dárek", "popis": "Šperk, luxus",
            "efekty": {"loajalita": 9, "duvera": 7, "srdce": 6, "touha": 5, "strach": -5},
            "cena_gold": 40, "cena_energie": 0, "vliv_inkvizice": -1},
    "privilegium": {"nazev": "Privilegium", "popis": "Spánek v posteli, zvláštní pozornost",
                    "efekty": {"loajalita": 14, "duvera": 12, "srdce": 10, "touha": 8, "strach": -8},
                    "cena_gold": 0, "cena_energie": 12, "vliv_inkvizice": -2},
    "vzacna": {"nazev": "Vzácná odměna", "popis": "Celá noc jen pro ni + uznání",
               "efekty": {"loajalita": 20, "duvera": 16, "srdce": 14, "touha": 12, "strach": -12, "submisivita": 6},
               "cena_gold": 80, "cena_energie": 20, "vliv_inkvizice": -4}
}
