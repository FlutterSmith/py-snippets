from math import isqrt


def is_prime(n: int) -> bool:
    """Return ``True`` if ``n`` is a prime number.

    >>> is_prime(11)
    True
    >>> [n for n in range(20) if is_prime(n)]
    [2, 3, 5, 7, 11, 13, 17, 19]
    >>> is_prime(-7)
    False
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    # @note isqrt is exact; int(sqrt(n)) can be off by one for huge n
    return all(n % d for d in range(3, isqrt(n) + 1, 2))
