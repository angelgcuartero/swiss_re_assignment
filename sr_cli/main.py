"""Main entry point for the swiss-re-assignment."""

import logging
import os
from pathlib import Path
from typing import Annotated, List

import typer
from .process_log import process_log_files

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__ )
app = typer.Typer()


@app.command()
def process(
    input: Annotated[List[Path], typer.Argument(help="List of paths to the input log files")],
    output: Annotated[Path, typer.Argument(help="Path to the output file")],
    mfip: Annotated[bool, typer.Option("--mfip", help="Calculate the most frequent IP")] = False,
    lfip: Annotated[bool, typer.Option("--lfip", help="Calculate the least frequent IP")] = False,
    eps: Annotated[bool, typer.Option("--eps", help="Calculate events per second")] = False,
    bytes: Annotated[bool, typer.Option("--bytes", help="Calculate total bytes exchanged")] = False,
):
    """Main entry point for the swiss-re-assignment.

    Args:
        input (List[Path]): List of input log files.
        output (Path): Path to the output file.

    Options:
        mfip (bool): Flag to calculate the most frequent IP.
        lfip (bool): Flag to calculate the least frequent IP.
        eps (bool): Flag to calculate events per second.
        bytes (bool): Flag to calculate total bytes exchanged.
    """

    # log.info("Hello from swiss-re-assignment!")
    # for file in input:
    #     log.debug(f"Input file: {file}")
    # log.debug(f"Output file: {output}")
    # log.debug(f"Most frequent IP flag: {mfip}")
    # log.debug(f"Least frequent IP flag: {lfip}")
    # log.debug(f"Events per second flag: {eps}")
    # log.debug(f"Total bytes exchanged flag: {bytes}")

    kwargs = {
        "calculate_mfip": mfip,
        "calculate_lfip": lfip,
        "calculate_eps": eps,
        "calculate_bytes": bytes,
    }
    process_log_files(input, output, **kwargs)


if __name__ == "__main__":
    app()
