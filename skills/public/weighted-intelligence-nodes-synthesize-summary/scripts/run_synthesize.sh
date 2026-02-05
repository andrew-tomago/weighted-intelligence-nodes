#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

MATRIX="${1:-$ROOT_DIR/data/output/committee_matrix.json}"
OUT="${2:-$ROOT_DIR/data/output/summary.md}"

python3 "$ROOT_DIR/scripts/mvp_committee.py" synthesize \
  --matrix "$MATRIX" \
  --out "$OUT"

printf 'Summary: %s\n' "$OUT"

