# Swiss Re Assignment

[![Package tests](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/python-pull-request.yml/badge.svg)](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/python-pull-request.yml) [![Snyk Security Scan](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/snyk-checks.yml/badge.svg)](https://github.com/angelgcuartero/swiss_re_assignment/actions/workflows/snyk-checks.yml)

Coding assignment for Swiss Re recruitment process. The requirements can be checked in [this document](./docs/coding-assignment-2023-06-02.md)

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

### Package creation

The Python package for this project can be created with this script:

```shell
build_tools/build_package.sh
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

- Tests are written in pytest-style in the `tests` folder.
- Unit tests are isolated from external state.

Run the tests with:

```shell
tests/run_tests.sh
```

More info about the tests can be found [in the documentation folder](./docs/testing.md).

## Configuration

The project is managed with `uv` and keeps the configuration in `pyproject.toml`. This document includes:

- The project dependencies.
- A development group that includes ruff for formatting purposes.
- A testing group that includes Pytest related packages.
- Formatting parameters.

## Formatting the code and checking the docstrings

The code can be formatted with `ruff`. The same tool can be used to check if some docstring is missing or ill-formatted. Information about how to do this tasks in the [code formatting document](./docs/code_formatting.md).

## Docker tasks

The tasks related to Docker, such as building the image, checking vulnerabilities and running the container, are documented [in a separate document](./docs/docker.md).

## Some considerations processing the data

- In the test data there is a line (82948) that contains 2 events together. The first line does not have all the fields and the next line is pasted with no `\n` separator. The parsing will read the missing fields of the first line as the first fields in the second line and will discard the rest of fields.
- If theres is a mismatch between the expected and read fields, the parsing stops in this cases:
  - The number of read fields is shorter than 10 (expected number of fields). The parser will provide default values for the missing fields.
  - The number of read fields is longer than 10 (expected number of fields). The parser returns just the expected number and the rest is discarded.
- The stattistics are show per file. If there are more than one file, each file processed will show its statistics for the flags reported when invoked.
- The stattistics are printed with the `log.info` function.
- At first, I considered using Pandas or Polars, but I quickly came to two conclusions:
  - They are very slow at loading files.
  - The use case involves processing large files, and we don't want to overload the memory, so it's better to read them line by line.
- The [project for this assignment](https://github.com/users/angelgcuartero/projects/2) uses a Kanban board to track the tickets and related tasks. I created tickets roughly for all the tasks, a branch and pull requests for each functionality.
