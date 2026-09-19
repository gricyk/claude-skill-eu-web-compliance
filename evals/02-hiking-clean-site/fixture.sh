#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
EX="$SRC/../../examples"
mkdir -p examples
cp -R "$EX/hiking-club-site" examples/hiking-club-site
