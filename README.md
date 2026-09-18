# Harem Dark - Dark Expansion

Textová erotická RPG hra v terminálu. Hraješ jako pán temného dominia: buduješ harém, lámeš vůli otrokyň, spravuješ mafii, bojuješ v tahových soubojích a posouváš se po mapě kampaně.

**Verze:** 22.1-dark  
**Jazyk:** Čeština  
**Platforma:** Windows (Python 3.10+)

---

## 🚀 Spuštění hry (Nové)

Hra nyní obsahuje chytré launchery, které automaticky nainstalují potřebné závislosti a spustí hru.

### Varianta A: Dvojklik (Doporučeno pro Windows)
Stačí ve složce s hrou dvakrát kliknout na soubor **`spustit.bat`**. 
- Skript ověří, zda je nainstalován Python.
- Automaticky doinstaluje grafické knihovny (`colorama`, `windows-curses`).
- Spustí hru a po jejím ukončení počká na stisk klávesy.

### Varianta B: Příkazová řádka
```bash
git clone https://github.com/WarDroid23/harem_game.git
cd harem_game
python launcher.py
```
*(Soubor `launcher.py` zajistí to samé jako .bat, ale z PowerShellu nebo klasické konzole, a elegantně zachycuje pády a crashe).*

---

## 📖 O hře

Jsi pán pevnosti a harému. Otrokyně mají **charakter**, **fázi zkaženosti**, **loajalitu**, **důvěru** a vlastní **osud**. Můžeš je trestat, odměňovat, jmenovat **oblíbenkyní**, vzít si **partnerku** nebo **manželku**, posílat je na nájem, lovit nové a rozšiřovat impérium.

Tón hry je temný a explicitní - dominance, degradace, vztahy a politická moc.

---

## ⚔️ Hlavní systémy

### Harém a otrokyně

| Systém | Popis |
|--------|--------|
| **Fáze zkaženosti** | Postupná degradace (až 16 fází v Dark Expansion) - od vzdoru po "prázdnou nádobu". |
| **Loajalita** | 7 stupňů (Vzbouřenkyně -> Absolutní majetek). Ovlivňuje odměny, tresty a riziko útěku. |
| **Odměny a tresty** | Hierarchie odměn. Tresty stojí temnou energii a ovlivňují strach i submisivitu. |
| **Oblíbenkyně ★** | Jedna vyvolená. Automatické reakce harému (žárlivost, podlézání, noční incidenty). |
| **Partnerka / manželství** | Romance -> partnerství -> zasnoubení -> svatba -> potomstvo. Soužití v rodině. |
| **Osudy** | Osobní příběhové větve u jednotlivých postav s vícero konci. |

### Pán a Dominium

- **Sexuální a temná energie** - spotřeba při interakcích; každý nový den se **naplní na maximum**.
- **Výdrž** - trénink ve Vývoji postavy zvyšuje **max energii** (strop 250 / 200).
- **Zlato, reputace, vliv inkvizice** - měny, které hýbou světem. Získávej je z questů, mapy a mafie.
- **Barevné UI s bary** - Herní interface nyní obsahuje boxované informační panely a vizuální HP/Energie bary.

### Svět a RPG

- **Mapa světa** - Barevná ASCII mapa spojující pevnost, trh, přístav, lesy, červenou čtvrť.
- **Tahové souboje** - Útoky, obrana, speciální temné údery, zastrašování a upravený bojový HUD s HP bary.
- **Příběhová kampaň** - Kapitoly s postupnými cíli.
- **Mafie / území** - Získej podsvětí pod kontrolu pro pasivní příjem.
- **Alchymie & Crafting** - Sbírej suroviny a vař elixíry či vyrob nástroje.

---

## 🕹️ Ovládání (herní menu)

| Volba | Akce |
|-------|------|
| **1** | Interakce s otrokyněmi (výpis karet s HP/Loajalita bary) |
| **2** | Nájem otrokyně (ekonomika) |
| **3** | Mafie / impérium |
| **4** | Vývoj postavy (dovednosti, **trénink výdrže**, zbraně) |
| **5-9** | Diplomacie, výzkum, domestikace, mapa (barevný lokátor), kampaň |
| **11** | Lov otrokyň |
| **12** | **Odpočinek / nový den** (plná energie + autosave) |
| **13-19** | Obchod, questy, dražba, budovy, statistiky, souboj, alchymie |
| **20** | Rychlý přehled |
| **23** | **Harém:** péče, odměny, oblíbenkyně, osudy, loajalita |
| **24-25** | Crafting, dobití energie |
| **26** | **Hlavní menu:** uložit / načíst / nastavení |
| **28** | Manželství a rodina |
| **A** | Automatický bezpečný tah |
| **0** | Konec (ulož hru) |

Zkratky: **S** / **L** / **M** -> menu 26, **Q** -> konec, **A** -> auto tah.

### Podmenu 26 - Hlavní menu

1. Uložit hru (JSON, sloty 1-5)  
2. Načíst hru  
3. Nastavení (barvy, obtížnost, **barevná témata**)  
4. Zpět do hry  
0. Ukončit s uložením  

---

## 💾 Ukládání (JSON)

- Soubor: `harem_dark_v18_save.json` (+ `_slot2` -> `_slot5`)
- Formát: Čitelný JSON (`indent=2`, české znaky)
- Atomický zápis + zálohy `.bak` / `.bak2` / `.bak3`
- **Autosave** při každém novém dni (`*_autosave.json`)
- Náhled slotu: den, zlato, velikost harému, ★ oblíbenkyně, čas uložení

---

## 🎨 Témata

**Nastavení -> 3) Barevné téma**

1. Temné dominium (výchozí)
2. Krvavý trůn  
3. Ledová panenka  
4. Zelený had  
5. Růžové hedvábí  
6. Monochrom (pro staré terminály)

---

## 📈 Loajalita (stupně)

| % | Titul | Poznámka |
|---|--------|----------|
| 0-14 | Vzbouřenkyně | vysoké riziko útěku |
| 15-29 | Nedůvěřivá | poslouchá ze strachu |
| 30-49 | Opatrná služka | neutrál |
| 50-69 | Oddaná | silnější odměny |
| 70-84 | Věrná otrokyně | útěk nepravděpodobný |
| 85-94 | Zasvěcená | hluboká oddanost |
| 95-100 | Absolutní majetek | útěk = 0 |

---

## 💡 Tipy pro nové hráče

1. Přidej nebo ulov první otrokyni (menu **11**).  
2. Buduj **loajalitu** a **důvěru** v sekci Péče (menu **23**).  
3. Sleduj **fázi zkaženosti** - otevírá nové možnosti a silnější odměny.  
4. Jmenuj **★ oblíbenkyni**, až budeš chtít privilegia i drama v harému.  
5. Každý den (**12**) se energie obnoví naplno a hra se autosave.  
6. Trénuj **výdrž** (4 -> 2), ať maximum energie roste.  
7. Cestuj po mapě (menu **8**) - v lokacích čekají speciální NPC a náhodné eventy.

---

## ⚠️ Upozornění

Hra obsahuje **explicitní erotický a temný obsah** (dominance, otroctví v herním světě, násilí v narativu). Je určena **výhradně pro dospělé (18+)**.

---

## Licence / Autor

Repozitář: [WarDroid23/harem_game](https://github.com/WarDroid23/harem_game)

*Dark Dominion – Dark Expansion*
