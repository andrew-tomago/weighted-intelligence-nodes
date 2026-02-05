#!/usr/bin/env bash
# Created: 2026-02-05
# Updated: 2026-02-05
# Created_by:
#   Github Username: andrew-tomago
#   Agent: Codex
#   Model: gpt-5

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

DEFAULT_TARGETS="$ROOT_DIR/data/input/targets.json"
DEFAULT_CONTENT="$ROOT_DIR/data/input/content.json"
LOCAL_TARGETS="$ROOT_DIR/data/input/targets.local.json"
LOCAL_CONTENT="$ROOT_DIR/data/input/content.local.json"

TARGETS_FALLBACK="$DEFAULT_TARGETS"
CONTENT_FALLBACK="$DEFAULT_CONTENT"
if [[ -f "$LOCAL_TARGETS" ]]; then
  TARGETS_FALLBACK="$LOCAL_TARGETS"
fi
if [[ -f "$LOCAL_CONTENT" ]]; then
  CONTENT_FALLBACK="$LOCAL_CONTENT"
fi

TARGETS="${1:-$TARGETS_FALLBACK}"
CONTENT="${2:-$CONTENT_FALLBACK}"
COMMITTEE="${3:-$ROOT_DIR/config/committee.json}"
OUTDIR="${4:-$ROOT_DIR/data/output}"

python3 "$ROOT_DIR/scripts/mvp_committee.py" run \
  --targets "$TARGETS" \
  --content "$CONTENT" \
  --committee "$COMMITTEE" \
  --outdir "$OUTDIR"

printf 'Summary: %s\n' "$OUTDIR/summary.md"
