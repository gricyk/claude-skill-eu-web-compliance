#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
EX="$SRC/../../examples"
mkdir -p examples
cp -R "$EX/cafe-site" examples/cafe-site
