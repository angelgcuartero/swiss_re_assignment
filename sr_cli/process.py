"""Process log files and perform calculations based on the provided flags."""

import logging
import os
import time
from collections import Counter
from pathlib import Path
from typing import Generator

from sr_cli.utils import calculate_stats, get_formatted_line, get_output_file_name, is_float

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
    num_lines, num_bytes, ip_counter, total_time = process_lines(input_file, output_file)
    return calculate_stats(num_lines, ip_counter, total_time, num_bytes)


def process_lines(input_file: Path, output_file: Path) -> tuple[int, int, Counter, float]:
    """Process each line of the log file, extract relevant data, and write formatted output to the output file.

    Args:
        input_file (Path): The path to the log file to be processed.
        output_file (Path): The path to the output file where results will be saved.
    Returns:
        tuple[int, int, Counter, float]: A tuple containing the number of lines processed, the total number of bytes, a Counter for client IPs, and the total processing time.
    """
    num_lines: int = 0
    num_bytes: int = 0
    ip = Counter()

    with open(output_file, mode="w") as out_file:
        out_file.write("[\n")
        first_line = True
        start_time = time.perf_counter()
        for line in line_reader(input_file):
            if not line.strip():  # Skip empty lines
                continue

            if not first_line:
                out_file.write(",\n")
            first_line = False

            num_lines += 1
            num_bytes += len(line)  # Calculate bytes based on the original line
            parsed_line = parse_line(line.strip())
            client_ip = parsed_line.get("client_ip", "")
            ip[client_ip] += 1
            out_file.write(get_formatted_line(parsed_line))
        end_time = time.perf_counter()
        out_file.write("\n]")
    total_time = end_time - start_time
    return num_lines, num_bytes, ip, total_time


def parse_line(fields: list[str]) -> dict[str, int | str | float]:
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


def line_reader(file_path: Path) -> Generator[str]:
    """Create a generator that yields lines from the file.

    Args:
        file_path: The path to the file to be read.

    Yields:
        str: The lines from the file.
    """
    with open(file_path, mode="r") as file:
        for line in file:
            yield line


if __name__ == "__main__":
    ...
