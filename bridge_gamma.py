"""
bridge_gamma.py

Utility function to check if a string is non-empty after stripping whitespace.
"""


def nonempty(text: str) -> bool:
    """
    Return True if the stripped text is non-empty, False otherwise.

    Args:
        text: Input string to check.

    Returns:
        bool: True if stripped text is non-empty, False otherwise.
    """
    return bool(text.strip())
