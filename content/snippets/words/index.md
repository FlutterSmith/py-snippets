---
slug: words
title: "Split a string into words"
summary: "Extract the words from text with a regex, keeping apostrophes and hyphens inside words."
category: strings
tags: [text]
module: strings/words.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [words]
  change: "Unicode-aware default pattern that keeps apostrophes; typed."
related: [naming-cases, slugify]
---

`text.split()` keeps punctuation attached: `'Python!!'`. A regex picks out the words alone.

<?snippet "strings/words.py"?>
```python
import re

# @note letters, optionally joined by ' or -, so "don't" stays one word
DEFAULT_WORD = r"[^\W\d_]+(?:['-][^\W\d_]+)*"


def words(text: str, pattern: str = DEFAULT_WORD) -> list[str]:
    """Return the words in ``text``, as matched by ``pattern``."""
    return re.findall(pattern, text)
```

<?snippet "strings/words.py" part="examples"?>
```pycon
>>> words("I love Python!!")
['I', 'love', 'Python']
>>> words("don't stop-motion, café & 42")
["don't", 'stop-motion', 'café']
>>> words("build -q --out one-item", r"\b[a-zA-Z-]+\b")
['build', 'q', 'out', 'one-item']
```

## How it works

- `[^\W\d_]` means a letter: not a non-word character, not a digit, not an underscore. It matches `é` and other non-ASCII letters too.
- `(?:['-]...)*` lets `don't` and `stop-motion` stay one word.
- Pass your own pattern to change what counts as a word.
