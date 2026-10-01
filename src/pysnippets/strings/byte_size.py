def byte_size(text: str, encoding: str = "utf-8") -> int:
    """Return the number of bytes ``text`` takes up in ``encoding``.

    >>> byte_size("Hello World")
    11
    >>> byte_size("😀")
    4
    >>> byte_size("😀", "utf-16")
    6
    """
    # @note len(text) counts code points; this counts bytes
    return len(text.encode(encoding))
