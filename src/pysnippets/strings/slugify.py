import re
import unicodedata


def slugify(text: str) -> str:
    """Turn ``text`` into a lowercase, URL-safe slug.

    >>> slugify("Hello World!")
    'hello-world'
    >>> slugify("  Crème brûlée -- 2nd_edition ")
    'creme-brulee-2nd-edition'
    >>> slugify("!!!")
    ''
    """
    # @note splits "é" into "e" + accent, then drops anything non-ASCII
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", ascii_text.lower())
    return "-".join(words)
