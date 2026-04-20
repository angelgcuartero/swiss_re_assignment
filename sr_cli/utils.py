"""Useful utility functions for the swiss-re-assignment CLI."""

from collections import Counter


def is_float(value: str) -> bool:
    """Check if the provided string can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    ...
