"""Společné koeficienty obtížnosti pro souboje a ekonomiku."""

from game.settings import OBTIZNOSTI, VYCHOZI_OBTIZNOST

PROFILY = {
    "lehka": {
        "nepritel": 0.85,
        "poskozeni": 0.85,
        "cena": 0.85,
        "odmena": 1.15,
        "xp": 1.10,
    },
    "normalni": {
        "nepritel": 1.0,
        "poskozeni": 1.0,
        "cena": 1.0,
        "odmena": 1.0,
        "xp": 1.0,
    },
    "tezka": {
        "nepritel": 1.2,
        "poskozeni": 1.2,
        "cena": 1.15,
        "odmena": 1.25,
        "xp": 1.2,
    },
}


def normalizuj_obtiznost(obtiznost):
    return obtiznost if obtiznost in OBTIZNOSTI else VYCHOZI_OBTIZNOST


def profil_obtiznosti(obtiznost):
    return PROFILY[normalizuj_obtiznost(obtiznost)]


def uprav_cenu(cena, obtiznost):
    return max(1, int(round(cena * profil_obtiznosti(obtiznost)["cena"])))


def uprav_odmenu(odmena, obtiznost):
    return max(0, int(round(odmena * profil_obtiznosti(obtiznost)["odmena"])))


def uprav_xp(xp, obtiznost):
    return max(0, int(round(xp * profil_obtiznosti(obtiznost)["xp"])))
