"""Pasivní schopnosti archetypů postav a jejich podmínky."""

from data.charaktery import normalizuj_charakter

SCHOPNOSTI = {
    "badatelka": "Při důvěře 40+ zlevní každý výzkum o 10 %.",
    "diplomatka": "Při důvěře 50+ posílí kladné diplomatické zisky o 20 %.",
    "ochranitelka": "Jako bojová společnice s důvěrou 50+ přidá +5 obrany.",
    "umelkyne": "Při důvěře 40+ přidá +5 zlata k dennímu příjmu harému.",
}


def aktivni_s_archetypem(hra, archetyp, duvera=0):
    """Vrátí členky přítomné v dominiu, které splňují podmínku schopnosti."""
    if hra is None or not hasattr(getattr(hra, "harem", None), "vsechny_aktivni"):
        return []
    return [
        otrok for otrok in hra.harem.vsechny_aktivni()
        if not getattr(otrok, "na_najmu", False)
        and normalizuj_charakter(getattr(otrok, "charakter", "")) == archetyp
        and getattr(otrok, "duvera", 0) >= duvera
    ]


def schopnost_postavy(otrok):
    archetyp = normalizuj_charakter(getattr(otrok, "charakter", ""))
    popis = SCHOPNOSTI.get(archetyp)
    if not popis:
        return "Její povaha ovlivňuje reakce na rozhovory a běžné interakce."
    return popis


def bonus_vyzkumu(hra):
    return 10 if aktivni_s_archetypem(hra, "badatelka", 40) else 0


def bonus_diplomacie(hra):
    return 20 if aktivni_s_archetypem(hra, "diplomatka", 50) else 0


def bonus_obrany(hra, jmeno_partnerky):
    if not jmeno_partnerky:
        return 0
    partnerka = next(
        (
            otrok for otrok in aktivni_s_archetypem(hra, "ochranitelka", 50)
            if otrok.jmeno == jmeno_partnerky
        ),
        None,
    )
    return 5 if partnerka else 0


def bonus_prijmu_haremu(hra):
    pocet = len(aktivni_s_archetypem(hra, "umelkyne", 40))
    return min(20, pocet * 5)
