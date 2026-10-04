# game/udalosti.py
import random
from utils.vypis import tisk_ok, tisk_chyba, tisk_info

def spust_nahodnou_udalost(hra):
    if random.random() > 0.3:
        return

    udalosti = [
        {
            "nazev": "Přepadení harému",
            "popis": "Skupina banditů zaútočila na harém.",
            "efekt": prepadeni,
            "podminka": lambda h: bool(h.harem.vsechny_aktivni()),
            "vaha": lambda h: max(1, 4 - h.mafie.bojova_sila() // 10),
        },
        {
            "nazev": "Nemoc otrokyně",
            "popis": "Jedna z otrokyň vážně onemocněla.",
            "efekt": nemoc,
            "podminka": lambda h: any(
                o.hp > 0 for o in h.harem.vsechny_aktivni()
            ),
            "vaha": lambda h: 1 + sum(
                o.hp < 40 for o in h.harem.vsechny_aktivni()
            ),
        },
        {
            "nazev": "Vzpoura otrokyň",
            "popis": "Otrokyně se pokusily o vzpouru.",
            "efekt": vzpoura,
            "podminka": lambda h: bool(h.harem.vsechny_aktivni()),
            "vaha": lambda h: 1 + sum(
                o.loajalita < 30 for o in h.harem.vsechny_aktivni()
            ),
        },
        {
            "nazev": "Inkvizice je blízko",
            "popis": "Inkvizice zesílila hlídky.",
            "efekt": inkvizice,
            "vaha": lambda h: 1 + h.hrac.vliv_inkvizice // 20,
        },
        {
            "nazev": "Obchodní příležitost",
            "popis": "Bohatý kupec chce koupit otrokyni.",
            "efekt": kupec,
            "podminka": lambda h: bool(h.harem.vsechny_aktivni()),
            "vaha": lambda h: 1 + (h.hrac.gold < 300),
        },
        {
            "nazev": "Setkání s NPC",
            "popis": "Na cestě tě oslovila neznámá postava.",
            "efekt": setkani_npc,
        },
        {
            "nazev": "Večer světel",
            "popis": "Skleněná zahrada se rozzářila lucernami; Lyra zve k upřímnému rozhovoru.",
            "efekt": vecer_svetel,
            "podminka": lambda h: (
                h.svet.aktualni_lokace == "sklenena_zahrada"
            ),
            "vaha": lambda h: 3,
        },
        {
            "nazev": "Signál z věže",
            "popis": "Observatoř vyslala varovný záblesk. Někdo se blíží k hvězdné bráně.",
            "efekt": signal_z_veze,
            "podminka": lambda h: (
                h.svet.aktualni_lokace == "observator"
            ),
            "vaha": lambda h: (
                3 if "strazce_hvezdne_brany" not in h.kampan.boss_porazeni else 1
            ),
        },
        {
            "nazev": "Tichá sklizeň",
            "popis": "Po jarním dešti se objevily vzácné měsíční byliny.",
            "efekt": ticha_sklizen,
            "podminka": lambda h: (
                h.svet.aktualni_lokace == "sklenena_zahrada"
                or h.kalendar.sezona == "jaro"
            ),
            "vaha": lambda h: (
                3 if h.svet.aktualni_lokace == "sklenena_zahrada" else 1
            ),
        },
        {
            "nazev": "Výkupné za posla",
            "popis": "Přístavní cech zadržel tvého posla a požaduje okamžité výkupné.",
            "efekt": vykupne_za_posla,
        },
        {
            "nazev": "Prasklý krystal",
            "popis": "Ve skladišti pevnosti se uvolnila temná esence z poškozeného krystalu.",
            "efekt": praskly_krystal,
            "podminka": lambda h: h.svet.aktualni_lokace == "pevnost",
            "vaha": lambda h: 1 + (h.hrac.dark_energy < h.hrac.max_temno() // 2),
        },
        {
            "nazev": "Tip z městské informační burzy",
            "popis": "Mafiánské kontakty zachytily zprávu o cenných výzkumných záznamech.",
            "efekt": tip_z_informacni_burzy,
            "podminka": lambda h: any(
                u.nazev == "Cechovní uličky" for u in h.mafie.uzemi
            ) or any(
                "informacni_burza" in getattr(u, "podniky", {})
                for u in h.mafie.uzemi
            ),
            "vaha": lambda h: 2,
        },
        {
            "nazev": "Zátah na nelegální podnik",
            "popis": "Městská garda odhalila stopu vedoucí k jednomu z tvých podniků.",
            "efekt": zatah_na_podnik,
            "podminka": lambda h: any(
                getattr(u, "podniky", {}) for u in h.mafie.uzemi
            ),
            "vaha": lambda h: 1 + h.hrac.vliv_inkvizice // 30,
        },
        {
            "nazev": "Výnosná černá tržba",
            "popis": "Síť čtvrtí uzavřela obchod s kupci, kteří se vyhýbají oficiálním cestám.",
            "efekt": cerna_trzba,
            "podminka": lambda h: bool(h.mafie.uzemi),
            "vaha": lambda h: max(1, len(h.mafie.uzemi)),
        },
    ]

    dostupne = [
        udalost for udalost in udalosti
        if udalost.get("podminka", lambda _hra: True)(hra)
    ]
    vaha = [max(1, udalost.get("vaha", lambda _hra: 1)(hra)) for udalost in dostupne]
    udalost = random.choices(dostupne, weights=vaha, k=1)[0]
    print(f"\n{udalost['nazev']}: {udalost['popis']}")
    udalost["efekt"](hra)
    if hasattr(hra, "kalendar"):
        hra.kalendar.udalosti.append({
            "den": hra.hrac.den,
            "udalost": udalost["nazev"],
        })
        hra.kalendar.udalosti = hra.kalendar.udalosti[-30:]

def prepadeni(hra):
    if hra.mafie.bojova_sila() > 20:
        tisk_ok("Tví vojáci odrazili útok.")
    else:
        ztrata = random.randint(10, 50)
        hra.hrac.gold = max(0, hra.hrac.gold - ztrata)
        tisk_chyba(f"Přišel jsi o {ztrata} zlaťáků.")

def nemoc(hra):
    otrokyne = hra.harem.vsechny_aktivni()
    if otrokyne:
        o = random.choice(otrokyne)
        o.hp -= random.randint(10, 30)
        if o.hp < 10:
            o.hp = 0
        tisk_chyba(f"{o.jmeno} je nemocná. HP: {o.hp}")

def vzpoura(hra):
    otrokyne = hra.harem.vsechny_aktivni()
    if otrokyne:
        o = random.choice(otrokyne)
        if o.loajalita < 30:
            if random.random() < 0.5:
                hra.harem.odstranit(o.jmeno)
                tisk_chyba(f"{o.jmeno} utekla!")
            else:
                o.submisivita += 10
                tisk_ok(f"{o.jmeno} byla potrestána a zůstala.")
        else:
            tisk_ok("Otrokyně jsou loajální, vzpoura potlačena.")

def inkvizice(hra):
    hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + random.randint(2, 5))
    tisk_chyba(f"Vliv inkvizice vzrostl na {hra.hrac.vliv_inkvizice}.")

def kupec(hra):
    if hra.harem.vsechny_aktivni():
        o = random.choice(hra.harem.vsechny_aktivni())
        cena = 50 + o.submisivita * 4
        hra.hrac.gold += cena
        hra.harem.odstranit(o.jmeno)
        tisk_ok(f"Prodal jsi {o.jmeno} za {cena} zlaťáků.")

def setkani_npc(hra):
    npc = random.choice([
        {
            "jmeno": "Mira, potulná léčitelka",
            "popis": "Nabízí ošetření za 30 zlaťáků.",
            "akce": "lecitelka",
        },
        {
            "jmeno": "Radan, pašerák",
            "popis": "Prodá ti tajnou zásobu za 40 zlaťáků.",
            "akce": "paserak",
        },
        {
            "jmeno": "Elian, městský informátor",
            "popis": "Za 20 zlaťáků prozradí, co se děje ve městě.",
            "akce": "informator",
        },
    ])

    print(f"\n{npc['jmeno']}: {npc['popis']}")
    volba = input("Přijmout nabídku? (a/n): ").strip().lower()
    if volba not in ("a", "ano"):
        tisk_info("Nabídku jsi odmítl.")
        return

    hrac = hra.hrac
    if npc["akce"] == "lecitelka":
        cena = 30
        if hrac.gold < cena:
            tisk_chyba("Nemáš dost zlata.")
            return
        hrac.gold -= cena
        hrac.hp = min(hrac.max_hp, hrac.hp + 35)
        tisk_ok(f"{npc['jmeno']} tě ošetřila. HP: {hrac.hp}.")
    elif npc["akce"] == "paserak":
        cena = 40
        if hrac.gold < cena:
            tisk_chyba("Nemáš dost zlata.")
            return
        hrac.gold -= cena
        hrac.dark_energy = min(hrac.max_temno(), hrac.dark_energy + 15)
        tisk_ok("Pašerák ti předal zakázanou zásobu. Temná energie +15.")
    else:
        cena = 20
        if hrac.gold < cena:
            tisk_chyba("Nemáš dost zlata.")
            return
        hrac.gold -= cena
        hrac.reputace_mesta += 3
        tisk_ok("Informátor ti předal cenné zprávy. Reputace města +3.")


def vecer_svetel(hra):
    if hra.svet.aktualni_lokace != "sklenena_zahrada":
        tisk_info("Událost se rozplynula dřív, než jsi dorazil do zahrady.")
        return
    print("Lyra: „Můžeme dnes jen sedět a poslouchat. Nemusíme nic dokazovat.“")
    volba = input("Zůstaneš a budeš respektovat její tempo? (a/n): ").strip().lower()
    if volba in ("a", "ano"):
        hra.svet.zmen_vztah("lyra", 8)
        hra.hrac.sex_energy = min(
            hra.hrac.max_sex(), hra.hrac.sex_energy + 15
        )
        hra.hrac.reputace_mesta += 1
        tisk_ok("Večer posílil důvěru. Sexuální energie +15, vztah s Lyrou +8.")
    else:
        tisk_info("Nechal jsi Lyře prostor. Její hranice zůstaly nedotčené.")


def signal_z_veze(hra):
    if hra.svet.aktualni_lokace != "observator":
        tisk_info("Záblesk z věže zahlédneš jen z dálky.")
        return
    hra.svet.zmen_vztah("cassian", 5)
    hra.hrac.dark_energy = min(
        hra.hrac.max_temno(), hra.hrac.dark_energy + 12
    )
    if "strazce_hvezdne_brany" not in hra.kampan.boss_porazeni:
        tisk_info("Cassian tě varoval: Strážce hvězdné brány je vzhůru. Temná energie +12.")
    else:
        tisk_ok("Cassian potvrdil, že věž je bezpečná. Temná energie +12.")


def ticha_sklizen(hra):
    """Malá pozitivní událost, která využívá již existující produkci alchymie."""
    mnozstvi = random.randint(1, 3)
    hra.alchymie.suroviny["bylina_mesicni"] = (
        hra.alchymie.suroviny.get("bylina_mesicni", 0) + mnozstvi
    )
    hra.frakce.frakce["obchodnici"].zmenit(2)
    _zapis_kroniku(hra, f"Tichá sklizeň přinesla {mnozstvi} měsíční byliny.")
    tisk_ok(f"Zahradnice sklidily {mnozstvi}× měsíční bylinu.")


def vykupne_za_posla(hra):
    cena = 75
    if hra.hrac.gold < cena:
        hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + 2)
        tisk_chyba("Nemáš na výkupné. Zpráva se ztratila a inkvizice získala stopu.")
        return
    hra.hrac.gold -= cena
    hra.hrac.reputace_mesta = min(100, hra.hrac.reputace_mesta + 2)
    hra.frakce.frakce["syndikat_stinu"].zmenit(-3)
    _zapis_kroniku(hra, "Výkupné za posla bylo zaplaceno; Syndikát stínů oslabil.")
    tisk_ok(f"Posel je zpět. Zaplatil jsi {cena} zlaťáků; reputace města +2.")


def praskly_krystal(hra):
    zisk = random.randint(8, 16)
    hra.hrac.dark_energy = min(hra.hrac.max_temno(), hra.hrac.dark_energy + zisk)
    hra.hrac.hp = max(1, hra.hrac.hp - 3)
    hra.frakce.frakce["kult_krve"].zmenit(3)
    _zapis_kroniku(hra, f"Prasklý krystal uvolnil {zisk} temné energie.")
    tisk_info(f"Získal jsi {zisk} temné energie, ale výboj tě zranil o 3 HP.")


def tip_z_informacni_burzy(hra):
    body = random.randint(2, 4)
    hra.vyzkum.pridej_body(body)
    hra.frakce.frakce["syndikat_stinu"].zmenit(2)
    _zapis_kroniku(hra, f"Informátor přinesl {body} výzkumné body.")
    tisk_ok(f"Síť informátorů přinesla +{body} výzkumné body.")


def zatah_na_podnik(hra):
    uzemi = random.choice([
        u for u in hra.mafie.uzemi if getattr(u, "podniky", {})
    ])
    ztrata_kontroly = min(max(0, uzemi.kontrola), random.randint(3, 8))
    uzemi.kontrola -= ztrata_kontroly
    hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + 2)
    _zapis_kroniku(
        hra, f"Zátah poškodil podniky ve čtvrti {uzemi.nazev} (kontrola −{ztrata_kontroly} %)."
    )
    tisk_chyba(
        f"Garda udeřila v {uzemi.nazev}. Kontrola území −{ztrata_kontroly} %, "
        f"vliv Inkvizice +2."
    )


def cerna_trzba(hra):
    pocet_podniku = sum(
        len(getattr(u, "podniky", {})) for u in hra.mafie.uzemi
    )
    zisk = 35 + len(hra.mafie.uzemi) * 10 + pocet_podniku * 15
    hra.hrac.gold += zisk
    hra.frakce.frakce["obchodnici"].zmenit(1)
    _zapis_kroniku(hra, f"Černá tržba přinesla {zisk} zlaťáků.")
    tisk_ok(f"Černá tržba z městské sítě: +{zisk} 🪙.")


def _zapis_kroniku(hra, text):
    from game.kronika import zaznamenej
    zaznamenej(hra, text)
