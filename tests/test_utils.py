"""Test the functionality."""

import pytest

from sr_cli.utils import is_valid_ip


def test_is_valid_ip():
    """Test the is_valid_ip function."""
    assert is_valid_ip("192.168.1.1")
    assert not is_valid_ip("256.0.0.1")
    assert not is_valid_ip("invalid_ip")
    assert not is_valid_ip("192.168.01.1")


def test_simplify_output():
    """Test the simplify_output function."""
    from sr_cli.output import simplify_output

    # Test with a single element
    process_response_single = [{"a": 100, "b": "127.0.0.1", "c": 3.14}]
    assert simplify_output(process_response_single) == process_response_single[0]

    process_response_empty = []
    assert simplify_output(process_response_empty) == process_response_empty

    process_response_multiple = [
        {"a": 100, "b": "127.0.0.1", "c": 3.14},
        {"a": 200, "b": "192.168.1.1", "c": 6.28},
        {"a": 300, "b": "10.0.0.1", "c": 9.42},
    ]
    assert simplify_output(process_response_multiple) == process_response_multiple


if __name__ == "__main__":
    pytest.main()
