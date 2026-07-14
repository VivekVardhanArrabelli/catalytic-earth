"""Compile and verify the seven-case Atlas-10 extension without mutating Atlas-3."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
ATLAS_ROOT = ROOT / "data/atlas/atlas10"
MANIFEST_PATH = ATLAS_ROOT / "source_manifest.json"
SPEC_PATH = ATLAS_ROOT / "compilation_spec.json"
KERNEL_PATH = ATLAS_ROOT / "kernel.json"
INHERITED_KERNEL_PATH = ROOT / "data/atlas/atlas3/kernel.json"
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas10_kernel import (  # noqa: E402
    COMPILER_VERSION,
    KERNEL_SCHEMA_VERSION,
    RECORD_SCHEMA_VERSION,
    canonical_sha256,
    validate_atlas10_compilation_spec,
    validate_atlas10_kernel,
)
from catalytic_earth.atlas10_selection import (  # noqa: E402
    load_atlas10_selection,
    validate_atlas10_selection,
)
from catalytic_earth.atlas10_source_adapters import (  # noqa: E402
    mcsa_gap_participants,
    mcsa_reference_residue_rows,
    parse_mcsa_scheme_flows,
    read_atlas10_mcsa_snapshot,
    read_atlas10_rhea_snapshot,
)
from catalytic_earth.atlas10_sources import (  # noqa: E402
    load_atlas10_source_manifest,
)
from catalytic_earth.atlas_source_adapters import (  # noqa: E402
    read_pdb_snapshot,
    read_uniprot_snapshot,
    residue_one_letter,
    uniprot_chain_ranges,
)


EXPECTED_INHERITED_FILE_SHA256 = (
    "0733a029b3eaa0900ff4124276c2060f94204ce3f3bf0b9bcf2c80e7589d674b"
)
RESIDUE_TOKEN = re.compile(
    r"\b(Ala|Arg|Asn|Asp|Cys|Gln|Glu|Gly|His|Ile|Leu|Lys|Met|Phe|Pro|Ser|Thr|Trp|Tyr|Val)\s*(\d+)\b",
    re.IGNORECASE,
)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest_index(manifest: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (record["source_id"], record["record_id"]): record
        for record in manifest["records"]
    }


def _binding_index(
    manifest: dict[str, Any],
) -> dict[tuple[str, str, str], dict[str, Any]]:
    return {
        (binding["case_id"], binding["source_id"], binding["record_id"]): binding
        for binding in manifest["bindings"]
    }


def _snapshot_path(
    manifest_index: dict[tuple[str, str], dict[str, Any]],
    source_id: str,
    record_id: str,
) -> Path:
    record = manifest_index[source_id, record_id]
    relative = record["snapshot_path"]
    if not isinstance(relative, str):
        raise ValueError(f"{source_id} {record_id} is not a bundled source snapshot")
    return ROOT / relative


def _evidence_id(source_id: str, record_id: str) -> str:
    return f"source:{source_id}:{record_id}"


def _case_evidence(
    selected: dict[str, Any],
    *,
    manifest_index: dict[tuple[str, str], dict[str, Any]],
    bindings: dict[tuple[str, str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for handle in selected["source_handles"]:
        key = handle["source_id"], handle["record_id"]
        record = manifest_index[key]
        binding = bindings[(selected["case_id"], *key)]
        output.append(
            {
                "evidence_id": _evidence_id(*key),
                "source_id": key[0],
                "source_record_id": key[1],
                "evidence_role": binding["evidence_role"],
                "applicability": binding["applicability"],
                "uri": record["uri"],
                "retrieval_status": record["retrieval_status"],
                "snapshot_sha256": record["snapshot_sha256"],
            }
        )
    return output


def _scope(selected: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_label": selected["label"],
        "organism": selected["organism"],
        "ec_number": selected["ec_number"],
        "uniprot_ids": sorted(
            handle["record_id"]
            for handle in selected["source_handles"]
            if handle["source_id"] == "UniProtKB"
        ),
        "direct_pdb_ids": sorted(
            handle["record_id"]
            for handle in selected["source_handles"]
            if handle["source_id"] == "PDB" and handle["applicability"] == "direct"
        ),
        "fold_classification_ids": selected["fold_classification_ids"],
        "relationship_group_ids": selected["relationship_group_ids"],
        "assay_candidate": False,
        "fingerprint_bridge": selected["fingerprint_bridge"],
    }


def _reaction(
    selected: dict[str, Any],
    entry: dict[str, Any],
    *,
    manifest_index: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    rhea_id = next(
        handle["record_id"]
        for handle in selected["source_handles"]
        if handle["source_id"] == "Rhea"
    )
    reaction = read_atlas10_rhea_snapshot(
        _snapshot_path(manifest_index, "Rhea", rhea_id),
        rhea_id,
        selected_participant_ids=set(selected["reaction_participant_ids"]),
    )
    if reaction["source_status"] == "documented_query_gap":
        reaction["participants"] = mcsa_gap_participants(
            entry,
            selected_participant_ids=set(selected["reaction_participant_ids"]),
        )
    if reaction["ec_number"] != selected["ec_number"]:
        raise ValueError(f"{selected['case_id']} reaction EC differs from selection")
    return reaction


def _find_coordinate_by_label(
    pdb: dict[str, Any], chain_id: str, label_position: int
) -> dict[str, Any]:
    matches = [
        residue
        for residue in pdb["residues"].values()
        if residue["chain_id"] == chain_id and residue["label_position"] == label_position
    ]
    if len(matches) != 1:
        raise ValueError(
            f"{pdb['pdb_id']} chain {chain_id} label {label_position} has {len(matches)} coordinates"
        )
    return matches[0]


def _sites(
    selected: dict[str, Any],
    entry: dict[str, Any],
    *,
    manifest_index: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    uniprot_id = next(
        handle["record_id"]
        for handle in selected["source_handles"]
        if handle["source_id"] == "UniProtKB"
    )
    uniprot = read_uniprot_snapshot(
        _snapshot_path(manifest_index, "UniProtKB", uniprot_id), uniprot_id
    )
    if uniprot["organism"] != selected["organism"]:
        raise ValueError(f"{selected['case_id']} UniProt organism differs from selection")
    pdb_applicability = {
        handle["record_id"]: handle["applicability"]
        for handle in selected["source_handles"]
        if handle["source_id"] == "PDB"
    }
    pdb_cache = {
        pdb_id: read_pdb_snapshot(
            _snapshot_path(manifest_index, "PDB", pdb_id), pdb_id
        )
        for pdb_id in pdb_applicability
    }
    grouped: dict[tuple[str, str, int], dict[str, Any]] = {}
    for row in mcsa_reference_residue_rows(entry):
        if row["uniprot_id"] != uniprot_id:
            raise ValueError(f"{selected['case_id']} M-CSA reference UniProt differs")
        natural_position = row["sequence_position"]
        if not isinstance(natural_position, int) or natural_position <= 0:
            raise ValueError(f"{selected['case_id']} M-CSA natural position is invalid")
        one_letter = residue_one_letter(row["residue_name"])
        if uniprot["sequence"][natural_position - 1] != one_letter:
            raise ValueError(f"{selected['case_id']} M-CSA/UniProt residue identity differs: {row}")
        source_pdb = pdb_cache.get(row["pdb_id"])
        if source_pdb is None:
            raise ValueError(f"{selected['case_id']} M-CSA PDB lacks a frozen snapshot: {row}")
        coordinate = source_pdb["residues"].get((row["chain_id"], row["author_position"]))
        if coordinate is None:
            raise ValueError(f"{selected['case_id']} M-CSA site is absent from coordinates: {row}")
        if (
            coordinate["label_position"] != row["label_position"]
            or residue_one_letter(coordinate["residue_name"]) != one_letter
        ):
            raise ValueError(f"{selected['case_id']} M-CSA/mmCIF site mapping differs: {row}")
        key = uniprot_id, one_letter, natural_position
        item = grouped.setdefault(
            key,
            {
                "residue_name": row["residue_name"],
                "roles": set(),
                "mappings": {},
            },
        )
        item["roles"].update(row["roles"])
        mapping_key = row["pdb_id"], row["chain_id"]
        mapping = {
            "pdb_id": row["pdb_id"],
            "chain_id": row["chain_id"],
            "author_position": row["author_position"],
            "label_position": row["label_position"],
            "applicability": pdb_applicability[row["pdb_id"]],
            "mapping_basis": "mcsa_reference_and_coordinate",
            "numbering_note": (
                f"M-CSA maps UniProt natural position {natural_position} to "
                f"{row['pdb_id']} chain {row['chain_id']} author position "
                f"{row['author_position']} and mmCIF label position {row['label_position']}; "
                "the residue identity was checked in the frozen coordinate file."
            ),
        }
        previous = item["mappings"].get(mapping_key)
        if previous is not None and previous != mapping:
            raise ValueError(f"{selected['case_id']} M-CSA mappings conflict for {key}")
        item["mappings"][mapping_key] = mapping

    for (site_uniprot, one_letter, natural_position), item in grouped.items():
        for pdb_id, applicability in pdb_applicability.items():
            properties = uniprot["pdb_cross_references"].get(pdb_id)
            if properties is None:
                raise ValueError(f"{selected['case_id']} UniProt lacks PDB cross-reference {pdb_id}")
            ranges = uniprot_chain_ranges(properties)
            if not ranges:
                raise ValueError(f"{selected['case_id']} UniProt lacks chain ranges for {pdb_id}")
            for chain_range in ranges:
                if not (
                    chain_range["uniprot_start"]
                    <= natural_position
                    <= chain_range["uniprot_end"]
                ):
                    continue
                label_position = natural_position - chain_range["uniprot_start"] + 1
                coordinate = _find_coordinate_by_label(
                    pdb_cache[pdb_id], chain_range["chain_id"], label_position
                )
                if residue_one_letter(coordinate["residue_name"]) != one_letter:
                    raise ValueError(
                        f"{selected['case_id']} UniProt/mmCIF identity differs for "
                        f"{site_uniprot}:{one_letter}{natural_position} in {pdb_id}"
                    )
                mapping_key = pdb_id, chain_range["chain_id"]
                if mapping_key in item["mappings"]:
                    existing = item["mappings"][mapping_key]
                    if (
                        existing["author_position"] != coordinate["author_position"]
                        or existing["label_position"] != coordinate["label_position"]
                    ):
                        raise ValueError(
                            f"{selected['case_id']} source and independent mappings conflict"
                        )
                    continue
                item["mappings"][mapping_key] = {
                    "pdb_id": pdb_id,
                    "chain_id": chain_range["chain_id"],
                    "author_position": coordinate["author_position"],
                    "label_position": coordinate["label_position"],
                    "applicability": applicability,
                    "mapping_basis": "uniprot_chain_range_and_coordinate",
                    "numbering_note": (
                        f"UniProt maps {pdb_id} chain {chain_range['chain_id']} to natural "
                        f"positions {chain_range['uniprot_start']}-{chain_range['uniprot_end']}; "
                        f"natural position {natural_position} resolves to mmCIF label "
                        f"{coordinate['label_position']} and author position "
                        f"{coordinate['author_position']} in the frozen coordinate file."
                    ),
                }

    output: list[dict[str, Any]] = []
    for (site_uniprot, one_letter, natural_position), item in sorted(
        grouped.items(), key=lambda pair: (pair[0][2], pair[0][1])
    ):
        mappings = [item["mappings"][key] for key in sorted(item["mappings"])]
        evidence_ids = [
            _evidence_id("M-CSA", entry["record_id"]),
            _evidence_id("UniProtKB", site_uniprot),
            *[_evidence_id("PDB", pdb_id) for pdb_id in sorted({m["pdb_id"] for m in mappings})],
        ]
        output.append(
            {
                "site_id": f"{site_uniprot}:{one_letter}{natural_position}",
                "uniprot_id": site_uniprot,
                "residue_name": item["residue_name"],
                "sequence_position": natural_position,
                "numbering_system": "UniProt natural sequence",
                "roles": sorted(item["roles"]),
                "pdb_mappings": mappings,
                "evidence_ids": evidence_ids,
                "mapping_status": "source_and_coordinate_verified",
                "notes": (
                    "M-CSA reference numbering, UniProt natural-sequence identity, and every "
                    "listed local mmCIF coordinate were checked. An empty roles list means the "
                    "source listed the residue without a role string."
                ),
            }
        )
    if not output:
        raise ValueError(f"{selected['case_id']} has no source-reference sites")
    return output


def _structures(
    selected: dict[str, Any],
    case_spec: dict[str, Any],
    *,
    manifest_index: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    uniprot_id = next(
        handle["record_id"]
        for handle in selected["source_handles"]
        if handle["source_id"] == "UniProtKB"
    )
    uniprot = read_uniprot_snapshot(
        _snapshot_path(manifest_index, "UniProtKB", uniprot_id), uniprot_id
    )
    output: list[dict[str, Any]] = []
    for context in case_spec["structure_contexts"]:
        pdb_id = context["pdb_id"]
        pdb = read_pdb_snapshot(_snapshot_path(manifest_index, "PDB", pdb_id), pdb_id)
        properties = uniprot["pdb_cross_references"].get(pdb_id)
        if properties is None:
            raise ValueError(f"{selected['case_id']} UniProt lacks {pdb_id} cross-reference")
        output.append(
            {
                "pdb_id": pdb_id,
                "applicability": context["applicability"],
                "context_flags": context["context_flags"],
                "limitation": context["limitation"],
                "experimental_method": pdb["method"],
                "resolution_angstrom": pdb["resolution_angstrom"],
                "uniprot_chain_ranges": uniprot_chain_ranges(properties),
                "evidence_ids": [
                    _evidence_id("PDB", pdb_id),
                    _evidence_id("UniProtKB", uniprot_id),
                ],
            }
        )
    return output


def _catalyst_site_ids(summary: str, sites: list[dict[str, Any]]) -> list[str]:
    candidates: dict[tuple[str, int], set[str]] = defaultdict(set)
    for site in sites:
        three = site["residue_name"].lower()
        candidates[(three, site["sequence_position"])].add(site["site_id"])
        for mapping in site["pdb_mappings"]:
            candidates[(three, mapping["author_position"])].add(site["site_id"])
    resolved: set[str] = set()
    for residue_name, position_text in RESIDUE_TOKEN.findall(summary):
        matches = candidates.get((residue_name.lower(), int(position_text)), set())
        if len(matches) == 1:
            resolved.update(matches)
    return sorted(resolved)


def _proposals(
    case_spec: dict[str, Any],
    entry: dict[str, Any],
    sites: list[dict[str, Any]],
    *,
    proposal_scope: str,
) -> list[dict[str, Any]]:
    mechanisms = {
        mechanism["mechanism_id"]: mechanism for mechanism in entry["mechanisms"]
    }
    output: list[dict[str, Any]] = []
    for mechanism_id in case_spec["mechanism_ids"]:
        mechanism = mechanisms.get(mechanism_id)
        if mechanism is None:
            raise ValueError(
                f"{case_spec['case_id']} lacks M-CSA mechanism {mechanism_id}"
            )
        if mechanism["rating"] != case_spec["expected_ratings"][str(mechanism_id)]:
            raise ValueError(f"{case_spec['case_id']} M-CSA rating differs")
        is_detailed = mechanism["is_detailed"]
        expected_detailed = case_spec["expected_granularity"] != "non_detailed"
        if is_detailed is not expected_detailed:
            raise ValueError(f"{case_spec['case_id']} M-CSA granularity differs")
        mechanism_steps: list[dict[str, Any]] = []
        terminal_ids: list[int] = []
        annotation_texts: list[str] = []
        issues: list[dict[str, Any]] = []
        for source_step in mechanism.get("steps", []):
            scheme = entry["scheme_index"][(mechanism_id, source_step["step_id"])]
            parsed = parse_mcsa_scheme_flows(scheme)
            if source_step["is_product"]:
                terminal_ids.append(source_step["step_id"])
                continue
            if not is_detailed:
                annotation_texts.append(source_step["description"])
                issues.append(
                    {
                        "source_step_id": source_step["step_id"],
                        "status": parsed["scheme_status"],
                        "source_url": scheme["source_url"],
                    }
                )
                continue
            if parsed["scheme_status"] != "source_curved_arrows_preserved":
                raise ValueError(f"{case_spec['case_id']} detailed scheme is unavailable")
            mechanism_steps.append(
                {
                    "step_id": (
                        f"{case_spec['case_id']}.mcsa-{entry['record_id']}."
                        f"mechanism-{mechanism_id}.step-{source_step['step_id']}"
                    ),
                    "order": len(mechanism_steps) + 1,
                    "summary": source_step["description"],
                    "source_step_id": source_step["step_id"],
                    "is_inferred": bool(
                        re.search(r"\binferred\b", source_step["description"], re.IGNORECASE)
                    ),
                    "catalyst_site_ids": _catalyst_site_ids(
                        source_step["description"], sites
                    ),
                    "evidence_ids": [_evidence_id("M-CSA", entry["record_id"])],
                    "source_scheme_sha256": parsed["scheme_sha256"],
                    "electron_flows": parsed["electron_flows"],
                    "electron_flow_semantics": (
                        "source_ordered_curved_arrow_endpoints_not_atom_mapped_bond_edits"
                    ),
                    "atom_mapping_status": "not_inferred",
                    "bond_edit_status": "not_compiled_from_unmapped_source_scheme",
                }
            )
        if not is_detailed and entry.get("description"):
            annotation_texts.insert(0, entry["description"])
        annotation_texts = list(dict.fromkeys(annotation_texts))
        output.append(
            {
                "proposal_id": (
                    f"{case_spec['case_id']}.mcsa-{entry['record_id']}.mechanism-{mechanism_id}"
                ),
                "source_id": "M-CSA",
                "source_record_id": entry["record_id"],
                "source_mechanism_id": mechanism_id,
                "rating": mechanism["rating"],
                "is_detailed": is_detailed,
                "preferred": mechanism_id in case_spec["preferred_mechanism_ids"],
                "proposal_scope": proposal_scope,
                "components_summary": mechanism["components_summary"],
                "mechanism_text": mechanism["mechanism_text"],
                "annotation_texts": annotation_texts,
                "mechanism_steps": mechanism_steps,
                "terminal_state_source_step_ids": terminal_ids,
                "structured_detail_status": (
                    "source_curved_arrows_preserved_no_atom_mapping_inference"
                    if is_detailed
                    else "abstained_non_detailed_source"
                ),
                "scheme_retrieval_issues": issues,
            }
        )
    return output


def _counterevidence(
    selected: dict[str, Any],
    case_spec: dict[str, Any],
    reaction: dict[str, Any],
    *,
    include_structures: bool,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    if reaction["source_status"] == "documented_query_gap":
        rhea_id = next(
            handle["record_id"]
            for handle in selected["source_handles"]
            if handle["source_id"] == "Rhea"
        )
        output.append(
            {
                "counterevidence_id": f"{selected['case_id']}.rhea-source-gap",
                "summary": reaction["gap_context"]["interpretation"],
                "evidence_ids": [_evidence_id("Rhea", rhea_id)],
                "effect": "Prevents attribution of a direct canonical Rhea reaction identifier.",
                "disposition": "Preserve the zero-row query and label M-CSA participants as source-scoped context.",
            }
        )
    if include_structures:
        for context in case_spec["structure_contexts"]:
            output.append(
                {
                    "counterevidence_id": (
                        f"{selected['case_id']}.structure-{context['pdb_id'].lower()}-limit"
                    ),
                    "summary": context["limitation"],
                    "evidence_ids": [_evidence_id("PDB", context["pdb_id"])],
                    "effect": "Limits mechanistic generalization from this static structural context.",
                    "disposition": "Retain the structure with its explicit applicability and context flags.",
                }
            )
    if include_structures and selected["case_id"] == "atlas10.hewl-chicken.covalent-glycosidase":
        output.append(
            {
                "counterevidence_id": f"{selected['case_id']}.source-alternatives",
                "summary": "M-CSA preserves two detailed proposals with ratings 3 and 1, including a source description that calls the lower-rated Phillips route disproved.",
                "evidence_ids": [_evidence_id("M-CSA", "M0203")],
                "effect": "Prevents flattening source history into a single unqualified mechanism object.",
                "disposition": "Keep both proposals, ratings, wording, and preferred status queryable without independent adjudication.",
            }
        )
    if include_structures and selected["case_id"] == "atlas10.cyclophilin-a-human.isomerization":
        output.append(
            {
                "counterevidence_id": f"{selected['case_id']}.non-detailed-source",
                "summary": "M-CSA M0189 is explicitly non-detailed and its linked Marvin scheme returns HTTP 404 in the frozen acquisition.",
                "evidence_ids": [_evidence_id("M-CSA", "M0189")],
                "effect": "Blocks compilation of discrete electron-flow, atom-mapped, or bond-edit steps.",
                "disposition": "Retain source text, sites, reaction, and a mandatory zero-step detail abstention.",
            }
        )
    return output


def _uncertainties(selected: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "uncertainty_id": f"{selected['case_id']}.uncertainty-{index}",
            "summary": summary,
            "status": "open",
            "abstention": "Do not resolve this ambiguity beyond the frozen sources and explicit compilation rules.",
        }
        for index, summary in enumerate(selected["known_ambiguities"], 1)
    ]


def _detail_abstention(
    selected: dict[str, Any],
    *,
    basis_evidence_ids: list[str],
    non_detailed: bool,
) -> dict[str, Any]:
    unsupported = [
        "atom_mapped_bond_edits",
        "independent_mechanism_validation",
        "complete_turnover_trajectory",
    ]
    reason = (
        "The frozen source schemes preserve curved-arrow endpoints but do not establish a verified atom map, compiled bond-edit list, independent validation, or complete turnover trajectory."
    )
    if non_detailed:
        unsupported = [
            "atom_mapped_bond_edits",
            "discrete_electron_and_proton_transfer_steps",
            "covalent_intermediates",
            "ordered_elementary_steps",
            "universal_substrate_applicability",
            "independent_mechanism_validation",
            "complete_turnover_trajectory",
        ]
        reason = (
            "M-CSA explicitly marks the selected proposal non-detailed and the linked scheme was unavailable; rating 3 does not authorize fabrication of discrete chemistry."
        )
    return {
        "required": True,
        "reason": reason,
        "unsupported_fields": unsupported,
        "source_basis_evidence_ids": basis_evidence_ids,
    }


def _claim_boundary(
    selected: dict[str, Any], object_type: str, reaction_status: str
) -> dict[str, list[str]]:
    if object_type == "reaction_or_source_gap":
        support = (
            "The frozen Rhea record and its source-scoped participants are represented."
            if reaction_status == "direct_record"
            else "The frozen zero-row Rhea EC query and M-CSA-scoped participant context are represented without inventing a Rhea identifier."
        )
        return {
            "supports": [support],
            "does_not_support": [
                "An elementary mechanism, independently validated catalytic path, or generalized substrate scope."
            ],
        }
    if object_type == "source_annotation":
        return {
            "supports": [
                "A queryable projection of the selected M-CSA proposal text, rating, granularity, source steps or explicit non-detailed abstention, sites, and bounded structures."
            ],
            "does_not_support": [
                "Independent adjudication of the source proposal, atom-mapped bond edits, or a complete observed turnover trajectory."
            ],
        }
    return {
        "supports": [selected["success_condition"]],
        "does_not_support": [
            "Mechanism truth beyond the frozen sources, unrestricted transfer across proteins or substrates, or replacement of experimental validation."
        ],
    }


def _record(
    selected: dict[str, Any],
    case_spec: dict[str, Any],
    *,
    object_type: str,
    reaction: dict[str, Any],
    all_evidence: list[dict[str, Any]],
    sites: list[dict[str, Any]],
    structures: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
    provenance: dict[str, str],
) -> dict[str, Any]:
    target_suffix = selected["target_record_id"].removeprefix("mechanism:")
    if object_type == "reaction_or_source_gap":
        record_id = f"reaction:{target_suffix}"
        evidence_ids = [_evidence_id("Rhea", reaction["source_record_id"])] if reaction[
            "source_status"
        ] == "direct_record" else [
            _evidence_id(
                "Rhea",
                next(
                    handle["record_id"]
                    for handle in selected["source_handles"]
                    if handle["source_id"] == "Rhea"
                ),
            ),
            _evidence_id("M-CSA", case_spec["mcsa_record_id"]),
        ]
        evidence = [item for item in all_evidence if item["evidence_id"] in evidence_ids]
        record_sites: list[dict[str, Any]] = []
        record_structures: list[dict[str, Any]] = []
        record_proposals: list[dict[str, Any]] = []
        tier = 0
        status = (
            "source_assertion"
            if reaction["source_status"] == "direct_record"
            else "documented_source_gap"
        )
        granularity = "not_applicable"
        counterevidence = _counterevidence(
            selected, case_spec, reaction, include_structures=False
        )
    else:
        record_id = (
            f"source-annotation:{target_suffix}"
            if object_type == "source_annotation"
            else selected["target_record_id"]
        )
        evidence = copy.deepcopy(all_evidence)
        evidence_ids = [item["evidence_id"] for item in evidence]
        record_sites = copy.deepcopy(sites)
        record_structures = copy.deepcopy(structures)
        proposal_scope = (
            "source_curated"
            if object_type == "source_annotation"
            else "bounded_hypothesis_projection"
        )
        record_proposals = copy.deepcopy(proposals)
        for proposal in record_proposals:
            proposal["proposal_scope"] = proposal_scope
        tier = 1 if object_type == "source_annotation" else 2
        non_detailed = case_spec["expected_granularity"] == "non_detailed"
        status = (
            "curated_non_detailed_annotation"
            if object_type == "source_annotation" and non_detailed
            else "curated_source_annotation"
            if object_type == "source_annotation"
            else "bounded_non_detailed_hypothesis"
            if non_detailed
            else "bounded_hypothesis"
        )
        granularity = case_spec["expected_granularity"]
        counterevidence = _counterevidence(
            selected, case_spec, reaction, include_structures=True
        )
    non_detailed = case_spec["expected_granularity"] == "non_detailed"
    basis = [
        evidence_id
        for evidence_id in (
            _evidence_id("M-CSA", case_spec["mcsa_record_id"]),
            *evidence_ids,
        )
        if evidence_id in evidence_ids
    ]
    return {
        "schema_version": RECORD_SCHEMA_VERSION,
        "record_id": record_id,
        "case_id": selected["case_id"],
        "object_type": object_type,
        "evidence_tier": tier,
        "label": f"{selected['label']} — {object_type.replace('_', ' ')}",
        "fixture_only": False,
        "status": status,
        "mechanism_granularity": granularity,
        "biological_scope": _scope(selected),
        "reaction": copy.deepcopy(reaction),
        "mechanism_proposals": record_proposals,
        "sites": record_sites,
        "structures": record_structures,
        "evidence": evidence,
        "counterevidence": counterevidence,
        "uncertainties": _uncertainties(selected),
        "detail_abstention": _detail_abstention(
            selected,
            basis_evidence_ids=list(dict.fromkeys(basis)),
            non_detailed=non_detailed,
        ),
        "claim_boundary": _claim_boundary(
            selected, object_type, reaction["source_status"]
        ),
        "provenance": provenance,
    }


def compile_kernel(
    selection: dict[str, Any],
    manifest: dict[str, Any],
    spec: dict[str, Any],
    inherited_kernel: dict[str, Any],
) -> dict[str, Any]:
    selection_summary = validate_atlas10_selection(selection)
    spec_summary = validate_atlas10_compilation_spec(
        spec, selection=selection, source_manifest=manifest
    )
    if _file_sha256(INHERITED_KERNEL_PATH) != EXPECTED_INHERITED_FILE_SHA256:
        raise ValueError("frozen Atlas-3 kernel file hash differs")
    manifest_index = _manifest_index(manifest)
    bindings = _binding_index(manifest)
    spec_cases = {case["case_id"]: case for case in spec["cases"]}
    provenance = {
        "selection_sha256": selection_summary["selection_sha256"],
        "source_snapshot_set_sha256": manifest["snapshot_set_sha256"],
        "compilation_spec_sha256": spec_summary["compilation_spec_sha256"],
        "compiler_version": COMPILER_VERSION,
    }
    records: list[dict[str, Any]] = []
    for selected in selection["follow_on_cases"]:
        case_spec = spec_cases[selected["case_id"]]
        all_evidence = _case_evidence(
            selected, manifest_index=manifest_index, bindings=bindings
        )
        entry = read_atlas10_mcsa_snapshot(
            _snapshot_path(
                manifest_index, "M-CSA", case_spec["mcsa_record_id"]
            ),
            case_spec["mcsa_record_id"],
        )
        reaction = _reaction(selected, entry, manifest_index=manifest_index)
        sites = _sites(selected, entry, manifest_index=manifest_index)
        structures = _structures(
            selected, case_spec, manifest_index=manifest_index
        )
        proposals = _proposals(
            case_spec, entry, sites, proposal_scope="source_curated"
        )
        for object_type in (
            "reaction_or_source_gap",
            "source_annotation",
            "mechanism_hypothesis",
        ):
            records.append(
                _record(
                    selected,
                    case_spec,
                    object_type=object_type,
                    reaction=reaction,
                    all_evidence=all_evidence,
                    sites=sites,
                    structures=structures,
                    proposals=proposals,
                    provenance=provenance,
                )
            )
    kernel = {
        "schema_version": KERNEL_SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
        "selection_sha256": provenance["selection_sha256"],
        "source_snapshot_set_sha256": provenance["source_snapshot_set_sha256"],
        "compilation_spec_sha256": provenance["compilation_spec_sha256"],
        "source_manifest_retrieved_at": manifest["retrieved_at"],
        "inherited_kernel": copy.deepcopy(spec["inherited_kernel"]),
        "case_count": 10,
        "record_count": 30,
        "follow_on_case_count": 7,
        "follow_on_record_count": 21,
        "follow_on_records": records,
        "relationships": copy.deepcopy(spec["relationships"]),
        "claim_boundary": copy.deepcopy(spec["claim_boundary"]),
    }
    validate_atlas10_kernel(
        kernel,
        selection=selection,
        source_manifest=manifest,
        inherited_kernel=inherited_kernel,
    )
    return kernel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the checked-in kernel is absent or differs from a fresh compile.",
    )
    args = parser.parse_args()
    selection = load_atlas10_selection(SELECTION_PATH)
    manifest = load_atlas10_source_manifest(
        MANIFEST_PATH, repo_root=ROOT, selection=selection
    )
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    inherited_kernel = json.loads(INHERITED_KERNEL_PATH.read_text(encoding="utf-8"))
    kernel = compile_kernel(selection, manifest, spec, inherited_kernel)
    raw = _json_bytes(kernel)
    if args.check:
        if not KERNEL_PATH.exists() or KERNEL_PATH.read_bytes() != raw:
            raise SystemExit("Atlas-10 kernel differs from deterministic compilation")
    else:
        KERNEL_PATH.write_bytes(raw)
    summary = validate_atlas10_kernel(
        kernel,
        selection=selection,
        source_manifest=manifest,
        inherited_kernel=inherited_kernel,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
