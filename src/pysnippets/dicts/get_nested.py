from collections.abc import Hashable, Iterable
from typing import Any


def get_nested(data: Any, path: Iterable[Hashable], default: Any = None) -> Any:
    """Follow ``path`` through nested dicts and lists, or return ``default``.

    >>> users = {"fred": {"name": {"last": "Smith"}, "posts": [1, 2, 3]}}
    >>> get_nested(users, ["fred", "name", "last"])
    'Smith'
    >>> get_nested(users, ["fred", "posts", 1])
    2
    >>> get_nested(users, ["fred", "posts", 9], default=0)
    0
    """
    for step in path:
        try:
            data = data[step]
        # @note missing key, index out of range, or a step into a non-container
        except (KeyError, IndexError, TypeError):
            return default
    return data
