"""Process log files and perform calculations based on the provided flags."""

import logging
import os
from pathlib import Path

from sr_cli.input import line_reader
from sr_cli.output import get_output_file_name, get_writer_class
from sr_cli.statistics import Statistics
from sr_cli.utils import is_float

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def process_data_file(input_file: Path, output_path: Path) -> dict[str, int | str | float]:
    """Read the log file and process its contents.

    Args:
        input_file (Path): The path to the log file to be processed.
        output_path (Path): The path to the output file where results will be saved.
    Returns:
        dict[str, int | str | float]: A dictionary containing the processed results.
    """
    output_file = get_output_file_name(input_file, output_path)
    return _process_lines(input_file, output_file)


def _process_lines(input_file: Path, output_file: Path, format="JSON") -> dict[str, int | str | float]:
    """Process each line of the log file, extract relevant data, and write formatted output to the output file.

    Args:
        input_file (Path): The path to the log file to be processed.
        output_file (Path): The path to the output file where results will be saved.
        format (str): The format for the output file.
    Returns:
        dict[str, int | str | float]: A dictionary containing the processed results.
    """
    with open(output_file, mode="w") as output_file_handle:
        writer = get_writer_class(format)(output_file_handle)
        stats = Statistics()
        for line in line_reader(input_file):
            parsed_line = _parse_line(line.strip())
            writer.write_line(parsed_line)
            stats.update(parsed_line.get("client_ip"), len(line))
        writer.finalize()
    return stats.calculate_stats()


def _parse_line(fields: list[str]) -> dict[str, int | str | float]:
    """Parse a log line and extract relevant fields. This is an example of the list of fields.

    Args:
        fields (list[str]): A list of strings representing the fields in a log line.

    Returns:
        tuple[int, str, int]: A tuple containing the response header size, client IP, and response size.
    """
    # Extract the first field (timestamp) and strip and split the rest
    try:
        timestamp, rest_of_fields = fields.strip().split(" ", 1)
        rest_of_fields = rest_of_fields.lstrip().split(" ")
    except ValueError:
        timestamp = fields.strip().split(" ", 1)[0]
        rest_of_fields = []

    all_fields = [*[timestamp], *rest_of_fields]

    # Initialize the response dictionary with default values
    response = {
        "timestamp": 0.0,
        "response_header_size": 0,
        "client_ip": "",
        "http_response_code": "",
        "response_size": 0,
        "http_request_method": "",
        "url": "",
        "username": "",
        "access_destination_ip": "",
        "response_type": "",
    }

    # Avoid using zip with strict=True to prevent issues with mismatched field counts, and instead handle it gracefully
    for key, field in zip(response.keys(), all_fields, strict=False):
        response[key] = field

    # Fix data types for specific fields
    response["timestamp"] = float(response["timestamp"]) if is_float(response["timestamp"]) else 0.0
    response["response_header_size"] = (
        int(response["response_header_size"])
        if isinstance(response["response_header_size"], str) and response["response_header_size"].isdigit()
        else 0
    )
    response["response_size"] = (
        int(response["response_size"]) if isinstance(response["response_size"], str) and response["response_size"].isdigit() else 0
    )

    return response


if __name__ == "__main__":
    ...
