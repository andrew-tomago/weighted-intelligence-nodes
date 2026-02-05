---
name: weighted-intelligence-nodes-profile-targets
description: Build audience target profiles from public signals in weighted-intelligence-nodes. Use when users ask to profile personas, extract audience interests/style from bios and posts, validate target input structure, or generate profiles.json before committee scoring.
---

# Weighted Intelligence Nodes Profile Targets

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
- `../weighted-intelligence-nodes-committee/references/data-contracts.md`

## Guardrails

- Use only public or user-provided target signals.
- Do not infer sensitive attributes.
- Keep personalized data in `*.local.json` files.
