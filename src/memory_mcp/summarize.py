"""Résumé extractif intelligent — format structuré stable, faits préservés."""

from __future__ import annotations

import re

from memory_mcp.storage import MemoryEntry

_ROLE_PREFIX = re.compile(r"^(user|assistant|system)\s*:\s*", re.IGNORECASE)
_EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.\w+", re.IGNORECASE)
_CONTRACT = re.compile(r"CTR-\d{4}-\d+", re.IGNORECASE)
_AMOUNT = re.compile(r"\d+[,.]\d+\s*€?")
_DATE = re.compile(
    r"\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)"
    r"|\d{1,2}/\d{1,2}(?:/\d{2,4})?",
    re.IGNORECASE,
)
_NAME = re.compile(r"\b[A-ZÀ-Ÿ][a-zà-ÿ]+(?:\s+[A-ZÀ-Ÿ][a-zà-ÿ]+)+\b")
_EMPTY = "—"


def strip_role(content: str) -> str:
    return _ROLE_PREFIX.sub("", content).strip()


def compress_line(content: str, max_len: int = 88) -> str:
    text = strip_role(content)
    text = re.sub(r"\s+", " ", text)
    return text[:max_len].strip()


def extract_signals(content: str) -> dict[str, str]:
    text = strip_role(content)
    signals: dict[str, str] = {}
    if m := _EMAIL.search(text):
        signals["email"] = m.group(0)
    if m := _CONTRACT.search(text):
        signals["contract"] = m.group(0)
    if m := _AMOUNT.search(text):
        signals["amount"] = m.group(0)
    if m := _DATE.search(text):
        signals["date"] = m.group(0)
    if m := _NAME.search(text):
        signals["name"] = m.group(0)
    return signals


def _merge_slots(slots: dict[str, str], content: str) -> None:
    for key, value in extract_signals(content).items():
        if value and slots.get(key, _EMPTY) == _EMPTY:
            slots[key] = value


def structured_summary(entries: list[MemoryEntry], max_chars: int = 500) -> str:
    """Résumé à slots fixes — taille stable tour après tour."""
    slots: dict[str, str] = {
        "name": _EMPTY,
        "contract": _EMPTY,
        "email": _EMPTY,
        "amount": _EMPTY,
        "date": _EMPTY,
    }

    for entry in entries:
        if "noise" in entry.tags:
            continue
        _merge_slots(slots, entry.content)
        if "fact" in entry.tags or "client" in entry.tags:
            line = compress_line(entry.content, 60)
            if slots["name"] == _EMPTY and _NAME.search(line):
                slots["name"] = _NAME.search(line).group(0)  # type: ignore[union-attr]

    # Slots à largeur fixe → coût tokens stable dès le tour 1
    summary = (
        f"CLIENT:{slots['name'][:22]:<22}|"
        f"CTR:{slots['contract'][:16]:<16}|"
        f"MAIL:{slots['email'][:24]:<24}|"
        f"EUR:{slots['amount'][:10]:<10}|"
        f"DATE:{slots['date'][:14]:<14}"
    )
    if len(summary) > max_chars:
        summary = summary[: max_chars - 3] + "..."
    return summary


def update_digest(digest: str, content: str, tags: list[str], max_chars: int = 500) -> str:
    """Compatibilité — délègue au format structuré via pseudo-entrée."""
    entry = MemoryEntry(id=0, content=content, tags=tags, session="", turn=0)
    existing = MemoryEntry(id=0, content=digest, tags=[], session="", turn=0) if digest else None
    entries = [e for e in (existing, entry) if e]
    return structured_summary(entries, max_chars=max_chars)


def build_summary(entries: list[MemoryEntry], max_chars: int = 500) -> str:
    if not entries:
        return ""
    clean = [e for e in entries if "noise" not in e.tags]
    if not clean:
        return f"SESSION:{len(entries)}tours|BRUIT:{len(entries)}"
    return structured_summary(clean, max_chars=max_chars)
