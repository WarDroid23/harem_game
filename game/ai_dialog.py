# game/ai_dialog.py — AI generované dialogy otrokyň (Ollama / API / fallback)
"""
Vyžaduje běžící Ollama (http://127.0.0.1:11434) nebo AI_API_KEY.
Vypínač: hra.nastaveni.ai_dialogy
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from config import MAGENTA, CYAN, NC

CACHE_SOUBOR = Path("saves/dialog_cache.json")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")
API_KEY = os.environ.get("AI_API_KEY", "")
API_BASE = os.environ.get("AI_API_BASE", "https://api.openai.com/v1")
API_MODEL = os.environ.get("AI_API_MODEL", "gpt-4o-mini")

# Ochrana před zamrznutím při offline backendu
_BACKEND_OFFLINE_UNTIL = 0.0
_CONNECT_TIMEOUT = 2.5


def _ai_zapnuto(hra_nebo_nastaveni) -> bool:
    n = getattr(hra_nebo_nastaveni, "nastaveni", hra_nebo_nastaveni)
    return bool(getattr(n, "ai_dialogy", False))


def _cache_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]


def _load_cache() -> dict:
    try:
        if CACHE_SOUBOR.exists():
            return json.loads(CACHE_SOUBOR.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def _save_cache(cache: dict) -> None:
    try:
        CACHE_SOUBOR.parent.mkdir(parents=True, exist_ok=True)
        if len(cache) > 300:
            keys = list(cache.keys())[-300:]
            cache = {k: cache[k] for k in keys}
        CACHE_SOUBOR.write_text(
            json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError:
        pass


def sestav_prompt(otrok, hrac, typ: str = "šeptání") -> str:
    faze = getattr(otrok, "faze_zkazenosti", 0)
    loaj = getattr(otrok, "loajalita", 50)
    hvezda = "ano ★" if getattr(otrok, "oblibena", False) else "ne"
    manz = "ano" if getattr(otrok, "je_manzelkou", False) or getattr(otrok, "partnerka", False) else "ne"
    char = getattr(otrok, "charakter", "subka")

    if faze <= 2:
        psychika = "Stále v ní hoří zbytky hrdosti a vzdoru, cítí ponížení, strach a zatíná zuby."
    elif faze <= 6:
        psychika = "Postupně se láme, začíná přijímat svou roli otrokyně, je pokorná a snaží se vyhnout trestu."
    elif faze <= 11:
        psychika = "Propadla temnotě a smyslnosti, aktivně touží po pánově doteku, chvále a tělesné dominanci."
    else:
        psychika = "Absolutní temná zkáza mysli – zvrácená, hluboce závislá na bolesti a ponižování, zcela odevzdaná prázdnota a rozkoš."

    return (
        "Jsi otrokyně v temném erotickém fantasy harému. Piš výhradně česky, 2 až 4 věty, "
        "bez markdownu, bez uvozovek kolem celku, bez vysvětlování.\n"
        f"Jméno: {getattr(otrok, 'jmeno', 'Otrokyně')}\n"
        f"Charakter: {char}\n"
        f"Fáze zkázanosti: {faze}/16 ({psychika})\n"
        f"Loajalita: {loaj}%\n"
        f"Oblíbenkyně: {hvezda}\n"
        f"Manželka/partnerka: {manz}\n"
        f"Typ scény: {typ}\n"
        f"Pán — den {getattr(hrac, 'den', 1)}, reputace {getattr(hrac, 'reputace_mesta', 0)}.\n"
        "Napiš jen její autentickou promluvu nebo tělesnou reakci v této chvíli."
    )


def _fallback(otrok, typ: str) -> str:
    j = getattr(otrok, "jmeno", "Otrokyně")
    loaj = getattr(otrok, "loajalita", 50)
    faze = getattr(otrok, "faze_zkazenosti", 0)
    is_star = bool(getattr(otrok, "oblibena", False))
    is_wife = bool(getattr(otrok, "je_manzelkou", False) or getattr(otrok, "partnerka", False))

    if "trest" in typ or "vzdor" in typ:
        if faze >= 10:
            volby = [
                f"{j} se s trhnutím prohne a na rtech jí vykvete zvrácený úsměv. „Víc, můj pane… temnota ve mně po tom prahne.“",
                f"{j} lapá po dechu a s lesknoucíma se očima šeptá: „Tvoje bolest je moje potěšení… netrestej mě málo.“",
                f"{j} se tiskne k tvým nohám i po ráně. „Děkuji… očisti mě od všeho, co ti nepatří.“",
            ]
        elif loaj < 40 or faze <= 3:
            volby = [
                f"{j} se štítí pohledu, ale neuhýbá. „Jak milostivě…“ šeptá s hořkým odporem.",
                f"{j} zatíná pěsti a sykne bolestí. „Myslíš, že mě tímhle zlomíš, pane?“",
                f"{j} sklopí zrak a po tváři jí steče slza hněvu. „Splním rozkaz, ale nic víc ode mě nečekej.“",
            ]
        else:
            volby = [
                f"{j} se chvěje pod tvou rukou. „Ano, pane… zasloužím si to. Budu poslušnější.“",
                f"{j} ztiší dech a skloní šíji. „Už se to nestane… odpust mi, pane.“",
                f"{j} padne na kolena. „Tvůj trest je spravedlivý. Jsem tvůj majetek.“",
            ]
        return random.choice(volby)

    if "odměn" in typ or "oddan" in typ:
        if is_wife:
            volby = [
                f"{j} tě jemně pohladí po tváři. „Všechno, co dělám, dělám pro naši říši… a pro tebe, můj muži.“",
                f"{j} se ti opře o hruď a vydechne: „Tvá přízeň je pro mě cennější než všechno zlato světa.“",
            ]
        elif is_star:
            volby = [
                f"{j} se pyšně a svůdně usměje na ostatní otrokyně v síni. „Věděla jsem, že jsem tvé číslo jedna, pane.“",
                f"{j} položí ruku na tvé stehno. „Nikdo ti nebude sloužit tak oddaně jako tvá oblíbenkyně.“",
            ]
        elif faze >= 10:
            volby = [
                f"{j} se v extázi přitiskne. „Děkuji, pane… tvá temná krev a vůle mě pohlcují.“",
                f"{j} políbí lem tvého pláště. „Jsem jen tvá hračka… tvoje zkažená loutka.“",
            ]
        else:
            volby = [
                f"{j} se nesměle pousměje a tváře jí zrudnou. „Děkuji, pane… jsi ke mně nečekaně laskavý.“",
                f"{j} se přitulí blíž. „Děkuji, pane… snažím se dělat vše správně.“",
                f"{j} sklopí oči s vděkem. „Každé tvé vlídné slovo mi dává sílu sloužit dál.“",
            ]
        return random.choice(volby)

    if "noč" in typ:
        if is_wife or is_star:
            volby = [
                f"Ve tmě komnaty slyšíš tichý dech. {j} ti vklouzne pod kožešiny: „Nemohla jsem bez tebe usnout, pane.“",
                f"{j} tě zezadu obejme v posteli a zašeptá: „Noc patří jen nám dvěma… drž mě pevně.“",
            ]
        elif faze >= 8:
            volby = [
                f"{j} se tiše plíží po chladné podlaze k tvému lůžku. „Povol mi ležet u tvých nohou, pane… třesu se touhou.“",
                f"Ve tmě se zalesknou její rozšířené zornice. {j} šeptá: „Tvá temná aura mě hřeje víc než oheň v krbu.“",
            ]
        else:
            volby = [
                f"Ve tmě slyšíš tichý dech. {j} šeptá ze svého kouta: „Smím zůstat… nablízku?“",
                f"{j} se neklidně převaluje na loži a sleduje tvůj stín. „Hlídám tvůj spánek, pane.“",
            ]
        return random.choice(volby)

    if "veřej" in typ:
        if faze >= 10:
            volby = [
                f"{j} s hrdostí vystaví své křivky zvědavým pohledům davu. „Ať všichni vidí, komu patřím tělem i duší.“",
                f"{j} se před zraky měšťanů svůdně prohne a vychutnává si jejich chtivý šepot i tvou pevnou ruku.",
            ]
        elif loaj < 40:
            volby = [
                f"{j} se třese hanbou a zarývá nehty do dlaní. „Tohle ti nikdy neodpustím… vystavovat mě jako zvěř.“",
                f"{j} sklopí hlavu a tváře jí hoří rudým studem před zraky celého náměstí.",
            ]
        else:
            volby = [
                f"{j} poslušně snáší pohledy davu, oči upřené jen na tebe. „Pro tebe to vydržím, pane…“",
                f"{j} tiše polkne a narovná se v řetězech. „Jsem tvá otrokyně… ať to město ví.“",
            ]
        return random.choice(volby)

    if "žárl" in typ:
        volby = [
            f"{j} vrhne jedovatý pohled na svou sokyni. „Ona ti nikdy nedá to, co já. Já vím, jaké choutky skrýváš.“",
            f"{j} ti položí ruku na hruď a zatlačí: „Nedívej se na ni takhle, pane… dívej se jen na mě.“",
            f"{j} tiše sykne s potemnělýma očima: „Její kůže brzy pozná, co znamená plést se mezi nás.“",
        ]
        return random.choice(volby)

    # Univerzální šeptání a běžné reakce
    if faze >= 12:
        volby = [
            f"{j} se ti něžně otře o ruku s prázdným, zamilovaným pohledem. „Udělej se mnou cokoliv, pane… jsem celá tvoje.“",
            f"{j} tiše zaúpí rozkoší při pouhém tvém doteku. „Má mysl už nezná jiného boha než tebe.“",
        ]
    elif faze >= 6:
        volby = [
            f"{j} tiše vydechne a skloní hlavu. „Tvůj dotek je návykový, pane… čekám na tvůj další rozkaz.“",
            f"{j} poslušně poklekne. „Jsem připravena ti posloužit v čemkoliv.“",
        ]
    else:
        volby = [
            f"{j} sklopí oči a čeká na další rozkaz s tichým tepem srdce.",
            f"{j} se mírně zachvěje při tvém hlase: „Ano, pane?“",
            f"{j} udržuje odstup, ale její pohled tě nepřestává sledovat.",
        ]
    return random.choice(volby)


def generuj_ollama(prompt: str, model: Optional[str] = None) -> str:
    global _BACKEND_OFFLINE_UNTIL
    body = json.dumps(
        {
            "model": model or OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.88, "num_predict": 140},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=_CONNECT_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return (data.get("response") or "").strip()
    except Exception as e:
        _BACKEND_OFFLINE_UNTIL = time.time() + 45.0
        raise e


def generuj_api(prompt: str) -> str:
    global _BACKEND_OFFLINE_UNTIL
    if not API_KEY:
        raise RuntimeError("Chybí AI_API_KEY")
    body = json.dumps(
        {
            "model": API_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Piš krátké erotické dialogy otrokyně česky, 2–4 věty.",
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 160,
            "temperature": 0.9,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE.rstrip('/')}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=_CONNECT_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        _BACKEND_OFFLINE_UNTIL = time.time() + 45.0
        raise e


def generuj_dialog(
    otrok,
    hrac,
    typ: str = "šeptání",
    *,
    nastaveni=None,
    pouzit_cache: bool = True,
    ticho: bool = False,
) -> str:
    global _BACKEND_OFFLINE_UNTIL
    zap = True
    if nastaveni is not None:
        zap = _ai_zapnuto(nastaveni)
    elif hasattr(hrac, "nastaveni"):
        zap = _ai_zapnuto(hrac)
    else:
        zap = os.environ.get("HAREM_AI", "").lower() in ("1", "true", "ano")

    if not zap:
        return _fallback(otrok, typ)

    # Pokud byl server nedávno offline, nevytváříme lag a použijeme fallback
    if time.time() < _BACKEND_OFFLINE_UNTIL:
        return _fallback(otrok, typ)

    prompt = sestav_prompt(otrok, hrac, typ)
    key = _cache_key(prompt + "|" + typ)
    cache = _load_cache()
    if pouzit_cache and key in cache:
        return cache[key]

    if not ticho:
        print(f"{CYAN}… šeptá ti něco do ucha …{NC}")

    text = ""
    try:
        if API_KEY:
            text = generuj_api(prompt)
        else:
            text = generuj_ollama(prompt)
    except Exception:
        text = ""

    if not text or len(text) < 8:
        text = _fallback(otrok, typ)
    else:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        text = " ".join(lines)
        if len(text) > 600:
            text = text[:597] + "…"

    cache[key] = text
    _save_cache(cache)
    return text


def vypis_dialog(otrok, hrac, typ: str = "šeptání", nastaveni=None) -> None:
    text = generuj_dialog(otrok, hrac, typ, nastaveni=nastaveni)
    print(f"{MAGENTA}{text}{NC}")


def typ_z_akce(akce: dict) -> str:
    if not akce:
        return "šeptání"
    t = (akce.get("typ") or "").lower()
    nazev = (akce.get("nazev") or akce.get("id") or "").lower()
    if t == "trest" or "trest" in nazev:
        return "po_trestu"
    if t == "odmena" or "odměn" in nazev or "odmen" in nazev:
        return "po_odměně"
    if "veřej" in nazev or "verej" in nazev:
        return "veřejný_výkon"
    return f"interakce:{akce.get('nazev', nazev)}"

