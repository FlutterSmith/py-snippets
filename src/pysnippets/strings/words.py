import re

# @note letters, optionally joined by ' or -, so "don't" stays one word
DEFAULT_WORD = r"[^\W\d_]+(?:['-][^\W\d_]+)*"


def words(text: str, pattern: str = DEFAULT_WORD) -> list[str]:
    r"""Return the words in ``text``, as matched by ``pattern``.

    >>> words("I love Python!!")
    ['I', 'love', 'Python']
    >>> words("don't stop-motion, café & 42")
    ["don't", 'stop-motion', 'café']
    >>> words("build -q --out one-item", r"\b[a-zA-Z-]+\b")
    ['build', 'q', 'out', 'one-item']
    """
    return re.findall(pattern, text)
