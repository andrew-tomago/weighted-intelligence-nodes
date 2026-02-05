<!--
Created: 2026-02-05
Updated: 2026-02-05
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

## Output Files

- `profiles.json`
- `committee_matrix.json`
- `summary.md`
