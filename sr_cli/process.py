"""Process log files and perform calculations based on the provided flags."""

import logging
import os
import time
from ast import List
from collections import Counter

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


# Sample log line format:
# Field 1: 1157689324.156 [Timestamp in seconds since the epoch]
# Field 2: 1372 [Response header size in bytes]
# Field 3: 10.105.21.199 [Client IP address]
# Field 4: TCP_MISS/200 [HTTP response code]
# Field 5: 399 [Response size in bytes]
# Field 6: GET [HTTP request method]
# Field 7: http://www.google-analytics.com/__utm.gif? [URL]
# Field 8: badeyek [Username]
# Field 9: DIRECT/66.102.9.147 [Type of access/destination IP address]
# Field 10: image/gif [Response type]


def process_log_files(
    input_file: List[str] | str,
    output_file: str,
    **kwargs,
) -> tuple:
    """Process log files and perform calculations based on the provided flags."""
    input_files = [input_file] if isinstance(input_file, str) else input_file

    # for file in input_files:
    #     log.debug(f"Input file: {file}")
    # log.debug(f"Output file: {output_file}")
    # log.debug(f"Most frequent IP flag: {kwargs.get('calculate_mfip', False)}")
    # log.debug(f"Least frequent IP flag: {kwargs.get('calculate_lfip', False)}")
    # log.debug(f"Events per second flag: {kwargs.get('calculate_eps', False)}")
    # log.debug(f"Total bytes exchanged flag: {kwargs.get('calculate_bytes', False)}")

    # Measure the time taken to read the file
    start_time = time.perf_counter()
    num_lines, mfip, lfip, eps, total_bytes = read_data_file(input_files[0])
    end_time = time.perf_counter()
    total_time = end_time - start_time

    log.info(f"Time taken to read the file: {total_time:.4f} seconds")
    log.info(f"Total lines read: {num_lines}")
    log.info(f"Most frequent IP: {mfip}")
    log.info(f"Least frequent IP: {lfip}")
    log.info(f"Events per second: {eps}")
    log.info(f"Total bytes exchanged: {total_bytes}")
    return num_lines, mfip, lfip, eps, total_bytes


def read_data_file(file_path: str) -> tuple[int, str, str, float, int]:
    """Read the log file and process its contents."""
    res_num_lines = 0
    res_mfip = ""
    res_lfip = ""
    res_eps: float = 0.0
    res_bytes: int = 0
    with open(file_path, mode="r") as file:
        for line in file:
            # fields = line.strip().split(" ", 1)
            if not line.strip():
                continue
            # if len(fields) < 2:
            #     continue
            res_num_lines += 1
            response_header_size, client_ip, response_size = parse_line(line.strip())
            res_bytes += response_header_size + response_size

    return res_num_lines, res_mfip, res_lfip, res_eps, res_bytes


def parse_line(fields: List[str]) -> tuple[int, str, int]:
    """Parse a log line and extract relevant fields."""
    _, rest_of_fields = fields.strip().split(" ", 1)
    rest_of_fields = rest_of_fields.lstrip().split(" ")
    response_header_size_str = rest_of_fields[0]
    client_ip = rest_of_fields[1]
    response_size_str = rest_of_fields[3]

    response_header_size = int(response_header_size_str) if response_header_size_str.isdigit() else 0
    response_size = int(response_size_str) if response_size_str.isdigit() else 0
    return response_header_size, client_ip, response_size
