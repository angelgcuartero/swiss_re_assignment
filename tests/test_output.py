"""Unit tests for the output-related functions."""

import json
from io import StringIO  # Import StringIO for in-memory file handling
from pathlib import Path

import pytest

from sr_cli.output import JSONWriter, TextWriter, get_output_file_name, get_writer_class


def test_get_output_file_name() -> None:
    """Test the get_output_file_name function."""
    # Test with a .json file
    assert get_output_file_name(Path("in_path/data.log"), Path("out_path")) == Path("out_path/data.json")

    # Test with a .txt file
    assert get_output_file_name(Path("in_path/data.log"), Path("out_path"), "TEXT") == Path("out_path/data.txt")

    # Test with a file in a subdirectory
    assert get_output_file_name(Path("folder/file.csv"), Path("out_path")) == Path("out_path/file.json")

    # Test with a file that has no extension
    assert get_output_file_name(Path("filename"), Path("out_path")) == Path("out_path/filename.json")

    # Test with a file that already has .json extension
    assert get_output_file_name(Path("output.json"), Path("out_path")) == Path("out_path/output.json")


def test_get_writer_class() -> None:
    """Test the get_writer_class function."""
    assert get_writer_class("JSON") == JSONWriter
    assert get_writer_class("TEXT") == TextWriter
    with pytest.raises(ValueError):
        get_writer_class("JPEG")


def test_get_formatted_line_simple_dict():
    """Test get_formatted_line with a simple dictionary."""
    parsed_line = {"ip": "192.168.1.1", "method": "GET"}
    writer = JSONWriter(None)  # Pass None since we won't actually write to a file
    result = writer.get_formatted_line(parsed_line)
    assert result == '{"ip": "192.168.1.1", "method": "GET"}'


def test_get_formatted_line_with_numbers():
    """Test get_formatted_line with numeric values."""
    parsed_line = {"status": 200, "bytes": 1024, "response_time": 0.5}
    writer = JSONWriter(None)
    result = writer.get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_get_formatted_line_empty_dict():
    """Test get_formatted_line with an empty dictionary."""
    parsed_line = {}
    writer = JSONWriter(None)
    result = writer.get_formatted_line(parsed_line)
    assert result == "{}"


def test_get_formatted_line_nested_dict():
    """Test get_formatted_line with nested dictionary."""
    parsed_line = {"request": {"method": "POST", "path": "/api/users"}}
    writer = JSONWriter(None)
    result = writer.get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_get_formatted_line_with_list():
    """Test get_formatted_line with a dictionary containing a list."""
    parsed_line = {"tags": ["error", "critical"], "count": 2}
    writer = JSONWriter(None)
    result = writer.get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_get_formatted_line_with_null_values():
    """Test get_formatted_line with null values."""
    parsed_line = {"ip": "192.168.1.1", "error": None}
    writer = JSONWriter(None)
    result = writer.get_formatted_line(parsed_line)
    assert json.loads(result) == parsed_line


def test_JSONWriter_write_line():
    """Test the write_line method of JSONWriter."""
    output = StringIO()
    writer = JSONWriter(output)
    writer.write_line({"ip": "192.168.1.1", "method": "GET"})
    writer.finalize()
    assert output.getvalue() == '[\n{"ip": "192.168.1.1", "method": "GET"}\n]'


def test_TextWriter_get_formatted_line():
    """Test the get_formatted_line method of TextWriter."""
    output = StringIO()
    writer = TextWriter(output)
    result = writer.get_formatted_line({"ip": "192.168.1.1", "method": "GET"})
    assert result == "ip: 192.168.1.1 | method: GET"
    assert output.getvalue() == ""  # Ensure that get_formatted_line does not write to the output


if __name__ == "__main__":
    pytest.main()
