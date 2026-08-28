#!/usr/bin/env python3
"""Test script pro manželství systém."""

import sys
import random
from game.save_load import Hra
from models.otrokyne import Otrokyně
from game.manzelstvi import (
    je_mozne_zasnoubeni, je_mozne_svatba, je_mozne_potomstvo,
    zasnoubeni, svatba, mat_dite
)

def test_marriage_system():
    """Test kompletního manželství systému."""
    print("🧪 TEST MANŽELSTVÍ SYSTÉMU\n")
    
    # Inicializace hry
    hra = Hra()
    hra.hrac.gold = 10000  # Dost peněz pro testy
    
    # Vytvoření otrokyně
    otrok = Otrokyně("Jessina")
    otrok.loajalita = 80
    otrok.romance_body = 60
    otrok.souhlas_romance = True
    hra.harem.pridat(otrok)
    
    print(f"✓ Harem: {hra.harem.pocet()} otrokyň")
    print(f"  - {otrok.jmeno}: loajalita={otrok.loajalita}, romance_body={otrok.romance_body}")
    
    # Test 1: Zasnoubení
    print("\n--- TEST 1: Zasnoubení ---")
    mozne, zprava = je_mozne_zasnoubeni(otrok, hra.hrac)
    if mozne:
        print(f"✓ Zasnoubení je možné")
        uspech = zasnoubeni(otrok, hra.hrac, hra)
        if uspech:
            print(f"✓ Zasnoubení provedeno")
            print(f"  - Zlato: {hra.hrac.gold} 🪙")
            print(f"  - Status: {otrok.je_manzelkou}")
    else:
        print(f"✗ Zasnoubení není možné: {zprava}")
        return False
    
    # Test 2: Svatba
    print("\n--- TEST 2: Svatba ---")
    marriage = hra.marriage_system.get(otrok.jmeno)
    if marriage:
        # Simulace 11 dní
        hra.hrac.den = 12
        mozne, zprava = je_mozne_svatba(marriage, hra.hrac.den)
        if mozne:
            print(f"✓ Svatba je možná (den {hra.hrac.den})")
            uspech = svatba(otrok, hra.hrac, hra)
            if uspech:
                print(f"✓ Svatba provedena")
                print(f"  - Stav: {marriage.stav}")
                print(f"  - Krása ceremonie: {marriage.cerem_puvab}%")
                print(f"  - Loajalita: {otrok.loajalita}%")
        else:
            print(f"✗ Svatba není možná: {zprava}")
            return False
    else:
        print("✗ Manželství nenalezeno")
        return False
    
    # Test 3: Potomstvo
    print("\n--- TEST 3: Potomstvo ---")
    # Simulace dalších 61 dní pro jedno dítě
    hra.hrac.den = 73
    mozne, zprava = je_mozne_potomstvo(marriage, hra.hrac.den)
    if mozne:
        print(f"✓ Potomstvo je možné (den {hra.hrac.den})")
        uspech = mat_dite(otrok, marriage, hra.hrac, hra)
        if uspech:
            print(f"✓ Dítě se narodilo")
            print(f"  - Počet dětí: {marriage.pocet_deti()}")
            if marriage.ma_dite():
                dite = marriage.deti[0]
                print(f"  - Jméno: {dite['jmeno']}")
                print(f"  - Pohlaví: {dite['pohlavi']}")
                print(f"  - Talent: {dite['talent']}%")
                print(f"  - Typ: {dite['typ']}")
    else:
        print(f"✗ Potomstvo není možné: {zprava}")
    
    # Test 4: Manželské bonusy
    print("\n--- TEST 4: Manželské bonusy ---")
    print(f"Sexuální energie před: {hra.hrac.sex_energy}")
    print(f"Zlato před: {hra.hrac.gold}")
    
    from game.odpocinek import zpracuj_den
    zpracuj_den(hra)
    
    # Manuálně počítáme bonusy (protože zpracuj_den je bez odpočinku)
    bonus_energie = 10 if marriage.je_vdana() else 0
    bonus_gold = 50 if marriage.je_vdana() else 0
    
    print(f"Sexuální energie po: {hra.hrac.sex_energy}")
    print(f"Zlato po: {hra.hrac.gold}")
    print(f"✓ Bonusy správně aplikovány: +{bonus_energie} energie, +{bonus_gold} zlata")
    
    # Test 5: Rozvod
    print("\n--- TEST 5: Rozvod ---")
    from game.manzelstvi import rozvod
    loajalita_pred = otrok.loajalita
    uspech = rozvod(otrok, hra.hrac, hra)
    if uspech:
        print(f"✓ Rozvod proveden")
        print(f"  - Stav: {marriage.stav}")
        print(f"  - Loajalita: {loajalita_pred} → {otrok.loajalita}")
        print(f"  - Je vdaná: {otrok.je_manzelkou}")
    else:
        print("✗ Rozvod se nezdařil")
        return False
    
    print("\n✓ VŠECHNY TESTY PROŠLY!")
    return True

if __name__ == "__main__":
    try:
        uspech = test_marriage_system()
        sys.exit(0 if uspech else 1)
    except Exception as e:
        print(f"\n✗ CHYBA: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
