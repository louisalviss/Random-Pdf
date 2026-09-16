"""
auto_prod_beta.py

Utility module for checking whether a given integer value is even.
"""


def is_even(value: int) -> bool:
    """
    Return True if the given integer value is even, otherwise False.

    An even number is an integer that is divisible by 2 without a remainder.

    Parameters
    ----------
    value : int
        The integer value to check.

    Returns
    -------
    bool
        True if value is even, False otherwise.

    Examples
    --------
    >>> is_even(4)
    True
    >>> is_even(7)
    False
    >>> is_even(0)
    True
    """
    return value % 2 == 0
