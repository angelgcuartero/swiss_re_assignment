# Formatting the code and checking the docstrings

## How to format the source code

The configuration for formatting the code follows specified in the [pyproject.toml](../pyproject.toml) file.

To reformat the code just run:

```shell
ruff format
```

## Checking the docstrings

The configuration for the docstring follows the pydocstyle convention [PEP257](https://peps.python.org/pep-0257/). This is configured in the [pyproject.toml](../pyproject.toml) file.

To check the docstrings just run:

```shell
ruff check --select D
```
