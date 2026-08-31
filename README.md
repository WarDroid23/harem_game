# Harem Dark – Dark Expansion

Textová erotická RPG hra v terminálu. Hraješ jako pán temného dominia: buduješ harém, láméš vůli otrokyň, spravuješ mafii, uzavíráš sňatky a posouváš se po mapě kampaně.

**Verze:** 22.1-dark  
**Jazyk:** čeština  
**Platforma:** Python 3 (terminál / konzole)

---

## Spuštění

```bash
git clone https://github.com/WarDroid23/harem_game.git
cd harem_game
python3 main.py
```

Žádné externí závislosti – stačí standardní knihovna Pythonu.

---

## O hře

Jsi pán pevnosti a harému. Otrokyně mají **charakter**, **fázi zkázanosti**, **loajalitu**, **důvěru** a vlastní **osud**. Můžeš je trestat, odměňovat, jmenovat **oblíbenkyní**, vzít si **partnerku** nebo **manželku**, posílat je na nájem, lovit nové a rozšiřovat impérium.

Tón hry je temný a explicitní – dominance, degradace, vztahy a politická moc.

---

## Hlavní systémy

### Harém a otrokyně

| Systém | Popis |
|--------|--------|
| **Fáze zkázanosti** | Postupná degradace (až 16 fází v Dark Expansion) – od vzdoru po „prázdnou nádobu“. |
| **Loajalita** | 7 stupňů (Vzbouřenkyně → Absolutní majetek). Ovlivňuje odměny, tresty a riziko útěku. |
| **Odměny a tresty** | Hierarchie odměn (fáze, partnerka, manželka, oblíbenkyně). Tresty stojí temnou energii. |
| **Oblíbenkyně ★** | Jedna vyvolená. Automatické reakce harému (žárlivost, podlézání, noční incidenty). |
| **Partnerka / manželství** | Romance → partnerství → zasnoubení → svatba → potomstvo. |
| **Osudy** | Osobní příběhové větve u jednotlivých postav. |

### Hráč

- **Sexuální a temná energie** – spotřeba při interakcích; každý nový den se **naplní na maximum**.
- **Výdrž** – trénink ve Vývoji postavy zvyšuje **max energii** (strop 250 / 200).
- **Vztahový bonus** – manželka a oblíbenkyně **každý den mírně zvedají max energii**; svatba a jmenování ★ dávají jednorázový impuls.
- **Level, XP, dovednosti** – svádění, obchod, velení, temnota, boj, výdrž…
- **Zlato, reputace, vliv inkvizice**

### Svět a postup

- **Mapa a lokace** – pevnost, trh, přístav, les, hranice…
- **Příběhová kampaň** – kapitoly s cíli
- **Mafie / území** – pasivní příjem
- **Questy a NPC** – úkoly a temné varianty
- **Dražba, lov otrokyň, budovy harému**
- **Souboje, alchymie, crafting, diplomacie, výzkum**
- **Náhodné události** – noční kontroly, žárlivost, temné sny…

---

## Ovládání (herní menu)

| Volba | Akce |
|-------|------|
| **1** | Interakce s otrokyněmi |
| **2** | Nájem otrokyně |
| **3** | Mafie / impérium |
| **4** | Vývoj postavy (dovednosti, **trénink výdrže**, zbraně) |
| **5–9** | Diplomacie, výzkum, domestikace, mapa, kampaň |
| **11** | Lov otrokyň |
| **12** | **Odpočinek / nový den** (plná energie + autosave) |
| **13–19** | Obchod, questy, dražba, budovy, statistiky, souboj, alchymie |
| **20** | Rychlý přehled |
| **23** | **Harém:** péče, odměny, oblíbenkyně, osudy, loajalita |
| **24–25** | Crafting, dobití energie |
| **26** | **Hlavní menu:** uložit / načíst / nastavení |
| **28** | Manželství a rodina |
| **A** | Automatický bezpečný tah |
| **0** | Konec (uloží hru) |

Zkratky: **S** / **L** / **M** → menu 26, **Q** → konec, **A** → auto tah.

### Podmenu 26 – Hlavní menu

1. Uložit hru (JSON, sloty 1–5)  
2. Načíst hru  
3. Nastavení (barvy, obtížnost, **barevná témata**)  
4. Zpět do hry  
0. Ukončit s uložením  

---

## Ukládání (JSON)

- Soubor: `harem_dark_v18_save.json` (+ `_slot2` … `_slot5`)
- Formát: čitelný JSON (`indent=2`, české znaky)
- Atomický zápis + zálohy `.bak` / `.bak2` / `.bak3`
- **Autosave** při každém novém dni (`*_autosave.json`)
- Náhled slotu: den, zlato, velikost harému, ★ oblíbenkyně, čas uložení

---

## Nastavení a témata

**Nastavení → 3) Barevné téma**

1. Temné dominium  
2. Krvavý trůn  
3. Ledová panenka  
4. Zelený had  
5. Růžový hedváb  
6. Monochrom  

---

## Loajalita (stupně)

| % | Titul | Poznámka |
|---|--------|----------|
| 0–14 | Vzbouřenkyně | vysoké riziko útěku |
| 15–29 | Nedůvěřivá | poslouchá ze strachu |
| 30–49 | Opatrná služka | neutrál |
| 50–69 | Oddaná | silnější odměny |
| 70–84 | Věrná otrokyně | útěk nepravděpodobný |
| 85–94 | Zasvěcená | hluboká oddanost |
| 95–100 | Absolutní majetek | útěk = 0 |

Přehled: **23 → 6) Přehled loajality harému**.

---

## Struktura projektu

```
harem_game/
├── main.py              # vstupní bod, menu
├── config.py            # verze, barvy, témata
├── data/                # charaktery, fáze, odměny, tresty, loajalita…
├── game/                # herní logika (harém, odpočinek, save, mafie…)
├── models/              # Hrac, Otrokyně, Harem, Marriage…
└── utils/               # výpis, ASCII ilustrace
```

---

## Tip pro nové hráče

1. Přidej nebo ulov první otrokyni.  
2. Buduj **loajalitu** a **důvěru** (péče v menu 23).  
3. Sleduj **fázi zkázanosti** – odemyká silnější odměny.  
4. Jmenuj **★ oblíbenkyni**, až budeš chtít privilegia i drama v harému.  
5. Každý den (**12**) se energie obnoví naplno a hra se autosave.  
6. Trénuj **výdrž** (4 → 2), ať maximum energie roste.  

---

## Upozornění

Hra obsahuje **explicitní erotický a temný obsah** (dominance, otroctví v herním světě, násilí v narativu). Je určena **výhradně pro dospělé (18+)**.

---

## Licence / autor

Repozitář: [WarDroid23/harem_game](https://github.com/WarDroid23/harem_game)

Dark Expansion – harém, loajalita, odměny, oblíbenkyně, témata, JSON save, výdrž a denní plná energie.
