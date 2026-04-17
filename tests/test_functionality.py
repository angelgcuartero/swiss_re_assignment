"""Test the functionality."""

import pytest

from sr_cli.process import parse_line
from sr_cli.utils import is_valid_ip


def test_is_valid_ip():
    """Test the is_valid_ip function."""
    assert is_valid_ip("192.168.1.1")
    assert not is_valid_ip("256.0.0.1")
    assert not is_valid_ip("invalid_ip")
    assert not is_valid_ip("192.168.01.1")


def test_parse_line():
    """Test the parse_line function."""
    lines = [
        "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -",
        "1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html",
        "1157689320.343   1357 10.105.21.199 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -",
        "1157689321.315      1 10.105.21.199 TCP_HIT/200 1464 GET http://www.goonernews.com/styles.css badeyek NONE/- text/css",
    ]

    parsed_lines = [
        (5006, "10.105.21.199", 19763),
        (2864, "10.105.21.199", 10182),
        (1357, "10.105.21.199", 214),
        (1, "10.105.21.199", 1464),
    ]

    for i, line in enumerate(lines):
        assert parse_line(line) == parsed_lines[i]


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
