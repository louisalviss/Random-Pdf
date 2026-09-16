"""
auto_prod_alpha.py

Utility module cung cấp hàm clamp (đánh giá giá trị và giới hạn).

Cách dùng:
    from auto_prod_alpha import clamp
    result = clamp(15, 0, 10)  # Trả về 10
"""

def clamp(value, low, high):
    """
    Đánh giá giá trị về khoảng [low, high].

    Nếu value nhỏ hơn low, trả về low.
    Nếu value lớn hơn high, trả về high.
    Ngược lại trả về value.

    Args:
        value (int | float): Giá trị cần đánh giá.
        low (int | float): Giới hạn dưới.
        high (int | float): Giới hạn trên.

    Returns:
        int | float: Giá trị đã được giới hạn trong khoảng [low, high].

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
