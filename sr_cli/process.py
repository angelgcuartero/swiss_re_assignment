"""Process log files and perform calculations based on the provided flags."""

import logging
import os
import time
from ast import List
from collections import Counter

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)


def process_files(
    input_file: List[str] | str,
    output_file: str,
    **kwargs,
) -> list[dict[str, int | str | float]]:
    """Process log files and perform calculations based on the provided flags.

    Args:
        input_file (List[str] | str): A list of input file paths or a single input file path.
        output_file (str): The output file path where results will be saved.
        **kwargs: Additional keyword arguments for processing.

    Returns:
        list[dict[str, int | str | float]]: A list of dictionaries containing the results of processing each input file.

    """
    input_files = [input_file] if isinstance(input_file, str) else input_file
    response = []

    # Log the input and output file paths and any additional keyword arguments
    for file in input_files:
        log.debug(f"Input file: {file}")
    log.debug(f"Output file: {output_file}")
    for key, value in kwargs.items():
        log.debug(f"{key}: {value}")

    for file in input_files:
        log.debug(f"Processing file: {file}")
        result_dict = read_data_file(file)
        for key, value in result_dict.items():
            log.debug(f"{key}: {value}")
        response.append(result_dict)
    return response


def read_data_file(file_path: str) -> dict[str, int | str | float]:
    """Read the log file and process its contents.

    Args:
        file_path (str): The path to the log file to be processed.

    Returns:
        dict[str, int | str | float]: A dictionary containing the processed results.

    """
    res_num_lines = 0
    res_mfip = ""
    res_lfip = ""
    res_eps: float = 0.0
    res_bytes: int = 0
    res_ip = Counter()

    start_time = time.perf_counter()
    with open(file_path, mode="r") as file:
        for line in file:
            if not line.strip():
                continue
            res_num_lines += 1
            response_header_size, client_ip, response_size = parse_line(line.strip())
            res_bytes += response_header_size + response_size
            res_ip[client_ip] += 1
    end_time = time.perf_counter()
    total_time = end_time - start_time

    # Calculate most and least frequent IPs
    if res_ip:
        res_mfip = res_ip.most_common(1)[0][0]
        res_lfip = res_ip.most_common()[-1][0]

    # Calculate events per second
    res_eps = (
        res_num_lines / total_time if total_time > 0 else None
    )  # Avoid division by zero

    return {
        "num_lines": res_num_lines,
        "mfip": res_mfip,
        "lfip": res_lfip,
        "eps": res_eps,
        "bytes": res_bytes,
    }


def parse_line(fields: List[str]) -> tuple[int, str, int]:
    """Parse a log line and extract relevant fields.

    Args:
        fields (List[str]): A list of strings representing the fields in a log line.

    Returns:
        tuple[int, str, int]: A tuple containing the response header size, client IP, and response size.

    """
    # Discard the first field (timestamp) and split the rest of the fields
    _, rest_of_fields = fields.strip().split(" ", 1)
    rest_of_fields = rest_of_fields.lstrip().split(" ")
    response_header_size_str = rest_of_fields[
        0
    ]  # Field 2: 1372 [Response header size in bytes]
    client_ip = rest_of_fields[1]  # Field 3: 10.105.21.199 [Client IP address]
    response_size_str = rest_of_fields[3]  # Field 5: 399 [Response size in bytes]

    response_header_size = (
        int(response_header_size_str) if response_header_size_str.isdigit() else 0
    )
    response_size = int(response_size_str) if response_size_str.isdigit() else 0
    return response_header_size, client_ip, response_size
