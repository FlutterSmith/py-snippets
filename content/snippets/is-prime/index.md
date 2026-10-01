---
slug: is-prime
title: "Check if a number is prime"
summary: "Test primality by trial division up to the integer square root."
category: numbers
tags: [validation]
module: numbers/is_prime.py
complexity: "O(√n) time, O(1) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [is-prime]
  change: "Uses math.isqrt, which stays exact for huge n where int(sqrt(n)) rounds; typed."
related: [digitize]
---

Fine up to about 10¹². For bigger numbers, use a probabilistic test like Miller–Rabin.

<?snippet "numbers/is_prime.py"?>
```python
from math import isqrt


def is_prime(n: int) -> bool:
    """Return ``True`` if ``n`` is a prime number."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    # @note isqrt is exact; int(sqrt(n)) can be off by one for huge n
    return all(n % d for d in range(3, isqrt(n) + 1, 2))
```

<?snippet "numbers/is_prime.py" part="examples"?>
```pycon
>>> is_prime(11)
True
>>> [n for n in range(20) if is_prime(n)]
[2, 3, 5, 7, 11, 13, 17, 19]
>>> is_prime(-7)
False
```

## How it works

- Numbers below 2 aren't prime; 2 and 3 are.
- Even numbers are ruled out once, then only odd divisors are tried.
- A divisor above √n would pair with one below it, so the search stops at `isqrt(n)`.
