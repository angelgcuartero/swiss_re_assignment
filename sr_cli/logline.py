"""Module containing the LogLine class, which represents a single log entry with its timestamp and message."""

from sr_cli.utils import is_float


class LogLine:
    """Class representing a single log line with its timestamp and message."""

    def __init__(self, fields: str):
        """Initialize the LogLine object with a timestamp and message."""
        self.timestamp = 0.0
        self.response_header_size = 0
        self.client_ip = ""
        self.http_response_code = 0
        self.response_size = 0
        self.http_request_method = ""
        self.url = ""
        self.username = ""
        self.access_destination_ip = ""
        self.response_type = ""
        self._parse_line(fields)

    def _parse_line(self, fields: str):
        """Parse a log line and extract relevant fields. This is an example of the list of fields.

        Args:
            fields (list[str]): A list of strings representing the fields in a log line.
        """
        # Extract the first field (timestamp) and strip and split the rest
        try:
            self.timestamp, rest_of_fields = fields.strip().split(" ", 1)
            rest_of_fields = rest_of_fields.lstrip().split(" ")
        except ValueError:
            self.timestamp = fields.strip().split(" ", 1)[0]
            rest_of_fields = []

        all_input_fields = [*[self.timestamp], *rest_of_fields]

        campos = [field for field in vars(self).keys()]

        for field_name, field_value in zip(campos, all_input_fields, strict=False):
            setattr(self, field_name, field_value)

        self.timestamp = float(self.timestamp) if is_float(self.timestamp) else 0.0
        self.response_header_size = (
            int(self.response_header_size)
            if isinstance(self.response_header_size, str) and self.response_header_size.isdigit()
            else 0
        )
        self.response_size = int(self.response_size) if isinstance(self.response_size, str) and self.response_size.isdigit() else 0


if __name__ == "__main__":
    ...
