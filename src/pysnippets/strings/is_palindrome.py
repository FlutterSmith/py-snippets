def is_palindrome(text: str) -> bool:
    """Return ``True`` if ``text`` is the same reversed, ignoring case and punctuation.

    >>> is_palindrome("taco cat")
    True
    >>> is_palindrome("A man, a plan, a canal: Panama!")
    True
    >>> is_palindrome("python")
    False
    """
    chars = [c for c in text.casefold() if c.isalnum()]
    # @note [::-1] is a reversed copy
    return chars == chars[::-1]
