# game/udalosti.py
import random
from utils.vypis import tisk_ok, tisk_chyba, tisk_info
from models.otrokyne import Otrokyně
from data.jmena import JMENA

def spust_nahodnou_udalost(hra):
    if random.random() > 0.3:
        return

    udalosti = [
        {
            "nazev": "Přepadení harému",
            "popis": "Skupina banditů zaútočila na harém.",
            "efekt": lambda h: prepadeni(h)
        },
        {
            "nazev": "Nemoc otrokyně",
            "popis": "Jedna z otrokyň vážně onemocněla.",
            "efekt": lambda h: nemoc(h)
        },
        {
            "nazev": "Vzpoura otrokyň",
            "popis": "Otrokyně se pokusily o vzpouru.",
            "efekt": lambda h: vzpoura(h)
        },
        {
            "nazev": "Inkvizice je blízko",
            "popis": "Inkvizice zesílila hlídky.",
            "efekt": lambda h: inkvizice(h)
        },
        {
            "nazev": "Obchodní příležitost",
            "popis": "Bohatý kupec chce koupit otrokyni.",
            "efekt": lambda h: kupec(h)
        },
        {
            "nazev": "Setkání s NPC",
            "popis": "Na cestě tě oslovila neznámá postava.",
            "efekt": lambda h: setkani_npc(h)
        },
        {
            "nazev": "Večer světel",
            "popis": "Skleněná zahrada se rozzářila lucernami; Lyra zve k upřímnému rozhovoru.",
            "efekt": lambda h: vecer_svetel(h)
        },
        {
            "nazev": "Signál z věže",
            "popis": "Observatoř vyslala varovný záblesk. Někdo se blíží k hvězdné bráně.",
            "efekt": lambda h: signal_z_veze(h)
        },
    ]

    udalost = random.choice(udalosti)
    print(f"\n{udalost['nazev']}: {udalost['popis']}")
    udalost["efekt"](hra)

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
        hrac.dark_energy = min(100, hrac.dark_energy + 15)
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
        hra.hrac.sex_energy = min(100, hra.hrac.sex_energy + 15)
        hra.hrac.reputace_mesta += 1
        tisk_ok("Večer posílil důvěru. Sexuální energie +15, vztah s Lyrou +8.")
    else:
        tisk_info("Nechal jsi Lyře prostor. Její hranice zůstaly nedotčené.")


def signal_z_veze(hra):
    if hra.svet.aktualni_lokace != "observator":
        tisk_info("Záblesk z věže zahlédneš jen z dálky.")
        return
    hra.svet.zmen_vztah("cassian", 5)
    hra.hrac.dark_energy = min(100, hra.hrac.dark_energy + 12)
    if "strazce_hvezdne_brany" not in hra.kampan.boss_porazeni:
        tisk_info("Cassian tě varoval: Strážce hvězdné brány je vzhůru. Temná energie +12.")
    else:
        tisk_ok("Cassian potvrdil, že věž je bezpečná. Temná energie +12.")
