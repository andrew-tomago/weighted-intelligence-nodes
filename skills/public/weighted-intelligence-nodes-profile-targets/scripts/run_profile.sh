#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

DEFAULT_TARGETS="$ROOT_DIR/data/input/targets.json"
LOCAL_TARGETS="$ROOT_DIR/data/input/targets.local.json"

TARGETS_FALLBACK="$DEFAULT_TARGETS"
if [[ -f "$LOCAL_TARGETS" ]]; then
  TARGETS_FALLBACK="$LOCAL_TARGETS"
fi

TARGETS="${1:-$TARGETS_FALLBACK}"
OUT="${2:-$ROOT_DIR/data/output/profiles.json}"

python3 "$ROOT_DIR/scripts/mvp_committee.py" profile \
  --targets "$TARGETS" \
  --out "$OUT"

printf 'Profiles: %s\n' "$OUT"

