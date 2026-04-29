"""Process log files and perform calculations based on the provided flags."""

import logging
import os
from pathlib import Path

from sr_cli.input import line_reader
from sr_cli.logline import LogLine
from sr_cli.logstatistic import LogStatistics
from sr_cli.output import get_output_file_name, get_writer_class

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def process_data_file(input_file: Path, output_path: Path) -> LogStatistics:
    """Read the log file and process its contents.

    Args:
        input_file (Path): The path to the log file to be processed.
        output_path (Path): The path to the output file where results will be saved.
    Returns:
        LogStatistics: The updated statistics object.
    """
    output_file = get_output_file_name(input_file, output_path)
    return _process_lines(input_file, output_file)


def _process_lines(input_file: Path, output_file: Path, format="JSON") -> LogStatistics:
    """Process each line of the log file, extract relevant data, and write formatted output to the output file.

    Args:
        input_file (Path): The path to the log file to be processed.
        output_file (Path): The path to the output file where results will be saved.
        format (str): The format for the output file.
    Returns:
        LogStatistics: The updated statistics object.
    """
    stats = LogStatistics()
    for line in line_reader(input_file):
        log_line = LogLine(line)
        stats.update(log_line.client_ip, len(line))
    with open(output_file, mode="w") as output_file_handle:
        writer = get_writer_class(format)(output_file_handle)
        writer.write_line(stats.to_dict())
        writer.finalize()
    return stats


if __name__ == "__main__":
    ...
