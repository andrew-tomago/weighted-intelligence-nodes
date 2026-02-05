#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

DEFAULT_CONTENT="$ROOT_DIR/data/input/content.json"
LOCAL_CONTENT="$ROOT_DIR/data/input/content.local.json"

CONTENT_FALLBACK="$DEFAULT_CONTENT"
if [[ -f "$LOCAL_CONTENT" ]]; then
  CONTENT_FALLBACK="$LOCAL_CONTENT"
fi

PROFILES="${1:-$ROOT_DIR/data/output/profiles.json}"
CONTENT="${2:-$CONTENT_FALLBACK}"
COMMITTEE="${3:-$ROOT_DIR/config/committee.json}"
OUT="${4:-$ROOT_DIR/data/output/committee_matrix.json}"

python3 "$ROOT_DIR/scripts/mvp_committee.py" evaluate \
  --profiles "$PROFILES" \
  --content "$CONTENT" \
  --committee "$COMMITTEE" \
  --out "$OUT"

printf 'Matrix: %s\n' "$OUT"

