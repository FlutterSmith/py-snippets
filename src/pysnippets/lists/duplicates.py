from collections import Counter
from collections.abc import Hashable, Iterable
from typing import TypeVar

H = TypeVar("H", bound=Hashable)


def duplicates(items: Iterable[H]) -> list[H]:
    """Return the values that appear more than once, in first-seen order.

    >>> duplicates([1, 2, 2, 3, 4, 4, 4, 5])
    [2, 4]
    >>> duplicates([1, 2, 3])
    []
    """
    return [item for item, count in Counter(items).items() if count > 1]


def singles(items: Iterable[H]) -> list[H]:
    """Return the values that appear exactly once, in first-seen order.

    >>> singles([1, 2, 2, 3, 4, 4, 4, 5])
    [1, 3, 5]
    >>> singles("aabbc")
    ['c']
    """
    # @note Counter keeps first-seen order, so the result does too
    return [item for item, count in Counter(items).items() if count == 1]
