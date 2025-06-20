#!/bin/bash

set -euo pipefail

uv sync
source .venv/bin/activate
serve run main:model
