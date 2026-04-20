"""Unit tests for the line_reader module."""

import bz2
import gzip
import lzma
import zipfile

import pytest

from sr_cli.line_reader import line_reader


def test_line_reader_plain_text(tmp_path):
    """Test line_reader with a plain text file."""
    file_path = tmp_path / "test.txt"
    content = "line1\nline2\nline3"
    file_path.write_text(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_gz(tmp_path):
    """Test line_reader with a .gz compressed file."""
    file_path = tmp_path / "test.txt.gz"
    content = "line1\nline2\nline3"
    with gzip.open(file_path, "wt") as f:
        f.write(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_bz2(tmp_path):
    """Test line_reader with a .bz2 compressed file."""
    file_path = tmp_path / "test.txt.bz2"
    content = "line1\nline2\nline3"
    with bz2.open(file_path, "wt") as f:
        f.write(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_xz(tmp_path):
    """Test line_reader with a .xz compressed file."""
    file_path = tmp_path / "test.txt.xz"
    content = "line1\nline2\nline3"
    with lzma.open(file_path, "wt") as f:
        f.write(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_zip(tmp_path):
    """Test line_reader with a .zip file."""
    zip_path = tmp_path / "test.zip"
    content = "line1\nline2\nline3"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("test.txt", content)
    lines = list(line_reader(zip_path))
    assert lines == ["line1\n", "line2\n", "line3"]


def test_line_reader_empty_file(tmp_path):
    """Test line_reader with an empty file."""
    file_path = tmp_path / "empty.txt"
    file_path.write_text("")
    lines = list(line_reader(file_path))
    assert lines == []


def test_line_reader_no_extension(tmp_path):
    """Test line_reader with a file that has no extension."""
    file_path = tmp_path / "testfile"
    content = "line1\nline2"
    file_path.write_text(content)
    lines = list(line_reader(file_path))
    assert lines == ["line1\n", "line2"]


if __name__ == "__main__":
    pytest.main()
