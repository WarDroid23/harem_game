# data/drogy.py
DROGY = {
    "modry_lotos": {
        "nazev": "Modrý lotos",
        "popis": "Uklidňuje, zvyšuje touhu a poddajnost.",
        "efekty": {"touha": 15, "submisivita": 10, "strach": -5, "duvera": 5},
        "trvale_nasledky": {"zavislost": 8, "mindbreak": 2, "broken": 1},
        "riziko_predavkovani": 0.02,
        "cena": 30,
        "suroviny": {"bylina_mesicni": 2, "vzacna_houba": 1}
    },
    "serafinsky_prach": {
        "nazev": "Serafínský prach",
        "popis": "Silně omamný, zvyšuje poslušnost a oddanost.",
        "efekty": {"poslusnost": 15, "loajalita": 10, "submisivita": 8},
        "trvale_nasledky": {"zavislost": 12, "broken": 3, "mindbreak": 2},
        "riziko_predavkovani": 0.05,
        "cena": 60,
        "suroviny": {"esence_temna": 2, "krystal_sily": 1}
    },
    "temny_elixir": {
        "nazev": "Temný elixír",
        "popis": "Extrémně návykový, láme vůli.",
        "efekty": {"submisivita": 20, "broken": 10, "mindbreak": 5, "strach": -10},
        "trvale_nasledky": {"zavislost": 20, "broken": 8, "mindbreak": 6, "hp": -10},
        "riziko_predavkovani": 0.10,
        "cena": 120,
        "suroviny": {"esence_temna": 3, "koren_mandragory": 2, "vzacna_houba": 1}
    },
    "ohnivy_prasek": {
        "nazev": "Ohnivý prášek",
        "popis": "Zvyšuje energii a agresivitu, ale ničí zdraví.",
        "efekty": {"touha": 10, "vlhkost": 15, "submisivita": 5, "hp": -5},
        "trvale_nasledky": {"zavislost": 10, "scarred": 3, "hp": -5},
        "riziko_predavkovani": 0.04,
        "cena": 50,
        "suroviny": {"krystal_sily": 2, "bylina_mesicni": 2}
    },
    "zlaty_nektar": {
        "nazev": "Zlatý nektar",
        "popis": "Luxusní droga, zvyšuje touhu a oddanost, mírně návyková.",
        "efekty": {"touha": 15, "loajalita": 8, "duvera": 5},
        "trvale_nasledky": {"zavislost": 5},
        "riziko_predavkovani": 0.01,
        "cena": 80,
        "suroviny": {"bylina_mesicni": 2, "vzacna_houba": 2, "esence_temna": 1}
    },
    "stinovy_extrakt": {
        "nazev": "Stínový extrakt",
        "popis": "Vyvolává halucinace, zvyšuje strach a poddajnost.",
        "efekty": {"strach": 15, "submisivita": 15, "broken": 5, "mindbreak": 5},
        "trvale_nasledky": {"zavislost": 15, "mindbreak": 8, "broken": 5},
        "riziko_predavkovani": 0.08,
        "cena": 100,
        "suroviny": {"esence_temna": 2, "koren_mandragory": 2}
    },
    "krvava_sul": {
        "nazev": "Krvavá sůl",
        "popis": "Brutální droga, zvyšuje odolnost bolesti, ale silně ničí zdraví.",
        "efekty": {"pain_addiction": 20, "tolerance_bolesti": 15, "scarred": 5, "hp": -15},
        "trvale_nasledky": {"zavislost": 18, "scarred": 8, "hp": -10},
        "riziko_predavkovani": 0.12,
        "cena": 150,
        "suroviny": {"krystal_sily": 3, "esence_temna": 2, "vzacna_houba": 2}
    },
    "aurora_pryskyric": {
        "nazev": "Aurora pryskyřice",
        "popis": "Zářící tekutina, zvyšuje max temnou energii a regeneruje zdraví.",
        "efekty": {"dark_energy": 5, "hp": 15, "touha": 10},
        "trvale_nasledky": {"zavislost": 6, "duvera": 4},
        "riziko_predavkovani": 0.02,
        "cena": 90,
        "suroviny": {"krystal_sily": 1, "bylina_mesicni": 2}
    },
    "snova_mlha": {
        "nazev": "Snová mlha",
        "popis": "Halucinogenní kadidlo, navozuje euforii a naprostou odevzdanost.",
        "efekty": {"submisivita": 25, "strach": -15, "poslusnost": 10},
        "trvale_nasledky": {"zavislost": 14, "mindbreak": 4},
        "riziko_predavkovani": 0.04,
        "cena": 110,
        "suroviny": {"vzacna_houba": 2, "esence_temna": 1}
    },
    "demonska_extaze": {
        "nazev": "Extáze démona",
        "popis": "Extrémně silné afrodiziakum podněcující divokou touhu.",
        "efekty": {"touha": 40, "vlhkost": 30, "submisivita": 10, "hp": -5},
        "trvale_nasledky": {"zavislost": 22, "broken": 5},
        "riziko_predavkovani": 0.08,
        "cena": 140,
        "suroviny": {"esence_temna": 3, "krystal_sily": 2}
    },
    "draci_krev": {
        "nazev": "Dračí krev",
        "popis": "Vzácný alchymistický extrakt propůjčující nadlidskou odolnost a sílu.",
        "efekty": {"tolerance_bolesti": 25, "hp": 20, "loajalita": 10},
        "trvale_nasledky": {"zavislost": 10, "scarred": 4},
        "riziko_predavkovani": 0.03,
        "cena": 180,
        "suroviny": {"krystal_sily": 4, "koren_mandragory": 2}
    },
}
