import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from textclean import (
    TextCleaningError,
    clean_text,
    collapse_whitespace,
    normalize_unicode,
    remove_puntuation,
    strip_html,
    tokenize,
    word_frequencies
)

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("  hello  world  ", "hello world"),
        ("a\n\tb", "a b"),
        ("", ""),
        ("  ", ""),
    ],
)
def test_collapse_whitespace(raw, expected):
    assert collapse_whitespace(raw) == expected


def test_remove_punctuation_keeps_words():
    assert remove_puntuation("Hi, there! (ok?)") == "Hi there ok"


def test_clean_text_default_pipeline():
    assert clean_text("  <b>Hello</b>,   WORLD!!  ") == "hello world"


def test_clean_text_custom_steps():
    assert clean_text("abc", steps=[str.upper, lambda s: s + "!"]) == "ABC!"


def test_tokenize_empty_returns_empty_list():
    assert tokenize("   !!!   ") == []


def test_word_frequencies_with_stopwords_and_top_n():
    text = "The cat and the hat. The CAT sat."
    result = word_frequencies(text, stopwords=["the", "and"], top_n=1)
    assert result == [("cat", 2)]


def test_word_frequencies_negative_top_n():
    with pytest.raises(ValueError):
        word_frequencies("a b",top_n=-1)


@pytest.mark.parametrize("bad", [None, 42, ["a"], b"bytes"])
def test_non_string_raises_custom_error(bad):
    with pytest.raises(TextCleaningError):
        clean_text(bad)


def test_custom_error_is_a_valueerror():
    assert issubclass(TextCleaningError, ValueError)