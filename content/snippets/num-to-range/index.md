---
slug: num-to-range
title: "Map a number from one range to another"
summary: "Linearly map a value from one range onto another, like Arduino's map()."
category: numbers
tags: [conversion]
module: numbers/num_to_range.py
complexity: "O(1) time and space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [num-to-range]
  change: "Clearer names; rejects an empty input range; typed."
related: [clamp-number]
---

Turn a 0–1023 sensor reading into 0–100 %, or a score into a colour position.

<?snippet "numbers/num_to_range.py"?>
```python
def num_to_range(
    value: float, in_min: float, in_max: float, out_min: float, out_max: float
) -> float:
    """Map ``value`` from the range ``in_min..in_max`` onto ``out_min..out_max``."""
    if in_min == in_max:
        raise ValueError(f"input range is empty: {in_min} to {in_max}")
    # @note how far along the input range value is, from 0.0 to 1.0
    fraction = (value - in_min) / (in_max - in_min)
    return out_min + fraction * (out_max - out_min)
```

<?snippet "numbers/num_to_range.py" part="examples"?>
```pycon
>>> num_to_range(5, 0, 10, 0, 100)
50.0
>>> num_to_range(25, 0, 100, 1, -1)
0.5
>>> num_to_range(1, 1, 1, 0, 10)
Traceback (most recent call last):
...
ValueError: input range is empty: 1 to 1
```

## How it works

- `fraction` is how far along the input range the value is.
- Scaling that fraction to the output range gives the result. Reversed output ranges work too.
- An empty input range raises instead of dividing by zero.
