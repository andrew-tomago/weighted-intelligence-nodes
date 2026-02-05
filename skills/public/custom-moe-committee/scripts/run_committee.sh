#!/usr/bin/env bash
# Created: 2026-02-05
# Updated: 2026-02-05
# Created_by:
#   Github Username: andrew-tomago
#   Agent: Codex
#   Model: gpt-5

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

TARGETS="${1:-$ROOT_DIR/data/input/targets.json}"
CONTENT="${2:-$ROOT_DIR/data/input/content.json}"
COMMITTEE="${3:-$ROOT_DIR/config/committee.json}"
OUTDIR="${4:-$ROOT_DIR/data/output}"

python3 "$ROOT_DIR/scripts/mvp_committee.py" run \
  --targets "$TARGETS" \
  --content "$CONTENT" \
  --committee "$COMMITTEE" \
  --outdir "$OUTDIR"

printf 'Summary: %s\n' "$OUTDIR/summary.md"
