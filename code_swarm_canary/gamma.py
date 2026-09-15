def safe_divide(a, b, default=None):
    """Return a / b, or default if b == 0."""
    if b == 0:
        return default
    return a / b