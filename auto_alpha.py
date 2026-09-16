"""
auto_alpha.py

Utility module providing a pure, documented clamp function.
"""


def clamp(value: float, low: float, high: float) -> float:
    """
    Clamp a value to the inclusive range [low, high].

    Args:
        value: The number to clamp.
        low: The lower bound of the range (inclusive).
        high: The upper bound of the range (inclusive).

    Returns:
        The clamped value. If value < low, returns low.
        If value > high, returns high. Otherwise returns value.

    Examples:
        >>> clamp(5, 0, 10)
        5
        >>> clamp(-3, 0, 10)
        0
        >>> clamp(15, 0, 10)
        10
    """
    if value < low:
        return low
    if value > high:
        return high
    return value
