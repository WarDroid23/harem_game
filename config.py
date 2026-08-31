# config.py
SAVE_FILE = "harem_dark_v18_save.json"
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
        "popis": "Klasická temná fialovo-zlatá paleta.",
        "barvy": {
            "RED": "\033[0;31m", "GREEN": "\033[0;32m", "YELLOW": "\033[0;33m",
            "BLUE": "\033[0;34m", "MAGENTA": "\033[0;35m", "CYAN": "\033[0;36m",
            "GOLD": "\033[0;33m", "ORANGE": "\033[38;5;208m", "VIOLET": "\033[38;5;129m",
            "WHITE": "\033[0;37m", "GRAY": "\033[0;90m",
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
        "nazev": "Růžový hedváb",
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
