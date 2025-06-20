#!/bin/bash

set -euo pipefail

uv sync
source .venv/bin/activate
exec serve run main:model
