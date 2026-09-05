"""Fetch or offline-verify the bounded M-CSA source-draft package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO
from urllib.error import HTTPError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas50_development_gate import (  # noqa: E402
    build_development_status,
    require_operation,
)
from catalytic_earth.atlas_draft_sources import (  # noqa: E402
    ATTRIBUTION_PATH,
    BOUNDARIES,
    DEVELOPMENT_STATUS_PATH,
    EXPECTED_ATTRIBUTION,
    EXPECTED_CHANGE_NOTICE,
    EXPECTED_LICENSE,
    MANIFEST_PATH,
    RIGHTS_MATRIX_PATH,
    SCHEMA_VERSION,
    SOURCE_ROOT,
    build_entry_request_url,
    default_draft_record_ids,
    probe_identity,
    render_source_attribution,
    scheme_flow_parse_receipt,
    scheme_url_from_step,
    validate_atlas_draft_source_manifest,
    validate_official_mcsa_url,
)
from catalytic_earth.canonical_hash import canonical_file_sha256  # noqa: E402


USER_AGENT = "CatalyticEarth/0.1 source-scoped M-CSA drafts"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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
    return _sha256(
        json.dumps(identity, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )


@dataclass
class AcquisitionMeter:
    requests_max: int
    download_bytes_max: int
    responses: list[dict[str, Any]] = field(default_factory=list)
    download_bytes_used: int = 0

    @property
    def requests_used(self) -> int:
        return len(self.responses)

    def ensure_request_capacity(self, additional_requests: int) -> None:
        if additional_requests < 0:
            raise ValueError("additional request count cannot be negative")
        if self.requests_used + additional_requests > self.requests_max:
            raise ValueError(
                "M-CSA acquisition would exceed the development-gate request budget"
            )

    def _read_bounded(self, stream: BinaryIO, content_length: str | None) -> bytes:
        remaining = self.download_bytes_max - self.download_bytes_used
        if remaining < 0:
            raise ValueError("M-CSA acquisition byte budget was already exceeded")
        if content_length is not None:
            try:
                declared = int(content_length)
            except ValueError:
                declared = None
            if declared is not None and declared > remaining:
                raise ValueError(
                    "M-CSA response Content-Length exceeds the remaining byte budget"
                )
        raw = stream.read(remaining + 1)
        if len(raw) > remaining:
            raise ValueError("M-CSA acquisition exceeded the byte budget during a read")
        return raw

    def _append(
        self,
        *,
        url: str,
        request_kind: str,
        record_ids: list[str],
        mechanism_id: int | None,
        step_id: int | None,
        http_status: int,
        raw: bytes,
        retrieval_status: str,
    ) -> dict[str, Any]:
        if self.download_bytes_used + len(raw) > self.download_bytes_max:
            raise ValueError("M-CSA acquisition would exceed the byte budget")
        self.download_bytes_used += len(raw)
        receipt = {
            "request_index": self.requests_used + 1,
            "request_kind": request_kind,
            "source_url": url,
            "record_ids": record_ids,
            "mechanism_id": mechanism_id,
            "step_id": step_id,
            "http_status": http_status,
            "response_bytes": len(raw),
            "response_sha256": _sha256(raw),
            "retrieval_status": retrieval_status,
        }
        self.responses.append(receipt)
        return receipt

    def register_provided_entry_response(
        self, url: str, record_ids: list[str], raw: bytes
    ) -> dict[str, Any]:
        self.ensure_request_capacity(1)
        validate_official_mcsa_url(url, kind="entry_batch")
        return self._append(
            url=url,
            request_kind="entry_batch",
            record_ids=record_ids,
            mechanism_id=None,
            step_id=None,
            http_status=200,
            raw=raw,
            retrieval_status="provided_source_response_reused",
        )

    def fetch(
        self,
        url: str,
        *,
        request_kind: str,
        record_ids: list[str],
        mechanism_id: int | None,
        step_id: int | None,
    ) -> tuple[int, bytes, dict[str, Any]]:
        self.ensure_request_capacity(1)
        validate_official_mcsa_url(url, kind=request_kind)
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urlopen(request, timeout=90) as response:
                http_status = int(response.status)
                raw = self._read_bounded(response, response.headers.get("Content-Length"))
        except HTTPError as exc:
            http_status = exc.code
            raw = self._read_bounded(exc, exc.headers.get("Content-Length"))
        if request_kind == "entry_batch":
            retrieval_status = "source_response_downloaded"
        elif http_status == 200:
            retrieval_status = "bundled_linked_scheme"
        elif http_status == 404:
            retrieval_status = "source_link_missing_http_404"
        else:
            retrieval_status = "source_link_http_error"
        receipt = self._append(
            url=url,
            request_kind=request_kind,
            record_ids=record_ids,
            mechanism_id=mechanism_id,
            step_id=step_id,
            http_status=http_status,
            raw=raw,
            retrieval_status=retrieval_status,
        )
        return http_status, raw, receipt


def _parse_ids(raw: str) -> tuple[str, ...]:
    values = [item.strip().upper() for item in raw.split(",") if item.strip()]
    if not values or any(not re.fullmatch(r"M\d{4}", item) for item in values):
        raise ValueError("--ids must be a comma-separated list of four-digit M-CSA IDs")
    if len(values) != len(set(values)):
        raise ValueError("--ids contains duplicates")
    return tuple(sorted(values))


def _source_entries(payload: Any, record_ids: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise ValueError("M-CSA entry API response has no results array")
    results = payload["results"]
    expected_numeric = {int(record_id[1:]) for record_id in record_ids}
    observed_numeric = [
        entry.get("mcsa_id") for entry in results if isinstance(entry, dict)
    ]
    if (
        len(results) != len(record_ids)
        or len(observed_numeric) != len(record_ids)
        or set(observed_numeric) != expected_numeric
        or len(set(observed_numeric)) != len(observed_numeric)
        or payload.get("count") != len(record_ids)
    ):
        raise ValueError("M-CSA entry API response differs from the explicit selection")
    return {f"M{entry['mcsa_id']:04d}": entry for entry in results}


def _step_count(entries: dict[str, dict[str, Any]]) -> int:
    return sum(probe_identity(entry)["source_step_count"] for entry in entries.values())


def _scheme_wrapper(
    *,
    step: dict[str, Any],
    mechanism_id: int,
    http_status: int,
    raw: bytes,
    retrieval_status: str,
) -> dict[str, Any]:
    if http_status == 200:
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("M-CSA Marvin scheme is not valid UTF-8") from exc
        if not text.lstrip().startswith("<cml"):
            raise ValueError("M-CSA Marvin scheme response is not CML")
        content_sha256: str | None = _sha256(raw)
    else:
        text = None
        content_sha256 = None
    wrapper = {
        "content_sha256": content_sha256,
        "content_utf8": text,
        "http_status": http_status,
        "is_product": step["is_product"],
        "mechanism_id": mechanism_id,
        "media_type": "chemical/x-mdl-molfile+xml",
        "retrieval_status": retrieval_status,
        "source_url": scheme_url_from_step(step),
        "step_id": step["step_id"],
    }
    wrapper.update(scheme_flow_parse_receipt(wrapper))
    return wrapper


def fetch_and_build(
    *,
    retrieved_at: str,
    explicit_record_ids: tuple[str, ...] | None = None,
    entry_payload_path: Path | None = None,
) -> dict[str, Any]:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", retrieved_at):
        raise ValueError("--retrieved-at must be an explicit UTC timestamp")
    status = build_development_status(ROOT)
    default_ids = default_draft_record_ids(ROOT)
    if explicit_record_ids is None:
        record_ids = default_ids
        selection_basis = "development_gate_default_mechanism_draft_cases"
        requested_operation = "source_scoped_mechanism_draft"
    else:
        record_ids = explicit_record_ids
        selection_basis = "explicit_record_ids"
        requested_operation = "source_annotation"
    for record_id in record_ids:
        require_operation(ROOT, "source_annotation", record_id)

    access = status["source_access"]
    meter = AcquisitionMeter(
        requests_max=access["maximum_requests_per_batch"],
        download_bytes_max=access["maximum_download_bytes_per_batch"],
    )
    entry_url = build_entry_request_url(record_ids)
    if entry_payload_path is None:
        entry_status, entry_raw, entry_receipt = meter.fetch(
            entry_url,
            request_kind="entry_batch",
            record_ids=list(record_ids),
            mechanism_id=None,
            step_id=None,
        )
        if entry_status != 200:
            raise ValueError(f"M-CSA entry API returned HTTP {entry_status}")
    else:
        entry_raw = entry_payload_path.read_bytes()
        entry_receipt = meter.register_provided_entry_response(
            entry_url, list(record_ids), entry_raw
        )
    try:
        payload = json.loads(entry_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("M-CSA entry API response is not valid UTF-8 JSON") from exc
    entries = _source_entries(payload, record_ids)
    expected_requests = 1 + _step_count(entries)
    meter.ensure_request_capacity(expected_requests - meter.requests_used)

    snapshot_bytes: dict[str, bytes] = {}
    records: list[dict[str, Any]] = []
    for record_id in record_ids:
        entry = entries[record_id]
        schemes: list[dict[str, Any]] = []
        for mechanism in entry["reaction"]["mechanisms"]:
            mechanism_id = mechanism["mechanism_id"]
            for step in mechanism["steps"]:
                source_url = scheme_url_from_step(step)
                http_status, scheme_raw, receipt = meter.fetch(
                    source_url,
                    request_kind="step_scheme",
                    record_ids=[record_id],
                    mechanism_id=mechanism_id,
                    step_id=step["step_id"],
                )
                schemes.append(
                    _scheme_wrapper(
                        step=step,
                        mechanism_id=mechanism_id,
                        http_status=http_status,
                        raw=scheme_raw,
                        retrieval_status=receipt["retrieval_status"],
                    )
                )
        schemes.sort(key=lambda item: (item["mechanism_id"], item["step_id"]))
        relative = (SOURCE_ROOT / f"{record_id}.json").as_posix()
        raw_snapshot = _json_bytes(
            {
                "entry": entry,
                "record_id": record_id,
                "source": "M-CSA",
                "step_schemes": schemes,
            }
        )
        snapshot_bytes[record_id] = raw_snapshot
        records.append(
            {
                "source_id": "M-CSA",
                "record_id": record_id,
                "uri": f"https://www.ebi.ac.uk/thornton-srv/m-csa/entry/{int(record_id[1:])}/",
                "retrieval_status": "bundled_source_scoped_snapshot",
                "snapshot_path": relative,
                "snapshot_sha256": _sha256(raw_snapshot),
                "snapshot_bytes": len(raw_snapshot),
                "retrieved_at": retrieved_at,
                "entry_response_sha256": entry_receipt["response_sha256"],
                "probe_identity": probe_identity(entry),
                "scheme_status_counts": dict(
                    sorted(Counter(item["retrieval_status"] for item in schemes).items())
                ),
                "license": EXPECTED_LICENSE,
                "attribution": EXPECTED_ATTRIBUTION,
                "change_notice": EXPECTED_CHANGE_NOTICE,
            }
        )

    by_id = {row["mcsa_id"]: row for row in status["cases"]}
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "selection": {
            "basis": selection_basis,
            "requested_operation": requested_operation,
            "record_ids": list(record_ids),
        },
        "retrieved_at": retrieved_at,
        "source": {
            "source_id": "M-CSA",
            "entry_request_url": entry_url,
            "allowed_https_origin": "https://www.ebi.ac.uk",
            "allowed_scheme_path_prefix": "/thornton-srv/m-csa/media/schemes/",
        },
        "development_gate": {
            "authorization_operation": "source_annotation",
            "status_path": DEVELOPMENT_STATUS_PATH.as_posix(),
            "status_sha256": canonical_file_sha256(ROOT / DEVELOPMENT_STATUS_PATH),
            "case_controls": [_case_control(by_id[record_id]) for record_id in record_ids],
        },
        "rights": {
            "license": EXPECTED_LICENSE,
            "attribution": EXPECTED_ATTRIBUTION,
            "change_notice": EXPECTED_CHANGE_NOTICE,
            "rights_matrix_path": RIGHTS_MATRIX_PATH.as_posix(),
            "rights_matrix_sha256": canonical_file_sha256(ROOT / RIGHTS_MATRIX_PATH),
        },
        "acquisition": {
            "external_requests_expected": expected_requests,
            "external_requests_used": meter.requests_used,
            "external_requests_max": meter.requests_max,
            "download_bytes_used": meter.download_bytes_used,
            "download_bytes_max": meter.download_bytes_max,
            "responses": meter.responses,
        },
        "records": records,
        "snapshot_set_sha256": _snapshot_set_digest(records),
        "boundaries": dict(BOUNDARIES),
    }
    if meter.requests_used != expected_requests:
        raise ValueError("actual M-CSA request count differs from the source step plan")

    for record_id, raw_snapshot in snapshot_bytes.items():
        path = ROOT / SOURCE_ROOT / f"{record_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw_snapshot)
    manifest_path = ROOT / MANIFEST_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(_json_bytes(manifest))
    attribution_path = ROOT / ATTRIBUTION_PATH
    attribution_path.write_text(render_source_attribution(manifest), encoding="utf-8")
    validate_atlas_draft_source_manifest(manifest, repo_root=ROOT)
    return manifest


def check() -> dict[str, Any]:
    manifest = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    return validate_atlas_draft_source_manifest(manifest, repo_root=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--fetch", action="store_true", help="perform the bounded network fetch")
    action.add_argument("--check", action="store_true", help="verify committed sources offline")
    parser.add_argument("--retrieved-at", help="explicit UTC timestamp required with --fetch")
    parser.add_argument(
        "--ids",
        help="explicit comma-separated source-annotation selection; default derives draft-permitted cases",
    )
    parser.add_argument(
        "--entry-payload",
        type=Path,
        help="reuse one already-retrieved response for the exact combined entry request",
    )
    args = parser.parse_args()
    if args.fetch:
        if not args.retrieved_at:
            parser.error("--fetch requires --retrieved-at")
        explicit_ids = _parse_ids(args.ids) if args.ids else None
        result = fetch_and_build(
            retrieved_at=args.retrieved_at,
            explicit_record_ids=explicit_ids,
            entry_payload_path=args.entry_payload,
        )
        summary = validate_atlas_draft_source_manifest(result, repo_root=ROOT)
    else:
        if args.retrieved_at or args.ids or args.entry_payload:
            parser.error("--retrieved-at, --ids, and --entry-payload require --fetch")
        summary = check()
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
