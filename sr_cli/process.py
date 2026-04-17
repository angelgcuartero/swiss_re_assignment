"""Process log files and perform calculations based on the provided flags."""

import logging
import os
import time
from ast import List
from collections import Counter

from sr_cli.utils import is_float

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


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
    res_eps = res_num_lines / total_time if total_time > 0 else None  # Avoid division by zero

    return {
        "num_lines": res_num_lines,
        "mfip": res_mfip,
        "lfip": res_lfip,
        "eps": res_eps,
        "bytes": res_bytes,
    }


def parse_line(fields: List[str]) -> tuple[int, str, int]:
    """Parse a log line and extract relevant fields. This is an example of the list of fields:

    Field 1: 1157689324.156 [Timestamp in seconds since the epoch]
    Field 2: 1372 [Response header size in bytes]
    Field 3: 10.105.21.199 [Client IP address]
    Field 4: TCP_MISS/200 [HTTP response code]
    Field 5: 399 [Response size in bytes]
    Field 6: GET [HTTP request method]
    Field 7: http://www.google-analytics.com/__utm.gif? [URL]
    Field 8: badeyek [Username]
    Field 9: DIRECT/66.102.9.147 [Type of access/destination IP address]
    Field 10: image/gif [Response type]

    Args:
        fields (List[str]): A list of strings representing the fields in a log line.

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
