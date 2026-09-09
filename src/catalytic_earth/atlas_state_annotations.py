"""Current source annotations beside immutable, reviewed state-probe reports.

Only component role wording and its provenance change in this view. Scientific permissions,
state variables, source transcription and historical reports are preserved.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .canonical_hash import canonical_file_sha256

INDEX = "data/atlas/atlas50/state_probe/current_annotations.json"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _json(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(result, dict), "annotation document must be an object")
    return result


def _path(root: Path, relative: str) -> Path:
    _require(isinstance(relative, str) and bool(relative), "annotation path is absent")
    posix, windows = PurePosixPath(relative), PureWindowsPath(relative)
    _require(not posix.is_absolute() and not windows.drive and "\\" not in relative
             and ".." not in posix.parts and posix.as_posix() == relative,
             "annotation path must be repository-relative")
    result = (root / relative).resolve()
    _require(root.resolve() in result.parents, "annotation path escapes repository")
    return result


def checked_annotations(root: Path) -> list[dict[str, Any]]:
    """Check review pins, source joins and cumulative acquisition lineage."""
    index = _json(root / INDEX)
    _require(index.get("schema_version") == "catalytic-earth.state-annotation-index.v1",
             "annotation index schema differs")
    output = []
    for relative in index["packets"]:
        packet = _path(root, relative)
        review = _json(packet / "review.json")
        _require(review.get("decision") == "accept_source_scoped_correction",
                 "source annotation has no accepted review")
        names = ("annotations.json", "source_inventory.json", "acquisition_appendix.json")
        _require(review.get("reviewed_sha256") == {
            name: canonical_file_sha256(packet / name) for name in names
        }, "source annotation review pins differ")
        inventory = _json(packet / "source_inventory.json")
        acquisition = _json(packet / "acquisition_appendix.json")
        inherited = acquisition["inherited_receipts"]
        inherited_path = _path(root, inherited["path"])
        _require(canonical_file_sha256(inherited_path) == inherited["sha256"],
                 "inherited acquisition pin differs")
        rows = _json(inherited_path)[inherited["receipt_field"]]
        count = sum(len(row.get("urls", [row.get("url")])) for row in rows)
        size = sum(sum(row["bytes"]) if isinstance(row["bytes"], list)
                   else row["bytes"] for row in rows)
        _require((count, size) == (acquisition["inherited_requests"],
                                  acquisition["inherited_bytes"]),
                 "inherited acquisition totals differ")
        attempts = acquisition["attempts"]
        _require([row["request_index"] for row in attempts]
                 == list(range(count + 1, count + len(attempts) + 1)),
                 "acquisition request sequence differs")
        _require(all(type(row.get("bytes")) is int and row["bytes"] >= 0
                     for row in attempts), "acquisition byte count is invalid")
        count += len(attempts)
        size += sum(row["bytes"] for row in attempts)
        _require((count, size) == (acquisition["cumulative_requests"],
                                  acquisition["cumulative_bytes"])
                 and count <= 100 and size <= 31457280,
                 "cumulative acquisition totals differ or exceed limits")
        _require(inventory["batch_id"] == acquisition["batch_id"],
                 "source acquisition batch differs")
        sources = {row["artifact_id"]: row for row in inventory["sources"]}
        _require(len(sources) == len(inventory["sources"]), "source IDs repeat")
        captures = {row["request_index"]: row for row in attempts}
        for source in sources.values():
            capture = captures.get(source["request_index"], {})
            _require(capture.get("status") == 200 and
                     (source["sha256"], source["bytes"], source["source_url"])
                     == (capture.get("sha256"), capture.get("bytes"), capture.get("url")),
                     "source capture binding differs")
        document = _json(packet / "annotations.json")
        _require(document.get("schema_version") == "catalytic-earth.state-source-annotations.v1",
                 "source annotation schema differs")
        for annotation in document["annotations"]:
            _require(annotation.get("permission_change") is False,
                     "source annotation cannot change permissions")
            findings = {row["finding_id"]: row for row in annotation["source_findings"]}
            _require(len(findings) == len(annotation["source_findings"]), "finding IDs repeat")
            role_ids = annotation["component_role_correction"]["source_finding_ids"]
            _require(bool(role_ids) and len(role_ids) == len(set(role_ids))
                     and set(role_ids) <= set(findings), "role finding binding differs")
            for finding in findings.values():
                ids = finding["source_artifact_ids"]
                _require(bool(ids) and set(ids) <= set(sources),
                         "annotation cites an absent source")
            _validate_report_bindings(root, annotation)
            output.append({**annotation, "sources": list(sources.values()),
                           "review": review})
    identifiers = [row["annotation_id"] for row in output]
    _require(len(identifiers) == len(set(identifiers)), "annotation IDs repeat")
    return output


def _apply_role(case: dict[str, Any], annotation: dict[str, Any]) -> None:
    correction = annotation["component_role_correction"]
    matches = [row for row in case["representation"]["components"]
               if row["component_id"] == correction["component_id"]]
    _require(len(matches) == 1, "annotated component is absent or ambiguous")
    _require(matches[0]["role"] == correction["expected_role"],
             "historical component role differs")
    role = correction["current_role"]
    _require(isinstance(role, str) and bool(role.strip()), "current role is absent")
    matches[0]["role"] = role
    findings = {row["finding_id"]: row for row in annotation["source_findings"]}
    matches[0]["role_annotation"] = {
        "annotation_id": annotation["annotation_id"],
        "historical_role": correction["expected_role"],
        "source_finding_ids": correction["source_finding_ids"],
        "source_artifact_ids": sorted({source_id for finding_id in correction["source_finding_ids"]
                                       for source_id in findings[finding_id]["source_artifact_ids"]}),
    }
    matches[0]["evidence_ids_scope"] = (
        "historical component identity; current role is supported by role_annotation"
    )


def _validate_report_bindings(root: Path, annotation: dict[str, Any]) -> None:
    bindings = annotation["report_bindings"]
    _require(bool(bindings) and len({row["path"] for row in bindings}) == len(bindings),
             "report binding paths are absent or repeat")
    for binding in bindings:
        path = _path(root, binding["path"])
        _require(canonical_file_sha256(path) == binding["sha256"],
                 "source annotation report binding differs")
        matches = [row for row in _json(path)["cases"]
                   if row["mcsa_id"] == annotation["mcsa_id"]]
        _require(len(matches) == 1, "annotated case is absent or ambiguous")
        _apply_role(copy.deepcopy(matches[0]), annotation)


def current_cases(root: Path, report_path: Path) -> dict[str, Any]:
    """Return corrected views with exact original bindings and source caveats."""
    report = _json(report_path)
    relative = report_path.resolve().relative_to(root.resolve()).as_posix()
    digest = canonical_file_sha256(report_path)
    annotations = checked_annotations(root)
    views = []
    for historical in report["cases"]:
        case = copy.deepcopy(historical)
        applicable = [row for row in annotations if row["mcsa_id"] == case["mcsa_id"]]
        for annotation in applicable:
            _require({"path": relative, "sha256": digest} in annotation["report_bindings"],
                     "source annotation report binding differs")
            _apply_role(case, annotation)
        views.append({"case": case, "current_source_annotations": applicable})
    return {"schema_version": "catalytic-earth.current-state-view.v1",
            "historical_report": {"path": relative, "sha256": digest},
            "permission_change": False, "cases": views}


def query_case(root: Path, report_path: Path, mcsa_id: str) -> dict[str, Any]:
    result = current_cases(root, report_path)
    matches = [row for row in result["cases"] if row["case"]["mcsa_id"] == mcsa_id]
    _require(len(matches) == 1, "requested case is absent or ambiguous")
    return {key: value for key, value in result.items() if key != "cases"} | matches[0]
