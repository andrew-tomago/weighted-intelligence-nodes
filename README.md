<!--
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# weighted-intelligence-nodes

MVP scaffold for an audience "committee" pipeline inspired by mixture-of-experts. It profiles targets from public signals, runs multiple persona evaluators against draft content, then synthesizes balanced feedback.

## MVP Scope

| Layer | Included now | Deferred |
| --- | --- | --- |
| Data ingestion | JSON inputs for public target signals and content drafts | Automated web search connectors |
| Profiling | Lightweight token-based profile extraction | LLM-driven psychographic inference |
| Committee | Multi-expert scoring with weights and rubric | Dynamic routing and expert selection |
| Synthesis | Weighted summary + consensus diagnostics | Citation-level explainability graph |

## Repository Layout

| Path | Purpose |
| --- | --- |
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/scripts/mvp_committee.py` | CLI pipeline (`profile`, `evaluate`, `synthesize`, `run`) |
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/config/committee.json` | Committee persona + rubric config |
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/data/input/targets.json` | Sample public target profiles (template) |
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/data/input/content.json` | Sample content drafts (template) |
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/examples/targets.laura-modiano.example.json` | Evidence-rich profile example (Laura Modiano) |
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/skills/public/` | Codex skill packages (`win-*`) |
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/docs/` | MVP spec + publish instructions |

## Quick Start

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

Outputs:

- `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/data/output/profiles.json`
- `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/data/output/committee_matrix.json`
- `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/data/output/summary.md`

Use the Laura evidence example:

```bash
cd /Users/tomago/andrew-tomago/public/weighted-intelligence-nodes
cp examples/targets.laura-modiano.example.json data/input/targets.local.json
```

## Codex Skills

Available skill packages (from `skills/public/*/SKILL.md`):

| Skill ID | Display Name | Scope | Wrapper Command |
| --- | --- | --- | --- |
| `win-committee` | WIN Committee | End-to-end (`profile` + `evaluate` + `synthesize`) | `bash skills/public/win-committee/scripts/run_committee.sh` |
| `win-profile` | WIN Profile | Profile stage (`profiles.json`) | `bash skills/public/win-profile/scripts/run_profile.sh` |
| `win-evaluate` | WIN Evaluate | Evaluate stage (`committee_matrix.json`) | `bash skills/public/win-evaluate/scripts/run_evaluate.sh` |
| `win-summary` | WIN Summary | Synthesis stage (`summary.md`) | `bash skills/public/win-summary/scripts/run_synthesize.sh` |

## Primitive Plan Status (Yet To Be Implemented)

Reference plan: `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/docs/2026-02-05_primitive-skills-plan.md`.

The current repository ships an MVP flow (`profile`, `evaluate`, `synthesize`, `run`) and four `win-*` skills. The following plan primitives are still incomplete:

| Primitive | Status | Current Gap |
| --- | --- | --- |
| `resolve-identity` | Missing | No identity resolution skill or `data/identity/<person_id>.json` artifact. |
| `harvest-public-evidence` | Missing | No evidence harvesting primitive or `data/evidence/<person_id>.json` artifact. |
| `write-profile-md` | Partial | `profile` exists, but outputs JSON (`profiles.json`) instead of `data/profiles/<person_id>.md` + index. |
| `refresh-profile-md` | Missing | No refresh mode (`expand` or `prune`) implementation or changelog updates. |
| `compose-committee` | Partial | Committee is static (`config/committee.json`); no dynamic composition primitive producing `data/committees/<committee_id>.json`. |
| `query-committee` | Partial | `evaluate` exists, but does not emit `data/opinions/<run_id>.json` with the planned schema. |
| `synthesize-report` | Partial | `summary.md` exists, but not the full planned report contract (`verdict`, `consensus`, `disagreements`, `expert_breakdown`, `priority_actions`). |
| `validate-artifacts` | Missing | No dedicated schema/citation quality gate primitive returning pass/fail + errors. |

## Safety Guardrails

- Use only public or user-provided data.
- Never infer private or sensitive attributes.
- Keep outputs focused on content fit, messaging clarity, and evidence quality.
- Stick to observable public work and stated preferences only.
- Put real audience data in `data/input/*.local.json` only. These files are gitignored.

## License

MIT. See `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/LICENSE`.
