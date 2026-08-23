# data/manipulace.py
MANIPULACE = {
    "gaslighting": {"nazev": "Gaslighting", "popis": "Zpochybňování reality",
                    "efekty": {"duvera": -12, "strach": 8, "broken": 6, "mindbreak": 4},
                    "dark_cost": 5, "energie_cost": 0, "base_detect": 0.28, "vliv_inkvizice": 2},
    "isolation": {"nazev": "Izolace", "popis": "Samota a ticho",
                  "efekty": {"strach": 14, "loajalita": 6, "duvera": -8, "broken": 5},
                  "dark_cost": 3, "energie_cost": 0, "base_detect": 0.15, "vliv_inkvizice": 1},
    "love_bombing": {"nazev": "Love bombing", "popis": "Střídání něhy a krutosti",
                     "efekty": {"touha": 10, "loajalita": 8, "duvera": -10, "strach": 7, "broken": 4},
                     "dark_cost": 4, "energie_cost": 8, "base_detect": 0.22, "vliv_inkvizice": 1},
    "conditioning": {"nazev": "Podmiňování", "popis": "Tresty a odměny dokola",
                     "efekty": {"poslusnost": 12, "submisivita": 10, "strach": 6, "broken": 3},
                     "dark_cost": 2, "energie_cost": 5, "base_detect": 0.12, "vliv_inkvizice": 0},
    "humiliation_loop": {"nazev": "Ponižovací smyčka", "popis": "Ničení sebeúcty",
                         "efekty": {"humiliation": 16, "broken": 9, "strach": 8, "duvera": -6},
                         "dark_cost": 6, "energie_cost": 0, "base_detect": 0.20, "vliv_inkvizice": 3},
    "mind_fracture": {"nazev": "Lámání mysli", "popis": "Intenzivní psychický nátlak",
                      "efekty": {"mindbreak": 14, "broken": 12, "strach": 15, "duvera": -15, "poslusnost": 10},
                      "dark_cost": 14, "energie_cost": 10, "base_detect": 0.08, "vliv_inkvizice": 7},
    "identity_erase": {"nazev": "Mazání identity", "popis": "Přepis osobnosti",
                       "efekty": {"mindbreak": 18, "broken": 16, "loajalita": 12, "duvera": -20},
                       "dark_cost": 18, "energie_cost": 15, "base_detect": 0.05, "vliv_inkvizice": 10}
}
