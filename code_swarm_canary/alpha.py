def clamp(value, low, high):
    """Return value constrained to the inclusive range [low, high].

    Raises:
        ValueError: if low > high.
    """
    if low > high:
        raise ValueError("low must be less than or equal to high")
    if value < low:
        return low
    if value > high:
        return high
    return value