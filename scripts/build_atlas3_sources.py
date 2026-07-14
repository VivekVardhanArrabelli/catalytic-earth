"""Fetch once or locally verify the bounded Atlas-3 authoritative source set."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data/atlas/atlas3_selection.json"
ATLAS_ROOT = ROOT / "data/atlas/atlas3"
SOURCES_ROOT = ATLAS_ROOT / "sources"
MANIFEST_PATH = ATLAS_ROOT / "source_manifest.json"
USER_AGENT = "CatalyticEarth/0.1 Atlas-3 source snapshot"
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_selection import (  # noqa: E402
    load_atlas3_selection,
    validate_atlas3_selection,
)
from catalytic_earth.atlas_sources import (  # noqa: E402
    EXPECTED_LICENSES,
    validate_atlas3_source_manifest,
)
from catalytic_earth.canonical_hash import canonical_file_sha256  # noqa: E402


ATTRIBUTIONS = {
    "DOI": "Cite the identified primary article and publisher; no article content bundled.",
    "M-CSA": "Credit M-CSA and cite Ribeiro et al. plus the accessed entry.",
    "PDB": "Cite the PDB identifier, structure authors/publication, RCSB PDB, and wwPDB.",
    "PMCID": "Cite the identified primary article; no article content bundled.",
    "Rhea": "Credit Rhea and cite the database release/publication.",
    "UniProtKB": "Credit UniProt and cite the database release/publication.",
}
MEDIA_TYPES = {
    "DOI": "text/uri-list",
    "M-CSA": "application/json",
    "PDB": "application/gzip",
    "PMCID": "text/uri-list",
    "Rhea": "application/json",
    "UniProtKB": "application/json",
}
CHANGE_NOTICES = {
    "DOI": "Reference-only handle; no third-party article text copied or modified.",
    "M-CSA": "API JSON normalized to sorted UTF-8 JSON; no scientific fields intentionally changed.",
    "PDB": "Exact gzip-compressed mmCIF archive bytes; no transformation.",
    "PMCID": "Reference-only handle; no third-party article text copied or modified.",
    "Rhea": "One official TSV result transformed to sorted UTF-8 JSON with the request URL retained.",
    "UniProtKB": "REST JSON normalized to sorted UTF-8 JSON; no scientific fields intentionally changed.",
}


def _fetch(url: str, timeout: int = 60) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _write(relative: str, raw: bytes) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def _snapshot_target(source_id: str, record_id: str) -> tuple[str, list[str]] | None:
    if source_id == "UniProtKB":
        return (
            f"data/atlas/atlas3/sources/uniprot/{record_id}.json",
            [f"https://rest.uniprot.org/uniprotkb/{record_id}.json"],
        )
    if source_id == "Rhea":
        numeric = record_id.split(":", 1)[1]
        params = urlencode(
            {
                "query": f"id:{numeric}",
                "columns": "rhea-id,equation,ec,chebi-id,chebi",
                "format": "tsv",
                "limit": "10",
            }
        )
        return (
            f"data/atlas/atlas3/sources/rhea/{record_id.replace(':', '_')}.json",
            [f"https://www.rhea-db.org/rhea?{params}"],
        )
    if source_id == "M-CSA":
        numeric = str(int(record_id[1:]))
        params = urlencode({"format": "json", "entries.mcsa_ids": numeric})
        return (
            f"data/atlas/atlas3/sources/mcsa/{record_id}.json",
            [f"https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/?{params}"],
        )
    if source_id == "PDB":
        return (
            f"data/atlas/atlas3/sources/pdb/{record_id}.cif.gz",
            [f"https://files.rcsb.org/download/{record_id}.cif.gz"],
        )
    return None


def _fetch_snapshot(source_id: str, record_id: str, url: str) -> bytes:
    raw = _fetch(url)
    if source_id == "PDB":
        if not raw.startswith(b"\x1f\x8b"):
            raise ValueError(f"PDB {record_id} did not return gzip data")
        return raw
    if source_id == "Rhea":
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        rows = list(csv.DictReader(StringIO(text), delimiter="\t"))
        if len(rows) != 1 or rows[0].get("Reaction identifier") != record_id:
            raise ValueError(f"Rhea query for {record_id} did not return exactly that record")
        return _json_bytes(
            {
                "record_id": record_id,
                "request_url": url,
                "row": rows[0],
                "source": "Rhea",
            }
        )
    payload = json.loads(raw)
    if source_id == "UniProtKB":
        if payload.get("primaryAccession") != record_id:
            raise ValueError(f"UniProt returned the wrong accession for {record_id}")
        return _json_bytes(payload)
    if source_id == "M-CSA":
        results = payload.get("results", [])
        if len(results) != 1 or results[0].get("mcsa_id") != int(record_id[1:]):
            raise ValueError(f"M-CSA returned the wrong entry for {record_id}")
        return _json_bytes(results[0])
    raise ValueError(f"unsupported bundled source: {source_id}")


def _source_handles(selection: dict[str, Any]) -> list[dict[str, Any]]:
    handles = [handle for case in selection["cases"] for handle in case["source_handles"]]
    return sorted(handles, key=lambda item: (item["source_id"], item["record_id"]))


def _manifest_set_digest(records: list[dict[str, Any]]) -> str:
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
    return hashlib.sha256(raw).hexdigest()


def fetch_and_build(retrieved_at: str) -> dict[str, Any]:
    if not retrieved_at.endswith("Z"):
        raise ValueError("--retrieved-at must be an explicit UTC time ending in Z")
    selection = load_atlas3_selection(SELECTION_PATH)
    records: list[dict[str, Any]] = []
    for handle in _source_handles(selection):
        source_id = handle["source_id"]
        record_id = handle["record_id"]
        target = _snapshot_target(source_id, record_id)
        if target is None:
            status = "reference_only_verified_handle"
            relative = None
            digest = None
            size = 0
            urls = [handle["uri"]]
        else:
            relative, urls = target
            path = _write(relative, _fetch_snapshot(source_id, record_id, urls[0]))
            status = "bundled_snapshot"
            digest = canonical_file_sha256(path)
            size = path.stat().st_size
        records.append(
            {
                "source_id": source_id,
                "record_id": record_id,
                "uri": handle["uri"],
                "evidence_role": handle["evidence_role"],
                "applicability": handle["applicability"],
                "retrieval_status": status,
                "snapshot_path": relative,
                "snapshot_sha256": digest,
                "snapshot_bytes": size,
                "retrieval_urls": urls,
                "media_type": MEDIA_TYPES[source_id],
                "license": EXPECTED_LICENSES[source_id],
                "attribution": ATTRIBUTIONS[source_id],
                "change_notice": CHANGE_NOTICES[source_id],
                "retrieved_at": retrieved_at,
            }
        )
    selection_sha = validate_atlas3_selection(selection)["selection_sha256"]
    manifest = {
        "schema_version": "catalytic-earth.atlas3-source-manifest.v1",
        "selection_sha256": selection_sha,
        "retrieved_at": retrieved_at,
        "rights_matrix_path": "docs/SOURCE_DATA_RIGHTS.md",
        "records": records,
        "snapshot_set_sha256": _manifest_set_digest(records),
    }
    _write(MANIFEST_PATH.relative_to(ROOT).as_posix(), _json_bytes(manifest))
    validate_atlas3_source_manifest(
        manifest, repo_root=ROOT, selection=selection
    )
    return manifest


def check() -> dict[str, int | str]:
    selection = load_atlas3_selection(SELECTION_PATH)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return validate_atlas3_source_manifest(
        manifest, repo_root=ROOT, selection=selection
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="perform the bounded network fetch")
    parser.add_argument(
        "--retrieved-at",
        help="explicit UTC retrieval timestamp required with --fetch",
    )
    args = parser.parse_args()
    if args.fetch:
        if not args.retrieved_at:
            parser.error("--fetch requires --retrieved-at")
        fetch_and_build(args.retrieved_at)
    elif args.retrieved_at:
        parser.error("--retrieved-at is only valid with --fetch")
    print(json.dumps(check(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
