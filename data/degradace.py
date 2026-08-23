# data/degradace.py
Faze = {
    0: {
        "nazev": "Čistá",
        "popis": "Otrokyně je zatím nedotčená.",
        "bonusy": {},
        "vyzaduje": {"zavislost": 0, "broken": 0, "scarred": 0}
    },
    1: {
        "nazev": "Submisivní služka",
        "popis": "Mírně poddajná, začíná být poslušná.",
        "bonusy": {"poslusnost": 5, "submisivita": 5},
        "vyzaduje": {"zavislost": 15, "broken": 15}
    },
    2: {
        "nazev": "Sub slut",
        "popis": "Sexuálně oddaná, touží po pozornosti.",
        "bonusy": {"touha": 10, "submisivita": 10, "loajalita": 3},
        "vyzaduje": {"zavislost": 30, "broken": 30, "touha": 50}
    },
    3: {
        "nazev": "Sub slutty whore",
        "popis": "Zcela oddaná rozkoši, poslouchá bez odporu.",
        "bonusy": {"touha": 15, "submisivita": 15, "poslusnost": 10, "loajalita": 5},
        "vyzaduje": {"zavislost": 50, "broken": 50, "touha": 70}
    },
    4: {
        "nazev": "Trash slut",
        "popis": "Zcela zničená, dělá cokoliv pro drogu.",
        "bonusy": {"touha": 20, "submisivita": 20, "poslusnost": 15, "loajalita": 8, "humiliation": 10},
        "vyzaduje": {"zavislost": 70, "broken": 70, "touha": 85, "humiliation": 50}
    },
    5: {
        "nazev": "Stepmom",
        "popis": "Starší otrokyně s mateřským instinktem, vhodná pro domácí službu.",
        "bonusy": {"poslusnost": 15, "loajalita": 12, "duvera": 10, "plodnost": 10},
        "vyzaduje": {"vek": 30, "broken": 40, "loajalita": 40}
    },
    6: {
        "nazev": "Stepsister",
        "popis": "Mladá, hravá, ale zkažená otrokyně.",
        "bonusy": {"touha": 15, "vlhkost": 15, "submisivita": 10, "duvera": 5},
        "vyzaduje": {"vek": 18, "broken": 30, "zavislost": 30}
    },
    7: {
        "nazev": "Pregnant teen",
        "popis": "Těhotná mladá otrokyně, snadno zranitelná.",
        "bonusy": {"plodnost": 20, "submisivita": 10, "touha": 10},
        "vyzaduje": {"tehotna": True, "vek": 18, "broken": 50}
    },
    8: {
        "nazev": "Prego mom",
        "popis": "Těhotná matka, ideální chovná otrokyně.",
        "bonusy": {"plodnost": 25, "submisivita": 20, "poslusnost": 15, "loajalita": 10},
        "vyzaduje": {"tehotna": True, "vek": 25, "broken": 60}
    },
    9: {
        "nazev": "Granny",
        "popis": "Starší zkušená otrokyně, loajální a oddaná.",
        "bonusy": {"poslusnost": 20, "loajalita": 15, "duvera": 10},
        "vyzaduje": {"vek": 45, "broken": 50, "loajalita": 60}
    },
    10: {
        "nazev": "Sub slutty whore bitch prego mom",
        "popis": "Naprosto zničená těhotná matka, zcela oddaná.",
        "bonusy": {"touha": 30, "submisivita": 30, "poslusnost": 25, "loajalita": 20, "plodnost": 30},
        "vyzaduje": {"zavislost": 90, "broken": 90, "touha": 95, "tehotna": True, "vek": 20}
    }
}

def ziskat_fazi(otrok):
    """Vrátí aktuální fázi zkaženosti podle vlastností otrokyně."""
    for faze_id in range(10, -1, -1):
        pozadavky = Faze[faze_id]["vyzaduje"]
        splneno = True
        for klic, hodnota in pozadavky.items():
            if klic == "tehotna":
                if otrok.tehotna != hodnota:
                    splneno = False
                    break
            elif klic == "vek":
                if getattr(otrok, 'vek', 0) < hodnota:
                    splneno = False
                    break
            else:
                if getattr(otrok, klic, 0) < hodnota:
                    splneno = False
                    break
        if splneno:
            return faze_id
    return 0

def aplikuj_bonusy(otrok):
    """Aplikuje bonusy fáze zkaženosti na otrokyni (jednorázově)."""
    faze_id = ziskat_fazi(otrok)
    bonusy = Faze[faze_id]["bonusy"]
    for stat, hodnota in bonusy.items():
        otrok.zvysit_stat(stat, hodnota)
    return faze_id
