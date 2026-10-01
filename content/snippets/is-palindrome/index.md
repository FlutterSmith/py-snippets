---
slug: is-palindrome
title: "Check if a string is a palindrome"
summary: "Check whether text reads the same reversed, ignoring case, spaces and punctuation."
category: strings
tags: [text, validation]
module: strings/is_palindrome.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [palindrome]
  change: "Renamed to is_palindrome; no regex; typed."
related: [is-anagram]
---

`A man, a plan, a canal: Panama!` is a palindrome once you ignore everything but the letters.

<?snippet "strings/is_palindrome.py"?>
```python
def is_palindrome(text: str) -> bool:
    """Return ``True`` if ``text`` is the same reversed, ignoring case and punctuation."""
    chars = [c for c in text.casefold() if c.isalnum()]
    # @note [::-1] is a reversed copy
    return chars == chars[::-1]
```

<?snippet "strings/is_palindrome.py" part="examples"?>
```pycon
>>> is_palindrome("taco cat")
True
>>> is_palindrome("A man, a plan, a canal: Panama!")
True
>>> is_palindrome("python")
False
```

## How it works

- Keep only letters and digits, casefolded.
- `[::-1]` makes a reversed copy, and `==` compares the two.
