"""Check source projections and package the reviewed retrospective evidence case."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from catalytic_earth.atlas_mechanism_evidence import validate_mechanism_evidence, query_mechanism_evidence
from catalytic_earth.atlas_fragment_sites import build_fragment_sites
from catalytic_earth.atlas_evidence_source_context import PRIMARY_OBSERVATION_FIELDS, build_source_contexts

SOURCE = Path("data/atlas/mechanism_evidence/m0187")
PACKAGE = Path("src/catalytic_earth/mechanism_evidence_data")
OBSERVATION_FIELDS = PRIMARY_OBSERVATION_FIELDS
CAPTURE_FIELDS = (
    "request_url", "response_url", "http_status", "retrieved_at_utc", "response_bytes",
    "response_sha256", "retention_scope",
)


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _source_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").encode("utf-8")


def validate_source_projections(
    value: dict, *, repo_root: Path = ROOT, raw_source_directory: Path | None = None,
) -> dict:
    """Check exact evidence/source joins; raw XML is optional local review material.

    These checks detect drift. They do not infer scientific truth from prose.
    The reviewed payload pin covers both interpretation and source file hashes.
    """
    bindings = {row["binding_id"]: row for row in value["source_bindings"]}
    sources = {}
    for binding in bindings.values():
        raw = _source_bytes(repo_root / binding["path"])
        _require(hashlib.sha256(raw).hexdigest() == binding["sha256"], "mechanism evidence source hash differs")
        sources[binding["binding_id"]] = json.loads(raw)
    ledgers = [sources[b["binding_id"]] for b in bindings.values() if b["artifact_kind"] == "acquisition_receipts"]
    _require(len(ledgers) == 1, "exactly one acquisition ledger is required")
    ledger = ledgers[0]
    _require(ledger["schema_version"] == "catalytic-earth.primary-case-acquisition.v1", "unsupported acquisition ledger")
    receipts = {row["source_record_id"]: row for row in ledger["requests"]}
    _require(len(receipts) == len(ledger["requests"]), "acquisition source identifiers repeat")
    _require(ledger["limits"] == {"requests": 12, "response_bytes": 2097152}, "named acquisition bounds differ")
    _require(len(receipts) <= ledger["limits"]["requests"], "acquisition exceeds request bound")
    total_bytes = sum(row["response_bytes"] for row in receipts.values())
    _require(total_bytes <= ledger["limits"]["response_bytes"], "acquisition exceeds response-byte bound")
    used_sources, used_observations = set(), set()
    quote_words: dict[str, int] = {}
    raw_abstracts: dict[str, str] = {}
    for case in value["cases"]:
        references = {row["evidence_id"]: row for row in case["evidence_references"]}
        for reference in references.values():
            binding_id = reference["source_binding_id"]
            projection = sources[binding_id]
            source_record_id = reference["source_record_id"]
            _require(projection["schema_version"] == "catalytic-earth.primary-observation-projection.v1", "unsupported primary observation projection")
            _require(
                (projection["source_id"], projection["source_record_id"])
                == (reference["source_id"], source_record_id),
                "primary projection belongs to another source record",
            )
            _require(source_record_id in receipts, "primary projection has no acquisition receipt")
            receipt = receipts[source_record_id]
            _require(projection["raw_capture"] == {field: receipt[field] for field in CAPTURE_FIELDS}, "primary projection capture differs from acquisition receipt")
            _require(
                receipt["http_status"] == 200 and receipt["response_bytes"] > 0
                and receipt["redirects_followed"] == receipt["retries"] == 0
                and receipt["raw_response_path"] is None
                and receipt["retention_scope"] == "local_analysis_only_not_redistributed",
                "capture or retention scope differs",
            )
            _require(
                projection["inspection_depth"] == "retained_truncated_primary_abstract_not_full_methods"
                and projection["full_text_inspected"] is False
                and projection["assayed_construct_sequence_inspected"] is False
                and projection["pdb_identifiers_in_inspected_abstract"] == [],
                "primary projection inspection scope differs",
            )
            used_sources.add(source_record_id)
            if raw_source_directory is not None and source_record_id not in raw_abstracts:
                pmid = source_record_id.removeprefix("PMID:")
                _require(pmid.isdigit(), "unsupported raw-source identifier")
                raw = (raw_source_directory / f"PMID_{pmid}.xml").read_bytes()
                _require(len(raw) == receipt["response_bytes"] and hashlib.sha256(raw).hexdigest() == receipt["response_sha256"], "retained raw primary response differs from captured bytes")
                xml = ET.fromstring(raw)
                _require(xml.findtext(".//MedlineCitation/PMID") == pmid, "raw primary response belongs to another PMID")
                dois = [item.text for item in xml.findall(".//ArticleId") if item.get("IdType") == "doi"]
                _require(projection["doi"] in dois, "raw primary DOI differs from projection")
                abstract = xml.find(".//Abstract")
                _require(abstract is not None, "raw primary abstract is missing")
                raw_abstracts[source_record_id] = "".join(abstract.itertext())
                _require("ABSTRACT TRUNCATED" in raw_abstracts[source_record_id], "raw inspection depth differs from projection")
        for observation in case["observations"]:
            for evidence_id in observation["evidence_ids"]:
                reference = references[evidence_id]
                binding_id = reference["source_binding_id"]
                projection = sources[binding_id]
                projected = [o for o in projection["observations"] if o["observation_id"] == observation["observation_id"]]
                _require(len(projected) == 1 and projected[0] == {field: observation[field] for field in OBSERVATION_FIELDS}, "typed observation differs from its primary source projection")
                used_observations.add((binding_id, observation["observation_id"]))
            for witness in observation["source_witnesses"]:
                source_id = references[witness["evidence_id"]]["source_record_id"]
                quote_words[source_id] = quote_words.get(source_id, 0) + len(witness["exact_text"].split())
                if raw_source_directory is not None:
                    _require(witness["exact_text"] in raw_abstracts[source_id], "source witness is absent from the retained primary abstract")
    expected_observations = {
        (binding_id, observation["observation_id"])
        for binding_id, binding in bindings.items()
        if binding["artifact_kind"] == "primary_source_projection"
        for observation in sources[binding_id]["observations"]
    }
    _require(used_observations == expected_observations, "primary source observations are unbound")
    _require(used_sources == set(receipts), "acquisition ledger contains an unbound source")
    _require(all(count <= 25 for count in quote_words.values()), "primary excerpts exceed the short-witness limit")
    return {"request_count": len(receipts), "response_bytes": total_bytes, "raw_abstract_witnesses_checked": raw_source_directory is not None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--raw-source-directory", type=Path, help="optional local captured PubMed XML; no network access")
    args = parser.parse_args()
    value = json.loads((ROOT / SOURCE / "evidence.json").read_text(encoding="utf-8"))
    load = lambda path: json.loads((ROOT / path).read_text(encoding="utf-8"))
    summary = validate_mechanism_evidence(
        value, atlas10_bundle=load("src/catalytic_earth/atlas_data/atlas10_kernel.json"),
        transformation_values={"M0187": load("data/atlas/transformations/m0187/transformations.json")},
    )
    summary["source_check"] = validate_source_projections(value, raw_source_directory=args.raw_source_directory)
    outputs = {
        "evidence.json": canonical_bytes(value),
        "attribution.md": _source_bytes(ROOT / SOURCE / "SOURCE_ATTRIBUTION.md"),
    }
    contexts = build_source_contexts(
        load("data/atlas/mechanism_evidence/source_context_spec.json"), value,
        lambda path: (ROOT / path).read_bytes(),
    )
    outputs["source_contexts.json"] = canonical_bytes(contexts)
    fragments = build_fragment_sites(
        load("data/atlas/mechanism_evidence/source_fragment_spec.json"),
        load("data/atlas/mechanism_evidence/source_fragment_review.json"),
        lambda path: _source_bytes(ROOT / path),
        atlas10_bundle=load("src/catalytic_earth/atlas_data/atlas10_kernel.json"),
        transformation_values={"M0187": load("data/atlas/transformations/m0187/transformations.json")},
        evidence_query=query_mechanism_evidence(
            value, atlas10_bundle=load("src/catalytic_earth/atlas_data/atlas10_kernel.json"),
            transformation_values={"M0187": load("data/atlas/transformations/m0187/transformations.json")},
        ),
    )
    outputs["source_fragments.json"] = canonical_bytes(fragments)
    summary["source_context_count"] = len(contexts["contexts"])
    for binding in value["source_bindings"]:
        name = Path(binding["path"]).name
        _require(name not in outputs, "packaged source filenames collide")
        outputs[name] = _source_bytes(ROOT / binding["path"])
    outputs["expected.json"] = canonical_bytes({
        "schema_version": "catalytic-earth.mechanism-evidence-package.v1",
        "files": {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(outputs.items())},
    })
    for name, raw in outputs.items():
        path = ROOT / PACKAGE / name
        if args.check:
            if not path.is_file() or path.read_bytes() != raw:
                raise SystemExit(f"mechanism evidence output is stale: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
