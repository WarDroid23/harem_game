import random
from dataclasses import dataclass, field

from config import (
    GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, GOLD, NC, BOLD, DIM, GRAY, WHITE
)
from utils.vypis import clear, terminalni_obrazek, tisk_chyba, tisk_info, tisk_ok, vytiskni_volbu

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
        "sousedni": ["pevnost", "hranice", "haj_soumraku", "svatyne_krvaveho_mesice"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "pristav": {
        "nazev": "Černý přístav",
        "kratky": "Přístav",
        "ikona": "⚓",
        "popis": "Místo pašeráků, lodí a zpráv z dalekých zemí.",
        "sousedni": ["trh", "molo_mesicniho_pristavu", "palac_bohatych", "cervena_ctvrt"],
        "uroven": 2,
        "nebezpeci": "střední",
    },
    "hranice": {
        "nazev": "Hraniční ves",
        "kratky": "Hranice",
        "ikona": "⚔",
        "popis": "Opevněná vesnice na pomezí říše, ohrožovaná nájezdy ze severu.",
        "sousedni": ["les", "observator"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
    "ctvrt_remeselniku": {
        "nazev": "Čtvrť řemeslníků",
        "kratky": "Řemesla",
        "ikona": "🔨",
        "popis": "Dílny, cechy a lidé, kteří umí proměnit suroviny v užitečné vybavení.",
        "sousedni": ["trh", "akademie", "palac_bohatych"],
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
        "sousedni": ["sklenena_zahrada", "hranice", "molo_mesicniho_pristavu"],
        "uroven": 3,
        "nebezpeci": "střední",
    },
    "molo_mesicniho_pristavu": {
        "nazev": "Molo Měsíčního přístavu",
        "kratky": "Molo",
        "ikona": "🌊",
        "popis": "Tiché molo na okraji přístavu, kde se uzavírají dohody a odplouvá do dálek.",
        "sousedni": ["pristav", "observator", "sklenena_zahrada"],
        "uroven": 3,
        "nebezpeci": "střední",
    },
    "katakomby": {
        "nazev": "Katakomby pod městem",
        "kratky": "Katakomby",
        "ikona": "💀",
        "popis": "Starobylé podzemní hrobky pod starým městem, zřídlo temné energie a zapomenutých relikvií.",
        "sousedni": ["trh", "lazne", "svatyne_krvaveho_mesice", "podzemni_arena", "chram_cistoty", "tajna_svatyne_stinu"],
        "uroven": 3,
        "nebezpeci": "vysoké",
    },
    "svatyne_krvaveho_mesice": {
        "nazev": "Krvavá svatyně v lese",
        "kratky": "Svatyně",
        "ikona": "🩸",
        "popis": "Opuštěná kultistická svatyně ukrytá v Mlžném lese pro temné rituály dominia.",
        "sousedni": ["les", "haj_soumraku", "katakomby"],
        "uroven": 3,
        "nebezpeci": "velmi vysoké",
    },
    "palac_bohatych": {
        "nazev": "Palác a čtvrť bohatých",
        "kratky": "Palác",
        "ikona": "👑",
        "popis": "Sídlo městské smetánky a guvernérův palác, centrum intrik, luxusu a politického vlivu.",
        "sousedni": ["trh", "ctvrt_remeselniku", "pristav", "cervena_ctvrt", "stribrne_terasy", "chram_cistoty"],
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
        "sousedni": ["trh", "palac_bohatych", "katakomby"],
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

    def _format_uzel(self, lok_id, hra):
        """Naformátuje uzel na mapě s ikonami statusu."""
        info = LOKACE[lok_id]
        kratky = info.get("kratky", info["nazev"][:7])
        ikona = info.get("ikona", "•")

        if lok_id not in self.odhalene_lokace:
            return f"{GRAY}[? Neodhaleno ?]{NC}"

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
            return f"{GREEN}{BOLD}▶[{text:^13}]◀{NC}"
        else:
            return f"{CYAN}[{text:^13}]{NC}"

    def vykresli_ascii_mapu(self, hra):
        """Vykreslí přehlednou barevnou síťovou mapu království."""
        u = lambda lid: self._format_uzel(lid, hra)

        print(f"{GOLD}╔═════════════════════════════ ASCII MAPA KRÁLOVSTVÍ ═════════════════════════════╗{NC}")
        print(f"║                                                                                   ║")
        print(f"║  {u('pevnost')} ═══════════ {u('les')} ═══════════ {u('hranice')}        ║")
        print(f"║        ║                       ║                         ║                        ║")
        print(f"║        ║                       ║                  {u('svatyne_krvaveho_mesice')}        ║")
        print(f"║        ║                       ║                         ║                        ║")
        print(f"║  {u('trh')} ═══════════ {u('haj_soumraku')} ═════════ {u('observator')}        ║")
        print(f"║   ║ ║  ║                       ║                         ║                        ║")
        print(f"║   ║ ║ {u('ctvrt_remeselniku')} ══════ {u('lazne')} ═══════════ {u('sklenena_zahrada')}        ║")
        print(f"║   ║ ║  ║                       ║                         ║                        ║")
        print(f"║   ║ ║ {u('palac_bohatych')} ═════ {u('stribrne_terasy')} ══════ {u('zahradni_altan')}        ║")
        print(f"║   ║ ║  ║                       ║                         ║                        ║")
        print(f"║  {u('cervena_ctvrt')} ═══ {u('pristav')}               ║                  {u('molo_mesicniho_pristavu')}        ║")
        print(f"║   ║    ║                       ║                         ║                        ║")
        print(f"║  {u('podzemni_arena')} ════ {u('katakomby')} ═════ {u('chram_cistoty')}                     ║")
        print(f"║        ║                                                                          ║")
        print(f"║  {u('tajna_svatyne_stinu')}                                                               ║")
        print(f"║                                                                                   ║")
        print(f"{GOLD}╚═══════════════════════════════════════════════════════════════════════════════════╝{NC}")
        print(f"{DIM}Legenda: {GREEN}▶[ ... ]◀{NC}{DIM} Jsi zde | {CYAN}[🛡️]{NC}{DIM} Území tvé mafie | {CYAN}[🎯]{NC}{DIM} Aktivní quest | {GRAY}[? Neodhaleno ?]{NC}\n")

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
                  f"  |  {YELLOW}P){NC} Průzkum"
                  f"  |  {MAGENTA}N){NC} Rozhovor s NPC"
                  f"  |  {CYAN}E){NC} Energie"
                  f"  |  {extra_prompt}"
                  f"  {RED}0){NC} Zpět")
            volba = input(f"\n{BOLD}>{NC} ").strip().lower()


            if volba == "0":
                return
            if volba == "b" and self.aktualni_lokace == "cervena_ctvrt":
                from game.nevestinec import menu_nevestinec
                menu_nevestinec(hra)
                continue
            if volba == "p":
                self.pruzkum_lokace(hra)
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
        vytiskni_volbu('1', 'Přátelsky si promluvit  2) Požádat o službu  3) Nabídnout pomoc')
        akce = input("> ").strip()
        vztah = self.vztahy_npc[npc_id]

        if akce == "1":
            self.zmen_vztah(npc_id, 4)
            hra.hrac.reputace_mesta += 1
            dialogy = npc.get("dialogy", [])
            if dialogy:
                index_dialogu = 0 if vztah < 35 else min(len(dialogy) - 1, 1)
                print(f"{npc['jmeno']}: „{dialogy[index_dialogu]}“")
            tisk_ok(f"{npc['jmeno']} si tě zapamatoval. Vztah +4.")

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
                else:
                    hra.hrac.gold += 30
                    self.zmen_vztah(npc_id, 6)
                    tisk_ok("Pomohl jsi NPC s její prací. Získal jsi 30 zlata, vztah +6.")
        else:
            tisk_chyba("Neplatná volba.")
        input("Enter...")

