"""Validation and loading for source-scoped M-CSA draft snapshots.

The package keeps source acquisition separate from mechanism-state projection.  It
contains the exact M-CSA entry objects and every linked step scheme, plus the
development-gate controls that constrain later compilation.
"""

from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlsplit

from .atlas10_source_adapters import (
    parse_mcsa_scheme_flows,
    read_atlas10_mcsa_snapshot,
)
from .atlas50_development_gate import build_development_status, require_operation
from .canonical_hash import canonical_file_sha256


SCHEMA_VERSION = "catalytic-earth.atlas-source-draft-manifest.v1"
MANIFEST_PATH = Path("data/atlas/source_drafts/source_manifest.json")
SOURCE_ROOT = Path("data/atlas/source_drafts/sources")
ATTRIBUTION_PATH = Path("data/atlas/source_drafts/SOURCE_ATTRIBUTION.md")
RIGHTS_MATRIX_PATH = Path("docs/SOURCE_DATA_RIGHTS.md")
DEVELOPMENT_STATUS_PATH = Path("data/atlas/atlas50/development_gate/status.json")
MCSA_ORIGIN = "https://www.ebi.ac.uk"
MCSA_ENTRY_API = f"{MCSA_ORIGIN}/thornton-srv/m-csa/api/entries/"
MCSA_SCHEME_PREFIX = f"{MCSA_ORIGIN}/thornton-srv/m-csa/media/schemes/"
MCSA_ENTRY_TEMPLATE = f"{MCSA_ORIGIN}/thornton-srv/m-csa/entry/{{mcsa_id}}/"
EXPECTED_LICENSE = "CC BY 4.0"
EXPECTED_ATTRIBUTION = (
    "Credit M-CSA and cite Ribeiro et al. together with each accessed entry."
)
EXPECTED_CHANGE_NOTICE = (
    "Official API entry objects and linked Marvin step schemes are wrapped in "
    "deterministically sorted UTF-8 JSON; source text, identifiers, alternatives, "
    "step order, terminal flags, scheme content, and retrieval status are retained."
)
BOUNDARIES = {
    "exact_reaction_instance_established": False,
    "gold_admission_permitted": False,
    "independent_validation_established": False,
    "protected_registry_modified": False,
    "raw_source_and_gate_controls_only": True,
}

MANIFEST_FIELDS = {
    "acquisition",
    "boundaries",
    "development_gate",
    "records",
    "retrieved_at",
    "rights",
    "schema_version",
    "selection",
    "snapshot_set_sha256",
    "source",
}
RECORD_FIELDS = {
    "attribution",
    "change_notice",
    "entry_response_sha256",
    "license",
    "probe_identity",
    "record_id",
    "retrieval_status",
    "retrieved_at",
    "scheme_status_counts",
    "snapshot_bytes",
    "snapshot_path",
    "snapshot_sha256",
    "source_id",
    "uri",
}
SCHEME_FIELDS = {
    "content_sha256",
    "content_utf8",
    "electron_flow_count",
    "flow_parse_error",
    "flow_parse_status",
    "http_status",
    "is_product",
    "mechanism_id",
    "media_type",
    "retrieval_status",
    "source_url",
    "step_id",
}
RECEIPT_FIELDS = {
    "http_status",
    "mechanism_id",
    "record_ids",
    "request_index",
    "request_kind",
    "response_bytes",
    "response_sha256",
    "retrieval_status",
    "source_url",
    "step_id",
}
CASE_CONTROL_FIELDS = {
    "allowed_operations",
    "challenge_claim_ids",
    "evidence_ids",
    "mandatory_abstentions",
    "open_objections",
    "record_id",
    "scope",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    _require(
        actual == expected,
        f"{context} keys differ; missing={sorted(expected - actual)}, "
        f"extra={sorted(actual - expected)}",
    )


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"JSON document must be an object: {path}")
    return value


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def build_entry_request_url(record_ids: list[str] | tuple[str, ...]) -> str:
    """Build one official filtered M-CSA API request for an explicit ID set."""
    _validate_record_ids(record_ids)
    numeric = ",".join(str(int(record_id[1:])) for record_id in record_ids)
    return MCSA_ENTRY_API + "?" + urlencode(
        {"format": "json", "entries.mcsa_ids": numeric}
    )


def _validate_record_ids(record_ids: Any) -> tuple[str, ...]:
    _require(isinstance(record_ids, (list, tuple)), "record_ids must be an array")
    ids = tuple(record_ids)
    _require(bool(ids), "record_ids must not be empty")
    _require(
        all(isinstance(item, str) and re.fullmatch(r"M\d{4}", item) for item in ids),
        "record_ids must contain canonical four-digit M-CSA identifiers",
    )
    _require(ids == tuple(sorted(set(ids))), "record_ids must be unique and sorted")
    return ids


def validate_official_mcsa_url(url: str, *, kind: str) -> None:
    """Reject redirects or source-provided links outside the official M-CSA paths."""
    parsed = urlsplit(url)
    _require(
        parsed.scheme == "https"
        and parsed.netloc == "www.ebi.ac.uk"
        and parsed.username is None
        and parsed.password is None
        and not parsed.fragment,
        f"non-official M-CSA URL rejected: {url}",
    )
    if kind == "entry_batch":
        _require(url.startswith(MCSA_ENTRY_API + "?"), "M-CSA entry API URL differs")
    elif kind == "step_scheme":
        _require(
            url.startswith(MCSA_SCHEME_PREFIX)
            and parsed.path.endswith(".mrv")
            and not parsed.query,
            f"M-CSA step-scheme URL differs: {url}",
        )
    else:
        raise ValueError(f"unsupported M-CSA request kind: {kind}")


def scheme_url_from_step(step: dict[str, Any]) -> str:
    raw = step.get("marvin_xml")
    _require(isinstance(raw, str) and raw, "M-CSA step lacks a Marvin scheme URL")
    url = "https://" + raw.removeprefix("https://")
    validate_official_mcsa_url(url, kind="step_scheme")
    return url


def _case_control(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_id": row["mcsa_id"],
        "allowed_operations": row["allowed_operations"],
        "scope": row["scope"],
        "mandatory_abstentions": row["mandatory_abstentions"],
        "open_objections": row["open_objections"],
        "challenge_claim_ids": row["challenge_claim_ids"],
        "evidence_ids": row["evidence_ids"],
    }


def default_draft_record_ids(repo_root: Path) -> tuple[str, ...]:
    """Derive the default batch from current mechanism-draft permissions."""
    status = build_development_status(Path(repo_root))
    return tuple(
        sorted(
            row["mcsa_id"]
            for row in status["cases"]
            if "source_scoped_mechanism_draft" in row["allowed_operations"]
        )
    )


def probe_identity(entry: dict[str, Any]) -> dict[str, Any]:
    mcsa_id = entry.get("mcsa_id")
    _require(
        isinstance(mcsa_id, int) and not isinstance(mcsa_id, bool) and mcsa_id > 0,
        "M-CSA entry identifier is invalid",
    )
    raw_entry_url = entry.get("url")
    _require(isinstance(raw_entry_url, str) and raw_entry_url, "M-CSA entry URL is missing")
    source_entry_url = "https://" + raw_entry_url.removeprefix("https://")
    expected_entry_url = MCSA_ENTRY_TEMPLATE.format(mcsa_id=mcsa_id)
    _require(source_entry_url == expected_entry_url, "M-CSA entry URL differs from its identity")
    mechanisms = entry.get("reaction", {}).get("mechanisms")
    _require(isinstance(mechanisms, list) and mechanisms, "M-CSA mechanisms are missing")
    mechanism_steps: list[dict[str, Any]] = []
    terminal_keys: list[dict[str, int]] = []
    seen_mechanisms: set[int] = set()
    step_count = 0
    for mechanism in mechanisms:
        _require(isinstance(mechanism, dict), "M-CSA mechanism must be an object")
        mechanism_id = mechanism.get("mechanism_id")
        _require(
            isinstance(mechanism_id, int)
            and not isinstance(mechanism_id, bool)
            and mechanism_id > 0
            and mechanism_id not in seen_mechanisms,
            "M-CSA mechanism identifiers must be unique positive integers",
        )
        seen_mechanisms.add(mechanism_id)
        steps = mechanism.get("steps")
        _require(isinstance(steps, list) and steps, "M-CSA mechanism steps are missing")
        step_ids: list[int] = []
        for step in steps:
            _require(isinstance(step, dict), "M-CSA step must be an object")
            step_id = step.get("step_id")
            _require(
                isinstance(step_id, int)
                and not isinstance(step_id, bool)
                and step_id > 0
                and step_id not in step_ids,
                "M-CSA step identifiers must be unique positive integers per mechanism",
            )
            _require(isinstance(step.get("description"), str), "M-CSA step lacks text")
            _require(type(step.get("is_product")) is bool, "M-CSA step lacks terminal flag")
            scheme_url_from_step(step)
            step_ids.append(step_id)
            if step["is_product"]:
                terminal_keys.append({"mechanism_id": mechanism_id, "step_id": step_id})
        _require(step_ids == sorted(step_ids), "M-CSA source steps are not ordered by step_id")
        _require(
            any(step.get("is_product") is True for step in steps),
            f"M-CSA mechanism {mechanism_id} lacks a terminal source step",
        )
        mechanism_steps.append(
            {"mechanism_id": mechanism_id, "step_ids": step_ids}
        )
        step_count += len(step_ids)
    _require(
        [item["mechanism_id"] for item in mechanism_steps]
        == sorted(seen_mechanisms),
        "M-CSA mechanisms are not deterministically ordered",
    )
    return {
        "mcsa_id": mcsa_id,
        "source_entry_url": source_entry_url,
        "mechanism_ids": sorted(seen_mechanisms),
        "mechanism_step_ids": mechanism_steps,
        "source_step_count": step_count,
        "terminal_source_step_keys": terminal_keys,
    }


def _scheme_status_counts(schemes: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(item["retrieval_status"] for item in schemes).items()))


def scheme_flow_parse_receipt(scheme: dict[str, Any]) -> dict[str, Any]:
    """Report whether the existing conservative arrow parser can read a scheme.

    Unsupported source syntax is an explicit abstention.  The raw scheme and source
    step remain usable evidence and are never rewritten to make parsing succeed.
    """
    if scheme.get("content_utf8") is None:
        return {
            "flow_parse_status": "source_scheme_unavailable",
            "flow_parse_error": None,
            "electron_flow_count": None,
        }
    try:
        parsed = parse_mcsa_scheme_flows(scheme)
    except (ValueError, ET.ParseError) as exc:
        return {
            "flow_parse_status": "source_flow_parse_abstention",
            "flow_parse_error": f"{type(exc).__name__}: {exc}",
            "electron_flow_count": None,
        }
    return {
        "flow_parse_status": parsed["scheme_status"],
        "flow_parse_error": None,
        "electron_flow_count": len(parsed["electron_flows"]),
    }


def _snapshot_set_digest(records: list[dict[str, Any]]) -> str:
    identity = [
        {
            "record_id": record["record_id"],
            "retrieval_status": record["retrieval_status"],
            "snapshot_sha256": record["snapshot_sha256"],
            "source_id": record["source_id"],
        }
        for record in records
    ]
    raw = json.dumps(identity, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return _sha256(raw)


def _expected_case_controls(
    status: dict[str, Any], record_ids: tuple[str, ...]
) -> list[dict[str, Any]]:
    by_id = {row["mcsa_id"]: row for row in status["cases"]}
    _require(set(record_ids) <= set(by_id), "selection contains a case outside the gate")
    return [_case_control(by_id[record_id]) for record_id in record_ids]


def _validate_scheme(
    scheme: dict[str, Any],
    *,
    source_step: dict[str, Any],
    context: str,
) -> None:
    _exact_keys(scheme, SCHEME_FIELDS, context)
    _require(
        scheme["source_url"] == scheme_url_from_step(source_step),
        f"{context}.source_url differs from the source entry",
    )
    _require(
        scheme["is_product"] is source_step["is_product"],
        f"{context}.is_product differs from the source entry",
    )
    _require(
        scheme["media_type"] == "chemical/x-mdl-molfile+xml",
        f"{context}.media_type differs",
    )
    status = scheme["retrieval_status"]
    content = scheme["content_utf8"]
    if status == "bundled_linked_scheme":
        _require(scheme["http_status"] == 200, f"{context} success status differs")
        _require(
            isinstance(content, str) and content.lstrip().startswith("<cml"),
            f"{context} does not contain Marvin CML",
        )
        _require(
            scheme["content_sha256"] == _sha256(content.encode("utf-8")),
            f"{context} content hash differs",
        )
    elif status == "source_link_missing_http_404":
        _require(scheme["http_status"] == 404, f"{context} missing status differs")
        _require(
            content is None and scheme["content_sha256"] is None,
            f"{context} missing scheme must not invent content",
        )
    elif status == "source_link_http_error":
        _require(
            isinstance(scheme["http_status"], int) and scheme["http_status"] >= 400,
            f"{context} HTTP error status differs",
        )
        _require(
            content is None and scheme["content_sha256"] is None,
            f"{context} HTTP error must not invent scheme content",
        )
    else:
        raise ValueError(f"{context} has unsupported retrieval status: {status!r}")
    expected_parse_receipt = scheme_flow_parse_receipt(scheme)
    _require(
        {
            "flow_parse_status": scheme["flow_parse_status"],
            "flow_parse_error": scheme["flow_parse_error"],
            "electron_flow_count": scheme["electron_flow_count"],
        }
        == expected_parse_receipt,
        f"{context} flow-parse receipt differs",
    )


def render_source_attribution(manifest: dict[str, Any]) -> str:
    ids = ", ".join(manifest["selection"]["record_ids"])
    acquisition = manifest["acquisition"]
    entry_links = "".join(
        f"- [{record['record_id']}]({record['uri']})\n"
        for record in manifest["records"]
    )
    return (
        "# M-CSA source-draft attribution and boundary\n\n"
        f"This source package contains official M-CSA records {ids}, retrieved at "
        f"`{manifest['retrieved_at']}`. It preserves all source mechanisms, ordered "
        "steps, terminal steps, linked Marvin schemes, and per-response retrieval "
        "status. The manifest binds every snapshot and response with SHA-256.\n\n"
        "M-CSA content is used under [CC BY 4.0]"
        "(https://creativecommons.org/licenses/by/4.0/). Credit M-CSA and cite "
        "each accessed entry:\n\n"
        f"{entry_links}\n"
        "Database citation: Ribeiro AJM, Holliday GL, Furnham N, Tyzack JD, "
        "Ferris K, Thornton JM. [Mechanism and Catalytic Site Atlas (M-CSA): a "
        "database of enzyme reaction mechanisms and active sites]"
        "(https://doi.org/10.1093/nar/gkx1012). *Nucleic Acids Research* "
        "46(D1):D618-D623 (2018).\n\n"
        "The wrapped JSON is a project transformation described by the manifest "
        "change notice.\n\n"
        f"The acquisition used {acquisition['external_requests_used']} of "
        f"{acquisition['external_requests_max']} permitted requests and "
        f"{acquisition['download_bytes_used']} of "
        f"{acquisition['download_bytes_max']} permitted bytes.\n\n"
        "These are source-scoped draft inputs. They establish no exact reaction "
        "instance, independent validation, gold admission, or protected-registry "
        "change. The development-gate controls in the manifest retain each source "
        "scope, objection, and mandatory abstention.\n"
    )


def validate_atlas_draft_source_manifest(
    value: Any, *, repo_root: Path
) -> dict[str, Any]:
    """Validate source identity, full step coverage, rights, receipts, and budgets."""
    root = Path(repo_root)
    _require(isinstance(value, dict), "source-draft manifest must be an object")
    _exact_keys(value, MANIFEST_FIELDS, "source-draft manifest")
    _require(value["schema_version"] == SCHEMA_VERSION, "unsupported source-draft manifest")

    selection = value["selection"]
    _require(isinstance(selection, dict), "selection must be an object")
    _exact_keys(selection, {"basis", "record_ids", "requested_operation"}, "selection")
    record_ids = _validate_record_ids(selection["record_ids"])
    _require(
        selection["basis"]
        in {"development_gate_default_mechanism_draft_cases", "explicit_record_ids"},
        "unsupported source-draft selection basis",
    )
    _require(
        selection["requested_operation"]
        in {"source_annotation", "source_scoped_mechanism_draft"},
        "unsupported source-draft requested operation",
    )
    if selection["basis"] == "development_gate_default_mechanism_draft_cases":
        _require(
            record_ids == default_draft_record_ids(root),
            "default source-draft selection differs from the current gate",
        )
        _require(
            selection["requested_operation"] == "source_scoped_mechanism_draft",
            "default source-draft selection operation differs",
        )
    for record_id in record_ids:
        require_operation(root, "source_annotation", record_id)

    retrieved_at = value["retrieved_at"]
    _require(
        isinstance(retrieved_at, str)
        and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", retrieved_at)),
        "retrieved_at must be an explicit UTC timestamp",
    )

    source = value["source"]
    _require(isinstance(source, dict), "source must be an object")
    _exact_keys(
        source,
        {"allowed_https_origin", "allowed_scheme_path_prefix", "entry_request_url", "source_id"},
        "source",
    )
    _require(
        source
        == {
            "source_id": "M-CSA",
            "entry_request_url": build_entry_request_url(record_ids),
            "allowed_https_origin": MCSA_ORIGIN,
            "allowed_scheme_path_prefix": "/thornton-srv/m-csa/media/schemes/",
        },
        "source identity or official URL boundary differs",
    )
    validate_official_mcsa_url(source["entry_request_url"], kind="entry_batch")

    status = build_development_status(root)
    status_path = root / DEVELOPMENT_STATUS_PATH
    _require(status_path.is_file(), "generated development status is missing")
    _require(_load_json(status_path) == status, "generated development status is stale")
    development_gate = value["development_gate"]
    _require(isinstance(development_gate, dict), "development_gate must be an object")
    _exact_keys(
        development_gate,
        {"authorization_operation", "case_controls", "status_path", "status_sha256"},
        "development_gate",
    )
    _require(
        development_gate["authorization_operation"] == "source_annotation",
        "source acquisition must be authorized as source_annotation",
    )
    _require(
        development_gate["status_path"] == DEVELOPMENT_STATUS_PATH.as_posix()
        and development_gate["status_sha256"] == canonical_file_sha256(status_path),
        "development-gate status binding differs",
    )
    controls = development_gate["case_controls"]
    expected_controls = _expected_case_controls(status, record_ids)
    _require(controls == expected_controls, "development-gate case controls differ")
    for index, control in enumerate(controls):
        _require(isinstance(control, dict), f"case_controls[{index}] must be an object")
        _exact_keys(control, CASE_CONTROL_FIELDS, f"case_controls[{index}]")

    rights = value["rights"]
    _require(isinstance(rights, dict), "rights must be an object")
    _exact_keys(
        rights,
        {"attribution", "change_notice", "license", "rights_matrix_path", "rights_matrix_sha256"},
        "rights",
    )
    rights_path = root / RIGHTS_MATRIX_PATH
    _require(
        rights
        == {
            "license": EXPECTED_LICENSE,
            "attribution": EXPECTED_ATTRIBUTION,
            "change_notice": EXPECTED_CHANGE_NOTICE,
            "rights_matrix_path": RIGHTS_MATRIX_PATH.as_posix(),
            "rights_matrix_sha256": canonical_file_sha256(rights_path),
        },
        "M-CSA rights or attribution binding differs",
    )
    _require(value["boundaries"] == BOUNDARIES, "source-draft boundary claims differ")

    records = value["records"]
    _require(isinstance(records, list), "records must be an array")
    _require(
        [record.get("record_id") for record in records] == list(record_ids),
        "records must exactly match the explicit selection order",
    )
    parsed_entries: dict[str, dict[str, Any]] = {}
    source_step_keys: dict[tuple[str, int, int], dict[str, Any]] = {}
    entry_response_hashes: set[str] = set()
    for index, record in enumerate(records):
        context = f"records[{index}]"
        _require(isinstance(record, dict), f"{context} must be an object")
        _exact_keys(record, RECORD_FIELDS, context)
        record_id = record["record_id"]
        expected_path = (SOURCE_ROOT / f"{record_id}.json").as_posix()
        expected_uri = MCSA_ENTRY_TEMPLATE.format(mcsa_id=int(record_id[1:]))
        _require(
            record["source_id"] == "M-CSA"
            and record["uri"] == expected_uri
            and record["retrieval_status"] == "bundled_source_scoped_snapshot"
            and record["snapshot_path"] == expected_path,
            f"{context} source identity differs",
        )
        _require(record["retrieved_at"] == retrieved_at, f"{context} timestamp differs")
        _require(
            record["license"] == EXPECTED_LICENSE
            and record["attribution"] == EXPECTED_ATTRIBUTION
            and record["change_notice"] == EXPECTED_CHANGE_NOTICE,
            f"{context} rights fields differ",
        )
        path = (root / expected_path).resolve()
        source_root = (root / SOURCE_ROOT).resolve()
        _require(source_root in path.parents and path.is_file(), f"{context} snapshot is missing")
        _require(
            record["snapshot_bytes"] == path.stat().st_size
            and record["snapshot_bytes"] > 0,
            f"{context} snapshot byte count differs",
        )
        _require(
            record["snapshot_sha256"] == canonical_file_sha256(path),
            f"{context} snapshot hash differs",
        )
        entry = read_atlas10_mcsa_snapshot(path, record_id)
        parsed_entries[record_id] = entry
        raw_snapshot = _load_json(path)
        source_entry = raw_snapshot["entry"]
        identity = probe_identity(source_entry)
        _require(identity["mcsa_id"] == int(record_id[1:]), f"{context} API identity differs")
        _require(record["probe_identity"] == identity, f"{context} probe identity differs")
        schemes = raw_snapshot["step_schemes"]
        _require(
            record["scheme_status_counts"] == _scheme_status_counts(schemes),
            f"{context} scheme status counts differ",
        )
        expected_steps = {
            (mechanism["mechanism_id"], step["step_id"]): step
            for mechanism in source_entry["reaction"]["mechanisms"]
            for step in mechanism["steps"]
        }
        observed_keys: set[tuple[int, int]] = set()
        for scheme_index, scheme in enumerate(schemes):
            _require(isinstance(scheme, dict), f"{context}.schemes[{scheme_index}] must be an object")
            key = (scheme.get("mechanism_id"), scheme.get("step_id"))
            _require(key in expected_steps and key not in observed_keys, f"{context} scheme identity differs")
            observed_keys.add(key)
            _validate_scheme(
                scheme,
                source_step=expected_steps[key],
                context=f"{context}.schemes[{scheme_index}]",
            )
            source_step_keys[(record_id, key[0], key[1])] = scheme
        _require(observed_keys == set(expected_steps), f"{context} does not preserve every source step")
        entry_hash = record["entry_response_sha256"]
        _require(
            isinstance(entry_hash, str) and bool(re.fullmatch(r"[a-f0-9]{64}", entry_hash)),
            f"{context}.entry_response_sha256 is invalid",
        )
        entry_response_hashes.add(entry_hash)

    _require(
        value["snapshot_set_sha256"] == _snapshot_set_digest(records),
        "snapshot-set digest differs",
    )

    acquisition = value["acquisition"]
    _require(isinstance(acquisition, dict), "acquisition must be an object")
    _exact_keys(
        acquisition,
        {
            "download_bytes_max",
            "download_bytes_used",
            "external_requests_expected",
            "external_requests_max",
            "external_requests_used",
            "responses",
        },
        "acquisition",
    )
    access = status["source_access"]
    _require(
        acquisition["external_requests_max"] == access["maximum_requests_per_batch"]
        and acquisition["download_bytes_max"] == access["maximum_download_bytes_per_batch"],
        "acquisition limits differ from the development gate",
    )
    expected_requests = 1 + len(source_step_keys)
    _require(
        acquisition["external_requests_expected"] == expected_requests
        and acquisition["external_requests_used"] == expected_requests
        and expected_requests <= acquisition["external_requests_max"],
        "acquisition request accounting differs from the source step set",
    )
    receipts = acquisition["responses"]
    _require(
        isinstance(receipts, list) and len(receipts) == expected_requests,
        "acquisition response receipts are incomplete",
    )
    _require(
        [receipt.get("request_index") for receipt in receipts]
        == list(range(1, expected_requests + 1)),
        "acquisition response receipt order differs",
    )
    _require(
        acquisition["download_bytes_used"]
        == sum(receipt.get("response_bytes", -1) for receipt in receipts)
        <= acquisition["download_bytes_max"],
        "acquisition byte accounting differs or exceeds the gate",
    )
    entry_receipts = []
    scheme_receipt_keys: set[tuple[str, int, int]] = set()
    for index, receipt in enumerate(receipts):
        context = f"acquisition.responses[{index}]"
        _require(isinstance(receipt, dict), f"{context} must be an object")
        _exact_keys(receipt, RECEIPT_FIELDS, context)
        _require(
            isinstance(receipt["response_bytes"], int) and receipt["response_bytes"] >= 0,
            f"{context}.response_bytes is invalid",
        )
        _require(
            isinstance(receipt["response_sha256"], str)
            and bool(re.fullmatch(r"[a-f0-9]{64}", receipt["response_sha256"])),
            f"{context}.response_sha256 is invalid",
        )
        request_kind = receipt["request_kind"]
        validate_official_mcsa_url(receipt["source_url"], kind=request_kind)
        if request_kind == "entry_batch":
            entry_receipts.append(receipt)
            _require(
                receipt["record_ids"] == list(record_ids)
                and receipt["mechanism_id"] is None
                and receipt["step_id"] is None
                and receipt["http_status"] == 200
                and receipt["retrieval_status"]
                in {"source_response_downloaded", "provided_source_response_reused"},
                f"{context} entry receipt differs",
            )
        else:
            ids = receipt["record_ids"]
            _require(isinstance(ids, list) and len(ids) == 1, f"{context} scheme scope differs")
            key = (ids[0], receipt["mechanism_id"], receipt["step_id"])
            _require(key in source_step_keys and key not in scheme_receipt_keys, f"{context} scheme key differs")
            scheme_receipt_keys.add(key)
            scheme = source_step_keys[key]
            _require(receipt["source_url"] == scheme["source_url"], f"{context} URL differs")
            _require(receipt["http_status"] == scheme["http_status"], f"{context} HTTP status differs")
            _require(
                receipt["retrieval_status"] == scheme["retrieval_status"],
                f"{context} retrieval status differs",
            )
            if scheme["content_utf8"] is not None:
                _require(
                    receipt["response_sha256"] == scheme["content_sha256"]
                    and receipt["response_bytes"]
                    == len(scheme["content_utf8"].encode("utf-8")),
                    f"{context} response receipt differs from bundled scheme",
                )
    _require(len(entry_receipts) == 1, "exactly one entry-batch receipt is required")
    _require(
        entry_receipts[0]["source_url"] == source["entry_request_url"]
        and entry_receipts[0]["response_sha256"] in entry_response_hashes
        and entry_response_hashes == {entry_receipts[0]["response_sha256"]},
        "entry-batch response binding differs",
    )
    _require(scheme_receipt_keys == set(source_step_keys), "scheme response receipts are incomplete")

    attribution_path = root / ATTRIBUTION_PATH
    _require(attribution_path.is_file(), "source-draft attribution file is missing")
    _require(
        attribution_path.read_text(encoding="utf-8") == render_source_attribution(value),
        "source-draft attribution file differs from the manifest",
    )
    return {
        "record_ids": list(record_ids),
        "source_records": len(records),
        "mechanisms": sum(len(entry["mechanisms"]) for entry in parsed_entries.values()),
        "source_steps": len(source_step_keys),
        "external_requests_used": acquisition["external_requests_used"],
        "download_bytes_used": acquisition["download_bytes_used"],
        "snapshot_set_sha256": value["snapshot_set_sha256"],
    }


def load_draft_sources(
    repo_root: Path,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Load and fail-closed validate the selected M-CSA source-draft package."""
    root = Path(repo_root)
    manifest = _load_json(root / MANIFEST_PATH)
    validate_atlas_draft_source_manifest(manifest, repo_root=root)
    entries = {
        record_id: read_atlas10_mcsa_snapshot(
            root / SOURCE_ROOT / f"{record_id}.json", record_id
        )
        for record_id in manifest["selection"]["record_ids"]
    }
    return manifest, entries
