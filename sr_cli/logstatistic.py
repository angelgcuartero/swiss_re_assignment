"""LogStatistics class to track statistics about log lines, such as the number of lines, most frequent IP, least frequent IP, and events per second (EPS)."""

import time
from collections import Counter


class LogStatistics:
    """Class to calculate and store statistics for processed log data."""

    def __init__(self):
        """Initialize the LogStatistics object with default values."""
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

    @property
    def mfip(self):
        """Most Frequent IP (MFIP) property."""
        if self.ip_counter:
            return self.ip_counter.most_common(1)[0][0]
        return ""

    @property
    def lfip(self):
        """Least Frequent IP (LFIP) property."""
        if self.ip_counter:
            return self.ip_counter.most_common()[-1][0]
        return ""

    @property
    def eps(self):
        """Events Per Second (EPS) property."""
        total_time = self.end_time - self.start_time
        return self.num_lines / total_time if total_time > 0 else None  # Avoid division by zero

    @property
    def bytes(self):
        """Total bytes property."""
        return self.total_bytes

    def to_dict(self) -> dict[str, int | str | float]:
        """Return the calculated statistics as a dictionary."""
        return {
            "mfip": self.mfip,
            "lfip": self.lfip,
            "eps": self.eps,
            "bytes": self.bytes,
        }


if __name__ == "__main__":
    ...
