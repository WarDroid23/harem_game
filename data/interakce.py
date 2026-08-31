# data/interakce.py
# Dark Expansion v1.0 – rozšířené interakce

INTERAKCE = [
    {
        "id": "neznost",
        "nazev": "Něžnost",
        "typ": "odmena",
        "efekty": {"touha": 5, "duvera": 3},
        "cena_energie": 5,
        "cena_temnoty": 0,
        "riziko": 0.0
    },
    {
        "id": "masaz",
        "nazev": "Masáž",
        "typ": "odmena",
        "efekty": {"touha": 8, "duvera": 4, "strach": -2},
        "cena_energie": 8,
        "cena_temnoty": 0,
        "riziko": 0.0
    },
    {
        "id": "vyprask",
        "nazev": "Výprask",
        "typ": "trest",
        "efekty": {"submisivita": 8, "strach": 5, "pain_addiction": 2},
        "cena_energie": 10,
        "cena_temnoty": 2,
        "riziko": 0.02
    },
    {
        "id": "svazovani",
        "nazev": "Svazování",
        "typ": "trest",
        "efekty": {"submisivita": 10, "strach": 4, "duvera": -2},
        "cena_energie": 12,
        "cena_temnoty": 3,
        "riziko": 0.03
    },
    {
        "id": "bicovani",
        "nazev": "Bičování",
        "typ": "trest",
        "efekty": {"submisivita": 12, "pain_addiction": 8, "broken": 3, "hp": -5},
        "cena_energie": 15,
        "cena_temnoty": 8,
        "riziko": 0.05
    },
    {
        "id": "forced_orgasm",
        "nazev": "Forced orgasm",
        "typ": "neutralni",
        "efekty": {"touha": -10, "submisivita": 6, "broken": 2},
        "cena_energie": 10,
        "cena_temnoty": 5,
        "riziko": 0.01
    },
    {
        "id": "bic_do_krve",
        "nazev": "Bič do krve",
        "typ": "trest",
        "efekty": {"pain_addiction": 15, "scarred": 5, "broken": 8, "hp": -12},
        "cena_energie": 18,
        "cena_temnoty": 12,
        "riziko": 0.08
    },
    {
        "id": "asfyxie",
        "nazev": "Asfyxie",
        "typ": "trest",
        "efekty": {"strach": 15, "broken": 6, "mindbreak": 3, "hp": -10},
        "cena_energie": 20,
        "cena_temnoty": 10,
        "riziko": 0.06
    },
    {
        "id": "knife_play",
        "nazev": "Knife play",
        "typ": "trest",
        "efekty": {"strach": 18, "submisivita": 10, "scarred": 7, "hp": -8},
        "cena_energie": 16,
        "cena_temnoty": 12,
        "riziko": 0.07
    },
    {
        "id": "smyslova_deprivace",
        "nazev": "Smyslová deprivace",
        "typ": "trest",
        "efekty": {"strach": 10, "submisivita": 8, "broken": 4, "duvera": -3},
        "cena_energie": 10,
        "cena_temnoty": 4,
        "riziko": 0.04
    },
    {
        "id": "teplotni_hra",
        "nazev": "Teplotní hra",
        "typ": "neutralni",
        "efekty": {"touha": 6, "strach": 6, "submisivita": 5, "pain_addiction": 3},
        "cena_energie": 8,
        "cena_temnoty": 5,
        "riziko": 0.03
    },
    {
        "id": "zavazky",
        "nazev": "Závazky",
        "typ": "odmena",
        "efekty": {"submisivita": 10, "duvera": 5, "loajalita": 3},
        "cena_energie": 12,
        "cena_temnoty": 0,
        "riziko": 0.02
    },
    {
        "id": "verejne_ponizeni",
        "nazev": "Veřejné ponížení",
        "typ": "trest",
        "efekty": {"humiliation": 15, "broken": 5, "strach": 8, "submisivita": 4},
        "cena_energie": 10,
        "cena_temnoty": 8,
        "riziko": 0.06,
        "vliv_inkvizice": 2
    },
    {
        "id": "psychologicky_natlak",
        "nazev": "Psychologický nátlak",
        "typ": "trest",
        "efekty": {"broken": 10, "mindbreak": 5, "strach": 8, "duvera": -6},
        "cena_energie": 5,
        "cena_temnoty": 10,
        "riziko": 0.03
    },
    {
        "id": "smyslne_trenovani",
        "nazev": "Smyslné trénování",
        "typ": "odmena",
        "efekty": {"touha": 12, "submisivita": 5, "loajalita": 2},
        "cena_energie": 15,
        "cena_temnoty": 0,
        "riziko": 0.0
    },
    {
        "id": "temny_ritual",
        "nazev": "Temný rituál",
        "typ": "trest",
        "efekty": {"mindbreak": 10, "broken": 8, "strach": 12},
        "cena_energie": 5,
        "cena_temnoty": 20,
        "riziko": 0.10
    },
    {
        "id": "nocni_sluzba",
        "nazev": "Noční služba",
        "typ": "odmena",
        "efekty": {"loajalita": 5, "touha": 4, "duvera": 2},
        "cena_energie": 8,
        "cena_temnoty": 0,
        "riziko": 0.0
    },
    {
        "id": "koupel_v_oleji",
        "nazev": "Koupel v oleji",
        "typ": "odmena",
        "efekty": {"touha": 8, "vlhkost": 10, "duvera": 3},
        "cena_energie": 7,
        "cena_temnoty": 0,
        "riziko": 0.0
    },
    # === DARK EXPANSION – nové interakce ===
    {
        "id": "znaceni_vlastnictvi",
        "nazev": "Značení vlastnictví",
        "typ": "trest",
        "efekty": {"loajalita": 8, "broken": 6, "humiliation": 12, "scarred": 4, "owned_mark": 1},
        "cena_energie": 12,
        "cena_temnoty": 15,
        "riziko": 0.05
    },
    {
        "id": "verejny_trenink",
        "nazev": "Veřejný trénink před harémem",
        "typ": "trest",
        "efekty": {"humiliation": 20, "submisivita": 12, "broken": 7, "strach": 10},
        "cena_energie": 15,
        "cena_temnoty": 10,
        "riziko": 0.07,
        "vliv_inkvizice": 3
    },
    {
        "id": "smyslove_pretižení",
        "nazev": "Smyslové přetížení",
        "typ": "trest",
        "efekty": {"touha": 15, "broken": 8, "mindbreak": 6, "vlhkost": 12},
        "cena_energie": 18,
        "cena_temnoty": 8,
        "riziko": 0.04
    },
    {
        "id": "nucena_regresse",
        "nazev": "Nucená regrese",
        "typ": "trest",
        "efekty": {"mindbreak": 12, "submisivita": 15, "broken": 5, "duvera": -4},
        "cena_energie": 10,
        "cena_temnoty": 18,
        "riziko": 0.06
    },
    {
        "id": "oralni_sluzba_hodiny",
        "nazev": "Orální služba (dlouhá)",
        "typ": "odmena",
        "efekty": {"poslusnost": 10, "loajalita": 6, "touha": 8, "submisivita": 5},
        "cena_energie": 20,
        "cena_temnoty": 0,
        "riziko": 0.0
    },
    {
        "id": "klec_a_cakani",
        "nazev": "Klec a čekání",
        "typ": "trest",
        "efekty": {"strach": 12, "submisivita": 10, "broken": 4, "duvera": -3},
        "cena_energie": 5,
        "cena_temnoty": 6,
        "riziko": 0.02
    },
    {
        "id": "kolektivni_pouziti",
        "nazev": "Kolektivní použití (harém)",
        "typ": "trest",
        "efekty": {"humiliation": 18, "broken": 10, "submisivita": 8, "touha": 5},
        "cena_energie": 25,
        "cena_temnoty": 12,
        "riziko": 0.08
    },
    {
        "id": "elixir_poslusnosti",
        "nazev": "Elixír poslušnosti",
        "typ": "neutralni",
        "efekty": {"poslusnost": 15, "submisivita": 10, "mindbreak": 4, "zavislost": 5},
        "cena_energie": 5,
        "cena_temnoty": 15,
        "riziko": 0.03
    },
    {
        "id": "rituali_poklona",
        "nazev": "Rituální poklona",
        "typ": "odmena",
        "efekty": {"loajalita": 12, "poslusnost": 8, "duvera": 4},
        "cena_energie": 8,
        "cena_temnoty": 5,
        "riziko": 0.0
    },
    {
        "id": "bolest_jako_odmena",
        "nazev": "Bolest jako odměna",
        "typ": "trest",
        "efekty": {"pain_addiction": 12, "touha": 10, "submisivita": 8, "broken": 3},
        "cena_energie": 14,
        "cena_temnoty": 10,
        "riziko": 0.05
    },
    {
        "id": "ticho_a_pohled",
        "nazev": "Ticho a pohled",
        "typ": "odmena",
        "efekty": {"duvera": 8, "loajalita": 5, "strach": -3},
        "cena_energie": 4,
        "cena_temnoty": 0,
        "riziko": 0.0
    },
    {
        "id": "vynucene_priznani",
        "nazev": "Vynucené přiznání",
        "typ": "trest",
        "efekty": {"broken": 9, "humiliation": 10, "mindbreak": 5, "duvera": -5},
        "cena_energie": 8,
        "cena_temnoty": 12,
        "riziko": 0.04
    },
]
