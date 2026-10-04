# config.py
import os
from pathlib import Path


def user_data_dir():
    """Return the per-user application data directory."""
    if os.name == "nt":
        root = Path(
            os.environ.get("APPDATA")
            or Path.home() / "AppData" / "Roaming"
        )
    else:
        root = Path(
            os.environ.get("XDG_DATA_HOME")
            or Path.home() / ".local" / "share"
        )
    return root / "HaremDark"


SAVE_FILE = str(user_data_dir() / "harem_dark_v18_save.json")
SAVE_SCHEMA_VERSION = 1
VERSION = "22.1-dark"

USE_COLORS = True
CURRENT_THEME = "temne_dominium"


class _ColorCode:
    """Dynamický kód – respektuje USE_COLORS i aktivní téma."""

    def __init__(self, name, default_code):
        self.name = name
        self.default = default_code
        self.code = default_code

    def __str__(self):
        return self.code if USE_COLORS else ""

    def __format__(self, spec):
        return str(self)

    def set_code(self, code):
        self.code = code


def set_colors_enabled(enabled):
    global USE_COLORS
    USE_COLORS = bool(enabled)


RED = _ColorCode("RED", "\033[0;31m")
GREEN = _ColorCode("GREEN", "\033[0;32m")
YELLOW = _ColorCode("YELLOW", "\033[0;33m")
BLUE = _ColorCode("BLUE", "\033[0;34m")
MAGENTA = _ColorCode("MAGENTA", "\033[0;35m")
CYAN = _ColorCode("CYAN", "\033[0;36m")
GOLD = _ColorCode("GOLD", "\033[0;33m")
ORANGE = _ColorCode("ORANGE", "\033[38;5;208m")
VIOLET = _ColorCode("VIOLET", "\033[38;5;129m")
WHITE = _ColorCode("WHITE", "\033[0;37m")
GRAY = _ColorCode("GRAY", "\033[0;90m")
BOLD = _ColorCode("BOLD", "\033[1m")
DIM = _ColorCode("DIM", "\033[2m")
NC = _ColorCode("NC", "\033[0m")

_COLOR_MAP = {
    "RED": RED, "GREEN": GREEN, "YELLOW": YELLOW, "BLUE": BLUE,
    "MAGENTA": MAGENTA, "CYAN": CYAN, "GOLD": GOLD, "ORANGE": ORANGE,
    "VIOLET": VIOLET, "WHITE": WHITE, "GRAY": GRAY,
}

THEMES = {
    "temne_dominium": {
        "nazev": "Temné dominium",
        "popis": "Královská temnota s jasným zlatem, ametystem a chladným tyrkysem.",
        "barvy": {
            "RED": "\033[38;5;196m", "GREEN": "\033[38;5;82m", "YELLOW": "\033[38;5;221m",
            "BLUE": "\033[38;5;75m", "MAGENTA": "\033[38;5;177m", "CYAN": "\033[38;5;87m",
            "GOLD": "\033[38;5;220m", "ORANGE": "\033[38;5;208m", "VIOLET": "\033[38;5;141m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;245m",
        },
    },
    "krvavy_tron": {
        "nazev": "Krvavý trůn",
        "popis": "Červené a temně zlaté tóny – bolest a luxus.",
        "barvy": {
            "RED": "\033[38;5;196m", "GREEN": "\033[38;5;88m", "YELLOW": "\033[38;5;178m",
            "BLUE": "\033[38;5;52m", "MAGENTA": "\033[38;5;125m", "CYAN": "\033[38;5;95m",
            "GOLD": "\033[38;5;220m", "ORANGE": "\033[38;5;202m", "VIOLET": "\033[38;5;89m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;240m",
        },
    },
    "ledova_panenka": {
        "nazev": "Ledová panenka",
        "popis": "Studené modré a stříbrné – chladná dominance.",
        "barvy": {
            "RED": "\033[38;5;67m", "GREEN": "\033[38;5;73m", "YELLOW": "\033[38;5;159m",
            "BLUE": "\033[38;5;39m", "MAGENTA": "\033[38;5;105m", "CYAN": "\033[38;5;51m",
            "GOLD": "\033[38;5;159m", "ORANGE": "\033[38;5;111m", "VIOLET": "\033[38;5;63m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;245m",
        },
    },
    "zeleny_had": {
        "nazev": "Zelený had",
        "popis": "Jedovatě zelená a temná – alchymie a drogy.",
        "barvy": {
            "RED": "\033[38;5;160m", "GREEN": "\033[38;5;46m", "YELLOW": "\033[38;5;154m",
            "BLUE": "\033[38;5;28m", "MAGENTA": "\033[38;5;90m", "CYAN": "\033[38;5;43m",
            "GOLD": "\033[38;5;148m", "ORANGE": "\033[38;5;142m", "VIOLET": "\033[38;5;54m",
            "WHITE": "\033[38;5;253m", "GRAY": "\033[38;5;239m",
        },
    },
    "ruzovy_hedvab": {
        "nazev": "Růžové hedvábí",
        "popis": "Jemná růžová a fialová – erotika a péče.",
        "barvy": {
            "RED": "\033[38;5;205m", "GREEN": "\033[38;5;176m", "YELLOW": "\033[38;5;218m",
            "BLUE": "\033[38;5;147m", "MAGENTA": "\033[38;5;213m", "CYAN": "\033[38;5;182m",
            "GOLD": "\033[38;5;223m", "ORANGE": "\033[38;5;209m", "VIOLET": "\033[38;5;177m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;246m",
        },
    },
    "monochrom": {
        "nazev": "Monochrom",
        "popis": "Černobílá elegance – bez rušivých barev.",
        "barvy": {
            "RED": "\033[38;5;250m", "GREEN": "\033[38;5;252m", "YELLOW": "\033[38;5;255m",
            "BLUE": "\033[38;5;245m", "MAGENTA": "\033[38;5;248m", "CYAN": "\033[38;5;251m",
            "GOLD": "\033[38;5;255m", "ORANGE": "\033[38;5;249m", "VIOLET": "\033[38;5;247m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;240m",
        },
    },
    "azurovy_kristal": {
        "nazev": "Azurový krystal",
        "popis": "Jasná tyrkysová a safírová se stříbrnými akcenty.",
        "barvy": {
            "RED": "\033[38;5;203m", "GREEN": "\033[38;5;48m", "YELLOW": "\033[38;5;159m",
            "BLUE": "\033[38;5;33m", "MAGENTA": "\033[38;5;117m", "CYAN": "\033[38;5;51m",
            "GOLD": "\033[38;5;153m", "ORANGE": "\033[38;5;45m", "VIOLET": "\033[38;5;75m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;245m",
        },
    },
    "smaragdovy_dvur": {
        "nazev": "Smaragdový dvůr",
        "popis": "Smaragdové, jadeitové a teplé zlaté odstíny.",
        "barvy": {
            "RED": "\033[38;5;203m", "GREEN": "\033[38;5;48m", "YELLOW": "\033[38;5;220m",
            "BLUE": "\033[38;5;31m", "MAGENTA": "\033[38;5;114m", "CYAN": "\033[38;5;86m",
            "GOLD": "\033[38;5;220m", "ORANGE": "\033[38;5;172m", "VIOLET": "\033[38;5;115m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;244m",
        },
    },
    "jantarovy_pokoj": {
        "nazev": "Jantarový pokoj",
        "popis": "Hřejivá jantarová a měděná s hlubokou vínovou.",
        "barvy": {
            "RED": "\033[38;5;167m", "GREEN": "\033[38;5;114m", "YELLOW": "\033[38;5;221m",
            "BLUE": "\033[38;5;109m", "MAGENTA": "\033[38;5;175m", "CYAN": "\033[38;5;116m",
            "GOLD": "\033[38;5;220m", "ORANGE": "\033[38;5;214m", "VIOLET": "\033[38;5;139m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;245m",
        },
    },
    "pulnocni_nebe": {
        "nazev": "Půlnoční nebe",
        "popis": "Indigová, noční modř a zářivé hvězdné akcenty.",
        "barvy": {
            "RED": "\033[38;5;203m", "GREEN": "\033[38;5;80m", "YELLOW": "\033[38;5;229m",
            "BLUE": "\033[38;5;63m", "MAGENTA": "\033[38;5;141m", "CYAN": "\033[38;5;117m",
            "GOLD": "\033[38;5;220m", "ORANGE": "\033[38;5;215m", "VIOLET": "\033[38;5;135m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;243m",
        },
    },
    "ohnivy_fenix": {
        "nazev": "Ohnivý fénix",
        "popis": "Zářivé ohnivé odstíny, měď a žhavá červeň.",
        "barvy": {
            "RED": "\033[38;5;196m", "GREEN": "\033[38;5;142m", "YELLOW": "\033[38;5;226m",
            "BLUE": "\033[38;5;67m", "MAGENTA": "\033[38;5;199m", "CYAN": "\033[38;5;180m",
            "GOLD": "\033[38;5;220m", "ORANGE": "\033[38;5;208m", "VIOLET": "\033[38;5;163m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;245m",
        },
    },
    "lesni_duch": {
        "nazev": "Lesní duch",
        "popis": "Mechová zeleň, listové tóny a měsíční stříbro.",
        "barvy": {
            "RED": "\033[38;5;167m", "GREEN": "\033[38;5;71m", "YELLOW": "\033[38;5;150m",
            "BLUE": "\033[38;5;67m", "MAGENTA": "\033[38;5;108m", "CYAN": "\033[38;5;115m",
            "GOLD": "\033[38;5;186m", "ORANGE": "\033[38;5;143m", "VIOLET": "\033[38;5;109m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;245m",
        },
    },
    "neonova_metropole": {
        "nazev": "Neonová metropole",
        "popis": "Elektrická tyrkysová, neonová růžová a digitální modř.",
        "barvy": {
            "RED": "\033[38;5;201m", "GREEN": "\033[38;5;46m", "YELLOW": "\033[38;5;226m",
            "BLUE": "\033[38;5;39m", "MAGENTA": "\033[38;5;198m", "CYAN": "\033[38;5;51m",
            "GOLD": "\033[38;5;220m", "ORANGE": "\033[38;5;208m", "VIOLET": "\033[38;5;165m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;244m",
        },
    },
    "rubinova_arcana": {
        "nazev": "Rubinová arcana",
        "popis": "Vínové červeň, jantar a bohaté královské purpurové tóny.",
        "barvy": {
            "RED": "\033[38;5;124m", "GREEN": "\033[38;5;94m", "YELLOW": "\033[38;5;214m",
            "BLUE": "\033[38;5;53m", "MAGENTA": "\033[38;5;126m", "CYAN": "\033[38;5;130m",
            "GOLD": "\033[38;5;208m", "ORANGE": "\033[38;5;166m", "VIOLET": "\033[38;5;90m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;240m",
        },
    },
    "safirova_noc": {
        "nazev": "Safírová noc",
        "popis": "Těžké modré a tyrkysové tóny až po noční královské černomodro.",
        "barvy": {
            "RED": "\033[38;5;131m", "GREEN": "\033[38;5;75m", "YELLOW": "\033[38;5;153m",
            "BLUE": "\033[38;5;21m", "MAGENTA": "\033[38;5;129m", "CYAN": "\033[38;5;45m",
            "GOLD": "\033[38;5;117m", "ORANGE": "\033[38;5;87m", "VIOLET": "\033[38;5;57m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;238m",
        },
    },
    "zlaty_renesance": {
        "nazev": "Zlatý renesance",
        "popis": "Přepychové zlato, mahagon a teplé měděné akcenty.",
        "barvy": {
            "RED": "\033[38;5;130m", "GREEN": "\033[38;5;100m", "YELLOW": "\033[38;5;220m",
            "BLUE": "\033[38;5;94m", "MAGENTA": "\033[38;5;178m", "CYAN": "\033[38;5;179m",
            "GOLD": "\033[38;5;226m", "ORANGE": "\033[38;5;172m", "VIOLET": "\033[38;5;138m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;244m",
        },
    },
    "emeraldni_louka": {
        "nazev": "Emeraldní louka",
        "popis": "Jadeitová zeleň a svěží zlato, jako výhřev v trávě a krvi.",
        "barvy": {
            "RED": "\033[38;5;167m", "GREEN": "\033[38;5;28m", "YELLOW": "\033[38;5;148m",
            "BLUE": "\033[38;5;35m", "MAGENTA": "\033[38;5;113m", "CYAN": "\033[38;5;84m",
            "GOLD": "\033[38;5;186m", "ORANGE": "\033[38;5;154m", "VIOLET": "\033[38;5;101m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;245m",
        },
    },
    "purpurova_inkvizice": {
        "nazev": "Purpurová inkvizice",
        "popis": "Náboženská purpura, stínová červeň a nepředstavitelně hluboká modř.",
        "barvy": {
            "RED": "\033[38;5;162m", "GREEN": "\033[38;5;54m", "YELLOW": "\033[38;5;136m",
            "BLUE": "\033[38;5;60m", "MAGENTA": "\033[38;5;129m", "CYAN": "\033[38;5;93m",
            "GOLD": "\033[38;5;173m", "ORANGE": "\033[38;5;132m", "VIOLET": "\033[38;5;98m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;241m",
        },
    },
    "satinova_pavouci": {
        "nazev": "Satínová pavoučí",
        "popis": "Měkké černé a broskvové odstíny pro luxusní stínový styl.",
        "barvy": {
            "RED": "\033[38;5;216m", "GREEN": "\033[38;5;96m", "YELLOW": "\033[38;5;223m",
            "BLUE": "\033[38;5;59m", "MAGENTA": "\033[38;5;181m", "CYAN": "\033[38;5;138m",
            "GOLD": "\033[38;5;216m", "ORANGE": "\033[38;5;180m", "VIOLET": "\033[38;5;104m",
            "WHITE": "\033[38;5;255m", "GRAY": "\033[38;5;239m",
        },
    },
}


def apply_theme(theme_id):
    global CURRENT_THEME
    if theme_id not in THEMES:
        theme_id = "temne_dominium"
    CURRENT_THEME = theme_id
    palette = THEMES[theme_id]["barvy"]
    for name, code in palette.items():
        if name in _COLOR_MAP:
            _COLOR_MAP[name].set_code(code)
    return THEMES[theme_id]["nazev"]


def theme_list():
    return list(THEMES.items())
