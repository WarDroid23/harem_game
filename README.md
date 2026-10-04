# ⚔️ Harem Dark — Dark Expansion

> **Textová erotická RPG hra v terminálu. Temné dominium, harém otrokyň, mafie, magie a tahové souboje — vše v češtině.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://github.com/WarDroid23/harem_game)
[![Verze](https://img.shields.io/badge/Verze-22.1--dark-darkred)](https://github.com/WarDroid23/harem_game)
[![Jazyk](https://img.shields.io/badge/Jazyk-čeština-green)](https://github.com/WarDroid23/harem_game)
[![18+](https://img.shields.io/badge/Obsah-18%2B-red)](https://github.com/WarDroid23/harem_game)

---

## ⚠️ Upozornění pro dospělé (18+)

Hra obsahuje **explicitní erotický a temný obsah** — dominance, otroctví v herním světě, násilí v narativu, drogy a černá magie. Je určena **výhradně pro hráče starší 18 let**.

---

## 🚀 Instalace a spuštění

### Varianta A — Dvojklik (Doporučeno)

1. Stáhni nebo naklonuj repozitář
2. Ve složce dvakrát klikni na **`spustit.bat`**
3. Skript automaticky:
   - Ověří instalaci Pythonu
   - Doinstaluje knihovny (`colorama`, `windows-curses`)
   - Spustí hru

### Varianta B — Příkazová řádka

```bash
git clone https://github.com/WarDroid23/harem_game.git
cd harem_game
python launcher.py
python main.py
```

### Požadavky

| Požadavek | Verze |
|-----------|-------|
| Python | 3.10 nebo vyšší |
| OS | Windows 10/11 |
| Terminál | CMD / PowerShell / Windows Terminal |

---

## 📖 Příběh a zasazení

Jsi **pán Černé pevnosti** — temný aristokrat a vládce tajemného dominia na okraji civilizace. Svět kolem tě ovládají tři síly: **Inkviziční církev** (moc a zákon), **Obchodní syndikáty** (peníze a informace) a **Podsvětní klany** (chaos a stíny).

Tvým cílem je **vybudovat harém**, zlomit nebo získat oddanost mocných žen, rozšířit vliv mafie na celé město, zvítězit v bojích na aréně a nakonec se postavit nepřátelům v závěrečné kampani.

Každá otrokyně v harému má **vlastní příběh, charakter a osud**. Ty rozhoduješ, jak s ní naložíš — zda ji zlomíš, osvobodíš, vezmeš si ji za manželku, nebo prodáš nejvyššímu zájemci.

---

## 🕹️ Ovládání — Hlavní menu

Po spuštění hry vstoupíš do hlavního herního menu. Zadáváš čísla nebo písmena a stiskáš Enter.

| Volba | Název | Popis |
|-------|-------|-------|
| `1` | **Interakce** | Výběr otrokyně a interakce s ní (viz níže) |
| `2` | **Nájem** | Pronájem otrokyně za zlato |
| `3` | **Mafie / Impérium** | Správa území, války a nelegální podniky |
| `4` | **Vývoj postavy** | Dovednosti, zbraně, trénink výdrže |
| `5` | **Diplomacie** | Vztahy s frakcemi (Inkvizice, Syndikát, Podsvětí) |
| `6` | **Výzkum** | Technologický strom dominia |
| `7` | **Domestikace** | Hloubkové zlomení vůle a psychologické podmínění |
| `8` | **Mapa světa** | Cestování po 26 lokacích, NPC, questy |
| `9` | **Kampaň** | Hlavní příběhová linie s kapitolami |
| `22` | **Deník úkolů** | Aktivní běžné a NPC úkoly, dostupné úkoly a postup kampaně |
| `11` | **Lov otrokyň** | Získání nových žen (trh, únos, duel) |
| `12` | **Odpočinek / Nový den** | Regenerace energie + autosave |
| `13` | **Obchod** | Nákup a prodej předmětů |
| `14` | **Questy** | Aktivní úkoly a odměny |
| `15` | **Dražba** | Speciální aukce vzácných dívek |
| `16` | **Budovy / Pevnost** | Stavba a správa pevnosti |
| `17` | **Statistiky** | Přehled hodnot hráče, harému a achievementů |
| `18` | **Souboj (Aréna)** | Tahový boj, žebříček, legendy |
| `19` | **Alchymie** | Vaření elixírů a jedů |
| `20` | **Rychlý přehled** | Stav harému a zdrojů na jedné obrazovce |
| `21` | **Nevěstinec** | Správa Rudého sametu, VIP klienti, eventy |
| `T` | **Testovací volba** | Přidá jednu testovací otrokyni (jen ve vývojářském režimu; zachována i stará volba `10`) |
| `23` | **Harém** | Péče, odměny, oblíbenkyně, osudy, loajalita |
| `24` | **Crafting** | Výroba předmětů ze surovin |
| `25` | **Dobití energie** | Rychlá obnova energie za zlato/rituál |
| `26` | **Hlavní menu** | Uložit / Načíst / Nastavení |
| `27` | **Průvodce dominiem** | Základy hry a doporučené další kroky podle aktuálního postupu |
| `28` | **Manželství a rodina** | Zasnoubení, svatba, potomstvo |
| `29` | **Kronika dominia** | Historie rozhodnutí, questů a událostí |
| `30` | **Denní rozkazy** | Naplánování běžných aktivit harému |
| `31` | **Veřejný výkon** | Městská aktivita s odměnou a reputačními následky |
| `32` | **Kalendář a události** | Sezóna a historie posledních událostí světa |
| `A` | **Auto tah** | Bezpečný automatický tah |
| `S/L/M` | Zkratky | Save / Load / Menu |
| `0` | **Konec** | Uložit a ukončit |

Nabídky používají rámečky, barvy a tematické ikony. Emoji se mohou v některých
starších terminálech zobrazit odlišně; číselné volby zůstávají plně funkční.
Hlavní menu navíc ukazuje aktivní cíle a konkrétní doporučený krok včetně
potřebné lokace, volby menu nebo podmínky pro postup kampaní. Stejná priorita
doporučení se používá také v průvodci.
Testovací volba `T` a cheaty `$`, `&`, `#`, `*` a `:` jsou skryté a neaktivní, dokud v nastavení hry
(`26` → `3` → `6`) nezapneš **Vývojářský režim**. V tomto režimu `T` (nebo
zpětně kompatibilní `10`) přidá testovací otrokyni a `$` přidá 10 000 zlata a
doplní energie; `&` přidá 1 000 kusů každé alchymistické suroviny a zásob
pevnosti (jídlo, dřevo, kámen, železo a krystaly); `#` zvýší všechny dovednosti
postavy včetně bojové zdatnosti o 10 a přidá 10 výzkumných bodů; `*` zvýší
všechny budovy i hlavní citadelu o jednu úroveň a `:` nastaví loajalitu, důvěru
i body romance všech otrokyň na 100. Režim je
uložený v save a je standardně vypnutý.
Náhodné události při odpočinku se vybírají podle místa, roční doby, stavu harému
a hrozeb ve světě; jejich historii najdeš v kalendáři (`32`).

---

## 👑 Systém Harému

### Statistiky otrokyně

Každá dívka má tyto základní hodnoty (0–100):

| Statistika | Popis |
|-----------|-------|
| **Loajalita** | Jak moc ti je oddaná. Ovlivňuje útěk, odměny, arénu. |
| **Důvěra** | Psychologická blízkost. Otvírá osobní příběhy. |
| **Submisivita** | Míra podřízenosti. Roste tresty a podmíněním. |
| **Strach** | Respekt z moci. Ovlivňuje reakce na tresty. |
| **Touha** | Erotické vzrušení. Zvyšují ho intimní interakce. |
| **Zkaženost** | Stupeň morální degradace (0–16 fází). |
| **Energie** | Kolik interakcí dnes ještě zvládne. |

### Fáze zkaženosti (0–16)

Fáze se zvyšuje při opakovaných interakcích a trestech. Každá nová fáze odemyká silnější akce a speciální dialogy. Finální fáze „Prázdná nádoba" = absolutní poddanost.

### Stupně loajality

| % | Titul | Efekt |
|---|-------|-------|
| 0–14 | 🔴 Vzbouřenkyně | Vysoké riziko útěku, odpor |
| 15–29 | 🟠 Nedůvěřivá | Poslouchá ze strachu |
| 30–49 | 🟡 Opatrná služka | Neutrální postoj |
| 50–69 | 🟢 Oddaná | Silnější odměny, žádný útěk |
| 70–84 | 💚 Věrná otrokyně | Bojová společnice, bonusy |
| 85–94 | 💙 Zasvěcená | Hluboká oddanost, speciální questy |
| 95–100 | 💜 Absolutní majetek | Nulové riziko útěku, max. odměny |

### Vztahy a role

- **★ Oblíbenkyně** — jedna vyvolená; harém reaguje žárlivostí a podlézáním
- **Partnerka** — romantický vztah s osobními eventy
- **Manželka** — zasnoubení → svatba → rodinný život a potomstvo
- **Bojová společnice** — loajalita 70+, doprovází tě do soubojů

---

## 🗣️ Interakce (Menu 1)

Po výběru otrokyně se zobrazí seznam dostupných interakcí. Každá spotřebuje **sexuální nebo temnou energii** a ovlivní statistiky.

### Profily, povahy a přehledy

Nové členky harému dostávají jedinečná jména z rozšířeného seznamu a jednu z
dostupných povah. Mezi nové archetypy patří badatelka, diplomatka, ochranitelka
a umělkyně; povaha ovlivňuje reakce na rozhovor i běžné interakce. Starší
varianty názvů povah se při načtení převedou na platný archetyp.

V menu **23** najdeš souhrn harému s grafickými ukazateli důvěry, loajality a
zdraví, rozdělení povah, profily a historii rozhodnutí. Osobní nabídka přidává
rozhovor o přáních postavy: můžeš jí naslouchat, povzbudit její silnou stránku
nebo společně vyjasnit hranice. Volba rozhovoru se zaznamená do její historie.
Menu **17** nově vykresluje grafy zdraví, energie, postupu, dovedností,
charakterů harému, vlivu mafie a reputace frakcí.

Každá povaha má také osobní třídílný příběh (volba **12** v osobní nabídce).
Příběh se rozvíjí rozhovory a důvěrou; hráč může naslouchat nebo nabídnout
pomoc, ale rozhodnutí postavy zůstává její. Osobní deník (volba **13**) shrnuje
její přání, stav příběhu a důležité volby. Volba **14** ukazuje graf statistik
v čase; hodnoty se zaznamenávají po významných interakcích a při uzavření dne.

Vybrané povahy poskytují i praktické schopnosti: badatelka zlevňuje výzkum,
diplomatka posiluje kladné diplomatické zisky, ochranitelka přidává obranu jako
bojová společnice a umělkyně zvyšuje denní příjem harému. Schopnosti mají
podmínky důvěry a nevztahují se na členky, které jsou právě na nájmu.

### Hlavní kategorie interakcí

| Kategorie | Příklady akcí |
|-----------|--------------|
| **Základní** | Rozkaz, Výcvik, Pokárání, Chvála |
| **Intimní** | Políbení, Objetí, Masáž, Olejová masáž celého těla |
| **Dominantní** | Svazování, Bičování, Hypnotický pohled, Znacka dominia |
| **Psychologické** | Hypnóza, Zkouška oddanosti, Iluze svobody |
| **Taneční** | Soukromý tanec, Rituální tanec stínů |
| **Speciální** | Alchymická proměna, Rituál temné přísahy |

### Podání drog (podmenu Drogy)

V menu interakcí → **Drogy** → číslovaný seznam všech dostupných látek:

| # | Název | Efekt |
|---|-------|-------|
| 1 | Lektvar poddajnosti | Submisivita +15, Vůle −10 |
| 2 | Elixír touhy | Touha +25, Inhibice −20 |
| 3 | Prach zapomnění | Resetuje vzpomínky na den |
| 4 | Kapky strachu | Strach +30 |
| 5 | Serum pravdy | Odhalí skryté statistiky |
| 6 | Temný nektar | Zkaženost +2, Touha +20 |
| 7 | Aurora pryskyřice | Loajalita +10, Halucinace |
| 8 | Snovová mlha | Poddajnost, sny |
| 9 | Démonská extáze | Silný efekt zkaženosti |
| 10 | Dračí krev | Síla a touha, riziko |
| + | *Vyrobené v alchymii* | Dle receptu |

---

## 🏰 Pevnost a Budovy (Menu 16)

Pevnost je tvoje základna. Budováním zvyšuješ produkci zdrojů a odemykáš nové možnosti.

### Suroviny pevnosti

| Ikona | Surovina | Použití |
|-------|---------|---------|
| 🪵 | Dřevo | Stavba, crafting |
| 🪨 | Kámen | Pevnostní budovy |
| ⚒️ | Kov | Zbraně, armatura |
| 🌾 | Jídlo | Udržování posádky |
| 🔮 | Temná esence | Magie, rituály, elixíry |

### Budovy pevnosti

| Budova | Efekt |
|--------|-------|
| **Kasárna** | Trénink vojáků, vyšší obrana |
| **Alchymistická věž** | Výroba lektvarů a jedů |
| **Harémový palác** | Bonus k loajalitě a pohodlí |
| **Trhliště** | Pasivní příjem zlata |
| **Temná kaple** | Temná energie, rituály |
| **Zbrojnice** | Přístup k lepším zbraním |
| **Bylinkový skleník** | Denní produkce bylin pro alchymii |
| **Alchymistická laboratoř** | Rychlejší vaření receptů, bonus kvality |
| **Studna moci** | Větší max. energie hráče |

### Správa personálu (Menu 16 → Personál)

| Role | Náklady | Efekt |
|------|---------|-------|
| Správce (Majordomus) | 500 🪙 | +20% příjem ze všech zdrojů |
| Léčitel (Šaman) | 400 🪙 | Denní obnova HP vojáků |
| Zahradník (Alchymista) | 350 🪙 | +50% produkce bylinkového skleníku |

---

## ⚗️ Alchymie (Menu 19)

Sbírej suroviny z mapy a vař lektvary v alchymistické věži.

### Recepty (výběr)

| Název | Suroviny | Efekt |
|-------|---------|-------|
| Lektvar síly | Kořen + Krev | +20 útok na 3 tahy |
| Elixír touhy | Růže + Nektar | Touha +30 |
| Jed bolesti | Durman + Síra | Nepřítel −HP/tah |
| Temný nektar | Tma + Med | Zkaženost +1, Touha +15 |
| Elixír věčného mládí | Drak. šupina + Modrá hvězda + Luna | Obnoví HP na max |
| Sérum absolutní poslušnosti | Mandra. kořen + Temná esence + Krev | Submisivita +40 |
| Elixír berserkra | Rudý mech + Drak. krev + Žluč | Útok ×3 na 2 tahy |

---

## ⚔️ Souboje a Aréna (Menu 18)

Tahový bojový systém s plnou mechanikou.

### Bojové akce

| Volba | Akce | Popis |
|-------|------|-------|
| `1` | Útok | Základní fyzický útok |
| `2` | Přesný útok | Vyšší poškození, může minout |
| `3` | Obrana | Snížení příchozího dmg na 1 tah |
| `4` | Temný vampirismus | Ukradne HP soupeři |
| `5` | 💃 Asistence společnice | Speciální útok partnerky |
| `6` | Předmět | Použití lektvaru nebo předmětu |
| `7` | Zastrašení | Psychický útok, snižuje morálku |
| `8` | Útěk | Pokus o opuštění boje |

### Bojová společnice

Pokud má dívka **loajalitu 70+**, může být přiřazena jako **bojová společnice** (Menu 1 → Interakce → Přiřadit bojovou společnici). V boji asistuje vlastním speciálním útokem dle svého archetypu:

| Archetyp | Bojová schopnost |
|---------|-----------------|
| Kurtizána | Zmatenost soupeře (vynechá tah) |
| Válečnice | Silný fyzický úder |
| Čarodějka | Magický plošný útok |
| Assassin | Kritický bod slabosti |
| Dračí míšenka | Dračí výdech (oheň) |

### Aréna — Žebříček

Postupuj žebříčkem a porážej stále silnější protivníky. Na vrcholu čekají **legendární bossové** s více fázemi a speciálními schopnostmi.

---

## 🗺️ Mapa světa — 26 lokací (Menu 8)

Cestuj po světě, prozkoumávej lokace a plň lokační úkoly.

### Kategorie lokací

| Typ | Příklady lokací | Co zde najdeš |
|-----|----------------|--------------|
| **Město a řemesla** | Trh, čtvrť řemeslníků, palác, přístav | Obchod, reputace, zásoby a kontakty |
| **Příroda a zahrady** | Mlžný les, Háj soumraku, Skleněná zahrada | Suroviny, odpočinek a skryté stezky |
| **Magie a ruiny** | Akademie, observatoř, astrální citadela | Zkušenosti, alchymie a průzkum mapy |
| **Nebezpečná místa** | Krvavý lom, katakomby, aréna, žalář | Odměny, rizikové výpravy a příběhové volby |
| **Společenská místa** | Lázně, hostinec, Stříbrné terasy, zahradní altán | Regenerace, vztahy a městská pověst |

### Lokační akce

Každá z 26 lokací má vlastní pověst a nabídku tematických akcí. Podle místa
můžeš získat suroviny pro pevnost či alchymii, zkušenosti, energii, reputaci,
vztahy s NPC, vliv frakcí nebo odhalit dosud skrytou cestu. Některé akce mají
cenu či riziko; před potvrzením zkontroluj požadované zlato a suroviny.

### Navazující úkoly NPC

Rozhovory s Mírou, Lyrou, Cassianem, Terezou, Selene a Lady Eleanor mohou po
získání jejich důvěry odemknout vícedílné úkoly. Každý úkol uchovává přijatou
variantu i v uložené hře a nabízí čestné či temné řešení s odlišnými odměnami.
Některé odměny jsou mapové nástroje nebo předměty, které ovlivňují další
průzkum a reputaci frakcí.

---

## 🏛️ Nevěstinec — Rudý samet (Menu 21)

Postav a provozuj nevěstinec v Červené čtvrti (300 🪙 na start).

### Mistnosti (specializace)

| Místnost | Bonus | Popis |
|---------|-------|-------|
| **Standardní** | — | Základní místnost |
| **VIP komnata** | +50% zisk | Luxus pro bohaté klienty |
| **Temná komnata** | +temná energie | Rituální prožitky |
| **Terapeutická** | +důvěra dívky | Klidná atmosféra |
| **Místnost zrcadel** | +submisivita | Narcistní iluze |
| **Astrální komnata** | +magická energie | Mystická spojení |

### VIP Klienti

| Klient | Požadavek | Odměna |
|--------|----------|--------|
| Kupec | Charisma dívky 50+ | Zlato, obchodní kontakty |
| Sadista | Zkaženost dívky 5+ | Vyšší zlatá odměna |
| Vojáci | Submisivita 60+ | Vojenský vliv |
| Kultista | Temná energie | Rituální předměty |
| Inkvizitor | Diskrétnost | Snížení vlivu Inkvizice |
| Otrokář | Loajalita nízká | Prodejní nabídka |
| Šlechtic | Celkový luxus | Diplomacie, renomé |

### Eventy nevěstince

- **Divoká noc** — mimořádný zisk, ale únava dívek
- **Inspekce Inkvizice** — úplatek nebo skandál
- **VIP večírek** — bonusové reputace a aliance
- **Mravnostní razie** — možnost úplatku stráží

---

## 🕵️ Mafie a Impérium (Menu 3)

Buduj podsvětní říši kontrolováním území a vedením syndikátních válek.

### Území a kontrola

| Akce | Popis |
|------|-------|
| Koupit území | Připoj novou čtvrť pod svou kontrolu |
| Vylepšit kontrolu | Zvyš % kontroly = vyšší příjem |
| Nelegální podniky | Doupata, nevěstince, herny, pašerácké sklady, padělatelské dílny a tajné arény |
| Vydírání hodnostářů | Pasivní příjem + oslabení soupeře |

Dostupná síť nyní zahrnuje 16 čtvrtí, včetně Dýmové čtvrti, Cechovních uliček,
Půlnočního trhu, Starých katakomb, Kovárenského okrsku, Lucernové čtvrti,
Severních hradeb a Akademického náměstí. Převzetí čtvrti mění reputaci
odpovídajících frakcí. Podniky lze pořizovat v každém vlastněném území; vedle
stávajících provozů přibyly informační burza, černá slévárna a tajný archiv.
Jejich výnos se přičítá k pasivnímu příjmu mafie. Přehled mafie zobrazuje
panorama podsvětí, síť území s ukazatelem kontroly a seznam dosud volných čtvrtí.

### Syndikátní války

Napadni jiné organizace a přeber jejich území:

| Cíl | Obtížnost | Kořist |
|-----|----------|--------|
| Přístavní cech pašeráků | Snadná | Zlato, přístav |
| Syndikát Nočních stínů | Střední | Vliv, informátoři |
| Krvavý kult podsvětí | Těžká | Rituální předměty |
| Inkviziční garda | Extrémní | Oslabení Inkvizice |
| Železný baron Vargan | Boss | Výzkumné body a vliv v Podsvětí |
| Vévoda beze jména | Boss | Výzkumné body a vliv u Syndikátu stínů |

Vítězství nad bossy navíc přináší výzkumné body. Některé nové čtvrti odemykají
vlastní úkoly a události. Technologie **Síť informátorů** zvyšuje denní
produkci výzkumu podle počtu ovládaných území, zatímco **Účetní knihy podsvětí**
zvyšují jejich denní výnos. Nový obsah používá stávající save data, migrace
není potřeba; poražení bossové se ukládají a odměnu lze získat jen jednou.

### Strategie útoku

1. **Frontální nápor** — vojáci a kapitáni v plné síle
2. **Skrytá sabotáž** — vyžaduje informátory a korupci
3. **Temný úder dominia** — spotřebuje 15 temné energie pro silný bonus

---

## ⚖️ Obtížnost a odměny

Obtížnost ovlivňuje souboje, expedice, běžné a NPC questy i vybrané ceny:

| Obtížnost | Síla nepřátel a jejich poškození | Odměny ve zlatě | Zkušenosti | Ceny |
|-----------|----------------------------------|-----------------|------------|------|
| Lehká | ×0,85 | ×1,15 | ×1,10 | ×0,85 |
| Normální | ×1,00 | ×1,00 | ×1,00 | ×1,00 |
| Těžká | ×1,20 | ×1,25 | ×1,20 | ×1,15 |

Odměny za splněný úkol se připisují ihned. Souhrnný ukazatel questových a
bojových bonusů v hlavním menu zobrazuje dosud získanou částku, nikoli
nevyzvednutý zůstatek.

---

## 📜 Osobní osudy a questliny

Vedle osobních příběhových linií nabízí mapa také navazující úkoly NPC.
Postup úkolu, jeho větev i odměna zůstávají zachovány při uložení a načtení hry.

Každá dívka může mít svůj unikátní questline. Speciální questliny mají tyto protagonistky:

| Dívka | Questline | Téma |
|-------|-----------|------|
| **Elena** | Pomsta Eleny | Tajemství minulosti, krvavé odhalení |
| **Scarlett** | Sestra Scarlett | Rodinné vazby, volba loajality |
| **Lyra** | Stříbrný prsten Lyry | Prokletý artefakt, romantika |
| **Vespera** | Grimoire Vespery | Černá magie, pakt s démony |

Questliny se aktivují automaticky po dosažení dostatečné **Důvěry** a průzkumu příběhu dívky.

---

## 🧬 Archetypy postav

Při lovu nebo nákupu otrokyně se vygeneruje jeden z těchto archetypů:

| Archetyp | Silná stránka | Speciální vlastnost |
|---------|--------------|-------------------|
| Kurtizána | Charisma, Touha | Bonus příjem v nevěstinci |
| Válečnice | Síla, Výdrž | Bojová společnice od loajality 50+ |
| Čarodějka | Magie, Temná energie | Rituály a alchymie s bonusem |
| Assassin | Rychlost, Přesnost | Tajné mise na mapě |
| Šlechtična | Diplomacie, Intrika | Frakční bonusy |
| Kněžka | Víra, Léčení | Obnoví HP po souboji |
| Obchodnice | Zlato, Trhy | +10% příjem z nájmu |
| Lovkyně | Průzkum, Příroda | Bonus suroviny z lokací |
| **Královská kněžka** | Magie + Víra | Dual-efekt rituálů |
| **Dračí míšenka** | Oheň + Síla | Ohnivý útok v souboji |
| **Temná elfka** | Stíny + Magie | Neviditelnost, kritické údery |

---

## 🔬 Výzkum a technologický strom (Menu 6)

Technologie stojí zlato i výzkumné body. Každá větev začíná samostatnou
základní technologií; další uzly vyžadují předchozí výzkum ve stejné větvi.
Strom zobrazuje dostupné, dokončené i uzamčené technologie, jejich cenu a
aktuální zásobu bodů.

| Větev | Technologie a bonusy |
|-------|----------------------|
| **Magie** | Temná energie a silnější temné útoky |
| **Hospodářství** | Okamžité zlato a rostoucí denní příjem |
| **Infiltrace** | Snížení vlivu Inkvizice a sleva na další výzkum |
| **Válečnictví** | Trvalé bonusy k útoku a obraně v soubojích |

Výzkumné body každý den vyrábí **Temný archiv & Knihovna** (+3 body za úroveň)
a **Alchymistická laboratoř** (+1 bod za úroveň). Vylepši tyto budovy v menu
16. Výzkumná síť badatelky a technologie infiltrace navíc zlevňují zlatou část
ceny. Zásoba bodů, dokončené technologie i bonusy se ukládají do save.

---

## 💊 Drogy a Alchymie

### Vaření elixírů (Menu 19)

1. Získej suroviny (průzkum mapy, obchod, pevnostní skleník)
2. Otevři Alchymii → vyber recept
3. Pokud máš všechny ingredience, elixír se uvaří
4. Uvarené elixíry se přidají do zásob a jsou dostupné při interakcích

### Podání drogy dívce

`Menu 1 → Interakce → Dívka → Drogy → [číslo drogy]`

Drogy mají **okamžitý** nebo **přetrvávající** efekt (trvá až do nového dne).

---

## 💾 Ukládání a načítání

### Sloty (1–5)

- JSON formát, čitelný, s českými znaky
- Atomický zápis + zálohy `.bak`, `.bak2`, `.bak3`
- **Autosave** při každém novém dni

### Náhled slotu

Před načtením uvidíš: den, zlato, velikost harému, ★ oblíbenkyně, čas uložení.

### Cesta k uloženým hrám

```
%LOCALAPPDATA%\Temp\  (nebo složka hry)
harem_dark_v18_save_slot1.json
harem_dark_v18_save_slot1.bak
harem_dark_v18_autosave.json
```

---

## 🎨 Barevná témata

`Menu 26 → Nastavení → 3) Skin / barevné schéma`

| # | Téma | Popis |
|---|------|-------|
| 1 | **Temné dominium** | Výchozí — tmavá fialová a červená |
| 2 | **Krvavý trůn** | Sytá červená a zlatá |
| 3 | **Ledová panenka** | Studená modrá a stříbrná |
| 4 | **Zelený had** | Jedovatě zelená a temná |
| 5 | **Růžové hedvábí** | Jemná růžová a fialová |
| 6 | **Monochrom** | Elegantní odstíny šedi |
| 7 | **Azurový krystal** | Tyrkysová, safírová a stříbrná |
| 8 | **Smaragdový dvůr** | Smaragdová a teplá zlatá |
| 9 | **Jantarový pokoj** | Jantarová, měděná a vínová |
| 10 | **Půlnoční nebe** | Indigová a noční modř |
| 11 | **Ohnivý fénix** | Žhavá červeň, oranžová a měď |
| 12 | **Lesní duch** | Mechová zeleň a měsíční stříbro |
| 13 | **Neonová metropole** | Elektrická tyrkysová a růžová |

Skin mění sémantickou barevnou paletu napříč herním rozhraním a v nastavení
zobrazuje barevný náhled. Barvy terminálu lze nezávisle vypnout volbou **1**.

V nastavení najdeš také **7) Styl hlavního menu**:
- **Kategorie v rámečcích** — čtyři tematické panely.
- **Seznam bez kategorií** — původní jednoduchý seznam všech voleb.
- **Kompaktní dva sloupce** — úspornější zobrazení bez rámečků.
- **Sekce bez rámečků** — kategorie jsou barevně oddělené nadpisy.
- **Třísloupcová mřížka** — zkrácené názvy šetří místo na obrazovce.

Skin i rozložení menu se ukládají do uložené hry. Starší uložené hry automaticky
dostanou výchozí temný skin a kategorické menu.

---

## 💡 Tipy pro nové hráče

1. **Začni** přidáním nebo ulovením první otrokyně (menu `11`)
2. **Buduj loajalitu a důvěru** v sekci Péče (menu `23`) — bez toho se nedostaneš k osobním questům
3. **Každý den** (`12`) se energie obnoví naplno a spustí se autosave
4. **Trénuj výdrž** (`4 → 2`), ať maximum energie roste nad výchozích 100
5. **Postav nevěstinec** (`21`) co nejdříve — pasivní příjem zlata tě udrží
6. **Prozkoumávej mapu** (`8`) — lokace dávají suroviny, nové dívky i questliny
7. **Spravuj mafii** (`3`) — územní příjem je nejrychlejší cesta k bohatství
8. **Jmenuj ★ oblíbenkyni** až budeš chtít harémová dramata a privilegia
9. **Přiřaď bojovou společnici** (loajalita 70+) — výrazně usnadní souboje
10. **Čti Kroniku** (`29`) — zaznamenává tvá důležitá rozhodnutí

---

## ⚡ Energie a zdroje hráče

| Zdroj | Max | Obnovení | Použití |
|-------|-----|---------|---------|
| Sexuální energie | 100–250 | Každý nový den | Interakce, rituály |
| Temná energie | 100–200 | Každý nový den | Souboje, tresty, magie |
| Zlato 🪙 | Neomezené | Příjem, questy, mafie | Nákupy, stavba, armáda |
| XP | — | Souboje, questy | Level up, dovednosti |

---

## 📐 Struktura projektu

```
harem_game/
├── main.py              # Vstupní bod
├── launcher.py          # Chytrý spouštěč s auto-instalací
├── spustit.bat          # Windows double-click launcher
├── config.py            # ANSI barvy a konstanty
├── data/                # Herní data (drogy, zbraně, interakce...)
│   ├── drogy.py         # Definice všech drog
│   ├── interakce.py     # Seznam interakcí
│   ├── charaktery.py    # Archetypy postav
│   ├── zbrane.py        # Zbraně a armatury
│   ├── klienti.py       # VIP klienti nevěstince
│   └── osudy.py         # Osobní questliny
├── models/              # Datové třídy
│   ├── otrokyne.py      # Model otrokyně
│   ├── harem.py         # Model harému
│   ├── fortress.py      # Model pevnosti a budov
│   ├── mafie.py         # Model mafie a území
│   └── nevestinec.py    # Model nevěstince
├── game/                # Herní logika
│   ├── menu_hlavni.py   # Vykreslení hlavního herního menu
│   ├── souboje.py       # Tahové souboje
│   ├── budovy.py        # Správa pevnosti
│   ├── mafie.py         # Mafie menu
│   ├── alchymie.py      # Alchymický systém
│   ├── svet.py          # Mapa světa a lokace
│   └── nocni_eventy.py  # Noční harémové eventy
├── tests/
│   └── test_game.py     # Regresní a systémové testy
└── NOVE_SYSTEMY.md      # Dokumentace nových systémů
```

---

## 🧪 Testování

```bash
python -m unittest tests/test_game.py
```

Před vydáním musí projít celá sada testů.

---

## 📝 Changelog (Nejnovější)

### v22.1-dark (aktuální)
- ✅ 5 nových interakcí (olejová masáž, hypnóza, soukromý tanec, znacka dominia, zkouška oddanosti)
- ✅ 3 nové archetypy (Královská kněžka, Dračí míšenka, Temná elfka)
- ✅ 2 nové mistnosti nevěstince (Zrcadla, Astrální komnata)
- ✅ 4 nové drogy (Aurora pryskyřice, Snovová mlha, Démonská extáze, Dračí krev)
- ✅ 4 osobní questliny (Elena, Scarlett, Lyra, Vespera)
- ✅ Nelegální podniky a vydírání v mafii
- ✅ Bylinkový skleník a Alchymistická laboratoř v pevnosti
- ✅ Správa personálu pevnosti (Majordomus, Šaman, Zahradník)
- ✅ Noční harémové eventy (sesterství, koupelna, dary)
- ✅ Bojová společnice systém

---

## 🔗 Repozitář

**GitHub:** [WarDroid23/harem_game](https://github.com/WarDroid23/harem_game)

*Dark Dominion — Dark Expansion | Verze 22.1-dark | Výhradně pro dospělé 18+*
