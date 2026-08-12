"""Offline deterministic smart filter engine.

Uses normalization + token matching + SequenceMatcher. No AI, no external API,
and no internet connection are required.
"""
from difflib import SequenceMatcher
from typing import Iterable

from .arabic import normalize_arabic
from .english import normalize_english
from .suggestions import build_suggestion


def normalize(text: str) -> str:
    """Normalize Arabic/English text while preserving mixed-language searches."""
    text = (text or "").strip().lower()
    ar = normalize_arabic(text)
    en = normalize_english(text)
    parts = [p for p in (ar, en) if p]
    # Keep only unique normalized representations.
    return " ".join(dict.fromkeys(parts))


def _score(query: str, candidate: str) -> float:
    q = normalize(query)
    c = normalize(candidate)
    if not q or not c:
        return 0.0
    if q == c:
        return 1.0
    if q in c:
        return 0.96

    q_tokens = set(q.split())
    c_tokens = set(c.split())
    overlap = len(q_tokens & c_tokens) / max(1, len(q_tokens))
    ratio = SequenceMatcher(None, q, c).ratio()
    # Character similarity is useful for typos; token overlap helps full bike names.
    return (ratio * 0.7) + (overlap * 0.3)


def suggest_motorcycles(motorcycles: Iterable, query: str, limit: int = 6) -> list[dict]:
    query = (query or "").strip()
    if len(query) < 2:
        return []

    ranked = []
    seen = set()
    for bike in motorcycles:
        brand_ar = bike.get_brand_display()
        brand_en = bike.brand
        candidates = [
            bike.name,
            f"{brand_ar} {bike.name}",
            f"{brand_en} {bike.name}",
            brand_ar,
            brand_en,
        ]
        score = max(_score(query, value) for value in candidates)
        if bike.id in seen or score < 0.33:
            continue
        seen.add(bike.id)
        ranked.append((score, bike))

    ranked.sort(key=lambda pair: (-pair[0], pair[1].name.lower()))
    return [build_suggestion(bike, score, query) for score, bike in ranked[:limit]]
