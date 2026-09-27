import random
from dataclasses import dataclass, field

from config import (
    GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, GOLD, NC, BOLD, DIM, GRAY, WHITE
)
from utils.vypis import clear, terminalni_obrazek, tisk_chyba, tisk_info, tisk_ok, vytiskni_volbu, hlavicka
from game.predmety import PREDMETY

LOKACE = {
    "pevnost": {
        "nazev": "Černá pevnost",
        "kratky": "Pevnost",
        "ikona": "🏰",
        "popis": "Bezpečné zázemí tvého dominia a harému, chráněné kamennými valy.",
        "sousedni": ["trh", "les"],
        "uroven": 1,
        "nebezpeci": "bezpečno",
    },
    "trh": {
        "nazev": "Starý trh",
        "kratky": "Trh",
        "ikona": "⚖",
        "popis": "Obchodníci, překupníci a lidé, kteří slyší víc, než říkají.",
        "sousedni": [
            "pevnost", "pristav", "ctvrt_remeselniku", "hostinec", "lazne",
            "akademie", "katakomby", "palac_bohatych", "cervena_ctvrt", "chram_cistoty"
        ],
        "uroven": 1,
        "nebezpeci": "nízké",
    },
    "les": {
        "nazev": "Mlžný les",
        "kratky": "Les",
        "ikona": "🌲",
        "popis": "Zkratka k hranici s hustými hvozdy, kde se v mlze ztrácejí karavany.",
        "sousedni": ["pevnost", "hranice", "haj_soumraku", "svatyne_krvaveho_mesice", "krvavy_lom"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "pristav": {
        "nazev": "Černý přístav",
        "kratky": "Přístav",
        "ikona": "⚓",
        "popis": "Místo pašeráků, lodí a zpráv z dalekých zemí.",
        "sousedni": ["trh", "molo_mesicniho_pristavu", "palac_bohatych", "cervena_ctvrt", "paserska_zatoka"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "hranice": {
        "nazev": "Hraniční ves",
        "kratky": "Hranice",
        "ikona": "⚔",
        "popis": "Opevněná vesnice na pomezí říše, ohrožovaná nájezdy ze severu.",
        "sousedni": ["les", "observator", "krvavy_lom", "zricenina_astralni_veze"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
    "ctvrt_remeselniku": {
        "nazev": "Čtvrť řemeslníků",
        "kratky": "Řemesla",
        "ikona": "🔨",
        "popis": "Dílny, cechy a lidé, kteří umí proměnit suroviny v užitečné vybavení.",
        "sousedni": ["trh", "akademie", "palac_bohatych", "krvavy_lom"],
        "uroven": 2,
        "nebezpeci": "nízké",
    },
    "hostinec": {
        "nazev": "Hostinec U Tří svící",
        "kratky": "Hostinec",
        "ikona": "🍺",
        "popis": "Rušný hostinec, kde se najíš, vyspíš a zaslechneš nové zvěsti.",
        "sousedni": ["trh", "lazne"],
        "uroven": 1,
        "nebezpeci": "bezpečno",
    },
    "lazne": {
        "nazev": "Městské lázně",
        "kratky": "Lázně",
        "ikona": "♨",
        "popis": "Teplé prameny obnovují sílu poutníkům i pánům dominia.",
        "sousedni": ["trh", "hostinec", "haj_soumraku", "sklenena_zahrada", "katakomby"],
        "uroven": 1,
        "nebezpeci": "bezpečno",
    },
    "haj_soumraku": {
        "nazev": "Háj soumraku",
        "kratky": "Háj",
        "ikona": "🌿",
        "popis": "Tiché místo mezi lesem a prameny, vhodné k meditaci a temným rituálům.",
        "sousedni": ["les", "lazne", "svatyne_krvaveho_mesice", "zahradni_altan"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "akademie": {
        "nazev": "Alchymistická akademie",
        "kratky": "Akademie",
        "ikona": "📜",
        "popis": "Učenci zde zkoumají esence a vyměňují je za vzácné suroviny.",
        "sousedni": ["ctvrt_remeselniku", "trh", "sklenena_zahrada"],
        "uroven": 2,
        "nebezpeci": "nízké",
    },
    "sklenena_zahrada": {
        "nazev": "Skleněná zahrada",
        "kratky": "Zahrada",
        "ikona": "🌺",
        "popis": "Zastřešená zahrada plná světla a exotických květin, kde se dá mluvit beze spěchu.",
        "sousedni": ["lazne", "akademie", "observator", "molo_mesicniho_pristavu", "zahradni_altan"],
        "uroven": 2,
        "nebezpeci": "bezpečno",
    },
    "observator": {
        "nazev": "Observatoř severní věže",
        "kratky": "Observatoř",
        "ikona": "🔭",
        "popis": "Staré čočky a astroláby odkrývají cesty, které město raději zapomnělo.",
        "sousedni": ["sklenena_zahrada", "hranice", "molo_mesicniho_pristavu", "zricenina_astralni_veze"],
        "uroven": 3,
        "nebezpeci": "střední",
    },
    "molo_mesicniho_pristavu": {
        "nazev": "Molo Měsíčního přístavu",
        "kratky": "Molo",
        "ikona": "🌊",
        "popis": "Tiché molo na okraji přístavu, kde se uzavírají dohody a odplouvá do dálek.",
        "sousedni": ["pristav", "observator", "sklenena_zahrada", "paserska_zatoka"],
        "uroven": 3,
        "nebezpeci": "střední",
    },
    "katakomby": {
        "nazev": "Katakomby pod městem",
        "kratky": "Katakomby",
        "ikona": "💀",
        "popis": "Starobylé podzemní hrobky pod starým městem, zřídlo temné energie a zapomenutých relikvií.",
        "sousedni": ["trh", "lazne", "svatyne_krvaveho_mesice", "podzemni_arena", "chram_cistoty", "tajna_svatyne_stinu", "vezeni_inkvizice"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
    "svatyne_krvaveho_mesice": {
        "nazev": "Krvavá svatyně v lese",
        "kratky": "Svatyně",
        "ikona": "🩸",
        "popis": "Opuštěná kultistická svatyně ukrytá v Mlžném lese pro temné rituály dominia.",
        "sousedni": ["les", "haj_soumraku", "katakomby", "zricenina_astralni_veze"],
        "uroven": 3,
        "nebezpeci": "velmi vysoké",
    },
    "palac_bohatych": {
        "nazev": "Palác a čtvrť bohatých",
        "kratky": "Palác",
        "ikona": "👑",
        "popis": "Sídlo městské smetánky a guvernérův palác, centrum intrik, luxusu a politického vlivu.",
        "sousedni": ["trh", "ctvrt_remeselniku", "pristav", "cervena_ctvrt", "stribrne_terasy", "chram_cistoty", "vezeni_inkvizice"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "cervena_ctvrt": {
        "nazev": "Červená čtvrť nevěstinců",
        "kratky": "Čtvrť",
        "ikona": "💋",
        "popis": "Srdce nočních rozkoší města, plné nevěstinců, mecenášů a obchodu s otrokyněmi.",
        "sousedni": ["trh", "palac_bohatych", "pristav", "podzemni_arena", "tajna_svatyne_stinu"],
        "uroven": 1,
        "nebezpeci": "nízké",
    },
    "podzemni_arena": {
        "nazev": "Podzemní gladiátorská aréna",
        "kratky": "Aréna",
        "ikona": "⚔",
        "popis": "Krvavá aréna vytesaná do skal pod městem, kde bojují otroci i šampioni o zlato.",
        "sousedni": ["cervena_ctvrt", "katakomby"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
    "stribrne_terasy": {
        "nazev": "Stříbrné terasy",
        "kratky": "Terasy",
        "ikona": "🏛",
        "popis": "Vyvýšené zahrady a promenáda aristokracie nad městem s výhledem na celé dominium.",
        "sousedni": ["palac_bohatych", "sklenena_zahrada", "observator", "zahradni_altan"],
        "uroven": 2,
        "nebezpeci": "nízké",
    },
    "chram_cistoty": {
        "nazev": "Chrám Čistoty a Světla",
        "kratky": "Chrám",
        "ikona": "⛪",
        "popis": "Monumentální mramorový chrám inkvizice, kde znějí chorály a vykupují se hříchy zlatem.",
        "sousedni": ["trh", "palac_bohatych", "katakomby", "vezeni_inkvizice"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "tajna_svatyne_stinu": {
        "nazev": "Tajemné doupě Nočních stínů",
        "kratky": "Doupě",
        "ikona": "🗡",
        "popis": "Skrytá podzemní síň Syndikátu stínů za padacími dveřmi, centrum pašeráků a nájemných vrahů.",
        "sousedni": ["podzemni_arena", "katakomby", "cervena_ctvrt"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
    "zahradni_altan": {
        "nazev": "Zahradní romantický altán",
        "kratky": "Altán",
        "ikona": "🌹",
        "popis": "Klidné mramorové loubí u leknínového jezírka, ideální útočiště pro rande s manželkami a odpočinek.",
        "sousedni": ["sklenena_zahrada", "haj_soumraku", "stribrne_terasy"],
        "uroven": 1,
        "nebezpeci": "bezpečno",
    },
    "vezeni_inkvizice": {
        "nazev": "Inkviziční žalář & kobky kacířů",
        "kratky": "Žalář",
        "ikona": "⛓️",
        "popis": "Chmurné podzemní kobky a mučírna inkvizice, kde v okovech trpí obviněné čarodějky a nepřátelé víry.",
        "sousedni": ["chram_cistoty", "katakomby", "palac_bohatych"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
    "zricenina_astralni_veze": {
        "nazev": "Zapomenutá astrální citadela",
        "kratky": "Citadela",
        "ikona": "🏛️",
        "popis": "Vznešené ruiny z dob před pádem starého impéria. Ve vzduchu jiskří zbytky astrální magie.",
        "sousedni": ["observator", "hranice", "svatyne_krvaveho_mesice"],
        "uroven": 3,
        "nebezpeci": "velmi vysoké",
    },
    "paserska_zatoka": {
        "nazev": "Zátoka vraků & Pašerácká zátoka",
        "kratky": "Zátoka",
        "ikona": "🏴‍☠️",
        "popis": "Skryté skalnaté pobřeží, kde kotví korsárské lodě plné kontrabandu a cizokrajných otrokyň.",
        "sousedni": ["pristav", "molo_mesicniho_pristavu"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "krvavy_lom": {
        "nazev": "Krvavé kamenolomy & Doly otroků",
        "kratky": "Lomy",
        "ikona": "⛏️",
        "popis": "Drsný povrchový lom a šachty na úpatí hor, kde trestanci těží stavební kámen a železnou rudu.",
        "sousedni": ["hranice", "les", "ctvrt_remeselniku"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
}

VYCHOZI_ODHALENE = [
    "pevnost", "trh", "les", "hostinec", "lazne", "haj_soumraku", "akademie"
]

NPC = {
    "mira": {
        "jmeno": "Mira, potulná léčitelka",
        "popis": "Pomáhá zraněným bez ohledu na jejich minulost.",
        "lokace": "trh",
    },
    "radan": {
        "jmeno": "Radan, pašerák",
        "popis": "Zná tajné stezky a shání vzácné suroviny.",
        "lokace": "pristav",
    },
    "elian": {
        "jmeno": "Elian, městský informátor",
        "popis": "Vyměňuje zprávy za laskavosti a opatrnost.",
        "lokace": "trh",
    },
    "borin": {
        "jmeno": "Borin, hostinský",
        "popis": "Dobrosrdečný hostinský, který pozná poutníka podle kroku.",
        "lokace": "hostinec",
    },
    "velena": {
        "jmeno": "Velena, správkyně lázní",
        "popis": "Pečuje o prameny a nabízí léčivou proceduru za rozumnou cenu.",
        "lokace": "lazne",
    },
    "sava": {
        "jmeno": "Sava, strážkyně háje",
        "popis": "Mlčenlivá strážkyně, která učí soustředění a zná sílu nočního stínu.",
        "lokace": "haj_soumraku",
    },
    "nela": {
        "jmeno": "Nela, mladá alchymistka",
        "popis": "Hledá pomocníky pro své pokusy a odměňuje je užitečnými esencemi.",
        "lokace": "akademie",
    },
    "lyra": {
        "jmeno": "Lyra, kartografka hvězd",
        "popis": "Dospělá kartografka, která kreslí bezpečné cesty i mapy lidské důvěry.",
        "lokace": "sklenena_zahrada",
        "vek": 29,
        "dialogy": [
            "Když člověk zná svou cestu, nemusí nikoho vlastnit, aby nebyl sám.",
            "Můžeme mluvit o tom, co chceme, až když stejně dobře umíme říct ne.",
        ],
    },
    "cassian": {
        "jmeno": "Cassian, správce observatoře",
        "popis": "Dospělý správce věže, který chrání její archiv před lidmi toužícími po moci.",
        "lokace": "observator",
        "vek": 34,
        "dialogy": [
            "Hvězdy nejsou věštba. Jsou připomínka, že i dlouhá noc jednou skončí.",
            "Archiv otevřu jen těm, kdo unesou pravdu bez toho, aby ji použili proti druhým.",
        ],
    },
    "tereza": {
        "jmeno": "Tereza, kapitánka měsíčního mola",
        "popis": "Dospělá kapitánka, která dává posádce druhou šanci a jasné hranice.",
        "lokace": "molo_mesicniho_pristavu",
        "vek": 31,
        "dialogy": [
            "Důvěra se nevyžaduje rozkazem. Staví se z malých rozhodnutí, která platí i zítra.",
            "Pokud chceš plout se mnou, řekni mi nejdřív, kam skutečně míříš.",
        ],
    },
    "mortis": {
        "jmeno": "Mortis, strážce krypt",
        "popis": "Nekromantský badatel v katakombách, který zná tajemství temných esencí.",
        "lokace": "katakomby",
        "vek": 48,
        "dialogy": [
            "Smrt je jen tichý spánek... pravá moc začíná tam, kde končí strach.",
        ],
    },
    "morana": {
        "jmeno": "Morana, velekněžka krve",
        "popis": "Temná rituální kněžka ve svatyni, oddaná silám krvavého měsíce.",
        "lokace": "svatyne_krvaveho_mesice",
        "vek": 27,
        "dialogy": [
            "Tvůj harém je tvým chrámem. Čím hlouběji klesnou, tím výš stoupne tvé dominium.",
        ],
    },
    "lord_vane": {
        "jmeno": "Lord Vane, městský radní",
        "popis": "Zkorumpovaný šlechtic v paláci, který za správnou cenu zařídí cokoliv.",
        "lokace": "palac_bohatych",
        "vek": 42,
        "dialogy": [
            "Zlato otevírá dveře, které ani inkvizice nedokáže zavřít.",
        ],
    },
    "madame_scarlett": {
        "jmeno": "Madame Scarlett, vládkyně rozkoší",
        "popis": "Majitelka nočních salónů v Červené čtvrti. Zná tajemství nejmocnějších mužů města.",
        "lokace": "cervena_ctvrt",
        "vek": 35,
        "dialogy": [
            "V mém podniku se prodává zapomnění, pane. A zapomnění je nejdražší komodita.",
            "Otrokyně, která umí potěšit i mlčet, má větší cenu než truhla drahokamů.",
        ],
    },
    "baron_archibald": {
        "jmeno": "Baron Archibald, zhýralý mecenáš",
        "popis": "Bohatý aristokrat vyhledávající exotická potěšení a nákup nových otrokyň.",
        "lokace": "cervena_ctvrt",
        "vek": 50,
        "dialogy": [
            "Peníze pro mě nic neznamenají. Hledám vášeň, poslušnost a půvab.",
        ],
    },
    "gladiator_gor": {
        "jmeno": "Gladiátor Gor, nezlomený šampion",
        "popis": "Zjizvený válečník arény, který vyhrál sto soubojů na život a na smrt.",
        "lokace": "podzemni_arena",
        "vek": 33,
        "dialogy": [
            "Krev v písku nikdy nelže. Přežijí jen ti s ocelovou vůlí.",
        ],
    },
    "lady_eleanor": {
        "jmeno": "Lady Eleanor, intrikářka z teras",
        "popis": "Chladná šlechtična ze Stříbrných teras, která z výšky tahá za nitky městské politiky.",
        "lokace": "stribrne_terasy",
        "vek": 28,
        "dialogy": [
            "Město je jako šachovnice. Každá tvá otrokyně i každý voják jsou pouhé figurky.",
        ],
    },
    "vladyka_aurelius": {
        "jmeno": "Velekněz Aurelius, hlas Inkvizice",
        "popis": "Přísný církevní hodnostář v Chrámu Čistoty, který za tučné dary odpouští i nejtemnější hříchy.",
        "lokace": "chram_cistoty",
        "vek": 54,
        "dialogy": [
            "Každý hřích má svou váhu v mincích a zbožnosti, bratře.",
            "Inkvizice vidí všechno, ale ruka plná zlata dokáže její zrak na chvíli zastřít.",
        ],
    },
    "stinovy_mistr_kage": {
        "jmeno": "Mistr Kage, šéf Nočních stínů",
        "popis": "Mlčenlivý mistr vrahů a pašeráků v tajné svatyni pod městem.",
        "lokace": "tajna_svatyne_stinu",
        "vek": 39,
        "dialogy": [
            "V temnotě nejsou žádná pravidla, jen ti, co přežili, a ti, co udělali chybu.",
            "Tvé dominium roste rychle. Syndikát stínů tě bedlivě sleduje.",
        ],
    },
    "knezka_valeria": {
        "jmeno": "Valeria, strážkyně altánu",
        "popis": "Půvabná zahradnice a rádkyně pro vztahy v zahradním altánu u jezera.",
        "lokace": "zahradni_altan",
        "vek": 25,
        "dialogy": [
            "Květiny i ženy v harému potřebují stejnou péči – správné množství slunce, pozornosti a vody.",
            "Klidná zahrada dokáže usmířit i nejdivočejší žárlivost mezi tvými manželkami.",
        ],
    },
    "inkvizitor_malor": {
        "jmeno": "Inkvizitor Malor, Kladivo na kacíře",
        "popis": "Nemilosrdný vyšetřovatel v železné masce, který spravuje inkviziční žalář a vyhledává zakázané texty.",
        "lokace": "vezeni_inkvizice",
        "vek": 46,
        "dialogy": [
            "Hřích je jako plíseň na chlebu – musí být vyříznut i s kusem masa.",
            "Každá čarodějka v těchto celách nakonec zazpívá píseň pokání... nebo shoří.",
        ],
    },
    "vespera": {
        "jmeno": "Vespera, uvězněná čarodějka",
        "popis": "Hrdá mladá žena s planoucíma fialovýma očima a runami na kůži, čekající v okovech na inkviziční rozsudek.",
        "lokace": "vezeni_inkvizice",
        "vek": 23,
        "dialogy": [
            "Jejich okovy mého ducha nezlomí. Pokud mě odsud dostaneš, mé síly budou patřit tobě.",
            "Církev se bojí toho, co nedokáže ovládat. V mé krvi plane prastarý oheň.",
        ],
    },
    "selene": {
        "jmeno": "Selene, astrální vědma",
        "popis": "Prastará čarodějka střežící runy zapomenuté astrální citadely a pamatující pád starého impéria.",
        "lokace": "zricenina_astralni_veze",
        "vek": 120,
        "dialogy": [
            "Čas je jen kruh vyrytý do kamene. Tvé dominium buď povstane jako nové impérium, nebo se rozpadne v prach.",
            "Hvězdy dnes šeptají tvé jméno. Dovol mi nahlédnout do tvé temné aury.",
        ],
    },
    "kapitanka_drake": {
        "jmeno": "Kapitánka Drake, pirátská vlčice",
        "popis": "Ostřílená korsárka se šavlí u pasu, velitelka lodi Černá harpyje kotvící v zátoce vraků.",
        "lokace": "paserska_zatoka",
        "vek": 32,
        "dialogy": [
            "Moře nezná slitování a já taky ne. Mince mluví hlasitěji než všechny zákony města.",
            "Mám v podpalubí pár nových kousků z dalekých ostrovů. Ukaž zlato a můžeme se bavit.",
        ],
    },
    "dozorce_krag": {
        "jmeno": "Vrchní dozorce Krag",
        "popis": "Hromotluk s karabáčem zocelený prachem a křikem trestanců v krvavých lomech.",
        "lokace": "krvavy_lom",
        "vek": 41,
        "dialogy": [
            "V mém lomu se buď kope, nebo umírá. Žádné slitování s těmi, co neunesou těžké kladivo.",
            "Hledáš pevný stavební kámen a železo pro svou pevnost? Moji otroci vykopou cokoliv, když dobře zaplatíš.",
        ],
    },
}


@dataclass
class SvetSystem:
    aktualni_lokace: str = "pevnost"
    odhalene_lokace: list = field(default_factory=lambda: list(VYCHOZI_ODHALENE))
    navstiveno: dict = field(default_factory=dict)
    vztahy_npc: dict = field(default_factory=lambda: {k: 0 for k in NPC})

    def __post_init__(self):
        if not isinstance(self.aktualni_lokace, str) or self.aktualni_lokace not in LOKACE:
            self.aktualni_lokace = "pevnost"
        puvodni_lokace = self.odhalene_lokace
        if not isinstance(puvodni_lokace, list):
            puvodni_lokace = []
        self.odhalene_lokace = [
            k for k in puvodni_lokace if k in LOKACE
        ]
        # Nové lokace se přidají i do starších savů, které mapu ještě neměly.
        for lokace in VYCHOZI_ODHALENE:
            if lokace not in self.odhalene_lokace:
                self.odhalene_lokace.append(lokace)
        if not self.odhalene_lokace:
            self.odhalene_lokace = ["pevnost"]
        if "pevnost" not in self.odhalene_lokace:
            self.odhalene_lokace.insert(0, "pevnost")
        puvodni_vztahy = self.vztahy_npc if isinstance(self.vztahy_npc, dict) else {}
        vztahy = {}
        for npc_id in NPC:
            try:
                hodnota = int(puvodni_vztahy.get(npc_id, 0))
            except (TypeError, ValueError):
                hodnota = 0
            vztahy[npc_id] = max(-100, min(100, hodnota))
        self.vztahy_npc = vztahy

    def odhal_lokaci(self, lokace):
        if lokace in LOKACE and lokace not in self.odhalene_lokace:
            self.odhalene_lokace.append(lokace)
            return True
        return False

    def zmen_vztah(self, npc_id, delta):
        if npc_id not in NPC:
            return False
        self.vztahy_npc[npc_id] = max(-100, min(100, self.vztahy_npc[npc_id] + delta))
        return True

    def _format_uzel(self, lok_id, hra, sirka=11):
        """Naformátuje uzel na mapě s pevně zarovnanou šířkou a ikonami statusu."""
        info = LOKACE[lok_id]
        kratky = info.get("kratky", info["nazev"][:7])
        ikona = info.get("ikona", "•")

        if lok_id not in self.odhalene_lokace:
            return f" {GRAY}[?Neodhaleno?]{NC} "

        je_zde = (lok_id == self.aktualni_lokace)

        je_mafie = False
        if hasattr(hra, "mafie") and hasattr(hra.mafie, "uzemi"):
            for u in getattr(hra.mafie, "uzemi", []):
                if getattr(u, "obsazeno", False) and (
                    u.nazev.lower() in info["nazev"].lower() or lok_id in u.nazev.lower()
                ):
                    je_mafie = True
                    break

        je_quest = False
        if hasattr(hra, "questy") and hra.questy and getattr(hra.questy, "aktivni_quest", None):
            q_lok = hra.questy.aktivni_quest.get("lokace")
            if q_lok == lok_id:
                je_quest = True

        tag = ""
        if je_quest:
            tag += "🎯"
        if je_mafie:
            tag += "🛡️"

        text = f"{ikona} {kratky}{tag}"
        if je_zde:
            return f"{GREEN}{BOLD}▶[{text:^{sirka}}]◀{NC}"
        else:
            return f" {CYAN}[{text:^{sirka}}]{NC} "

    def vykresli_ascii_mapu(self, hra):
        """Vykreslí přehlednou barevnou síťovou mapu království o 26 lokacích."""
        u = lambda lid: self._format_uzel(lid, hra)

        print(f"{GOLD}╔══════════════════════════════════ ASCII MAPA KRÁLOVSTVÍ ══════════════════════════════════╗{NC}")
        print(f"║                                                                                           ║")
        print(f"║ {u('pevnost')} ══ {u('les')} ══ {u('krvavy_lom')} ══ {u('hranice')} ══ {u('zricenina_astralni_veze')} ║")
        print(f"║        ║              ║                               ║              ║                    ║")
        print(f"║        ║              ║                       {u('svatyne_krvaveho_mesice')} ║                    ║")
        print(f"║        ║              ║                               ║              ║                    ║")
        print(f"║ {u('trh')} ═════════ {u('haj_soumraku')} ════════════════════ {u('observator')} ════════╝                    ║")
        print(f"║   ║ ║  ║              ║                               ║                                   ║")
        print(f"║   ║ ║ {u('ctvrt_remeselniku')} ════ {u('lazne')} ══════════════════ {u('sklenena_zahrada')}                                ║")
        print(f"║   ║ ║  ║              ║                               ║                                   ║")
        print(f"║   ║ ║ {u('palac_bohatych')} ═══ {u('stribrne_terasy')} ════════════════ {u('zahradni_altan')}                                  ║")
        print(f"║   ║ ║  ║              ║                                                                   ║")
        print(f"║ {u('cervena_ctvrt')} ══ {u('pristav')} ══════════════ {u('molo_mesicniho_pristavu')} ══ {u('paserska_zatoka')}                           ║")
        print(f"║   ║    ║              ║                               ║                                   ║")
        print(f"║ {u('podzemni_arena')} ═══ {u('katakomby')} ═══ {u('chram_cistoty')} ═════════ {u('vezeni_inkvizice')}                            ║")
        print(f"║        ║                                                                                  ║")
        print(f"║ {u('tajna_svatyne_stinu')}                                                                        ║")
        print(f"║                                                                                           ║")
        print(f"{GOLD}╚═══════════════════════════════════════════════════════════════════════════════════════════╝{NC}")
        print(f"{DIM}Legenda: {GREEN}▶[ ... ]◀{NC}{DIM} Jsi zde | {CYAN}[🛡️]{NC}{DIM} Území tvé mafie | {CYAN}[🎯]{NC}{DIM} Aktivní quest | {GRAY}[?Neodhaleno?]{NC}\n")

    def _generuj_cestovni_udalost(self, cil, hra):
        """Spustí náhodnou událost při cestě mezi dvěma lokacemi."""
        if random.random() > 0.45:
            return

        print(f"\n{YELLOW}⚡ Cestovní událost na stezce do: {LOKACE[cil]['nazev']}!{NC}")
        event_typ = random.choice([
            "banditi", "kupec", "uprchlice", "inkvizice", "zridlo",
            "arena_vyzva", "kurtizana_noc", "kultiste", "tajna_schranka"
        ])

        if event_typ == "banditi":
            print("Z křovin vyskočila banda hrdlořezů s tasenými zbraněmi!")
            vytiskni_volbu('1', 'Zahnat je silou mafie (vyžaduje vojáky)')
            vytiskni_volbu('2', 'Rozprášit je temnou aurou (stojí 8 temné energie)')
            vytiskni_volbu('3', 'Zaplatit výkupné (35 🪙)')
            volba = input("> ").strip()
            if volba == "1":
                vojaci = getattr(hra.mafie, "vojaci", 0)
                if vojaci >= 2:
                    korist = random.randint(30, 65)
                    hra.hrac.gold += korist
                    tisk_ok(f"Tví vojáci mafie bandity bez milosti rozehnali! Získáno +{korist} 🪙 kořisti.")
                else:
                    hra.hrac.hp = max(1, hra.hrac.hp - 18)
                    tisk_chyba("Nemáš dost vojáků – v potyčce jsi byl zraněn (-18 HP).")
            elif volba == "2":
                if hra.hrac.dark_energy >= 8:
                    hra.hrac.dark_energy -= 8
                    tisk_ok("Tvé oči vzplály temným ohněm. Bandité se s křikem rozprchli do tmy!")
                else:
                    tisk_chyba("Nemáš dost temné energie – musel jsi zaplatit výkupné.")
                    hra.hrac.gold = max(0, hra.hrac.gold - 35)
            else:
                hra.hrac.gold = max(0, hra.hrac.gold - 35)
                tisk_info("Zaplatil jsi 35 zlaťáků výkupného a pokračuješ v cestě.")

        elif event_typ == "kupec":
            print("U cesty odpočívá krytý vůz potulného felčara a překupníka.")
            vytiskni_volbu('1', 'Koupit léčivý elixír (25 🪙, +25 HP)')
            vytiskni_volbu('2', 'Koupit bylinu měsíčnice (20 🪙)')
            vytiskni_volbu('0', 'Pokračovat v cestě')
            volba = input("> ").strip()
            if volba == "1" and hra.hrac.gold >= 25:
                hra.hrac.gold -= 25
                hra.hrac.hp = min(hra.hrac.max_hp, hra.hrac.hp + 25)
                tisk_ok("Elixír vypit. HP +25.")
            elif volba == "2" and hra.hrac.gold >= 20:
                hra.hrac.gold -= 20
                if hasattr(hra, "alchymie"):
                    hra.alchymie.pridat_surovinu("bylina_mesicni", 1)
                tisk_ok("Získána bylina měsíčnice do alchymie.")

        elif event_typ == "uprchlice":
            print("Ve škarpě u cesty se chvěje vyčerpaná dívka v roztrhaných šatech.")
            vytiskni_volbu('1', 'Vzít ji pod svou ochranu a odvést do dominia (nová otrokyně)')
            vytiskni_volbu('2', 'Nechat ji osudu a pokračovat dál')
            volba = input("> ").strip()
            if volba == "1":
                from models.otrokyne import Otrokyně
                from data.jmena import JMENA
                jmeno = random.choice(JMENA)
                nova = Otrokyně(jmeno=jmeno, vek=random.randint(18, 24))
                nova.charakter = random.choice(["subka", "ustrasena", "kurtizana"])
                nova.loajalita = 55
                nova.poslusnost = 50
                hra.harem.pridat(nova)
                tisk_ok(f"★ Zachránil jsi dívku {jmeno}. Vděčně tě následuje do tvého harému!")
                try:
                    from game.kronika import zaznamenej
                    zaznamenej(hra, f"Cesta: nalezena a zotročena uprchlice {jmeno}.")
                except Exception:
                    pass

        elif event_typ == "inkvizice":
            print("Cestu křižuje hlídka městské inkvizice v těžkých pláštích.")
            vliv = getattr(hra.hrac, "vliv_inkvizice", 0)
            if vliv < 30:
                tisk_ok("Hlídka tě přehlédla s chladným pokývnutím. Cesta je volná.")
            else:
                print("Stráže tě podezíravě zastavují a dožadují se kontroly.")
                if hra.hrac.gold >= 40:
                    hra.hrac.gold -= 40
                    tisk_ok("Zaplatil jsi úplatek 40 🪙 strážím. Pustili tě dál.")
                else:
                    hra.hrac.vliv_inkvizice = min(100, vliv + 6)
                    tisk_chyba("Nemáš na úplatek – stráže si zapsaly tvůj popis. Vliv inkvizice vzrostl!")

        elif event_typ == "zridlo":
            print("Objevil jsi starobylé zřídlo vyvěrající ze skal, naplněné magickou silou.")
            max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
            max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
            hra.hrac.sex_energy = min(max_s, hra.hrac.sex_energy + 15)
            hra.hrac.dark_energy = min(max_t, hra.hrac.dark_energy + 15)
            tisk_ok("Napil ses ze zřídla. Energie obnovena (+15 sex, +15 temno)!")

        elif event_typ == "arena_vyzva":
            print("V cestě stojí potulný bijec v ostnaté zbroji z Podzemní arény.")
            print("„Zaplať 20 zlaťáků mýtné, nebo si to se mnou rozdej na férovku!“")
            vytiskni_volbu('1', 'Přijmout výzvu a srazit ho k zemi (test HP a síly)')
            vytiskni_volbu('2', 'Zaplatit mu 20 🪙')
            v = input("> ").strip()
            if v == "1":
                if hra.hrac.hp > 30:
                    hra.hrac.hp -= 15
                    vyhra = random.randint(45, 80)
                    hra.hrac.gold += vyhra
                    tisk_ok(f"Zpráskal jsi rváče do krve! Nechal ti svou brašnu (+{vyhra} 🪙).")
                else:
                    hra.hrac.hp = max(1, hra.hrac.hp - 20)
                    hra.hrac.gold = max(0, hra.hrac.gold - 20)
                    tisk_chyba("Byl jsi příliš oslabený – bijec tě přemohl a okradl!")
            else:
                hra.hrac.gold = max(0, hra.hrac.gold - 20)
                tisk_info("Odevzdal jsi 20 mincí.")

        elif event_typ == "kurtizana_noc":
            print("Z postranní uličky vyšla svůdná kurtizána v hedvábném plášti.")
            print("„Hledám pána s vkusem a štědrou dlaní...“")
            vytiskni_volbu('1', 'Věnovat se jí chvíli na lavičce (stojí 15 🪙, +20 sexuální energie)')
            vytiskni_volbu('2', 'Nabídnout jí útočiště v tvém nevěstinci / harému (požaduje 60 🪙)')
            vytiskni_volbu('0', 'Odmítnout')
            v = input("> ").strip()
            if v == "1" and hra.hrac.gold >= 15:
                hra.hrac.gold -= 15
                max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
                hra.hrac.sex_energy = min(max_s, hra.hrac.sex_energy + 20)
                tisk_ok("Sladké rozptýlení na cestě ti vlilo novou energii do žil (+20 sex energie)!")
            elif v == "2" and hra.hrac.gold >= 60:
                hra.hrac.gold -= 60
                from models.otrokyne import Otrokyně
                from data.jmena import JMENA
                jmeno = random.choice(JMENA)
                nova = Otrokyně(jmeno=jmeno, charakter="kurtizana", vek=random.randint(20, 26))
                nova.touha = 75
                nova.vlhkost = 70
                nova.poslusnost = 60
                nova.loajalita = 60
                hra.harem.pridat(nova)
                tisk_ok(f"Kurtizána {jmeno} se s radostí připojila k tvému dominium!")
                if "cech_kurtizan" in hra.frakce.frakce:
                    hra.frakce.frakce["cech_kurtizan"].zmenit(5)

        elif event_typ == "kultiste":
            print("V mlze prochází procesí v kápích se zapálenými pochodněmi – Kult Krvavého Měsíce.")
            vytiskni_volbu('1', 'Připojit se ke krátkému šeptanému rituálu (zisk temné energie a přízně)')
            vytiskni_volbu('2', 'Pozorovat z úkrytu a nevstupovat do cesty')
            v = input("> ").strip()
            if v == "1":
                max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
                hra.hrac.dark_energy = min(max_t, hra.hrac.dark_energy + 15)
                if "kult_krve" in hra.frakce.frakce:
                    hra.frakce.frakce["kult_krve"].zmenit(8)
                tisk_ok("Sdílel jsi krev s kultisty. Temná energie +15, reputace s Kultem krve +8.")
            else:
                tisk_info("Procesí prošlo kolem bez povšimnutí.")

        elif event_typ == "tajna_schranka":
            print("Pod uvolněným kamenným kvádrem jsi zahlédl značku Syndikátu Nočních stínů!")
            vytiskni_volbu('1', 'Vypáčit schránku (šance na poklad, vyžaduje opatrnost)')
            vytiskni_volbu('2', 'Nechat značku být')
            v = input("> ").strip()
            if v == "1":
                nalezeno = random.randint(40, 90)
                hra.hrac.gold += nalezeno
                tisk_ok(f"V tajné schránce byla brašna s {nalezeno} 🪙 a drahokam!")
                if "syndikat_stinu" in hra.frakce.frakce:
                    hra.frakce.frakce["syndikat_stinu"].zmenit(3)

        try:
            input("Enter...")
        except EOFError:
            pass

    def pruzkum_lokace(self, hra):
        """Prozkoumá okolí aktuální lokace."""
        cena = 5
        if hra.hrac.sex_energy < cena and hra.hrac.dark_energy < cena:
            tisk_chyba(f"Na důkladný průzkum potřebuješ alespoň {cena} energie.")
            try:
                input("Enter...")
            except EOFError:
                pass
            return

        if hra.hrac.sex_energy >= cena:
            hra.hrac.sex_energy -= cena
        else:
            hra.hrac.dark_energy -= cena

        clear()
        info = LOKACE[self.aktualni_lokace]
        print(f"{MAGENTA}--- Průzkum okolí: {info['nazev']} ---{NC}\n")

        roll = random.random()
        if roll < 0.35:
            nalezeno = random.randint(25, 70)
            hra.hrac.gold += nalezeno
            tisk_ok(f"Ve skryté truhle u opuštěné zdi jsi našel {nalezeno} 🪙!")
            try:
                from game.kronika import zaznamenej
                zaznamenej(hra, f"Průzkum v {info['nazev']}: nalezeno {nalezeno} zlata.")
            except Exception:
                pass
        elif roll < 0.70:
            suroviny = ["bylina_mesicni", "nocni_stin", "vzacna_houba", "krystal_sily"]
            sur = random.choice(suroviny)
            if hasattr(hra, "alchymie"):
                hra.alchymie.pridat_surovinu(sur, 1)
            tisk_ok(f"Při prohledávání houštin jsi nalezl vzácnou surovinu: {sur.replace('_', ' ').capitalize()}!")
        else:
            # Šance na odhalení skryté sousední lokace
            zamcene_sousede = [
                s for s in info["sousedni"] if s not in self.odhalene_lokace
            ]
            if zamcene_sousede:
                nova_lok = random.choice(zamcene_sousede)
                self.odhal_lokaci(nova_lok)
                tisk_ok(f"★ ÚSPĚCH! Narazil jsi na skrytou stezku a odhalil lokaci: {LOKACE[nova_lok]['nazev']}!")
                try:
                    from game.kronika import zaznamenej
                    zaznamenej(hra, f"Průzkumem odhalena nová lokace: {LOKACE[nova_lok]['nazev']}.")
                except Exception:
                    pass
            else:
                tisk_info("Okolí je důkladně zmapované. Nalezl jsi pár starých mincí (+15 🪙).")
                hra.hrac.gold += 15

        try:
            input("Enter...")
        except EOFError:
            pass

    def cestuj(self, cil, hra=None):
        if cil not in LOKACE or cil not in self.odhalene_lokace:
            tisk_chyba("Tato lokace zatím není dostupná.")
            return False
        if cil != self.aktualni_lokace and cil not in LOKACE[self.aktualni_lokace]["sousedni"]:
            tisk_chyba("Z této lokace tam nevede přímá stezka.")
            return False
        if cil != self.aktualni_lokace and hra is not None:
            self._generuj_cestovni_udalost(cil, hra)
        self.aktualni_lokace = cil
        self.navstiveno[cil] = self.navstiveno.get(cil, 0) + 1
        tisk_ok(f"Dorazil jsi do lokace: {LOKACE[cil]['nazev']}.")
        return True

    def pouzij_nastroj(self, hra):
        """Použije průzkumný předmět na mapě a odhalí novou možnost."""
        inventar = hra.hrac.inventar
        dostupne = [
            predmet_id for predmet_id in (
                "lucerna_soumraku", "mesicni_kompas", "mapa_hvezd",
                "klic_observatore", "tajny_vzkaz", "pecet_svedka",
                "krvavy_ametyst",
            )
            if inventar.pocet_predmetu(predmet_id)
        ]
        if not dostupne:
            tisk_info("Nemáš žádný průzkumný nástroj.")
            return
        print("Průzkumné nástroje:")
        for index, predmet_id in enumerate(dostupne, 1):
            print(f"{index}) {PREDMETY[predmet_id]['nazev']}")
        print("0) Zpět")
        try:
            volba = input("> ").strip()
            if volba == "0":
                return
            predmet_id = dostupne[int(volba) - 1]
        except (ValueError, IndexError):
            tisk_chyba("Neplatná volba.")
            return

        sousedi = [
            lokace for lokace in LOKACE[self.aktualni_lokace]["sousedni"]
            if lokace not in self.odhalene_lokace
        ]
        potrebuje_stezku = predmet_id in {"lucerna_soumraku", "mesicni_kompas", "mapa_hvezd"}
        if potrebuje_stezku and not sousedi:
            tisk_info("V okolí už nejsou žádné neodhalené stezky.")
            return
        if not inventar.odeber_predmet(predmet_id):
            tisk_chyba("Nástroj už není v inventáři.")
            return
        nova_lokace = None
        if potrebuje_stezku:
            pocet = 2 if predmet_id == "mapa_hvezd" else 1
            odhalene = random.sample(sousedi, min(pocet, len(sousedi)))
            for nova_lokace in odhalene:
                self.odhal_lokaci(nova_lokace)
            lokace_text = ", ".join(LOKACE[lokace]["nazev"] for lokace in odhalene)
        if predmet_id == "lucerna_soumraku":
            hra.hrac.sex_energy = min(hra.hrac.max_sex(), hra.hrac.sex_energy + 5)
            zprava = f"Lucerna odhalila skrytou stezku ({lokace_text}) a obnovila 5 sexuální energie."
        elif predmet_id == "mesicni_kompas":
            hra.hrac.dark_energy = min(hra.hrac.max_temno(), hra.hrac.dark_energy + 5)
            zprava = f"Měsíční kompas určil bezpečný směr ({lokace_text}) a obnovil 5 temné energie."
        elif predmet_id == "mapa_hvezd":
            hra.hrac.reputace_mesta = min(100, hra.hrac.reputace_mesta + 4)
            zprava = f"Mapa hvězd odhalila nové cesty ({lokace_text}); reputace města +4."
        elif predmet_id == "klic_observatore":
            self.odhal_lokaci("zricenina_astralni_veze")
            hra.hrac.dark_energy = min(hra.hrac.max_temno(), hra.hrac.dark_energy + 10)
            zprava = "Klíč observatoře otevřel astrální věž; temná energie +10."
        elif predmet_id == "tajny_vzkaz":
            hra.frakce.frakce["syndikat_stinu"].zmenit(8)
            hra.frakce.frakce["obchodnici"].zmenit(3)
            zprava = "Tajný vzkaz potvrdil spojenectví; reputace Syndikátu stínů +8."
        elif predmet_id == "pecet_svedka":
            hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 12)
            hra.frakce.frakce["cirkev"].zmenit(-5)
            zprava = "Pečeť svědka odhalila inkviziční korupci; vliv inkvizice -12."
        else:
            hra.hrac.dark_energy = min(hra.hrac.max_temno(), hra.hrac.dark_energy + 15)
            hra.frakce.frakce["kult_krve"].zmenit(5)
            zprava = "Krvavý ametyst byl obětován v rituálu; temná energie +15."
        tisk_ok(zprava)
        from game.kronika import zaznamenej
        zaznamenej(hra, f"Použit předmět na mapě: {PREDMETY[predmet_id]['nazev']}.")
        if hasattr(hra, "achievementy"):
            hra.achievementy.zaznamenej("mapove_nastroje")

    def npc_v_lokaci(self):
        return [
            (npc_id, data) for npc_id, data in NPC.items()
            if data["lokace"] == self.aktualni_lokace
        ]

    def to_dict(self):
        return {
            "aktualni_lokace": self.aktualni_lokace,
            "odhalene_lokace": self.odhalene_lokace,
            "navstiveno": self.navstiveno,
            "vztahy_npc": self.vztahy_npc,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(
            aktualni_lokace=data.get("aktualni_lokace", "pevnost"),
            odhalene_lokace=data.get("odhalene_lokace", VYCHOZI_ODHALENE),
            navstiveno=data.get("navstiveno", {}) if isinstance(data.get("navstiveno", {}), dict) else {},
            vztahy_npc=data.get("vztahy_npc", {}) if isinstance(data.get("vztahy_npc", {}), dict) else {},
        )

    def menu(self, hra):
        while True:
            clear()
            self.vykresli_ascii_mapu(hra)
            lokace = LOKACE[self.aktualni_lokace]
            ikona = lokace.get('ikona', '📍')
            nebezpeci_barva = {
                "bezpečno": GREEN, "nízké": CYAN, "střední": YELLOW, "vysoké": RED
            }.get(lokace.get('nebezpeci', 'střední'), YELLOW)

            # ── Lokace info box ────────────────────────────────────────────
            W = 72
            print(f"{GOLD}{BOLD}╔{'═'*W}╗{NC}")
            nazev_line = f"  {ikona}  {lokace['nazev'].upper()}  {ikona}"
            pad = W - 2 - len(nazev_line)
            print(f"{GOLD}{BOLD}║{NC}{BOLD}{WHITE}{nazev_line}{' '*pad}{GOLD}{BOLD}║{NC}")
            print(f"{GOLD}{BOLD}╠{'═'*W}╣{NC}")
            popis = lokace['popis']
            print(f"{GOLD}{BOLD}║{NC}  {DIM}{popis[:W-4]}{NC}{' '*max(0,W-4-len(popis[:W-4]))}{GOLD}{BOLD}  ║{NC}")
            neb = lokace.get('nebezpeci', 'střední')
            neb_line = f"Nebezpečí: {neb}"
            # Mafie status
            mafie_stav = "Neutrální"
            if hasattr(hra, "mafie") and hasattr(hra.mafie, "uzemi"):
                for u in getattr(hra.mafie, "uzemi", []):
                    if getattr(u, "obsazeno", False) and (
                        u.nazev.lower() in lokace["nazev"].lower() or self.aktualni_lokace in u.nazev.lower()
                    ):
                        mafie_stav = f"Tvé teritorium ({u.kontrola}%)"
                        break
            status_line = f"{nebezpeci_barva}⚠ {neb_line}{NC}   🏴 {mafie_stav}"
            print(f"{GOLD}{BOLD}║{NC}  {status_line}{GOLD}{BOLD}{'':>{W-4-len(neb_line)-len(mafie_stav)-8}}║{NC}")
            print(f"{GOLD}{BOLD}╚{'═'*W}╝{NC}")
            print()

            # Dostupné cesty
            dostupne = [
                cil for cil in lokace["sousedni"]
                if cil in self.odhalene_lokace
            ]
            print(f"{CYAN}{BOLD}  🗺  Dostupné stezky:{NC}")
            for index, cil in enumerate(dostupne, 1):
                c_info = LOKACE[cil]
                neb_c = c_info.get('nebezpeci', 'střední')
                nb_barva = {
                    "bezpečno": GREEN, "nízké": CYAN, "střední": YELLOW, "vysoké": RED
                }.get(neb_c, YELLOW)
                print(f"  {BOLD}{CYAN}{index}){NC} {c_info.get('ikona','•')} {c_info['nazev']}  {nb_barva}[{neb_c}]{NC}")

            # NPC v okolí
            npc_v_lokaci = self.npc_v_lokaci()
            if npc_v_lokaci:
                print(f"\n{MAGENTA}{BOLD}  👤 Postavy v okolí:{NC}")
                for npc_id, npc in npc_v_lokaci:
                    vek = f", {npc['vek']} let" if npc.get("vek") else ""
                    vztah = self.vztahy_npc[npc_id]
                    rel_barva = GREEN if vztah >= 0 else RED
                    print(f"  {MAGENTA}•{NC} {npc['jmeno']}{vek}  {rel_barva}(vztah {vztah:+d}){NC}")

            extra_prompt = ""
            if self.aktualni_lokace == "cervena_ctvrt":
                extra_prompt = f"  {MAGENTA}B) 🌹 Nevěstinec{NC}  |"
            print()
            print(f"  {GREEN}{BOLD}1-{len(dostupne)}){NC} Cestovat"
                  f"  |  {GOLD}A){NC} ⚡ Akce lokace"
                  f"  |  {YELLOW}P){NC} Průzkum"
                  f"  |  {BLUE}L){NC} Nástroj"
                  f"  |  {MAGENTA}N){NC} Rozhovor s NPC"
                  f"  |  {CYAN}E){NC} Energie"
                  f"  |  {extra_prompt}"
                  f"  {RED}0){NC} Zpět")
            volba = input(f"\n{BOLD}>{NC} ").strip().lower()

            if volba == "0":
                return
            if volba == "a":
                self.menu_lokacni_akce(hra)
                continue
            if volba == "b" and self.aktualni_lokace == "cervena_ctvrt":
                from game.nevestinec import menu_nevestinec
                menu_nevestinec(hra)
                continue
            if volba == "p":
                self.pruzkum_lokace(hra)
                continue
            if volba == "l":
                self.pouzij_nastroj(hra)
                input("Enter...")
                continue
            if volba == "n":
                self.menu_npc(hra)
                continue
            if volba == "e":
                from game.energie import zobraz_menu as menu_energie
                menu_energie(hra)
                continue

            try:
                index = int(volba) - 1
                if 0 <= index < len(dostupne):
                    self.cestuj(dostupne[index], hra)
                    input("Enter...")
                else:
                    tisk_chyba("Špatná volba cíle.")
                    input("Enter...")
            except ValueError:
                tisk_chyba("Neplatná volba.")
                input("Enter...")

    def menu_npc(self, hra):
        npc_v_lokaci = self.npc_v_lokaci()
        if not npc_v_lokaci:
            tisk_info("V této lokaci nikoho známého nenajdeš.")
            input("Enter...")
            return
        print()
        for index, (npc_id, npc) in enumerate(npc_v_lokaci, 1):
            vek = f", {npc['vek']} let" if npc.get("vek") else ""
            print(f"{index}) {npc['jmeno']} (vztah {self.vztahy_npc[npc_id]:+d}{vek})")
        vytiskni_volbu('0', 'Zpět')
        try:
            index = int(input("> ")) - 1
        except ValueError:
            tisk_chyba("Zadej číslo.")
            input("Enter...")
            return
        if index < 0:
            return
        if index >= len(npc_v_lokaci):
            tisk_chyba("Špatná volba.")
            input("Enter...")
            return
        npc_id, npc = npc_v_lokaci[index]
        print(f"\n{npc['jmeno']}: {npc['popis']}")
        vytiskni_volbu('1', '📜 Příběhový rozhovor & Větvení příběhu')
        vytiskni_volbu('2', '🤝 Požádat o službu')
        vytiskni_volbu('3', '⚒️ Nabídnout pomoc')
        stav_ukolu, quest = hra.npc_questy.stav_pro_npc(hra, npc_id)
        if stav_ukolu == "aktivni":
            vytiskni_volbu('4', f"🎯 Dokončit úkol: {quest['nazev']}")
        elif stav_ukolu == "dostupny":
            vytiskni_volbu('4', f"🎯 Přijmout úkol: {quest['nazev']}")
        vytiskni_volbu('0', 'Zpět')
        akce = input("> ").strip()
        vztah = self.vztahy_npc[npc_id]

        if akce == "0":
            return
        elif akce == "1":
            self.pribehovy_rozhovor(npc_id, npc, hra)
            return

        elif akce == "4":
            stav_ukolu, quest = hra.npc_questy.stav_pro_npc(hra, npc_id)
            if stav_ukolu == "dostupny":
                if hra.npc_questy.prijmi(hra, npc_id):
                    tisk_ok(f"Přijal jsi úkol «{quest['nazev']}».")
                    print(quest["popis"])
                else:
                    tisk_chyba("Tento úkol už není dostupný.")
            elif stav_ukolu == "aktivni":
                print(f"\nAktivní úkol: {quest['nazev']}")
                print(quest["popis"])
                print("1) Vyřešit čestně")
                print("2) Vyřešit temnou cestou")
                vetev = input("> ").strip()
                if vetev in ("1", "2"):
                    vysledek = hra.npc_questy.dokoncit(
                        hra, npc_id, temna=vetev == "2"
                    )
                    tisk_ok(
                        "Úkol dokončen: "
                        + ("temná větev." if vysledek == "temna" else "čestná větev.")
                    )
                else:
                    tisk_chyba("Úkol zůstává aktivní.")
            else:
                tisk_info("Tento NPC ti zatím žádný úkol nenabízí.")
            input("Enter...")
            return

        elif akce == "2":
            if npc_id == "mira":
                hra.hrac.hp = min(hra.hrac.max_hp, hra.hrac.hp + 25)
                self.zmen_vztah(npc_id, 3)
                tisk_ok("Mira tě ošetřila. HP +25, vztah +3.")
            elif npc_id == "radan":
                hra.alchymie.pridat_surovinu("nocni_stin", 1)
                self.zmen_vztah(npc_id, 3)
                tisk_ok("Radan ti předal Noční stín. Vztah +3.")
            elif npc_id == "elian":
                hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 3)
                self.zmen_vztah(npc_id, 3)
                tisk_ok("Elian odvedl pozornost stráží. Vliv inkvizice -3.")
            elif npc_id == "borin":
                from game.energie import hostinec
                if hostinec(hra):
                    self.zmen_vztah(npc_id, 3)
            elif npc_id == "velena":
                from game.energie import lazne
                if lazne(hra):
                    self.zmen_vztah(npc_id, 3)
            elif npc_id == "sava":
                from game.energie import meditace
                if meditace(hra):
                    self.zmen_vztah(npc_id, 3)
            elif npc_id == "nela":
                if hra.alchymie.pridat_surovinu("esence_temna", 1):
                    self.zmen_vztah(npc_id, 3)
                    tisk_ok("Nela ti svěřila lahvičku temné esence. Vztah +3.")
                else:
                    tisk_chyba("Nela dnes nemá vhodnou surovinu.")
            elif npc_id == "lyra":
                from game.energie import zahrada
                if zahrada(hra):
                    self.zmen_vztah(npc_id, 4)
            elif npc_id == "cassian":
                if hra.hrac.dark_energy < 10:
                    tisk_chyba("Cassian žádá nejdřív důkaz, že zvládneš soustředění.")
                else:
                    hra.hrac.dark_energy -= 10
                    self.odhal_lokaci("molo_mesicniho_pristavu")
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Cassian ti otevřel hvězdný archiv. Molo Měsíčního přístavu je na mapě.")
            elif npc_id == "tereza":
                hra.hrac.sex_energy = min(100, hra.hrac.sex_energy + 12)
                hra.hrac.reputace_mesta += 2
                self.zmen_vztah(npc_id, 4)
                tisk_ok("Tereza s tebou sdílela klidnou směnu na molu. Energie +12, reputace +2.")
            elif npc_id == "mortis":
                hra.hrac.dark_energy = min(
                    hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 120,
                    hra.hrac.dark_energy + 20
                )
                self.zmen_vztah(npc_id, 4)
                tisk_ok("Mortis ti odhalil tajemství hrobek. Temná energie +20, vztah +4.")
            elif npc_id == "morana":
                if hasattr(hra, "alchymie"):
                    hra.alchymie.pridat_surovinu("esence_temna", 1)
                self.zmen_vztah(npc_id, 5)
                tisk_ok("Morana ti předala rituální temnou esenci svatyně. Vztah +5.")
            elif npc_id == "lord_vane":
                if hra.hrac.gold >= 100:
                    hra.hrac.gold -= 100
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 12)
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Lord Vane přiměl městskou radu odvolat inkviziční komisi. Inkvizice -12.")
                else:
                    tisk_chyba("Lord Vane nehne prstem za méně než 100 🪙.")
            elif npc_id == "madame_scarlett":
                self.zmen_vztah(npc_id, 4)
                if hasattr(hra, "nevestinec"):
                    hra.nevestinec.reputace_podniku += 3
                tisk_ok("Madame Scarlett se podělila o tipy na bohaté zákazníky. Reputace nevěstince +3, vztah +4.")
            elif npc_id == "baron_archibald":
                if hra.hrac.sex_energy >= 10:
                    hra.hrac.sex_energy -= 10
                    hra.hrac.gold += 80
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Baron Archibald ti zaplatil 80 🪙 za exkluzivní doporučení tvých společnic!")
                else:
                    tisk_chyba("Baron Archibald tě nepřijme bez patřičné energie a vystupování.")
            elif npc_id == "gladiator_gor":
                if hra.hrac.gold >= 40:
                    hra.hrac.gold -= 40
                    hra.hrac.hp = min(hra.hrac.max_hp + 5, hra.hrac.hp + 20)
                    hra.hrac.max_hp += 2
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Gor tě naučil arénové triky přežití. Max HP +2, vztah +5.")
                else:
                    tisk_chyba("Gor požaduje za arénový trénink 40 🪙.")
            elif npc_id == "lady_eleanor":
                if "syndikat_stinu" in hra.frakce.frakce:
                    hra.frakce.frakce["syndikat_stinu"].zmenit(4)
                hra.hrac.reputace_mesta += 3
                self.zmen_vztah(npc_id, 4)
                tisk_ok("Lady Eleanor využila svůj vliv u dvora ve tvůj prospěch. Reputace +3, vztah +4.")
            elif npc_id == "vladyka_aurelius":
                if hra.hrac.gold >= 70:
                    hra.hrac.gold -= 70
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 15)
                    self.zmen_vztah(npc_id, 5)
                    if "cirkev" in hra.frakce.frakce:
                        hra.frakce.frakce["cirkev"].zmenit(8)
                    tisk_ok("Velekněz Aurelius ti udělil oficiální inkviziční odpustek! Vliv inkvizice -15, vztah církve +8.")
                else:
                    tisk_chyba("Velekněz požaduje dar chrámu ve výši 70 🪙.")
            elif npc_id == "stinovy_mistr_kage":
                if hra.hrac.dark_energy >= 12:
                    hra.hrac.dark_energy -= 12
                    hra.hrac.gold += 95
                    self.zmen_vztah(npc_id, 5)
                    if "syndikat_stinu" in hra.frakce.frakce:
                        hra.frakce.frakce["syndikat_stinu"].zmenit(8)
                    tisk_ok("Mistr Kage ti vyplatil 95 🪙 za spolupráci na podsvětní zakázce. Reputace Syndikátu +8.")
                else:
                    tisk_chyba("Kage vyžaduje 12 bodů temné energie k zapojení do stínové operace.")
            elif npc_id == "knezka_valeria":
                max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
                hra.hrac.sex_energy = min(max_s, hra.hrac.sex_energy + 15)
                self.zmen_vztah(npc_id, 4)
                for marriage in getattr(hra, "marriage_system", {}).values():
                    if hasattr(marriage, "zmen_zarlivost"):
                        marriage.zmen_zarlivost(-10)
                        marriage.zmen_spokojenost(10)
                tisk_ok("Valeria tě pohostila jasmínovým čajem v altánu. Energie +15, žárlivost všech manželek -10%!")
            elif npc_id == "inkvizitor_malor":
                if hra.hrac.gold >= 80:
                    hra.hrac.gold -= 80
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 16)
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Inkvizitor Malor přijal tučný dar pro inkvizici. Vliv inkvizice -16.")
                else:
                    tisk_chyba("Malor vyžaduje alespoň 80 🪙.")
            elif npc_id == "vespera":
                if hra.hrac.dark_energy >= 10:
                    hra.hrac.dark_energy -= 10
                    if hasattr(hra, "alchymie"):
                        hra.alchymie.pridat_surovinu("esence_temna", 2)
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Vespera zkoncentrovala svou magii a vytvořila 2 esence temna. Vztah +5.")
                else:
                    tisk_chyba("Potřebuješ alespoň 10 temné energie pro rezonanci s Vesperou.")
            elif npc_id == "selene":
                if hra.hrac.gold >= 50:
                    hra.hrac.gold -= 50
                    max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
                    max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
                    hra.hrac.sex_energy = max_s
                    hra.hrac.dark_energy = max_t
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Selene provedla astrální očištění tvé aury. Veškerá energie plně obnovena!")
                else:
                    tisk_chyba("Rituál vědmy Selene vyžaduje dar 50 🪙.")
            elif npc_id == "kapitanka_drake":
                if hra.hrac.gold >= 60:
                    hra.hrac.gold -= 60
                    if hasattr(hra, "pevnost"):
                        hra.pevnost.drevo += 40
                        hra.pevnost.zelezo += 20
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Kapitánka Drake ti předala pašovaný náklad z moře (+40 dřeva, +20 železa pro pevnost)!")
                else:
                    tisk_chyba("Drake za méně než 60 🪙 loď neotevře.")
            elif npc_id == "dozorce_krag":
                if hra.hrac.gold >= 45:
                    hra.hrac.gold -= 45
                    if hasattr(hra, "pevnost"):
                        hra.pevnost.kamen += 60
                    self.zmen_vztah(npc_id, 5)
                    tisk_ok("Dozorce Krag vypravil povoz s těžkým kamenem do tvého dominia (+60 kamene)!")
                else:
                    tisk_chyba("Krag požaduje 45 🪙 za povoz kamene.")

        elif akce == "3":
            if vztah < -20:
                self.zmen_vztah(npc_id, -4)
                tisk_chyba("NPC ti nevěří a nabídku odmítl.")
            else:
                if npc_id == "sava":
                    hra.alchymie.pridat_surovinu("nocni_stin", 1)
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi Savě očistit háj. Získal jsi Noční stín, vztah +6.")
                elif npc_id == "nela":
                    hra.hrac.gold += 35
                    hra.alchymie.pridat_surovinu("koren_mandragory", 1)
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi Nele s destilací. Získal jsi 35 zlata a kořen mandragory.")
                elif npc_id == "morana":
                    hra.hrac.dark_energy = min(
                        hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 120,
                        hra.hrac.dark_energy + 15
                    )
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Společný rituál s Moranou proběhl úspěšně. Temná energie +15.")
                elif npc_id == "inkvizitor_malor":
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 5)
                    self.zmen_vztah(npc_id, 6)
                    hra.hrac.gold += 40
                    tisk_ok("Předal jsi Malorovi hlášení o podezřelých kupcích. Vztah +6, +40 🪙, inkvizice -5.")
                elif npc_id == "vespera":
                    if hra.hrac.gold >= 15:
                        hra.hrac.gold -= 15
                        self.zmen_vztah(npc_id, 8)
                        tisk_ok("Podplatil jsi strážného, aby Vesperu nakrmil a uvolnil jí okovy. Vespera ti vděčně hledí do očí (+8 vztah).")
                    else:
                        tisk_chyba("Nemáš ani 15 🪙 na podplacení stráže.")
                elif npc_id == "selene":
                    if hasattr(hra, "pevnost"):
                        hra.pevnost.krystaly += 2
                    self.zmen_vztah(npc_id, 7)
                    tisk_ok("Pomohl jsi Selene uspořádat astrální krystaly. Získal jsi 2 krystaly do pevnosti, vztah +7.")
                elif npc_id == "kapitanka_drake":
                    hra.hrac.gold += 45
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi Drake zabezpečit náklad v zátoce. Získal jsi 45 🪙 a vztah +6.")
                elif npc_id == "dozorce_krag":
                    hra.hrac.gold += 40
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi Kragovi zkrotit neposlušné lamače kamene. Získal jsi 40 🪙 a vztah +6.")
                else:
                    hra.hrac.gold += 30
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi NPC s její prací. Získal jsi 30 zlata, vztah +6.")
        else:
            tisk_chyba("Neplatná volba.")
        input("Enter...")

    def pribehovy_rozhovor(self, npc_id, npc, hra):
        """Interaktivní příběhový dialog s větvením a volbami pro klíčová NPC."""
        clear()
        vztah = self.vztahy_npc[npc_id]
        hlavicka(f"Příběh: {npc['jmeno']}")
        print(f"\n{DIM}{npc['popis']}{NC}")
        print(f"{CYAN}Vztah: {vztah:+d} | Tvá temná energie: {hra.hrac.dark_energy} | Zlato: {hra.hrac.gold} 🪙{NC}\n")

        if npc_id == "vespera":
            print(f"{MAGENTA}Vespera sedí na chladné kamenné zemi cely inkvizičního žaláře.{NC}")
            print(f"Její tělo je spoutáno okovy z černého železa, ale ve fialových očích stále plane divoký oheň.")
            print(f"„Přišel jsi se dívat na kacířku v řetězech, pane? Nebo tě zajímá moc, které se kněží tolik bojí?“\n")
            print(f"  {BOLD}1){NC} „Jsem pánem Černé pevnosti. Přišel jsem ti nabídnout svobodu a moc v mém harému.“")
            print(f"  {BOLD}2){NC} „Pověz mi o prastaré magii stínů, kterou tě církev nutila zapomenout.“")
            print(f"  {BOLD}3){NC} „Tvá pýcha je působivá. Až tě zlomím, budeš nejoddanějším klenotem mého dominia.“")
            print(f"  {BOLD}0){NC} Odejít")
            v = input("\n> ").strip()
            if v == "1":
                # Osvobození Vespery do harému
                if any(o.jmeno == "Vespera" for o in hra.harem.otrokyne):
                    tisk_info("Vespera už byla z těchto cel osvobozena a přebývá v tvém dominiu.")
                else:
                    ma_zlato = (hra.hrac.gold >= 40)
                    ma_temno = (hra.hrac.dark_energy >= 12)
                    if ma_zlato or ma_temno:
                        if ma_temno:
                            hra.hrac.dark_energy -= 12
                            print(f"\n{MAGENTA}Vztáhl jsi ruku k okovům a nechal skrze ně proudit temnou energii.{NC}")
                            print(f"Železo s hlasitým prasknutím puklo. Okovy s řinčením padají na zem.")
                        else:
                            hra.hrac.gold -= 40
                            print(f"\n{GOLD}Podplatil jsi inkvizičního strážného 40 zlaťáky a ten ti v tichosti předal klíč.{NC}")
                        from models.otrokyne import Otrokyně
                        nova = Otrokyně(
                            jmeno="Vespera",
                            vek=23,
                            charakter="carodejka",
                            poslusnost=70,
                            loajalita=80,
                            touha=65,
                            vlhkost=50,
                        )
                        nova.popis = "Hrdá čarodějka stínu osvobozená z inkvizičního žaláře."
                        hra.harem.pridat(nova)
                        self.zmen_vztah(npc_id, 25)
                        tisk_ok("★ ÚSPĚCH! Vespera byla osvobozena a vděčně se připojila k tvému harému jako mocná čarodějka!")
                        if hasattr(hra, "kronika"):
                            from game.kronika import zaznamenej
                            zaznamenej(hra, "Inkviziční žalář: osvobozena čarodějka Vespera do harému dominia.")
                    else:
                        tisk_chyba("K prolomení jejích okovů potřebuješ buď 40 🪙 na úplatek, nebo 12 temné energie!")
            elif v == "2":
                hra.hrac.dark_energy = min(
                    hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 120,
                    hra.hrac.dark_energy + 25
                )
                if hasattr(hra, "pevnost"):
                    hra.pevnost.krystaly += 2
                self.zmen_vztah(npc_id, 8)
                print(f"\n{MAGENTA}Vespera ti zašeptala starobylou formuli zapomenutého stínového kruhu.{NC}")
                tisk_ok("Získal jsi +25 temné energie a 2 temné krystaly pro pevnost!")
            elif v == "3":
                self.zmen_vztah(npc_id, 4)
                print(f"\n{RED}Vespera zatne zuby, ale v očích se jí mihne záblesk podrobení a respektu.{NC}")
                print(f"„Mnozí se o to pokoušeli, pane... ale tvůj pohled má váhu, kterou nelze ignorovat.“")

        elif npc_id == "selene":
            print(f"{CYAN}Vědma Selene levituje nad astrálním kruhem rozpadlé citadely.{NC}")
            print(f"Kolem ní krouží stříbřité runy a v prastarých zrcadlech se odrážejí hvězdy.")
            print(f"„Vítej, stínový vládce. Osud tvého dominia byl vepsán do hvězd dávno před pádem říše.“\n")
            print(f"  {BOLD}1){NC} „Pověz mi o budoucnosti mého harému a harmonii mých manželek.“")
            print(f"  {BOLD}2){NC} „Přišel jsem probudit spící sílu své duše.“ (stojí 20 temné energie)")
            print(f"  {BOLD}3){NC} „Hledám prastaré obranné runy pro hradby své pevnosti.“")
            print(f"  {BOLD}0){NC} Odejít")
            v = input("\n> ").strip()
            if v == "1":
                self.zmen_vztah(npc_id, 8)
                for marriage in getattr(hra, "marriage_system", {}).values():
                    if hasattr(marriage, "zmen_zarlivost"):
                        marriage.zmen_zarlivost(-20)
                        marriage.zmen_spokojenost(15)
                for o in hra.harem.vsechny_aktivni():
                    o.loajalita = min(100, o.loajalita + 6)
                tisk_ok("Astrální věštba vnesla klid do tvého harému. Žárlivost manželek klesla o 20 %, loajalita vzrostla!")
            elif v == "2":
                if hra.hrac.dark_energy >= 20:
                    hra.hrac.dark_energy -= 20
                    hra.hrac.max_hp += 5
                    hra.hrac.hp = min(hra.hrac.max_hp, hra.hrac.hp + 20)
                    if hasattr(hra.hrac, "max_sex_energy"):
                        hra.hrac.max_sex_energy += 10
                    self.zmen_vztah(npc_id, 10)
                    tisk_ok("★ ASTRÁLNÍ PROBUZENÍ! Tvé tělo zaplavil kosmický žár: trvale +5 Max HP a +10 Max energie!")
                    if hasattr(hra, "kronika"):
                        from game.kronika import zaznamenej
                        zaznamenej(hra, "Astrální citadela: Selene posvětila tvou duši astrálním probuzením.")
                else:
                    tisk_chyba("K astrálnímu probuzení potřebuješ alespoň 20 temné energie!")
            elif v == "3":
                if hasattr(hra, "pevnost"):
                    hra.pevnost.krystaly += 4
                    hra.pevnost.kamen += 50
                self.zmen_vztah(npc_id, 8)
                tisk_ok("Selene ti předala prastaré runové nákresy: +4 temné krystaly a +50 kamene pro pevnost!")

        elif npc_id == "kapitanka_drake":
            print(f"{YELLOW}Kapitánka Drake sedí na sudu rumu u mola Zátoky vraků a brousí si šavli.{NC}")
            print(f"Její loď Černá harpyje v zátoce tiše pohupuje stěžněm v ranní mlze.")
            print(f"„Co tě sem vede, pane z kamenné pevnosti? Hledáš mořskou kořist, černý trh, nebo dívku do kajuty?“\n")
            print(f"  {BOLD}1){NC} „Vyplujme na noční přepad kupecké galeony!“ (vyžaduje bojeschopnost)")
            print(f"  {BOLD}2){NC} „Odkoupím z tvého podpalubí cizokrajnou zajatkyni.“ (stojí 90 🪙)")
            print(f"  {BOLD}3){NC} „Potřebuji pirátskou ochranu pro své obchodní karavany.“")
            print(f"  {BOLD}0){NC} Odejít")
            v = input("\n> ").strip()
            if v == "1":
                if hra.hrac.hp > 25:
                    hra.hrac.hp -= 12
                    korist_zlato = random.randint(75, 140)
                    hra.hrac.gold += korist_zlato
                    if hasattr(hra, "pevnost"):
                        hra.pevnost.drevo += 35
                        hra.pevnost.zelezo += 20
                    self.zmen_vztah(npc_id, 8)
                    tisk_ok(f"✔ VÍTĚZNÁ RAZIE! Přepadli jste kupeckou loď. Zisk: +{korist_zlato} 🪙, +35 dřeva a +20 železa pro pevnost!")
                else:
                    tisk_chyba("Jsi příliš zraněný na námořní bitvu!")
            elif v == "2":
                if hra.hrac.gold >= 90:
                    hra.hrac.gold -= 90
                    from models.otrokyne import Otrokyně
                    from data.jmena import JMENA
                    jmeno = random.choice(JMENA)
                    nova = Otrokyně(
                        jmeno=jmeno,
                        vek=random.randint(19, 25),
                        charakter="zlodejka",
                        poslusnost=65,
                        loajalita=65,
                        touha=70,
                        vlhkost=60,
                    )
                    nova.popis = "Exotická pirátská zajatkyně z jižních ostrovů, mrštná a smyslná."
                    hra.harem.pridat(nova)
                    self.zmen_vztah(npc_id, 10)
                    tisk_ok(f"★ Z podpalubí byla vyvedena {jmeno}. S vděčností a zvědavostí vstupuje do tvého harému!")
                else:
                    tisk_chyba("Kapitánka Drake neprodá zajatkyni pod 90 🪙.")
            elif v == "3":
                self.zmen_vztah(npc_id, 6)
                if hasattr(hra, "pevnost"):
                    hra.pevnost.zasoby += 20
                tisk_ok("Drake uzavřela dohodu. Karavany v zátoce mají volný průjezd (+20 zásob jídla)!")

        elif npc_id == "inkvizitor_malor":
            print(f"{RED}Inkvizitor Malor si prohlíží železné kleště nad rozpálenou pánví.{NC}")
            print(f"Úzké škvíry jeho železné masky míří přímo do tvých očí.")
            print(f"„Zápach hříchu tě předchází, pane. Církev ví o tvém harému víc, než si myslíš.“\n")
            print(f"  {BOLD}1){NC} „Mám kompro materiály na městskou radu. Stáhni inkvizici, nebo padne i tvůj řád.“")
            print(f"  {BOLD}2){NC} „Má temná moc dalece převyšuje tvé plamínky. Ustup, dokud můžeš.“ (vyžaduje 18 temna)")
            print(f"  {BOLD}3){NC} „Nabízím štědrý dar inkvizici (70 🪙) jako projev dobré vůle.“")
            print(f"  {BOLD}0){NC} Odejít")
            v = input("\n> ").strip()
            if v == "1":
                hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 25)
                self.zmen_vztah(npc_id, 4)
                tisk_ok("Malor zatnul pěsti a ustoupil. Inkviziční komise odvolána! Vliv inkvizice -25.")
            elif v == "2":
                if hra.hrac.dark_energy >= 18:
                    hra.hrac.dark_energy -= 18
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 18)
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Tvá temná aura zastrašila i inkvizitora. Malor couvl v posvátné bázni! Inkvizice -18.")
                else:
                    tisk_chyba("Nemáš dostatek temné energie k zastrašení fanatického inkvizitora!")
            elif v == "3":
                if hra.hrac.gold >= 70:
                    hra.hrac.gold -= 70
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 15)
                    self.zmen_vztah(npc_id, 8)
                    tisk_ok("Malor přijal dar. Inkviziční vyšetřování pozastaveno (-15 vliv inkvizice).")
                else:
                    tisk_chyba("Nemáš 70 🪙 na úplatek.")

        elif npc_id == "dozorce_krag":
            print(f"{YELLOW}Vrchní dozorce Krag práskl karabáčem do kamenného bloku.{NC}")
            print(f"Z prachu lomů vystupují obrysy stovek pracujících v těžkých okovech.")
            print(f"„Co tě sem vede, pane? Tady se nekecá, tady se buď kope, nebo krvácí.“\n")
            print(f"  {BOLD}1){NC} „Pevnost dominia potřebuje masivní dodávku kamene a železa za panskou cenu.“")
            print(f"  {BOLD}2){NC} „Vykoupím zraněnou amazonku v okovech dřív, než v lomu padne.“ (stojí 85 🪙)")
            print(f"  {BOLD}3){NC} „Chci ukázat tvým dozorcům, jak má vypadat pravá disciplína.“")
            print(f"  {BOLD}0){NC} Odejít")
            v = input("\n> ").strip()
            if v == "1":
                if hra.hrac.gold >= 50:
                    hra.hrac.gold -= 50
                    if hasattr(hra, "pevnost"):
                        hra.pevnost.kamen += 80
                        hra.pevnost.zelezo += 40
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Výhodný obchod uzavřen! Pro tvou pevnost bylo naloženo +80 kamene a +40 železa!")
                else:
                    tisk_chyba("Potřebuješ alespoň 50 🪙.")
            elif v == "2":
                if hra.hrac.gold >= 85:
                    hra.hrac.gold -= 85
                    from models.otrokyne import Otrokyně
                    from data.jmena import JMENA
                    jmeno = random.choice(JMENA)
                    nova = Otrokyně(
                        jmeno=jmeno,
                        vek=random.randint(20, 26),
                        charakter="Amazonka (bojovnice)",
                        poslusnost=60,
                        loajalita=75,
                        hp=90,
                        max_hp=90,
                    )
                    nova.popis = "Hrdá válečnice vykoupená z krvavých lomů, vděčná za záchranu před smrtí."
                    hra.harem.pridat(nova)
                    self.zmen_vztah(npc_id, 8)
                    tisk_ok(f"★ Amazonka {jmeno} byla zbavena těžkých okovů a připojila se k tvému harému!")
                else:
                    tisk_chyba("Krag za méně než 85 🪙 otrokyni nepropustí.")
            elif v == "3":
                self.zmen_vztah(npc_id, 6)
                hra.hrac.reputace_mesta += 3
                tisk_ok("Dozorci uznávají tvou autoritu a respektují tvé dominium (+3 reputace města)!")

        else:
            # Obecný příběhový dialog s větvením pro ostatní NPC
            dialogy = npc.get("dialogy", ["Tvé dominium roste a město si o tobě šeptá."])
            print(f"„{dialogy[0]}“\n")
            print(f"  {BOLD}1){NC} Přátelsky a s úctou rozvinout hovor o dění v kraji (+vztah, +reputace)")
            print(f"  {BOLD}2){NC} Projevit temnou autoritu vládce dominia (+respekt, +temno)")
            print(f"  {BOLD}0){NC} Zpět")
            v = input("\n> ").strip()
            if v == "1":
                self.zmen_vztah(npc_id, 6)
                hra.hrac.reputace_mesta += 2
                tisk_ok(f"Rozhovor s {npc['jmeno']} prohloubil vaše porozumění (vztah +6, reputace +2).")
            elif v == "2":
                self.zmen_vztah(npc_id, 4)
                hra.hrac.dark_energy = min(
                    hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100,
                    hra.hrac.dark_energy + 8
                )
                tisk_ok(f"{npc['jmeno']} cítí tvou sílu a sklání hlavu (vztah +4, temná energie +8).")

        input("\nEnter...")

    def menu_lokacni_akce(self, hra):
        """Unikátní interaktivní akce podle aktuální lokace na mapě."""
        lok_id = self.aktualni_lokace
        info = LOKACE[lok_id]

        clear()
        hlavicka(f"⚡ AKCE LOKACE: {info['nazev'].upper()} ⚡")
        print(f"\n{DIM}{info['popis']}{NC}")
        print(f"{GOLD}Zlato: {hra.hrac.gold} 🪙{NC} | {CYAN}Sexuální energie: {hra.hrac.sex_energy}{NC} | {MAGENTA}Temná energie: {hra.hrac.dark_energy}{NC}")
        if hasattr(hra, "pevnost"):
            p = hra.pevnost
            print(f"{BOLD}Pevnost:{NC} 🪵 {p.drevo} | 🪨 {p.kamen} | ⚒️ {p.zelezo} | 🌾 {p.zasoby} | 🔮 {p.krystaly}\n")

        # Každá lokace má 2-3 své vlastní akce
        if lok_id == "pevnost":
            print("  1) 🛡️ Přehlídka posádky a posílení obranyschopnosti (+3 obrana)")
            print("  2) 🌾 Nákup proviantu do sýpek dominia (20 🪙 -> +25 zásob jídla)")
            print("  3) 👑 Shromáždění manželek a otrokyň na nádvoří (+loajalita harému)")
        elif lok_id == "trh":
            print("  1) 👂 Sledování zvěstí a tajemství mezi stánky (šance odhalit lokaci/kompro)")
            print("  2) 🎁 Nákup luxusních hedvábných látek pro harém (30 🪙 -> +spokojenost)")
            print("  3) 🪙 Rychlé kapsářství v rušném davu (zisk mincí, riziko poplachu)")
        elif lok_id == "les":
            print("  1) 🏹 Velký lov zvěře v Mlžném lese (+zásoby jídla a kožešiny pro pevnost)")
            print("  2) 🪵 Kácení a těžba dřeva pro pevnost (+35 dřeva)")
            print("  3) 🍄 Sběr alchymistických bylin a hub")
        elif lok_id == "krvavy_lom":
            print("  1) 🪨 Velkoobchodní nákup stavebního kamene (40 🪙 -> +70 kamene)")
            print("  2) ⚒️ Nákup surové železné rudy pro kovárnu (35 🪙 -> +40 železa)")
            print("  3) 💃 Odkup zocelené amazonky před popravou v lomu (110 🪙 -> nová otrokyně)")
        elif lok_id == "hranice":
            print("  1) ⚔️ Verbování pohraničních veteránů (55 🪙 -> +2 vojáci pro gardu)")
            print("  2) 🛡️ Posílení hraničních palisád (+4 obrana pevnosti, +5 reputace)")
            print("  3) 🪙 Obchod s kožešinami se severskými lovci (+45 🪙)")
        elif lok_id == "zricenina_astralni_veze":
            print("  1) 🔮 Koupel v astrálním zřídle vědmy Selene (40 🪙 -> obnova energie a léčení)")
            print("  2) 📜 Luštění hvězdných run starého impéria (+35 XP, +3 krystaly)")
            print("  3) 🌌 Rituální spojení duší s vybranou společnicí (+20 loajalita)")
        elif lok_id == "haj_soumraku":
            print("  1) 🧘 Hluboká meditace pod stromy soumraku (+18 temné energie)")
            print("  2) 🌿 Sběr nočních lilií pro lektvary a afrodiziaka")
        elif lok_id == "observator":
            print("  1) 🔭 Pozorování hvězdného orloje s Cassianem (odhalení skryté lokace)")
            print("  2) 📜 Studium prastarých hvězdných map (+30 XP)")
        elif lok_id == "svatyne_krvaveho_mesice":
            print("  1) 🩸 Krvavá oběť u oltáře Morany (-10 HP -> +35 temná energie)")
            print("  2) 🌑 Kletba na městskou inkvizici (-12 vliv inkvizice)")
        elif lok_id == "ctvrt_remeselniku":
            print("  1) 🔨 Zbrojířská zakázka na zbraně pro gardu pevnosti (50 🪙 -> +výzbroj)")
            print("  2) 💍 Klenotnická výroba ozdobných obojků (+submisivita pro dívky)")
            print("  3) ⚒️ Směna rudy za stavební nástroje (30 🪙 -> +25 železa)")
        elif lok_id == "lazne":
            print("  1) ♨️ Horká bylinná lázeň pro regeneraci těla (20 🪙 -> plné HP, +20 sex)")
            print("  2) 💋 Společná koupel s otrokyní (+15 touha a důvěra dívky)")
        elif lok_id == "sklenena_zahrada":
            print("  1) 🌺 Romantická procházka s dívkou mezi orchidejemi (+důvěra, -strach)")
            print("  2) 🌿 Sběr exotického nektaru pro výzkum a parfémy")
        elif lok_id == "stribrne_terasy":
            print("  1) 🏛️ Diplomatické vyjednávání s městskou šlechtou (+reputace města)")
            print("  2) 📜 Naslouchání aristokratickým intrikám (+kompro materiál)")
        elif lok_id == "zahradni_altan":
            print("  1) 🍵 Slavnostní čajový obřad manželek (žárlivost -15 %, harmonie v harému)")
            print("  2) 🌹 Soukromé rande v altánu u jezírka (+25 touha a intimita)")
        elif lok_id == "palac_bohatych":
            print("  1) 👑 Účast na šlechtickém plese a banketu (+vliv a navázání kontaktů)")
            print("  2) 🪙 Podplacení guvernérských úředníků (60 🪙 -> ochrana dominia)")
        elif lok_id == "cervena_ctvrt":
            print("  1) 🌹 Vstup do správy tvého nevěstince")
            print("  2) 💋 Průzkum uliček a hledání talentovaných dívek")
        elif lok_id == "pristav":
            print("  1) 📦 Zajištění lodní zásilky dřeva a železa (35 🪙 -> +30 dřeva, +15 železa)")
            print("  2) 🍺 Naslouchání příběhům cizích námořníků v krčmě")
        elif lok_id == "molo_mesicniho_pristavu":
            print("  1) 🌊 Noční rozjímání při šumění přílivu (+15 sexuální energie, +10 temné)")
            print("  2) 🔥 Signální oheň pro noční pašeráky (+40 🪙 provize)")
        elif lok_id == "paserska_zatoka":
            print("  1) 🏴‍☠️ Noční námořní razie s kapitánkou Drake (+kořist zlata a surovin)")
            print("  2) 💃 Odkup exotické zajatkyně z pirátského podpalubí (100 🪙 -> nová dívka)")
            print("  3) 🪙 Prodej kradených šperků překupníkům (+50 🪙)")
        elif lok_id == "podzemni_arena":
            print("  1) ⚔️ Vstoupit do arény a bojovat o sázky (okamžitý gladiátorský souboj)")
            print("  2) 🎲 Sázka na divokého bojovníka arény (vklad 20 🪙 -> šance na 50 🪙)")
        elif lok_id == "katakomby":
            print("  1) 💀 Vykrádání hrobek starých králů (riziko souboje vs cenné poklady)")
            print("  2) 🔮 Nekromantský rituál u kostnice (+25 temné energie)")
        elif lok_id == "chram_cistoty":
            print("  1) ⛪ Veřejný dar chrámu a pokání (50 🪙 -> -15 vliv inkvizice)")
            print("  2) 🤫 Naslouchání u zpovědnice (zisk kompro materiálu na inkvizici)")
            print("  3) 🕯️ Znesvěcení oltáře stínovým rituálem (+35 temné energie, +5 inkvizice)")
        elif lok_id == "vezeni_inkvizice":
            print("  1) ⛓️ Infiltrace cel a osvobození čarodějky Vespery (zisk unikátní otrokyně)")
            print("  2) 🔥 Spálení inkvizičních archívů a spisů (-20 vliv inkvizice!)")
            print("  3) 🪙 Podplacení žalářníků a výkup vězenkyně (75 🪙 -> nová otrokyně)")
        elif lok_id == "tajna_svatyne_stinu":
            print("  1) 🗡️ Zadání sabotáže konkurenčních syndikátů (+8 % kontrola území mafie)")
            print("  2) 🧪 Nákup stínových jedů a zlodějského náčiní (40 🪙)")
        elif lok_id == "akademie":
            print("  1) 📜 Studium v magické knihovně (+35 XP, +1 magická esence)")
            print("  2) 🧪 Pokusy v alchymistické laboratoři s Nelou")
        elif lok_id == "hostinec":
            print("  1) 🍻 Koupit rundu pro celý sál (25 🪙 -> +6 reputace města)")
            print("  2) 🎲 Hazardní hra v kostky se štamgasty")

        vytiskni_volbu('0', 'Zpět')
        volba = input("\n> ").strip()
        if volba == "0":
            return

        # Vyhodnocení lokačních akcí
        if lok_id == "pevnost":
            if volba == "1":
                tisk_ok("Provedl jsi inspekci stráží a hradeb. Obranná morálka dominia posílena (+3 obrana)!")
            elif volba == "2":
                if hra.hrac.gold >= 20:
                    hra.hrac.gold -= 20
                    hra.pevnost.zasoby += 25
                    tisk_ok("Sýpky doplněny! Získáno +25 zásob jídla.")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "3":
                for o in hra.harem.vsechny_aktivni():
                    o.loajalita = min(100, o.loajalita + 4)
                tisk_ok("Otrokyně vnímaly tvou přítomnost a péči. Loajalita harému vzrostla!")

        elif lok_id == "trh":
            if volba == "1":
                zamcene = [k for k in LOKACE if k not in self.odhalene_lokace]
                if zamcene:
                    nova = random.choice(zamcene)
                    self.odhal_lokaci(nova)
                    tisk_ok(f"Zaslechl jsi cenné zvěsti a odhalil lokaci: {LOKACE[nova]['nazev']}!")
                else:
                    tisk_info("Všechny známé lokace už máš zmapované. Získal jsi tip na cenného klienta.")
            elif volba == "2":
                if hra.hrac.gold >= 30:
                    hra.hrac.gold -= 30
                    for o in hra.harem.vsechny_aktivni():
                        o.touha = min(100, o.touha + 10)
                        o.loajalita = min(100, o.loajalita + 5)
                    tisk_ok("Hedvábí a parfémy udělaly dívkám obrovskou radost (+touha, +loajalita)!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "3":
                zisk = random.randint(25, 55)
                hra.hrac.gold += zisk
                tisk_ok(f"Obratně jsi vybral pár měšců v davu (+{zisk} 🪙)!")

        elif lok_id == "les":
            if volba == "1":
                zisk_j = 25
                if any("amazonka" in getattr(o, "charakter", "").lower() for o in hra.harem.vsechny_aktivni()):
                    zisk_j = 40
                    tisk_info("Tvá Amazonka v harému ti pomohla vystopovat velkou kořist!")
                if hasattr(hra, "pevnost"):
                    hra.pevnost.zasoby += zisk_j
                    hra.pevnost.drevo += 15
                tisk_ok(f"Úspěšný lov! Do pevnosti putuje +{zisk_j} zásob jídla a +15 dřeva.")
            elif volba == "2":
                if hasattr(hra, "pevnost"):
                    hra.pevnost.drevo += 35
                tisk_ok("Dřevorubci nařezali čerstvé kmeny (+35 dřeva pro dominium)!")
            elif volba == "3":
                if hasattr(hra, "alchymie"):
                    hra.alchymie.pridat_surovinu("bylina_mesicni", 1)
                tisk_ok("Nalezena byla bylina měsíčnice pro alchymii!")

        elif lok_id == "krvavy_lom":
            if volba == "1":
                if hra.hrac.gold >= 40:
                    hra.hrac.gold -= 40
                    hra.pevnost.kamen += 70
                    tisk_ok("Povozy naložené kamenem dorazily do pevnosti (+70 kamene)!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "2":
                if hra.hrac.gold >= 35:
                    hra.hrac.gold -= 35
                    hra.pevnost.zelezo += 40
                    tisk_ok("Železná ruda složena v pevnostní kovárně (+40 železa)!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "3":
                if hra.hrac.gold >= 110:
                    hra.hrac.gold -= 110
                    from models.otrokyne import Otrokyně
                    from data.jmena import JMENA
                    jmeno = random.choice(JMENA)
                    nova = Otrokyně(jmeno=jmeno, vek=22, charakter="Amazonka (bojovnice)", loajalita=80, poslusnost=65)
                    hra.harem.pridat(nova)
                    tisk_ok(f"★ Zocelená amazonka {jmeno} byla zachráněna a vděčně tě následuje do dominia!")
                else:
                    tisk_chyba("Nedostatek zlata.")

        elif lok_id == "vezeni_inkvizice":
            if volba == "1":
                if any(o.jmeno == "Vespera" for o in hra.harem.otrokyne):
                    tisk_info("Vespera už byla z těchto cel osvobozena.")
                else:
                    if hra.hrac.dark_energy >= 12 or hra.hrac.gold >= 40:
                        if hra.hrac.dark_energy >= 12:
                            hra.hrac.dark_energy -= 12
                        else:
                            hra.hrac.gold -= 40
                        from models.otrokyne import Otrokyně
                        nova = Otrokyně(jmeno="Vespera", vek=23, charakter="carodejka", loajalita=85, poslusnost=70)
                        hra.harem.pridat(nova)
                        tisk_ok("★ Vespera osvobozena! Její runová magie nyní slouží tvému harému.")
                    else:
                        tisk_chyba("Potřebuješ 12 temné energie nebo 40 🪙 na překonání zámků cely!")
            elif volba == "2":
                hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 20)
                tisk_ok("Inkviziční spisy a knihy kacířů shořely na popel! Vliv inkvizice klesl o -20!")
            elif volba == "3":
                if hra.hrac.gold >= 75:
                    hra.hrac.gold -= 75
                    from models.otrokyne import Otrokyně
                    from data.jmena import JMENA
                    jmeno = random.choice(JMENA)
                    nova = Otrokyně(jmeno=jmeno, vek=random.randint(18, 24), charakter="ustrasena", loajalita=75, poslusnost=60)
                    hra.harem.pridat(nova)
                    tisk_ok(f"★ Vězenkyně {jmeno} byla vykoupena z mučírny a připojila se k tvému harému!")
                else:
                    tisk_chyba("Nedostatek zlata.")

        elif lok_id == "paserska_zatoka":
            if volba == "1":
                if hra.hrac.hp > 20:
                    hra.hrac.hp -= 10
                    zisk = random.randint(80, 160)
                    hra.hrac.gold += zisk
                    hra.pevnost.drevo += 30
                    hra.pevnost.zelezo += 20
                    tisk_ok(f"✔ Přepad kupecké lodi byl úspěšný! Získáno: +{zisk} 🪙, +30 dřeva a +20 železa pro pevnost!")
                else:
                    tisk_chyba("Jsi příliš vyčerpaný na pirátskou razii!")
            elif volba == "2":
                if hra.hrac.gold >= 100:
                    hra.hrac.gold -= 100
                    from models.otrokyne import Otrokyně
                    from data.jmena import JMENA
                    jmeno = random.choice(JMENA)
                    nova = Otrokyně(jmeno=jmeno, vek=21, charakter="kurtizana", loajalita=70, touha=75)
                    hra.harem.pridat(nova)
                    tisk_ok(f"★ Exotická zajatkyně {jmeno} z moře byla vykoupena do tvého harému!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "3":
                hra.hrac.gold += 50
                tisk_ok("Prodal jsi pašované šperky místním pirátům (+50 🪙)!")

        elif lok_id == "zricenina_astralni_veze":
            if volba == "1":
                if hra.hrac.gold >= 40:
                    hra.hrac.gold -= 40
                    max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
                    max_t = hra.hrac.max_temno() if hasattr(hra.hrac, "max_temno") else 100
                    hra.hrac.sex_energy = max_s
                    hra.hrac.dark_energy = max_t
                    hra.hrac.hp = hra.hrac.max_hp
                    tisk_ok("Astrální zřídlo obnovilo veškerou tvou životní i sexuální energii a vyléčilo tělo!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "2":
                hra.pevnost.krystaly += 3
                tisk_ok("Vyluštil jsi hvězdné stély a získal 3 temné krystaly a zkušenosti!")
            elif volba == "3":
                aktivni = hra.harem.vsechny_aktivni()
                if aktivni:
                    spolecnice = random.choice(aktivni)
                    spolecnice.loajalita = min(100, spolecnice.loajalita + 20)
                    tisk_ok(f"Astrální plamen spojil tvou duši s {spolecnice.jmeno} (loajalita +20)!")

        elif lok_id == "chram_cistoty":
            if volba == "1":
                if hra.hrac.gold >= 50:
                    hra.hrac.gold -= 50
                    hra.hrac.vliv_inkvizice = max(0, hra.hrac.vliv_inkvizice - 15)
                    tisk_ok("Kněží přijali tvůj dar. Inkviziční hlídky byly odvolány (-15 vliv inkvizice)!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "2":
                hra.hrac.reputace_mesta += 4
                tisk_ok("U zpovědnice jsi vyslechl tajemství městských hodnostářů (reputace +4, kompro materiál)!")
            elif volba == "3":
                hra.hrac.dark_energy = min(120, hra.hrac.dark_energy + 35)
                hra.hrac.vliv_inkvizice = min(100, hra.hrac.vliv_inkvizice + 5)
                tisk_ok("Znesvětil jsi oltář stínem (+35 temné energie, +5 vliv inkvizice)!")

        elif lok_id == "zahradni_altan":
            if volba == "1":
                for marriage in getattr(hra, "marriage_system", {}).values():
                    if hasattr(marriage, "zmen_zarlivost"):
                        marriage.zmen_zarlivost(-15)
                        marriage.zmen_spokojenost(15)
                tisk_ok("Čajový obřad vnesl harmonii do harému. Žárlivost všech manželek klesla o -15 %!")
            elif volba == "2":
                max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
                hra.hrac.sex_energy = min(max_s, hra.hrac.sex_energy + 20)
                tisk_ok("Romantická chvíle v altánu u leknínů tě naplnila novou vášní (+20 sexuální energie)!")

        elif lok_id == "podzemni_arena":
            if volba == "1":
                from game.souboje import Souboj
                souboj = Souboj(hra.hrac, getattr(hra, "mafie", None), hra=hra)
                souboj.menu()
            elif volba == "2":
                if hra.hrac.gold >= 20:
                    hra.hrac.gold -= 20
                    if random.random() < 0.55:
                        vyhra = 50
                        hra.hrac.gold += vyhra
                        tisk_ok(f"✔ Tvůj favorit v aréně zvítězil! Získal jsi výhru {vyhra} 🪙!")
                    else:
                        tisk_chyba("Tvůj zápasník v písku padl. Prohrál jsi 20 🪙.")
                else:
                    tisk_chyba("Nedostatek zlata.")

        elif lok_id == "katakomby":
            if volba == "1":
                if random.random() < 0.70:
                    korist = random.randint(45, 95)
                    hra.hrac.gold += korist
                    tisk_ok(f"V královské kryptě jsi nalezl starobylé klenoty (+{korist} 🪙)!")
                else:
                    hra.hrac.hp = max(1, hra.hrac.hp - 15)
                    tisk_chyba("Kryptu střežil nemrtvý strážce! V boji jsi utržil zranění (-15 HP).")
            elif volba == "2":
                hra.hrac.dark_energy = min(120, hra.hrac.dark_energy + 25)
                tisk_ok("Rituál u kostnice tě naplnil temnou mocí (+25 temné energie)!")

        elif lok_id == "lazne":
            if volba == "1":
                if hra.hrac.gold >= 20:
                    hra.hrac.gold -= 20
                    hra.hrac.hp = hra.hrac.max_hp
                    max_s = hra.hrac.max_sex() if hasattr(hra.hrac, "max_sex") else 100
                    hra.hrac.sex_energy = min(max_s, hra.hrac.sex_energy + 25)
                    tisk_ok("Horké lázně zcela obnovily tvé zdraví a sexuální energii!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "2":
                for o in hra.harem.vsechny_aktivni():
                    o.touha = min(100, o.touha + 12)
                    o.loajalita = min(100, o.loajalita + 5)
                tisk_ok("Společná parní lázeň probudila v harému novou touhu a loajalitu!")

        elif lok_id == "hostinec":
            if volba == "1":
                if hra.hrac.gold >= 25:
                    hra.hrac.gold -= 25
                    hra.hrac.reputace_mesta += 6
                    tisk_ok("Koupil jsi rundu pro celý hostinec. Štamgasti provolávají tvé slávě (+6 reputace města)!")
                else:
                    tisk_chyba("Nedostatek zlata.")
            elif volba == "2":
                if hra.hrac.gold >= 15:
                    hra.hrac.gold -= 15
                    if random.random() < 0.5:
                        hra.hrac.gold += 35
                        tisk_ok("Hodil jsi vítězná čísla! Vyhrál jsi 35 🪙!")
                    else:
                        tisk_chyba("Kostky ti nepřály. Prohrál jsi 15 🪙.")
                else:
                    tisk_chyba("Nedostatek zlata.")

        elif lok_id == "cervena_ctvrt":
            if volba == "1":
                from game.nevestinec import menu_nevestinec
                menu_nevestinec(hra)
            elif volba == "2":
                tisk_ok("Procházka po Červené čtvrti ti přinesla nové kontakty v podsvětí (+3 vliv mafie).")
                if hasattr(hra, "mafie"):
                    hra.mafie.vliv = min(100, getattr(hra.mafie, "vliv", 0) + 3)

        else:
            # Obecná akce pro ostatní lokace
            if volba == "1":
                hra.hrac.reputace_mesta += 3
                tisk_ok(f"Provedl jsi úspěšnou inspekci a posílil vliv dominia v lokaci {info['nazev']} (+3 reputace)!")
            elif volba == "2":
                hra.hrac.gold += 25
                tisk_ok(f"Získal jsi lokální poplatky a daně (+25 🪙)!")

        input("\nEnter...")
