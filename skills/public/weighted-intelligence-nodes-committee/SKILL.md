---
name: weighted-intelligence-nodes-committee
description: Validate ideas with a weighted-intelligence-nodes expert panel.
---

# Weighted Intelligence Nodes Committee

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
cd /Users/tomago/andrew-tomago/public/weighted-intelligence-nodes
cp data/input/targets.json data/input/targets.local.json
cp data/input/content.json data/input/content.local.json
python3 scripts/mvp_committee.py run \
  --targets data/input/targets.local.json \
  --content data/input/content.local.json \
  --committee config/committee.json \
  --outdir data/output
```

Use the Laura evidence-rich example as input:

```bash
cd /Users/tomago/andrew-tomago/public/weighted-intelligence-nodes
cp examples/targets.laura-modiano.example.json data/input/targets.local.json
```

Run staged pipeline:

```bash
cd /Users/tomago/andrew-tomago/public/weighted-intelligence-nodes
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
- Never infer private or sensitive attributes.
- Keep analysis focused on content quality and audience-fit signals.
- Stick to observable public work and stated preferences only.
- Keep user-specific input in `data/input/*.local.json` (gitignored).

## References

- `references/workflow.md`
- `references/data-contracts.md`
- `scripts/run_committee.sh`
