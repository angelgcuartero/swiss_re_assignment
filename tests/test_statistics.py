"""Unit tests for the statistics module."""

from collections import Counter

import pytest

from sr_cli.process import parse_line
from sr_cli.statistics import Statistics


def test_calculate_stats_with_data():
    """Test calculate_stats with valid data."""
    lines = [
        "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -",
        "1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html",
        "1157689320.343   1357 10.105.21.199 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -",
    ]

    total_length = sum(len(line) for line in lines)
    stats = Statistics()
    for line in lines:
        parsed_line = parse_line(line)
        stats.update(parsed_line.get("client_ip"), len(str(line)))
    statistics = stats.calculate_stats()

    assert statistics["num_lines"] == 3
    assert statistics["mfip"] == "10.105.21.199"
    assert statistics["lfip"] == "10.105.21.199"
    assert statistics["eps"] == 3 / (stats.end_time - stats.start_time)
    assert statistics["bytes"] == total_length


def test_calculate_stats_empty_counter():
    """Test calculate_stats with an empty IP counter."""
    stats = Statistics()
    stats.num_lines = 0
    stats.ip_counter = Counter()
    result = stats.calculate_stats()

    assert result["num_lines"] == 0
    assert result["mfip"] == ""
    assert result["lfip"] == ""
    assert result["eps"] is None
    assert result["bytes"] == 0


def test_calculate_stats_multiple_ips():
    """Test calculate_stats with multiple IP addresses."""
    lines = [
        "1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -",
        "1157689320.327   2864 10.105.21.1 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html",
        "1157689320.343   1357 10.105.21.1 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -",
        "1157689320.343   1357 10.105.21.10 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -",
        "1157689320.343   1357 10.105.21.10 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -",
        "1157689320.343   1357 10.105.21.10 TCP_REFRESH_HIT/304 214 GET http://www.goonernews.com/styles.css badeyek DIRECT/207.58.145.61 -",
    ]

    total_length = sum(len(line) for line in lines)
    stats = Statistics()
    for line in lines:
        parsed_line = parse_line(line)
        stats.update(parsed_line.get("client_ip"), len(str(line)))
    statistics = stats.calculate_stats()

    assert statistics["num_lines"] == 6
    assert statistics["mfip"] == "10.105.21.10"
    assert statistics["lfip"] == "10.105.21.199"
    assert statistics["eps"] == 6 / (stats.end_time - stats.start_time)
    assert statistics["bytes"] == total_length


def test_calculate_stats_single_ip():
    """Test calculate_stats with a single IP address."""
    lines = ["1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -"]

    total_length = sum(len(line) for line in lines)
    stats = Statistics()
    for line in lines:
        parsed_line = parse_line(line)
        stats.update(parsed_line.get("client_ip"), len(str(line)))
    statistics = stats.calculate_stats()

    assert statistics["num_lines"] == 1
    assert statistics["mfip"] == "10.105.21.199"
    assert statistics["lfip"] == "10.105.21.199"
    assert statistics["eps"] == 1 / (stats.end_time - stats.start_time)
    assert statistics["bytes"] == total_length


if __name__ == "__main__":
    pytest.main()
