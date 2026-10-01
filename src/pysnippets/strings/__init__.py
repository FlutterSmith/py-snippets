"""Strings: slugs, cases, words and checks."""

from pysnippets.strings.byte_size import byte_size
from pysnippets.strings.hamming_distance import hamming_distance
from pysnippets.strings.hex_rgb import hex_to_rgb, rgb_to_hex
from pysnippets.strings.is_anagram import is_anagram
from pysnippets.strings.is_palindrome import is_palindrome
from pysnippets.strings.naming_cases import (
    split_words,
    to_camel,
    to_kebab,
    to_pascal,
    to_snake,
)
from pysnippets.strings.slugify import slugify
from pysnippets.strings.words import words

__all__ = [
    "byte_size",
    "hamming_distance",
    "hex_to_rgb",
    "is_anagram",
    "is_palindrome",
    "rgb_to_hex",
    "slugify",
    "split_words",
    "to_camel",
    "to_kebab",
    "to_pascal",
    "to_snake",
    "words",
]
