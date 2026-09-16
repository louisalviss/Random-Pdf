"""
auto_beta.py

A simple module providing a pure function to check if an integer is even.
"""

def is_even(value: int) -> bool:
    """Return True if value is even, False otherwise.

    Args:
        value (int): The integer to test.

    Returns:
        bool: True if value is even, False if odd.
    """
    return value % 2 == 0
