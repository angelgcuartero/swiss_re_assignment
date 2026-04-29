"""Main entry point for the swiss-re-assignment."""

import logging
import os
from pathlib import Path
from typing import Annotated

import typer

from sr_cli.input import get_file_list
from sr_cli.logstatistic import LogStatistics
from sr_cli.process import process_data_file

# Set up logging configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def process(
    input: Annotated[
        Path,
        typer.Argument(
            help="Path to the input file/s",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    output: Annotated[
        Path,
        typer.Argument(
            help="Path to the output file/s", exists=True, file_okay=False, dir_okay=True, writable=True, resolve_path=True
        ),
    ],
    mfip: Annotated[bool, typer.Option("--mfip", help="Calculate the most frequent IP")] = False,
    lfip: Annotated[bool, typer.Option("--lfip", help="Calculate the least frequent IP")] = False,
    eps: Annotated[bool, typer.Option("--eps", help="Calculate events per second")] = False,
    bytes: Annotated[bool, typer.Option("--bytes", help="Calculate total bytes exchanged")] = False,
):
    """Do main CLI task for the swiss-re-assignment.

    Args:
        input (Path): Path to the input file/s.
        output (Path): Path to the output file/s.

    Options:
        mfip (bool): Flag to calculate the most frequent IP.
        lfip (bool): Flag to calculate the least frequent IP.
        eps (bool): Flag to calculate events per second.
        bytes (bool): Flag to calculate total bytes exchanged.

    """
    input_files = get_file_list(input)
    options = [mfip, lfip, eps, bytes]

    if not any(options):
        log.error("No options provided. Please specify at least one option to calculate.")
        raise typer.Exit(code=1)

    for file in input_files:
        log.info(f"Processing file: {file}")
        stats: LogStatistics = process_data_file(file, output)

        if mfip:
            log.info(f"Most frequent IP: {stats.mfip}")
        if lfip:
            log.info(f"Least frequent IP: {stats.lfip}")
        if eps:
            log.info(f"Events per second: {stats.eps}")
        if bytes:
            log.info(f"Total bytes processed: {stats.bytes}")


if __name__ == "__main__":
    app()
