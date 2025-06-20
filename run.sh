#!/bin/bash

set -euo pipefail

uv sync
uv run ruff format .
source .venv/bin/activate
exec serve run main:model
