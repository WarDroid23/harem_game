# config.py
SAVE_FILE = "harem_dark_v18_save.json"
VERSION = "21.0"

USE_COLORS = True


class _ColorCode:
    """Dynamický kód, aby nastavení barev platilo i pro již importované moduly."""

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code if USE_COLORS else ""

    def __format__(self, spec):
        return str(self)


def set_colors_enabled(enabled):
    global USE_COLORS
    USE_COLORS = bool(enabled)


RED = _ColorCode('\033[0;31m')
GREEN = _ColorCode('\033[0;32m')
YELLOW = _ColorCode('\033[0;33m')
BLUE = _ColorCode('\033[0;34m')
MAGENTA = _ColorCode('\033[0;35m')
CYAN = _ColorCode('\033[0;36m')
GOLD = _ColorCode('\033[0;33m')
ORANGE = _ColorCode('\033[38;5;208m')
VIOLET = _ColorCode('\033[38;5;129m')
WHITE = _ColorCode('\033[0;37m')
GRAY = _ColorCode('\033[0;90m')
BOLD = _ColorCode('\033[1m')
DIM = _ColorCode('\033[2m')
NC = _ColorCode('\033[0m')
