def num_to_range(
    value: float, in_min: float, in_max: float, out_min: float, out_max: float
) -> float:
    """Map ``value`` from the range ``in_min..in_max`` onto ``out_min..out_max``.

    Values outside the input range map outside the output range; clamp first
    if that's not what you want.

    >>> num_to_range(5, 0, 10, 0, 100)
    50.0
    >>> num_to_range(25, 0, 100, 1, -1)
    0.5
    >>> num_to_range(1, 1, 1, 0, 10)
    Traceback (most recent call last):
    ...
    ValueError: input range is empty: 1 to 1
    """
    if in_min == in_max:
        raise ValueError(f"input range is empty: {in_min} to {in_max}")
    # @note how far along the input range value is, from 0.0 to 1.0
    fraction = (value - in_min) / (in_max - in_min)
    return out_min + fraction * (out_max - out_min)
