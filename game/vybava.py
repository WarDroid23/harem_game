from models.equipment import EQUIPMENT
from utils.vypis import (
    hlavicka, clear, nacti_volbu, tisk_chyba, tisk_ok, vytiskni_volbu,
)


def kup_vybavu(hra, vybaveni_id):
    data = EQUIPMENT.get(vybaveni_id)
    if data is None or hra.hrac.gold < data["cena"]:
        return False
    hra.hrac.gold -= data["cena"]
    hra.hrac.inventar.pridej_vybaveni(vybaveni_id)
    return True


def prirad_tymu(hra, vybaveni_id, jmeno):
    if vybaveni_id not in EQUIPMENT:
        return False
    otrok = next((o for o in hra.harem.otrokyne if o.jmeno == jmeno), None)
    if otrok is None or vybaveni_id not in hra.hrac.inventar.vybaveni.get("hrac", []):
        return False
    hra.hrac.inventar.odeber_vybaveni(vybaveni_id)
    if vybaveni_id not in otrok.vybaveni:
        otrok.vybaveni.append(vybaveni_id)
    return True


def menu_vybavy(hra):
    while True:
        clear()
        hlavicka('Výbava hráče a týmu')
        print("Hráč:", ", ".join(
            EQUIPMENT[x]["nazev"] for x in hra.hrac.inventar.vybaveni.get("hrac", [])
            if x in EQUIPMENT
        ) or "žádná")
        for otrok in hra.harem.vsechny_aktivni():
            nazvy = ", ".join(EQUIPMENT[x]["nazev"] for x in otrok.vybaveni if x in EQUIPMENT)
            print(f"{otrok.jmeno}: {nazvy or 'žádná'}")
        print("\nDostupná výbava:")
        for ident, data in EQUIPMENT.items():
            print(f"{ident}) {data['nazev']} — {data['cena']} zlata "
                  f"(výpravy +{data['expedicni_bonus']}, boj +{data['bojovy_bonus']})")
        vytiskni_volbu('K', 'koupit | T) přiřadit poslední kus člence týmu | 0) Zpět')
        try:
            volba = nacti_volbu(
                {"0", "k", "t"},
                chybova_zprava="Neplatná volba. Zadej K, T nebo 0.",
            )
        except EOFError:
            return
        if volba == "0":
            return
        if volba == "k":
            try:
                ident = nacti_volbu(
                    {"0", *EQUIPMENT},
                    prompt="ID výbavy (0 = zpět): ",
                    chybova_zprava="Neznámá výbava.",
                )
            except EOFError:
                return
            if ident == "0":
                continue
            if kup_vybavu(hra, ident):
                tisk_ok("Výbava zakoupena.")
            else:
                tisk_chyba("Nedostatek zlata.")
        elif volba == "t":
            try:
                ident = nacti_volbu(
                    {"0", *EQUIPMENT},
                    prompt="ID výbavy (0 = zpět): ",
                    chybova_zprava="Neznámá výbava.",
                )
            except EOFError:
                return
            if ident == "0":
                continue
            jmena = {}
            for otrok in hra.harem.otrokyne:
                jmena.setdefault(otrok.jmeno.lower(), otrok.jmeno)
            if not jmena:
                tisk_chyba("V týmu není nikdo, komu by šlo výbavu přiřadit.")
                try:
                    input("Enter...")
                except EOFError:
                    return
                continue
            try:
                jmeno = nacti_volbu(
                    {"0", *jmena},
                    prompt="Jméno člena týmu (0 = zpět): ",
                    chybova_zprava="Člen týmu nebyl nalezen.",
                )
            except EOFError:
                return
            if jmeno == "0":
                continue
            if prirad_tymu(hra, ident, jmena[jmeno]):
                tisk_ok("Výbava přiřazena.")
            else:
                tisk_chyba("Výbavu nelze přiřadit.")
        else:
            tisk_chyba("Neplatná volba.")
        try:
            input("Enter...")
        except EOFError:
            return
