from utils.vypis import hlavicka, clear, vytiskni_volbu


def zobraz_kalendar(hra):
    while True:
        clear()
        kalendar = hra.kalendar
        hlavicka('Kalendář a sezónní události')
        print(f"Den {hra.hrac.den} | týden {kalendar.tyden} | sezóna: {kalendar.sezona}")
        print(kalendar.sezonni_udalost())
        print("\nPoslední události:")
        zaznamy = [
            udalost for udalost in kalendar.udalosti
            if isinstance(udalost, dict)
        ]
        if zaznamy:
            for udalost in zaznamy[-8:]:
                print(f"  den {udalost.get('den', '?')}: {udalost.get('udalost', 'Neznámá událost')}")
        else:
            print("  Zatím se nestala žádná zaznamenaná událost.")
        vytiskni_volbu('0', 'Zpět')
        try:
            if input("> ").strip() == "0":
                return
        except EOFError:
            return
