# Swiss Re Assignment

[![Package tests](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/python-pull-request.yml/badge.svg)](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/python-pull-request.yml) [![Snyk Security Scan](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/snyk-checks.yml/badge.svg)](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/snyk-checks.yml)

Coding assignment for Swiss Re recruitment process. The requirements can be checked at [this document](./docs/coding-assignment-2023-06-02.md)

## Features

- Python 3.12
- CLI powered by Typer
- Testing with Pytest
- Environment, dependency, and test management via uv

## Requirements

- Python 3.12
- uv (for environment & package management)

## Quickstart

### Install uv (if not already installed)

Follow `uv` installation instructions for your OS: <https://docs.astral.sh/uv/getting-started/installation/>

### Recreate the virtual environment and install project dependencies with test tools

```shell
uv sync --group dev --group test
```

### Run the CLI (example)

Executing the command-line tool with the `--help` flag with show the parameters and options the too accepts:

```console
$ uv run swiss-re-assignment --help

 Usage: swiss-re-assignment [OPTIONS] INPUT OUTPUT

 Do main CLI task for the swiss-re-assignment.

 Args:
     input (Path): Path to the input file/s.
     output (Path): Path to the output file/s.

 Options:
     mfip (bool): Flag to calculate the most frequent IP.
     lfip (bool): Flag to calculate the least frequent IP.
     eps (bool): Flag to calculate events per second.
     bytes (bool): Flag to calculate total bytes exchanged.

╭─ Arguments ───────────────────────────────────────────────────────────────────╮
│ *    input       DIRECTORY  Path to the input file/s [required]               │
│ *    output      DIRECTORY  Path to the output file/s [required]              │
╰───────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────╮
│ --mfip                        Calculate the most frequent IP                  │
│ --lfip                        Calculate the least frequent IP                 │
│ --eps                         Calculate events per second                     │
│ --bytes                       Calculate total bytes exchanged                 │
│ --install-completion          Install completion for the current shell.       │
│ --show-completion             Show completion for the current shell, to copy  │
│                               it or customize the installation.               │
│ --help                        Show this message and exit.                     │
╰───────────────────────────────────────────────────────────────────────────────╯
```

This is an example of a typical execution with parameters and options:

```shell
uv run swiss-re-assignment tests/resources tests/output --lfip --mfip --bytes --eps
```

## Testing Guidelines

- Tests are written in pytest-style in the `tests/` folder.
- Unit tests are isolated from external state.

```shell
tests/run_tests.sh 
```

This will run the tests for the module sr_cli and show a coverage report to the console:

```shell
uv run pytest tests --cov=sr_cli --cov-report term
```

## Configuration

The project is managed with `uv` and keeps the configuration in `pyproject.toml`

## Docker tasks

The tasks related to Docker, such as building the image, checking vulnerabilities and running the container are documented [in a separate document](./docs/docker.md).
