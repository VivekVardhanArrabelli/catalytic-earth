#!/usr/bin/env python3
"""Backfill prior lane candidate hits into candidate-level evidence rows.

This converter reads compact lane artifacts only, finds existing within-window
heteromeric candidate hits, and emits `epk_candidate_evidence_v1` rows. It is a
review-only schema conversion: it does not fetch coordinates, compute scores for
production, import labels, tune thresholds, edit registries/fingerprints, or
make production-readiness claims.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import guarded_phrase_candidate_rows as candidate_schema


LANE_ID = "epk_positive_evidence"
SCHEMA_VERSION = candidate_schema.SCHEMA_VERSION
TARGET_FAMILY_ID = candidate_schema.TARGET_FAMILY_ID
TARGET_FINGERPRINT_ID = candidate_schema.TARGET_FINGERPRINT_ID


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text())
    except Exception:  # noqa: BLE001 - skip malformed/non-JSON artifacts.
        return None


def iter_scan_rows(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    rows = payload.get("rows")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict) and row.get("pdb_id")]


def row_has_candidate_hit(row: dict[str, Any]) -> bool:
    return bool(row.get("heteromeric_candidate_hits") or row.get("transition_analog_candidate_hits"))


def candidate_dedupe_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    geometry = candidate.get("source_free_geometry", {})
    state = candidate.get("coordinate_state")
    if state == "active_gamma":
        distance = geometry.get("nearest_terminal_distance_angstrom")
        donor_context = (
            geometry.get("terminal_ligand_code"),
            geometry.get("terminal_associated_polymer_chain_name")
            or geometry.get("terminal_chain_name"),
            geometry.get("terminal_associated_polymer_entity_id"),
        )
    else:
        distance = geometry.get("nearest_analog_distance_angstrom")
        donor_context = (
            geometry.get("analog_ligand_code"),
            geometry.get("analog_chain_name"),
            geometry.get("analog_auth_seq_id"),
        )
    return (
        candidate.get("pdb_id"),
        state,
        *donor_context,
        geometry.get("candidate_chain_name"),
        geometry.get("candidate_auth_seq_id"),
        geometry.get("candidate_residue_code"),
        geometry.get("candidate_atom_name"),
        distance,
    )


def specificity_score(candidate: dict[str, Any]) -> int:
    geometry = candidate.get("source_free_geometry", {})
    score = 0
    if not geometry.get("terminal_instance_inferred_from_associated_polymer"):
        score += 2
    if "source_mapped" in candidate.get("signal_tags", []):
        score += 1
    if "local_metal" in candidate.get("signal_tags", []):
        score += 1
    return score


def collect_candidate_rows(
    artifacts_dir: Path,
    out: Path,
    max_source_rows: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    prior_pdb_ids = candidate_schema.collect_prior_pdb_ids(artifacts_dir, out)
    emitted_by_key: dict[tuple[Any, ...], dict[str, Any]] = {}
    source_rows: list[dict[str, Any]] = []
    source_artifact_counts: dict[str, int] = {}

    for path in sorted(artifacts_dir.glob("*.json")):
        if path.resolve() == out.resolve():
            continue
        payload = load_json(path)
        for scan_row in iter_scan_rows(payload):
            if not row_has_candidate_hit(scan_row):
                continue
            if len(source_rows) >= max_source_rows:
                break
            source_rows.append(
                {
                    "source_artifact": str(path),
                    "pdb_id": scan_row.get("pdb_id"),
                    "candidate_status": scan_row.get("candidate_status"),
                    "heteromeric_candidate_hit_count": len(scan_row.get("heteromeric_candidate_hits", [])),
                    "transition_analog_candidate_hit_count": len(
                        scan_row.get("transition_analog_candidate_hits", [])
                    ),
                }
            )
            source_artifact_counts[str(path)] = source_artifact_counts.get(str(path), 0) + 1
            for candidate in candidate_schema.candidate_rows_from_scan(scan_row, prior_pdb_ids):
                candidate["source_context"]["source_artifact"] = str(path)
                candidate["blockers"] = sorted(
                    set(candidate["blockers"] + ["backfilled_from_prior_lane_artifact"])
                )
                candidate["signal_tags"] = sorted(
                    set(candidate["signal_tags"] + ["prior_lane_schema_backfill"])
                )
                key = candidate_dedupe_key(candidate)
                existing = emitted_by_key.get(key)
                if existing is None or specificity_score(candidate) > specificity_score(existing):
                    emitted_by_key[key] = candidate
        if len(source_rows) >= max_source_rows:
            break

    return list(emitted_by_key.values()), source_rows, source_artifact_counts


def build_artifact(
    out: Path,
    artifacts_dir: Path,
    max_source_rows: int,
) -> dict[str, Any]:
    generated_at = candidate_schema.current.now_iso()
    candidate_rows, source_rows, source_artifact_counts = collect_candidate_rows(
        artifacts_dir, out, max_source_rows
    )
    coordinate_state_counts: dict[str, int] = {}
    policy_counts: dict[str, int] = {}
    for row in candidate_rows:
        state = row["coordinate_state"]
        coordinate_state_counts[state] = coordinate_state_counts.get(state, 0) + 1
        policy = row["policy_decision"]
        policy_counts[policy] = policy_counts.get(policy, 0) + 1

    folded = [
        row["candidate_id"]
        for row in candidate_rows
        if any(tag.startswith("folded_protein") for tag in row.get("signal_tags", []))
    ]
    local_metal = [
        row["candidate_id"]
        for row in candidate_rows
        if "local_metal" in row.get("signal_tags", [])
    ]

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "prior_candidate_evidence_row_backfill",
            "schema_version": SCHEMA_VERSION,
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "source_rows_reviewed": len(source_rows),
            "candidate_evidence_rows_emitted": len(candidate_rows),
            "coordinate_state_counts": coordinate_state_counts,
            "policy_decision_counts": policy_counts,
            "folded_protein_candidate_row_count": len(folded),
            "local_metal_candidate_row_count": len(local_metal),
            "source_artifact_counts": source_artifact_counts,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Backfill converts prior compact lane hits to candidate evidence rows. "
                "Source context remains separate from geometry and is not a predictive feature."
            ),
        },
        "source_rows": source_rows,
        "candidate_evidence_rows": candidate_rows,
        "source_review_summary": {
            "primary_outcome": "candidate_evidence_rows_emitted",
            "production_claim_allowed": False,
            "search_surface_exhausted": False,
            "evidence_for": [
                f"Converted {len(candidate_rows)} prior lane candidate hits into candidate-level evidence rows.",
                "Rows preserve active-gamma versus transition-analog coordinate states and keep source context separate from source-free geometry.",
            ],
            "evidence_against": [
                "Rows are backfilled review-only evidence from prior lane artifacts, not fresh production positives.",
                "Every emitted row keeps policy_decision=review_only_abstain and countable_label_candidate=false.",
            ],
            "counterexamples_found": [],
            "recommendation": (
                "Use these rows as review-only anchors for adjudication and stress testing. "
                "Do not import labels, tune thresholds, edit registries/fingerprints, or claim production readiness."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_positive_evidence"),
    )
    parser.add_argument("--max-source-rows", type=int, default=220)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(args.out, args.artifacts_dir, args.max_source_rows)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "source_rows_reviewed": artifact["metadata"]["source_rows_reviewed"],
                "candidate_evidence_rows_emitted": artifact["metadata"][
                    "candidate_evidence_rows_emitted"
                ],
                "coordinate_state_counts": artifact["metadata"]["coordinate_state_counts"],
                "folded_protein_candidate_row_count": artifact["metadata"][
                    "folded_protein_candidate_row_count"
                ],
                "local_metal_candidate_row_count": artifact["metadata"][
                    "local_metal_candidate_row_count"
                ],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
