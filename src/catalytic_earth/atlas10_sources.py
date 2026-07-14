"""Validation for the bounded Atlas-10 follow-on source package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .atlas10_selection import validate_atlas10_selection
from .canonical_hash import canonical_file_sha256


SCHEMA_VERSION = "catalytic-earth.atlas10-source-manifest.v1"
SOURCE_ROOT = "data/atlas/atlas10/sources/"
BUNDLED_SOURCES = {"CATH", "M-CSA", "PDB", "Rhea", "UniProtKB"}
REFERENCE_ONLY_SOURCES = {"DOI"}
EXPECTED_LICENSES = {
    "CATH": "CC BY 4.0",
    "DOI": "article-specific terms; reference-only handle",
    "M-CSA": "CC BY 4.0",
    "PDB": "CC0 1.0 archive file",
    "Rhea": "CC BY 4.0",
    "UniProtKB": "CC BY 4.0",
}
RECORD_FIELDS = {
    "attribution",
    "change_notice",
    "license",
    "media_type",
    "record_id",
    "retrieval_status",
    "retrieval_urls",
    "retrieved_at",
    "snapshot_bytes",
    "snapshot_path",
    "snapshot_sha256",
    "source_id",
    "uri",
}
BINDING_FIELDS = {
    "applicability",
    "case_id",
    "evidence_role",
    "record_id",
    "source_id",
}


def _exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{context} keys differ; missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )


def _selection_surface(
    selection: dict[str, Any],
) -> tuple[list[dict[str, str]], dict[tuple[str, str], dict[str, str]]]:
    bindings: list[dict[str, str]] = []
    records: dict[tuple[str, str], dict[str, str]] = {}
    for case in selection["follow_on_cases"]:
        for handle in case["source_handles"]:
            binding = {
                "case_id": case["case_id"],
                "source_id": handle["source_id"],
                "record_id": handle["record_id"],
                "evidence_role": handle["evidence_role"],
                "applicability": handle["applicability"],
            }
            bindings.append(binding)
            key = handle["source_id"], handle["record_id"]
            identity = {
                "source_id": handle["source_id"],
                "record_id": handle["record_id"],
                "uri": handle["uri"],
            }
            previous = records.setdefault(key, identity)
            if previous != identity:
                raise ValueError(f"selection reuses {key} with conflicting record identity")
    return bindings, records


def _manifest_set_digest(records: list[dict[str, Any]]) -> str:
    identity = [
        {
            "record_id": record["record_id"],
            "retrieval_status": record["retrieval_status"],
            "snapshot_sha256": record["snapshot_sha256"],
            "source_id": record["source_id"],
        }
        for record in sorted(records, key=lambda item: (item["source_id"], item["record_id"]))
    ]
    raw = json.dumps(identity, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _validate_gap_snapshot(path: Path, record_id: str) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("source") != "Rhea" or value.get("record_id") != record_id:
        raise ValueError(f"Rhea source-gap snapshot identity differs for {record_id}")
    if value.get("query_result_kind") != "documented_zero_row_query":
        raise ValueError(f"Rhea source-gap snapshot is not marked zero-row for {record_id}")
    if value.get("rows") != []:
        raise ValueError(f"Rhea source-gap snapshot contains result rows for {record_id}")
    if value.get("participant_rows") != [] or value.get("participant_request_url") is not None:
        raise ValueError(f"Rhea source-gap snapshot cannot contain participants for {record_id}")
    if value.get("query") != record_id.lower():
        raise ValueError(f"Rhea source-gap query differs from {record_id}")


def _validate_rhea_direct_snapshot(path: Path, record_id: str) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("source") != "Rhea" or value.get("record_id") != record_id:
        raise ValueError(f"Rhea direct snapshot identity differs for {record_id}")
    if value.get("query_result_kind") != "direct_record":
        raise ValueError(f"Rhea direct snapshot status differs for {record_id}")
    rows = value.get("rows")
    if (
        not isinstance(rows, list)
        or len(rows) != 1
        or rows[0].get("Reaction identifier") != record_id
    ):
        raise ValueError(f"Rhea direct TSV row differs for {record_id}")
    participant_rows = value.get("participant_rows")
    if not isinstance(participant_rows, list) or len(participant_rows) < 2:
        raise ValueError(f"Rhea direct RDF participants are missing for {record_id}")
    expected_uri = "http://rdf.rhea-db.org/" + record_id.split(":", 1)[1]
    if any(item.get("reaction_uri") != expected_uri for item in participant_rows):
        raise ValueError(f"Rhea direct RDF participant identity differs for {record_id}")
    if not isinstance(value.get("participant_request_url"), str):
        raise ValueError(f"Rhea direct RDF request URL is missing for {record_id}")
    if record_id == "RHEA:16237":
        observed = {
            (item.get("accession"), item.get("reactive_chebi_uri"))
            for item in participant_rows
        }
        expected = {
            ("GENERIC:10747", "http://purl.obolibrary.org/obo/CHEBI_83833"),
            ("GENERIC:10748", "http://purl.obolibrary.org/obo/CHEBI_83834"),
        }
        if observed != expected:
            raise ValueError("RHEA:16237 macromolecule/reactive-part mapping differs")


def _validate_cath_snapshot(path: Path, record_id: str) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("source") != "CATH" or value.get("record_id") != record_id:
        raise ValueError(f"CATH snapshot identity differs for {record_id}")
    classification = record_id.removeprefix("CATH:")
    name_row = value.get("name_row")
    if not isinstance(name_row, dict) or name_row.get("classification_id") != classification:
        raise ValueError(f"CATH name row differs for {record_id}")
    selected_pdb_ids = value.get("selected_pdb_ids")
    domain_rows = value.get("domain_rows")
    if not isinstance(selected_pdb_ids, list) or not selected_pdb_ids:
        raise ValueError(f"CATH snapshot has no selected PDB scope for {record_id}")
    if not isinstance(domain_rows, list) or not domain_rows:
        raise ValueError(f"CATH snapshot has no matching domain rows for {record_id}")
    observed_pdb_ids: set[str] = set()
    for row in domain_rows:
        if not isinstance(row, dict) or row.get("classification_id") != classification:
            raise ValueError(f"CATH domain row differs for {record_id}")
        domain_id = row.get("domain_id")
        if not isinstance(domain_id, str) or len(domain_id) < 4:
            raise ValueError(f"CATH domain row lacks an identifier for {record_id}")
        observed_pdb_ids.add(domain_id[:4].upper())
    if set(selected_pdb_ids) - observed_pdb_ids:
        raise ValueError(f"CATH snapshot does not cover every selected PDB for {record_id}")


def _validate_mcsa_snapshot(path: Path, record_id: str) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("source") != "M-CSA" or value.get("record_id") != record_id:
        raise ValueError(f"M-CSA snapshot identity differs for {record_id}")
    entry = value.get("entry")
    if not isinstance(entry, dict) or entry.get("mcsa_id") != int(record_id[1:]):
        raise ValueError(f"M-CSA entry differs for {record_id}")
    mechanisms = entry.get("reaction", {}).get("mechanisms", [])
    expected_steps = {
        (mechanism.get("mechanism_id"), step.get("step_id")): step
        for mechanism in mechanisms
        if isinstance(mechanism, dict)
        for step in mechanism.get("steps", [])
        if isinstance(step, dict)
    }
    schemes = value.get("step_schemes")
    if not isinstance(schemes, list) or len(schemes) != len(expected_steps):
        raise ValueError(f"M-CSA scheme coverage differs for {record_id}")
    seen: set[tuple[int, int]] = set()
    for scheme in schemes:
        if not isinstance(scheme, dict):
            raise ValueError(f"M-CSA scheme must be an object for {record_id}")
        _exact_keys(
            scheme,
            {
                "content_sha256",
                "content_utf8",
                "is_product",
                "mechanism_id",
                "media_type",
                "http_status",
                "retrieval_status",
                "source_url",
                "step_id",
            },
            f"M-CSA {record_id} scheme",
        )
        key = scheme["mechanism_id"], scheme["step_id"]
        if key in seen or key not in expected_steps:
            raise ValueError(f"M-CSA scheme identity differs for {record_id}: {key}")
        seen.add(key)
        source_step = expected_steps[key]
        expected_url = "https://" + str(source_step.get("marvin_xml", "")).removeprefix(
            "https://"
        )
        if scheme["source_url"] != expected_url:
            raise ValueError(f"M-CSA scheme URL differs for {record_id}: {key}")
        if scheme["is_product"] is not source_step.get("is_product"):
            raise ValueError(f"M-CSA scheme product flag differs for {record_id}: {key}")
        content = scheme["content_utf8"]
        if scheme["retrieval_status"] == "bundled_linked_scheme":
            if scheme["http_status"] != 200:
                raise ValueError(f"M-CSA scheme HTTP status differs for {record_id}: {key}")
            if not isinstance(content, str) or not content.lstrip().startswith("<cml"):
                raise ValueError(f"M-CSA scheme content is invalid for {record_id}: {key}")
            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            if scheme["content_sha256"] != digest:
                raise ValueError(f"M-CSA scheme content hash differs for {record_id}: {key}")
        elif scheme["retrieval_status"] == "source_link_missing_http_404":
            if (
                record_id != "M0189"
                or key != (1, 1)
                or scheme["http_status"] != 404
                or content is not None
                or scheme["content_sha256"] is not None
            ):
                raise ValueError(f"unexpected missing M-CSA scheme for {record_id}: {key}")
            mechanism = next(
                item for item in mechanisms if item.get("mechanism_id") == key[0]
            )
            if mechanism.get("is_detailed") is not False:
                raise ValueError("a detailed M-CSA mechanism cannot lose its scheme silently")
        else:
            raise ValueError(f"unsupported M-CSA scheme retrieval status for {record_id}: {key}")
    if seen != set(expected_steps):
        raise ValueError(f"M-CSA scheme set differs for {record_id}")


def validate_atlas10_source_manifest(
    value: Any,
    *,
    repo_root: Path,
    selection: dict[str, Any],
) -> dict[str, int | str]:
    """Validate source identities, reuse, rights, hashes, gaps, and budgets."""
    if not isinstance(value, dict):
        raise ValueError("Atlas-10 source manifest must be an object")
    _exact_keys(
        value,
        {
            "acquisition",
            "bindings",
            "records",
            "retrieved_at",
            "rights_matrix_path",
            "schema_version",
            "selection_sha256",
            "snapshot_set_sha256",
        },
        "source_manifest",
    )
    if value["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported Atlas-10 source manifest: {value['schema_version']!r}")
    selection_summary = validate_atlas10_selection(selection)
    if value["selection_sha256"] != selection_summary["selection_sha256"]:
        raise ValueError("source manifest is not bound to the frozen Atlas-10 selection")
    if value["rights_matrix_path"] != "docs/SOURCE_DATA_RIGHTS.md":
        raise ValueError("source manifest must bind the checked source-rights matrix")
    retrieved_at = value["retrieved_at"]
    if not isinstance(retrieved_at, str) or not retrieved_at.endswith("Z"):
        raise ValueError("source manifest retrieved_at must be UTC")

    expected_bindings, expected_records = _selection_surface(selection)
    bindings = value["bindings"]
    if not isinstance(bindings, list) or len(bindings) != 45:
        raise ValueError("Atlas-10 source manifest must preserve all 45 case bindings")
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            raise ValueError(f"source_manifest.bindings[{index}] must be an object")
        _exact_keys(binding, BINDING_FIELDS, f"source_manifest.bindings[{index}]")
    if bindings != expected_bindings:
        raise ValueError("source manifest bindings differ from the frozen selection order")

    records = value["records"]
    if not isinstance(records, list) or len(records) != 44:
        raise ValueError("Atlas-10 source manifest must contain 44 unique source records")
    if records != sorted(records, key=lambda item: (item["source_id"], item["record_id"])):
        raise ValueError("Atlas-10 source records must be deterministically sorted")
    seen: set[tuple[str, str]] = set()
    bundled = 0
    reference_only = 0
    source_gaps = 0
    total_snapshot_bytes = 0
    for index, record in enumerate(records):
        context = f"source_manifest.records[{index}]"
        if not isinstance(record, dict):
            raise ValueError(f"{context} must be an object")
        _exact_keys(record, RECORD_FIELDS, context)
        key = record["source_id"], record["record_id"]
        if key in seen:
            raise ValueError(f"source manifest repeats unique record {key}")
        seen.add(key)
        expected = expected_records.get(key)
        if expected is None:
            raise ValueError(f"source manifest contains an unselected record: {key}")
        if record["uri"] != expected["uri"]:
            raise ValueError(f"{context}.uri differs from the frozen selection")
        if record["retrieved_at"] != retrieved_at:
            raise ValueError(f"{context}.retrieved_at differs from the manifest timestamp")
        if record["license"] != EXPECTED_LICENSES.get(record["source_id"]):
            raise ValueError(f"{context}.license differs from the checked rights policy")
        for field in ("attribution", "change_notice", "media_type"):
            if not isinstance(record[field], str) or not record[field].strip():
                raise ValueError(f"{context}.{field} must be a non-empty string")
        urls = record["retrieval_urls"]
        if (
            not isinstance(urls, list)
            or not urls
            or any(not isinstance(url, str) or not url.startswith("https://") for url in urls)
        ):
            raise ValueError(f"{context}.retrieval_urls must contain HTTPS URLs")

        if record["source_id"] in BUNDLED_SOURCES:
            expected_status = (
                "bundled_query_gap_snapshot"
                if record["source_id"] == "Rhea" and record["record_id"].startswith("EC:")
                else "bundled_snapshot"
            )
            if record["retrieval_status"] != expected_status:
                raise ValueError(f"{context}.retrieval_status differs from source semantics")
            relative = record["snapshot_path"]
            if not isinstance(relative, str) or not relative.startswith(SOURCE_ROOT):
                raise ValueError(f"{context}.snapshot_path escapes the Atlas-10 namespace")
            path = (repo_root / relative).resolve()
            source_root = (repo_root / SOURCE_ROOT).resolve()
            if source_root not in path.parents or not path.is_file():
                raise ValueError(f"{context}.snapshot_path is missing or outside source root")
            size = path.stat().st_size
            if record["snapshot_bytes"] != size or size <= 0:
                raise ValueError(f"{context}.snapshot_bytes differs from the local file")
            if record["snapshot_sha256"] != canonical_file_sha256(path):
                raise ValueError(f"{context}.snapshot_sha256 differs from the local file")
            if expected_status == "bundled_query_gap_snapshot":
                _validate_gap_snapshot(path, record["record_id"])
                source_gaps += 1
            elif record["source_id"] == "Rhea":
                _validate_rhea_direct_snapshot(path, record["record_id"])
            if record["source_id"] == "CATH":
                _validate_cath_snapshot(path, record["record_id"])
            if record["source_id"] == "M-CSA":
                _validate_mcsa_snapshot(path, record["record_id"])
            bundled += 1
            total_snapshot_bytes += size
        elif record["source_id"] in REFERENCE_ONLY_SOURCES:
            if record["retrieval_status"] != "reference_only_verified_handle":
                raise ValueError(f"{context} must remain a reference-only literature handle")
            if (
                record["snapshot_path"] is not None
                or record["snapshot_sha256"] is not None
                or record["snapshot_bytes"] != 0
            ):
                raise ValueError(f"{context} cannot bundle reference-only article content")
            reference_only += 1
        else:
            raise ValueError(f"{context}.source_id is unsupported")
    if seen != set(expected_records):
        raise ValueError("source manifest does not exactly cover the unique frozen records")
    if (bundled, reference_only, source_gaps) != (36, 8, 3):
        raise ValueError("Atlas-10 bundled/reference/source-gap counts differ")

    acquisition = value["acquisition"]
    if not isinstance(acquisition, dict):
        raise ValueError("source_manifest.acquisition must be an object")
    _exact_keys(
        acquisition,
        {
            "download_bytes_max",
            "download_bytes_used",
            "external_requests_max",
            "external_requests_used",
        },
        "source_manifest.acquisition",
    )
    budget = selection["phase_compute_budget"]
    if acquisition["download_bytes_max"] != budget["download_bytes_max"]:
        raise ValueError("source acquisition download ceiling differs from selection")
    if acquisition["external_requests_max"] != budget["external_requests_max"]:
        raise ValueError("source acquisition request ceiling differs from selection")
    requests_used = acquisition["external_requests_used"]
    download_bytes_used = acquisition["download_bytes_used"]
    if requests_used != 64 or requests_used > acquisition["external_requests_max"]:
        raise ValueError("source acquisition request count differs from the bounded plan")
    if (
        not isinstance(download_bytes_used, int)
        or download_bytes_used < total_snapshot_bytes
        or download_bytes_used > acquisition["download_bytes_max"]
    ):
        raise ValueError("source acquisition download bytes are invalid or over budget")

    digest = _manifest_set_digest(records)
    if value["snapshot_set_sha256"] != digest:
        raise ValueError("Atlas-10 source snapshot-set digest differs")
    return {
        "schema_version": SCHEMA_VERSION,
        "case_bindings": len(bindings),
        "unique_source_records": len(records),
        "bundled_snapshots": bundled,
        "reference_only_handles": reference_only,
        "documented_rhea_gaps": source_gaps,
        "external_requests_used": requests_used,
        "download_bytes_used": download_bytes_used,
        "snapshot_bytes": total_snapshot_bytes,
        "snapshot_set_sha256": digest,
    }


def load_atlas10_source_manifest(
    path: Path, *, repo_root: Path, selection: dict[str, Any]
) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    validate_atlas10_source_manifest(value, repo_root=repo_root, selection=selection)
    return value
