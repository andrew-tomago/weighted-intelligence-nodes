<!--
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# Workflow Reference

## Decision Tree

| Condition | Action |
| --- | --- |
| Inputs missing required fields | Fix data contracts first |
| Profiles generated but scores look noisy | Tune `focus_keywords` and `rubric_weights` |
| Expert disagreement is high | Split content by audience segment and re-run |
| Most rows are `Pass` | Rewrite content hooks and add proof points |

## Fast Iteration Loop

1. Edit `data/input/content.json` with 2-5 variants.
2. Run full pipeline.
3. Use `summary.md` to pick top candidate.
4. Apply edits and re-run until score and consensus improve.

## Scale-Up Pattern

- Keep one committee template per vertical.
- Maintain a small target profile bank for each market.
- Batch-run candidates and rank by weighted score.
