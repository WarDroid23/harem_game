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
    "pomsta_elena": {
        "nazev": "Krev inkvizitora",
        "popis": "Elena pátrá po inkvizitorovi, který vyvraždil její rodinu pod záminkou kacířství.",
        "kroky": [
            {
                "text": "Elena zachytila stopu. Inkviziční soudce Malakor se skrývá v podzemních kobkách. Žádá tě o pomoc s infiltrací.",
                "volby": [
                    {
                        "nazev": "Vyzbrojit Elenu a vést přímý útok",
                        "popis": "Čelní útok na inkviziční garnizonu. Prověří vaši sílu.",
                        "efekty": {"loajalita": 20, "duvera": 15, "bloodlust": 10, "xp": 50},
                        "odmena": {"id": "inkvizicni_dyka", "mnozstvi": 1},
                    },
                    {
                        "nazev": "Vylákat soudce lstí a podplatit stráže",
                        "popis": "Tichá pomsta beze svědků. (Stojí 150 zlaťáků)",
                        "podminka": {"gold": 150},
                        "efekty": {"gold": -150, "duvera": 25, "loajalita": 25, "vliv_inkvizice": -15, "xp": 40},
                    },
                ],
            },
            {
                "text": "Soudce leží v řetězech před Elenou. Dívka třesoucí se rukou drží čepel a hledí na tebe, zda má vykonat ortel.",
                "volby": [
                    {
                        "nazev": "Nechat Elenu vykonat pomstu vlastní rukou",
                        "popis": "Ukončí trauma krví a najde vnitřní sílu a klid.",
                        "efekty": {"loajalita": 30, "duvera": 20, "poslusnost": 20, "reputace_mesta": 5},
                    },
                    {
                        "nazev": "Ušetřit soudce a uvrhnout ho do otroctví v tvém dole",
                        "popis": "Chladný kalkul přinese tvému dominiu doživotního dělníka.",
                        "efekty": {"loajalita": 15, "broken": 5, "gold": 250, "xp": 60},
                    },
                ],
            },
        ],
    },
    "sestra_scarlett": {
        "nazev": "Stíny aukční síně",
        "popis": "Scarlettina mladší sestra byla unesena cechem otrokářů a má být vydražena mecenášům.",
        "kroky": [
            {
                "text": "Scarlett klečí před tebou v slzách. Zjistila, že dražba proběhne dnes v noci v Červené čtvrti.",
                "volby": [
                    {
                        "nazev": "Odkoupit sestru zlatem na aukci",
                        "popis": "Čisté a bezpečné řešení. (Stojí 300 zlaťáků)",
                        "podminka": {"gold": 300},
                        "efekty": {"gold": -300, "duvera": 35, "loajalita": 30, "touha": 15},
                    },
                    {
                        "nazev": "Přepadnout aukční karavanu s mafií",
                        "popis": "Tvrdý úder na konkurenční překupníky.",
                        "efekty": {"loajalita": 25, "duvera": 20, "mafie_vliv": 10, "xp": 50},
                    },
                ],
            },
            {
                "text": "Sestra je v bezpečí. Scarlett je zaplavena nepopsatelným vděkem a přísahá ti věčnou oddanost.",
                "volby": [
                    {
                        "nazev": "Přijmout Scarlett jako svou věrnou choť a chráněnku",
                        "popis": "Povýšíš její status na váženou paní dominia.",
                        "efekty": {"loajalita": 40, "duvera": 30, "touha": 25, "reputace_mesta": 5},
                    },
                    {
                        "nazev": "Připomenout jí, komu nyní obě patří",
                        "popis": "Upevníš svou absolutní dominanci nad oběma dívkami.",
                        "efekty": {"poslusnost": 35, "submisivita": 30, "strach": 10, "broken": 5},
                    },
                ],
            },
        ],
    },
    "stribrny_prsten_lyra": {
        "nazev": "Dědictví rodu Von Ravens",
        "popis": "Lyra touží získat zpět rodinný stříbrný prsten, který jí zabavil lichvář v přístavu.",
        "kroky": [
            {
                "text": "Lichvář odmítá prsten vydat bez obrovského výkupného nebo laskavosti pro místní cech.",
                "volby": [
                    {
                        "nazev": "Zastrašit lichváře mocí tvého dominia",
                        "popis": "Ukážeš sílu zbraní a strachu.",
                        "efekty": {"loajalita": 15, "poslusnost": 20, "mafie_vliv": 5},
                    },
                    {
                        "nazev": "Zaplatit výkupné 180 zlaťáků",
                        "popis": "Čestné vykoupení relikvie bez zbytečného rozruchu.",
                        "podminka": {"gold": 180},
                        "efekty": {"gold": -180, "duvera": 25, "loajalita": 20},
                    },
                ],
            },
            {
                "text": "Prsten je zpět. Lyra ti jej nabízí, abys ho navlékl na její prst jako symbol věčného spojení.",
                "volby": [
                    {
                        "nazev": "Navléknout jí prsten jako symbol vzájemné lásky a cti",
                        "popis": "Spojení dvou duší v královském svazku.",
                        "efekty": {"duvera": 30, "loajalita": 30, "touha": 20, "xp": 45},
                    },
                    {
                        "nazev": "Ponechat si prsten jako cenný magický artefakt",
                        "popis": "Posílí tvou vlastní obranu a prestiž.",
                        "efekty": {"obrana": 3, "loajalita": 5, "poslusnost": 15},
                    },
                ],
            },
        ],
    },
    "grimoar_vespera": {
        "nazev": "Zakázaný grimoár stínů",
        "popis": "Čarodějka Vespera cítí volání ztraceného grimoáru ukrytého v ruinách observatoře.",
        "kroky": [
            {
                "text": "V ruinách staré hvězdárny hlídá zapečetěný grimoár prastarý magický přízrak.",
                "volby": [
                    {
                        "nazev": "Porazit strážce společnou temnou magií",
                        "popis": "Vyžaduje 20 temné energie hráče.",
                        "efekty": {"loajalita": 25, "duvera": 20, "xp": 60},
                    },
                    {
                        "nazev": "Použít krystal síly k prolomení pečeti",
                        "popis": "Alchymistické prolomení magické bariéry.",
                        "podminka": {"item": "krystal_sily"},
                        "efekty": {"duvera": 25, "loajalita": 20, "xp": 40},
                    },
                ],
            },
            {
                "text": "Grimoár je otevřen. Stránky pulzují temnou energií. Vespera nabízí, že s tebou rituálně splyne v temnotě.",
                "volby": [
                    {
                        "nazev": "Podstoupit rituál temného splynutí",
                        "popis": "Získáš +30 temné energie a Vespera se stane tvou temnou kněžkou.",
                        "efekty": {"loajalita": 35, "touha": 30, "duvera": 25, "mindbreak": 3},
                    },
                    {
                        "nazev": "Uložit grimoár do archivu dominia pro výzkum",
                        "popis": "Zvýší dlouhodobý přísun znalostí pro celou pevnost.",
                        "efekty": {"xp": 80, "reputace_mesta": 5, "loajalita": 20},
                    },
                ],
            },
        ],
    },
}

OSUDY_PORADI = tuple(OSUDY)
