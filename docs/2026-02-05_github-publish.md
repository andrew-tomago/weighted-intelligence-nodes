<!--
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
-->

# GitHub Publish Guide

Last Updated: 2026-02-05
Version: 0.1.0

## Create Public Repo

Option A (`gh` CLI):

```bash
cd /Users/tomago/andrew-tomago/public/custom-moe
git init
git checkout -b codex/mvp-scaffold
git add .
git commit -m "Scaffold custom-moe MVP and Codex skill"
gh repo create weighted-intelligence-nodes --public --source=. --remote=origin --push
```

Option B (manual remote):

```bash
cd /Users/tomago/andrew-tomago/public/custom-moe
git init
git checkout -b codex/mvp-scaffold
git add .
git commit -m "Scaffold custom-moe MVP and Codex skill"
git remote add origin git@github.com:<your-user>/weighted-intelligence-nodes.git
git push -u origin codex/mvp-scaffold
```

## Publish Skill Spec

The public skill spec path in this repo:

- `/Users/tomago/andrew-tomago/public/custom-moe/skills/public/custom-moe-committee/SKILL.md`

Share this direct URL once pushed:

- `https://github.com/<your-user>/weighted-intelligence-nodes/blob/codex/mvp-scaffold/skills/public/custom-moe-committee/SKILL.md`

## Hackathon Demo Sequence

```bash
cd /Users/tomago/andrew-tomago/public/custom-moe
cp data/input/targets.json data/input/targets.local.json
cp data/input/content.json data/input/content.local.json
python3 scripts/mvp_committee.py run \
  --targets data/input/targets.local.json \
  --content data/input/content.local.json \
  --committee config/committee.json \
  --outdir data/output
cat data/output/summary.md
```

## Optional Fast Follow

- Add `data/input/targets_live.json` generated from web-search snapshots.
- Add a one-command shell wrapper for judges.
