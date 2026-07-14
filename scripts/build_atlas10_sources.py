"""Fetch once or locally verify the bounded Atlas-10 follow-on source package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
ATLAS_ROOT = ROOT / "data/atlas/atlas10"
MANIFEST_PATH = ATLAS_ROOT / "source_manifest.json"
USER_AGENT = "CatalyticEarth/0.1 Atlas-10 source snapshot"
CATH_NAMES_URL = (
    "https://download.cathdb.info/cath/releases/latest-release/"
    "cath-classification-data/cath-names.txt"
)
CATH_DOMAINS_URL = (
    "https://download.cathdb.info/cath/releases/latest-release/"
    "cath-classification-data/cath-domain-list.txt"
)
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas10_selection import (  # noqa: E402
    load_atlas10_selection,
    validate_atlas10_selection,
)
from catalytic_earth.atlas10_sources import (  # noqa: E402
    EXPECTED_LICENSES,
    validate_atlas10_source_manifest,
)
from catalytic_earth.canonical_hash import canonical_file_sha256  # noqa: E402


ATTRIBUTIONS = {
    "CATH": "Credit CATH-Gene3D and cite the applicable release/publication.",
    "DOI": "Cite the identified primary article and publisher; no article content bundled.",
    "M-CSA": "Credit M-CSA and cite Ribeiro et al. plus the accessed entry.",
    "PDB": "Cite the PDB identifier, structure authors/publication, RCSB PDB, and wwPDB.",
    "Rhea": "Credit Rhea and cite the database release/publication.",
    "UniProtKB": "Credit UniProt and cite the database release/publication.",
}
MEDIA_TYPES = {
    "CATH": "application/json",
    "DOI": "text/uri-list",
    "M-CSA": "application/json",
    "PDB": "application/gzip",
    "Rhea": "application/json",
    "UniProtKB": "application/json",
}
CHANGE_NOTICES = {
    "CATH": "Selected official release name/domain rows transformed to sorted UTF-8 JSON; identifiers and source rows retained.",
    "DOI": "Reference-only handle; no third-party article text copied or modified.",
    "M-CSA": "API JSON and its linked Marvin step schemes wrapped in sorted UTF-8 JSON; source content and per-scheme hashes retained.",
    "PDB": "Exact gzip-compressed mmCIF archive bytes; no transformation.",
    "Rhea": "Official TSV result transformed to sorted UTF-8 JSON with the query and request URL retained.",
    "UniProtKB": "REST JSON normalized to sorted UTF-8 JSON; no scientific fields intentionally changed.",
}


@dataclass
class AcquisitionMeter:
    external_requests_used: int = 0
    download_bytes_used: int = 0

    def fetch(self, url: str, timeout: int = 180) -> bytes:
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        self.external_requests_used += 1
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
        self.download_bytes_used += len(raw)
        return raw


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _write(relative: str, raw: bytes) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def _selection_bindings(selection: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "case_id": case["case_id"],
            "source_id": handle["source_id"],
            "record_id": handle["record_id"],
            "evidence_role": handle["evidence_role"],
            "applicability": handle["applicability"],
        }
        for case in selection["follow_on_cases"]
        for handle in case["source_handles"]
    ]


def _unique_handles(selection: dict[str, Any]) -> list[dict[str, Any]]:
    handles: dict[tuple[str, str], dict[str, Any]] = {}
    for case in selection["follow_on_cases"]:
        for handle in case["source_handles"]:
            key = handle["source_id"], handle["record_id"]
            previous = handles.setdefault(key, handle)
            if previous["uri"] != handle["uri"]:
                raise ValueError(f"selection reuses {key} with different URIs")
    return [handles[key] for key in sorted(handles)]


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


def _rhea_sparql_url(record_id: str) -> str:
    numeric = record_id.split(":", 1)[1]
    query = f"""PREFIX rh: <http://rdf.rhea-db.org/>
SELECT ?reaction ?side ?participant ?compound ?accession ?name ?chebi ?reactivePart ?reactiveChebi
WHERE {{
  VALUES ?reaction {{ rh:{numeric} }}
  ?reaction rh:side ?side .
  ?side rh:contains ?participant .
  ?participant rh:compound ?compound .
  OPTIONAL {{ ?compound rh:accession ?accession }}
  OPTIONAL {{ ?compound rh:name ?name }}
  OPTIONAL {{ ?compound rh:chebi ?chebi }}
  OPTIONAL {{
    ?compound rh:reactivePart ?reactivePart .
    OPTIONAL {{ ?reactivePart rh:chebi ?reactiveChebi }}
  }}
}}
ORDER BY ?reaction ?side ?participant"""
    return "https://sparql.rhea-db.org/sparql?" + urlencode(
        {"query": query, "format": "application/sparql-results+json"}
    )


def _snapshot_target(source_id: str, record_id: str) -> tuple[str, list[str]] | None:
    if source_id == "UniProtKB":
        return (
            f"data/atlas/atlas10/sources/uniprot/{record_id}.json",
            [f"https://rest.uniprot.org/uniprotkb/{record_id}.json"],
        )
    if source_id == "Rhea":
        query = (
            f"id:{record_id.split(':', 1)[1]}"
            if record_id.startswith("RHEA:")
            else record_id.lower()
        )
        params = urlencode(
            {
                "query": query,
                "columns": "rhea-id,equation,ec,chebi-id,chebi",
                "format": "tsv",
                "limit": "10",
            }
        )
        suffix = (
            record_id.replace(":", "_") + ".json"
            if record_id.startswith("RHEA:")
            else record_id.replace(":", "_").replace(".", "_") + ".query-gap.json"
        )
        urls = [f"https://www.rhea-db.org/rhea?{params}"]
        if record_id.startswith("RHEA:"):
            urls.append(_rhea_sparql_url(record_id))
        return (
            f"data/atlas/atlas10/sources/rhea/{suffix}",
            urls,
        )
    if source_id == "M-CSA":
        numeric = str(int(record_id[1:]))
        params = urlencode({"format": "json", "entries.mcsa_ids": numeric})
        return (
            f"data/atlas/atlas10/sources/mcsa/{record_id}.json",
            [f"https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/?{params}"],
        )
    if source_id == "PDB":
        return (
            f"data/atlas/atlas10/sources/pdb/{record_id}.cif.gz",
            [f"https://files.rcsb.org/download/{record_id}.cif.gz"],
        )
    if source_id == "CATH":
        return (
            f"data/atlas/atlas10/sources/cath/{record_id.removeprefix('CATH:')}.json",
            [CATH_NAMES_URL, CATH_DOMAINS_URL],
        )
    return None


def _fetch_snapshot(source_id: str, record_id: str, url: str, meter: AcquisitionMeter) -> bytes:
    raw = meter.fetch(url)
    if source_id == "PDB":
        if not raw.startswith(b"\x1f\x8b"):
            raise ValueError(f"PDB {record_id} did not return gzip data")
        return raw
    if source_id == "Rhea":
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        reader = csv.DictReader(StringIO(text), delimiter="\t")
        rows = list(reader)
        if record_id.startswith("RHEA:"):
            if len(rows) != 1 or rows[0].get("Reaction identifier") != record_id:
                raise ValueError(f"Rhea query for {record_id} did not return exactly that record")
            result_kind = "direct_record"
            participant_payload = json.loads(meter.fetch(_rhea_sparql_url(record_id)))
            participant_rows = []
            for binding in participant_payload.get("results", {}).get("bindings", []):
                def value(field: str) -> str | None:
                    item = binding.get(field)
                    return item.get("value") if isinstance(item, dict) else None

                participant_rows.append(
                    {
                        "accession": value("accession"),
                        "chebi_uri": value("chebi"),
                        "compound_uri": value("compound"),
                        "name": value("name"),
                        "participant_uri": value("participant"),
                        "reaction_uri": value("reaction"),
                        "reactive_chebi_uri": value("reactiveChebi"),
                        "reactive_part_uri": value("reactivePart"),
                        "side_uri": value("side"),
                    }
                )
            expected_reaction_uri = (
                "http://rdf.rhea-db.org/" + record_id.split(":", 1)[1]
            )
            if not participant_rows or any(
                item["reaction_uri"] != expected_reaction_uri for item in participant_rows
            ):
                raise ValueError(f"Rhea SPARQL participants differ for {record_id}")
        else:
            if rows:
                raise ValueError(
                    f"frozen Rhea source gap {record_id} now returns records; stop and review"
                )
            result_kind = "documented_zero_row_query"
            participant_rows = []
        return _json_bytes(
            {
                "columns": reader.fieldnames,
                "query": (
                    f"id:{record_id.split(':', 1)[1]}"
                    if record_id.startswith("RHEA:")
                    else record_id.lower()
                ),
                "query_result_kind": result_kind,
                "record_id": record_id,
                "request_url": url,
                "participant_request_url": (
                    _rhea_sparql_url(record_id) if record_id.startswith("RHEA:") else None
                ),
                "participant_rows": participant_rows,
                "rows": rows,
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
        entry = results[0]
        schemes: list[dict[str, Any]] = []
        for mechanism in entry.get("reaction", {}).get("mechanisms", []):
            mechanism_id = mechanism.get("mechanism_id")
            for step in mechanism.get("steps", []):
                step_id = step.get("step_id")
                source_url = "https://" + str(step.get("marvin_xml", "")).removeprefix(
                    "https://"
                )
                if not source_url.endswith(".mrv"):
                    raise ValueError(
                        f"M-CSA {record_id} mechanism {mechanism_id} step {step_id} lacks MRV"
                    )
                try:
                    scheme_raw = meter.fetch(source_url)
                    scheme_text: str | None = scheme_raw.decode("utf-8")
                    if not scheme_text.lstrip().startswith("<cml"):
                        raise ValueError(
                            f"M-CSA {record_id} mechanism {mechanism_id} step {step_id} returned invalid MRV"
                        )
                    scheme_digest: str | None = hashlib.sha256(
                        scheme_text.encode("utf-8")
                    ).hexdigest()
                    retrieval_status = "bundled_linked_scheme"
                    http_status = 200
                except HTTPError as exc:
                    if (record_id, mechanism_id, step_id, exc.code) != (
                        "M0189",
                        1,
                        1,
                        404,
                    ):
                        raise
                    scheme_text = None
                    scheme_digest = None
                    retrieval_status = "source_link_missing_http_404"
                    http_status = 404
                schemes.append(
                    {
                        "content_sha256": scheme_digest,
                        "content_utf8": scheme_text,
                        "http_status": http_status,
                        "is_product": step.get("is_product"),
                        "mechanism_id": mechanism_id,
                        "media_type": "chemical/x-mdl-molfile+xml",
                        "retrieval_status": retrieval_status,
                        "source_url": source_url,
                        "step_id": step_id,
                    }
                )
        schemes.sort(key=lambda item: (item["mechanism_id"], item["step_id"]))
        return _json_bytes(
            {
                "entry": entry,
                "record_id": record_id,
                "source": "M-CSA",
                "step_schemes": schemes,
            }
        )
    raise ValueError(f"unsupported per-record bundled source: {source_id}")


def _cath_context(selection: dict[str, Any]) -> dict[str, set[str]]:
    context: dict[str, set[str]] = {}
    for case in selection["follow_on_cases"]:
        pdb_ids = {
            handle["record_id"]
            for handle in case["source_handles"]
            if handle["source_id"] == "PDB"
        }
        for handle in case["source_handles"]:
            if handle["source_id"] == "CATH":
                context.setdefault(handle["record_id"], set()).update(pdb_ids)
    return context


def _cath_snapshots(
    selection: dict[str, Any], meter: AcquisitionMeter
) -> dict[str, bytes]:
    names_text = meter.fetch(CATH_NAMES_URL).decode("utf-8")
    domains_text = meter.fetch(CATH_DOMAINS_URL).decode("utf-8")
    context = _cath_context(selection)
    classifications = {record_id.removeprefix("CATH:") for record_id in context}
    names: dict[str, dict[str, str]] = {}
    for raw_line in names_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"(\S+)\s+(\S+)\s+:(.*)", line)
        if match is None or match.group(1) not in classifications:
            continue
        classification, representative, description = match.groups()
        names[classification] = {
            "classification_id": classification,
            "description": description,
            "raw_source_row": line,
            "representative_domain_id": representative,
        }

    selected_pdbs = {pdb_id for values in context.values() for pdb_id in values}
    domains: dict[str, list[dict[str, Any]]] = {item: [] for item in classifications}
    for raw_line in domains_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        columns = line.split()
        if len(columns) != 12 or columns[0][:4].upper() not in selected_pdbs:
            continue
        classification = ".".join(columns[1:5])
        if classification not in classifications:
            continue
        domains[classification].append(
            {
                "architecture": int(columns[2]),
                "class": int(columns[1]),
                "classification_id": classification,
                "domain_id": columns[0],
                "domain_length": int(columns[10]),
                "homologous_superfamily": int(columns[4]),
                "raw_source_row": line,
                "resolution_angstrom": float(columns[11]),
                "s100_cluster": int(columns[8]),
                "s100_count": int(columns[9]),
                "s35_cluster": int(columns[5]),
                "s60_cluster": int(columns[6]),
                "s95_cluster": int(columns[7]),
                "topology": int(columns[3]),
            }
        )

    snapshots: dict[str, bytes] = {}
    for record_id, pdb_ids in sorted(context.items()):
        classification = record_id.removeprefix("CATH:")
        name_row = names.get(classification)
        if name_row is None:
            raise ValueError(f"CATH names release lacks {record_id}")
        rows = sorted(domains[classification], key=lambda row: row["domain_id"])
        observed = {row["domain_id"][:4].upper() for row in rows}
        if pdb_ids - observed:
            raise ValueError(
                f"CATH release does not map {sorted(pdb_ids - observed)} to {record_id}"
            )
        snapshots[record_id] = _json_bytes(
            {
                "domain_rows": rows,
                "name_row": name_row,
                "record_id": record_id,
                "release_locator": "latest-release",
                "selected_pdb_ids": sorted(pdb_ids),
                "source": "CATH",
                "source_files": [CATH_NAMES_URL, CATH_DOMAINS_URL],
            }
        )
    return snapshots


def fetch_and_build(retrieved_at: str) -> dict[str, Any]:
    if not retrieved_at.endswith("Z"):
        raise ValueError("--retrieved-at must be an explicit UTC time ending in Z")
    selection = load_atlas10_selection(SELECTION_PATH)
    meter = AcquisitionMeter()
    cath_snapshots = _cath_snapshots(selection, meter)
    records: list[dict[str, Any]] = []
    for handle in _unique_handles(selection):
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
            raw = (
                cath_snapshots[record_id]
                if source_id == "CATH"
                else _fetch_snapshot(source_id, record_id, urls[0], meter)
            )
            path = _write(relative, raw)
            status = (
                "bundled_query_gap_snapshot"
                if source_id == "Rhea" and record_id.startswith("EC:")
                else "bundled_snapshot"
            )
            digest = canonical_file_sha256(path)
            size = path.stat().st_size
        records.append(
            {
                "source_id": source_id,
                "record_id": record_id,
                "uri": handle["uri"],
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
    records.sort(key=lambda item: (item["source_id"], item["record_id"]))
    selection_sha = validate_atlas10_selection(selection)["selection_sha256"]
    manifest = {
        "schema_version": "catalytic-earth.atlas10-source-manifest.v1",
        "selection_sha256": selection_sha,
        "retrieved_at": retrieved_at,
        "rights_matrix_path": "docs/SOURCE_DATA_RIGHTS.md",
        "acquisition": {
            "external_requests_used": meter.external_requests_used,
            "external_requests_max": selection["phase_compute_budget"][
                "external_requests_max"
            ],
            "download_bytes_used": meter.download_bytes_used,
            "download_bytes_max": selection["phase_compute_budget"]["download_bytes_max"],
        },
        "bindings": _selection_bindings(selection),
        "records": records,
        "snapshot_set_sha256": _manifest_set_digest(records),
    }
    _write(MANIFEST_PATH.relative_to(ROOT).as_posix(), _json_bytes(manifest))
    validate_atlas10_source_manifest(manifest, repo_root=ROOT, selection=selection)
    return manifest


def check() -> dict[str, int | str]:
    selection = load_atlas10_selection(SELECTION_PATH)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return validate_atlas10_source_manifest(manifest, repo_root=ROOT, selection=selection)


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
