# Nové systémy (Dark Expansion)

## Po `git pull`

| Volba | Co dělá |
|-------|--------|
| **12 Odpočinek** | Plná energie + **noční eventy** (žárlivost ★/manželka, zrádkyně, razie) + denní režim + zápis do kroniky |
| **29 Kronika** | Posledních ~20 událostí dominia |
| **30 Denní rozkazy** | Tvrdý / Laskavý / Výstavní režim harému |
| **31 Veřejný výkon** | Otrokyně na očích města — reputace vs inkvizice |
| **Mafie → 5** | Válka o území |
| **Obchod → 9** | Černý trh (korupce/temná energie) |
| **Nastavení → 4** | Ironman (příznak v save) |

### Soubory
- `game/kronika.py`
- `game/denni_rozkazy.py`
- `game/nocni_eventy.py`
- `game/verejny_vykon.py`
- `game/menu_extra.py`

### Integrace main.py
Přidej import a v menu tisky 29–31 a volání:

```python
from game.menu_extra import obsluz_extra_volbu
# v tisku menu:
# 29) Kronika  30) Denní rozkazy  31) Veřejný výkon
# ve větvení:
if obsluz_extra_volbu(volba, hra):
    continue
```
