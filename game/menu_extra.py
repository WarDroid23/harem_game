# game/menu_extra.py — volby 29–35
from utils.vypis import tisk_info


def obsluz_extra_volbu(volba, hra):
    if volba == "29":
        if getattr(hra, "kronika", None):
            hra.kronika.zobraz()
        else:
            tisk_info("Kronika je prázdná.")
        try:
            input("Enter...")
        except EOFError:
            pass
        return True
    if volba == "30":
        from game.denni_rozkazy import menu_rozkazu
        menu_rozkazu(hra)
        return True
    if volba == "31":
        from game.verejny_vykon import menu_verejneho_vykonu
        menu_verejneho_vykonu(hra)
        return True
    if volba == "32":
        from game.kalendar import zobraz_kalendar
        zobraz_kalendar(hra)
        return True
    if volba == "33":
        hra.mestska_krize.menu(hra)
        return True
    if volba == "34":
        hra.rozsireni_haremu.zobraz_menu(hra)
        return True
    if volba == "35":
        from game.rozsireni import menu_specializace_ctvrti
        menu_specializace_ctvrti(hra)
        return True
    if volba == "36":
        hra.mestske_frakce.menu(hra)
        return True
    return False
