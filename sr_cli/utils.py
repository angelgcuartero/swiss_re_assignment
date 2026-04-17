"""Useful utility functions for the swiss-re-assignment CLI."""

import ipaddress


def is_valid_ip(ip: str) -> bool:
    """Validate if the provided string is a valid IP address."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

    # Alternative manual validation (not recommended):
    # parts = ip.split(".")
    # if len(parts) != 4:
    #     return False
    # for part in parts:
    #     if not part.isdigit() or not 0 <= int(part) <= 255:
    #         return False
    # return True


def is_float(value: str) -> bool:
    """Check if the provided string can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False
