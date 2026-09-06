"""Build the bounded unreviewed candidate-event catalog for offline queries."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.scan_atlas_candidates import render
from scripts.scan_atlas_context_candidates import scan_context_candidates
from catalytic_earth import atlas_candidate_events
from catalytic_earth.atlas_candidate_events import (
    build_candidate_event_catalog,
    validate_candidate_event_catalog,
)
from catalytic_earth.atlas_context_candidates import extract_context_panel_candidate
from catalytic_earth.atlas_drafts import validate_source_drafts


REGISTRY = ROOT / "data/atlas/candidate_extraction/source_registry.json"
BASELINE_SCAN = ROOT / "data/atlas/candidate_extraction/scan.json"
CONTEXT_SCAN = ROOT / "data/atlas/context_candidates/scan.json"
OUTPUT_DIRECTORY = ROOT / "src/catalytic_earth/candidate_event_data"
CATALOG_IMPLEMENTATIONS = (
    "scripts/build_atlas_candidate_events.py",
    "src/catalytic_earth/atlas_candidate_events.py",
)
DRAFT_PACKAGES = (
    ("source_drafts.json", "source_drafts_expected.json", "source_drafts_attribution.md"),
    (
        "aldolase_transketolase.json",
        "aldolase_transketolase_expected.json",
        "aldolase_transketolase_attribution.md",
    ),
    ("plp_pyruvoyl.json", "plp_pyruvoyl_expected.json", "plp_pyruvoyl_attribution.md"),
)


ATTRIBUTION = """# Candidate event catalog attribution

The retained mechanism records and MRV panels used to derive this catalog come
from the **Mechanism and Catalytic Site Atlas (M-CSA)**:

- [M0049, histidine decarboxylase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/49/)
- [M0066, D-amino-acid transaminase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/66/)
- [M0106, pyruvate dehydrogenase E1](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/106/)
- [M0212, nitrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/212/)
- [M0219, transketolase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/219/)

M-CSA data are available under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the M-CSA
authors for the curated mechanisms and source depictions, and cite Ribeiro AJM
et al., “Mechanism and Catalytic Site Atlas (M-CSA): a database of enzyme
reaction mechanisms and active sites,” *Nucleic Acids Research* 46(D1),
D618-D623 (2018),
[doi:10.1093/nar/gkx1012](https://doi.org/10.1093/nar/gkx1012).

This project generated the packaged catalog offline from twelve candidates in
the frozen 101-pair context scan. Each row retains its exact M-CSA source
snapshot and panel hashes, source-flow witnesses, complete candidate payload,
and the source-specific scope and abstentions copied from the corresponding
packaged Tier-1 source draft. The catalog packages derived candidate data but
does not redistribute the raw M-CSA snapshot files.

The candidates are unreviewed drawing-level graph comparisons. Search results
do not establish a physical atom map, canonical participant identity,
stereochemical or coordination interpretation, complete mechanism,
experimentally observed intermediate, or experimental validation. A
source-arrow-only event is separately labeled from an event confirmed in the
adjacent source graph. Formal-charge replay does not replay raw lone-pair
annotations. Multiple query clauses must match within one candidate, but that
does not assert shared atoms, a shared source arrow, or mechanism equivalence.
"""


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _load_verified_scan() -> tuple[dict, bytes]:
    frozen_raw = CONTEXT_SCAN.read_bytes()
    frozen = json.loads(frozen_raw)
    regenerated = scan_context_candidates()
    if render(regenerated).encode("utf-8") != frozen_raw:
        raise ValueError("frozen context scan no longer reproduces")
    registry_raw = REGISTRY.read_bytes()
    baseline_raw = BASELINE_SCAN.read_bytes()
    if digest(registry_raw) != frozen["source_registry_sha256"]:
        raise ValueError("context scan source-registry binding differs")
    if digest(baseline_raw) != frozen["baseline_scan_sha256"]:
        raise ValueError("context scan baseline binding differs")
    for path, expected in frozen["implementation_sha256"].items():
        implementation = ROOT / path
        if not implementation.is_file() or digest(implementation.read_bytes()) != expected:
            raise ValueError(f"context scan implementation binding differs: {path}")
    return frozen, frozen_raw


def _load_source_registry() -> dict[str, tuple[Path, bytes]]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources: dict[str, tuple[Path, bytes]] = {}
    for row in registry["records"]:
        path = ROOT / row["snapshot_path"]
        raw = path.read_bytes()
        if digest(raw) != row["snapshot_sha256"]:
            raise ValueError(f"source snapshot differs from registry: {row['record_id']}")
        sources[row["record_id"]] = (path, raw)
    return sources


def _load_draft_records() -> tuple[list[dict], dict[str, tuple[dict, dict]]]:
    bindings: list[dict] = []
    records: dict[str, tuple[dict, dict]] = {}
    directory = ROOT / "src/catalytic_earth/draft_data"
    for bundle_name, expected_name, attribution_name in DRAFT_PACKAGES:
        path = directory / bundle_name
        raw = path.read_bytes()
        expected = json.loads((directory / expected_name).read_text(encoding="utf-8"))
        attribution_raw = (directory / attribution_name).read_bytes()
        if expected.get("schema_version") != "catalytic-earth.source-drafts-package.v1":
            raise ValueError(f"unsupported source-draft package: {bundle_name}")
        if digest(raw) != expected.get("bundle_sha256"):
            raise ValueError(f"source-draft package differs from its expected hash: {bundle_name}")
        if digest(attribution_raw) != expected.get("attribution_sha256"):
            raise ValueError(f"source-draft attribution differs from its expected hash: {attribution_name}")
        bundle = json.loads(raw)
        validate_source_drafts(bundle)
        binding = {
            "bundle_id": bundle["bundle_id"],
            "path": _relative(path),
            "sha256": digest(raw),
        }
        bindings.append(binding)
        for record in bundle["records"]:
            mcsa_id = record["mcsa_id"]
            if mcsa_id in records:
                raise ValueError(f"duplicate source-draft record: {mcsa_id}")
            records[mcsa_id] = (binding, record)
    return bindings, records


def _raw_source_step(source: dict, mechanism_id: int, source_step_id: int) -> dict:
    mechanism = next(
        row for row in source["entry"]["reaction"]["mechanisms"]
        if row["mechanism_id"] == mechanism_id
    )
    return next(row for row in mechanism["steps"] if row["step_id"] == source_step_id)


def _step_binding(
    *,
    role: str,
    source_step_id: int,
    scheme_sha256: str,
    proposal: dict,
    source: dict,
    mechanism_id: int,
) -> dict:
    compiled = {
        row["source_step_id"]: row for row in proposal["mechanism_steps"]
    }.get(source_step_id)
    if compiled is not None:
        if compiled["source_scheme_sha256"] != scheme_sha256:
            raise ValueError("draft step and candidate scheme hashes differ")
        return {
            "role": role,
            "source_kind": "source_draft_step",
            "step_id": compiled["step_id"],
            "source_step_id": source_step_id,
            "scheme_sha256": scheme_sha256,
            "summary": compiled["summary"],
            "is_inferred": compiled["is_inferred"],
        }
    if source_step_id not in proposal["terminal_state_source_step_ids"]:
        raise ValueError("candidate panel is absent from the matching source draft")
    raw_step = _raw_source_step(source, mechanism_id, source_step_id)
    if raw_step.get("is_product") is not True:
        raise ValueError("uncompiled source panel is not a declared terminal state")
    return {
        "role": role,
        "source_kind": "mcsa_terminal_state",
        "step_id": None,
        "source_step_id": source_step_id,
        "scheme_sha256": scheme_sha256,
        "summary": raw_step["description"],
        "is_inferred": None,
    }


def _source_context(
    candidate: dict,
    *,
    draft_binding: dict,
    record: dict,
    source: dict,
) -> dict:
    source_binding = candidate["source_binding"]
    mechanism_id = source_binding["mechanism_id"]
    proposal = next(
        row for row in record["mechanism_proposals"]
        if row["source_mechanism_id"] == mechanism_id
    )
    if proposal["source_record_id"] != record["mcsa_id"]:
        raise ValueError("source-draft proposal belongs to another record")
    return {
        "source_draft_bundle_id": draft_binding["bundle_id"],
        "record_binding": {
            "record_id": record["record_id"],
            "mcsa_id": record["mcsa_id"],
        },
        "proposal_binding": {
            "proposal_id": proposal["proposal_id"],
            "source_mechanism_id": mechanism_id,
        },
        "source_scope": record["source_scope"],
        "step_bindings": [
            _step_binding(
                role="before",
                source_step_id=source_binding["before_step_id"],
                scheme_sha256=source_binding["before_scheme_sha256"],
                proposal=proposal,
                source=source,
                mechanism_id=mechanism_id,
            ),
            _step_binding(
                role="after",
                source_step_id=source_binding["after_step_id"],
                scheme_sha256=source_binding["after_scheme_sha256"],
                proposal=proposal,
                source=source,
                mechanism_id=mechanism_id,
            ),
        ],
        "mandatory_abstentions": record["mandatory_abstentions"],
    }


def build() -> dict:
    if Path(__file__).resolve() != (ROOT / CATALOG_IMPLEMENTATIONS[0]).resolve():
        raise ValueError("candidate-event builder origin differs from its hash path")
    if Path(atlas_candidate_events.__file__).resolve() != (ROOT / CATALOG_IMPLEMENTATIONS[1]).resolve():
        raise ValueError("candidate-event module origin differs from its hash path")
    scan, scan_raw = _load_verified_scan()
    sources = _load_source_registry()
    draft_bindings, draft_records = _load_draft_records()
    rows = [row for row in scan["pairs"] if row["extraction_status"] == "candidate"]
    if len(rows) != 12 or scan["aggregate"]["candidate_count"] != 12:
        raise ValueError("candidate event catalog requires exactly the frozen twelve candidates")
    candidates: list[dict] = []
    candidate_contexts: list[dict] = []
    for row in rows:
        source_path, source_raw = sources[row["record_id"]]
        source = json.loads(source_raw)
        candidate = extract_context_panel_candidate(
            source_raw,
            mechanism_id=row["mechanism_id"],
            before_step_id=row["before_step_id"],
        )
        if candidate["candidate_id"] != row["candidate_id"]:
            raise ValueError("reproduced candidate ID differs from frozen scan")
        candidate_sha256 = digest(render(candidate).encode("utf-8"))
        if candidate_sha256 != row["candidate_sha256"]:
            raise ValueError(f"candidate differs from frozen context scan: {row['candidate_id']}")
        if candidate["source_binding"]["snapshot_sha256"] != digest(source_raw):
            raise ValueError(f"candidate source binding differs: {_relative(source_path)}")
        try:
            draft_binding, draft_record = draft_records[row["record_id"]]
        except KeyError as exc:
            raise ValueError(f"candidate lacks a packaged source draft: {row['record_id']}") from exc
        context = _source_context(
            candidate,
            draft_binding=draft_binding,
            record=draft_record,
            source=source,
        )
        candidates.append(candidate)
        candidate_contexts.append({
            "candidate_id": candidate["candidate_id"],
            "candidate_sha256": candidate_sha256,
            "source_context_sha256": digest(canonical_bytes(context)),
            "source_context": context,
        })
    provenance = {
        "context_scan": {
            "schema_version": scan["schema_version"],
            "path": _relative(CONTEXT_SCAN),
            "sha256": digest(scan_raw),
            "source_registry_sha256": scan["source_registry_sha256"],
            "baseline_scan_sha256": scan["baseline_scan_sha256"],
            "implementation_sha256": scan["implementation_sha256"],
        },
        "source_draft_bundles": draft_bindings,
        "candidate_contexts": candidate_contexts,
        "catalog_implementation_sha256": {
            path: digest((ROOT / path).read_bytes()) for path in CATALOG_IMPLEMENTATIONS
        },
    }
    catalog = build_candidate_event_catalog(candidates, provenance=provenance)
    validate_candidate_event_catalog(catalog)
    return catalog


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog = build()
    summary = validate_candidate_event_catalog(catalog)
    raw = canonical_bytes(catalog)
    attribution = ATTRIBUTION.encode("utf-8")
    expected = {
        "schema_version": "catalytic-earth.candidate-event-package.v1",
        "catalog_sha256": digest(raw),
        "attribution_sha256": digest(attribution),
    }
    outputs = {
        "catalog.json": raw,
        "attribution.md": attribution,
        "expected.json": canonical_bytes(expected),
    }
    for name, content in outputs.items():
        path = OUTPUT_DIRECTORY / name
        if args.check:
            if not path.is_file() or path.read_bytes() != content:
                raise SystemExit(f"candidate-event output is stale: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if summary["catalog_sha256"] != expected["catalog_sha256"]:
        raise ValueError("catalog validator and packaged bytes use different canonical forms")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
