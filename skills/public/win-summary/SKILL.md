---
name: win-summary
description: Summarize WIN committee_matrix.json into ranked markdown feedback. Use to surface consensus, disagreements, and top rewrite actions.
---

# WIN Summary

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
- `../win-committee/references/data-contracts.md`
- `../win-committee/references/workflow.md`

## Guardrails

- Preserve score, majority opinion, and consensus fields from source matrix.
- Keep summary deterministic and easy to compare across reruns.
