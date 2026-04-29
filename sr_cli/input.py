"""Module for reading lines from various file formats, including compressed files."""

import bz2
import gzip
import io
import logging
import lzma
import os
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def get_file_list(input_path: Path) -> list[Path]:
    """Get a list of files from the input path.

    Args:
        input_path: The path to the input file or directory.

    Returns:
        list[Path]: A list of file paths.

    """
    if input_path.is_file():
        return [input_path]
    elif input_path.is_dir():
        return [f for f in input_path.iterdir() if f.is_file()]
    else:
        log.error(f"Invalid input path: {input_path}")
        return []


def _get_custom_reader(file_path) -> tuple[callable, str]:
    """Return the appropriate reader function based on the file extension.

    Args:
        file_path: The path to the file to be read.
    Returns:
        A tuple containing the reader function and mode.
    """
    readers = {".gz": gzip.open, ".bz2": bz2.open, ".xz": lzma.open}

    if file_path.suffix == ".zip":
        zf = zipfile.ZipFile(file_path)
        file_name = zf.namelist()[0]

        # Return a function that ignores the mode and returns the text stream.
        # ZipFile should be closed after reading, so adding the decorator
        # contextlib.contextmanager manages this resource properly
        @contextmanager
        def zip_reader_wrapper():
            raw_file = zf.open(file_name, "r")
            # Wrap the raw bytes in a TextIOWrapper to read it as text because
            # zipfile returns a binary file-like object
            yield io.TextIOWrapper(raw_file, encoding="utf-8")

        return zip_reader_wrapper, "r"
    elif file_path.suffix in readers:
        return readers[file_path.suffix], "rt"
    else:
        return open, "rt"


def line_reader(file_path: Path) -> Generator[str, None, None]:
    """Create a generator that yields lines from the file.

    Args:
        file_path: The path to the file to be read.

    Yields:
        str: The lines from the file.
    """
    custom_reader, mode = _get_custom_reader(file_path)
    with custom_reader(file_path, mode=mode, encoding="utf-8") as file:
        for line in file:
            yield line


if __name__ == "__main__":
    ...
