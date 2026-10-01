---
slug: is-anagram
title: "Check if two strings are anagrams"
summary: "Compare letter counts, ignoring case, spaces and punctuation."
category: strings
tags: [text, validation]
module: strings/is_anagram.py
complexity: "O(n + m) time, O(k) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [is-anagram]
  change: "casefold instead of lower; typed."
related: [is-palindrome, have-same-contents]
---

`Listen` and `Silent` are anagrams. Sorting both strings works, but counting is linear.

<?snippet "strings/is_anagram.py"?>
```python
from collections import Counter


def is_anagram(a: str, b: str) -> bool:
    """Return ``True`` if ``a`` and ``b`` use the same letters and digits."""

    def letters(s: str) -> Counter[str]:
        # @note casefold handles cases lower() misses, like "ß" -> "ss"
        return Counter(c for c in s.casefold() if c.isalnum())

    return letters(a) == letters(b)
```

<?snippet "strings/is_anagram.py" part="examples"?>
```pycon
>>> is_anagram("#anagram", "Nag a ram!")
True
>>> is_anagram("Listen", "Silent")
True
>>> is_anagram("abc", "abcc")
False
```

## How it works

- `casefold()` is a stronger `lower()` meant for comparisons.
- `isalnum()` drops spaces and punctuation.
- Two `Counter`s are equal when every character occurs the same number of times.
