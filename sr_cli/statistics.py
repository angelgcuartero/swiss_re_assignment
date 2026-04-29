"""Module for handling line statistics."""

import time
from collections import Counter


class Statistics:
    """Class to calculate and store statistics for processed log data."""

    def __init__(self):
        """Initialize the Statistics object with default values."""
        self.num_lines = 0
        self.ip_counter = Counter()
        self.start_time = time.perf_counter()  # Start the timer when the Statistics object is created
        self.total_bytes = 0
        self.end_time = self.start_time  # Initialize end_time to start_time to avoid issues if update is never called

    def update(self, ip: str, bytes: int):
        """Update statistics with data from a processed line.

        Args:
            ip (str): The client IP address from the log line.
            bytes (int): The response size in bytes from the log line.
        """
        self.num_lines += 1
        self.ip_counter[ip] += 1
        self.total_bytes += bytes
        self.end_time = time.perf_counter()

    def calculate_stats(self) -> dict[str, int | str | float]:
        """Calculate and return the final statistics.

        Returns:
            dict[str, int | str | float]: A dictionary containing the calculated statistics.
        """
        # Calculate the total processing time
        self.total_time = self.end_time - self.start_time

        if self.ip_counter:
            mfip = self.ip_counter.most_common(1)[0][0]
            lfip = self.ip_counter.most_common()[-1][0]
        else:
            mfip = ""
            lfip = ""

        # Calculate events per second
        eps = self.num_lines / self.total_time if self.total_time > 0 else None  # Avoid division by zero

        return {
            "mfip": mfip,
            "lfip": lfip,
            "eps": eps,
            "bytes": self.total_bytes,
        }


if __name__ == "__main__":
    ...
