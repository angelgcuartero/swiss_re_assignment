#!/usr/bin/env bash

pushd ..
uv run pytest tests --cov=sr_cli --cov-report term
popd || exit
