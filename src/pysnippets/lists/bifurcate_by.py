from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def bifurcate_by(
    items: Iterable[T], predicate: Callable[[T], object]
) -> tuple[list[T], list[T]]:
    """Split ``items`` into the ones that pass ``predicate`` and the ones that don't.

    >>> bifurcate_by(["beep", "boop", "foo", "bar"], lambda w: w.startswith("b"))
    (['beep', 'boop', 'bar'], ['foo'])
    >>> passed, failed = bifurcate_by(range(10), lambda n: n % 3 == 0)
    >>> passed, failed
    ([0, 3, 6, 9], [1, 2, 4, 5, 7, 8])
    >>> bifurcate_by([], bool)
    ([], [])
    """
    passed: list[T] = []
    failed: list[T] = []
    for item in items:
        # @note one pass, so `predicate` runs once per item
        (passed if predicate(item) else failed).append(item)
    return passed, failed
