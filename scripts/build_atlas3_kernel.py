"""Compile and verify the bounded Atlas-3 first biological kernel."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data/atlas/atlas3_selection.json"
ATLAS_ROOT = ROOT / "data/atlas/atlas3"
MANIFEST_PATH = ATLAS_ROOT / "source_manifest.json"
SPEC_PATH = ATLAS_ROOT / "compilation_spec.json"
ATTRIBUTION_PATH = ATLAS_ROOT / "SOURCE_ATTRIBUTION.md"
KERNEL_PATH = ATLAS_ROOT / "kernel.json"
QUERY_PATH = ATLAS_ROOT / "queries/case_truth_summary.sql"
EXPECTED_PATH = ATLAS_ROOT / "queries/case_truth_summary_expected.json"
PACKAGE_ROOT = ROOT / "src/catalytic_earth/atlas_data"
PACKAGE_KERNEL_PATH = PACKAGE_ROOT / "atlas3_kernel.json"
PACKAGE_QUERY_PATH = PACKAGE_ROOT / "case_truth_summary.sql"
PACKAGE_EXPECTED_PATH = PACKAGE_ROOT / "case_truth_summary_expected.json"
PACKAGE_ATTRIBUTION_PATH = PACKAGE_ROOT / "SOURCE_ATTRIBUTION.md"
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_kernel import (  # noqa: E402
    COMPILER_VERSION,
    KERNEL_SCHEMA_VERSION,
    RECORD_SCHEMA_VERSION,
    build_atlas3_runtime_result,
    canonical_sha256,
    validate_atlas3_kernel,
)
from catalytic_earth.atlas_selection import (  # noqa: E402
    load_atlas3_selection,
    validate_atlas3_selection,
)
from catalytic_earth.atlas_source_adapters import (  # noqa: E402
    mcsa_residue_rows,
    read_mcsa_snapshot,
    read_pdb_snapshot,
    read_rhea_snapshot,
    read_uniprot_snapshot,
    residue_one_letter,
    select_mcsa_mechanism,
    uniprot_chain_ranges,
)
from catalytic_earth.atlas_sources import (  # noqa: E402
    load_atlas3_source_manifest,
    validate_atlas3_source_manifest,
)


TOP_SPEC_FIELDS = {
    "schema_version",
    "compiler_version",
    "selection_sha256",
    "source_snapshot_set_sha256",
    "cases",
    "claim_boundary",
}
CASE_FIELDS = {
    "case_id",
    "ec_number",
    "rhea_record_id",
    "net_reaction",
    "source_mechanism",
    "hypothesis",
}
NET_FIELDS = {
    "record_id",
    "evidence_keys",
    "counterevidence",
    "uncertainties",
    "claim_boundary",
}
SOURCE_FIELDS = {
    "record_id",
    "status",
    "mcsa_record_id",
    "mechanism_id",
    "step_transformations",
    "evidence_keys",
    "counterevidence",
    "uncertainties",
    "claim_boundary",
}
HYPOTHESIS_FIELDS = {
    "record_id",
    "evidence_keys",
    "steps",
    "sites",
    "counterevidence",
    "uncertainties",
    "claim_boundary",
}
COUNTER_FIELDS = {
    "counterevidence_id",
    "summary",
    "evidence_keys",
    "effect",
    "disposition",
}
STEP_SPEC_FIELDS = {
    "step_id",
    "order",
    "summary",
    "transformation",
    "catalyst_site_ids",
    "evidence_keys",
    "confidence",
    "source_step_id",
}
SITE_SPEC_FIELDS = {
    "site_id",
    "uniprot_id",
    "residue_name",
    "sequence_position",
    "numbering_system",
    "roles",
    "pdb_mapping",
    "evidence_keys",
    "mapping_status",
    "notes",
}


def _exact(value: Any, fields: set[str], context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    actual = set(value)
    if actual != fields:
        raise ValueError(
            f"{context} keys differ; missing={sorted(fields - actual)}, "
            f"extra={sorted(actual - fields)}"
        )
    return value


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _source_key(raw: str) -> tuple[str, str]:
    if not isinstance(raw, str) or "::" not in raw:
        raise ValueError(f"invalid source key: {raw!r}")
    source_id, record_id = raw.split("::", 1)
    if not source_id or not record_id:
        raise ValueError(f"invalid source key: {raw!r}")
    return source_id, record_id


def _evidence_id(raw: str) -> str:
    source_id, record_id = _source_key(raw)
    return f"source:{source_id}:{record_id}"


def _manifest_index(manifest: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (record["source_id"], record["record_id"]): record
        for record in manifest["records"]
    }


def _evidence(
    keys: Any,
    *,
    manifest_index: dict[tuple[str, str], dict[str, Any]],
    allowed_keys: set[tuple[str, str]],
    context: str,
) -> list[dict[str, Any]]:
    if not isinstance(keys, list) or not keys or any(not isinstance(key, str) for key in keys):
        raise ValueError(f"{context} must be a non-empty source-key list")
    if len(keys) != len(set(keys)):
        raise ValueError(f"{context} repeats a source key")
    output: list[dict[str, Any]] = []
    for raw in keys:
        key = _source_key(raw)
        if key not in allowed_keys:
            raise ValueError(f"{context} uses a source outside its frozen case: {key}")
        manifest = manifest_index.get(key)
        if manifest is None:
            raise ValueError(f"{context} source is absent from the snapshot manifest: {key}")
        output.append(
            {
                "evidence_id": _evidence_id(raw),
                "source_id": manifest["source_id"],
                "source_record_id": manifest["record_id"],
                "evidence_role": manifest["evidence_role"],
                "applicability": manifest["applicability"],
                "uri": manifest["uri"],
                "retrieval_status": manifest["retrieval_status"],
                "snapshot_sha256": manifest["snapshot_sha256"],
            }
        )
    return output


def _convert_counterevidence(value: Any, *, evidence_ids: set[str], context: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError(f"{context} must be a list")
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(value):
        item = _exact(raw, COUNTER_FIELDS, f"{context}[{index}]")
        resolved = [_evidence_id(key) for key in item["evidence_keys"]]
        if not resolved or not set(resolved).issubset(evidence_ids):
            raise ValueError(f"{context}[{index}] evidence does not resolve in the record")
        output.append(
            {
                "counterevidence_id": item["counterevidence_id"],
                "summary": item["summary"],
                "evidence_ids": resolved,
                "effect": item["effect"],
                "disposition": item["disposition"],
            }
        )
    return output


def _snapshot_path(
    manifest_index: dict[tuple[str, str], dict[str, Any]], source_id: str, record_id: str
) -> Path:
    record = manifest_index[source_id, record_id]
    relative = record["snapshot_path"]
    if not isinstance(relative, str):
        raise ValueError(f"{source_id} {record_id} is not a bundled snapshot")
    return ROOT / relative


def _scope(selected_case: dict[str, Any], ec_number: str) -> dict[str, Any]:
    direct_uniprot = sorted(
        handle["record_id"]
        for handle in selected_case["source_handles"]
        if handle["source_id"] == "UniProtKB" and handle["applicability"] == "direct"
    )
    direct_pdb = sorted(
        handle["record_id"]
        for handle in selected_case["source_handles"]
        if handle["source_id"] == "PDB" and handle["applicability"] == "direct"
    )
    return {
        "case_label": selected_case["label"],
        "organism": selected_case["organism"],
        "ec_number": ec_number,
        "uniprot_ids": direct_uniprot,
        "pdb_ids": direct_pdb,
        "assay_candidate": selected_case["assay_candidate"],
    }


def _record_provenance(
    *, selection_sha256: str, snapshot_set_sha256: str, spec_sha256: str
) -> dict[str, str]:
    return {
        "selection_sha256": selection_sha256,
        "source_snapshot_set_sha256": snapshot_set_sha256,
        "compilation_spec_sha256": spec_sha256,
        "compiler_version": COMPILER_VERSION,
    }


def _source_sites(
    entry: dict[str, Any],
    *,
    record_evidence: list[dict[str, Any]],
    manifest_index: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in mcsa_residue_rows(entry):
        key = (
            row["uniprot_id"],
            row["residue_name"],
            row["sequence_position"],
            row["pdb_id"],
            row["chain_id"],
            row["author_position"],
            row["label_position"],
        )
        if key not in grouped:
            grouped[key] = {**row, "roles": set(row["roles"])}
        else:
            grouped[key]["roles"].update(row["roles"])
    evidence_by_source = {
        (item["source_id"], item["source_record_id"]): item["evidence_id"]
        for item in record_evidence
    }
    mcsa_evidence = evidence_by_source[("M-CSA", entry["record_id"])]
    pdb_cache: dict[str, dict[str, Any]] = {}
    output: list[dict[str, Any]] = []
    for key in sorted(grouped, key=lambda item: (str(item[0]), int(item[2]), str(item[4]))):
        row = grouped[key]
        pdb_id = row["pdb_id"]
        pdb = pdb_cache.setdefault(
            pdb_id,
            read_pdb_snapshot(
                _snapshot_path(manifest_index, "PDB", pdb_id), pdb_id
            ),
        )
        coordinate = pdb["residues"].get((row["chain_id"], row["author_position"]))
        if coordinate is None:
            raise ValueError(f"M-CSA site is absent from {pdb_id} coordinates: {row}")
        if (
            residue_one_letter(coordinate["residue_name"])
            != residue_one_letter(row["residue_name"])
            or coordinate["label_position"] != row["label_position"]
        ):
            raise ValueError(f"M-CSA/PDB residue mapping differs: {row}")
        evidence_ids = [mcsa_evidence]
        for source_key in (
            ("PDB", pdb_id),
            ("UniProtKB", row["uniprot_id"]),
        ):
            if source_key in evidence_by_source:
                evidence_ids.append(evidence_by_source[source_key])
        natural = row["sequence_position"]
        author = row["author_position"]
        numbering_note = (
            f"M-CSA maps UniProt natural position {natural} to {pdb_id} "
            f"chain {row['chain_id']} author position {author} and mmCIF label "
            f"position {row['label_position']}."
        )
        output.append(
            {
                "site_id": (
                    f"{row['uniprot_id']}:"
                    f"{residue_one_letter(row['residue_name'])}{row['sequence_position']}"
                ),
                "uniprot_id": row["uniprot_id"],
                "residue_name": row["residue_name"],
                "sequence_position": row["sequence_position"],
                "numbering_system": "UniProt natural sequence",
                "roles": sorted(row["roles"]),
                "pdb_mapping": {
                    "pdb_id": pdb_id,
                    "chain_ids": [row["chain_id"]],
                    "author_position": author,
                    "label_position": row["label_position"],
                    "numbering_note": numbering_note,
                },
                "evidence_ids": evidence_ids,
                "mapping_status": "source_reported_and_coordinate_verified",
                "notes": "Roles and numbering are extracted from the checked M-CSA entry; coordinate residue identity was rechecked locally.",
            }
        )
    site_ids = [site["site_id"] for site in output]
    if len(site_ids) != len(set(site_ids)):
        raise ValueError(f"M-CSA site IDs remain duplicated after mapping: {site_ids}")
    return output


def _source_steps(
    mechanism: dict[str, Any],
    transformations: Any,
    *,
    mcsa_evidence_id: str,
) -> list[dict[str, Any]]:
    source_steps = [step for step in mechanism.get("steps", []) if not step.get("is_product")]
    if (
        not isinstance(transformations, list)
        or len(transformations) != len(source_steps)
        or any(not isinstance(item, str) or not item for item in transformations)
    ):
        raise ValueError("source step transformations do not exactly cover non-product steps")
    output: list[dict[str, Any]] = []
    for order, (step, transformation) in enumerate(
        zip(source_steps, transformations, strict=True), start=1
    ):
        if step.get("step_id") != order or not isinstance(step.get("description"), str):
            raise ValueError("M-CSA source steps are not contiguous or described")
        output.append(
            {
                "step_id": f"M{mechanism['mechanism_id']}:source-step:{order}",
                "order": order,
                "summary": step["description"],
                "transformation": transformation,
                "catalyst_site_ids": [],
                "evidence_ids": [mcsa_evidence_id],
                "confidence": "source_curated",
                "source_step_id": step["step_id"],
            }
        )
    return output


def _hypothesis_steps(
    value: Any, *, evidence_ids: set[str]
) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ValueError("hypothesis.steps must be non-empty")
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(value):
        step = _exact(raw, STEP_SPEC_FIELDS, f"hypothesis.steps[{index}]")
        resolved = [_evidence_id(key) for key in step["evidence_keys"]]
        if not resolved or not set(resolved).issubset(evidence_ids):
            raise ValueError(f"hypothesis.steps[{index}] evidence does not resolve")
        output.append(
            {
                "step_id": step["step_id"],
                "order": step["order"],
                "summary": step["summary"],
                "transformation": step["transformation"],
                "catalyst_site_ids": copy.deepcopy(step["catalyst_site_ids"]),
                "evidence_ids": resolved,
                "confidence": step["confidence"],
                "source_step_id": step["source_step_id"],
            }
        )
    return output


def _hypothesis_sites(
    value: Any,
    *,
    evidence_ids: set[str],
    manifest_index: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ValueError("hypothesis.sites must be non-empty")
    uniprot_cache: dict[str, dict[str, Any]] = {}
    pdb_cache: dict[str, dict[str, Any]] = {}
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(value):
        site = _exact(raw, SITE_SPEC_FIELDS, f"hypothesis.sites[{index}]")
        uniprot_id = site["uniprot_id"]
        uniprot = uniprot_cache.setdefault(
            uniprot_id,
            read_uniprot_snapshot(
                _snapshot_path(manifest_index, "UniProtKB", uniprot_id), uniprot_id
            ),
        )
        position = site["sequence_position"]
        if (
            not isinstance(position, int)
            or position <= 0
            or position > len(uniprot["sequence"])
            or uniprot["sequence"][position - 1]
            != residue_one_letter(site["residue_name"])
        ):
            raise ValueError(f"hypothesis site differs from UniProt sequence: {site['site_id']}")
        mapping = site["pdb_mapping"]
        pdb_id = mapping["pdb_id"]
        pdb = pdb_cache.setdefault(
            pdb_id,
            read_pdb_snapshot(_snapshot_path(manifest_index, "PDB", pdb_id), pdb_id),
        )
        properties = uniprot["pdb_cross_references"].get(pdb_id)
        if properties is None:
            raise ValueError(f"{uniprot_id} does not cross-reference {pdb_id}")
        ranges = {item["chain_id"]: item for item in uniprot_chain_ranges(properties)}
        for chain_id in mapping["chain_ids"]:
            chain_range = ranges.get(chain_id)
            if chain_range is None or not (
                chain_range["uniprot_start"] <= position <= chain_range["uniprot_end"]
            ):
                raise ValueError(f"site {site['site_id']} is outside the UniProt/PDB chain range")
            expected_label = position - chain_range["uniprot_start"] + 1
            if mapping["label_position"] != expected_label:
                raise ValueError(f"site {site['site_id']} has the wrong mmCIF label position")
            coordinate = pdb["residues"].get((chain_id, mapping["author_position"]))
            if (
                coordinate is None
                or coordinate["label_position"] != mapping["label_position"]
                or residue_one_letter(coordinate["residue_name"])
                != residue_one_letter(site["residue_name"])
            ):
                raise ValueError(f"site {site['site_id']} differs from {pdb_id} coordinates")
        resolved = [_evidence_id(key) for key in site["evidence_keys"]]
        if not resolved or not set(resolved).issubset(evidence_ids):
            raise ValueError(f"hypothesis site evidence does not resolve: {site['site_id']}")
        output.append(
            {
                "site_id": site["site_id"],
                "uniprot_id": uniprot_id,
                "residue_name": site["residue_name"],
                "sequence_position": position,
                "numbering_system": site["numbering_system"],
                "roles": copy.deepcopy(site["roles"]),
                "pdb_mapping": copy.deepcopy(mapping),
                "evidence_ids": resolved,
                "mapping_status": site["mapping_status"],
                "notes": site["notes"],
            }
        )
    return output


def _record(
    *,
    record_id: str,
    case_id: str,
    object_type: str,
    label: str,
    status: str,
    scope: dict[str, Any],
    reaction: dict[str, Any],
    steps: list[dict[str, Any]],
    sites: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    counterevidence: list[dict[str, Any]],
    uncertainties: list[dict[str, Any]],
    claim_boundary: dict[str, Any],
    provenance: dict[str, str],
) -> dict[str, Any]:
    return {
        "schema_version": RECORD_SCHEMA_VERSION,
        "record_id": record_id,
        "case_id": case_id,
        "object_type": object_type,
        "evidence_tier": {"net_reaction": 0, "source_mechanism": 1, "mechanism_hypothesis": 2}[
            object_type
        ],
        "label": label,
        "fixture_only": False,
        "status": status,
        "biological_scope": copy.deepcopy(scope),
        "reaction": copy.deepcopy(reaction),
        "mechanism_steps": steps,
        "sites": sites,
        "evidence": evidence,
        "counterevidence": counterevidence,
        "uncertainties": copy.deepcopy(uncertainties),
        "claim_boundary": copy.deepcopy(claim_boundary),
        "provenance": copy.deepcopy(provenance),
    }


def build_kernel() -> dict[str, Any]:
    selection = load_atlas3_selection(SELECTION_PATH)
    selection_summary = validate_atlas3_selection(selection)
    manifest = load_atlas3_source_manifest(
        MANIFEST_PATH, repo_root=ROOT, selection=selection
    )
    validate_atlas3_source_manifest(manifest, repo_root=ROOT, selection=selection)
    manifest_index = _manifest_index(manifest)
    spec = _exact(json.loads(SPEC_PATH.read_text(encoding="utf-8")), TOP_SPEC_FIELDS, "spec")
    if spec["schema_version"] != "catalytic-earth.atlas3-compilation-spec.v1":
        raise ValueError("unsupported Atlas-3 compilation spec")
    if spec["compiler_version"] != COMPILER_VERSION:
        raise ValueError("compilation spec/compiler version differs")
    if spec["selection_sha256"] != selection_summary["selection_sha256"]:
        raise ValueError("compilation spec is not bound to the frozen selection")
    if spec["source_snapshot_set_sha256"] != manifest["snapshot_set_sha256"]:
        raise ValueError("compilation spec is not bound to the checked source set")
    spec_sha256 = canonical_sha256(spec)
    provenance = _record_provenance(
        selection_sha256=spec["selection_sha256"],
        snapshot_set_sha256=spec["source_snapshot_set_sha256"],
        spec_sha256=spec_sha256,
    )
    selected_by_id = {case["case_id"]: case for case in selection["cases"]}
    raw_cases = spec["cases"]
    if not isinstance(raw_cases, list) or len(raw_cases) != 3:
        raise ValueError("compilation spec must contain three cases")
    records: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()
    for case_index, raw_case in enumerate(raw_cases):
        case = _exact(raw_case, CASE_FIELDS, f"spec.cases[{case_index}]")
        case_id = case["case_id"]
        if case_id in seen_case_ids or case_id not in selected_by_id:
            raise ValueError(f"invalid or duplicate compilation case: {case_id}")
        seen_case_ids.add(case_id)
        selected = selected_by_id[case_id]
        allowed_keys = {
            (handle["source_id"], handle["record_id"])
            for handle in selected["source_handles"]
        }
        reaction_snapshot = _snapshot_path(
            manifest_index, "Rhea", case["rhea_record_id"]
        )
        extracted_reaction = read_rhea_snapshot(
            reaction_snapshot, case["rhea_record_id"]
        )
        if extracted_reaction["ec_number"] != case["ec_number"]:
            raise ValueError(f"{case_id} EC differs from Rhea")
        if sorted(
            participant["chebi_id"] for participant in extracted_reaction["participants"]
        ) != sorted(selected["reaction_participant_ids"]):
            raise ValueError(f"{case_id} participants differ from selection/Rhea")
        reaction = {
            key: extracted_reaction[key]
            for key in (
                "source_id",
                "source_record_id",
                "directionality",
                "equation",
                "participants",
            )
        }
        scope = _scope(selected, case["ec_number"])

        net = _exact(case["net_reaction"], NET_FIELDS, f"{case_id}.net_reaction")
        net_evidence = _evidence(
            net["evidence_keys"],
            manifest_index=manifest_index,
            allowed_keys=allowed_keys,
            context=f"{case_id}.net_reaction.evidence_keys",
        )
        net_evidence_ids = {item["evidence_id"] for item in net_evidence}
        records.append(
            _record(
                record_id=net["record_id"],
                case_id=case_id,
                object_type="net_reaction",
                label=f"{selected['label']} net reaction",
                status="source_assertion",
                scope=scope,
                reaction=reaction,
                steps=[],
                sites=[],
                evidence=net_evidence,
                counterevidence=_convert_counterevidence(
                    net["counterevidence"],
                    evidence_ids=net_evidence_ids,
                    context=f"{case_id}.net_reaction.counterevidence",
                ),
                uncertainties=net["uncertainties"],
                claim_boundary=net["claim_boundary"],
                provenance=provenance,
            )
        )

        source = _exact(
            case["source_mechanism"], SOURCE_FIELDS, f"{case_id}.source_mechanism"
        )
        source_evidence = _evidence(
            source["evidence_keys"],
            manifest_index=manifest_index,
            allowed_keys=allowed_keys,
            context=f"{case_id}.source_mechanism.evidence_keys",
        )
        source_evidence_ids = {item["evidence_id"] for item in source_evidence}
        mcsa_entry = read_mcsa_snapshot(
            _snapshot_path(manifest_index, "M-CSA", source["mcsa_record_id"]),
            source["mcsa_record_id"],
        )
        if source["status"] == "curated_source_proposal":
            direct_uniprot = set(scope["uniprot_ids"])
            if set(mcsa_entry["proteins"]) != direct_uniprot:
                raise ValueError(f"{case_id} direct M-CSA proteins differ")
            mechanism = select_mcsa_mechanism(mcsa_entry, source["mechanism_id"])
            if mechanism["rating"] != 3:
                raise ValueError(f"{case_id} selected source proposal is not three-star")
            source_steps = _source_steps(
                mechanism,
                source["step_transformations"],
                mcsa_evidence_id=_evidence_id(f"M-CSA::{source['mcsa_record_id']}"),
            )
            source_sites = _source_sites(
                mcsa_entry,
                record_evidence=source_evidence,
                manifest_index=manifest_index,
            )
        elif source["status"] == "abstained_no_direct_source_mechanism":
            if source["mechanism_id"] is not None or source["step_transformations"]:
                raise ValueError(f"{case_id} abstaining source object cannot select a mechanism")
            if set(mcsa_entry["proteins"]) & set(scope["uniprot_ids"]):
                raise ValueError(f"{case_id} counterexample unexpectedly matches direct protein")
            source_steps = []
            source_sites = []
        else:
            raise ValueError(f"{case_id} source status is unsupported")
        records.append(
            _record(
                record_id=source["record_id"],
                case_id=case_id,
                object_type="source_mechanism",
                label=f"{selected['label']} source mechanism",
                status=source["status"],
                scope=scope,
                reaction=reaction,
                steps=source_steps,
                sites=source_sites,
                evidence=source_evidence,
                counterevidence=_convert_counterevidence(
                    source["counterevidence"],
                    evidence_ids=source_evidence_ids,
                    context=f"{case_id}.source_mechanism.counterevidence",
                ),
                uncertainties=source["uncertainties"],
                claim_boundary=source["claim_boundary"],
                provenance=provenance,
            )
        )

        hypothesis = _exact(
            case["hypothesis"], HYPOTHESIS_FIELDS, f"{case_id}.hypothesis"
        )
        if hypothesis["record_id"] != selected["target_record_id"]:
            raise ValueError(f"{case_id} hypothesis target differs from selection")
        hypothesis_evidence = _evidence(
            hypothesis["evidence_keys"],
            manifest_index=manifest_index,
            allowed_keys=allowed_keys,
            context=f"{case_id}.hypothesis.evidence_keys",
        )
        hypothesis_evidence_ids = {
            item["evidence_id"] for item in hypothesis_evidence
        }
        hypothesis_steps = _hypothesis_steps(
            hypothesis["steps"], evidence_ids=hypothesis_evidence_ids
        )
        hypothesis_sites = _hypothesis_sites(
            hypothesis["sites"],
            evidence_ids=hypothesis_evidence_ids,
            manifest_index=manifest_index,
        )
        records.append(
            _record(
                record_id=hypothesis["record_id"],
                case_id=case_id,
                object_type="mechanism_hypothesis",
                label=f"{selected['label']} grounded hypothesis",
                status="bounded_hypothesis",
                scope=scope,
                reaction=reaction,
                steps=hypothesis_steps,
                sites=hypothesis_sites,
                evidence=hypothesis_evidence,
                counterevidence=_convert_counterevidence(
                    hypothesis["counterevidence"],
                    evidence_ids=hypothesis_evidence_ids,
                    context=f"{case_id}.hypothesis.counterevidence",
                ),
                uncertainties=hypothesis["uncertainties"],
                claim_boundary=hypothesis["claim_boundary"],
                provenance=provenance,
            )
        )

    if seen_case_ids != set(selected_by_id):
        raise ValueError("compilation case set differs from selection")
    kernel = {
        "schema_version": KERNEL_SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
        "selection_sha256": spec["selection_sha256"],
        "source_snapshot_set_sha256": spec["source_snapshot_set_sha256"],
        "compilation_spec_sha256": spec_sha256,
        "source_manifest_retrieved_at": manifest["retrieved_at"],
        "case_count": 3,
        "record_count": 9,
        "records": records,
        "claim_boundary": copy.deepcopy(spec["claim_boundary"]),
    }
    validate_atlas3_kernel(
        kernel,
        selection=selection,
        source_manifest=manifest,
    )
    return kernel


def build_expected(kernel: dict[str, Any], query_sql: str) -> dict[str, Any]:
    runtime = build_atlas3_runtime_result(kernel, query_sql)
    return {
        "schema_version": "catalytic-earth.atlas3-expected.v1",
        "kernel_sha256": runtime["kernel_sha256"],
        "query_sha256": runtime["query_sha256"],
        "runtime_result_sha256": canonical_sha256(runtime),
        "query_rows": runtime["query_rows"],
        "what_it_claims": "Deterministic reproduction of the first three-case, nine-object biological Atlas kernel and its local truth-boundary query.",
        "what_it_does_not_claim": "This is not biological validation, an accuracy benchmark, Atlas-scale coverage, prospective discovery, or a completed assay.",
    }


def _outputs() -> dict[Path, bytes]:
    kernel = build_kernel()
    query_sql = QUERY_PATH.read_text(encoding="utf-8").replace("\r\n", "\n").replace(
        "\r", "\n"
    )
    if not query_sql.endswith("\n"):
        query_sql += "\n"
    expected = build_expected(kernel, query_sql)
    kernel_bytes = _json_bytes(kernel)
    expected_bytes = _json_bytes(expected)
    query_bytes = query_sql.encode("utf-8")
    attribution_bytes = ATTRIBUTION_PATH.read_bytes().replace(b"\r\n", b"\n").replace(
        b"\r", b"\n"
    )
    return {
        KERNEL_PATH: kernel_bytes,
        EXPECTED_PATH: expected_bytes,
        PACKAGE_KERNEL_PATH: kernel_bytes,
        PACKAGE_QUERY_PATH: query_bytes,
        PACKAGE_EXPECTED_PATH: expected_bytes,
        PACKAGE_ATTRIBUTION_PATH: attribution_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = _outputs()
    if args.check:
        stale = [
            path.relative_to(ROOT).as_posix()
            for path, expected in outputs.items()
            if not path.is_file() or path.read_bytes() != expected
        ]
        if stale:
            raise SystemExit(f"Atlas-3 kernel outputs are stale: {stale}")
        print("Atlas-3 kernel outputs are current")
        return 0
    for path, raw in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    kernel = json.loads(outputs[KERNEL_PATH])
    summary = validate_atlas3_kernel(kernel)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
