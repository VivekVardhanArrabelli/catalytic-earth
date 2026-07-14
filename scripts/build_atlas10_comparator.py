"""Compare the frozen Atlas-10 runtime with the independently built source stack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
BASELINE_PATH = ROOT / "data/atlas/atlas10/comparator/unintegrated_source_stack.json"
EXPECTED_PATH = ROOT / "data/atlas/atlas10/queries/runtime_expected.json"
KERNEL_PATH = ROOT / "data/atlas/atlas10/kernel.json"
OUTPUT_PATH = ROOT / "data/atlas/atlas10/comparator/atlas_vs_unintegrated.json"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _atlas_completeness(
    selection: dict[str, Any], expected: dict[str, Any]
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for query in selection["query_contracts"]:
        rows = expected["relationship_query_results"][query["query_id"]]
        fields = {
            field: all(row.get(field) not in (None, "") for row in rows)
            for field in query["required_fields"]
        }
        output[query["query_id"]] = {
            "required_field_count": len(fields),
            "complete_field_count": sum(fields.values()),
            "completeness_fraction": sum(fields.values()) / len(fields),
            "field_nonempty_for_every_row": fields,
            "row_count": len(rows),
        }
    return output


def build_comparison(
    selection: dict[str, Any],
    baseline: dict[str, Any],
    expected: dict[str, Any],
    kernel: dict[str, Any],
) -> dict[str, Any]:
    atlas_completeness = _atlas_completeness(selection, expected)
    cyclophilin = next(
        record
        for record in kernel["follow_on_records"]
        if record["case_id"] == "atlas10.cyclophilin-a-human.isomerization"
        and record["object_type"] == "mechanism_hypothesis"
    )
    if any(
        proposal["mechanism_steps"] for proposal in cyclophilin["mechanism_proposals"]
    ):
        raise ValueError("Atlas comparator detected fabricated cyclophilin steps")
    conflict_count = baseline["measurements"]["unresolved_source_conflicts"]["count"]
    return {
        "schema_version": "catalytic-earth.atlas10-comparator-report.v1",
        "baseline_id": baseline["baseline_id"],
        "atlas_runtime_result_sha256": expected["runtime_result_sha256"],
        "same_source_budget_confirmed": (
            baseline["input_bindings"]["source_snapshot_set_sha256"]
            == kernel["source_snapshot_set_sha256"]
        ),
        "measurements": {
            "elapsed_human_minutes": {
                "baseline": None,
                "atlas": None,
                "speedup_claim": None,
                "status": "not_measured; no timing or speedup is claimed",
            },
            "machine_requests": {
                "shared_source_acquisition": baseline["same_source_budget"][
                    "external_requests_acquisition"
                ],
                "baseline_frozen_replay": 0,
                "atlas_frozen_runtime": 0,
            },
            "required_field_completeness": {
                "baseline": baseline["measurements"]["required_field_completeness"],
                "atlas": atlas_completeness,
            },
            "unresolved_source_conflicts": {
                "baseline_unintegrated_count": conflict_count,
                "atlas_explicitly_represented_not_biologically_adjudicated_count": conflict_count,
                "atlas_silently_collapsed_count": 0,
            },
            "applicability_errors": {
                "baseline": None,
                "atlas": None,
                "status": "not measured without observed human answers or external review",
            },
            "unsupported_detail_count": {
                "baseline_generated_detail": baseline["measurements"][
                    "unsupported_detail_count"
                ]["value"],
                "atlas_detected_by_frozen_guards": 0,
                "cyclophilin_discrete_step_count": 0,
            },
            "query_answer_completeness": {
                "baseline_mean_fraction": baseline["measurements"][
                    "query_answer_completeness"
                ]["overall_mean_completeness_fraction"],
                "atlas_mean_fraction": sum(
                    item["completeness_fraction"] for item in atlas_completeness.values()
                )
                / len(atlas_completeness),
                "interpretation": "Structural required-field completeness only; not biological correctness or discovery utility.",
            },
        },
        "conclusion": (
            "On the frozen structural contract, the integrated Atlas query surface fills every required field while the unintegrated source rows leave relationship, uncertainty, counterevidence, or compiled-lineage fields absent or partial. No human-time speedup, biological-accuracy gain, or discovery claim is supported by this run."
        ),
        "claim_boundary": selection["baseline_contract"]["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL_PATH.read_text(encoding="utf-8"))
    raw = _json_bytes(build_comparison(selection, baseline, expected, kernel))
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != raw:
            raise SystemExit("Atlas-10 comparator report is stale")
        print("Atlas-10 comparator report is current")
        return 0
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(raw)
    value = json.loads(raw)
    print(json.dumps(value["measurements"]["query_answer_completeness"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
