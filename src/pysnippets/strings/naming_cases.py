import re

# @note an acronym, a capitalised word, a lowercase run, or digits
_WORD = re.compile(r"[A-Z]+(?=[A-Z][a-z]|\b|_|\d)|[A-Z]?[a-z]+|[A-Z]+|\d+")


def split_words(text: str) -> list[str]:
    """Split ``text`` into words at spaces, ``-``, ``_`` and case changes.

    >>> split_words("parseHTTPResponse_v2 and-more")
    ['parse', 'HTTP', 'Response', 'v', '2', 'and', 'more']
    """
    return _WORD.findall(text)


def to_snake(text: str) -> str:
    """Convert ``text`` to snake_case.

    >>> to_snake("AllThe-small Things")
    'all_the_small_things'
    >>> to_snake("parseHTTPResponse")
    'parse_http_response'
    """
    return "_".join(word.lower() for word in split_words(text))


def to_kebab(text: str) -> str:
    """Convert ``text`` to kebab-case.

    >>> to_kebab("some-mixed_string With spaces")
    'some-mixed-string-with-spaces'
    """
    return "-".join(word.lower() for word in split_words(text))


def to_camel(text: str) -> str:
    """Convert ``text`` to camelCase.

    >>> to_camel("some_database_field_name")
    'someDatabaseFieldName'
    >>> to_camel("")
    ''
    """
    pascal = to_pascal(text)
    return pascal[:1].lower() + pascal[1:]


def to_pascal(text: str) -> str:
    """Convert ``text`` to PascalCase.

    >>> to_pascal("some label that needs pascal")
    'SomeLabelThatNeedsPascal'
    """
    return "".join(word.capitalize() for word in split_words(text))
