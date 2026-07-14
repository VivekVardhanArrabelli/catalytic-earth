"""Run the frozen Atlas-10 unintegrated same-source comparator without Atlas joins."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
MANIFEST_PATH = ROOT / "data/atlas/atlas10/source_manifest.json"
OUTPUT_PATH = ROOT / "data/atlas/atlas10/comparator/unintegrated_source_stack.json"
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas10_selection import load_atlas10_selection  # noqa: E402
from catalytic_earth.atlas10_source_adapters import (  # noqa: E402
    mcsa_reference_residue_rows,
    read_atlas10_mcsa_snapshot,
    read_atlas10_rhea_snapshot,
    read_cath_snapshot,
)
from catalytic_earth.atlas10_sources import load_atlas10_source_manifest  # noqa: E402
from catalytic_earth.atlas_source_adapters import (  # noqa: E402
    read_pdb_snapshot,
    read_uniprot_snapshot,
)


FIELD_STATUS_WEIGHT = {"complete": 1.0, "partial": 0.5, "absent": 0.0}


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot_path(record: dict[str, Any]) -> Path:
    relative = record["snapshot_path"]
    if not isinstance(relative, str):
        raise ValueError(f"{record['source_id']} {record['record_id']} has no snapshot")
    return ROOT / relative


def _source_rows(
    selection: dict[str, Any], manifest: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    records = {
        (record["source_id"], record["record_id"]): record
        for record in manifest["records"]
    }
    rows: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    hazards: list[dict[str, Any]] = []
    for case in selection["follow_on_cases"]:
        case_rows: list[dict[str, Any]] = []
        mcsa: dict[str, Any] | None = None
        reaction: dict[str, Any] | None = None
        for handle in case["source_handles"]:
            key = handle["source_id"], handle["record_id"]
            record = records[key]
            common = {
                "source_id": key[0],
                "source_record_id": key[1],
                "evidence_role": handle["evidence_role"],
                "applicability": handle["applicability"],
                "retrieval_status": record["retrieval_status"],
                "snapshot_sha256": record["snapshot_sha256"],
            }
            if key[0] == "UniProtKB":
                source = read_uniprot_snapshot(_snapshot_path(record), key[1])
                details = {
                    "protein_name": source["protein_name"],
                    "organism": source["organism"],
                    "sequence_length": len(source["sequence"]),
                    "pdb_cross_reference_ids": sorted(source["pdb_cross_references"]),
                }
            elif key[0] == "Rhea":
                reaction = read_atlas10_rhea_snapshot(
                    _snapshot_path(record),
                    key[1],
                    selected_participant_ids=set(case["reaction_participant_ids"]),
                )
                details = {
                    "source_status": reaction["source_status"],
                    "source_record_id": reaction["source_record_id"],
                    "source_query": reaction["source_query"],
                    "equation": reaction["equation"],
                    "rhea_participant_count": len(reaction["participants"]),
                }
            elif key[0] == "PDB":
                source = read_pdb_snapshot(_snapshot_path(record), key[1])
                details = {
                    "title": source["title"],
                    "experimental_method": source["method"],
                    "resolution_angstrom": source["resolution_angstrom"],
                    "coordinate_residue_count": len(source["residues"]),
                }
            elif key[0] == "M-CSA":
                mcsa = read_atlas10_mcsa_snapshot(_snapshot_path(record), key[1])
                details = {
                    "enzyme_name": mcsa["enzyme_name"],
                    "mechanisms": [
                        {
                            "mechanism_id": mechanism["mechanism_id"],
                            "rating": mechanism["rating"],
                            "is_detailed": mechanism["is_detailed"],
                            "non_product_step_count": sum(
                                not step["is_product"]
                                for step in mechanism.get("steps", [])
                            ),
                        }
                        for mechanism in mcsa["mechanisms"]
                    ],
                    "reference_residue_row_count": len(
                        mcsa_reference_residue_rows(mcsa)
                    ),
                    "compound_row_count": len(mcsa["compounds"]),
                    "scheme_retrieval_statuses": sorted(
                        {item["retrieval_status"] for item in mcsa["scheme_index"].values()}
                    ),
                }
            elif key[0] == "CATH":
                source = read_cath_snapshot(_snapshot_path(record), key[1])
                details = {
                    "classification_id": source["classification_id"],
                    "description": source["description"],
                    "selected_pdb_ids": source["selected_pdb_ids"],
                }
            elif key[0] == "DOI":
                details = {
                    "uri": record["uri"],
                    "content_bundled": False,
                    "reason": "reference-only handle; article text is not redistributed",
                }
            else:
                raise ValueError(f"unsupported baseline source: {key[0]}")
            case_rows.append({**common, "source_fields": details})
        if reaction is None or mcsa is None:
            raise ValueError(f"{case['case_id']} baseline lacks Rhea or M-CSA")
        if reaction["source_status"] == "documented_query_gap" and mcsa["compounds"]:
            conflicts.append(
                {
                    "conflict_id": f"{case['case_id']}.rhea-gap-vs-mcsa-context",
                    "case_id": case["case_id"],
                    "summary": "The official Rhea EC query has zero rows while M-CSA separately supplies participant context; an unintegrated stack does not provide a canonical cross-source resolution.",
                    "status": "unresolved_in_baseline",
                }
            )
        if len(mcsa["mechanisms"]) > 1:
            conflicts.append(
                {
                    "conflict_id": f"{case['case_id']}.multiple-mcsa-proposals",
                    "case_id": case["case_id"],
                    "summary": "M-CSA supplies multiple proposals and ratings; the source stack does not independently adjudicate them.",
                    "status": "unresolved_in_baseline",
                }
            )
        pdb_applicabilities = {
            handle["applicability"]
            for handle in case["source_handles"]
            if handle["source_id"] == "PDB"
        }
        if {"direct", "engineered_source_reference"}.issubset(pdb_applicabilities):
            conflicts.append(
                {
                    "conflict_id": f"{case['case_id']}.direct-vs-engineered-structure",
                    "case_id": case["case_id"],
                    "summary": "Direct and engineered source-reference structures coexist and require an explicit applicability join.",
                    "status": "unresolved_in_baseline",
                }
            )
        for mechanism in mcsa["mechanisms"]:
            if not mechanism["is_detailed"] and mechanism["rating"] > 0:
                hazards.append(
                    {
                        "hazard_id": f"{case['case_id']}.rating-granularity-confusion",
                        "case_id": case["case_id"],
                        "summary": "A positive source rating and non-detailed granularity are separate dimensions; treating rating as permission to create steps would fabricate detail.",
                    }
                )
        rows.append({"case_id": case["case_id"], "source_rows": case_rows})
    return rows, conflicts, hazards


def _field_assessments(selection: dict[str, Any]) -> dict[str, Any]:
    assessment_by_field = {
        "case_id": ("complete", "Frozen selection identifier."),
        "fold_classification_ids": ("complete", "Individual CATH source rows."),
        "catalytic_site_roles": ("complete", "Individual M-CSA residue/role rows."),
        "mechanism_steps_or_abstention": (
            "complete",
            "M-CSA step rows and is_detailed flag, without cross-source grounding.",
        ),
        "source_applicability": (
            "complete",
            "Frozen handle applicability labels and individual structure metadata.",
        ),
        "counterevidence": (
            "absent",
            "No integrated counterevidence object exists in the unjoined source rows.",
        ),
        "uncertainty": (
            "absent",
            "No integrated open-uncertainty/abstention object exists in the source rows.",
        ),
        "provenance": (
            "partial",
            "Per-source hashes exist, but no compiled record lineage binds the cross-source answer.",
        ),
        "reaction_or_source_gap": ("complete", "Individual Rhea record or zero-row query."),
        "metal_and_intermediate_roles": ("complete", "Individual M-CSA role and step text."),
        "conserved_and_repurposed_sites": (
            "absent",
            "Requires the cross-case relationship join prohibited in this baseline.",
        ),
    }
    output: dict[str, Any] = {}
    fractions: list[float] = []
    for query in selection["query_contracts"]:
        fields = {
            field: {
                "status": assessment_by_field[field][0],
                "basis": assessment_by_field[field][1],
            }
            for field in query["required_fields"]
        }
        score = sum(FIELD_STATUS_WEIGHT[item["status"]] for item in fields.values())
        fraction = score / len(fields)
        fractions.append(fraction)
        output[query["query_id"]] = {
            "fields": fields,
            "weighted_complete_equivalent": score,
            "required_field_count": len(fields),
            "completeness_fraction": fraction,
        }
    return {
        "by_query": output,
        "overall_mean_completeness_fraction": sum(fractions) / len(fractions),
        "scoring": FIELD_STATUS_WEIGHT,
    }


def build_baseline(
    selection: dict[str, Any], manifest: dict[str, Any]
) -> dict[str, Any]:
    rows, conflicts, hazards = _source_rows(selection, manifest)
    return {
        "schema_version": "catalytic-earth.atlas10-unintegrated-baseline.v1",
        "baseline_id": selection["baseline_contract"]["baseline_id"],
        "status": "run_from_frozen_sources",
        "input_bindings": {
            "selection_file_sha256": _file_sha256(SELECTION_PATH),
            "source_manifest_file_sha256": _file_sha256(MANIFEST_PATH),
            "source_snapshot_set_sha256": manifest["snapshot_set_sha256"],
            "retrieved_at": manifest["retrieved_at"],
            "atlas_outputs_used": [],
        },
        "method": selection["baseline_contract"]["comparator"],
        "same_source_budget": {
            "external_requests_acquisition": manifest["acquisition"][
                "external_requests_used"
            ],
            "download_bytes_acquisition": manifest["acquisition"][
                "download_bytes_used"
            ],
            "external_requests_replay": 0,
            "network_used_during_replay": False,
        },
        "unintegrated_case_source_rows": rows,
        "measurements": {
            "elapsed_human_minutes": {
                "value": None,
                "status": "not_measured_no_observed_human_run",
            },
            "machine_requests": {
                "source_acquisition": manifest["acquisition"]["external_requests_used"],
                "frozen_replay": 0,
            },
            "required_field_completeness": _field_assessments(selection),
            "unresolved_source_conflicts": {
                "count": len(conflicts),
                "items": conflicts,
            },
            "applicability_errors": {
                "value": None,
                "status": "not_measured_without_observed_human_answers_or_external_review",
            },
            "unsupported_detail_count": {
                "value": 0,
                "basis": "The baseline emits source rows and no generated mechanism detail; this does not imply query completeness.",
            },
            "query_answer_completeness": _field_assessments(selection),
        },
        "interpretation_hazards": hazards,
        "claim_boundary": selection["baseline_contract"]["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    selection = load_atlas10_selection(SELECTION_PATH)
    manifest = load_atlas10_source_manifest(
        MANIFEST_PATH, repo_root=ROOT, selection=selection
    )
    raw = _json_bytes(build_baseline(selection, manifest))
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != raw:
            raise SystemExit("Atlas-10 unintegrated baseline output is stale")
        print("Atlas-10 unintegrated baseline output is current")
        return 0
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(raw)
    value = json.loads(raw)
    print(
        json.dumps(
            {
                "unresolved_source_conflicts": value["measurements"][
                    "unresolved_source_conflicts"
                ]["count"],
                "query_completeness": value["measurements"][
                    "query_answer_completeness"
                ]["overall_mean_completeness_fraction"],
                "human_minutes": None,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
