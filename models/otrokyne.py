# models/otrokyne.py
from dataclasses import dataclass, asdict, field, fields
import random
from data.charaktery import CHARAKTERY
from data.degradace import ziskat_fazi, aplikuj_bonusy, Faze

@dataclass
class Otrokyně:
    jmeno: str
    srdce: int = 70
    poslusnost: int = 30
    vlhkost: int = 50
    submisivita: int = 40
    loajalita: int = 30
    nalada: str = "neutrální"
    plodnost: int = 50
    duvera: int = 30
    touha: int = 50
    tehotna: bool = False
    dny_tehotenstvi: int = 0
    deti: int = 0
    tolerance_bolesti: int = 50
    preference_drsnosti: int = 50
    strach: int = 30
    broken: int = 0
    pain_addiction: int = 0
    humiliation: int = 0
    bloodlust: int = 0
    mindbreak: int = 0
    scarred: int = 0
    owned_mark: bool = False
    hp: int = 100
    max_hp: int = 100
    podezreni_manipulace: int = 0
    na_najmu: bool = False
    klient: str = None
    typ_najmu: str = None
    dny_na_najmu: int = 0
    najem_zbyva_dni: int = 0
    najem_prijem_celkem: int = 0
    charakter: str = "subka"
    zavislost: int = 0
    typ_zavislosti: str = None
    abstinenco_priznaky: bool = False
    predavkovani: bool = False
    faze_zkazenosti: int = 0
    vek: int = 18

    def __post_init__(self):
        if self.charakter == "subka" and random.random() < 0.7:
            self.charakter = random.choice(list(CHARAKTERY.keys()))
        if self.vek == 18:
            self.vek = random.randint(18, 45)
        self.aktualizuj_fazi()

    def zvysit_stat(self, stat, hodnota):
        if hasattr(self, stat):
            nova = getattr(self, stat) + hodnota
            if stat == "hp":
                setattr(self, stat, max(0, min(self.max_hp, nova)))
            else:
                setattr(self, stat, max(0, min(100, nova)))
            self.aktualizuj_fazi()

    def aktualizuj_fazi(self):
        nova_faze = ziskat_fazi(self)
        if nova_faze > self.faze_zkazenosti:
            self.faze_zkazenosti = nova_faze
            aplikuj_bonusy(self)
            print(f"★ {self.jmeno} postoupila do fáze: {Faze[nova_faze]['nazev']}")

    def je_broken(self):
        return self.broken >= 85 or self.mindbreak >= 90

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data otrokyně musí být objekt.")
        allowed = {f.name for f in fields(cls)}
        values = {key: value for key, value in data.items() if key in allowed}
        otrok = cls(**values)
        # Staré sejvy mohou obsahovat výchozí charakter „subka“. Ten nesmí
        # být při načtení znovu náhodně přegenerován.
        for key, value in values.items():
            setattr(otrok, key, value)
        return otrok
