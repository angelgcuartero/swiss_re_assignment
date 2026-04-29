FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copy the project into the image
COPY pyproject.toml uv.lock README.md /app/
COPY ./sr_cli /app/sr_cli

# Disable development dependencies
ENV UV_NO_DEV=1

# Create a non-root user before sync
RUN apk add --no-cache shadow && useradd -m non-root

# Sync the project into a venv outside /app so volume mounts don't overwrite it
RUN UV_PROJECT_ENVIRONMENT=/venv uv sync --locked

# Fix permissions for non-root user
RUN chown -R non-root:non-root /app /venv
USER non-root

# Place executables in the environment at the front of the path
ENV PATH="/venv/bin:$PATH" PYTHONPATH="/app"

# Reset the entrypoint, invoke the module directly
ENTRYPOINT ["python", "-m", "sr_cli.main"]

# Default command - override with: docker run <image> <input> <output>
CMD ["--help"]
