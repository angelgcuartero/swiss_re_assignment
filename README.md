# Swiss Re Assignment

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

### Create and activate the project environment with uv

```shell
uv init swiss_re_assignment
. .env/bin/activate
```

### Install project dependencies with test tools

```shell
uv sync --group dev --group test
```

### Run the CLI (example)

```shell
python -m your_package.main [COMMAND] [OPTIONS]
```

## Testing Guidelines

- Tests are written in pytest-style in the `tests/` folder.
- Unit tests are isolated from external state.

```shell
cd tests
./tests/run_tests.sh 
```

## Configuration

- Keep configuration in pyproject.toml

## Build the container

Make sure you have Docker installed on your machine: Follow the Docker installation instructions for your OS: <https://docs.astral.sh/uv/getting-started/installation/>
