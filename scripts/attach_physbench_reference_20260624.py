#!/usr/bin/env python3
"""Attach PhysBench as an additional Physical AI L4-card reference."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
JSON_TARGETS = [
    DATA_DIR / "interactive_l1_l2_l3_payload.json",
    DATA_DIR / "global_ai_risk_l4_overlay_nodes.json",
    DATA_DIR / "global_ai_risk_l4_overlay_nodes.v2.json",
]
CSV_TARGET = DATA_DIR / "global_ai_risk_l4_overlay_nodes.csv"

PHYSBENCH = {
    "physbench_reference_title": "PhysBench: Benchmarking and Enhancing Vision-Language Models for Physical World Understanding",
    "physbench_reference_url": "https://huggingface.co/papers/2501.16411",
    "physbench_arxiv_url": "https://arxiv.org/abs/2501.16411",
    "physbench_project_url": "https://physbench.github.io/",
    "physbench_dataset_url": "https://huggingface.co/datasets/USC-PSI-Lab/PhysBench",
    "physbench_github_url": "https://github.com/USC-GVL/PhysBench",
    "physbench_reference_type": "Benchmark paper / dataset",
    "physbench_reference_year": "2025",
    "physbench_dataset_rows": "10002",
    "physbench_capability_domains": "physical object properties; physical object relationships; physical scene understanding; physics-based dynamics",
    "physbench_capability_dimensions": "8",
    "physbench_subclasses": "19",
    "physbench_models_evaluated": "75",
    "physbench_reference_attached_at": "2026-06-24",
}

DIRECT = re.compile(
    r"perception|situational|scene|object|physical commonsense|dynamics|world-model|"
    r"sensor|occlusion|localization|vision|household|danger recognition|unsafe-action|"
    r"humanoid scene|physicality|foundation-model robotics",
    re.I,
)
SUPPORTING = re.compile(
    r"planning|control|manipulation|motion|collision|locomotion|runtime|adaptation|"
    r"monitor|sim-to-real|simulation|transfer|safe task|hazard|robot|humanoid|"
    r"embodied|assistive|interaction|benchmark|reward|physical action",
    re.I,
)

BASIS = {
    "direct": "Matches PhysBench physical-world understanding domains.",
    "supporting": "Physical-world understanding is a safety precondition for this card.",
    "contextual": "Contextual Physical AI benchmark reference; not a direct benchmark target.",
}


def is_phys_card(row: dict) -> bool:
    return str(row.get("id", "")).startswith("PHYS")


def relevance(row: dict) -> str:
    text = " ".join(str(row.get(k, "")) for k in ["l2", "l3", "l4_label", "definition", "source", "evidence_title"])
    if DIRECT.search(text):
        return "direct"
    if SUPPORTING.search(text):
        return "supporting"
    return "contextual"


def attach(row: dict) -> str:
    tier = relevance(row)
    row.update(PHYSBENCH)
    row["physbench_relevance_tier"] = tier
    row["physbench_relevance_basis"] = BASIS[tier]
    return tier


def iter_risk_nodes(data: object) -> list[dict]:
    if isinstance(data, dict):
        return data.get("risk_nodes", [])
    if isinstance(data, list):
        return data
    return []


def update_json(path: Path) -> Counter:
    data = json.loads(path.read_text(encoding="utf-8"))
    counts: Counter = Counter()
    for row in iter_risk_nodes(data):
        if is_phys_card(row):
            counts[attach(row)] += 1
    if isinstance(data, dict):
        metadata = data.setdefault("risk_metadata", {})
        metadata["physbench_reference_update"] = {
            "date": "2026-06-24",
            "source": PHYSBENCH["physbench_reference_title"],
            "hf_paper_url": PHYSBENCH["physbench_reference_url"],
            "arxiv_url": PHYSBENCH["physbench_arxiv_url"],
            "dataset_url": PHYSBENCH["physbench_dataset_url"],
            "attached_to_physical_ai_l4_cards": int(sum(counts.values())),
            "relevance_tier_counts": dict(counts),
            "method": "Rule-based matching from L2/L3/L4 labels, definitions, and evidence titles to PhysBench physical-world understanding domains.",
        }
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return counts


def update_csv(path: Path) -> Counter:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []
    counts: Counter = Counter()
    for row in rows:
        if is_phys_card(row):
            counts[attach(row)] += 1
    for key in list(PHYSBENCH) + ["physbench_relevance_tier", "physbench_relevance_basis"]:
        if key not in fieldnames:
            fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return counts


def main() -> None:
    for path in JSON_TARGETS:
        if path.exists():
            print(path.name, dict(update_json(path)))
    if CSV_TARGET.exists():
        print(CSV_TARGET.name, dict(update_csv(CSV_TARGET)))


if __name__ == "__main__":
    main()
