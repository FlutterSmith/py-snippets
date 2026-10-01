---
slug: naming-cases
title: "Convert between naming cases"
summary: "Convert text between snake_case, kebab-case, camelCase and PascalCase, acronyms included."
category: strings
tags: [text, conversion]
module: strings/naming_cases.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
fixes: "The original `camel` lowercased the inside of every word, so `someDatabaseField` became `somedatabasefield`, and an empty string raised `IndexError`."
origin:
  upstream: [camel, kebab, snake]
  change: "Merged three snippets around one shared word splitter; added PascalCase; typed."
related: [slugify, words]
---

One word splitter, four joins. The hard part is splitting `parseHTTPResponse` into `parse`, `HTTP`, `Response`.

<?snippet "strings/naming_cases.py"?>
```python
import re

# @note an acronym, a capitalised word, a lowercase run, or digits
_WORD = re.compile(r"[A-Z]+(?=[A-Z][a-z]|\b|_|\d)|[A-Z]?[a-z]+|[A-Z]+|\d+")


def split_words(text: str) -> list[str]:
    """Split ``text`` into words at spaces, ``-``, ``_`` and case changes."""
    return _WORD.findall(text)


def to_snake(text: str) -> str:
    """Convert ``text`` to snake_case."""
    return "_".join(word.lower() for word in split_words(text))


def to_kebab(text: str) -> str:
    """Convert ``text`` to kebab-case."""
    return "-".join(word.lower() for word in split_words(text))


def to_camel(text: str) -> str:
    """Convert ``text`` to camelCase."""
    pascal = to_pascal(text)
    return pascal[:1].lower() + pascal[1:]


def to_pascal(text: str) -> str:
    """Convert ``text`` to PascalCase."""
    return "".join(word.capitalize() for word in split_words(text))
```

<?snippet "strings/naming_cases.py" part="examples"?>
```pycon
>>> split_words("parseHTTPResponse_v2 and-more")
['parse', 'HTTP', 'Response', 'v', '2', 'and', 'more']
>>> to_snake("AllThe-small Things")
'all_the_small_things'
>>> to_snake("parseHTTPResponse")
'parse_http_response'
>>> to_kebab("some-mixed_string With spaces")
'some-mixed-string-with-spaces'
>>> to_camel("some_database_field_name")
'someDatabaseFieldName'
>>> to_camel("")
''
>>> to_pascal("some label that needs pascal")
'SomeLabelThatNeedsPascal'
```

## How it works

- The regex matches, in order: an acronym followed by a capitalised word, a capitalised or lowercase word, a run of capitals, or digits.
- Spaces, hyphens and underscores are never part of a match, so they act as separators.
- Each case function only lowercases or capitalises the words and joins them.
- Single-letter words don't survive a round trip: `to_pascal('a_b')` is `AB`, which then reads as one acronym.
