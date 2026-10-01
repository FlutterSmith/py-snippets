from collections import Counter


def is_anagram(a: str, b: str) -> bool:
    """Return ``True`` if ``a`` and ``b`` use the same letters and digits.

    Case, spaces and punctuation are ignored.

    >>> is_anagram("#anagram", "Nag a ram!")
    True
    >>> is_anagram("Listen", "Silent")
    True
    >>> is_anagram("abc", "abcc")
    False
    """

    def letters(s: str) -> Counter[str]:
        # @note casefold handles cases lower() misses, like "ß" -> "ss"
        return Counter(c for c in s.casefold() if c.isalnum())

    return letters(a) == letters(b)
