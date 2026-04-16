"""Main entry point for the swiss-re-assignment."""

import logging
import os
from pathlib import Path
from typing import Annotated, List

import typer

from sr_cli.output import generate_output_file
from sr_cli.process import process_log_files

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
    # Pass the flags as keyword arguments to the processing function
    kwargs = {
        "calculate_mfip": mfip,
        "calculate_lfip": lfip,
        "calculate_eps": eps,
        "calculate_bytes": bytes,
    }
    res_num_lines, res_mfip, res_lfip, res_eps, res_bytes = process_log_files(input, output, **kwargs)
    generate_output_file(output, res_num_lines, res_mfip, res_lfip, res_eps, res_bytes)


if __name__ == "__main__":
    app()
