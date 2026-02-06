#!/usr/bin/env python3
"""
Created: 2026-02-05
Updated: 2026-02-06
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
URL_NOISE_TOKENS = {"http", "https", "www", "com", "org", "net", "index"}
FOCUS_BONUS_CAP = 12.0

METRIC_LENS_TERMS = {
    "fit": {
        "market",
        "wedge",
        "distribution",
        "user",
        "growth",
        "retention",
        "roadmap",
        "workflow",
        "strategy",
        "scale",
        "product",
        "behavior",
    },
    "clarity": {
        "story",
        "clarity",
        "framing",
        "pitch",
        "communication",
        "digestible",
        "narrative",
        "readability",
    },
    "novelty": {
        "novel",
        "novelty",
        "creative",
        "innovation",
        "differentiation",
        "moat",
        "wedge",
    },
    "trust": {
        "safety",
        "risk",
        "reliability",
        "latency",
        "guardrail",
        "telemetry",
        "rollout",
        "evidence",
        "proof",
        "architecture",
        "maintainability",
        "performance",
        "quality",
        "tooling",
        "ergonomic",
        "defensibility",
        "deployment",
    },
}

METRIC_STRENGTH_MESSAGES = {
    "fit": "there is a real wedge worth testing",
    "clarity": "the framing is direct and understandable",
    "novelty": "the mechanism has differentiated potential",
    "trust": "the idea signals responsible decision-making intent",
}

METRIC_GAP_MESSAGES = {
    "fit": "target user, wedge, and distribution path are underspecified",
    "clarity": "input/output workflow is still too abstract",
    "novelty": "differentiation versus generic review tooling is still thin",
    "trust": "evidence, guardrails, and reliability proof are missing",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def normalize_token(token: str) -> str:
    token = token.lower().strip("'")
    if token.endswith("'s"):
        token = token[:-2]
    for suffix in ("ing", "ed", "ly", "es", "s"):
        if len(token) > 4 and token.endswith(suffix):
            token = token[: -len(suffix)]
            break
    return token


def tokenize(text: str) -> list[str]:
    raw = re.findall(r"[a-z0-9']+", text.lower())
    normalized = [normalize_token(t) for t in raw]
    return [
        t
        for t in normalized
        if len(t) >= 3 and t not in STOPWORDS and t not in URL_NOISE_TOKENS
    ]


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


def normalize_weight_map(weight_map: dict[str, float]) -> dict[str, float]:
    cleaned = {k: max(float(v), 0.0) for k, v in weight_map.items()}
    total = sum(cleaned.values())
    if total <= 0:
        size = max(1, len(cleaned))
        return {k: 1.0 / size for k in cleaned}
    return {k: v / total for k, v in cleaned.items()}


def build_default_judging_criteria(rubric_weights: dict[str, float]) -> list[dict[str, Any]]:
    normalized = normalize_weight_map(rubric_weights)
    return [
        {
            "id": metric,
            "label": metric.title(),
            "description": f"Derived from {metric} rubric signal.",
            "mapped_metric": metric,
            "weight": weight,
        }
        for metric, weight in normalized.items()
    ]


def extract_judging_criteria(
    committee_payload: dict[str, Any],
    rubric_weights: dict[str, float],
) -> list[dict[str, Any]]:
    raw = committee_payload.get("judging_criteria", [])
    criteria: list[dict[str, Any]] = []

    for item in raw:
        mapped_metric = item.get("mapped_metric")
        if mapped_metric not in rubric_weights:
            continue
        weight = float(item.get("weight", 0.0))
        if weight <= 0:
            continue
        criteria.append(
            {
                "id": item.get("id", mapped_metric),
                "label": item.get("label", str(mapped_metric).title()),
                "description": item.get("description", ""),
                "mapped_metric": mapped_metric,
                "weight": weight,
            }
        )

    if not criteria:
        return build_default_judging_criteria(rubric_weights)

    normalized = normalize_weight_map({c["id"]: c["weight"] for c in criteria})
    for criterion in criteria:
        criterion["weight"] = normalized[criterion["id"]]
    return criteria


def build_expert_metric_weights(
    expert_focus_tokens: set[str],
    rubric_weights: dict[str, float],
) -> dict[str, float]:
    base = normalize_weight_map(rubric_weights)
    adjusted: dict[str, float] = {}

    for metric, base_weight in base.items():
        lens_terms = METRIC_LENS_TERMS.get(metric, set())
        overlap = len(expert_focus_tokens.intersection(lens_terms))
        signal = overlap / max(1, len(expert_focus_tokens))
        adjusted[metric] = base_weight * (1.0 + (0.9 * signal))

    return normalize_weight_map(adjusted)


def score_focus_alignment(
    expert_focus_tokens: set[str],
    content_token_set: set[str],
    profile_interest_tokens: set[str],
) -> tuple[float, dict[str, list[str]]]:
    content_overlap = sorted(expert_focus_tokens.intersection(content_token_set))
    profile_overlap = sorted(expert_focus_tokens.intersection(profile_interest_tokens))

    bonus = min(
        FOCUS_BONUS_CAP,
        (len(content_overlap) * 2.6) + (len(profile_overlap) * 1.4),
    )

    return (
        bonus,
        {
            "content_overlap": content_overlap[:5],
            "profile_overlap": profile_overlap[:5],
        },
    )


def synthesize_criteria_scores(
    subscores: dict[str, float],
    judging_criteria: list[dict[str, Any]],
    expert_focus_tokens: set[str],
    profile_interest_tokens: set[str],
    content_token_set: set[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for criterion in judging_criteria:
        mapped_metric = criterion["mapped_metric"]
        base = float(subscores.get(mapped_metric, 0.0))
        criterion_text = (
            f"{criterion.get('id', '')} "
            f"{criterion.get('label', '')} "
            f"{criterion.get('description', '')}"
        )
        criterion_tokens = set(tokenize(criterion_text))
        focus_hits = sorted(criterion_tokens.intersection(expert_focus_tokens))
        profile_hits = sorted(criterion_tokens.intersection(profile_interest_tokens))
        content_hits = sorted(criterion_tokens.intersection(content_token_set))

        empathy_boost = min(
            10.0,
            (len(focus_hits) * 2.0) + (len(profile_hits) * 1.2) + (len(content_hits) * 1.0),
        )
        score = clamp(base + empathy_boost)

        if score >= 70:
            takeaway = METRIC_STRENGTH_MESSAGES.get(
                mapped_metric,
                "this criterion has strong support",
            )
        else:
            takeaway = METRIC_GAP_MESSAGES.get(
                mapped_metric,
                "this criterion needs sharper execution detail",
            )

        rows.append(
            {
                "id": criterion.get("id", mapped_metric),
                "label": criterion.get("label", str(mapped_metric).title()),
                "mapped_metric": mapped_metric,
                "weight": round(float(criterion.get("weight", 0.0)), 4),
                "score": round(score, 2),
                "takeaway": takeaway,
                "signals": {
                    "focus_hits": focus_hits[:3],
                    "profile_hits": profile_hits[:3],
                    "content_hits": content_hits[:3],
                },
            }
        )

    return rows


def dominant_metric(metric_weights: dict[str, float]) -> str:
    if not metric_weights:
        return "fit"
    return max(metric_weights.items(), key=lambda item: item[1])[0]


def build_persona_messages(
    expert: dict[str, Any],
    profile: dict[str, Any],
    opinion: str,
    subscores: dict[str, float],
    metric_weights: dict[str, float],
    criteria_scores: list[dict[str, Any]],
    focus_alignment: dict[str, list[str]],
) -> tuple[list[str], list[str], str]:
    persona = expert.get("persona", expert.get("id", "expert"))
    strongest = (
        max(criteria_scores, key=lambda row: row["score"])
        if criteria_scores
        else {"label": "Clarity", "mapped_metric": "clarity", "score": subscores.get("clarity", 0)}
    )
    weakest = (
        min(criteria_scores, key=lambda row: row["score"])
        if criteria_scores
        else {"label": "Fit", "mapped_metric": "fit", "score": subscores.get("fit", 0)}
    )
    primary_lens = dominant_metric(metric_weights)
    primary_score = float(subscores.get(primary_lens, 0.0))
    profile_overlap = focus_alignment.get("profile_overlap", [])
    content_overlap = focus_alignment.get("content_overlap", [])

    pros: list[str] = []
    if profile_overlap:
        overlap_preview = ", ".join(profile_overlap[:2])
        pros.append(f"{persona}: profile evidence shows strong bias toward {overlap_preview}")
    if content_overlap:
        focus_token = content_overlap[0]
        pros.append(f"{persona}: proposal directly touches my '{focus_token}' lens")
    if primary_score >= 70 and primary_lens in METRIC_STRENGTH_MESSAGES:
        pros.append(f"{persona}: {METRIC_STRENGTH_MESSAGES[primary_lens]}")
    if strongest["score"] >= 70:
        pros.append(f"{persona}: {strongest['label']} suggests {strongest['takeaway']}")
    if subscores.get("clarity", 0) >= 70:
        pros.append(f"{persona}: framing is crisp and easy to parse quickly")

    cons: list[str] = []
    if not content_overlap:
        if profile_overlap:
            cons.append(
                f"{persona}: pitch does not explicitly answer my core lens ({profile_overlap[0]})"
            )
        else:
            cons.append(
                f"{persona}: content still misses my operating vocabulary ({', '.join(expert.get('focus_keywords', [])[:3])})"
            )
    if primary_lens in METRIC_GAP_MESSAGES and primary_score < 65:
        cons.append(f"{persona}: {METRIC_GAP_MESSAGES[primary_lens]}")
    if weakest["score"] < 70:
        cons.append(f"{persona}: {weakest['label']} gap: {weakest['takeaway']}")
    if not pros:
        pros.append(f"{persona}: clear intent to operationalize idea validation")
    if not cons:
        cons.append(f"{persona}: add one concrete experiment plus a success metric before ship")

    style_preference = profile.get("style_preference", "snackable")
    delivery_hint = (
        "Keep the pitch concise and decision-oriented."
        if style_preference == "snackable"
        else "Use a detailed memo with explicit evidence and tradeoffs."
    )
    rationale = (
        f"As {persona}, I read this as a solid intent to systematize idea review. "
        f"Strongest signal: {strongest['label']} ({strongest['score']}). "
        f"Main blocker: {weakest['label']} ({weakest['score']}). "
        f"Current call: {opinion}. {delivery_hint}"
    )

    return pros[:3], cons[:3], rationale


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


def canonicalize_feedback_phrase(text: str) -> str:
    return re.sub(r"^[^:]+:\s*", "", text).strip()


def build_expert_feedback(
    profile: dict[str, Any],
    content: dict[str, Any],
    expert: dict[str, Any],
    rubric_weights: dict[str, float],
    judging_criteria: list[dict[str, Any]],
) -> dict[str, Any]:
    text = f"{content.get('title', '')}\n{content.get('body', '')}"
    content_tokens = tokenize(text)
    content_token_set = set(content_tokens)
    profile_interest_tokens = set(profile.get("interests", []))
    expert_focus_tokens = set(tokenize(" ".join(expert.get("focus_keywords", []))))

    metric_weights = build_expert_metric_weights(expert_focus_tokens, rubric_weights)

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

    focus_bonus, focus_alignment = score_focus_alignment(
        expert_focus_tokens,
        content_token_set,
        profile_interest_tokens,
    )

    weighted = sum(subscores[k] * metric_weights.get(k, 0.0) for k in subscores)
    overall = clamp(weighted + focus_bonus)

    if overall >= 78:
        opinion = "Ship"
    elif overall >= 62:
        opinion = "Iterate"
    else:
        opinion = "Pass"

    criteria_scores = synthesize_criteria_scores(
        subscores,
        judging_criteria,
        expert_focus_tokens,
        profile_interest_tokens,
        content_token_set,
    )
    pros, cons, rationale = build_persona_messages(
        expert,
        profile,
        opinion,
        subscores,
        metric_weights,
        criteria_scores,
        focus_alignment,
    )

    return {
        "expert_id": expert["id"],
        "persona": expert.get("persona", expert["id"]),
        "weight": expert.get("weight", 1.0),
        "opinion": opinion,
        "overall": round(overall, 2),
        "subscores": subscores,
        "lens_metric_weights": {k: round(v, 4) for k, v in metric_weights.items()},
        "focus_bonus": round(focus_bonus, 2),
        "focus_alignment": focus_alignment,
        "criteria_scores": criteria_scores,
        "rationale": rationale,
        "pros": pros[:3],
        "cons": cons[:3],
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
            pro_counts[canonicalize_feedback_phrase(pro)] += 1
        for con in fb.get("cons", []):
            con_counts[canonicalize_feedback_phrase(con)] += 1

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
    rubric_weights = normalize_weight_map(
        committee_payload.get(
        "rubric_weights",
        {"fit": 0.45, "clarity": 0.2, "novelty": 0.2, "trust": 0.15},
        )
    )
    judging_criteria = extract_judging_criteria(committee_payload, rubric_weights)

    matrix: list[dict[str, Any]] = []
    for profile in profiles:
        for content in content_items:
            feedback = [
                build_expert_feedback(
                    profile,
                    content,
                    expert,
                    rubric_weights,
                    judging_criteria,
                )
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
        "rubric_weights": rubric_weights,
        "judging_criteria": judging_criteria,
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
        "Updated: 2026-02-06",
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
