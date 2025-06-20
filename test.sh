#!/bin/bash

set -euo pipefail

curl -v -X POST -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me a short story about a brave knight and a dragon.", "max_new_tokens": 100}' \
  http://localhost:8000/generate
