FROM python:3.12-alpine

WORKDIR /app

# Copy the project into the image
COPY pyproject.toml README.md /app/
COPY ./sr_cli /app/sr_cli

# Create a non-root user
RUN apk add --no-cache shadow && useradd -m non-root

# Install dependencies
RUN pip install --no-cache-dir .

# Fix permissions for non-root user
RUN chown -R non-root:non-root /app
USER non-root

ENV PYTHONPATH="/app"

# Reset the entrypoint, invoke the module directly
ENTRYPOINT ["python", "-m", "sr_cli.main"]

# Default command - override with: docker run <image> <input> <output>
CMD ["--help"]
