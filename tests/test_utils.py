"""Unit tests for the utils module."""

import json
from collections import Counter
from pathlib import Path

import pytest

from sr_cli.process import get_file_list
from sr_cli.utils import calculate_stats, get_formatted_line, get_output_file_name, is_float


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


def test_get_file_list_invalid_path():
    """Test get_file_list with an invalid path."""
    invalid_path = Path("/nonexistent/path/to/file.txt")
    result = get_file_list(invalid_path)
    assert result == []


def test_get_output_file_name() -> None:
    """Test the get_output_file_name function."""
    # Test with a .csv file
    assert get_output_file_name(Path("in_path/data.csv"), Path("out_path")) == Path("out_path/data.json")

    # Test with a file in a subdirectory
    assert get_output_file_name(Path("folder/file.csv"), Path("out_path")) == Path("out_path/file.json")

    # Test with a file that has no extension
    assert get_output_file_name(Path("filename"), Path("out_path")) == Path("out_path/filename.json")

    # Test with a file that already has .json extension
    assert get_output_file_name(Path("output.json"), Path("out_path")) == Path("out_path/output.json")


def test_get_formatted_line_simple_dict():
    """Test get_formatted_line with a simple dictionary."""
    parsed_line = {"ip": "192.168.1.1", "method": "GET"}
    result = get_formatted_line(parsed_line)
    assert result == '{"ip": "192.168.1.1", "method": "GET"}'


def test_get_formatted_line_with_numbers():
    """Test get_formatted_line with numeric values."""
    parsed_line = {"status": 200, "bytes": 1024, "response_time": 0.5}
    result = get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_get_formatted_line_empty_dict():
    """Test get_formatted_line with an empty dictionary."""
    parsed_line = {}
    result = get_formatted_line(parsed_line)
    assert result == "{}"


def test_get_formatted_line_nested_dict():
    """Test get_formatted_line with nested dictionary."""
    parsed_line = {"request": {"method": "POST", "path": "/api/users"}}
    result = get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_get_formatted_line_with_list():
    """Test get_formatted_line with a dictionary containing a list."""
    parsed_line = {"tags": ["error", "critical"], "count": 2}
    result = get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_get_formatted_line_with_null_values():
    """Test get_formatted_line with null values."""
    parsed_line = {"ip": "192.168.1.1", "error": None}
    result = get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_calculate_stats_with_data():
    """Test calculate_stats with valid data."""
    ip_counter = Counter({"192.168.1.1": 5, "192.168.1.2": 3, "192.168.1.3": 1})
    result = calculate_stats(num_lines=9, ip_counter=ip_counter, total_time=2.0, total_bytes=1024)

    assert result["num_lines"] == 9
    assert result["mfip"] == "192.168.1.1"
    assert result["lfip"] == "192.168.1.3"
    assert result["eps"] == 4.5
    assert result["bytes"] == 1024


def test_calculate_stats_empty_counter():
    """Test calculate_stats with an empty IP counter."""
    ip_counter = Counter()
    result = calculate_stats(num_lines=0, ip_counter=ip_counter, total_time=1.0, total_bytes=0)

    assert result["num_lines"] == 0
    assert result["mfip"] == ""
    assert result["lfip"] == ""
    assert result["eps"] == 0.0
    assert result["bytes"] == 0


def test_calculate_stats_zero_total_time():
    """Test calculate_stats with zero total time."""
    ip_counter = Counter({"192.168.1.1": 5})
    result = calculate_stats(num_lines=5, ip_counter=ip_counter, total_time=0, total_bytes=512)

    assert result["num_lines"] == 5
    assert result["mfip"] == "192.168.1.1"
    assert result["eps"] is None
    assert result["bytes"] == 512


def test_calculate_stats_single_ip():
    """Test calculate_stats with a single IP address."""
    ip_counter = Counter({"10.0.0.1": 10})
    result = calculate_stats(num_lines=10, ip_counter=ip_counter, total_time=5.0, total_bytes=2048)

    assert result["mfip"] == "10.0.0.1"
    assert result["lfip"] == "10.0.0.1"
    assert result["eps"] == 2.0


if __name__ == "__main__":
    pytest.main()
