# utils/term_render.py
"""Optimalizované vykreslování terminálu – buffer, kurzor, animace."""

from __future__ import annotations

import sys
import time
from typing import Callable, List, Optional, Sequence, Union

_HIDE_CURSOR = "\033[?25l"
_SHOW_CURSOR = "\033[?25h"
_HOME = "\033[H"
_CLEAR = "\033[2J"


def _stdout_write(data: str) -> None:
    sys.stdout.write(data)


def _flush() -> None:
    try:
        sys.stdout.flush()
    except Exception:
        pass


def hide_cursor() -> None:
    _stdout_write(_HIDE_CURSOR)
    _flush()


def show_cursor() -> None:
    _stdout_write(_SHOW_CURSOR)
    _flush()


def clear_fast() -> None:
    """Rychlé smazání obrazovky bez volání shellu."""
    _stdout_write(_CLEAR + _HOME)
    _flush()


def home() -> None:
    _stdout_write(_HOME)
    _flush()


def render_frame(lines: Union[str, Sequence[str]], *, use_home: bool = True, pad_lines: int = 0) -> None:
    """Jeden snímek – sestavený do stringu, jeden zápis (méně blikání)."""
    if isinstance(lines, str):
        text = lines if lines.endswith("\n") else lines + "\n"
    else:
        text = "\n".join(lines) + "\n"
    if pad_lines > 0:
        text += "\n" * pad_lines
    if use_home:
        _stdout_write(_HOME + text)
    else:
        _stdout_write(text)
    _flush()


def render_block(text: str, *, clear: bool = False) -> None:
    if clear:
        clear_fast()
    _stdout_write(text if text.endswith("\n") else text + "\n")
    _flush()


def animuj(
    framy: Sequence[Union[str, Sequence[str]]],
    *,
    fps: float = 8.0,
    cyklu: int = 1,
    clear_first: bool = True,
    skryt_kurzor: bool = True,
    on_frame: Optional[Callable[[int], None]] = None,
) -> None:
    """Přehráje seznam framů (fps, počet cyklů)."""
    if not framy:
        return
    delay = 1.0 / max(0.5, fps)
    if skryt_kurzor:
        hide_cursor()
    try:
        if clear_first:
            clear_fast()
        for _ in range(max(1, cyklu)):
            for i, frame in enumerate(framy):
                render_frame(frame, use_home=True, pad_lines=2)
                if on_frame:
                    on_frame(i)
                time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        if skryt_kurzor:
            show_cursor()


# ── Ukázka kódu pro animaci ──────────────────────────────────
PRIKLAD_ANIMACE = '''
# ── Ukázka: animace v Harem Dark ─────────────────────────────
from utils.term_render import animuj, clear_fast, render_frame
from utils.ascii_gen import (
    framy_hvezd_pulz,
    framy_napln_energie,
    framy_harem_dych,
    framy_noc,
)
import time

# 1) Pulzující hvězda (oblíbenkyně)
animuj(framy_hvezd_pulz(cyklu_framu=6, jmeno="Selene"), fps=6, cyklu=2)

# 2) Plnění energie (progress bary)
animuj(framy_napln_energie(sex_cil=100, temno_cil=80, kroku=14), fps=12, cyklu=1)

# 3) Harém „dýchá“
animuj(framy_harem_dych(pocet=5, oblibena=True, framy=8), fps=5, cyklu=3)

# 4) Noční obloha
animuj(framy_noc(10), fps=6, cyklu=2)

# Vlastní frame ručně:
clear_fast()
for i in range(5):
    render_frame([f"  Den {i}", "  ★  " + "·" * i], use_home=True)
    time.sleep(0.15)
'''
