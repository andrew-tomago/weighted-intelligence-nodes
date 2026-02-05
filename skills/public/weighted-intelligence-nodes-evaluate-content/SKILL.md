---
name: weighted-intelligence-nodes-evaluate-content
description: Score content variants against weighted-intelligence-nodes committee personas. Use when users ask to run committee evaluation, compare draft messages, tune rubric weights or expert focus keywords, or generate committee_matrix.json from existing profiles.
---

# Weighted Intelligence Nodes Evaluate Content

## Overview

Run only the committee scoring stage to produce `data/output/committee_matrix.json`.

## Workflow

1. Ensure `profiles.json` already exists (run profile stage first if needed).
2. Validate content and committee input contracts.
3. Run committee evaluation and inspect weighted scores plus consensus spread.

## Command

```bash
scripts/run_evaluate.sh
```

## Input Contracts

Expected schemas are documented in:
- `../weighted-intelligence-nodes-committee/references/data-contracts.md`

## Guardrails

- Keep scoring criteria explicit through `rubric_weights`.
- Avoid overfitting to one persona by checking expert weights and consensus spread.
- Keep user-specific drafts in `*.local.json` files.
