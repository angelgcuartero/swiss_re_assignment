"""Module for handling output file naming and related utilities."""

import json
from abc import ABC, abstractmethod
from io import TextIOWrapper
from pathlib import Path


def get_output_file_name(input_file: Path, output_path: Path, format: str = "JSON") -> Path:
    """Generate an output file name based on the input file name.

    Args:
        input_file (Path): The path to the input file.
        output_path (Path): The directory where the output file should be saved.
        format (str): The format for the output file.

    Returns:
        Path: The path to the output file.
    """
    extensions = {
        "JSON": "json",
        "TEXT": "txt",
    }
    output_file: Path = output_path / f"{input_file.stem}.{extensions.get(format.upper(), '.json')}"
    return output_file


class Writer(ABC):
    """Base class for handling output writing."""

    def __init__(self, output_file: TextIOWrapper):
        """Initialize the Writer with the output file."""
        self.output_file = output_file

    @abstractmethod
    def get_formatted_line(self, parsed_line: dict) -> str:
        """Format the parsed line for output."""
        raise NotImplementedError("Subclasses must implement the get_formatted_line method.")

    @abstractmethod
    def write_line(self, line: dict):
        """Write a formatted line to the output file."""
        raise NotImplementedError

    @abstractmethod
    def finalize(self):
        """Finalize the output file."""
        raise NotImplementedError


class JSONWriter(Writer):
    """Class to handle writing JSON-formatted lines to an output file."""

    def __init__(self, output_file: TextIOWrapper):
        """Initialize the JSONWriter with the output file."""
        self.format = "JSON"
        super().__init__(output_file)
        self.first_line = True

    def get_formatted_line(self, parsed_line: dict) -> str:
        """Format the parsed line as a JSON string."""
        return json.dumps(parsed_line)

    def write_line(self, line: dict) -> None:
        """Write a formatted line to the output file, handling commas and newlines appropriately."""
        if self.first_line:
            self.output_file.write("[\n")
            self.first_line = False
        else:
            self.output_file.write(",\n")
        formatted_line = self.get_formatted_line(line)
        self.output_file.write(formatted_line)

    def finalize(self) -> None:
        """Finalize the output file by writing the closing bracket if necessary."""
        if not self.first_line:  # Only write closing bracket if we have written at least one line
            self.output_file.write("\n]")


class TextWriter(Writer):
    """Class to handle writing plain text lines to an output file."""

    def __init__(self, output_file):
        """Initialize the TextWriter with the output file."""
        super().__init__(output_file)
        self.format = "TEXT"

    def get_formatted_line(self, parsed_line: dict) -> str:
        """Format the parsed line as a plain text string."""
        return " | ".join(f"{key}: {value or '-'}" for key, value in parsed_line.items())

    def write_line(self, line: dict) -> None:
        """Write a line of text to the output plain text file."""
        formatted_line = self.get_formatted_line(line)
        self.output_file.write(f"{formatted_line}\n")

    def finalize(self) -> None:
        """Finalize the output file (no special handling needed for plain text)."""
        pass


def get_writer_class(format: str = "JSON") -> Writer:
    """Get the appropriate Writer class based on the specified format.

    Args:
        format (str): The format for which to get the Writer class (e.g., "json").

    Returns:
        type: The Writer class corresponding to the specified format.

    Raises:
        ValueError: If the specified format is not supported.
    """
    match format.upper():
        case "JSON":
            return JSONWriter
        case "TEXT":
            return TextWriter
        case _:
            raise ValueError(f"Unsupported format: {format}")


if __name__ == "__main__":
    ...
