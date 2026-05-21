#!/usr/bin/env python3
"""Adjudicate fresh source-published non-peptide literature mappings.

The input artifact already contains bounded source/article mapping and compact
coordinate scans. This helper converts those fresh mapped rows into a compact
review-only adjudication surface without fetching or storing raw coordinates.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import current_release_epk_followup as current


LANE_ID = "epk_positive_evidence"


def nearest_acceptor_summaries(row: dict[str, Any]) -> list[dict[str, Any]]:
    summaries = []
    for donor in row.get("terminal_donor_records", []):
        nearest = donor.get("nearest_heteromeric_acceptor")
        summaries.append(
            {
                "terminal_ligand_code": donor.get("terminal_ligand_code"),
                "terminal_atom_name": donor.get("terminal_atom_name"),
                "terminal_chain_name": donor.get("terminal_chain_name"),
                "terminal_auth_seq_id": donor.get("terminal_auth_seq_id"),
                "associated_polymer_chain_name": donor.get("associated_polymer_chain_name"),
                "associated_polymer_entity_id": donor.get("associated_polymer_entity_id"),
                "local_metals": donor.get("local_metals", []),
                "nearest_heteromeric_acceptor": nearest,
            }
        )
    for analog in row.get("transition_analog_records", []):
        nearest = analog.get("nearest_heteromeric_acceptor")
        summaries.append(
            {
                "analog_ligand_code": analog.get("analog_ligand_code"),
                "analog_chain_name": analog.get("analog_chain_name"),
                "analog_auth_seq_id": analog.get("analog_auth_seq_id"),
                "local_metals": analog.get("local_metals", []),
                "nearest_heteromeric_acceptor": nearest,
            }
        )
    return summaries


def compact_entities(row: dict[str, Any]) -> list[dict[str, Any]]:
    entities = []
    for entity_id, entity in sorted(row.get("polymer_entities", {}).items()):
        entities.append(
            {
                "entity_id": entity_id,
                "description": entity.get("description"),
                "auth_asym_ids": entity.get("auth_asym_ids", []),
                "uniprot_ids": entity.get("uniprot_ids", []),
                "polymer_type": entity.get("polymer_type"),
                "length": row.get("polymer_entity_lengths", {}).get(str(entity_id)),
            }
        )
    return entities


def adjudication_status(row: dict[str, Any]) -> tuple[str, list[str]]:
    title = (row.get("title") or "").lower()
    entities = " ".join(
        (entity.get("description") or "").lower()
        for entity in row.get("polymer_entities", {}).values()
    )
    status = row.get("candidate_status")
    blockers = ["review_only_lane", "production_policy_abstain"]
    if status == "donor_or_analog_without_heteromeric_acceptor_review_only":
        blockers.append("no_within_6_angstrom_heteromeric_acceptor")
    if "craf" in title or "raf" in entities or "mek" in entities:
        blockers.append("source_published_raf_mek_geometry_negative")
        if any(not donor.get("local_metals") for donor in row.get("terminal_donor_records", [])):
            blockers.append("no_local_mg_or_mn_on_relevant_donor")
        return "source_published_folded_protein_geometry_negative_review_only", blockers
    if "selo" in title or "ampylation" in (row.get("citation", {}).get("title") or "").lower():
        blockers.append("non_epk_pseudokinase_ampylation_context")
        return "non_epk_or_non_phosphoryl_transfer_source_mismatch_review_only", blockers
    if "parkin" in title or "prohibitin" in title or "cop9" in title or "peptide" in title:
        blockers.append("keyword_article_mapping_not_epk_substrate_transfer_state")
        return "source_keyword_mapping_noise_review_only", blockers
    if status == "no_active_donor_or_transition_analog_review_only":
        blockers.append("no_active_gamma_or_transition_analog_state")
    return "fresh_source_mapped_geometry_negative_review_only", blockers


def build_artifact(input_path: Path, out: Path) -> dict[str, Any]:
    source = json.loads(input_path.read_text())
    rows = []
    status_counts: dict[str, int] = {}
    blocker_counts: dict[str, int] = {}
    for row in source.get("rows", []):
        decision, blockers = adjudication_status(row)
        status_counts[decision] = status_counts.get(decision, 0) + 1
        for blocker in blockers:
            blocker_counts[blocker] = blocker_counts.get(blocker, 0) + 1
        rows.append(
            {
                "pdb_id": row.get("pdb_id"),
                "structure_title": row.get("title"),
                "citation": row.get("citation", {}),
                "source_hits": row.get("search_hits", []),
                "candidate_status": row.get("candidate_status"),
                "adjudication_status": decision,
                "policy_decision": "review_only_abstain",
                "claim_status": "candidate_review_only_non_countable",
                "blockers": blockers,
                "polymer_entities": compact_entities(row),
                "source_free_geometry_summary": {
                    "terminal_donor_atom_count": row.get("terminal_donor_atom_count"),
                    "transition_analog_group_count": row.get("transition_analog_group_count"),
                    "heteromeric_candidate_hit_count": len(row.get("heteromeric_candidate_hits", [])),
                    "transition_analog_candidate_hit_count": len(
                        row.get("transition_analog_candidate_hits", [])
                    ),
                    "donor_or_analog_summaries": nearest_acceptor_summaries(row),
                },
                "source_review_not_predictive_coordinate_feature": True,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "epk_score_computed": False,
                "ready_for_production_scoring": False,
                "ready_for_label_import": False,
            }
        )

    no_acceptor_ids = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "donor_or_analog_without_heteromeric_acceptor_review_only"
    ]
    source_published_negative_ids = [
        row["pdb_id"]
        for row in rows
        if row["adjudication_status"] == "source_published_folded_protein_geometry_negative_review_only"
    ]
    non_epk_ids = [
        row["pdb_id"]
        for row in rows
        if row["adjudication_status"] == "non_epk_or_non_phosphoryl_transfer_source_mismatch_review_only"
    ]
    keyword_noise_ids = [
        row["pdb_id"]
        for row in rows
        if row["adjudication_status"] == "source_keyword_mapping_noise_review_only"
    ]

    evidence_for = [
        (
            f"Adjudicated {len(rows)} fresh source-published/literature-mapped PDB rows "
            "from the non-peptide phosphosite follow-up."
        )
    ]
    evidence_against = [
        "No fresh row contains a within-6-Angstrom heteromeric Ser/Thr/Tyr acceptor candidate.",
    ]
    if no_acceptor_ids:
        evidence_against.append(
            "Fresh donor/analog rows without a local heteromeric acceptor: "
            + ", ".join(no_acceptor_ids[:20])
            + "."
        )
    if source_published_negative_ids:
        evidence_against.append(
            "Source-published folded-protein rows are geometry-negative rather than positive transfer states: "
            + ", ".join(source_published_negative_ids[:20])
            + "."
        )
    if non_epk_ids:
        evidence_against.append(
            "Fresh source mappings include non-ePK or non-phosphoryl-transfer mismatches: "
            + ", ".join(non_epk_ids[:20])
            + "."
        )
    if keyword_noise_ids:
        evidence_against.append(
            f"{len(keyword_noise_ids)} fresh mappings are source-keyword noise without active ePK donor-to-substrate geometry."
        )

    counterexamples = []
    if non_epk_ids:
        counterexamples.append(
            "Non-ePK/non-phosphoryl-transfer source mismatches: " + ", ".join(non_epk_ids[:20])
        )
    if source_published_negative_ids:
        counterexamples.append(
            "Source-published folded-protein geometry negatives: "
            + ", ".join(source_published_negative_ids[:20])
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "source_published_nonpeptide_adjudication",
            "generated_at": current.now_iso(),
            "input_artifact": str(input_path),
            "rows_reviewed": len(rows),
            "adjudication_status_counts": status_counts,
            "blocker_counts": blocker_counts,
            "candidate_evidence_rows_emitted": 0,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Adjudication summarizes source context separately from source-free "
                "geometry and does not create production labels or scoring features."
            ),
        },
        "rows": rows,
        "source_review_summary": {
            "primary_outcome": "search_surface_exhausted",
            "production_claim_allowed": False,
            "search_surface_exhausted": True,
            "evidence_for": evidence_for,
            "evidence_against": evidence_against,
            "counterexamples_found": counterexamples,
            "recommendation": (
                "Use these fresh rows as review-only negative source-surface evidence. "
                "Do not promote any production label, threshold, registry, fingerprint, "
                "migration, scoring feature, or readiness claim."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(args.input, args.out)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "rows_reviewed": artifact["metadata"]["rows_reviewed"],
                "adjudication_status_counts": artifact["metadata"]["adjudication_status_counts"],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
