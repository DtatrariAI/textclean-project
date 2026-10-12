"""A small text-cleaning module (Day 1 assignment)."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Callable, Iterable, Optional

_WHITESPACE_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]")
_HTML_TAG_RE = re.compile(r"<[^>]+>")

# A "step" is any function that takes a string and returns a string
Step = Callable[[str], str]


class TextCleaningError(ValueError):
    """Raised when the input cannot be cleaned (e.g. it is not a string.)"""


def _require_str(text: object) -> str:
    if not isinstance(text, str):
        raise TextCleaningError(f"expected str, got {type(text).__name__}")
    return text


def normalize_unicode(text: str, form: str = "NFKC") -> str:
    """Normalize unicode so visually-identical character compare equal."""
    return unicodedata.normalize(form, _require_str(text))


def strip_html(text: str) -> str:
    """Remove simple HTML tags (not a full parser)."""
    return _HTML_TAG_RE.sub("", _require_str(text))


def remove_puntuation(text: str) -> str:
    """Delete punctuation, keeping letters, digits, underscores and spaces."""
    return _PUNCT_RE.sub("", _require_str(text))


def collapse_whitespace(text: str) -> str:
    """Replace any run of whitespace with a single space and trim the ends."""
    return _WHITESPACE_RE.sub(" ", _require_str(text)).strip()


def lowercase(text: str) -> str:
    return _require_str(text).casefold()


DEFAULT_STEPS: tuple[Step, ...] = (
    normalize_unicode,
    strip_html,
    lowercase,
    remove_puntuation,
    collapse_whitespace
)


def clean_text(text: str, steps: Optional[Iterable[Step]] = None) -> str:
    """Run text through a pipeline of cleaning steps, in order."""
    result = _require_str(text)
    for step in steps if steps is not None else DEFAULT_STEPS:
        result = step(result)
    return result


def tokenize(text: str) -> list[str]:
    """Clean text and split it into words"""
    cleaned = clean_text(text)
    return cleaned.split() if cleaned else []


def word_frequencies(text: str, stopwords: Iterable[str] = (), top_n: Optional[int] = None) -> list[tuple[str, int]]:
    """Return (word, count) pairs, most common first, skipping stopwords."""
    if top_n is not None and top_n < 0:
        raise ValueError("top_n must be non-negative")
    ignore = {w.casefold() for w in stopwords}
    counts = Counter(w for w in tokenize(text) if w not in ignore)
    return counts.most_common(top_n)

