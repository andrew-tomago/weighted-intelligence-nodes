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
| `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/skills/public/weighted-intelligence-nodes-committee` | Codex skill package |
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

## Codex Skill

The skill package lives at:

- `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/skills/public/weighted-intelligence-nodes-committee`

Use it when you want Codex to run this pipeline, tune committee members, or generate evaluation summaries from new datasets.

## Safety Guardrails

- Use only public or user-provided data.
- Do not infer or store protected/sensitive attributes.
- Keep outputs focused on content fit, messaging clarity, and evidence quality.
- Put real audience data in `data/input/*.local.json` only. These files are gitignored.

## License

MIT. See `/Users/tomago/andrew-tomago/public/weighted-intelligence-nodes/LICENSE`.
