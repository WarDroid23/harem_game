from utils.vypis import clear, vytiskni_volbu


def zobraz_kalendar(hra):
    while True:
        clear()
        kalendar = hra.kalendar
        hlavicka('Kalendář a sezónní události')
        print(f"Den {hra.hrac.den} | týden {kalendar.tyden} | sezóna: {kalendar.sezona}")
        print(kalendar.sezonni_udalost())
        print("\nPoslední události:")
        for udalost in kalendar.udalosti[-8:]:
            print(f"  den {udalost.get('den')}: {udalost.get('udalost')}")
        vytiskni_volbu('0', 'Zpět')
        if input("> ").strip() == "0":
            return
