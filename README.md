<!--
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# weighted-intelligence-nodes

Run a deterministic audience committee over draft content.
The pipeline profiles targets, scores drafts with weighted experts, then writes a summary.

No external dependencies. Python 3 stdlib only.

## Quick Start

```bash
cd /path/to/weighted-intelligence-nodes
cp data/input/targets.json data/input/targets.local.json
cp data/input/content.json data/input/content.local.json
bash skills/public/win-committee/scripts/run_committee.sh
cat data/output/summary.md
```

`run_committee.sh` fallback behavior:

- If `data/input/targets.local.json` exists, it is used; otherwise `data/input/targets.json`.
- If `data/input/content.local.json` exists, it is used; otherwise `data/input/content.json`.

## Commands

| Goal | Command | Output |
| --- | --- | --- |
| Full pipeline | `bash skills/public/win-committee/scripts/run_committee.sh` | `data/output/profiles.json`, `data/output/committee_matrix.json`, `data/output/summary.md` |
| Profile only | `bash skills/public/win-profile/scripts/run_profile.sh` | `data/output/profiles.json` |
| Evaluate only | `bash skills/public/win-evaluate/scripts/run_evaluate.sh` | `data/output/committee_matrix.json` |
| Synthesize only | `bash skills/public/win-summary/scripts/run_synthesize.sh` | `data/output/summary.md` |

Pass custom paths to the full wrapper:

```bash
bash skills/public/win-committee/scripts/run_committee.sh \
  data/input/targets.local.json \
  data/input/content.local.json \
  config/committee.json \
  data/output
```

## Input Files

| File | Required keys |
| --- | --- |
| `data/input/targets.json` | `targets[].id`, `targets[].public_data` |
| `data/input/content.json` | `content[].id`, `content[].title`, `content[].body` |
| `config/committee.json` | `experts[].id`, `experts[].weight`, `rubric_weights` |

Full schema examples live in `skills/public/win-committee/references/data-contracts.md`.

Real user data should live in `*.local.json` files only. These are gitignored.

Use the evidence-rich Laura example:

```bash
cp examples/targets.laura-modiano.example.json data/input/targets.local.json
```

## How It Works

Read [How It Works (Cited)](docs/2026-02-05_how-it-works.md) for stage flow, scoring logic, and source citations.
Read [Primitive Skills Plan](docs/2026-02-05_primitive-skills-plan.md) for roadmap and missing primitives.

## Safety

- Use only public or user-provided data.
- Never infer private or sensitive attributes.
- Keep outputs focused on content fit, message clarity, and evidence quality.
- Keep real audience data in `data/input/*.local.json` only.

## License

MIT. See `LICENSE`.
