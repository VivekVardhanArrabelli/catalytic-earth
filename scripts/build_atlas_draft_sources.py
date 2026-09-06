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
from catalytic_earth.atlas_draft_batch import (  # noqa: E402
    DEFAULT_BATCH,
    DraftBatchPaths,
    resolve_batch,
)
from catalytic_earth.atlas_draft_sources import (  # noqa: E402
    BOUNDARIES,
    EXPECTED_ATTRIBUTION,
    EXPECTED_CHANGE_NOTICE,
    EXPECTED_LICENSE,
    RIGHTS_MATRIX_PATH,
    SCHEMA_VERSION,
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
                final_url = response.geturl()
                validate_official_mcsa_url(final_url, kind=request_kind)
                if final_url != url:
                    raise ValueError("M-CSA response redirected from the requested URL")
                raw = self._read_bounded(response, response.headers.get("Content-Length"))
        except HTTPError as exc:
            http_status = exc.code
            final_url = exc.geturl()
            validate_official_mcsa_url(final_url, kind=request_kind)
            if final_url != url:
                raise ValueError("M-CSA response redirected from the requested URL")
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


_CAPTURE_RECEIPT_FIELDS = {
    "final_url",
    "http_status",
    "mechanism_id",
    "record_ids",
    "request_index",
    "request_kind",
    "response_bytes",
    "response_sha256",
    "retrieval_status",
    "retrieved_at",
    "source_url",
    "started_at",
    "step_id",
}
_CAPTURE_LEDGER_FIELDS = {
    "aggregate",
    "completed_at",
    "limits",
    "preflight",
    "responses",
    "schema_version",
    "selection",
}


class CapturedResponses:
    """Verify and consume a complete prior bounded acquisition without network."""

    def __init__(
        self,
        directory: Path,
        *,
        record_ids: tuple[str, ...],
        meter: AcquisitionMeter,
    ) -> None:
        self.directory = Path(directory)
        ledger_path = self.directory / "receipts.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        if not isinstance(ledger, dict) or set(ledger) != _CAPTURE_LEDGER_FIELDS:
            raise ValueError("captured response ledger fields differ")
        if ledger.get("schema_version") != "catalytic-earth.temp-source-receipts.v1":
            raise ValueError("captured response ledger schema differs")
        if ledger.get("selection") != list(record_ids):
            raise ValueError("captured response selection differs")
        if ledger.get("limits") != {
            "maximum_requests": meter.requests_max,
            "maximum_download_bytes": meter.download_bytes_max,
        }:
            raise ValueError("captured response budget differs from the development gate")
        receipts = ledger.get("responses")
        if not isinstance(receipts, list) or not receipts:
            raise ValueError("captured response ledger is empty")
        if any(
            not isinstance(item, dict) or set(item) != _CAPTURE_RECEIPT_FIELDS
            for item in receipts
        ):
            raise ValueError("captured response receipt fields differ")
        if [item.get("request_index") for item in receipts] != list(
            range(1, len(receipts) + 1)
        ):
            raise ValueError("captured response order differs")
        response_bytes = [item.get("response_bytes") for item in receipts]
        if any(type(value) is not int or value < 0 for value in response_bytes):
            raise ValueError("captured response byte accounting differs")
        total_bytes = sum(response_bytes)
        preflight = ledger.get("preflight")
        entry_requests = sum(
            item.get("request_kind") == "entry_batch" for item in receipts
        )
        scheme_requests = sum(
            item.get("request_kind") == "step_scheme" for item in receipts
        )
        if preflight != {
            "entry_requests": entry_requests,
            "linked_scheme_requests": scheme_requests,
            "total_requests": len(receipts),
        }:
            raise ValueError("captured response preflight differs")
        aggregate = ledger.get("aggregate")
        if aggregate != {
            "all_expected_responses_present": True,
            "download_bytes_remaining": meter.download_bytes_max - total_bytes,
            "download_bytes_used": total_bytes,
            "requests_remaining": meter.requests_max - len(receipts),
            "requests_used": len(receipts),
        }:
            raise ValueError("captured response aggregate differs")
        if total_bytes > meter.download_bytes_max:
            raise ValueError("captured responses exceed the development-gate byte budget")
        meter.ensure_request_capacity(len(receipts))
        self.receipts = receipts
        self.meter = meter
        self.consumed: set[int] = set()

    def consume(
        self,
        *,
        url: str,
        request_kind: str,
        record_ids: list[str],
        mechanism_id: int | None,
        step_id: int | None,
    ) -> tuple[int, bytes, dict[str, Any]]:
        index = len(self.consumed)
        if index >= len(self.receipts):
            raise ValueError("captured response ledger ended before source coverage")
        captured = self.receipts[index]
        if not isinstance(captured, dict) or set(captured) != _CAPTURE_RECEIPT_FIELDS:
            raise ValueError(f"captured response {index + 1} fields differ")
        expected_identity = {
            "request_index": index + 1,
            "request_kind": request_kind,
            "source_url": url,
            "final_url": url,
            "record_ids": record_ids,
            "mechanism_id": mechanism_id,
            "step_id": step_id,
        }
        if any(captured.get(key) != value for key, value in expected_identity.items()):
            raise ValueError(f"captured response {index + 1} identity differs")
        for field_name in ("started_at", "retrieved_at"):
            if not isinstance(captured.get(field_name), str) or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", captured[field_name]
            ):
                raise ValueError(f"captured response {index + 1} time differs")
        if request_kind == "entry_batch":
            raw_path = self.directory / "raw" / "entry_batch.json"
        else:
            raw_path = (
                self.directory
                / "raw"
                / "schemes"
                / record_ids[0]
                / f"mechanism-{mechanism_id}"
                / f"step-{step_id}.mrv"
            )
        raw = raw_path.read_bytes()
        if (
            captured.get("response_bytes") != len(raw)
            or captured.get("response_sha256") != _sha256(raw)
        ):
            raise ValueError(f"captured response {index + 1} bytes or hash differ")
        http_status = captured.get("http_status")
        if not isinstance(http_status, int):
            raise ValueError(f"captured response {index + 1} HTTP status differs")
        expected_status = (
            "source_response_downloaded"
            if request_kind == "entry_batch"
            else (
                "bundled_linked_scheme"
                if http_status == 200
                else (
                    "source_link_missing_http_404"
                    if http_status == 404
                    else "source_link_http_error"
                )
            )
        )
        if captured.get("retrieval_status") != expected_status:
            raise ValueError(f"captured response {index + 1} retrieval status differs")
        self.meter.ensure_request_capacity(1)
        projected = self.meter._append(
            url=url,
            request_kind=request_kind,
            record_ids=record_ids,
            mechanism_id=mechanism_id,
            step_id=step_id,
            http_status=http_status,
            raw=raw,
            retrieval_status=expected_status,
        )
        expected_projection = {
            key: captured[key]
            for key in projected
        }
        if projected != expected_projection:
            raise ValueError(f"captured response {index + 1} receipt projection differs")
        self.consumed.add(index)
        return http_status, raw, projected

    def finish(self) -> None:
        if len(self.consumed) != len(self.receipts):
            raise ValueError("captured response ledger has unconsumed requests")


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
    retrieved_at: str | None,
    explicit_record_ids: tuple[str, ...] | None = None,
    entry_payload_path: Path | None = None,
    captured_response_directory: Path | None = None,
    batch: DraftBatchPaths = DEFAULT_BATCH,
) -> dict[str, Any]:
    if entry_payload_path is not None and captured_response_directory is not None:
        raise ValueError("entry payload and captured responses are mutually exclusive")
    status = build_development_status(ROOT, batch=batch)
    default_ids = default_draft_record_ids(ROOT, batch=batch)
    if explicit_record_ids is None:
        record_ids = default_ids
        selection_basis = "development_gate_default_mechanism_draft_cases"
        requested_operation = "source_scoped_mechanism_draft"
    else:
        record_ids = explicit_record_ids
        selection_basis = "explicit_record_ids"
        requested_operation = "source_annotation"
    for record_id in record_ids:
        require_operation(ROOT, "source_annotation", record_id, batch=batch)

    access = status["source_access"]
    meter = AcquisitionMeter(
        requests_max=access["maximum_requests_per_batch"],
        download_bytes_max=access["maximum_download_bytes_per_batch"],
    )
    captured = (
        CapturedResponses(
            captured_response_directory,
            record_ids=record_ids,
            meter=meter,
        )
        if captured_response_directory is not None
        else None
    )
    if captured is not None and retrieved_at is None:
        retrieved_at = captured.receipts[0].get("retrieved_at")
    if not isinstance(retrieved_at, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", retrieved_at
    ):
        raise ValueError("--retrieved-at must be an explicit UTC timestamp")
    if captured is not None and retrieved_at != captured.receipts[0].get("retrieved_at"):
        raise ValueError("retrieved_at differs from the captured entry response")
    entry_url = build_entry_request_url(record_ids)
    if captured is not None:
        entry_status, entry_raw, entry_receipt = captured.consume(
            url=entry_url,
            request_kind="entry_batch",
            record_ids=list(record_ids),
            mechanism_id=None,
            step_id=None,
        )
        if entry_status != 200:
            raise ValueError(f"M-CSA entry API returned HTTP {entry_status}")
    elif entry_payload_path is None:
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
                if captured is not None:
                    http_status, scheme_raw, receipt = captured.consume(
                        url=source_url,
                        request_kind="step_scheme",
                        record_ids=[record_id],
                        mechanism_id=mechanism_id,
                        step_id=step["step_id"],
                    )
                else:
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
        relative = (batch.sources_directory / f"{record_id}.json").as_posix()
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
            "status_path": batch.status_path.as_posix(),
            "status_sha256": canonical_file_sha256(ROOT / batch.status_path),
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
    if captured is not None:
        captured.finish()

    for record_id, raw_snapshot in snapshot_bytes.items():
        path = ROOT / batch.sources_directory / f"{record_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw_snapshot)
    manifest_path = ROOT / batch.manifest_path
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(_json_bytes(manifest))
    attribution_path = ROOT / batch.attribution_path
    attribution_path.write_text(render_source_attribution(manifest), encoding="utf-8")
    validate_atlas_draft_source_manifest(manifest, repo_root=ROOT, batch=batch)
    return manifest


def check(batch: DraftBatchPaths = DEFAULT_BATCH) -> dict[str, Any]:
    manifest = json.loads((ROOT / batch.manifest_path).read_text(encoding="utf-8"))
    return validate_atlas_draft_source_manifest(manifest, repo_root=ROOT, batch=batch)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--fetch", action="store_true", help="perform the bounded network fetch")
    action.add_argument(
        "--reuse-captured",
        type=Path,
        metavar="DIRECTORY",
        help="build offline from a complete verified raw-response capture",
    )
    action.add_argument("--check", action="store_true", help="verify committed sources offline")
    parser.add_argument(
        "--batch",
        default="default",
        help="source-draft batch name (default: legacy default batch)",
    )
    parser.add_argument(
        "--retrieved-at",
        help="explicit UTC timestamp required with --fetch; captured entry time is reused offline",
    )
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
    try:
        batch = resolve_batch(args.batch)
    except ValueError as exc:
        parser.error(str(exc))
    if args.fetch:
        if not args.retrieved_at:
            parser.error("--fetch requires --retrieved-at")
        explicit_ids = _parse_ids(args.ids) if args.ids else None
        result = fetch_and_build(
            retrieved_at=args.retrieved_at,
            explicit_record_ids=explicit_ids,
            entry_payload_path=args.entry_payload,
            batch=batch,
        )
        summary = validate_atlas_draft_source_manifest(
            result, repo_root=ROOT, batch=batch
        )
    elif args.reuse_captured is not None:
        if args.entry_payload:
            parser.error("--entry-payload cannot be used with --reuse-captured")
        explicit_ids = _parse_ids(args.ids) if args.ids else None
        result = fetch_and_build(
            retrieved_at=args.retrieved_at,
            explicit_record_ids=explicit_ids,
            captured_response_directory=args.reuse_captured,
            batch=batch,
        )
        summary = validate_atlas_draft_source_manifest(
            result, repo_root=ROOT, batch=batch
        )
    else:
        if args.retrieved_at or args.ids or args.entry_payload:
            parser.error(
                "--retrieved-at, --ids, and --entry-payload require --fetch or "
                "--reuse-captured"
            )
        summary = check(batch)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
