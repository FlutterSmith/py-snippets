from collections.abc import Iterable, Iterator


def deep_flatten(items: Iterable[object]) -> Iterator[object]:
    """Yield every non-iterable value from arbitrarily nested iterables.

    Strings and bytes count as single values, not as iterables of characters.

    >>> list(deep_flatten([1, [2], [[3], 4], 5]))
    [1, 2, 3, 4, 5]
    >>> list(deep_flatten(["ab", ("cd", ["ef"])]))
    ['ab', 'cd', 'ef']
    >>> list(deep_flatten([[], [[]]]))
    []
    """
    for item in items:
        # @note without this check "ab" recurses forever: "a" is iterable too
        if isinstance(item, Iterable) and not isinstance(item, str | bytes):
            yield from deep_flatten(item)
        else:
            yield item
