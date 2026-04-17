"""Useful utility functions for the swiss-re-assignment CLI."""

import json
from collections import Counter
from pathlib import Path


def is_float(value: str) -> bool:
    """Check if the provided string can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_output_file_name(input_file: Path, output_path: Path) -> Path:
    """Generate an output file name based on the input file name."""
    output_file: Path = output_path / f"{input_file.stem}.json"
    return output_file


def get_formatted_line(parsed_line: dict) -> str:
    """Format the parsed line for output in JSON."""
    return json.dumps(parsed_line)


def calculate_stats(num_lines: int, ip_counter: Counter, total_time: float, total_bytes: int) -> dict[str, int | str | float]:
    """Calculate statistics based on the processed log data.

    Args:
        num_lines (int): The total number of lines processed.
        ip_counter (Counter): A Counter object containing the frequency of each client IP.
        total_time (float): The total time taken to process the log file.
        total_bytes (int): The total number of bytes processed.

    Returns:
        dict[str, int | str | float]: A dictionary containing the calculated statistics.
    """
    if ip_counter:
        mfip = ip_counter.most_common(1)[0][0]
        lfip = ip_counter.most_common()[-1][0]
    else:
        mfip = ""
        lfip = ""

    # Calculate events per second
    eps = num_lines / total_time if total_time > 0 else None  # Avoid division by zero

    return {
        "num_lines": num_lines,
        "mfip": mfip,
        "lfip": lfip,
        "eps": eps,
        "bytes": total_bytes,
    }


if __name__ == "__main__":
    ...
