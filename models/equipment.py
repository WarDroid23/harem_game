"""Výbava hráče a výprav; starší zbraně zůstávají v inventáři odděleně."""

EQUIPMENT = {
    "ocelovy_plat": {
        "nazev": "Ocelový plát",
        "slot": "brneni",
        "cena": 180,
        "bojovy_bonus": 4,
        "expedicni_bonus": 2,
    },
    "pruzkumna_mapa": {
        "nazev": "Průzkumná mapa",
        "slot": "nastroj",
        "cena": 140,
        "bojovy_bonus": 0,
        "expedicni_bonus": 6,
    },
    "znak_spojencu": {
        "nazev": "Znak spojenců",
        "slot": "odznak",
        "cena": 220,
        "bojovy_bonus": 2,
        "expedicni_bonus": 4,
    },
    "stit_haremu": {
        "nazev": "Štít harému",
        "slot": "ochrana",
        "cena": 260,
        "bojovy_bonus": 7,
        "expedicni_bonus": 1,
    },
    "lekarnicka_vypravy": {
        "nazev": "Lékárnička výpravy",
        "slot": "podpora",
        "cena": 160,
        "bojovy_bonus": 1,
        "expedicni_bonus": 5,
    },
}


def seznam_vybavy(inventory, vlastnik="hrac"):
    return [
        EQUIPMENT[item_id]
        for item_id in inventory.vybaveni.get(str(vlastnik), [])
        if item_id in EQUIPMENT
    ]
