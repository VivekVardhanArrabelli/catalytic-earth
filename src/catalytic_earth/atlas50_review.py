"""Local, append-only intake for the frozen Atlas-50 Phase B review packets.

Structural validation cannot establish reviewer identity or scientific agreement.
The July checkpoint stays immutable; incoming decisions are reported separately.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Sequence

from .atlas50_phase_b import (
    PHASE_B_RELATIVE,
    canonical_json_bytes,
    validate_phase_b_package,
    validate_review_submission,
)


SUBMISSIONS_RELATIVE = PHASE_B_RELATIVE / "review_submissions"


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON value: {value}")


def _parse_submission(raw: bytes) -> dict[str, Any]:
    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=_unique_object,
        parse_constant=_invalid_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("review submission must be a JSON object")
    return value


def load_review_context(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Bind intake to checked, byte-current packets and their frozen contract."""
    validate_phase_b_package(repo_root)
    phase_b = repo_root / PHASE_B_RELATIVE
    spec = json.loads((phase_b / "review_spec.json").read_bytes())
    packets = {}
    for name in ("crosswalk_review_queue.json", "panel_review_queue.json"):
        for packet in json.loads((phase_b / name).read_bytes())["packets"]:
            if packet["packet_id"] in packets:
                raise ValueError("duplicate review packet ID")
            packets[packet["packet_id"]] = packet
    return spec, packets


def build_template(packet: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    """Return an intentionally invalid draft without fabricating human choices."""
    if packet["packet_type"] == "crosswalk":
        fields = {
            "classification": "",
            "source_links": {
                key: "" for key in spec["crosswalk_review_contract"]["required_source_keys"]
            },
        }
    else:
        fields = {key: "" for key in spec["panel_review_contract"]["review_dimensions"]}
    return {
        "schema_version": "catalytic-earth.atlas50-review-submission.v1",
        "submission_id": "",
        "packet_id": packet["packet_id"],
        "packet_type": packet["packet_type"],
        "packet_sha256": hashlib.sha256(canonical_json_bytes(packet)).hexdigest(),
        "reviewer": {
            **{key: "" for key in spec["reviewer_evidence_contract"]["required_identity_fields"]},
            "project_author": None,
        },
        "attestation": "",
        "decision": {"outcome": "", "rationale": "", "uncertainty": [], "field_decisions": fields},
        "evidence_references": [],
        "conflicts": [],
        "submitted_at": "",
        "independent_annotation_claimed": False,
    }


def _validate_raw(raw: bytes, packets: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    value = _parse_submission(raw)
    packet_id = value.get("packet_id")
    if not isinstance(packet_id, str) or packet_id not in packets:
        raise ValueError("submission refers to an unknown packet ID")
    validate_review_submission(value, packets[packet_id], spec)
    return value


def validate_submission_file(
    path: Path, packets: dict[str, Any], spec: dict[str, Any]
) -> dict[str, Any]:
    return _validate_raw(path.read_bytes(), packets, spec)


def _submission_directory(repo_root: Path) -> Path:
    directory = repo_root / SUBMISSIONS_RELATIVE
    # Reject indirection through any ancestor, including a missing leaf reached
    # through an existing symlink, before creating files or following evidence.
    for path in [directory, *directory.parents]:
        if path == repo_root:
            break
        if path.is_symlink():
            raise ValueError(f"submission namespace contains a symlink: {path}")
    if directory.exists() and not directory.is_dir():
        raise ValueError("submission namespace must be a directory")
    return directory


def _check_append_only(repo_root: Path, baseline_ref: str) -> None:
    """Preserve every submission already present at the selected Git baseline.

    CI must pass its base/previous SHA to catch edits committed on a PR branch;
    HEAD alone protects previously committed files against worktree changes.
    """
    commit = subprocess.check_output(
        ["git", "rev-parse", "--verify", "--end-of-options", f"{baseline_ref}^{{commit}}"],
        cwd=repo_root, stderr=subprocess.PIPE, text=True,
    ).strip()
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "-z", commit, "--", SUBMISSIONS_RELATIVE.as_posix()],
        cwd=repo_root,
    )
    for raw_path in paths.split(b"\0"):
        if not raw_path:
            continue
        relative = raw_path.decode("utf-8")
        path = repo_root / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"append-only submission deleted or replaced: {relative}")
        original = subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=repo_root)
        if path.read_bytes() != original:
            raise ValueError(f"append-only submission changed: {relative}")


def _needs_resolution(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_needs_resolution(item) for item in value.values())
    if isinstance(value, list):
        return any(_needs_resolution(item) for item in value)
    return isinstance(value, str) and value in {
        "unresolved", "revise_classification", "revise_with_evidence",
        "reject_candidate_mapping", "replace_with_supported_mapping",
    }


def build_review_status(
    repo_root: Path, packets: dict[str, Any], spec: dict[str, Any], *, baseline_ref: str = "HEAD"
) -> dict[str, Any]:
    directory = _submission_directory(repo_root)
    _check_append_only(repo_root, baseline_ref)
    seen: set[str] = set()
    submissions: dict[str, list[dict[str, Any]]] = {key: [] for key in packets}
    for path in sorted(directory.iterdir()) if directory.exists() else []:
        if path.is_symlink() or not path.is_file() or path.suffix != ".json":
            raise ValueError(f"unexpected entry in submission namespace: {path.name}")
        raw = path.read_bytes()
        value = _validate_raw(raw, packets, spec)
        submission_id = value["submission_id"]
        if submission_id in seen:
            raise ValueError(f"duplicate submission ID: {submission_id}")
        seen.add(submission_id)
        submissions[value["packet_id"]].append({
            "path": path.relative_to(repo_root).as_posix(),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "submission_id": submission_id,
            "reviewer_id": value["reviewer"]["reviewer_id"],
            "project_author": value["reviewer"]["project_author"],
            "decision": value["decision"],
            "conflicts": value["conflicts"],
            "evidence_references": value["evidence_references"],
        })
    rows = []
    for packet_id, packet in packets.items():
        entries = submissions[packet_id]
        signatures = {canonical_json_bytes(entry["decision"]["field_decisions"]) +
                      entry["decision"]["outcome"].encode("utf-8") for entry in entries}
        rows.append({
            "packet_id": packet_id,
            "packet_type": packet["packet_type"],
            "valid_submission_count": len(entries),
            "multiple_decision_variants": len(signatures) > 1,
            "requires_resolution": any(
                _needs_resolution(entry["decision"]) or entry["conflicts"] for entry in entries
            ) or len(signatures) > 1,
            "submissions": entries,
        })
    return {
        "schema_version": "catalytic-earth.atlas50-review-intake-status.v1",
        "append_only_baseline_ref": baseline_ref,
        "packet_count": len(rows),
        "valid_submission_count": len(seen),
        "packets_with_valid_submissions": sum(bool(row["submissions"]) for row in rows),
        "packets_without_submissions": sum(not row["submissions"] for row in rows),
        "packets_requiring_resolution": sum(row["requires_resolution"] for row in rows),
        "packets": rows,
        "selection_frozen": False,
        "source_acquisition_permitted": False,
        "independent_annotation_claimed": False,
        "claim_boundary": "Schema-valid submissions are recorded assertions, not authenticated human review, scientific agreement, independent annotation, or freeze approval. The original Phase B checkpoint is unchanged.",
    }


def record_submission(
    repo_root: Path, submission_path: Path, packets: dict[str, Any], spec: dict[str, Any]
) -> Path:
    raw = submission_path.read_bytes()
    value = _validate_raw(raw, packets, spec)
    status = build_review_status(repo_root, packets, spec)
    if any(value["submission_id"] == entry["submission_id"]
           for row in status["packets"] for entry in row["submissions"]):
        raise ValueError(f"duplicate submission ID: {value['submission_id']}")
    directory = _submission_directory(repo_root)
    directory.mkdir(parents=True, exist_ok=True)
    # The ID cannot become a filesystem path. Publish fully written bytes with
    # an exclusive hard link, so concurrent readers never see a partial record
    # and retries cannot replace existing files or dangling symlinks.
    name = hashlib.sha256(value["submission_id"].encode("utf-8")).hexdigest() + ".json"
    destination = directory / name
    descriptor, temporary_name = tempfile.mkstemp(prefix=".review-intake-", dir=directory.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, destination)
    finally:
        temporary.unlink()
    return destination


def _write_new_json(path: Path, value: Any, repo_root: Path) -> None:
    # Draft/output files belong outside the source tree so a typo cannot alter
    # a frozen packet, protected registry, or append-only evidence directory.
    resolved = path.resolve()
    if resolved == repo_root.resolve() or repo_root.resolve() in resolved.parents:
        raise ValueError("write draft/output files outside the repository (for example, a temporary directory)")
    with path.open("xb") as stream:
        stream.write(canonical_json_bytes(value))


def main(argv: Sequence[str] | None = None, *, repo_root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="list the 97 frozen packet IDs")
    for name in ("packet", "template"):
        command = commands.add_parser(name, help="export a frozen packet" if name == "packet" else "create an intentionally incomplete review draft")
        command.add_argument("--packet-id", required=True)
        command.add_argument("--output", type=Path, required=True)
    for name in ("validate", "record"):
        command = commands.add_parser(name, help="validate supplied review assertions" if name == "validate" else "store supplied review assertions without overwriting evidence")
        command.add_argument("--submission", type=Path, required=True)
    status = commands.add_parser("status", help="report intake and unresolved decisions without freezing selection")
    status.add_argument("--output", type=Path)
    status.add_argument("--baseline-ref", default="HEAD", help="Git base or previous SHA for append-only verification")
    args = parser.parse_args(argv)
    root = repo_root or Path(__file__).resolve().parents[2]
    try:
        spec, packets = load_review_context(root)
        if args.command == "list":
            result = [{"packet_id": key, "packet_type": packet["packet_type"]} for key, packet in packets.items()]
        elif args.command in {"packet", "template"}:
            if args.packet_id not in packets:
                raise ValueError("unknown packet ID; use list to find exact identifiers")
            packet = packets[args.packet_id]
            result = packet if args.command == "packet" else build_template(packet, spec)
            _write_new_json(args.output, result, root)
            result = {"output": str(args.output), "status": "exported_packet" if args.command == "packet" else "incomplete_draft_not_a_submission"}
        elif args.command == "validate":
            value = validate_submission_file(args.submission, packets, spec)
            result = {"submission_id": value["submission_id"], "status": "schema_valid_identity_and_science_not_authenticated"}
        elif args.command == "record":
            path = record_submission(root, args.submission, packets, spec)
            result = {"path": path.relative_to(root).as_posix(), "status": "recorded_assertions_not_freeze_approval"}
        else:
            result = build_review_status(root, packets, spec, baseline_ref=args.baseline_ref)
            if args.output:
                _write_new_json(args.output, result, root)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Review intake failed: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
