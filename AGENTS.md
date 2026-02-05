<!--
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# AGENTS.md

Project-level operating defaults for `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes`.
These rules override broader workspace defaults when they conflict.

## Project Intent

- Keep this repository a deterministic MVP for audience profiling and weighted committee evaluation.
- Optimize for reproducible CLI runs from JSON inputs.
- Prefer transparent heuristics and simple data contracts over hidden complexity.

## Source-of-Truth Files

| Path | Role | Agent Rule |
| --- | --- | --- |
| `scripts/mvp_committee.py` | Pipeline logic (`profile`, `evaluate`, `synthesize`, `run`) | Treat CLI shape and output filenames as stable interface unless migration is requested |
| `config/committee.json` | Expert personas and rubric weights | Keep weights explicit; avoid silent defaults in docs |
| `data/input/*.json` | Input templates and local variants | Real user data lives in `*.local.json` only |
| `skills/public/weighted-intelligence-nodes-committee/SKILL.md` | Public skill entrypoint | Update when workflow or commands change |
| `skills/public/weighted-intelligence-nodes-committee/references/data-contracts.md` | Contract reference | Update immediately after schema changes |
| `docs/2026-02-05_mvp-spec.md` | Product and acceptance criteria | Update when scoring logic or pipeline behavior changes |

## Standard Workflow

1. Validate input JSON against `skills/public/weighted-intelligence-nodes-committee/references/data-contracts.md`.
2. Run full pipeline with local or template inputs.
3. Review `data/output/summary.md` and `data/output/committee_matrix.json` for score/coherence regressions.
4. If behavior changed, sync docs and skill references in the same change.

## Canonical Commands

| Goal | Command |
| --- | --- |
| Full pipeline | `python3 scripts/mvp_committee.py run --targets data/input/targets.local.json --content data/input/content.local.json --committee config/committee.json --outdir data/output` |
| Staged profile | `python3 scripts/mvp_committee.py profile --targets data/input/targets.local.json --out data/output/profiles.json` |
| Staged evaluate | `python3 scripts/mvp_committee.py evaluate --profiles data/output/profiles.json --content data/input/content.local.json --committee config/committee.json --out data/output/committee_matrix.json` |
| Staged synthesize | `python3 scripts/mvp_committee.py synthesize --matrix data/output/committee_matrix.json --out data/output/summary.md` |
| Wrapper script | `skills/public/weighted-intelligence-nodes-committee/scripts/run_committee.sh` |

If local files do not exist, copy templates first:

```bash
cp data/input/targets.json data/input/targets.local.json
cp data/input/content.json data/input/content.local.json
```

## Change Control Rules

- Keep dependencies minimal; prefer Python standard library unless external dependency is explicitly needed.
- Do not hand-edit generated artifacts in `data/output/`; regenerate them.
- Preserve public-data-only boundaries. Do not add sensitive-attribute inference.
- When changing CLI args, schema, scoring, or rubric semantics, update all affected references:
  - `README.md`
  - `docs/2026-02-05_mvp-spec.md`
  - `skills/public/weighted-intelligence-nodes-committee/SKILL.md`
  - `skills/public/weighted-intelligence-nodes-committee/references/data-contracts.md`
  - `skills/public/weighted-intelligence-nodes-committee/references/workflow.md`

## Validation Gate Before Merge

- Run at least one end-to-end command successfully.
- Confirm expected outputs exist:
  - `data/output/profiles.json`
  - `data/output/committee_matrix.json`
  - `data/output/summary.md`
- Ensure docs and skill references match implementation behavior.
