---
slug: byte-size
title: "Size of a string in bytes"
summary: "Count the bytes a string takes up once encoded, which len() doesn't tell you."
category: strings
tags: [text]
module: strings/byte_size.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [byte-size]
  change: "Added the encoding parameter; typed."
related: [hamming-distance]
---

A database column holds 255 *bytes*, an emoji is 4 of them, and `len('😀')` is 1.

<?snippet "strings/byte_size.py"?>
```python
def byte_size(text: str, encoding: str = "utf-8") -> int:
    """Return the number of bytes ``text`` takes up in ``encoding``."""
    # @note len(text) counts code points; this counts bytes
    return len(text.encode(encoding))
```

<?snippet "strings/byte_size.py" part="examples"?>
```pycon
>>> byte_size("Hello World")
11
>>> byte_size("😀")
4
>>> byte_size("😀", "utf-16")
6
```

## How it works

- `len(text)` counts code points.
- `.encode()` produces the bytes that are actually stored or sent; their `len` is the size.
- The encoding matters: the same emoji is 4 bytes in UTF-8 and 6 in UTF-16, including the 2-byte BOM.
