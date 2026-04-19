FROM python:3.14-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copy the project into the image
COPY pyproject.toml uv.lock README.md /app/
COPY ./sr_cli /app/sr_cli

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Create a non-root user and switch to it
RUN apk add --no-cache shadow && useradd -m non-root && chown -R non-root:non-root /app
USER non-root

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT ["uv", "run", "swiss-re-assignment"]

# Default command - override with: docker run <image> <input> <output>
CMD ["--help"]
