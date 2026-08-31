# game/ai_dialog.py — AI generované dialogy otrokyň (Ollama / API / fallback)
"""
Vyžaduje běžící Ollama (http://127.0.0.1:11434) nebo AI_API_KEY.
Vypínač: hra.nastaveni.ai_dialogy
"""
from __future__ import annotations

import hashlib
import json
import os
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
        if len(cache) > 200:
            keys = list(cache.keys())[-200:]
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
    return (
        "Jsi otrokyně v temném erotickém harému. Piš výhradně česky, 2 až 4 věty, "
        "bez markdownu, bez uvozovek kolem celku, bez vysvětlování.\n"
        f"Jméno: {getattr(otrok, 'jmeno', 'Otrokyně')}\n"
        f"Charakter: {char}\n"
        f"Fáze zkázanosti: {faze}/16\n"
        f"Loajalita: {loaj}%\n"
        f"Oblíbenkyně: {hvezda}\n"
        f"Manželka/partnerka: {manz}\n"
        f"Typ scény: {typ}\n"
        f"Pán — den {getattr(hrac, 'den', 1)}, reputace {getattr(hrac, 'reputace_mesta', 0)}.\n"
        "Napiš jen její promluvu nebo tělesnou reakci v této chvíli."
    )


def _fallback(otrok, typ: str) -> str:
    j = getattr(otrok, "jmeno", "Otrokyně")
    loaj = getattr(otrok, "loajalita", 50)
    if "trest" in typ or "vzdor" in typ:
        if loaj < 40:
            return f"{j} se štítí pohledu, ale neuhýbá. „Jak milostivě…“ šeptá s odporem."
        return f"{j} se chvěje. „Ano, pane… zasloužím si to.“"
    if "odměn" in typ or "oddan" in typ:
        return f"{j} se přitulí blíž. „Děkuji, pane… jsem jen tvoje.“"
    if "noč" in typ:
        return f"Ve tmě slyšíš dech. {j} šeptá: „Smím zůstat… u tebe?“"
    if "veřej" in typ:
        return f"{j} sklopí oči před davem, tváře hoří. „Pro tebe, pane…“"
    if "žárl" in typ:
        return f"{j} tiše sykne: „Ona není jako já. Já vím, co chceš.“"
    return f"{j} sklopí oči a čeká na další rozkaz."


def generuj_ollama(prompt: str, model: Optional[str] = None) -> str:
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
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data.get("response") or "").strip()


def generuj_api(prompt: str) -> str:
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
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def generuj_dialog(
    otrok,
    hrac,
    typ: str = "šeptání",
    *,
    nastaveni=None,
    pouzit_cache: bool = True,
    ticho: bool = False,
) -> str:
    zap = True
    if nastaveni is not None:
        zap = _ai_zapnuto(nastaveni)
    elif hasattr(hrac, "nastaveni"):
        zap = _ai_zapnuto(hrac)
    else:
        zap = os.environ.get("HAREM_AI", "").lower() in ("1", "true", "ano")

    if not zap:
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
