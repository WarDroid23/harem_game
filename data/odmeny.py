# data/odmeny.py
# Dark Expansion – plný systém odměn + fáze, manželka, oblíbenkyně

ODMENY = {
    # --- Základní ---
    "drobna": {
        "nazev": "Drobná náklonnost",
        "popis": "Pohladění po tváři, tichá pochvala, prst ve vlasech.",
        "efekty": {"loajalita": 5, "duvera": 4, "touha": 3, "strach": -3},
        "cena_gold": 0, "cena_energie": 2, "vliv_inkvizice": 0,
        "typ": "zakladni", "min_faze": 0
    },
    "pochvala": {
        "nazev": "Veřejná pochvala",
        "popis": "Před celým harémem řekneš, jak je dobrá. Hanba a hrdost se mísí.",
        "efekty": {"loajalita": 8, "duvera": 5, "humiliation": 4, "submisivita": 3},
        "cena_gold": 0, "cena_energie": 4, "vliv_inkvizice": 0,
        "typ": "zakladni", "min_faze": 0
    },
    "dar": {
        "nazev": "Dárek",
        "popis": "Šperk, hedvábí, parfém. Něco, co si může dát na tělo a cítit, že patří tobě.",
        "efekty": {"loajalita": 9, "duvera": 7, "srdce": 6, "touha": 5, "strach": -5},
        "cena_gold": 40, "cena_energie": 0, "vliv_inkvizice": -1,
        "typ": "zakladni", "min_faze": 0
    },
    "privilegium": {
        "nazev": "Privilegium postele",
        "popis": "Smí spát v tvé posteli. Celou noc cítí tvé tělo vedle sebe.",
        "efekty": {"loajalita": 14, "duvera": 12, "srdce": 10, "touha": 8, "strach": -8},
        "cena_gold": 0, "cena_energie": 12, "vliv_inkvizice": -2,
        "typ": "stredni", "min_faze": 1
    },
    "vzacna": {
        "nazev": "Vzácná noc",
        "popis": "Celá noc jen pro ni. Žádné jiné otrokyně. Jen ty a ona.",
        "efekty": {"loajalita": 20, "duvera": 16, "srdce": 14, "touha": 12, "strach": -12, "submisivita": 6},
        "cena_gold": 80, "cena_energie": 20, "vliv_inkvizice": -4,
        "typ": "vyssi", "min_faze": 2
    },
    "orální_odměna": {
        "nazev": "Orální privilegium",
        "popis": "Dovolíš jí, aby tě lízala tak dlouho, jak chce. Odměna i trénink.",
        "efekty": {"touha": 14, "submisivita": 8, "loajalita": 7, "poslusnost": 5},
        "cena_gold": 0, "cena_energie": 10, "vliv_inkvizice": 0,
        "typ": "eroticka", "min_faze": 1
    },
    "doteky_pana": {
        "nazev": "Doteky pána",
        "popis": "Pomalu ji prozkoumáváš prsty. Každý dotek je odměna i vlastnictví.",
        "efekty": {"touha": 12, "vlhkost": 15, "duvera": 6, "submisivita": 5},
        "cena_gold": 0, "cena_energie": 8, "vliv_inkvizice": 0,
        "typ": "eroticka", "min_faze": 0
    },
    "povolení_orgasmu": {
        "nazev": "Povolení orgasmu",
        "popis": "Dovolíš jí přijít. Pláče vděčností, když se konečně uvolní.",
        "efekty": {"touha": -15, "loajalita": 12, "duvera": 10, "submisivita": 8, "strach": -6},
        "cena_gold": 0, "cena_energie": 6, "vliv_inkvizice": 0,
        "typ": "eroticka", "min_faze": 2
    },
    "spolecna_koupel": {
        "nazev": "Společná koupel",
        "popis": "Myješ ji. Ona tebe. Voda, olej, ticho. Intimita, která bolí víc než bič.",
        "efekty": {"duvera": 14, "srdce": 10, "loajalita": 9, "strach": -10, "touha": 6},
        "cena_gold": 20, "cena_energie": 10, "vliv_inkvizice": -1,
        "typ": "intimni", "min_faze": 1
    },
    "znaceni_jemne": {
        "nazev": "Jemné značení",
        "popis": "Malý znak na kůži. Připomínka, že patří tobě. Políbíš místo po sobě.",
        "efekty": {"loajalita": 15, "submisivita": 10, "owned_mark": 1, "duvera": 5, "humiliation": 4},
        "cena_gold": 30, "cena_energie": 8, "vliv_inkvizice": 1,
        "typ": "vlastnictvi", "min_faze": 3
    },
    "role_v_haremu": {
        "nazev": "Zvláštní role v harému",
        "popis": "Povýšíš ji. Ostatní ji začnou respektovat… nebo nenávidět.",
        "efekty": {"loajalita": 18, "duvera": 8, "poslusnost": 6, "srdce": 5},
        "cena_gold": 50, "cena_energie": 5, "vliv_inkvizice": -2,
        "typ": "status", "min_faze": 2
    },
    "tajna_sluzba": {
        "nazev": "Tajná služba",
        "popis": "Slouží ti ve skrytu – v knihovně, v koupelně, pod stolem. Nikdo jiný to neví.",
        "efekty": {"touha": 10, "submisivita": 9, "loajalita": 8, "humiliation": 5},
        "cena_gold": 0, "cena_energie": 12, "vliv_inkvizice": 0,
        "typ": "eroticka", "min_faze": 1
    },
    "spolecne_jidlo": {
        "nazev": "Společné jídlo",
        "popis": "Jí z tvé ruky. Intimita stolu. Oči na sebe.",
        "efekty": {"duvera": 10, "loajalita": 7, "srdce": 6, "strach": -5},
        "cena_gold": 15, "cena_energie": 3, "vliv_inkvizice": 0,
        "typ": "intimni", "min_faze": 0
    },
    "volnost_na_den": {
        "nazev": "Volnost na jeden den",
        "popis": "Jeden den bez příkazů. Paradoxně to zvyšuje loajalitu víc než bič.",
        "efekty": {"loajalita": 12, "duvera": 15, "strach": -15, "srdce": 8},
        "cena_gold": 0, "cena_energie": 0, "vliv_inkvizice": -2,
        "typ": "paradox", "min_faze": 0
    },
    "elixir_blazenosti": {
        "nazev": "Elixír blaženosti",
        "popis": "Alchymický nápoj. Na pár hodin cítí jen rozkoš a tvoji vůli.",
        "efekty": {"touha": 20, "submisivita": 12, "mindbreak": 3, "vlhkost": 15, "zavislost": 4},
        "cena_gold": 60, "cena_energie": 5, "vliv_inkvizice": 0,
        "typ": "alchymie", "min_faze": 4
    },
    "rituali_odměna": {
        "nazev": "Rituální odměna",
        "popis": "Před harémem ji poklekneš, políbíš jí ruku a veřejně prohlásíš, že je tvá.",
        "efekty": {"loajalita": 25, "submisivita": 15, "duvera": 12, "humiliation": 8, "poslusnost": 10},
        "cena_gold": 100, "cena_energie": 25, "vliv_inkvizice": -5,
        "typ": "ritual", "min_faze": 5
    },
    "noc_s_partnerkou": {
        "nazev": "Noc s partnerkou",
        "popis": "Jen pro partnerky. Blízkost, která už není jen službou.",
        "efekty": {"loajalita": 22, "duvera": 18, "srdce": 16, "touha": 10, "romance_body": 8},
        "cena_gold": 0, "cena_energie": 18, "vliv_inkvizice": -3,
        "typ": "partnerska", "min_faze": 0, "vyzaduje_partnerku": True
    },
    "manzelska_noc": {
        "nazev": "Manželská noc",
        "popis": "Noc vyhrazená jen manželce. Žádné otrokyně – jen ty a ona jako žena.",
        "efekty": {"loajalita": 28, "duvera": 22, "srdce": 20, "touha": 12, "romance_body": 12},
        "cena_gold": 0, "cena_energie": 22, "vliv_inkvizice": -4,
        "typ": "manzelska", "min_faze": 0, "vyzaduje_manzelku": True
    },
    "prsten_a_slib": {
        "nazev": "Prsten a slib",
        "popis": "Obnovíš slib. Políbíš jí prsten a řekneš, že je víc než majetek.",
        "efekty": {"loajalita": 20, "duvera": 18, "srdce": 15, "strach": -10},
        "cena_gold": 120, "cena_energie": 8, "vliv_inkvizice": -3,
        "typ": "manzelska", "min_faze": 0, "vyzaduje_manzelku": True
    },
    "privilegium_oblibene": {
        "nazev": "Privilegium oblíbenkyně",
        "popis": "Speciální péče jen pro tu, kterou jsi označil jako oblíbenou. Ostatní to vidí.",
        "efekty": {"loajalita": 16, "duvera": 12, "touha": 10, "humiliation": 6, "srdce": 8},
        "cena_gold": 25, "cena_energie": 10, "vliv_inkvizice": 0,
        "typ": "oblibena", "min_faze": 0, "vyzaduje_oblibenou": True
    },
    "verejne_povyseni": {
        "nazev": "Veřejné povýšení oblíbenkyně",
        "popis": "Před celým harémem ji prohlásíš za svou oblíbenou. Žárlivost i touha v očích ostatních.",
        "efekty": {"loajalita": 20, "submisivita": 8, "humiliation": 10, "duvera": 6},
        "cena_gold": 40, "cena_energie": 8, "vliv_inkvizice": 1,
        "typ": "oblibena", "min_faze": 2, "vyzaduje_oblibenou": True
    },
}
