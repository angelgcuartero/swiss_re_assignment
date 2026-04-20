"""Unit tests for the utils module."""

import pytest

from sr_cli.utils import is_float


def test_is_float_valid_integers():
    """Test is_float with valid integer strings."""
    assert is_float("0") is True
    assert is_float("42") is True
    assert is_float("-10") is True


def test_is_float_valid_floats():
    """Test is_float with valid float strings."""
    assert is_float("3.14") is True
    assert is_float("-2.5") is True
    assert is_float("0.0") is True
    assert is_float(".5") is True
    assert is_float("1.") is True


def test_is_float_scientific_notation():
    """Test is_float with scientific notation."""
    assert is_float("1e10") is True
    assert is_float("1.5e-3") is True
    assert is_float("-2E+5") is True


def test_is_float_invalid_strings():
    """Test is_float with invalid strings."""
    assert is_float("not_a_number") is False
    assert is_float("12.34.56") is False
    assert is_float("") is False
    assert is_float("abc123") is False


def test_is_float_whitespace():
    """Test is_float with whitespace."""
    assert is_float(" 42 ") is True
    assert is_float("  3.14  ") is True
    assert is_float("\t5.0\n") is True


def test_is_float_special_values():
    """Test is_float with special float values."""
    assert is_float("inf") is True
    assert is_float("-inf") is True
    assert is_float("nan") is True


if __name__ == "__main__":
    pytest.main()
