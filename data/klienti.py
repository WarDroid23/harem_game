# data/klienti.py
KLIENTI = {
    "kupec": {"jmeno": "Bohatý kupec", "popis": "Platí dobře.", "typ": "bezny", "multi": 1.3,
              "preferuje": ["poslusnost", "loajalita"], "riziko": 0.07,
              "efekty": {"humiliation": 3, "loajalita": 2}},
    "sadista": {"jmeno": "Sadistický lord", "popis": "Miluje bolest.", "typ": "temny", "multi": 2.1,
                "preferuje": ["pain_addiction", "submisivita"], "riziko": 0.22,
                "efekty": {"pain_addiction": 12, "scarred": 8, "broken": 6, "hp": -12}},
    "vojaci": {"jmeno": "Skupina vojáků", "popis": "Hrubí a bezohlední.", "typ": "temny", "multi": 1.9,
               "preferuje": ["humiliation", "submisivita"], "riziko": 0.18,
               "efekty": {"humiliation": 18, "broken": 5}},
    "kultista": {"jmeno": "Temný kultista", "popis": "Rituály a zlomená mysl.", "typ": "extremni", "multi": 2.8,
                 "preferuje": ["broken", "mindbreak"], "riziko": 0.30,
                 "efekty": {"mindbreak": 14, "broken": 10}},
    "inkvizitor": {"jmeno": "Inkvizitor", "popis": "Nebezpečný.", "typ": "temny", "multi": 1.6,
                   "preferuje": ["strach", "poslusnost"], "riziko": 0.15,
                   "efekty": {"strach": 15, "broken": 4}, "frakce_efekt": ("cirkev", -8)},
    "otrokar": {"jmeno": "Otrokář z jihu", "popis": "Nejdrsnější.", "typ": "extremni", "multi": 3.5,
                "preferuje": ["broken", "pain_addiction"], "riziko": 0.35,
                "efekty": {"broken": 18, "scarred": 12, "hp": -20}},
    "slechtic": {"jmeno": "Anonymní šlechtic", "popis": "Diskrétní.", "typ": "bezny", "multi": 1.5,
                 "preferuje": ["duvera", "loajalita"], "riziko": 0.06,
                 "efekty": {"loajalita": 4, "duvera": 3}}
}

AUKCNI_DOBA = {"kratka": (2, 3), "stredni": (4, 5), "dlouha": (6, 8)}
