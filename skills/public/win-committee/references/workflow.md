<!--
Created: 2026-02-05
Updated: 2026-02-06
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
| Profiles generated but scores look noisy | Tune `focus_keywords`, `rubric_weights`, and `judging_criteria` phrasing |
| Expert disagreement is high | Split content by audience segment and re-run |
| Most rows are `Pass` | Rewrite content hooks and add proof points |

## Fast Iteration Loop

1. Edit `data/input/content.local.json` with 2-5 variants.
2. Ensure `committee.json` criteria labels and descriptions reflect how judges actually think.
3. Run full pipeline.
4. Inspect `committee_matrix.json` for `rationale`, `criteria_scores`, and `focus_alignment`.
5. Use `summary.md` to pick top candidate.
6. Apply edits and re-run until score and consensus improve.

## Scale-Up Pattern

- Keep one committee template per vertical.
- Maintain a small target profile bank for each market.
- Batch-run candidates and rank by weighted score.
