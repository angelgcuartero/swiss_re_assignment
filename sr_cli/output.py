"""Output file generation for the swiss-re-assignment."""

# Set up logging configuration
import json
import logging
import os

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)


def generate_output_file(
    output: str,
    process_response: list[dict[str, int | str | float]],
    format: str = "JSON",
) -> None:
    """Generate the output file based on the processed data.

    Args:
        output (str): The path to the output file.
        process_response (list[dict[str, int | str | float]]): The list of processed response dictionaries to be written to the output file.
        format (str): The format of the output file (default is "JSON"). Supported formats are "JSON" and "YAML".

    """
    # If one element just dump the dict, otherwise dump the list of dicts
    match format:
        case "JSON":
            log.debug(f"Generating JSON output file: {output}")
            to_dump = simplify_output(process_response)
            json.dump(to_dump, open(output, mode="w"), indent=4)
        case _:
            log.debug(f"Unsupported format '{format}' specified. Defaulting to JSON.")
            dump_content_str = "This is an unformatted string for the output content."
            with open(output, mode="w") as file:
                file.write(dump_content_str)


def simplify_output(process_response) -> dict | list[dict]:
    """Simplify the output by checking if the list contains only one element, return this element.

    Args:
        process_response (list[dict[str, int | str | float]]): The list of processed response dictionaries.

    Returns:
        dict[str, int | str | float] | list[dict[str, int | str | float]]: The simplified output.

    """
    to_dump = process_response[0] if len(process_response) == 1 else process_response
    return to_dump
