from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def chunk_into_n(items: Sequence[T], n: int) -> list[list[T]]:
    """Split ``items`` into ``n`` lists whose sizes differ by at most one.

    >>> chunk_into_n([1, 2, 3, 4, 5, 6, 7], 4)
    [[1, 2], [3, 4], [5, 6], [7]]
    >>> chunk_into_n([1, 2, 3, 4, 5], 4)
    [[1, 2], [3], [4], [5]]
    >>> chunk_into_n([1, 2], 3)
    [[1], [2], []]
    """
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")
    # @note the first `extra` chunks get one more item
    size, extra = divmod(len(items), n)
    chunks = []
    start = 0
    for i in range(n):
        end = start + size + (i < extra)
        chunks.append(list(items[start:end]))
        start = end
    return chunks
