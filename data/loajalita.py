# data/loajalita.py
# Systém loajality otrokyň – stupně, tituly, efekty

STUPNE_LOAJALITY = [
    {
        "id": "vzpoura",
        "min": 0,
        "max": 14,
        "titul": "Vzbouřenkyně",
        "popis": "Otevřeně vzdoruje. Riziko útěku vysoké. Tresty jsou nutnost.",
        "mod_utek": 1.8,
        "mod_odmena": 0.6,
        "mod_trest": 1.3,
        "barva": "RED",
    },
    {
        "id": "neduvera",
        "min": 15,
        "max": 29,
        "titul": "Nedůvěřivá",
        "popis": "Poslouchá jen ze strachu. Loajalita se buduje pomalu.",
        "mod_utek": 1.3,
        "mod_odmena": 0.8,
        "mod_trest": 1.15,
        "barva": "ORANGE",
    },
    {
        "id": "opatrna",
        "min": 30,
        "max": 49,
        "titul": "Opatrná služka",
        "popis": "Plní příkazy, ale bez nadšení. Čeká, co přijde.",
        "mod_utek": 1.0,
        "mod_odmena": 1.0,
        "mod_trest": 1.0,
        "barva": "YELLOW",
    },
    {
        "id": "oddaná",
        "min": 50,
        "max": 69,
        "titul": "Oddaná",
        "popis": "Začíná ti věřit. Odměny mají silnější účinek.",
        "mod_utek": 0.6,
        "mod_odmena": 1.15,
        "mod_trest": 0.95,
        "barva": "CYAN",
    },
    {
        "id": "verna",
        "min": 70,
        "max": 84,
        "titul": "Věrná otrokyně",
        "popis": "Tvé jméno ji drží. Útěk je nepravděpodobný.",
        "mod_utek": 0.25,
        "mod_odmena": 1.25,
        "mod_trest": 0.85,
        "barva": "GREEN",
    },
    {
        "id": "zasvecena",
        "min": 85,
        "max": 94,
        "titul": "Zasvěcená",
        "popis": "Téměř bez vlastní vůle ve tvé prospěch. Hluboká oddanost.",
        "mod_utek": 0.05,
        "mod_odmena": 1.35,
        "mod_trest": 0.75,
        "barva": "MAGENTA",
    },
    {
        "id": "absolutni",
        "min": 95,
        "max": 100,
        "titul": "Absolutní majetek",
        "popis": "Neexistuje bez tebe. Útěk = 0. Odměny i tresty ji jen utvrzují.",
        "mod_utek": 0.0,
        "mod_odmena": 1.5,
        "mod_trest": 0.7,
        "barva": "GOLD",
    },
]


def stupen_loajality(loajalita):
    try:
        val = max(0, min(100, int(loajalita)))
    except (TypeError, ValueError):
        val = 0
    for st in STUPNE_LOAJALITY:
        if st["min"] <= val <= st["max"]:
            return st
    return STUPNE_LOAJALITY[0]


def titul_loajality(loajalita):
    return stupen_loajality(loajalita)["titul"]


def popis_loajality(loajalita):
    st = stupen_loajality(loajalita)
    return f"{st['titul']} ({loajalita}%) – {st['popis']}"


def modifikator_odmeny(loajalita):
    return stupen_loajality(loajalita)["mod_odmena"]


def modifikator_trestu(loajalita):
    return stupen_loajality(loajalita)["mod_trest"]


def sance_uteku_mod(loajalita):
    return stupen_loajality(loajalita)["mod_utek"]
