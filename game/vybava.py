from models.equipment import EQUIPMENT
from utils.vypis import clear, tisk_chyba, tisk_ok


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
        print("--- Výbava hráče a týmu ---")
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
        print("K) koupit | T) přiřadit poslední kus člence týmu | 0) Zpět")
        volba = input("> ").strip().lower()
        if volba == "0":
            return
        if volba == "k":
            ident = input("ID výbavy: ").strip().lower()
            tisk_ok("Výbava zakoupena.") if kup_vybavu(hra, ident) else tisk_chyba("Nedostatek zlata nebo neznámá výbava.")
        elif volba == "t":
            ident = input("ID výbavy: ").strip().lower()
            jmeno = input("Jméno člena týmu: ").strip()
            tisk_ok("Výbava přiřazena.") if prirad_tymu(hra, ident, jmeno) else tisk_chyba("Výbavu nelze přiřadit.")
        else:
            tisk_chyba("Neplatná volba.")
        input("Enter...")
