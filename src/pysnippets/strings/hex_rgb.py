def hex_to_rgb(color: str) -> tuple[int, int, int]:
    """Convert ``"#RRGGBB"`` or ``"RGB"`` shorthand to an ``(r, g, b)`` tuple.

    >>> hex_to_rgb("#FFA501")
    (255, 165, 1)
    >>> hex_to_rgb("0af")
    (0, 170, 255)
    """
    digits = color.removeprefix("#")
    # @note "0af" is shorthand for "00aaff"
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    if len(digits) != 6:
        raise ValueError(f"expected 3 or 6 hex digits, got {color!r}")
    value = int(digits, 16)
    return value >> 16, (value >> 8) & 0xFF, value & 0xFF


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert red, green and blue (each 0-255) to ``"#RRGGBB"``.

    >>> rgb_to_hex(255, 165, 1)
    '#FFA501'
    >>> rgb_to_hex(256, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: channels must be 0-255, got (256, 0, 0)
    """
    if not all(0 <= c <= 255 for c in (r, g, b)):
        raise ValueError(f"channels must be 0-255, got {(r, g, b)}")
    # @note 02X: two uppercase hex digits, zero-padded
    return f"#{r:02X}{g:02X}{b:02X}"
