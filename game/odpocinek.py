# game/odpocinek.py
from utils.vypis import clear, tisk_ok, tisk_chyba
from config import GREEN, CYAN, MAGENTA, NC

def odpocinek(hra):
    hrac = hra.hrac
    clear()
    print(f"{GREEN}--- Odpočinek ---{NC}\n")

    hrac.den += 1
    hrac.sex_energy = min(100, hrac.sex_energy + 30)
    hrac.dark_energy = min(100, hrac.dark_energy + 10)
    hrac.hp = min(hrac.max_hp, hrac.hp + 20)

    prijem_harem = hra.harem.pasivni_prijem()
    prijem_mafie = hra.mafie.vypocet_prijmu()
    hrac.gold += prijem_harem + prijem_mafie

    tisk_ok(f"Odpočinul sis. Energie: {hrac.sex_energy} (sex) / {hrac.dark_energy} (temno).")
    tisk_ok(f"Pasivní příjem: {prijem_harem + prijem_mafie} zlaťáků.")
    input("Enter...")
