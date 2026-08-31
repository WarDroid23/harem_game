# data/odmeny.py
# Dark Expansion – plný systém odměn
# Odměny jsou hierarchické: od drobné náklonnosti až po rituální vlastnictví.
# Některé odměny snižují vliv inkvizice, jiné zvyšují loajalitu a submisivitu zároveň.

ODMENY = {
    # --- Základní odměny ---
    "drobna": {
        "nazev": "Drobná náklonnost",
        "popis": "Pohladění po tváři, tichá pochvala, prst ve vlasech. Malý gest, které jí připomene, že jsi si jí všiml.",
        "efekty": {"loajalita": 5, "duvera": 4, "touha": 3, "strach": -3},
        "cena_gold": 0,
        "cena_energie": 2,
        "vliv_inkvizice": 0,
        "typ": "zakladni"
    },
    "pochvala": {
        "nazev": "Veřejná pochvala",
        "popis": "Před celým harémem řekneš, jak je dobrá. Oči ostatních na ní. Hanba a hrdost se mísí.",
        "efekty": {"loajalita": 8, "duvera": 5, "humiliation": 4, "submisivita": 3},
        "cena_gold": 0,
        "cena_energie": 4,
        "vliv_inkvizice": 0,
        "typ": "zakladni"
    },
    "dar": {
        "nazev": "Dárek",
        "popis": "Šperk, hedvábí, parfém. Něco, co si může dát na tělo a cítit, že patří tobě.",
        "efekty": {"loajalita": 9, "duvera": 7, "srdce": 6, "touha": 5, "strach": -5},
        "cena_gold": 40,
        "cena_energie": 0,
        "vliv_inkvizice": -1,
        "typ": "zakladni"
    },
    "privilegium": {
        "nazev": "Privilegium postele",
        "popis": "Smí spát v tvé posteli. Celou noc cítí tvé tělo vedle sebe. Ráno ji vyhodíš… nebo necháš.",
        "efekty": {"loajalita": 14, "duvera": 12, "srdce": 10, "touha": 8, "strach": -8},
        "cena_gold": 0,
        "cena_energie": 12,
        "vliv_inkvizice": -2,
        "typ": "stredni"
    },
    "vzacna": {
        "nazev": "Vzácná noc",
        "popis": "Celá noc jen pro ni. Žádné jiné otrokyně. Jen ty a ona. A tvé rozkazy.",
        "efekty": {"loajalita": 20, "duvera": 16, "srdce": 14, "touha": 12, "strach": -12, "submisivita": 6},
        "cena_gold": 80,
        "cena_energie": 20,
        "vliv_inkvizice": -4,
        "typ": "vyssi"
    },

    # --- Dark Expansion: erotické a temné odměny ---
    "orální_odměna": {
        "nazev": "Orální privilegium",
        "popis": "Dovolíš jí, aby tě lízala tak dlouho, jak chce. Je to odměna… a zároveň trénink.",
        "efekty": {"touha": 14, "submisivita": 8, "loajalita": 7, "poslusnost": 5},
        "cena_gold": 0,
        "cena_energie": 10,
        "vliv_inkvizice": 0,
        "typ": "eroticka"
    },
    "doteky_pana": {
        "nazev": "Doteky pána",
        "popis": "Pomalu ji prozkoumáváš prsty. Každý dotek je odměna i připomínka, kdo vlastní její tělo.",
        "efekty": {"touha": 12, "vlhkost": 15, "duvera": 6, "submisivita": 5},
        "cena_gold": 0,
        "cena_energie": 8,
        "vliv_inkvizice": 0,
        "typ": "eroticka"
    },
    "povolení_orgasmu": {
        "nazev": "Povolení orgasmu",
        "popis": "Dovolíš jí přijít. Poprvé za dlouhou dobu. Pláče vděčností, když se konečně uvolní.",
        "efekty": {"touha": -15, "loajalita": 12, "duvera": 10, "submisivita": 8, "strach": -6},
        "cena_gold": 0,
        "cena_energie": 6,
        "vliv_inkvizice": 0,
        "typ": "eroticka"
    },
    "spolecna_koupel": {
        "nazev": "Společná koupel",
        "popis": "Myješ ji. Ona tebe. Voda, olej, ticho. Intimita, která bolí víc než bič.",
        "efekty": {"duvera": 14, "srdce": 10, "loajalita": 9, "strach": -10, "touha": 6},
        "cena_gold": 20,
        "cena_energie": 10,
        "vliv_inkvizice": -1,
        "typ": "intimni"
    },
    "znaceni_jemne": {
        "nazev": "Jemné značení",
        "popis": "Malý znak na kůži – ne bolestivý, ale trvalý. Připomínka, že patří tobě. Políbíš místo po sobě.",
        "efekty": {"loajalita": 15, "submisivita": 10, "owned_mark": 1, "duvera": 5, "humiliation": 4},
        "cena_gold": 30,
        "cena_energie": 8,
        "vliv_inkvizice": 1,
        "typ": "vlastnictvi"
    },
    "role_v_haremu": {
        "nazev": "Zvláštní role v harému",
        "popis": "Povýšíš ji – strážkyně, pečovatelka, oblíbenkyně. Ostatní ji začnou respektovat… nebo nenávidět.",
        "efekty": {"loajalita": 18, "duvera": 8, "poslusnost": 6, "srdce": 5},
        "cena_gold": 50,
        "cena_energie": 5,
        "vliv_inkvizice": -2,
        "typ": "status"
    },
    "noc_s_partnerkou": {
        "nazev": "Noc s partnerkou",
        "popis": "Jen pro ty, které jsi přijal jako partnerky. Blízkost, která už není jen službou.",
        "efekty": {"loajalita": 22, "duvera": 18, "srdce": 16, "touha": 10, "romance_body": 8},
        "cena_gold": 0,
        "cena_energie": 18,
        "vliv_inkvizice": -3,
        "typ": "partnerska",
        "vyzaduje_partnerku": True
    },
    "rituali_odměna": {
        "nazev": "Rituální odměna",
        "popis": "Před harémem ji poklekneš, políbíš jí ruku a veřejně prohlásíš, že je tvá. Pak ji vezmeš.",
        "efekty": {"loajalita": 25, "submisivita": 15, "duvera": 12, "humiliation": 8, "poslusnost": 10},
        "cena_gold": 100,
        "cena_energie": 25,
        "vliv_inkvizice": -5,
        "typ": "ritual"
    },
    "elixir_blazenosti": {
        "nazev": "Elixír blaženosti",
        "popis": "Alchymický nápoj. Na pár hodin cítí jen rozkoš a tvoji vůli. Ráno se probudí s prázdnou hlavou a mokrými stehny.",
        "efekty": {"touha": 20, "submisivita": 12, "mindbreak": 3, "vlhkost": 15, "zavislost": 4},
        "cena_gold": 60,
        "cena_energie": 5,
        "vliv_inkvizice": 0,
        "typ": "alchymie"
    },
    "volnost_na_den": {
        "nazev": "Volnost na jeden den",
        "popis": "Jeden den bez příkazů, bez trestu, bez služby. Paradoxně to zvyšuje loajalitu víc než bič.",
        "efekty": {"loajalita": 12, "duvera": 15, "strach": -15, "srdce": 8},
        "cena_gold": 0,
        "cena_energie": 0,
        "vliv_inkvizice": -2,
        "typ": "paradox"
    },
    "spolecne_jidlo": {
        "nazev": "Společné jídlo",
        "popis": "Jí z tvé ruky. Nebo ty z její. Intimita stolu. Oči na sebe.",
        "efekty": {"duvera": 10, "loajalita": 7, "srdce": 6, "strach": -5},
        "cena_gold": 15,
        "cena_energie": 3,
        "vliv_inkvizice": 0,
        "typ": "intimni"
    },
    "tajna_sluzba": {
        "nazev": "Tajná služba",
        "popis": "Necháš ji sloužit ti ve skrytu – v knihovně, v koupelně, pod stolem při poradě. Nikdo jiný to neví.",
        "efekty": {"touha": 10, "submisivita": 9, "loajalita": 8, "humiliation": 5},
        "cena_gold": 0,
        "cena_energie": 12,
        "vliv_inkvizice": 0,
        "typ": "eroticka"
    },
}
