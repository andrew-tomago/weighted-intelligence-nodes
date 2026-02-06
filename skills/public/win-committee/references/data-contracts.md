<!--
Created: 2026-02-05
Updated: 2026-02-06
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# Data Contracts

Use `*.local.json` filenames for real user data (for example, `targets.local.json` and `content.local.json`). The repo ignores these files by default.

## `targets.json`

```json
{
  "targets": [
    {
      "id": "string",
      "name": "string",
      "public_data": {
        "bio": "string",
        "posts": ["string"],
        "links": ["string"]
      }
    }
  ]
}
```

## `content.json`

```json
{
  "content": [
    {
      "id": "string",
      "title": "string",
      "body": "string"
    }
  ]
}
```

## `committee.json`

```json
{
  "committee_name": "string",
  "judging_criteria": [
    {
      "id": "string",
      "label": "string",
      "weight": 0.25,
      "mapped_metric": "fit|clarity|novelty|trust",
      "description": "string"
    }
  ],
  "rubric_weights": {
    "fit": 0.45,
    "clarity": 0.2,
    "novelty": 0.2,
    "trust": 0.15
  },
  "experts": [
    {
      "id": "string",
      "persona": "string",
      "focus_keywords": ["string"],
      "weight": 1.0
    }
  ]
}
```

`judging_criteria` is optional. If omitted, criteria are derived from `rubric_weights`.

## Output Files

- `profiles.json`
- `committee_matrix.json`
- `summary.md`

## `committee_matrix.json` Expert Feedback Shape

Each `matrix[].expert_feedback[]` row includes:
- `expert_id`, `persona`, `weight`, `opinion`, `overall`
- `subscores`
- `lens_metric_weights`
- `focus_bonus`, `focus_alignment`
- `criteria_scores`
- `rationale`
- `pros`, `cons`
