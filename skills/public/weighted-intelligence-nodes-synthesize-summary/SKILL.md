---
name: weighted-intelligence-nodes-synthesize-summary
description: Convert weighted-intelligence-nodes committee results into a ranked markdown summary. Use when users ask to summarize committee_matrix.json, prioritize rewrite backlog from low-score rows, or produce decision-ready committee output for stakeholders.
---

# Weighted Intelligence Nodes Synthesize Summary

## Overview

Run only the synthesis stage to produce `data/output/summary.md`.

## Workflow

1. Ensure `committee_matrix.json` exists (run evaluation stage first if needed).
2. Generate markdown summary.
3. Use low-score rows as the first rewrite backlog.

## Command

```bash
scripts/run_synthesize.sh
```

## Input Contract

Output columns and artifacts are documented in:
- `../weighted-intelligence-nodes-committee/references/data-contracts.md`
- `../weighted-intelligence-nodes-committee/references/workflow.md`

## Guardrails

- Preserve score, majority opinion, and consensus fields from source matrix.
- Keep summary deterministic and easy to compare across reruns.
