import pytest
from sr_cli.process import parse_line

"""Test the parse_line function."""


def test_parse_line_valid_input():
    """Test parse_line with valid log line input."""
    line = "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = parse_line(line)

    assert result["timestamp"] == 1157689312.049
    assert result["response_header_size"] == 5006
    assert result["client_ip"] == "10.105.21.199"
    assert result["http_response_code"] == "TCP_MISS/200"
    assert result["response_size"] == 19763
    assert result["http_request_method"] == "CONNECT"
    assert result["url"] == "login.yahoo.com:443"
    assert result["username"] == "badeyek"
    assert result["access_destination_ip"] == "DIRECT/209.73.177.115"
    assert result["response_type"] == "-"


def test_parse_line_multiple_entries():
    """Test parse_line with multiple different log entries."""
    lines = [
        "1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html",
        "1157689321.315      1 10.105.21.199 TCP_HIT/200 1464 GET http://www.goonernews.com/styles.css fake_user NONE/- text/css",
    ]

    results = [
        {
            "timestamp": 1157689320.327,
            "response_header_size": 2864,
            "client_ip": "10.105.21.199",
            "http_response_code": "TCP_MISS/200",
            "response_size": 10182,
            "http_request_method": "GET",
            "url": "http://www.goonernews.com/",
            "username": "badeyek",
            "access_destination_ip": "DIRECT/207.58.145.61",
            "response_type": "text/html",
        },
        {
            "timestamp": 1157689321.315,
            "response_header_size": 1,
            "client_ip": "10.105.21.199",
            "http_response_code": "TCP_HIT/200",
            "response_size": 1464,
            "http_request_method": "GET",
            "url": "http://www.goonernews.com/styles.css",
            "username": "fake_user",
            "access_destination_ip": "NONE/-",
            "response_type": "text/css",
        },
    ]

    for line, expected in zip(lines, results, strict=False):
        result = parse_line(line)
        assert result == expected


def test_parse_line_invalid_timestamp():
    """Test parse_line with invalid timestamp."""
    line = "invalid_timestamp   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = parse_line(line)

    assert result["timestamp"] == 0.0


def test_parse_line_invalid_response_header_size():
    """Test parse_line with invalid response header size."""
    line = "1157689312.049   invalid 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = parse_line(line)

    assert result["response_header_size"] == 0


def test_parse_line_invalid_response_size():
    """Test parse_line with invalid response size."""
    line = "1157689312.049   5006 10.105.21.199 TCP_MISS/200 invalid CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = parse_line(line)

    assert result["response_size"] == 0


def test_parse_line_short_line():
    """Test parse_line with a line that has fewer fields than expected."""
    line = "1157689312.049"
    result = parse_line(line)
    assert result["timestamp"] == 1157689312.049
    assert result["response_header_size"] == 0
    assert result["client_ip"] == ""
    assert result["http_response_code"] == ""
    assert result["response_size"] == 0
    assert result["http_request_method"] == ""
    assert result["url"] == ""
    assert result["username"] == ""
    assert result["access_destination_ip"] == ""
    assert result["response_type"] == ""
