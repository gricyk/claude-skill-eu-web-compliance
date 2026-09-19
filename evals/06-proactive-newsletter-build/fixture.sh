#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
EX="$SRC/../../examples"
cp "$SRC/index.html" index.html
