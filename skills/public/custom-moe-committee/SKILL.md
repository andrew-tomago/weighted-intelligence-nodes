---
name: custom-moe-committee
description: Build and run an audience-profiling committee workflow that turns public target signals into profiles, evaluates draft content from multiple persona perspectives, and synthesizes a balanced recommendation. Use when users ask to test content against persona panels, tune expert weights/rubrics, scale to more target personas, or produce committee summaries from target/content JSON data.
---

# Custom MoE Committee

## Overview

Use this skill to execute a fast MoE-style audience feedback loop for hackathon or MVP contexts.

## Workflow

1. Validate inputs against the contracts in `references/data-contracts.md`.
2. Run profiling from target public data.
3. Run committee evaluation across experts and content drafts.
4. Synthesize output into a balanced summary with consensus signals.

## Commands

Run full pipeline:

```bash
cd /Users/tomago/andrew-tomago/public/custom-moe
cp data/input/targets.json data/input/targets.local.json
cp data/input/content.json data/input/content.local.json
python3 scripts/mvp_committee.py run \
  --targets data/input/targets.local.json \
  --content data/input/content.local.json \
  --committee config/committee.json \
  --outdir data/output
```

Run staged pipeline:

```bash
cd /Users/tomago/andrew-tomago/public/custom-moe
python3 scripts/mvp_committee.py profile --targets data/input/targets.local.json --out data/output/profiles.json
python3 scripts/mvp_committee.py evaluate --profiles data/output/profiles.json --content data/input/content.local.json --committee config/committee.json --out data/output/committee_matrix.json
python3 scripts/mvp_committee.py synthesize --matrix data/output/committee_matrix.json --out data/output/summary.md
```

## Tuning Rules

- Add or remove committee experts in `config/committee.json`.
- Adjust score emphasis via `rubric_weights`.
- Keep weights normalized enough to avoid one expert dominating output.
- Add domain-specific focus keywords per expert to reflect committee specialization.

## Guardrails

- Use only public or user-provided data.
- Do not infer sensitive attributes.
- Keep analysis focused on content quality and audience-fit signals.
- Keep user-specific input in `data/input/*.local.json` (gitignored).

## References

- `references/workflow.md`
- `references/data-contracts.md`
- `scripts/run_committee.sh`
