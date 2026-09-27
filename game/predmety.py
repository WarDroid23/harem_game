"""Předměty použitelné v boji a jako výstup craftingu."""

PREDMETY = {
    "zdravotni_balicek": {
        "nazev": "Zdravotní balíček",
        "popis": "Obnoví 35 HP.",
        "boj": "leceni",
        "hodnota": 35,
    },
    "elixir_temnoty": {
        "nazev": "Elixír temnoty",
        "popis": "Doplní 25 temné energie.",
        "boj": "temnota",
        "hodnota": 25,
    },
    "dymovnice": {
        "nazev": "Dýmovnice",
        "popis": "Výrazně zvýší šanci na útěk.",
        "boj": "utek",
        "hodnota": 0,
    },
    "pecet_svedka": {
        "nazev": "Pečeť svědka",
        "popis": "Důkaz pro příběhové vyjednávání.",
        "boj": None,
        "hodnota": 0,
    },
    "remeslne_naradi": {
        "nazev": "Řemeslné nářadí",
        "popis": "Pomůže při správě území a opravách.",
        "boj": None,
        "hodnota": 0,
    },
    "signalni_roh": {
        "nazev": "Signální roh",
        "popis": "Přivolá pomoc během budoucí výpravy.",
        "boj": None,
        "hodnota": 0,
    },
    "tajny_vzkaz": {
        "nazev": "Tajný vzkaz",
        "popis": "Doklad o spojenectví s odbojem.",
        "boj": None,
        "hodnota": 0,
    },
    "opravarenska_sada": {
        "nazev": "Opravárenská sada",
        "popis": "Jednorázově posílí obranu při střetu.",
        "boj": "obrana",
        "hodnota": 8,
    },
    "dukazni_listina": {
        "nazev": "Důkazní listina",
        "popis": "Dokument, který mění vyjednávání s frakcemi.",
        "boj": None,
        "hodnota": 0,
    },
    "mapa_hvezd": {
        "nazev": "Mapa hvězd",
        "popis": "Pomáhá plánovat cesty mezi zahradou, věží a molem.",
        "boj": None,
        "hodnota": 0,
    },
    "klic_observatore": {
        "nazev": "Klíč observatoře",
        "popis": "Otevírá zabezpečené dveře severní věže.",
        "boj": None,
        "hodnota": 0,
    },
    "mesicni_kompas": {
        "nazev": "Měsíční kompas",
        "popis": "Jednou za den ukáže cestu k bezpečnému návratu.",
        "boj": None,
        "hodnota": 0,
    },
    "balzam_stinu": {
        "nazev": "Balzám stínů",
        "popis": "Obnoví 20 HP a 8 temné energie mimo boj.",
        "boj": "leceni_temnota",
        "hodnota": 20,
    },
    "ocelovy_zamek": {
        "nazev": "Ocelový zámek",
        "popis": "Dočasně posílí obranu v příštím souboji.",
        "boj": "obrana",
        "hodnota": 12,
    },
    "lucerna_soumraku": {
        "nazev": "Lucerna soumraku",
        "popis": "Vzácný nástroj pro průzkum a bezpečnější cestování.",
        "boj": None,
        "hodnota": 0,
    },
    "krvavy_ametyst": {
        "nazev": "Krvavý ametyst",
        "popis": "Vzácný krystal, který lze směnit za temnou esenci nebo použít v pokročilém rituálu.",
        "boj": None,
        "hodnota": 0,
    },
}
