"""Reproduce a bounded unreviewed scan from an explicit retained-source registry."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_candidate_extraction import extract_panel_candidate


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def render(value: dict) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def _unique_keys(pairs: list[tuple[str, object]]) -> dict:
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _positive_integer(value: object) -> bool:
    return type(value) is int and value > 0


def _validate_registry(registry: object) -> list[dict]:
    if not isinstance(registry, dict) or registry.get("schema_version") != "catalytic-earth.candidate-source-registry.v1":
        raise ValueError("unsupported candidate source registry")
    records = registry.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("registry records must be a nonempty array")
    seen_records = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("registry record must be an object")
        record_id = record.get("record_id")
        path = record.get("snapshot_path")
        sha = record.get("snapshot_sha256")
        if not isinstance(record_id, str) or re.fullmatch(r"M[0-9]{4}", record_id) is None or record_id in seen_records:
            raise ValueError("registry must contain unique M-CSA record IDs")
        seen_records.add(record_id)
        if not isinstance(path, str) or not path or "\\" in path or Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("snapshot path must be a safe relative path")
        if not isinstance(sha, str) or re.fullmatch(r"[0-9a-f]{64}", sha) is None:
            raise ValueError("snapshot SHA256 must be a lowercase hex digest")
        mechanisms = record.get("mechanisms")
        if not isinstance(mechanisms, list) or not mechanisms:
            raise ValueError("record mechanisms must be a nonempty array")
        seen_mechanisms = set()
        for mechanism in mechanisms:
            if not isinstance(mechanism, dict):
                raise ValueError("mechanism must be an object")
            mechanism_id = mechanism.get("mechanism_id")
            step_ids = mechanism.get("step_ids")
            if not _positive_integer(mechanism_id) or mechanism_id in seen_mechanisms:
                raise ValueError("record must have exactly one row per positive integer mechanism ID")
            seen_mechanisms.add(mechanism_id)
            if not isinstance(step_ids, list) or len(step_ids) < 2 or not all(_positive_integer(step) for step in step_ids):
                raise ValueError("step IDs must be a nonempty array of positive integers with an adjacent pair")
            if step_ids != sorted(set(step_ids)) or any(after != before + 1 for before, after in zip(step_ids, step_ids[1:])):
                raise ValueError("mechanism step IDs must be unique, ordered and contiguous")
    return records


def scan(registry_path: Path, *, repo_root: Path = ROOT) -> dict:
    if repo_root.resolve() != ROOT.resolve():
        raise ValueError("scan must use the repository containing its executing implementation")
    raw_registry = registry_path.read_bytes()
    records = _validate_registry(json.loads(raw_registry, object_pairs_hook=_unique_keys))
    results = []
    per_record = []
    for record in records:
        source_path = (repo_root / record["snapshot_path"]).resolve()
        source_path.relative_to(repo_root.resolve())
        raw_source = source_path.read_bytes()
        if digest(raw_source) != record["snapshot_sha256"]:
            raise ValueError(f"snapshot hash mismatch: {record['record_id']}")
        source = json.loads(raw_source, object_pairs_hook=_unique_keys)
        if source["record_id"] != record["record_id"]:
            raise ValueError("registry and snapshot record IDs differ")
        actual = [(s["mechanism_id"], s["step_id"]) for s in source["step_schemes"]]
        if any(not _positive_integer(m) or not _positive_integer(s) for m, s in actual):
            raise ValueError("source scheme IDs must be positive integers")
        actual.sort()
        source_mechanisms = source["entry"]["reaction"]["mechanisms"]
        source_ids = [m["mechanism_id"] for m in source_mechanisms]
        if any(not _positive_integer(m) for m in source_ids) or len(set(source_ids)) != len(source_ids):
            raise ValueError("source mechanism IDs must be unique positive integers")
        if set(source_ids) != {m["mechanism_id"] for m in record["mechanisms"]}:
            raise ValueError("registry mechanism inventory differs from source")
        entry_panels = [(m["mechanism_id"], s["step_id"]) for m in source_mechanisms for s in m["steps"]]
        if any(not _positive_integer(step) for _, step in entry_panels) or sorted(entry_panels) != actual:
            raise ValueError("retained panel inventory differs from source entry steps")
        declared = sorted(
            (m["mechanism_id"], step_id)
            for m in record["mechanisms"] for step_id in m["step_ids"]
        )
        if actual != declared or len(set(declared)) != len(declared):
            raise ValueError("registry must cover every retained source panel exactly once")
        record_rows = []
        for mechanism in record["mechanisms"]:
            step_ids = mechanism["step_ids"]
            if step_ids != sorted(step_ids) or len(step_ids) < 2:
                raise ValueError("mechanism requires ordered adjacent source panels")
            for before, after in zip(step_ids, step_ids[1:]):
                if after != before + 1:
                    raise ValueError("noncontiguous source panels cannot be scanned as adjacent")
                # Integrity errors deliberately propagate; they are not chemical abstentions.
                candidate = extract_panel_candidate(
                    raw_source, mechanism_id=mechanism["mechanism_id"], before_step_id=before,
                )
                coverage = candidate["coverage"]
                row = {
                    "candidate_id": candidate["candidate_id"],
                    "record_id": record["record_id"],
                    "mechanism_id": mechanism["mechanism_id"],
                    "before_step_id": before,
                    "after_step_id": after,
                    "status": candidate["status"],
                    "extraction_status": candidate["extraction_status"],
                    "candidate_sha256": digest(render(candidate).encode("utf-8")),
                    "diagnostics": candidate["diagnostics"],
                    "edit_counts": dict(sorted(Counter(
                        edit["support"] for edit in candidate["proposed_graph_edits"]
                    ).items())),
                    "coverage": None if coverage is None else {
                        key: coverage[key] for key in (
                            "before_node_count", "after_node_count", "mapped_node_count",
                            "projection_replays_exactly", "full_panel_replay_asserted",
                        )
                    },
                }
                record_rows.append(row)
        results.extend(record_rows)
        if len(record_rows) != len(actual) - len(record["mechanisms"]):
            raise ValueError("scan must cover every adjacency within each source mechanism")
        per_record.append({
            "record_id": record["record_id"],
            "pair_count": len(record_rows),
            "candidate_count": sum(r["extraction_status"] == "candidate" for r in record_rows),
            "needs_review_count": sum(r["extraction_status"] == "needs_review" for r in record_rows),
        })
    if len({r["candidate_id"] for r in results}) != len(results):
        raise ValueError("candidate IDs must be unique across the scan")
    dependencies = [
        "scripts/scan_atlas_candidates.py",
        "src/catalytic_earth/atlas_candidate_extraction.py",
        "src/catalytic_earth/atlas_partial_panels.py",
        "src/catalytic_earth/atlas_transformations.py",
        "src/catalytic_earth/atlas10_source_adapters.py",
    ]
    for path in dependencies[1:]:
        module = importlib.import_module("catalytic_earth." + Path(path).stem)
        if Path(module.__file__).resolve() != (ROOT / path).resolve():
            raise ValueError("dependency hash path differs from executing module origin")
    return {
        "schema_version": "catalytic-earth.candidate-scan.v1",
        "status": "unreviewed",
        "source_registry_sha256": digest(raw_registry),
        "implementation_sha256": {p: digest((repo_root / p).read_bytes()) for p in dependencies},
        "scope": {
            "retained_sources_only": True,
            "network_requests": 0,
            "reviewed_evidence": False,
            "experimentally_validated": False,
            "candidate_count_is_validated_transition_count": False,
            "diagnostics_are_exhaustive": False,
            "interpretation": "First blocking diagnostic per attempted pair; no claims about unexamined chemistry.",
        },
        "aggregate": {
            "record_count": len(records),
            "mechanism_count": sum(len(r["mechanisms"]) for r in records),
            "pair_count": len(results),
            "candidate_count": sum(r["extraction_status"] == "candidate" for r in results),
            "needs_review_count": sum(r["extraction_status"] == "needs_review" for r in results),
            "full_panel_replay_count": sum(bool(r["coverage"] and r["coverage"]["full_panel_replay_asserted"]) for r in results),
            "diagnostic_counts": dict(sorted(Counter(
                d["code"] for r in results for d in r["diagnostics"]
            ).items())),
        },
        "records": per_record,
        "pairs": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=ROOT / "data/atlas/candidate_extraction/source_registry.json")
    parser.add_argument("--output", type=Path, help="new JSON report path; refuses overwrites")
    parser.add_argument("--check", type=Path, help="require a retained report to match the reproduced bytes")
    args = parser.parse_args()
    result = scan(args.registry)
    rendered = render(result)
    if args.check and args.check.read_bytes() != rendered.encode("utf-8"):
        raise ValueError("retained candidate scan does not reproduce exactly")
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)
    print(json.dumps(result["aggregate"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
