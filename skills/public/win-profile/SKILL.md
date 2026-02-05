---
name: win-profile
description: Build WIN target profiles from public signals. Use to generate profiles.json, validate target input shape, and extract interests/style before scoring.
---

# WIN Profile

## Overview

Run only the profiling stage to produce `data/output/profiles.json`.

## Workflow

1. Validate target input shape using the `targets.json` contract.
2. Run profiling from `targets.local.json` (or fallback to `targets.json`).
3. Confirm profile count and inspect top interests before evaluation.

## Command

```bash
scripts/run_profile.sh
```

## Input Contract

Expected target schema is documented in:
- `../win-committee/references/data-contracts.md`

## Guardrails

- Use only public or user-provided target signals.
- Do not infer sensitive attributes.
- Keep personalized data in `*.local.json` files.
