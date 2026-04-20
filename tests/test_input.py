"""Unit tests for the line_reader module."""

import bz2
import gzip
import lzma
import zipfile
from pathlib import Path

import pytest

from sr_cli.input import get_file_list, line_reader


def test_get_file_list_single_file(tmp_path: Path):
    """Test get_file_list with a single file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    result = get_file_list(test_file)
    assert result == [test_file]


def test_get_file_list_directory(tmp_path: Path):
    """Test get_file_list with a directory containing multiple files."""
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("content1")
    file2.write_text("content2")

    result = get_file_list(tmp_path)
    assert len(result) == 2
    assert file1 in result
    assert file2 in result


def test_get_file_list_empty_directory(tmp_path: Path):
    """Test get_file_list with an empty directory."""
    result = get_file_list(tmp_path)
    assert result == []


def test_get_file_list_invalid_path():
    """Test get_file_list with an invalid path."""
    invalid_path = Path("/nonexistent/path/to/file.txt")
    result = get_file_list(invalid_path)
    assert result == []


def test_get_file_list_directory_with_subdirs(tmp_path: Path):
    """Test get_file_list ignores subdirectories."""
    file1 = tmp_path / "file1.txt"
    file1.write_text("content")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    file2 = subdir / "file2.txt"
    file2.write_text("content")

    result = get_file_list(tmp_path)
    assert result == [file1]


def test_line_reader_plain_text(tmp_path: Path):
    """Test line_reader with a plain text file."""
    file_path = tmp_path / "test.txt"
    content = "line1\nline2\nline3"
    file_path.write_text(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_gz(tmp_path: Path):
    """Test line_reader with a .gz compressed file."""
    file_path = tmp_path / "test.txt.gz"
    content = "line1\nline2\nline3"
    with gzip.open(file_path, "wt") as f:
        f.write(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_bz2(tmp_path: Path):
    """Test line_reader with a .bz2 compressed file."""
    file_path = tmp_path / "test.txt.bz2"
    content = "line1\nline2\nline3"
    with bz2.open(file_path, "wt") as f:
        f.write(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_xz(tmp_path: Path):
    """Test line_reader with a .xz compressed file."""
    file_path = tmp_path / "test.txt.xz"
    content = "line1\nline2\nline3"
    with lzma.open(file_path, "wt") as f:
        f.write(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_zip(tmp_path: Path):
    """Test line_reader with a .zip file."""
    zip_path = tmp_path / "test.zip"
    content = "line1\nline2\nline3"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("test.txt", content)
    lines = list(line_reader(zip_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_empty_file(tmp_path: Path):
    """Test line_reader with an empty file."""
    file_path = tmp_path / "empty.txt"
    file_path.write_text("")
    lines = list(line_reader(file_path))
    assert lines == []


def test_line_reader_no_extension(tmp_path: Path):
    """Test line_reader with a file that has no extension."""
    file_path = tmp_path / "testfile"
    content = "line1\nline2"
    file_path.write_text(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2"]


if __name__ == "__main__":
    pytest.main()
