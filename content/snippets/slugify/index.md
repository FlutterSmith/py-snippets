---
slug: slugify
title: "Turn text into a URL slug"
summary: "Make a lowercase, ASCII, hyphen-separated slug from any text, including accented letters."
category: strings
tags: [text, conversion]
module: strings/slugify.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
fixes: "The original kept non-ASCII letters (`\\w` matches `é`), so its slugs weren't URL-safe ASCII."
origin:
  upstream: [slugify]
  change: "Rewritten: transliterates accents to ASCII, simpler regex; typed."
related: [naming-cases, words]
---

`Crème brûlée` should become `creme-brulee`, not `crme-brle` and not `crème-brûlée`.

<?snippet "strings/slugify.py"?>
```python
import re
import unicodedata


def slugify(text: str) -> str:
    """Turn ``text`` into a lowercase, URL-safe slug."""
    # @note splits "é" into "e" + accent, then drops anything non-ASCII
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", ascii_text.lower())
    return "-".join(words)
```

<?snippet "strings/slugify.py" part="examples"?>
```pycon
>>> slugify("Hello World!")
'hello-world'
>>> slugify("  Crème brûlée -- 2nd_edition ")
'creme-brulee-2nd-edition'
>>> slugify("!!!")
''
```

## How it works

- NFKD normalisation splits each accented letter into a base letter plus an accent mark.
- Encoding to ASCII with `ignore` drops the marks, and any other non-ASCII character.
- `re.findall` picks out runs of letters and digits; `'-'.join` glues them together. Leading and trailing separators can't happen.
