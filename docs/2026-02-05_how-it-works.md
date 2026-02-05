<!--
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# How It Works (Cited)

Last Updated: 2026-02-05  
Version: 0.1.0

This document explains the current MVP behavior and cites the exact source files.

## Pipeline Flow

| Stage | What it does | Output | Source |
| --- | --- | --- | --- |
| `profile` | Reads targets, tokenizes public signals, builds top interests and style preference. | `profiles.json` | `scripts/mvp_committee.py:167`, `scripts/mvp_committee.py:146` |
| `evaluate` | Scores each `(target, content, expert)` tuple, then computes weighted synthesis. | `committee_matrix.json` | `scripts/mvp_committee.py:316`, `scripts/mvp_committee.py:189`, `scripts/mvp_committee.py:274` |
| `synthesize` | Writes a markdown summary table from matrix synthesis fields. | `summary.md` | `scripts/mvp_committee.py:363` |
| `run` | Executes `profile -> evaluate -> synthesize` in order. | all three outputs | `scripts/mvp_committee.py:405`, `scripts/mvp_committee.py:478` |

CLI subcommands and required args are defined in `scripts/mvp_committee.py:428`.

## Scoring Model

| Dimension | Rule | Source |
| --- | --- | --- |
| Fit | Keyword overlap between profile interests and content tokens, scaled then clamped to `0-100`. | `scripts/mvp_committee.py:181` |
| Clarity | Penalizes distance from a 16-word average sentence target. | `scripts/mvp_committee.py:124` |
| Novelty | Uses unique-token ratio, scaled then clamped. | `scripts/mvp_committee.py:133` |
| Trust | Uses numeric density plus source-term hits (`study`, `report`, `data`, `evidence`, `benchmark`, `survey`). | `scripts/mvp_committee.py:85`, `scripts/mvp_committee.py:140` |

Overall score = weighted subscore sum + focus bonus (max `+10`) from expert keyword overlap.
Opinion thresholds:

- `Ship`: `overall >= 78`
- `Iterate`: `62 <= overall < 78`
- `Pass`: `overall < 62`

Source: `scripts/mvp_committee.py:210`, `scripts/mvp_committee.py:214`, `scripts/mvp_committee.py:217`.

Consensus labels use score spread (`stddev`):

- `high` if spread `< 7`
- `mixed` if spread `< 14`
- `polarized` otherwise

Source: `scripts/mvp_committee.py:261`.

## Inputs, Defaults, and Wrappers

| Component | Current behavior | Source |
| --- | --- | --- |
| Full wrapper | `run_committee.sh` calls `mvp_committee.py run`. | `skills/public/win-committee/scripts/run_committee.sh:32` |
| Local-file fallback | Prefers `targets.local.json` / `content.local.json`; falls back to templates if missing. | `skills/public/win-committee/scripts/run_committee.sh:13`, `skills/public/win-committee/scripts/run_committee.sh:20` |
| Default committee | Uses `config/committee.json` unless caller passes arg 3. | `skills/public/win-committee/scripts/run_committee.sh:29` |
| Default outputs | Uses `data/output` unless caller passes arg 4. | `skills/public/win-committee/scripts/run_committee.sh:30` |

## Data Contracts and Committee Config

- Canonical input/output contract examples: `skills/public/win-committee/references/data-contracts.md:10`.
- Default rubric weights and expert set: `config/committee.json:2`.

## Current Scope vs Roadmap

This repo ships an MVP with `profile`, `evaluate`, `synthesize`, and `run`.
Planned primitives such as `resolve-identity` and `validate-artifacts` remain open.

Source: `docs/2026-02-05_primitive-skills-plan.md:1`.
