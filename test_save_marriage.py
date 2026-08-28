#!/usr/bin/env python3
"""Test uložení a načtení manželství."""

import json
import tempfile
from pathlib import Path
from game.save_load import Hra, uloz_hru, nacti_slot
from models.otrokyne import Otrokyně

def test_save_load_marriage():
    """Test uložení a načtení manželství."""
    print("💾 TEST ULOŽENÍ A NAČTENÍ MANŽELSTVÍ\n")
    
    # Vytvoření hry s manželstvím
    print("--- Vytvoření hry ---")
    hra1 = Hra()
    hra1.hrac.gold = 10000
    hra1.hrac.den = 1
    
    # Přidání otrokyně
    otrok = Otrokyně("Isabela")
    otrok.loajalita = 85
    otrok.romance_body = 70
    otrok.souhlas_romance = True
    hra1.harem.pridat(otrok)
    
    # Zasnoubení
    from game.manzelstvi import zasnoubeni, svatba
    zasnoubeni(otrok, hra1.hrac, hra1)
    
    # Svatba
    hra1.hrac.den = 12
    svatba(otrok, hra1.hrac, hra1)
    
    print(f"✓ Hra 1 vytvořena: {len(hra1.marriage_system)} manželství")
    
    # Uložení
    print("\n--- Uložení do JSON ---")
    data = hra1.to_dict()
    print(f"✓ Data konvertována do dict")
    print(f"  - marriage_system klíčů: {len(data.get('marriage_system', {}))}")
    
    if 'marriage_system' in data:
        for jmeno, marriage_data in data['marriage_system'].items():
            print(f"  - Manželství: {jmeno}")
            print(f"    Stav: {marriage_data.get('stav')}")
            print(f"    Den zasnubin: {marriage_data.get('den_zasnubin')}")
    
    # Uložení jako JSON
    json_str = json.dumps(data, indent=2)
    print(f"✓ JSON vytvořen ({len(json_str)} znaků)")
    
    # Načtení z JSON
    print("\n--- Načtení z JSON ---")
    data_loaded = json.loads(json_str)
    hra2 = Hra.from_dict(data_loaded)
    
    print(f"✓ Hra 2 načtena ze souboru")
    print(f"  - Manželství: {len(hra2.marriage_system)}")
    print(f"  - Hráč den: {hra2.hrac.den}")
    
    # Ověření dat
    print("\n--- Ověření dat ---")
    if "Isabela" in hra2.marriage_system:
        marriage = hra2.marriage_system["Isabela"]
        print(f"✓ Manželství Isabely nalezeno")
        print(f"  - Stav: {marriage.stav}")
        print(f"  - Den zasnubin: {marriage.den_zasnubin}")
        print(f"  - Den svatby: {marriage.den_svatby}")
        print(f"  - Krása ceremonie: {marriage.cerem_puvab}%")
        print(f"  - Intimita: {marriage.intimita_level}%")
    else:
        print("✗ Manželství nenalezeno!")
        return False
    
    # Ověření otrokyně
    otrok2 = hra2.harem.vsechny_aktivni()[0]
    print(f"\n✓ Otrokyně Isabela v harému")
    print(f"  - Je vdaná: {otrok2.je_manzelkou}")
    print(f"  - Partner od dne: {otrok2.partner_od_den}")
    print(f"  - Je partnerka: {otrok2.partnerka}")
    print(f"  - Loajalita: {otrok2.loajalita}%")
    
    print("\n✓ ULOŽENÍ A NAČTENÍ FUNGUJE!")
    return True

if __name__ == "__main__":
    import sys
    try:
        uspech = test_save_load_marriage()
        sys.exit(0 if uspech else 1)
    except Exception as e:
        print(f"\n✗ CHYBA: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
