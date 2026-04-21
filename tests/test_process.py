"""Unit tests for the process module."""

from pathlib import Path

import pytest

from sr_cli.process import _parse_line, line_reader, process_data_file


def test_parse_line_valid_input():
    """Test parse_line with valid log line input."""
    line = "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = _parse_line(line)

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
        result = _parse_line(line)
        assert result == expected


def test_parse_line_invalid_timestamp():
    """Test parse_line with invalid timestamp, should be float."""
    line = "invalid_timestamp   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = _parse_line(line)

    assert isinstance(result["timestamp"], float)
    assert result["timestamp"] == 0.0


def test_parse_line_invalid_response_header_size():
    """Test parse_line with invalid response header size, should be numeric."""
    line = "1157689312.049   invalid 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = _parse_line(line)

    assert isinstance(result["response_header_size"], int)
    assert result["response_header_size"] == 0


def test_parse_line_invalid_response_size():
    """Test parse_line with invalid response size, should be numeric."""
    line = "1157689312.049   5006 10.105.21.199 TCP_MISS/200 invalid CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"
    result = _parse_line(line)

    assert isinstance(result["response_size"], int)
    assert result["response_size"] == 0


def test_parse_line_short_line():
    """Test parse_line with a line that has fewer fields than expected."""
    line = "1157689312.049"
    result = _parse_line(line)
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


def test_line_reader_single_line(tmp_path: Path):
    """Test line_reader with a file containing a single line."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("single line")

    lines = list(line_reader(test_file))
    assert len(lines) == 1
    assert lines[0] == "single line"


def test_line_reader_multiple_lines(tmp_path: Path):
    """Test line_reader with a file containing multiple lines."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("line1\nline2\nline3\n")

    lines = list(line_reader(test_file))
    assert len(lines) == 3
    assert lines[0] == "line1\n"
    assert lines[1] == "line2\n"
    assert lines[2] == "line3\n"


def test_line_reader_empty_file(tmp_path: Path):
    """Test line_reader with an empty file."""
    test_file = tmp_path / "empty.txt"
    test_file.write_text("")

    lines = list(line_reader(test_file))
    assert len(lines) == 0


def test_process_data_file_single_file(tmp_path: Path):
    """Test process_data_file with a single log file."""
    input_file = tmp_path / "input.txt"
    output_path = tmp_path / "output"
    output_path.mkdir()

    input_file.write_text(
        "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -\n"
    )

    result = process_data_file(input_file, output_path)

    assert isinstance(result, dict)
    assert "num_lines" in result
    assert result["num_lines"] == 1
    assert "bytes" in result
    assert "mfip" in result


def test_process_data_file_multiple_lines(tmp_path: Path):
    """Test process_data_file with multiple log lines."""
    input_file = tmp_path / "input.txt"
    output_path = tmp_path / "output"
    output_path.mkdir()

    input_file.write_text(
        "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -\n"
        "1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html\n"
    )

    result = process_data_file(input_file, output_path)

    assert result["num_lines"] == 2
    assert result["mfip"] == "10.105.21.199"
    assert isinstance(result["eps"], float)


def test_process_data_file_creates_output_file(tmp_path: Path):
    """Test process_data_file creates an output file."""
    input_file = tmp_path / "input.txt"
    output_path = tmp_path / "output"
    output_path.mkdir()

    input_file.write_text(
        "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -\n"
    )

    process_data_file(input_file, output_path)
    output_files = list(f for f in output_path.iterdir() if f.is_file())

    assert len(output_files) > 0


def test_process_data_file_with_empty_lines(tmp_path: Path):
    """Test process_data_file skips empty lines."""
    input_file = tmp_path / "input.txt"
    output_path = tmp_path / "output"
    output_path.mkdir()

    input_file.write_text(
        "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -\n"
        "\n"
        "1157689320.327   2864 10.105.21.200 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html\n"
    )

    result = process_data_file(input_file, output_path)

    assert result["num_lines"] == 3


if __name__ == "__main__":
    pytest.main()
