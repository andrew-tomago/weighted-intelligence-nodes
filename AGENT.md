# AGENT.md

Reusable evaluator instructions for running a First Round committee review against any new project idea in this repo.

## Purpose

Use this workflow when the user wants a project concept evaluated by the First Round judge personas in `config/comittee/First Round/`.

## Inputs Required From User

Collect or infer these before running:

- `project_name`: short name.
- `idea_summary`: 2-6 sentence description of what it does.
- `problem_and_user`: who it is for and what pain it solves.
- `stage`: concept, prototype, or live product.
- `evidence`: optional links, metrics, screenshots, or docs.
- `ask`: what decision is needed (for example: go/no-go, pitch readiness, top risks).

If data is missing, proceed with explicit assumptions and mark confidence lower.

## Source of Truth for Judges

- Primary index: `config/comittee/README.md`
- Judge profiles: `config/comittee/First Round/*.md`

Use every `.md` file in `First Round` that exists on disk, even if the README list is stale.

## Execution Workflow

1. Load all First Round profile markdown files.
2. Spawn one subagent per judge profile.
3. If concurrent-agent cap is reached, run in batches until all judges are processed.
4. Give each subagent:
   - Full judge profile markdown.
   - The same project input packet.
   - A fixed response schema (below).
5. Wait for all results and close all spawned subagents.
6. Aggregate results into one committee readout.

## Subagent Prompt Contract

Each subagent must respond with:

- `judge`
- `verdict` (`Advance` | `Borderline` | `Decline`)
- `overall_score` (1-10 integer)
- `strengths` (3-5 bullets)
- `concerns` (3-5 bullets)
- `required_proof` (3-5 bullets)
- `suggested_next_steps` (3-5 bullets)
- `confidence` (`High` | `Medium` | `Low`)

Scoring guidance:

- `8-10`: investment-grade clarity and evidence.
- `5-7`: promising but materially unproven.
- `1-4`: weak differentiation, missing critical proof, or high risk.

## Synthesis Output Format

Return a single markdown report with these sections:

1. `First-Round Outcomes` (one line per judge: verdict + score + key blocker)
2. `Committee Aggregate`
   - verdict distribution
   - average score
   - top 3 strengths themes
   - top 3 risk themes
3. `What Must Be True To Advance` (ranked proof requirements)
4. `Two-Week Build Plan` (5-8 concrete tasks tied to proof requirements)
5. `Open Questions` (blocking unknowns)

## Quality Gates

Before finalizing:

- Confirm every First Round profile produced exactly one result.
- Call out missing/failed judge runs explicitly.
- Keep recommendations evidence-oriented, not generic.
- Separate assumptions from facts.

## Reusability Rule

This workflow is project-agnostic. For each new project:

- Reuse the same process and schema.
- Replace only the project input packet.
- Preserve comparable scoring so results can be benchmarked over time.
