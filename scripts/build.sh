#!/bin/bash
# Build script that updates manifest before building
#
# Usage: ./scripts/build.sh
#
# Requires AECH_LLM_WORKER_MODEL env var for manifest generation

set -e

cd "$(dirname "$0")/.."

echo "==> Updating manifest.json from source code..."
uv run python scripts/update_manifest.py

echo "==> Building wheel..."
uv build

echo "==> Done!"
