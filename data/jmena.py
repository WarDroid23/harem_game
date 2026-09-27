# data/jmena.py
import random


JMENA = [
    "Luna", "Nova", "Vesper", "Nyx", "Lilith", "Sable", "Aria", "Mira", "Zara", "Eva",
    "Ivy", "Rose", "Jade", "Raven", "Willow", "Selene", "Freya", "Morrigan", "Belladonna",
    "Ishtar", "Kali", "Morgana", "Circe", "Astarte", "Hecate", "Lamia", "Medusa",
    "Nephthys", "Sekhmet", "Eris", "Aradia", "Bastet",
    "Cleopatra", "Semiramis", "Zenobia", "Boudica", "Cartimandua",
    "Vlasta", "Kazimíra", "Bohdana", "Drahuše", "Mlada", "Rusalka", "Morana",
    "Vesna", "Živa", "Lada", "Světlana", "Radana", "Doubravka",
    "Seraphina", "Azrael", "Nerissa", "Ondine", "Sylphie", "Ember", "Storm",
    "Frost", "Shadow", "Myst", "Echo", "Siren", "Vixen", "Wren",
    "Mei", "Yuki", "Sakura", "Hana", "Kira", "Miyu", "Rei", "Aiko",
    "Lin", "Xia", "Meiling", "Yuna",
    "Althea", "Calista", "Dahlia", "Elara", "Fiora", "Isolde", "Leona",
    "Maribel", "Nadia", "Ophelia", "Persephone", "Thalia", "Valeria",
    "Aurelia", "Briseis", "Dione", "Elektra", "Gaia", "Helena", "Ione",
    "Juniper", "Kassia", "Lyra", "Maelis", "Niamh", "Orla", "Phoebe",
    "Amálie", "Barbora", "Eliška", "Jitka", "Karolína", "Lenka", "Markéta",
    "Nela", "Radka", "Tereza", "Veronika", "Zdena", "Adéla", "Kristýna",
    "Anastasia", "Beatrix", "Celeste", "Davina", "Elowen", "Genevieve",
    "Imara", "Isadora", "Jessamine", "Lorelei", "Mirabel", "Noelle",
    "Octavia", "Rosalind", "Serena", "Tatiana", "Vivienne", "Yvette",
    "Amina", "Farah", "Inaya", "Layla", "Nour", "Samira", "Zahra",
    "Akari", "Emi", "Kaori", "Natsuki", "Rin", "Tomoe", "Umiko",
]

JMENA.extend([
    "Anežka", "Běla", "Božena", "Cecílie", "Dita", "Ema", "Hedvika", "Ilona",
    "Irena", "Josefína", "Klára", "Lída", "Milada", "Otilie", "Pavla", "Růžena",
    "Šárka", "Zora", "Ayla", "Darya", "Esme", "Ingrid", "Katerina",
    "Mirela", "Nika", "Oksana", "Petra", "Rhea", "Sabina", "Talia", "Varya",
    "Xenia", "Yara", "Zoraida", "Amara", "Briar", "Cleo", "Evelyn", "Isla",
    "Mara", "Nerina", "Sienna", "Tamsin", "Violetta", "Zarina",
])
JMENA[:] = list(dict.fromkeys(JMENA))


def vyber_nove_jmeno(obsazena_jmena=()):
    """Vybere jméno, které ještě nepoužívá žádná postava v seznamu."""
    obsazena = {
        str(getattr(postava, "jmeno", postava)).strip().casefold()
        for postava in obsazena_jmena
    }
    dostupna = [jmeno for jmeno in JMENA if jmeno.casefold() not in obsazena]
    if dostupna:
        return random.choice(dostupna)

    zaklad = random.choice(JMENA)
    cislo = 2
    while f"{zaklad} {cislo}".casefold() in obsazena:
        cislo += 1
    return f"{zaklad} {cislo}"


JMENA_AGENTU = ["Shadow", "Vesper", "Cinder", "Raven", "Silas", "Nyx", "Ash", "Wraith", "Echo"]
