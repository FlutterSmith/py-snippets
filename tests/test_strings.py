import re

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pysnippets.strings import (
    byte_size,
    hamming_distance,
    hex_to_rgb,
    is_anagram,
    is_palindrome,
    rgb_to_hex,
    slugify,
    split_words,
    to_camel,
    to_kebab,
    to_pascal,
    to_snake,
    words,
)


@given(st.text())
def test_slugify_is_url_safe_and_idempotent(text: str) -> None:
    slug = slugify(text)
    assert re.fullmatch(r"([a-z0-9]+(-[a-z0-9]+)*)?", slug)
    assert slugify(slug) == slug


identifier_words = st.lists(st.from_regex(r"[a-z]{2,6}", fullmatch=True), min_size=1)


@given(identifier_words)
def test_naming_cases_round_trip(parts: list[str]) -> None:
    snake = "_".join(parts)
    assert to_snake(to_camel(snake)) == snake
    assert to_snake(to_pascal(snake)) == snake
    assert to_snake(to_kebab(snake)) == snake


def test_split_words_handles_acronyms_and_digits() -> None:
    assert split_words("XMLHttpRequest2") == ["XML", "Http", "Request", "2"]
    assert to_kebab("IOError") == "io-error"


@given(st.text(alphabet="abcAB ,!", max_size=12))
def test_is_anagram_of_its_reverse(text: str) -> None:
    assert is_anagram(text, text[::-1])


@given(st.text(alphabet="abcAB ,!", max_size=12))
def test_mirrored_text_is_a_palindrome(text: str) -> None:
    assert is_palindrome(text + text[::-1])


@given(st.text())
def test_byte_size_counts_utf8_bytes(text: str) -> None:
    surrogate_free = text.encode("utf-8", "surrogatepass")
    if surrogate_free.decode("utf-8", "ignore") == text:
        assert byte_size(text) == len(surrogate_free)


@given(st.text(max_size=10), st.text(max_size=10))
def test_hamming_distance(a: str, b: str) -> None:
    if len(a) != len(b):
        with pytest.raises(ValueError, match="equal length"):
            hamming_distance(a, b)
    else:
        assert hamming_distance(a, b) == hamming_distance(b, a)
        assert hamming_distance(a, a) == 0


@given(st.tuples(*[st.integers(0, 255)] * 3))
def test_hex_rgb_round_trip(rgb: tuple[int, int, int]) -> None:
    assert hex_to_rgb(rgb_to_hex(*rgb)) == rgb


@pytest.mark.parametrize("bad", ["", "#12", "1234567", "#abcd"])
def test_hex_to_rgb_rejects_bad_lengths(bad: str) -> None:
    with pytest.raises(ValueError, match="hex digits"):
        hex_to_rgb(bad)


def test_words_keeps_contractions() -> None:
    assert words("It's state-of-the-art.") == ["It's", "state-of-the-art"]


def test_single_letter_words_merge_once_joined() -> None:
    # Documented limitation: "AA" reads as one acronym.
    assert to_snake(to_pascal("a_a")) == "aa"
