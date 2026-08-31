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
    role: str = "členka harému"
    osud_id: str = ""
    osud_krok: int = 0
    osud_volby: list = field(default_factory=list)
    osud_dokonceno: bool = False
    romance_body: int = 0
    romance_stav: str = "otevřená možnost"
    romance_volby: list = field(default_factory=list)
    souhlas_romance: bool = False
    historie_voleb: list = field(default_factory=list)
    partnerka: bool = False
    partner_od_den: int = 0
    lecba_zavislosti: int = 0
    vybaveni: list = field(default_factory=list)
    osud_zaver: str = ""
    manzelstvi: dict = field(default_factory=dict)
    je_manzelkou: bool = False
    den_zasnubin: int = 0
    den_svatby: int = 0
    oblibena: bool = False
    oblibena_od_den: int = 0

    def __post_init__(self):
        if self.charakter == "subka" and random.random() < 0.7:
            self.charakter = random.choice(list(CHARAKTERY.keys()))
        if self.vek == 18:
            self.vek = random.randint(18, 45)
        try:
            self.vek = max(18, int(self.vek))
        except (TypeError, ValueError):
            self.vek = 18
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

    def popis_osudu(self):
        if not self.osud_id:
            return "Osud zatím neznámý"
        return f"{self.osud_id} ({self.osud_krok})"

    def zaznamenej_volbu(self, kategorie, popis, den=None):
        zaznam = {"typ": kategorie, "volba": popis}
        if den is not None:
            zaznam["den"] = den
        self.historie_voleb.append(zaznam)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data otrokyně musí být objekt.")
        allowed = {f.name for f in fields(cls)}
        values = {key: value for key, value in data.items() if key in allowed}
        otrok = cls(**values)
        for key, value in values.items():
            setattr(otrok, key, value)
        try:
            otrok.vek = max(18, int(otrok.vek))
        except (TypeError, ValueError):
            otrok.vek = 18
        if not isinstance(otrok.romance_volby, list):
            otrok.romance_volby = []
        if not isinstance(otrok.historie_voleb, list):
            otrok.historie_voleb = []
        if not isinstance(otrok.vybaveni, list):
            otrok.vybaveni = []
        if not isinstance(otrok.osud_zaver, str):
            otrok.osud_zaver = ""
        if not isinstance(otrok.partnerka, bool):
            otrok.partnerka = False
        try:
            otrok.partner_od_den = max(0, int(otrok.partner_od_den))
        except (TypeError, ValueError):
            otrok.partner_od_den = 0
        try:
            otrok.lecba_zavislosti = max(0, min(100, int(otrok.lecba_zavislosti)))
        except (TypeError, ValueError):
            otrok.lecba_zavislosti = 0
        if not isinstance(otrok.romance_stav, str):
            otrok.romance_stav = "otevřená možnost"
        try:
            otrok.romance_body = max(0, min(100, int(otrok.romance_body)))
        except (TypeError, ValueError):
            otrok.romance_body = 0
        if not isinstance(getattr(otrok, "oblibena", False), bool):
            otrok.oblibena = bool(getattr(otrok, "oblibena", False))
        try:
            otrok.oblibena_od_den = max(0, int(getattr(otrok, "oblibena_od_den", 0) or 0))
        except (TypeError, ValueError):
            otrok.oblibena_od_den = 0
        if not isinstance(getattr(otrok, "je_manzelkou", False), bool):
            otrok.je_manzelkou = bool(getattr(otrok, "je_manzelkou", False))
        if not isinstance(getattr(otrok, "owned_mark", False), bool):
            otrok.owned_mark = bool(getattr(otrok, "owned_mark", False))
        try:
            otrok.loajalita = max(0, min(100, int(getattr(otrok, "loajalita", 30))))
        except (TypeError, ValueError):
            otrok.loajalita = 30
        return otrok
