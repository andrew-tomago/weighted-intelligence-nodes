<!--
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# Weighted Intelligence Nodes Primitive Skills Plan

Last Updated: 2026-02-05
Version: 0.2.0

## Direct Answer

Yes, these capabilities are composable into larger workflows if each skill is a strict state transition with typed input/output artifacts.

You are missing one critical primitive for MECE design:

- `resolve-identity`: prevents profile contamination when input is only a name or partial handle.

You should also add one quality gate primitive:

- `validate-artifacts`: schema + citation checks before downstream steps run.

## MECE Primitive Skill Set

| Skill | Owns | Input | Output | Does Not Own |
| --- | --- | --- | --- | --- |
| `resolve-identity` | Canonical person resolution | `name` + optional `email`, `linkedin`, `website`, `socials[]` | `data/identity/<person_id>.json` | Profiling, opinion synthesis |
| `harvest-public-evidence` | Public evidence collection + normalization | `person_id` + identity file | `data/evidence/<person_id>.json` | Persona inference decisions |
| `write-profile-md` | Profile generation from evidence | Evidence file | `data/profiles/<person_id>.md` + profile index row | Committee logic |
| `refresh-profile-md` | Profile updates and drift control | Existing profile + refresh mode (`expand` or `prune`) | Updated profile + changelog entry | Committee scoring |
| `compose-committee` | Expert set construction from profile corpus | `profile_ids[]` + objective | `data/committees/<committee_id>.json` | Running evaluations |
| `query-committee` | Per-expert evaluation pass | Committee spec + query payload | `data/opinions/<run_id>.json` | Report synthesis |
| `synthesize-report` | Balanced aggregate report | Opinions file + synthesis rubric | `data/reports/<run_id>.md` | Profile maintenance |
| `validate-artifacts` | Contract and quality gates | Any artifact path | `pass/fail` + error list | Business logic generation |

## Artifact Contracts (MVP)

| Artifact | Required Fields |
| --- | --- |
| `identity.json` | `person_id`, `canonical_name`, `match_confidence`, `disambiguation_notes`, `input_fingerprint` |
| `evidence.json` | `person_id`, `sources[]`, `facts[]`, `collected_at` |
| `profile.md` frontmatter | `person_id`, `canonical_name`, `profile_version`, `freshness_date`, `confidence`, `tags[]` |
| `committee.json` | `committee_id`, `objective`, `experts[]`, `rubric_weights` |
| `opinions.json` | `run_id`, `committee_id`, `query`, `expert_opinions[]` |
| `report.md` | `verdict`, `consensus`, `disagreements`, `expert_breakdown`, `priority_actions` |

## Indexed Profile Format

Store profiles as Markdown in `data/profiles/`, with index at `data/profiles/index.json`.

| File | Purpose |
| --- | --- |
| `data/profiles/<person_id>.md` | Human-readable profile record and evidence summary |
| `data/profiles/index.json` | Fast lookup by `person_id`, name aliases, tags, freshness |
| `data/profiles/changelog.jsonl` | Append-only update history for refresh events |

## Composition Patterns

### 1) New Person Intake

1. `resolve-identity`
2. `harvest-public-evidence`
3. `write-profile-md`
4. `validate-artifacts` on profile + index

### 2) Refresh Existing Profile

1. `resolve-identity` (re-verify)
2. `harvest-public-evidence`
3. `refresh-profile-md` with mode:
   - `expand`: keep old facts, add new
   - `prune`: remove stale/low-confidence facts
4. `validate-artifacts`

### 3) Committee Run

1. `compose-committee`
2. `query-committee`
3. `synthesize-report`
4. `validate-artifacts` on final report

## Committee Query and Synthesis Design

### Per-Expert Opinion Schema (MVP)

| Field | Type | Notes |
| --- | --- | --- |
| `expert_id` | string | Stable expert reference |
| `stance` | enum | `approve`, `revise`, `reject` |
| `scores` | object | `{fit, clarity, novelty, trust}` 0-100 |
| `strengths[]` | string[] | Max 3 |
| `concerns[]` | string[] | Max 3 |
| `edits[]` | string[] | Concrete edits only |
| `confidence` | number | 0-1 |

### Final Report Sections (MVP)

| Section | Requirement |
| --- | --- |
| `Overall Verdict` | One-line ship decision |
| `Consensus` | Items raised by >=50% of experts |
| `Disagreements` | High-variance or conflicting expert calls |
| `Expert Breakdown` | One row per expert with stance + top rationale |
| `Priority Actions` | Top 3 edits ranked by impact x agreement x confidence |

## Why This Is Composable

| Property | Mechanism |
| --- | --- |
| Loose coupling | Each skill reads/writes files, not in-memory hidden state |
| Reusability | Same profile artifacts feed multiple committees |
| Replaceability | You can swap one primitive implementation without rewriting others |
| Scale path | Batch each stage independently (`profiles`, then `committees`, then `reports`) |

## MVP Build Order (Hackathon)

| Priority | Deliverable | Exit Criteria |
| --- | --- | --- |
| P0 | `resolve-identity`, `write-profile-md`, `compose-committee`, `query-committee`, `synthesize-report` | End-to-end run works on 3 people x 3 experts |
| P0 | `validate-artifacts` | Pipeline fails fast on malformed files |
| P1 | `harvest-public-evidence` enrichment quality | Better source coverage + fewer ambiguous matches |
| P1 | `refresh-profile-md` prune mode | Drift cleanup works without manual edits |
| P2 | Multi-committee routing | Different committee templates by audience segment |

## Minimal Skill Packaging Recommendation

Publish as:

- One umbrella skill: `weighted-intelligence-nodes-orchestrator` (runs workflows)
- Eight primitive skills listed above (callable independently)

This gives both speed (single command) and composability (skill chaining).
