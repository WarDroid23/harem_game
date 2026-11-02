# Harem Game 2.0 — Dark Dominion

Textová tahová RPG v češtině o správě dominia, průzkumu propojeného světa,
frakcích, postavách, vztazích, ekonomice a soubojích. Verze 2.0 propojuje
dosavadní herní systémy s offline simulací, ve které města, NPC a frakce
pokračují ve svých činnostech i mezi hráčovými rozhodnutími.

**Tvůrce: #LordRusty23**

> Hra pracuje s temnými a dospělými fikčními tématy a je určena dospělému
> publiku. Herní systémy nenahrazují skutečné vztahy, služby ani historické
> informace.

## Spuštění

Potřebuješ Python 3.8 nebo novější. Projekt je připraven hlavně pro Windows;
volitelnou knihovnu `colorama` spouštěč zkusí doinstalovat, pokud chybí.

**Windows:** spusť `spustit.bat`, případně v PowerShellu nebo terminálu:

```powershell
python launcher.py
```

**Přímé spuštění:**

```bash
python main.py
```

Závislosti nejsou povinné pro základní textové rozhraní. Hra běží lokálně,
nevyžaduje síťovou službu ani připojení k online AI.

## Jak hra funguje

Hráč vede vlastní dominium, získává zdroje, rozvíjí pevnost, vyjednává
s frakcemi a rozhoduje o událostech ve Starém městě i Východním Brodě.
Herní den posouvá simulaci světa, městské ukazatele, cíle frakcí, pohyb NPC,
provoz personálu, armádní rozkazy a některé ekonomické systémy. Hráč může
svět ovlivňovat přímými volbami, úkoly, mapovými akcemi i hospodařením.

Hlavní menu vypisuje aktuálně dostupné volby a podporuje více rozložení.
Číselné zkratky se převádějí na interní volby kvůli kompatibilitě se staršími
savy. Řiď se proto názvy zobrazenými ve své hře; nabídka obsahuje mimo jiné:

- interakce a profily postav, harém a vztahy;
- mapu, lokace, NPC, questy a příběhovou kampaň;
- diplomacii, správu frakcí a živý svět;
- pevnost, budovy, ekonomiku, personál a armádu;
- souboje, arénu, alchymii, crafting a výzkum;
- kasino v Červené čtvrti s kostkami, jednadvacítkou a rozvojem podniku;
- fikční drogová laboratoř a pěstírna konopí s výrobou, prodejem a výzkumem;
- manželství, rodinu, kroniku, kalendář a nastavení.

Terminálové rozhraní používá barevné ASCII ilustrace: profilům postav přidává
stylizovaný portrét podle jejich role a lokace mají vlastní malou scenérii.
Světová mapa dál vyznačuje polohu hráče a barvy frakcí. Jde o textovou grafiku
bez obrázkových souborů a bez Pygame; zobrazení barev závisí na terminálu.

Klávesa **Q** v hlavním menu otevře rozcestník **Hlavní menu / uložit /
nahrát / nastavení**, kde lze hru uložit, načíst, otevřít nastavení nebo se
vrátit do hry. **0** zůstává návratem/ukončením podle právě otevřené nabídky;
**S/L/M** jsou zkratky pro práci s uložením. Nastavení nabízí barevné skiny, zapnutí barev,
obtížnost, Ironman, AI dialogy, vývojářský režim, městskou výzdobu a šest
rozložení hlavního menu: kategorie, seznam, dva sloupce, sekce, mřížka a jeden
sloupec. Náhled ukazuje aktivní vzhled a volba obnovy vrátí pouze vzhledové
volby na výchozí hodnoty. Nastavení hry se ukládají spolu s uloženou hrou.

Průvodce dominiem obsahuje stavový rychlý start, který sleduje první průzkum,
volbu spojence a posun herního dne. Čísla voleb v nápovědě odpovídají právě
zobrazenému menu. Volba spojence v kampani se později projeví při návštěvě
Skleněné zahrady na stavu Starého města, reputaci frakce, vztahu s NPC
a v kronice.

V živém světě lze investovat do prosperity, bezpečí nebo stability města.
Každý další projekt stejného typu ve stejném městě stojí více zlata a ukazatele
se zastaví na 100. Vydírání radního spotřebuje informátora a lze ho provést
nejvýše jednou za herní den; tento limit se ukládá do save.

V hlavním menu se zobrazuje také podpis **Tvůrce: #LordRusty23**.

## Živý svět 2.0

### Města a mapa

Mapa obsahuje 46 propojených lokací ve dvou městech:

- **Staré město** — pevnost, tržiště, přístav, akademie, hostinec a další
  městské, společenské, přírodní a nebezpečné oblasti.
- **Východní Brod** — Východní přístav, tržiště, radnice, kasárna a zahrady;
  navazuje na říční a obchodní cestu ze Starého města.

Hráč objevuje lokace cestováním a průzkumem. Každá lokace má sousedy,
atmosféru, nebezpečí a případné místní akce či odměny. Odhalené oblasti na
mapě získávají barvu podle frakce s nejsilnějším vlivem; legenda rozlišuje
frakční kontrolu a aktuální polohu hráče.
Tekno Party je samostatná lokace se SoundSystemem a tržištěm pro fikční herní
produkty.

### Frakce a místní simulace

Dvanáct frakcí sleduje vlastní cíl. Jejich denní činnost může měnit bezpečí,
prosperitu či stabilitu měst, postupně ovlivňovat kontrolu lokací a vytvářet
rozhodovací situace pro hráče. Městské hodnoty se drží v rozsahu 0–100 a jejich
vzájemné působení znamená, že dlouhodobě nebezpečné či nestabilní město může
ztrácet prosperitu.

Frakce postupně rozvíjejí další etapy cílů. Adaptivní herní AI upravuje jejich
priority podle bezpečí, prosperity a stability jejich města; změny se ukládají
do hry a fungují offline bez externího modelu. Systemáci spravují SoundSystem
v Tekno Party a jsou spojenci Narkomanů.

Šest dvojic frakcí má navíc uložené vztahy. Rivalita může způsobit pokles
bezpečí a stability, spojenectví naopak stabilitu posiluje. V nabídce živého
světa lze vztahy ovlivnit zprostředkováním smíru nebo podporou soupeření.

Nová frakce **Gamblerů** působí v Červené čtvrti, na Půlnočním trhu a
v podzemní aréně. Sleduje růst hazardních heren; jejich turnaje podporují
prosperitu, ale mohou zhoršovat stabilitu. Otevření kasina a hry u jeho stolů
frakci přidávají reputaci i místní vliv. Gamblerové soupeří s policií, která
se snaží držet pořádek a omezovat následky dluhů.

### NPC a jejich příběhy

Městské postavy se přesouvají po propojené mapě a podle své role vyhledávají
oblasti, kde mohou prospět. Jejich činnost přispívá k místnímu stavu měst a
jejich poloha se ukládá. Hráč může otevřít jejich třídílné dlouhodobé příběhy,
pomoci jim za zlato nebo podpořit jejich vlastní rozhodnutí. Dokončení příběhu
ovlivní vztah, město a příslušnou frakci.

Každá z dvanácti frakcí má vlastní starost, obchodní specializaci a tři
příběhové kapitoly. Kronika frakcí v nabídce živého světa ukazuje jejich
reputaci, město, aktuální téma příběhu a zboží. Příběhové rozhovory zobrazují
konkrétní kapitolu příslušné frakce. Přehled obou měst navíc vypíše jejich
nejnaléhavější problém podle prosperity, bezpečí a stability.

V nabídce živého světa lze také oslovit NPC, která se právě nacházejí ve stejné
lokaci jako hráč. Postava sdílí svou poslední akci a starost frakce; hráč může
jen vyslechnout zprávu, nebo jednou za den pomoci s její konkrétní prosbou.
Léčitelky zlepšují bezpečí, kupci podporují prosperitu a doplňují trh,
informátoři přispívají ke stabilitě a výzkumu. Každá pomoc stojí 10 zlata
a zlepšuje vztah s postavou i přízeň její frakce. Poloha, vztahy i den poslední
pomoci se ukládají do hry.
Při příchodu do lokace hra oznámí jména přítomných NPC a připomene možnost
setkání v nabídce živého světa.

### Městská tržiště a ekonomika

Staré město a Východní Brod mají oddělené, uložené zásoby potravin, dřeva,
kamene, železa a krystalů. Na tržišti v živém světě lze suroviny nakupovat
i prodávat; ceny se mění podle místní prosperity, stability a množství zboží.
Sklady se každý den doplňují a jejich stav přetrvá načtení hry. Denní činnosti
frakcí navíc mění místní zásoby: hlídky či jiné skupiny spotřebovávají proviant
a materiál, zatímco obchodníci doplňují zásoby. Tyto změny se promítají do
množství zboží a dynamických cen. Prodejní cena je nižší než nákupní, aby
opakované obchodování nevytvářelo zisk bez rizika.

Denní příjem panství je umírněnější a závisí na zvolené daňové politice,
hodnosti, trhu a hospodářském stavu Starého města. Kruté daně přinášejí více
zlata, ale dál snižují stabilitu a zvyšují pozornost inkvizice; laskavá správa
má menší výnos a podporuje stabilitu.

### Události, návaznosti a karavany

Městské situace se pravidelně objevují v omezené frontě. Hráč může zvolit
placenou pomoc, bezplatné řešení nebo nezasahovat. Nevyřešené či odmítnuté
situace mají důsledky pro městské ukazatele a zaznamenávají se do historie.
Některá rozhodnutí naplánují pokračování o několik dní později, například
oživení tržiště, bezpečnější čtvrť nebo potíže se zásobami.

Každý dvanáctý herní den může město s nejhorším souhrnným stavem dostat
iniciativu jedné z frakcí, která v něm působí. Situaci přináší konkrétní NPC,
její text vychází ze starosti frakce a poslední zaznamenané akce postavy.
Podpora zlepší odpovídající ukazatel města, reputaci frakce i vztah s poslem;
ignorování naopak zhorší místní stav a vztah. Iniciativy a jejich průběh se
ukládají společně se stavem živého světa.

Městské události navíc reagují na krizi: pokud prosperita nebo bezpečí klesnou
na 30 či méně, další situace se zaměří na karavanu či nedostatek zásob, případně
na hlídky. Při nízké stabilitě vznikne iniciativa místní frakce a NPC; jinak
zůstává běžný kalendářní cyklus událostí zachován.

Karavany cestují po existujících hranách mapy. Jejich bezpečný příjezd může
přinést hráči zlato, městu prosperitu a obchodníkům vliv; špatné podmínky
zásilku odkloní. Přehled živého světa ukazuje současné karavany, vztahy
frakcí, nadcházející návazné situace a poslední změny.

### Rozvoj sídla

Panství lze postupně rozšířit z **Černé tvrze** přes **Opevněné sídlo** a
**Citadelu** až na **Hrad** a **Velký hrad**. Každé rozšíření spotřebuje zlato,
dřevo, kámen a železo; vyšší stupně navíc vyžadují odpovídající hradby, kasárna
a tržiště. Náklady jsou zobrazené před stavbou. Starší uložené hry si zachovají
dosavadní úroveň, budovy a světový stav; nové tržní sklady se doplní při načtení.

Simulace je lokální herní logika, nikoli generativní online AI. Její vývoj
vychází z uloženého stavu, pravidel systému a herního dne; veškerá rozhodnutí
hráče zůstávají pod jeho kontrolou.

## Personál a armádní rozkazy

V menu personálu lze najmout průzkumníka, herolda, správce zásob, polního
lékaře nebo válečného velitele. Pracovník má specializaci, denní mzdu, město
působení, zkušenosti a poslední zaznamenanou akci. Mise přinášejí například
objevené lokace, reputaci, příjem, léčení, bezpečí či morálku armády.

Každému pracovníkovi lze nastavit cílové město a styl mise:

- **Vyváženě** — základní účinky a mzda.
- **Úsporně** — denní mzda je nižší.
- **Podpora města** — vyšší mzda a dodatečná stabilita cílového města.
- **Intenzivně** — vyšší mzda a dodatečná prosperita cílového města.

Armáda může hlídkovat, cvičit, patrolovat území nebo podniknout riskantní
tažení. Žold a výsledek závisí na nastavení, počtech vojáků a kapitánů, morálce
a síle oddílů. Starší pracovníci v uložených hrách dostanou výchozí vyvážený
styl mise.

## Kasino a hazard

Volba **38** otevře kasino U Červené čtvrti. Založení stojí 300 zlata; každé
vylepšení rozšiřuje maximální sázku o 100 zlata a zvyšuje denní příjem podniku.
Kasino má nejvýše pět úrovní, sázky jsou celé částky od 10 zlata do aktuálního
limitu a hráč nemůže vsadit více, než má.

- **Kostky:** zvol „pod 7“ nebo „nad 7“ při hodu dvěma šestistěnnými kostkami.
  Součet 7 vrací sázku; správný tip vyplácí dvojnásobek vsazené částky včetně
  původní sázky.
- **Duel v kostkách:** ty i soupeř hodíte dvěma kostkami; vyšší součet bere
  výhru, při remíze se sázka vrací. Hraje se výhradně o herní zlato.
- **Jednadvacet:** ber karty nebo zůstaň; eso má hodnotu 11 nebo 1 podle toho,
  co zabrání překročení 21. Krupiér dobírá do 17. Běžná výhra vrací dvojnásobek
  sázky a přirozený blackjack vyplácí čistý zisk 1,5násobku sázky.
- **Evidence:** podnik ukládá nejvýše 20 posledních her, počet výher, proher a
  remíz, celkově vsazené zlato a čistý výsledek. Kasino také přidává
  10 zlata za herní den na každou úroveň.

Výsledky hazardních her používají náhodné hody. Sázky jsou omezené a
ovlivňují herní zlato; hra nikdy nepoužívá člověka jako sázku ani výhru.
Před potvrzením sázky se zobrazuje limit i dostupné prostředky.

## Laboratoř a pěstírna

Volba **39** otevře fiktivní provoz laboratoře a pěstírny konopí. Za zlato lze
vybudovat a až na třetí úroveň rozšířit obě zařízení. Abstraktní sklizeň
spotřebuje zásoby pevnosti a doplní sklad konopných květů a bylinných zásob;
laboratoř z nich a z krystalů vyrábí jeden z jedenácti fikčních produktů
uvedených v herním katalogu. Sklizeň i výroba přidávají výzkumné body.

Produkty a konopné květy lze ze skladu prodávat za pevně stanovené herní ceny.
Úrovně provozů, sklad, tržby i získané výzkumné body se ukládají s hrou.
Jde výhradně o abstraktní herní ekonomiku, nikoli o skutečný návod k pěstování
nebo výrobě drog.

## Dominion, ekonomika a frakce

Pevnost je základna pro budovy, zásoby a rozvoj. Budovy zvyšují produkci nebo
odemykají funkce; tržiště může provozovat obchodní smlouvy, jejichž výsledek
závisí na dostupných surovinách. Městská ekonomika je ovlivněna bezpečím,
prosperitou, stabilitou, karavanami a činností frakcí.

Systém mafie a území spravuje kontrolu čtvrtí, podniky, příjmy, vojáky,
kapitány, morálku a konflikty s organizacemi. Diplomacie mění reputaci frakcí.
Výzkum odemyká technologické bonusy a crafting zpracovává dostupné předměty
a suroviny. Alchymie vyrábí lektvary podle odemčených receptů a zásob
ingrediencí.

## Postavy, vztahy a rodina

Postavy mají vlastní profily, vlastnosti, zdraví, energii, příběhy a historii
rozhodnutí. Hráč může rozvíjet důvěru, loajalitu a vztahy, plnit osobní i
mapové úkoly a přidělovat postavám různé role. Systém manželství a rodiny
zahrnuje zasnoubení, svatbu a rodinný život; harém, vztahy a významné volby
mají samostatné přehledy.

## Dobrodružství, úkoly a souboje

Mapa, běžné questy, NPC linky a kampaň nabízejí cíle s různými podmínkami
a odměnami. Deník úkolů ukazuje aktivní postup, kalendář zaznamenává události
a kronika uchovává důležité volby. Souboje jsou tahové; aréna přidává
protivníky, postup a odměny. Postava může využívat dovednosti, vybavení,
předměty a dostupnou bojovou podporu.

## Ukládání

Hra nabízí pět save slotů a autosave při přechodu na nový den. Uložené hry
jsou ve formátu JSON; zápis je atomický a starší podporované save se při
načítání migrují. Nové systémy živého světa, NPC, měst, vztahů, karavan,
událostí i rozkazů personálu se ukládají. Starším save se při načtení doplní
bezpečné výchozí hodnoty. Formát budoucí verze, kterou tato hra nezná, se
odmítne místo tichého poškození dat.

Ve Windows se uživatelská data ukládají do adresáře aplikace v `%APPDATA%`.
Konkrétní cestu určuje `config.py`; hlavní soubor používá historický název
`harem_dark_v18_save.json`. Save soubory jsou osobní herní data — před ručními
úpravami si vytvoř kopii.

## Nastavení a přístupnost

Nastavení umožňuje upravit vizuální téma, barvy terminálu, rozložení menu,
obtížnost a vývojářský režim. Vývojářské volby jsou standardně vypnuté.
Barevné vykreslení je doplňkové; běžné číselné volby zůstávají ovladatelné
textem. Vzhled emoji závisí na fontu a terminálu.

## Testování a struktura projektu

Testy spustíš z kořenové složky:

```bash
python -m unittest discover -s tests -q
python -m compileall -q data game models utils tests
```

Hlavní části repozitáře:

| Složka / soubor | Obsah |
|---|---|
| `data/` | Definice měst, mapy, frakcí, postav, předmětů a dalších herních dat |
| `game/` | Pravidla, menu, simulace, questy, souboje, ekonomika a ukládání |
| `models/` | Datové modely hráče, postav, měst, frakcí, armády a dalších systémů |
| `utils/` | Pomocné funkce, rozhodovací logika a výpisy |
| `tests/` | Regresní a systémové testy |
| `main.py` | Vstupní bod hry |
| `launcher.py` | Kontrola prostředí a spuštění |

## Poznámka pro recenzenty

Tento README je popis funkcí projektu, nikoli soubor uživatelských recenzí.
Hodnocení hráčů zde nejsou doplňována ani vydávána za skutečná. Hra je
terminálové RPG v češtině; aktuální stav implementace a případné změny ověř
přímo v repozitáři a v testech.

## Tvůrce a repozitář

**Tvůrce: #LordRusty23**

Zdrojový kód: [WarDroid23/harem_game](https://github.com/WarDroid23/harem_game)
