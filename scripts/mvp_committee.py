#!/usr/bin/env python3
"""
Created: 2026-02-05
Updated: 2026-02-05
Created_by:
  Github Username: andrew-tomago
  Agent: Codex
  Model: gpt-5
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "this",
    "that",
    "from",
    "are",
    "you",
    "your",
    "our",
    "their",
    "they",
    "them",
    "was",
    "were",
    "have",
    "has",
    "had",
    "will",
    "can",
    "not",
    "but",
    "about",
    "into",
    "than",
    "then",
    "just",
    "like",
    "also",
    "more",
    "less",
    "very",
    "what",
    "when",
    "where",
    "how",
    "why",
    "who",
    "all",
    "any",
    "out",
    "too",
    "its",
    "it",
    "on",
    "in",
    "at",
    "of",
    "to",
    "a",
    "an",
    "is",
    "as",
    "be",
    "or",
    "if",
    "by",
    "we",
    "i",
}

SOURCE_TERMS = {"study", "report", "data", "evidence", "benchmark", "survey"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def tokenize(text: str) -> list[str]:
    raw = re.findall(r"[a-z0-9']+", text.lower())
    return [t for t in raw if len(t) >= 3 and t not in STOPWORDS]


def collect_text(payload: Any) -> list[str]:
    if payload is None:
        return []
    if isinstance(payload, str):
        return [payload]
    if isinstance(payload, list):
        chunks: list[str] = []
        for item in payload:
            chunks.extend(collect_text(item))
        return chunks
    if isinstance(payload, dict):
        chunks = []
        for value in payload.values():
            chunks.extend(collect_text(value))
        return chunks
    return []


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def score_clarity(text: str) -> float:
    words = re.findall(r"\b\w+\b", text)
    sentence_count = max(1, len(re.findall(r"[.!?]", text)))
    avg_sentence_len = len(words) / sentence_count if words else 0
    target = 16
    penalty = abs(avg_sentence_len - target) * 2.8
    return clamp(95 - penalty)


def score_novelty(tokens: list[str]) -> float:
    if not tokens:
        return 0
    unique_ratio = len(set(tokens)) / len(tokens)
    return clamp(unique_ratio * 120)


def score_trust(text: str, tokens: list[str]) -> float:
    numeric_density = len(re.findall(r"\d", text))
    source_hits = sum(1 for t in tokens if t in SOURCE_TERMS)
    return clamp(35 + (numeric_density * 2.0) + (source_hits * 8.0))


def build_profile(target: dict[str, Any]) -> dict[str, Any]:
    signals = collect_text(target.get("public_data", {}))
    signals.extend(collect_text(target.get("signals", {})))
    tokens = tokenize(" ".join(signals))
    token_counts = Counter(tokens)

    top_interests = [token for token, _ in token_counts.most_common(12)]
    longform_signals = sum(1 for chunk in signals if len(chunk.split()) > 35)
    style = "longform" if longform_signals >= max(1, len(signals) // 3) else "snackable"

    return {
        "id": target["id"],
        "name": target.get("name", target["id"]),
        "interests": top_interests,
        "style_preference": style,
        "signal_count": len(signals),
        "raw_token_count": len(tokens),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def profile_targets(targets_path: Path, out_path: Path) -> dict[str, Any]:
    payload = load_json(targets_path)
    targets = payload.get("targets", [])
    profiles = [build_profile(t) for t in targets]

    result = {
        "source": str(targets_path),
        "profile_count": len(profiles),
        "profiles": profiles,
    }
    dump_json(out_path, result)
    return result


def score_fit(profile: dict[str, Any], content_tokens: list[str]) -> float:
    interests = set(profile.get("interests", []))
    if not interests:
        return 0
    overlap = len(interests.intersection(content_tokens))
    return clamp((overlap / len(interests)) * 125)


def build_expert_feedback(
    profile: dict[str, Any],
    content: dict[str, Any],
    expert: dict[str, Any],
    rubric_weights: dict[str, float],
) -> dict[str, Any]:
    text = f"{content.get('title', '')}\n{content.get('body', '')}"
    content_tokens = tokenize(text)

    fit = score_fit(profile, content_tokens)
    clarity = score_clarity(text)
    novelty = score_novelty(content_tokens)
    trust = score_trust(text, content_tokens)

    subscores = {
        "fit": round(fit, 2),
        "clarity": round(clarity, 2),
        "novelty": round(novelty, 2),
        "trust": round(trust, 2),
    }

    focus_keywords = set(expert.get("focus_keywords", []))
    focus_overlap = len(focus_keywords.intersection(content_tokens)) if focus_keywords else 0
    focus_bonus = min(10, focus_overlap * 3)

    weighted = sum(subscores[k] * rubric_weights.get(k, 0) for k in subscores)
    overall = clamp(weighted + focus_bonus)

    if overall >= 78:
        opinion = "Ship"
    elif overall >= 62:
        opinion = "Iterate"
    else:
        opinion = "Pass"

    pros = []
    if fit >= 65:
        pros.append("strong audience-interest overlap")
    if clarity >= 70:
        pros.append("clear and digestible framing")
    if trust >= 65:
        pros.append("credible signal density")
    if focus_bonus > 0:
        pros.append(f"aligned with {expert['id']} focus")

    cons = []
    if fit < 50:
        cons.append("weak match to audience interests")
    if clarity < 60:
        cons.append("message density hurts clarity")
    if novelty < 55:
        cons.append("angle feels familiar")
    if trust < 55:
        cons.append("insufficient proof points")

    if not pros:
        pros.append("solid baseline structure")
    if not cons:
        cons.append("minor polish on hook and CTA")

    return {
        "expert_id": expert["id"],
        "persona": expert.get("persona", expert["id"]),
        "weight": expert.get("weight", 1.0),
        "opinion": opinion,
        "overall": round(overall, 2),
        "subscores": subscores,
        "pros": pros[:2],
        "cons": cons[:2],
    }


def consensus_label(scores: list[float]) -> tuple[str, float]:
    if not scores:
        return ("unknown", 0.0)
    mean = sum(scores) / len(scores)
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    spread = math.sqrt(variance)
    if spread < 7:
        return ("high", round(spread, 2))
    if spread < 14:
        return ("mixed", round(spread, 2))
    return ("polarized", round(spread, 2))


def synthesize_expert_feedback(expert_feedback: list[dict[str, Any]]) -> dict[str, Any]:
    if not expert_feedback:
        return {
            "weighted_score": 0,
            "consensus": "unknown",
            "spread": 0,
            "majority_opinion": "Pass",
            "top_pro": "no signal",
            "top_con": "no signal",
        }

    weighted_total = 0.0
    weight_sum = 0.0
    opinions = Counter()
    pro_counts = Counter()
    con_counts = Counter()
    scores = []

    for fb in expert_feedback:
        weight = float(fb.get("weight", 1.0))
        score = float(fb.get("overall", 0.0))
        weighted_total += score * weight
        weight_sum += weight
        opinions[fb.get("opinion", "Pass")] += 1
        scores.append(score)
        for pro in fb.get("pros", []):
            pro_counts[pro] += 1
        for con in fb.get("cons", []):
            con_counts[con] += 1

    consensus, spread = consensus_label(scores)

    return {
        "weighted_score": round(weighted_total / max(weight_sum, 1.0), 2),
        "consensus": consensus,
        "spread": spread,
        "majority_opinion": opinions.most_common(1)[0][0],
        "top_pro": pro_counts.most_common(1)[0][0] if pro_counts else "no strong pro",
        "top_con": con_counts.most_common(1)[0][0] if con_counts else "no strong con",
    }


def evaluate_content(
    profiles_path: Path,
    content_path: Path,
    committee_path: Path,
    out_path: Path,
) -> dict[str, Any]:
    profiles_payload = load_json(profiles_path)
    content_payload = load_json(content_path)
    committee_payload = load_json(committee_path)

    profiles = profiles_payload.get("profiles", [])
    content_items = content_payload.get("content", [])
    experts = committee_payload.get("experts", [])
    rubric_weights = committee_payload.get(
        "rubric_weights",
        {"fit": 0.45, "clarity": 0.2, "novelty": 0.2, "trust": 0.15},
    )

    matrix: list[dict[str, Any]] = []
    for profile in profiles:
        for content in content_items:
            feedback = [
                build_expert_feedback(profile, content, expert, rubric_weights)
                for expert in experts
            ]
            synthesis = synthesize_expert_feedback(feedback)
            matrix.append(
                {
                    "target_id": profile["id"],
                    "target_name": profile.get("name", profile["id"]),
                    "content_id": content["id"],
                    "content_title": content.get("title", content["id"]),
                    "expert_feedback": feedback,
                    "synthesis": synthesis,
                }
            )

    result = {
        "committee_name": committee_payload.get("committee_name", "committee"),
        "matrix_count": len(matrix),
        "matrix": matrix,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    dump_json(out_path, result)
    return result


def write_summary_markdown(matrix_payload: dict[str, Any], out_path: Path) -> None:
    rows = matrix_payload.get("matrix", [])
    generated = datetime.now(timezone.utc).isoformat()

    lines = [
        "<!--",
        "Created: 2026-02-05",
        "Updated: 2026-02-05",
        "Created_by:",
        "  Github Username: andrew-tomago",
        "  Agent: Codex",
        "  Model: gpt-5",
        "-->",
        "",
        "# Audience Committee Summary",
        "",
        f"Generated: {generated}",
        f"Committee: {matrix_payload.get('committee_name', 'committee')}",
        "",
        "| Target | Content | Score | Majority | Consensus | Top Pro | Top Con |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]

    for row in rows:
        synth = row.get("synthesis", {})
        lines.append(
            "| "
            f"{row.get('target_name', row.get('target_id', 'n/a'))} | "
            f"{row.get('content_title', row.get('content_id', 'n/a'))} | "
            f"{synth.get('weighted_score', 0)} | "
            f"{synth.get('majority_opinion', 'n/a')} | "
            f"{synth.get('consensus', 'n/a')} | "
            f"{synth.get('top_pro', 'n/a')} | "
            f"{synth.get('top_con', 'n/a')} |"
        )

    lines.extend(["", "## Notes", "", "- Use low-score rows as your first rewrite backlog."])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")


def run_full_pipeline(
    targets_path: Path,
    content_path: Path,
    committee_path: Path,
    out_dir: Path,
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles_path = out_dir / "profiles.json"
    matrix_path = out_dir / "committee_matrix.json"
    summary_path = out_dir / "summary.md"

    profile_targets(targets_path, profiles_path)
    matrix_payload = evaluate_content(profiles_path, content_path, committee_path, matrix_path)
    write_summary_markdown(matrix_payload, summary_path)

    return {
        "profiles": profiles_path,
        "matrix": matrix_path,
        "summary": summary_path,
    }


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MVP pipeline for audience profiling + committee synthesis.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    profile_cmd = subparsers.add_parser("profile", help="Build target audience profiles")
    profile_cmd.add_argument("--targets", required=True, type=Path)
    profile_cmd.add_argument("--out", required=True, type=Path)

    eval_cmd = subparsers.add_parser("evaluate", help="Run committee scoring")
    eval_cmd.add_argument("--profiles", required=True, type=Path)
    eval_cmd.add_argument("--content", required=True, type=Path)
    eval_cmd.add_argument("--committee", required=True, type=Path)
    eval_cmd.add_argument("--out", required=True, type=Path)

    synth_cmd = subparsers.add_parser("synthesize", help="Generate markdown summary")
    synth_cmd.add_argument("--matrix", required=True, type=Path)
    synth_cmd.add_argument("--out", required=True, type=Path)

    run_cmd = subparsers.add_parser("run", help="Run full pipeline")
    run_cmd.add_argument("--targets", required=True, type=Path)
    run_cmd.add_argument("--content", required=True, type=Path)
    run_cmd.add_argument("--committee", required=True, type=Path)
    run_cmd.add_argument("--outdir", required=True, type=Path)

    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()

    if args.command == "profile":
        payload = profile_targets(args.targets, args.out)
        print(f"profiles={payload['profile_count']} out={args.out}")
        return 0

    if args.command == "evaluate":
        payload = evaluate_content(args.profiles, args.content, args.committee, args.out)
        print(f"matrix_rows={payload['matrix_count']} out={args.out}")
        return 0

    if args.command == "synthesize":
        payload = load_json(args.matrix)
        write_summary_markdown(payload, args.out)
        print(f"summary_out={args.out}")
        return 0

    if args.command == "run":
        outputs = run_full_pipeline(args.targets, args.content, args.committee, args.outdir)
        print("pipeline_complete")
        for name, path in outputs.items():
            print(f"{name}={path}")
        return 0

    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
