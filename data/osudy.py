"""Datově řízené, ne-erotické osobní příběhy postav."""

OSUDY = {
    "ztraceny_zapisnik": {
        "nazev": "Ztracený zápisník",
        "popis": "V zápisníku jsou poznámky, které mohou očistit její rodinu.",
        "kroky": [
            {
                "text": "Našla starý zápisník. Chce, abys rozhodl, zda ho vrátit jeho původnímu majiteli.",
                "volby": [
                    {
                        "nazev": "Vrátit zápisník",
                        "popis": "Důvěra je důležitější než okamžitý zisk.",
                        "efekty": {"duvera": 8, "loajalita": 10, "reputace_mesta": 3},
                    },
                    {
                        "nazev": "Prodat informace",
                        "popis": "Získáš zlato, ale její rodina ti nebude věřit.",
                        "efekty": {"duvera": -8, "loajalita": -10, "gold": 120},
                    },
                ],
            },
            {
                "text": "Majitel zápisníku nabízí svědectví výměnou za bezpečný odchod z města.",
                "volby": [
                    {
                        "nazev": "Zajistit bezpečný odchod",
                        "popis": "Pomůžeš svědkovi zmizet přes přístav.",
                        "efekty": {"loajalita": 12, "duvera": 8, "xp": 30, "unlock_location": "pristav"},
                        "odmena": {"id": "pecet_svedka", "mnozstvi": 1},
                    },
                    {
                        "nazev": "Předat svědka stráži",
                        "popis": "Získáš přízeň úřadů, ale ztratíš její respekt.",
                        "efekty": {"loajalita": -15, "duvera": -10, "reputace_mesta": 8, "vliv_inkvizice": -3},
                    },
                ],
            },
        ],
    },
    "dluh_rodiny": {
        "nazev": "Dluh rodiny",
        "popis": "Starý dluh ohrožuje její sourozence i jejich malý obchod.",
        "kroky": [
            {
                "text": "Výběrčí dluhu přišel k branám. Můžeš rodině pomoci penězi nebo hledat jinou cestu.",
                "volby": [
                    {
                        "nazev": "Zaplatit 100 zlaťáků",
                        "popis": "Uhradíš dluh a získáš čas.",
                        "podminka": {"gold": 100},
                        "efekty": {"gold": -100, "loajalita": 14, "duvera": 10},
                    },
                    {
                        "nazev": "Vyjednat odklad",
                        "popis": "Riskantní dohoda s výběrčím.",
                        "efekty": {"loajalita": 6, "duvera": 4, "vliv_inkvizice": 2},
                    },
                ],
            },
            {
                "text": "Rodina chce znovu otevřít dílnu a potřebuje někoho, kdo ji ochrání.",
                "volby": [
                    {
                        "nazev": "Dosadit ochranku",
                        "popis": "Využiješ vliv mafie k ochraně dílny.",
                        "efekty": {"loajalita": 12, "reputace_mesta": 2, "mafie_vliv": 4},
                        "odmena": {"id": "remeslne_naradi", "mnozstvi": 1},
                    },
                    {
                        "nazev": "Nechat rodinu jednat samostatně",
                        "popis": "Respektuješ její přání, ale cesta bude pomalejší.",
                        "efekty": {"duvera": 14, "loajalita": 8, "xp": 25},
                    },
                ],
            },
        ],
    },
    "hranicarcina_prisaha": {
        "nazev": "Hraničářčina přísaha",
        "popis": "Kdysi chránila vesnici na hranici a stále slyší volání o pomoc.",
        "kroky": [
            {
                "text": "Posel přináší zprávu: hranice čelí nájezdům. Rozhodni, jak odpovíš.",
                "volby": [
                    {
                        "nazev": "Vyslat pomoc",
                        "popis": "Obětuješ část zdrojů pro bezpečí vesnice.",
                        "podminka": {"gold": 80},
                        "efekty": {"gold": -80, "loajalita": 12, "reputace_mesta": 6},
                    },
                    {
                        "nazev": "Vyslechnout nejdřív svědky",
                        "popis": "Získáš informace a vyhneš se zbrklému rozhodnutí.",
                        "efekty": {"duvera": 8, "loajalita": 6, "xp": 20},
                    },
                ],
            },
            {
                "text": "Vesničané chtějí, aby se vrátila jako velitelka hlídky.",
                "volby": [
                    {
                        "nazev": "Dovolit jí vést výpravu",
                        "popis": "Dočasně ji pošleš mimo pevnost, ale získáš zkušenou spojenkyni.",
                        "efekty": {"loajalita": 16, "duvera": 6, "xp": 40},
                        "odmena": {"id": "signalni_roh", "mnozstvi": 1},
                    },
                    {
                        "nazev": "Požádat ji, aby zůstala",
                        "popis": "Bezpečí pevnosti má přednost, její volání ale nevyslyšíš.",
                        "efekty": {"loajalita": -8, "duvera": -6, "obrana": 3},
                    },
                ],
            },
        ],
    },
    "hlas_odboje": {
        "nazev": "Hlas odboje",
        "popis": "Její přátelé tajně pomáhají lidem, které město přehlíží.",
        "kroky": [
            {
                "text": "Odboj žádá o zásoby. Každá volba změní, jak ti bude věřit.",
                "volby": [
                    {
                        "nazev": "Darovat zásoby",
                        "popis": "Zmenšíš vlastní zásoby, ale posílíš odboj.",
                        "podminka": {"item": "zdravotni_balicek"},
                        "efekty": {"loajalita": 12, "duvera": 10},
                    },
                    {
                        "nazev": "Předat jen informace",
                        "popis": "Pomůžeš bez přímého rizika.",
                        "efekty": {"loajalita": 6, "reputace_mesta": 3, "vliv_inkvizice": 2},
                    },
                ],
            },
            {
                "text": "Inkvizice odhalila stopu a hledá viníka.",
                "volby": [
                    {
                        "nazev": "Vzít vinu na sebe",
                        "popis": "Odvedeš pozornost od svých spojenců.",
                        "efekty": {"loajalita": 18, "vliv_inkvizice": 8, "xp": 35},
                        "odmena": {"id": "tajny_vzkaz", "mnozstvi": 1},
                    },
                    {
                        "nazev": "Přerušit kontakt",
                        "popis": "Snížíš nebezpečí, ale zklameš ji.",
                        "efekty": {"loajalita": -12, "duvera": -8, "vliv_inkvizice": -4},
                    },
                ],
            },
        ],
    },
    "dilna_a_dedictvi": {
        "nazev": "Dílna a dědictví",
        "popis": "Po rodičích jí zůstala dílna, o kterou se přou dva dědicové.",
        "kroky": [
            {
                "text": "Dva příbuzní tvrdí, že právě oni mají na dílnu právo.",
                "volby": [
                    {
                        "nazev": "Najít nestranného svědka",
                        "popis": "Pomůžeš odhalit pravdu bez násilí.",
                        "efekty": {"duvera": 10, "loajalita": 8, "reputace_mesta": 4},
                    },
                    {
                        "nazev": "Podpořit silnějšího",
                        "popis": "Rychlé řešení přinese okamžitý klid.",
                        "efekty": {"gold": 80, "loajalita": -6, "duvera": -4},
                    },
                ],
            },
            {
                "text": "Dílna může vyrábět vybavení pro tvé lidi, pokud dostane ochranu.",
                "volby": [
                    {
                        "nazev": "Uzavřít férovou smlouvu",
                        "popis": "Dílna zůstane samostatná a bude ti dodávat vybavení.",
                        "efekty": {"loajalita": 14, "duvera": 12, "mafie_vliv": 3},
                        "odmena": {"id": "opravarenska_sada", "mnozstvi": 1},
                    },
                    {
                        "nazev": "Dílnu zabrat pro sebe",
                        "popis": "Získáš výrobu, ale ztratíš její důvěru.",
                        "efekty": {"loajalita": -18, "duvera": -15, "mafie_vliv": 8},
                    },
                ],
            },
        ],
    },
    "tichy_svedek": {
        "nazev": "Tichý svědek",
        "popis": "Viděla zločin mocných a bojí se, že pravda zničí její život.",
        "kroky": [
            {
                "text": "Chce mluvit, ale jen pokud jí zaručíš bezpečí a možnost volby.",
                "volby": [
                    {
                        "nazev": "Slíbit ochranu",
                        "popis": "Převezmeš odpovědnost za její bezpečí.",
                        "efekty": {"duvera": 14, "loajalita": 10, "vliv_inkvizice": 3},
                    },
                    {
                        "nazev": "Požádat o důkaz",
                        "popis": "Jistota je důležitější než její strach.",
                        "efekty": {"duvera": -4, "loajalita": 4, "xp": 20},
                    },
                ],
            },
            {
                "text": "Důkaz je připraven. Je čas rozhodnout, komu bude pravda sloužit.",
                "volby": [
                    {
                        "nazev": "Zveřejnit pravdu",
                        "popis": "Město se dozví, co se stalo.",
                        "efekty": {"loajalita": 16, "duvera": 10, "reputace_mesta": 10, "vliv_inkvizice": 6},
                        "odmena": {"id": "dukazni_listina", "mnozstvi": 1},
                    },
                    {
                        "nazev": "Použít důkaz k vyjednávání",
                        "popis": "Získáš politickou výhodu a ochráníš její jméno.",
                        "efekty": {"gold": 180, "loajalita": 5, "duvera": 5, "mafie_vliv": 5},
                    },
                ],
            },
        ],
    },
    "cesta_pod_hvezdami": {
        "nazev": "Cesta pod hvězdami",
        "popis": "Učí se znovu věřit vlastnímu hlasu a hledá vztah založený na klidu a volbě.",
        "kroky": [
            {
                "text": "Po dlouhém dni se svěří, že chce být slyšena, ne řízena. Jak odpovíš?",
                "volby": [
                    {
                        "nazev": "Nechat ji určit tempo",
                        "popis": "Dáš jí prostor říct, co skutečně chce.",
                        "efekty": {"duvera": 12, "loajalita": 8, "touha": 4},
                    },
                    {
                        "nazev": "Slíbit ochranu bez podmínek",
                        "popis": "Nabídneš bezpečí a respekt k jejím hranicím.",
                        "efekty": {"duvera": 8, "loajalita": 12, "reputace_mesta": 2},
                    },
                ],
            },
            {
                "text": "Na střeše observatoře je ticho. Mezi vámi vzniká důvěrná chvíle, která nic nevyžaduje.",
                "volby": [
                    {
                        "nazev": "Sdílet vlastní nejistotu",
                        "popis": "Vzájemná upřímnost prohloubí blízkost.",
                        "efekty": {"duvera": 14, "loajalita": 8, "xp": 25},
                    },
                    {
                        "nazev": "Zůstat po jejím boku v tichu",
                        "popis": "Respektuješ, že blízkost může být i beze slov.",
                        "efekty": {"duvera": 10, "loajalita": 10, "touha": 6},
                    },
                ],
            },
        ],
    },
    "spolecny_pristan": {
        "nazev": "Společný přístav",
        "popis": "Dospělý vztah, ve kterém si oba chrání svobodu a přesto se k sobě vracejí.",
        "kroky": [
            {
                "text": "Navrhne, abyste si před důležitým rozhodnutím vždy řekli pravdu. Přijmeš to?",
                "volby": [
                    {
                        "nazev": "Ano, žádná dohoda bez souhlasu",
                        "popis": "Postavíš vztah na otevřené komunikaci.",
                        "efekty": {"duvera": 14, "loajalita": 10, "reputace_mesta": 2},
                    },
                    {
                        "nazev": "Nechat sliby růst přirozeně",
                        "popis": "Nebudeš nic uspěchávat ani vlastnit.",
                        "efekty": {"duvera": 10, "loajalita": 8, "xp": 30},
                    },
                ],
            },
            {
                "text": "Po vítězství se ptá, zda má zůstat v pevnosti, nebo pokračovat po vlastní cestě.",
                "volby": [
                    {
                        "nazev": "Jít spolu, ale každý s vlastním hlasem",
                        "popis": "Sdílíte cestu bez ztráty osobní svobody.",
                        "efekty": {"duvera": 16, "loajalita": 12, "touha": 5},
                    },
                    {
                        "nazev": "Podpořit její samostatnou misi",
                        "popis": "Láska není klec; pomůžeš jí odejít a vrátit se z vlastní vůle.",
                        "efekty": {"duvera": 18, "loajalita": 8, "reputace_mesta": 4, "xp": 35},
                    },
                ],
            },
        ],
    },
}

OSUDY_PORADI = tuple(OSUDY)
