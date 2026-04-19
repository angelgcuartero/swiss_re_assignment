# Docker related tasks

## How to build the Docker image

Make sure you have Docker installed on your machine: Follow the Docker installation instructions for your OS: <https://docs.astral.sh/uv/getting-started/installation/>

Run the builder script:

```shell
build_tools/build_docker.sh
```

A Docker image will be created and tagged with the name and version included in `pyproject.toml`.

## How to run with Docker

To execute the command-line tool:

```shell
docker run -it -v $(pwd):/app -e LOG_LEVEL=DEBUG swiss-re-assignment:0.1.0 tests/resources tests/output --lfip --mfip --bytes --eps
```
