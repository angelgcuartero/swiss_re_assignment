"""Main entry point for the swiss-re-assignment."""

import logging
import os
from pathlib import Path
from typing import Annotated, List

import typer

from sr_cli.output import generate_output_file
from sr_cli.process import read_data_file

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def process(
    input: Annotated[
        List[Path],
        typer.Argument(
            help="List of paths to the input log files",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output: Annotated[Path, typer.Argument(help="Path to the output file")],
    mfip: Annotated[bool, typer.Option("--mfip", help="Calculate the most frequent IP")] = False,
    lfip: Annotated[bool, typer.Option("--lfip", help="Calculate the least frequent IP")] = False,
    eps: Annotated[bool, typer.Option("--eps", help="Calculate events per second")] = False,
    bytes: Annotated[bool, typer.Option("--bytes", help="Calculate total bytes exchanged")] = False,
):
    """Do main CLI task for the swiss-re-assignment.

    Args:
        input (List[Path]): List of input log files.
        output (Path): Path to the output file.

    Options:
        mfip (bool): Flag to calculate the most frequent IP.
        lfip (bool): Flag to calculate the least frequent IP.
        eps (bool): Flag to calculate events per second.
        bytes (bool): Flag to calculate total bytes exchanged.

    """
    input_files = [input] if isinstance(input, str) else input
    response = []

    for file in input_files:
        log.debug(f"Processing file: {file}")
        result_dict = read_data_file(file)
        response.append(result_dict)

    generate_output_file(output, response)


if __name__ == "__main__":
    app()
