"""Evaluate opaque-context extraction on the frozen 101-pair source inventory."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.scan_atlas_candidates import render, scan
from catalytic_earth import atlas_context_candidates
from catalytic_earth.atlas_candidate_extraction import extract_panel_candidate


REGISTRY = ROOT / "data/atlas/candidate_extraction/source_registry.json"
BASELINE = ROOT / "data/atlas/candidate_extraction/scan.json"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def scan_context_candidates() -> dict:
    # Reuse the frozen scanner's complete source/entry/registry integrity checks.
    baseline = scan(REGISTRY)
    baseline_bytes = BASELINE.read_bytes()
    registry_bytes = REGISTRY.read_bytes()
    if render(baseline).encode("utf-8") != baseline_bytes:
        raise ValueError("frozen v1 candidate scan no longer reproduces")
    if _sha(registry_bytes) != baseline["source_registry_sha256"]:
        raise ValueError("source registry changed after baseline validation")
    if Path(atlas_context_candidates.__file__).resolve() != (ROOT / "src/catalytic_earth/atlas_context_candidates.py").resolve():
        raise ValueError("context implementation origin differs from its hash path")
    registry = json.loads(registry_bytes)
    sources = {r["record_id"]: (ROOT / r["snapshot_path"]).read_bytes() for r in registry["records"]}
    # Verify again at the point of use, rather than relying on an earlier read.
    for record in registry["records"]:
        if _sha(sources[record["record_id"]]) != record["snapshot_sha256"]:
            raise ValueError("source changed between baseline validation and context extraction")
    rows = []
    for old in baseline["pairs"]:
        raw = sources[old["record_id"]]
        result = atlas_context_candidates.extract_context_panel_candidate(
            raw, mechanism_id=old["mechanism_id"], before_step_id=old["before_step_id"],
        )
        if result["status"] != "unreviewed" or result["extraction_status"] not in {"candidate", "needs_review"}:
            raise ValueError("unexpected context-candidate status")
        candidate = result["extraction_status"] == "candidate"
        was_candidate = old["extraction_status"] == "candidate"
        if was_candidate and candidate:
            original = extract_panel_candidate(raw, mechanism_id=old["mechanism_id"], before_step_id=old["before_step_id"])
            for side in ("before_graph", "after_graph"):
                original["source_panels"][side]["graph_id"] = original["source_panels"][side]["graph_id"].replace(
                    ":full-source-panel", ":full-covalent-source-panel",
                )
            if result["proposed_graph_edits"] != original["proposed_graph_edits"] or result["source_panels"] != original["source_panels"]:
                raise ValueError("context mode regressed a frozen v1 candidate")
        context = result["opaque_source_context"]
        coverage = result["coverage"]
        rows.append({
            "candidate_id": result["candidate_id"],
            "record_id": old["record_id"],
            "mechanism_id": old["mechanism_id"],
            "before_step_id": old["before_step_id"],
            "after_step_id": old["after_step_id"],
            "status": result["status"],
            "extraction_status": result["extraction_status"],
            "baseline_extraction_status": old["extraction_status"],
            "newly_supported": candidate and not was_candidate,
            "baseline_withheld": was_candidate and not candidate,
            "candidate_sha256": _sha(render(result).encode("utf-8")),
            "diagnostics": result["diagnostics"],
            "edit_counts": dict(sorted(Counter(e["support"] for e in result["proposed_graph_edits"]).items())),
            "context_counts": None if context is None else {
                side: None if context[side] is None else {
                    kind: len(context[side][kind]) for kind in ("bond_stereo", "atom_parity", "bond_conventions")
                } for side in ("before", "after")
            },
            "coverage": None if coverage is None else {
                key: coverage[key] for key in (
                    "before_node_count", "after_node_count", "mapped_node_count",
                    "projection_replays_exactly", "full_covalent_graph_replay_asserted",
                )
            },
        })
    dependency_paths = [
        "scripts/scan_atlas_context_candidates.py",
        "src/catalytic_earth/atlas_context_candidates.py",
    ]
    return {
        "schema_version": "catalytic-earth.context-candidate-scan.v1",
        "status": "unreviewed",
        "source_registry_sha256": _sha(registry_bytes),
        "baseline_scan_sha256": _sha(baseline_bytes),
        "implementation_sha256": {
            **baseline["implementation_sha256"],
            **{path: _sha((ROOT / path).read_bytes()) for path in dependency_paths},
        },
        "scope": {
            "retained_sources_only": True,
            "network_requests": 0,
            "reviewed_evidence": False,
            "experimentally_validated": False,
            "stereochemistry_interpreted": False,
            "coordination_chemistry_interpreted": False,
            "candidate_count_is_validated_transition_count": False,
            "diagnostics_are_exhaustive": False,
            "interpretation": "Unreviewed covalent-graph candidates; special annotations are preserved opaquely and are outside chemical-state replay.",
        },
        "aggregate": {
            "record_count": baseline["aggregate"]["record_count"],
            "mechanism_count": baseline["aggregate"]["mechanism_count"],
            "pair_count": len(rows),
            "baseline_candidate_count": baseline["aggregate"]["candidate_count"],
            "baseline_retained_candidate_count": sum(r["baseline_extraction_status"] == "candidate" and r["extraction_status"] == "candidate" for r in rows),
            "baseline_withheld_count": sum(r["baseline_withheld"] for r in rows),
            "candidate_count": sum(r["extraction_status"] == "candidate" for r in rows),
            "newly_supported_count": sum(r["newly_supported"] for r in rows),
            "needs_review_count": sum(r["extraction_status"] == "needs_review" for r in rows),
            "full_covalent_graph_replay_count": sum(bool(r["coverage"] and r["coverage"]["full_covalent_graph_replay_asserted"]) for r in rows),
            "diagnostic_counts": dict(sorted(Counter(d["code"] for r in rows for d in r["diagnostics"]).items())),
        },
        "pairs": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="new report path; refuses overwrites")
    parser.add_argument("--check", type=Path, help="require a report to match reproduced bytes")
    args = parser.parse_args()
    result = scan_context_candidates()
    rendered = render(result)
    if args.check and args.check.read_bytes() != rendered.encode("utf-8"):
        raise ValueError("retained context scan does not reproduce exactly")
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)
    print(json.dumps(result["aggregate"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
