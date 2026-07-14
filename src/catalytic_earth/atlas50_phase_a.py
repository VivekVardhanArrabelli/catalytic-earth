"""Deterministic builders and fail-closed validators for Atlas-50 Phase A."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote


CROSSWALK_SCHEMA_VERSION = "catalytic-earth.atlas50-crosswalk-draft.v1"
CANDIDATE_MATRIX_SCHEMA_VERSION = "catalytic-earth.atlas50-candidate-matrix.v1"
PROPOSAL_SCHEMA_VERSION = "catalytic-earth.atlas50-proposal.v1"
BLOCKER_SCHEMA_VERSION = "catalytic-earth.atlas50-blocker-report.v1"
MANIFEST_SCHEMA_VERSION = "catalytic-earth.atlas50-phase-a-package-manifest.v1"
BASELINE_SCHEMA_VERSION = "catalytic-earth.atlas50-inherited-baseline.v1"

BASELINE_COMMIT = "89498a7b0e6e5ea419654bb8ff563512ab36bb89"
ATLAS10_SELECTION_SHA256 = (
    "9bc114aaf793c51ec3b6273466f62a83974512a2dcf969d95d8b97453dd2795e"
)
PHASE_RELATIVE = Path("data/atlas/atlas50/phase_a")

CLASSIFICATIONS = (
    "exact_duplicate",
    "aggregation",
    "specialization",
    "interoperability_bridge",
    "genuinely_missing_concept",
    "unsupported_or_ill_defined",
)
REQUIRED_SOURCE_KEYS = (
    "mcsa",
    "mcsa_arrow_environments",
    "rhea",
    "chebi",
    "ec_blast",
    "enzymemap",
    "mechfind",
    "ezmechanism",
    "enzymm",
    "ec",
    "interpro",
    "pfam",
    "cath",
)
GENERIC_REPRESENTATION_FIELDS = (
    "reaction",
    "mechanism_proposals",
    "sites",
    "structures",
    "evidence",
    "counterevidence",
    "uncertainties",
    "detail_abstention",
    "claim_boundary",
    "provenance",
)
PROHIBITED_PHASE_A_KEYS = {
    "atom_map",
    "atom_maps",
    "bond_edit",
    "bond_edits",
    "catalytic_roles",
    "mechanism_steps",
}

_MCSA_RE = re.compile(r"^M[0-9]{4}$")
_EC_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+\.(?:[0-9]+|-)$")
_UNIPROT_RE = re.compile(r"^[A-Z0-9]{6,10}$")
_PDB_RE = re.compile(r"^[0-9][a-z0-9]{3}$")
_CATH_RE = re.compile(r"^[0-9]+(?:\.[0-9]+){3}$")
_CHEBI_RE = re.compile(r"^CHEBI:[0-9]+$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_json_bytes(value: Any) -> bytes:
    """Return repository-canonical, human-readable JSON bytes."""

    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def compact_digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _file_sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _require_exact_keys(value: Any, expected: set[str], context: str) -> None:
    _require(isinstance(value, dict), f"{context} must be an object")
    actual = set(value)
    _require(
        actual == expected,
        f"{context} keys differ: missing={sorted(expected - actual)}, "
        f"extra={sorted(actual - expected)}",
    )


def _require_string_list(
    value: Any,
    context: str,
    *,
    minimum: int = 0,
    pattern: re.Pattern[str] | None = None,
) -> list[str]:
    _require(isinstance(value, list), f"{context} must be an array")
    _require(len(value) >= minimum, f"{context} must contain at least {minimum} items")
    _require(all(isinstance(item, str) and item for item in value), f"{context} must contain non-empty strings")
    _require(len(value) == len(set(value)), f"{context} must not contain duplicates")
    if pattern is not None:
        _require(all(pattern.fullmatch(item) for item in value), f"{context} contains an invalid identifier")
    return value


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def validate_crosswalk_spec(value: Any, registry: list[dict[str, Any]]) -> None:
    _require_exact_keys(
        value,
        {
            "baseline_commit",
            "classification_vocabulary",
            "decisions",
            "schema_version",
            "spec_id",
            "status",
        },
        "crosswalk_spec",
    )
    _require(
        value["schema_version"] == "catalytic-earth.atlas50-crosswalk-spec.v1",
        "unsupported crosswalk spec schema",
    )
    _require(value["baseline_commit"] == BASELINE_COMMIT, "crosswalk baseline differs")
    _require(
        value["status"] == "machine_draft_input_not_reviewed",
        "crosswalk spec cannot imply review",
    )
    _require(tuple(value["classification_vocabulary"]) == CLASSIFICATIONS, "classification vocabulary differs")
    decisions = value["decisions"]
    _require(isinstance(decisions, list) and len(decisions) == 57, "crosswalk spec must contain exactly 57 decisions")
    registry_ids = [row["id"] for row in registry]
    decision_ids: list[str] = []
    for index, decision in enumerate(decisions):
        context = f"crosswalk_spec.decisions[{index}]"
        _require_exact_keys(
            decision,
            {
                "basis_note",
                "candidate_ec_numbers",
                "candidate_mcsa_ids",
                "classification",
                "counterexample_mcsa_ids",
                "fingerprint_id",
            },
            context,
        )
        decision_ids.append(decision["fingerprint_id"])
        _require(decision["classification"] in CLASSIFICATIONS, f"{context} has unsupported classification")
        _require_string_list(decision["candidate_mcsa_ids"], f"{context}.candidate_mcsa_ids", pattern=_MCSA_RE)
        _require_string_list(decision["counterexample_mcsa_ids"], f"{context}.counterexample_mcsa_ids", pattern=_MCSA_RE)
        _require_string_list(decision["candidate_ec_numbers"], f"{context}.candidate_ec_numbers", pattern=_EC_RE)
        _require(
            not set(decision["candidate_mcsa_ids"]) & set(decision["counterexample_mcsa_ids"]),
            f"{context} cannot treat one M-CSA entry as candidate and counterexample",
        )
        _require(isinstance(decision["basis_note"], str) and len(decision["basis_note"]) >= 40, f"{context}.basis_note is too weak")
    _require(decision_ids == registry_ids, "crosswalk decisions must preserve all 57 registry rows in order")


def validate_candidate_spec(value: Any) -> None:
    _require_exact_keys(
        value,
        {
            "baseline_commit",
            "blockers",
            "candidates",
            "representation_contract",
            "schema_version",
            "selected_mcsa_response",
            "spec_id",
            "status",
        },
        "candidate_spec",
    )
    _require(
        value["schema_version"] == "catalytic-earth.atlas50-candidate-spec.v1",
        "unsupported candidate spec schema",
    )
    _require(value["baseline_commit"] == BASELINE_COMMIT, "candidate baseline differs")
    _require(
        value["status"] == "precompilation_feasibility_input_not_selection_freeze",
        "candidate spec cannot freeze selection",
    )
    selected = value["selected_mcsa_response"]
    _require_exact_keys(
        selected,
        {"entry_count", "query_acquisition_id", "raw_response_bundled", "response_sha256", "retrieved_on"},
        "candidate_spec.selected_mcsa_response",
    )
    _require(selected["entry_count"] == 40, "selected M-CSA response must contain 40 candidates")
    _require(_SHA256_RE.fullmatch(selected["response_sha256"]) is not None, "selected response hash is invalid")
    _require(selected["raw_response_bundled"] is False, "raw M-CSA response cannot be bundled")
    contract = value["representation_contract"]
    _require_exact_keys(
        contract,
        {
            "family_specific_ad_hoc_fields_permitted",
            "generic_fields_considered",
            "mechanism_compilation_permitted",
            "projected_schema",
            "projection_only",
        },
        "candidate_spec.representation_contract",
    )
    _require(contract["projection_only"] is True, "representation result must remain a projection")
    _require(contract["mechanism_compilation_permitted"] is False, "Phase A cannot compile mechanisms")
    _require(contract["family_specific_ad_hoc_fields_permitted"] is False, "ad hoc fields cannot be authorized")
    _require(tuple(contract["generic_fields_considered"]) == GENERIC_REPRESENTATION_FIELDS, "generic field projection differs")

    candidates = value["candidates"]
    _require(isinstance(candidates, list) and len(candidates) == 40, "candidate spec must contain exactly 40 rows")
    ids: list[str] = []
    failed: dict[str, str] = {}
    for index, candidate in enumerate(candidates):
        context = f"candidate_spec.candidates[{index}]"
        _require_exact_keys(
            candidate,
            {
                "annotation_level",
                "blocker_id",
                "cath_ids",
                "chebi_ids",
                "ec_numbers",
                "label",
                "mcsa_id",
                "mechanism_proposal_count",
                "pdb_ids",
                "representation_gate",
                "representation_pressures",
                "uniprot_ids",
            },
            context,
        )
        ids.append(candidate["mcsa_id"])
        _require(_MCSA_RE.fullmatch(candidate["mcsa_id"]) is not None, f"{context}.mcsa_id is invalid")
        _require(isinstance(candidate["label"], str) and candidate["label"], f"{context}.label is empty")
        _require_string_list(candidate["ec_numbers"], f"{context}.ec_numbers", minimum=1, pattern=_EC_RE)
        _require_string_list(candidate["uniprot_ids"], f"{context}.uniprot_ids", minimum=1, pattern=_UNIPROT_RE)
        _require_string_list(candidate["pdb_ids"], f"{context}.pdb_ids", pattern=_PDB_RE)
        _require_string_list(candidate["cath_ids"], f"{context}.cath_ids", pattern=_CATH_RE)
        _require_string_list(candidate["chebi_ids"], f"{context}.chebi_ids", minimum=1, pattern=_CHEBI_RE)
        _require(candidate["annotation_level"] in {"detailed", "non_detailed"}, f"{context}.annotation_level is invalid")
        _require(isinstance(candidate["mechanism_proposal_count"], int) and candidate["mechanism_proposal_count"] >= 1, f"{context}.mechanism_proposal_count is invalid")
        _require_string_list(candidate["representation_pressures"], f"{context}.representation_pressures", minimum=2)
        _require(candidate["representation_gate"] in {"pass", "fail_missing_general_contract"}, f"{context}.representation_gate is invalid")
        if candidate["representation_gate"] == "pass":
            _require(candidate["blocker_id"] is None, f"{context} passing row cannot carry a blocker")
        else:
            _require(isinstance(candidate["blocker_id"], str) and candidate["blocker_id"], f"{context} failed row needs a blocker")
            failed[candidate["mcsa_id"]] = candidate["blocker_id"]
    _require(len(ids) == len(set(ids)), "candidate M-CSA IDs must be unique")
    _require(ids == sorted(ids, key=lambda item: int(item[1:])), "candidate rows must be numerically ordered")
    _require(len(failed) == 3, "exactly three declared representation blockers are expected")

    blockers = value["blockers"]
    _require(isinstance(blockers, list) and len(blockers) == 3, "candidate spec must contain three blocker contracts")
    blocker_map: dict[str, str] = {}
    for index, blocker in enumerate(blockers):
        context = f"candidate_spec.blockers[{index}]"
        _require_exact_keys(
            blocker,
            {"blocker_id", "mcsa_id", "missing_general_contract", "unlock_condition", "why_material"},
            context,
        )
        _require(blocker["mcsa_id"] in failed, f"{context} does not name a failed candidate")
        _require(failed[blocker["mcsa_id"]] == blocker["blocker_id"], f"{context} differs from candidate blocker")
        for field in ("missing_general_contract", "unlock_condition", "why_material"):
            _require(isinstance(blocker[field], str) and len(blocker[field]) >= 50, f"{context}.{field} is too weak")
        blocker_map[blocker["mcsa_id"]] = blocker["blocker_id"]
    _require(blocker_map == failed, "blocker contracts must exactly match failed candidates")


def validate_source_catalog(value: Any) -> None:
    _require(value.get("schema_version") == "catalytic-earth.atlas50-phase-a-source-catalog.v1", "unsupported source catalog")
    _require(value.get("baseline_commit") == BASELINE_COMMIT, "source catalog baseline differs")
    _require(value.get("status") == "bounded_acquisition_complete", "source acquisition is not bounded-complete")
    _require(tuple(value.get("required_crosswalk_source_keys", [])) == REQUIRED_SOURCE_KEYS, "required crosswalk source keys differ")
    resources = value.get("resources")
    _require(isinstance(resources, list), "source catalog resources must be an array")
    resource_keys = [resource.get("source_key") for resource in resources]
    _require(tuple(resource_keys) == REQUIRED_SOURCE_KEYS, "source catalog must define each source once in required order")
    for index, resource in enumerate(resources):
        for field in ("official_uri", "rights", "redistribution_boundary", "row_link_policy"):
            _require(isinstance(resource.get(field), str) and resource[field], f"source_catalog.resources[{index}].{field} is empty")
        _require(isinstance(resource.get("limitations"), list) and resource["limitations"], f"source_catalog.resources[{index}] needs limitations")
    usage = value.get("usage", {})
    _require(usage.get("gpu_hours") == 0, "source acquisition used GPU work")
    _require(usage.get("raw_source_bodies_committed") is False, "raw source bodies cannot be committed")
    _require(usage.get("article_bodies_acquired") is False, "article bodies cannot be acquired in this phase")
    _require(usage.get("external_operations_conservatively_counted", 10**9) <= usage.get("external_requests_max", -1), "source request budget exceeded")
    _require(usage.get("download_mib_conservatively_accounted", 10**9) <= usage.get("download_mib_max", -1), "source download budget exceeded")
    for acquisition in value.get("acquisitions", []):
        _require(_SHA256_RE.fullmatch(str(acquisition.get("sha256", ""))) is not None, "source acquisition hash is invalid")
    _require(isinstance(value.get("failed_acquisitions"), list), "failed acquisitions must remain explicit")


def _selection_source_index(repo_root: Path, candidate_spec: dict[str, Any]) -> dict[str, dict[str, set[str]]]:
    index: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for candidate in candidate_spec["candidates"]:
        record = index[candidate["mcsa_id"]]
        for key in ("ec_numbers", "uniprot_ids", "pdb_ids", "cath_ids", "chebi_ids"):
            record[key].update(candidate[key])

    selection_specs = (
        ("data/atlas/atlas3_selection.json", "cases"),
        ("data/atlas/atlas10_selection.json", "follow_on_cases"),
    )
    for relative, case_key in selection_specs:
        selection = _load_json(repo_root / relative)
        for case in selection[case_key]:
            handles = case["source_handles"]
            mcsa_ids = [handle["record_id"] for handle in handles if handle["source_id"] == "M-CSA"]
            for mcsa_id in mcsa_ids:
                record = index[mcsa_id]
                for handle in handles:
                    source = handle["source_id"]
                    record_id = handle["record_id"]
                    if source == "UniProtKB":
                        record["uniprot_ids"].add(record_id)
                    elif source == "PDB":
                        record["pdb_ids"].add(record_id.lower())
                    elif source == "CATH":
                        record["cath_ids"].add(record_id.removeprefix("CATH:"))
                    elif source == "Rhea" and record_id.startswith("RHEA:"):
                        record["rhea_ids"].add(record_id)
                    elif source == "Rhea" and record_id.startswith("EC:"):
                        record["ec_numbers"].add(record_id.removeprefix("EC:"))
                record["chebi_ids"].update(
                    item for item in case.get("reaction_participant_ids", []) if _CHEBI_RE.fullmatch(item)
                )
                ec_number = case.get("ec_number")
                if isinstance(ec_number, str) and _EC_RE.fullmatch(ec_number):
                    record["ec_numbers"].add(ec_number)
    return index


def _source_link(
    *,
    status: str,
    records: list[dict[str, str]],
    uris: Iterable[str],
    lookup_keys: Iterable[str],
    gap_reason: str | None,
) -> dict[str, Any]:
    return {
        "status": status,
        "records": records,
        "uris": sorted(set(uris)),
        "lookup_keys": sorted(set(lookup_keys)),
        "gap_reason": gap_reason,
        "mapping_assertion": "none_unreviewed_candidate_only",
    }


def _mcsa_uri(mcsa_id: str) -> str:
    return f"https://www.ebi.ac.uk/thornton-srv/m-csa/entry/{int(mcsa_id[1:])}/"


def _rhea_uri(rhea_id: str) -> str:
    return f"https://www.rhea-db.org/rhea/{rhea_id.removeprefix('RHEA:')}"


def _rhea_query_uri(ec_number: str) -> str:
    return "https://www.rhea-db.org/rhea?query=" + quote(f"ec:{ec_number}", safe="")


def _build_source_links(
    decision: dict[str, Any],
    source_index: dict[str, dict[str, set[str]]],
) -> dict[str, dict[str, Any]]:
    candidate_ids = decision["candidate_mcsa_ids"]
    counterexample_ids = decision["counterexample_mcsa_ids"]
    metadata: dict[str, set[str]] = defaultdict(set)
    for mcsa_id in candidate_ids:
        for key, values in source_index.get(mcsa_id, {}).items():
            metadata[key].update(values)
    ec_numbers = sorted(set(decision["candidate_ec_numbers"]) | metadata["ec_numbers"])
    mcsa_records = [
        {"record_id": mcsa_id, "role": "candidate_handle_unreviewed"}
        for mcsa_id in candidate_ids
    ] + [
        {"record_id": mcsa_id, "role": "counterexample_only_not_mapping"}
        for mcsa_id in counterexample_ids
    ]
    if candidate_ids:
        mcsa_status = "candidate_handles_unreviewed"
        mcsa_gap = None
    elif counterexample_ids:
        mcsa_status = "counterexample_only_no_candidate_handle"
        mcsa_gap = "Only a counterexample is linked; no applicable M-CSA mechanism candidate was adjudicated."
    else:
        mcsa_status = "explicit_gap_no_candidate_handle"
        mcsa_gap = "No direct M-CSA candidate was adjudicated during the bounded Phase A inventory."

    rhea_records = [
        {"record_id": record_id, "role": "inherited_direct_handle_unreviewed"}
        for record_id in sorted(metadata["rhea_ids"])
    ] + [
        {"record_id": f"EC:{ec}", "role": "query_key_only_no_reaction_match"}
        for ec in ec_numbers
    ]
    rhea_uris = [_rhea_uri(record_id) for record_id in metadata["rhea_ids"]] + [
        _rhea_query_uri(ec) for ec in ec_numbers
    ]
    if metadata["rhea_ids"]:
        rhea_status = "inherited_direct_and_or_ec_query_handles_unreviewed"
        rhea_gap = None
    elif ec_numbers:
        rhea_status = "ec_query_only_not_retrieved"
        rhea_gap = "No new direct Rhea record was assigned; EC links are search keys only."
    else:
        rhea_status = "explicit_gap_no_reaction_key"
        rhea_gap = "No defensible EC or direct Rhea handle was frozen for this broad fingerprint."

    chebi_ids = sorted(metadata["chebi_ids"])
    uniprot_ids = sorted(metadata["uniprot_ids"])
    cath_ids = sorted(metadata["cath_ids"], key=lambda value: tuple(int(part) for part in value.split(".")))
    lookup_basis = candidate_ids + ec_numbers
    links = {
        "mcsa": _source_link(
            status=mcsa_status,
            records=mcsa_records,
            uris=[_mcsa_uri(mcsa_id) for mcsa_id in candidate_ids + counterexample_ids],
            lookup_keys=candidate_ids + counterexample_ids,
            gap_reason=mcsa_gap,
        ),
        "mcsa_arrow_environments": _source_link(
            status="reference_only_lookup_not_run" if candidate_ids else "explicit_gap_no_candidate_lookup_key",
            records=[{"record_id": mcsa_id, "role": "lookup_key_only_no_arrow_match"} for mcsa_id in candidate_ids],
            uris=["https://github.com/maranasgroup/MechFind/tree/fcc0896"] if candidate_ids else [],
            lookup_keys=candidate_ids + (["M-CSA_arrow_rules_r0.json"] if candidate_ids else []),
            gap_reason=(
                "No arrow-environment similarity or equivalence was computed; MechFind is reference-only."
                if candidate_ids
                else "No candidate M-CSA key is available for an arrow-environment lookup."
            ),
        ),
        "rhea": _source_link(
            status=rhea_status,
            records=rhea_records,
            uris=rhea_uris,
            lookup_keys=ec_numbers + sorted(metadata["rhea_ids"]),
            gap_reason=rhea_gap,
        ),
        "chebi": _source_link(
            status="source_reported_candidate_participants_unreviewed" if chebi_ids else "explicit_gap_no_participant_ids",
            records=[{"record_id": record_id, "role": "candidate_participant_unreviewed"} for record_id in chebi_ids],
            uris=[f"https://www.ebi.ac.uk/chebi/searchId.do?chebiId={quote(record_id, safe='')}" for record_id in chebi_ids],
            lookup_keys=chebi_ids,
            gap_reason=(
                "Participant identity, side, stoichiometry, protonation, and reaction balance were not adjudicated."
                if chebi_ids
                else "No source-reported ChEBI candidate set was retained for this row."
            ),
        ),
        "ec_blast": _source_link(
            status="ec_lookup_keys_only_search_not_run" if ec_numbers else "explicit_gap_no_ec_lookup_key",
            records=[{"record_id": f"EC:{ec}", "role": "lookup_key_only_no_bond_change_match"} for ec in ec_numbers],
            uris=["https://www.ebi.ac.uk/thornton-srv/software/rbl/"] if ec_numbers else [],
            lookup_keys=ec_numbers,
            gap_reason="No EC-BLAST search or bond-change comparison was run." if ec_numbers else "No EC key was frozen for EC-BLAST lookup.",
        ),
        "enzymemap": _source_link(
            status="ec_lookup_keys_only_dataset_not_queried" if ec_numbers else "explicit_gap_no_ec_lookup_key",
            records=[{"record_id": f"EC:{ec}", "role": "lookup_key_only_no_atom_map_match"} for ec in ec_numbers],
            uris=["https://zenodo.org/records/8254726"] if ec_numbers else [],
            lookup_keys=ec_numbers,
            gap_reason="EnzymeMap v2 was not downloaded or queried; no atom-mapped reaction match is asserted." if ec_numbers else "No EC key was frozen for an EnzymeMap lookup.",
        ),
        "mechfind": _source_link(
            status="reference_only_inputs_not_run" if lookup_basis else "explicit_gap_no_lookup_key",
            records=[{"record_id": key, "role": "possible_input_only_no_prediction"} for key in lookup_basis],
            uris=["https://github.com/maranasgroup/MechFind/tree/fcc0896"] if lookup_basis else [],
            lookup_keys=lookup_basis,
            gap_reason="MechFind was not run and its non-commercial distribution remains reference-only." if lookup_basis else "No M-CSA or EC key was frozen for a MechFind lookup.",
        ),
        "ezmechanism": _source_link(
            status="registration_required_not_accessed",
            records=[],
            uris=["https://www.ebi.ac.uk/thornton-srv/m-csa/EzMechanism/documentation"],
            lookup_keys=lookup_basis,
            gap_reason="No account was requested and no input chemistry, protonation, structure, or generated result was supplied.",
        ),
        "enzymm": _source_link(
            status="candidate_lookup_keys_only_scan_not_run" if (candidate_ids or uniprot_ids) else "explicit_gap_no_template_lookup_key",
            records=[{"record_id": key, "role": "lookup_key_only_no_template_match"} for key in candidate_ids + uniprot_ids],
            uris=["https://www.ebi.ac.uk/thornton-srv/m-csa/enzymm-documentation/"] if (candidate_ids or uniprot_ids) else [],
            lookup_keys=candidate_ids + uniprot_ids,
            gap_reason="No structure/template scan was run; no catalytic-template match is asserted." if (candidate_ids or uniprot_ids) else "No M-CSA or protein handle was frozen for an EnzyMM lookup.",
        ),
        "ec": _source_link(
            status="source_reported_lookup_keys_unreviewed" if ec_numbers else "explicit_gap_no_ec_key",
            records=[{"record_id": f"EC:{ec}", "role": "lookup_key_only_not_mechanism_equivalence"} for ec in ec_numbers],
            uris=[f"https://enzyme.expasy.org/EC/{ec}" for ec in ec_numbers],
            lookup_keys=ec_numbers,
            gap_reason="EC classification does not establish a unique mechanism." if ec_numbers else "No defensible EC key was frozen for this row.",
        ),
        "interpro": _source_link(
            status="protein_lookup_keys_only_api_not_queried" if uniprot_ids else "explicit_gap_no_protein_key",
            records=[{"record_id": record_id, "role": "lookup_key_only_no_domain_assignment"} for record_id in uniprot_ids],
            uris=[f"https://www.ebi.ac.uk/interpro/protein/UniProt/{record_id}/" for record_id in uniprot_ids],
            lookup_keys=uniprot_ids,
            gap_reason="No InterPro row lookup or mechanism transfer was performed." if uniprot_ids else "No protein handle was retained for an InterPro lookup.",
        ),
        "pfam": _source_link(
            status="protein_lookup_keys_only_no_family_assignment" if uniprot_ids else "explicit_gap_no_protein_key",
            records=[{"record_id": record_id, "role": "lookup_key_only_no_pfam_assignment"} for record_id in uniprot_ids],
            uris=["https://www.ebi.ac.uk/interpro/entry/pfam/"] if uniprot_ids else [],
            lookup_keys=uniprot_ids,
            gap_reason="No Pfam API/HMM lookup or family-to-mechanism transfer was performed." if uniprot_ids else "No protein handle was retained for a Pfam lookup.",
        ),
        "cath": _source_link(
            status="source_reported_candidate_folds_unreviewed" if cath_ids else "explicit_gap_no_fold_handle",
            records=[{"record_id": f"CATH:{record_id}", "role": "candidate_fold_unreviewed"} for record_id in cath_ids],
            uris=[f"https://www.cathdb.info/version/latest/superfamily/{record_id}" for record_id in cath_ids],
            lookup_keys=cath_ids,
            gap_reason="A fold handle does not authorize mechanism transfer." if cath_ids else "No source-reported CATH handle was retained for this row.",
        ),
    }
    _require(tuple(links) == REQUIRED_SOURCE_KEYS, "crosswalk source-link order differs")
    return links


def build_crosswalk(
    repo_root: Path,
    registry: list[dict[str, Any]],
    spec: dict[str, Any],
    candidate_spec: dict[str, Any],
    source_catalog: dict[str, Any],
) -> dict[str, Any]:
    source_index = _selection_source_index(repo_root, candidate_spec)
    registry_sha = _file_sha256(repo_root / "data/registries/mechanism_fingerprints.json")
    rows: list[dict[str, Any]] = []
    for ordinal, (fingerprint, decision) in enumerate(zip(registry, spec["decisions"], strict=True), start=1):
        classification = decision["classification"]
        rows.append(
            {
                "ordinal": ordinal,
                "fingerprint_id": fingerprint["id"],
                "fingerprint_name": fingerprint["name"],
                "classification": classification,
                "classification_rationale": (
                    f"Machine-draft {classification.replace('_', ' ')} classification for "
                    f"{fingerprint['name']}. {decision['basis_note']}"
                ),
                "uncertainty": (
                    "Scope, source applicability, reaction granularity, and cross-source "
                    "equivalence remain unresolved until a real reviewer adjudicates this row."
                ),
                "review_status": "unreviewed",
                "reviewer": None,
                "reviewed_at": None,
                "source_links": _build_source_links(decision, source_index),
            }
        )
    counts = Counter(row["classification"] for row in rows)
    return {
        "schema_version": CROSSWALK_SCHEMA_VERSION,
        "draft_id": "atlas50.phase-a.crosswalk-draft.2026-07-14",
        "status": "machine_draft_unreviewed",
        "baseline_commit": BASELINE_COMMIT,
        "generated_from": {
            "fingerprint_registry_path": "data/registries/mechanism_fingerprints.json",
            "fingerprint_registry_sha256": registry_sha,
            "crosswalk_spec_sha256": _file_sha256(repo_root / PHASE_RELATIVE / "crosswalk_spec.json"),
            "candidate_spec_sha256": _file_sha256(repo_root / PHASE_RELATIVE / "candidate_spec.json"),
            "source_catalog_sha256": _file_sha256(repo_root / PHASE_RELATIVE / "source_catalog.json"),
        },
        "review_contract": {
            "default_status": "unreviewed",
            "upstream_curation_counts_as_independent_review": False,
            "machine_draft_counts_as_reviewed_crosswalk": False,
            "outreach_or_expert_agreement_claimed": False,
        },
        "classification_vocabulary": list(CLASSIFICATIONS),
        "classification_counts": {classification: counts.get(classification, 0) for classification in CLASSIFICATIONS},
        "required_source_keys": list(source_catalog["required_crosswalk_source_keys"]),
        "row_count": len(rows),
        "rows": rows,
        "claim_boundary": [
            "This is a deterministic source-linked machine draft, not the reviewed Section 10.1 crosswalk.",
            "Candidate handles, queries, upstream curation, and source-reported identifiers do not establish equivalence or applicability.",
            "No mechanism steps, atom maps, bond edits, catalytic roles, independent review, or registry admission are produced."
        ],
    }


def _candidate_id(mcsa_id: str) -> str:
    return f"atlas50.candidate.{mcsa_id.lower()}"


def _candidate_source_gaps(candidate: dict[str, Any]) -> list[str]:
    gaps = [
        "No direct Rhea record, balanced reaction, or Rhea participant applicability was assigned in Phase A.",
        "No primary-literature body or claim-level literature adjudication was acquired.",
        "EC-BLAST, EnzymeMap, MechFind, EzMechanism, EnzyMM, InterPro, and Pfam were not run per row."
    ]
    if not candidate["pdb_ids"]:
        gaps.append("No source-reported PDB handle was present in the selected M-CSA response.")
    if not candidate["cath_ids"]:
        gaps.append("No source-reported CATH handle was present in the selected M-CSA response.")
    if candidate["annotation_level"] == "non_detailed":
        gaps.append("The selected M-CSA entry is non-detailed; ordered steps and discrete electron-flow detail require abstention.")
    if any(ec.endswith("-") for ec in candidate["ec_numbers"]):
        gaps.append("The source-reported EC handle is partial and was preserved without completion.")
    return gaps


def _tier_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    possible = [
        {
            "tier": 0,
            "status": "contingent",
            "condition": "A balanced canonical reaction and stable Rhea/ChEBI provenance must be independently retrieved and checked in a later phase."
        }
    ]
    abstentions: list[str] = []
    if candidate["annotation_level"] == "detailed":
        possible.append(
            {
                "tier": 1,
                "status": "contingent",
                "condition": "Detailed source steps and alternatives must be reacquired, rights-checked, compiled without invention, and source-linked in a later authorized phase."
            }
        )
        if candidate["pdb_ids"]:
            possible.append(
                {
                    "tier": 2,
                    "status": "contingent",
                    "condition": "Protein, site, coordinate, structure-context, and applicability evidence must be verified in a later authorized phase."
                }
            )
        else:
            abstentions.append("Tier 2 is blocked until a directly applicable structure/site evidence handle is established.")
    else:
        abstentions.extend(
            [
                "Tier 1 ordered-step detail is unsupported by the non-detailed source entry.",
                "Tier 2 is unsupported until a bounded mechanism hypothesis and site-grounding evidence both exist."
            ]
        )
    return {
        "phase_a_objects_created": [],
        "later_possible_tiers": possible,
        "mandatory_abstentions": abstentions,
        "projection_not_completion": True,
    }


def _candidate_gates(candidate: dict[str, Any], blocker: dict[str, Any] | None) -> dict[str, Any]:
    representation_pass = candidate["representation_gate"] == "pass"
    return {
        "source": {
            "outcome": "pass",
            "reason": "A resolvable M-CSA entry plus source-reported EC, UniProt, and ChEBI candidate handles exist; missing Rhea/PDB/CATH/detail fields remain explicit gaps."
        },
        "diversity": {
            "outcome": "pass",
            "reason": "The row contributes at least two declared representation pressures to the stratified 50-case surface."
        },
        "rights": {
            "outcome": "pass",
            "reason": "Only identifiers, links, and bounded metadata are redistributed; raw M-CSA, article, MechFind, and derived rule bodies are absent."
        },
        "provenance": {
            "outcome": "pass",
            "reason": "The selected 40-entry response query, retrieval date, byte count, and SHA-256 are frozen in the source catalog; row metadata remains source-reported and unreviewed."
        },
        "representation": {
            "outcome": "pass" if representation_pass else "fail",
            "reason": (
                "Generic v3 fields plus explicit abstention appear sufficient in this precompilation projection; no family-specific field is proposed."
                if representation_pass
                else blocker["why_material"]
            ),
            "blocker_id": None if representation_pass else blocker["blocker_id"],
        },
    }


def build_candidate_matrix(candidate_spec: dict[str, Any]) -> dict[str, Any]:
    blockers = {blocker["blocker_id"]: blocker for blocker in candidate_spec["blockers"]}
    rows: list[dict[str, Any]] = []
    for ordinal, candidate in enumerate(candidate_spec["candidates"], start=1):
        blocker = blockers.get(candidate["blocker_id"])
        gates = _candidate_gates(candidate, blocker)
        passed = all(gate["outcome"] == "pass" for gate in gates.values())
        inclusion_reasons = (
            [
                "All declared Phase A source, diversity, rights, provenance, and representation gates pass.",
                "The case remains an unreviewed proposal for later selection freeze and compilation, not a compiled or selected mechanism."
            ]
            if passed
            else []
        )
        exclusion_reasons = (
            []
            if passed
            else [
                "The shared-representation gate fails closed.",
                blocker["missing_general_contract"],
            ]
        )
        rows.append(
            {
                "ordinal": ordinal,
                "candidate_id": _candidate_id(candidate["mcsa_id"]),
                "label": candidate["label"],
                "decision": "propose_include" if passed else "exclude_blocked",
                "review_status": "unreviewed",
                "inclusion_reasons": inclusion_reasons,
                "exclusion_reasons": exclusion_reasons,
                "source_identity": {
                    "mcsa_id": candidate["mcsa_id"],
                    "mcsa_uri": _mcsa_uri(candidate["mcsa_id"]),
                    "annotation_level": candidate["annotation_level"],
                    "source_reported_mechanism_proposal_count": candidate["mechanism_proposal_count"],
                    "ec_numbers": candidate["ec_numbers"],
                    "uniprot_ids": candidate["uniprot_ids"],
                    "pdb_ids": candidate["pdb_ids"],
                    "cath_ids": [f"CATH:{record_id}" for record_id in candidate["cath_ids"]],
                    "chebi_ids": candidate["chebi_ids"],
                    "mapping_assertion": "source_reported_candidates_unreviewed",
                },
                "source_availability": {
                    "mcsa": "public_entry_handle_detailed" if candidate["annotation_level"] == "detailed" else "public_entry_handle_non_detailed",
                    "rhea": "ec_query_key_only_no_direct_record_assigned",
                    "chebi": "source_reported_candidate_ids_not_reaction_adjudication",
                    "uniprot": "source_reported_lookup_handles_not_retrieved",
                    "pdb": "source_reported_lookup_handles_not_retrieved" if candidate["pdb_ids"] else "explicit_source_gap",
                    "cath": "source_reported_candidate_handles_unreviewed" if candidate["cath_ids"] else "explicit_source_gap",
                    "comparison_tools": "reference_or_lookup_surfaces_available_not_run",
                    "primary_literature": "claim_level_sources_not_acquired_or_adjudicated",
                    "explicit_gaps": _candidate_source_gaps(candidate),
                },
                "licensing": {
                    "gate": "pass_identifiers_and_links_only",
                    "redistributed_source_bodies": False,
                    "boundaries": [
                        "M-CSA and ChEBI metadata are attributed as CC BY 4.0 candidate identifiers.",
                        "CATH candidate identifiers are attributed as CC BY 4.0; InterPro/Pfam lookup surfaces are CC0 but were not queried.",
                        "MechFind and its arrow environments remain reference-only under non-commercial terms.",
                        "EC-BLAST result rights were not captured, so no results are redistributed.",
                        "No article body, EnzymeMap reaction file, EnzyMM template, or EzMechanism result is bundled."
                    ],
                },
                "representation_pressures": candidate["representation_pressures"],
                "expected_object_tiers": _tier_projection(candidate),
                "phase_a_compute_ceiling": {
                    "cpu_seconds_max_per_deterministic_row_build": 1,
                    "gpu_hours_max": 0,
                    "external_requests_max": 0,
                    "mechanism_compilation_permitted": False,
                },
                "stop_conditions": [
                    "Stop if a source identifier, reaction, participant, step, site, cofactor state, or applicability claim would need to be guessed.",
                    "Stop if a rights or provenance boundary cannot be recorded.",
                    "Stop and exclude if generic shared fields plus abstention cannot represent the pressure without a family-specific field."
                ],
                "gates": gates,
                "mechanism_compiled": False,
                "independent_review_claimed": False,
                "uncertainties": [
                    "All row metadata and gate interpretations remain unreviewed.",
                    "M-CSA candidate participants do not establish a balanced canonical reaction or ChEBI microspecies applicability.",
                    "Primary-literature conflicts and source alternatives have not been adjudicated."
                ],
            }
        )
    counts = Counter(row["decision"] for row in rows)
    pressure_counts = Counter(
        pressure for row in rows for pressure in row["representation_pressures"]
    )
    return {
        "schema_version": CANDIDATE_MATRIX_SCHEMA_VERSION,
        "matrix_id": "atlas50.phase-a.candidate-feasibility.2026-07-14",
        "status": "precompilation_feasibility_projection_unreviewed",
        "baseline_commit": BASELINE_COMMIT,
        "candidate_count": len(rows),
        "proposed_include_count": counts["propose_include"],
        "excluded_blocked_count": counts["exclude_blocked"],
        "mechanisms_compiled": 0,
        "gpu_hours": 0,
        "source_response": candidate_spec["selected_mcsa_response"],
        "gate_order": ["source", "diversity", "rights", "provenance", "representation"],
        "pressure_counts": dict(sorted(pressure_counts.items())),
        "rows": rows,
        "claim_boundary": [
            "This matrix measures bounded source and representation feasibility; it is not a selection freeze, compilation, benchmark, or scientific result.",
            "Inclusion means only that declared Phase A gates appear to pass; exclusion preserves a blocker rather than resolving it for convenience.",
            "No accuracy, speedup, independent-validation, discovery, design-readiness, assay, or atlas-coverage claim is supported."
        ],
    }


def _pressure_inventory() -> list[dict[str, Any]]:
    return [
        {"pressure": "radicals", "status": "present", "examples": ["atlas3.mcm-pfre.radical", "atlas50.candidate.m0767", "atlas50.candidate.m0991"]},
        {"pressure": "metals_and_metalloclusters", "status": "present_with_one_blocked_extreme", "examples": ["atlas3.mnsod-ecoli.redox", "atlas50.candidate.m0107", "atlas50.candidate.m0127", "atlas50.candidate.m0212"]},
        {"pressure": "redox_and_cofactor_states", "status": "present", "examples": ["atlas50.candidate.m0099", "atlas50.candidate.m0139", "atlas50.candidate.m0980"]},
        {"pressure": "covalent_intermediates", "status": "present", "examples": ["atlas3.tem1-ecoli.covalent", "atlas50.candidate.m0031", "atlas50.candidate.m0174"]},
        {"pressure": "proton_ambiguity", "status": "present", "examples": ["atlas10.caii-human.proton-relay", "atlas50.candidate.m0050", "atlas50.candidate.m0133"]},
        {"pressure": "conformational_gating", "status": "present_with_one_blocked_extreme", "examples": ["atlas50.candidate.m0064", "atlas50.candidate.m0191", "atlas50.candidate.m0753"]},
        {"pressure": "same_net_reaction_different_mechanisms", "status": "present", "examples": ["atlas50.candidate.m0052", "atlas50.candidate.m0222"]},
        {"pressure": "convergent_strategy_unrelated_folds", "status": "inherited_atlas10", "examples": ["atlas10.trypsin-fusarium.serine-protease", "atlas10.subtilisin-bpn-bacillus.serine-protease"]},
        {"pressure": "divergent_chemistry_within_a_fold", "status": "inherited_and_extended", "examples": ["atlas10.mandelate-racemase-pputida.enolate", "atlas10.methylaspartate-lyase-ctetanomorphum.enolate", "atlas50.candidate.m0050", "atlas50.candidate.m0052"]},
        {"pressure": "alternative_mechanisms", "status": "source_alternatives_present_unadjudicated", "examples": ["atlas10.hewl-chicken.covalent-glycosidase", "atlas50.candidate.m0007", "atlas50.candidate.m0135"]},
        {"pressure": "conflicting_literature", "status": "pressure_flagged_for_later_adjudication_not_established_as_fact", "examples": ["atlas50.candidate.m0007", "atlas50.candidate.m0132", "atlas50.candidate.m0139"]},
        {"pressure": "experimentally_unresolved_mechanisms", "status": "non_detailed_source_abstentions_present", "examples": ["atlas10.cyclophilin-a-human.isomerization", "atlas50.candidate.m0767", "atlas50.candidate.m0851", "atlas50.candidate.m0935"]},
        {"pressure": "applicability_gaps", "status": "present", "examples": ["atlas50.candidate.m0204", "atlas50.candidate.m0997"]},
        {"pressure": "abstention", "status": "present", "examples": ["atlas10.cyclophilin-a-human.isomerization", "atlas50.candidate.m0767", "atlas50.candidate.m0851", "atlas50.candidate.m0935"]},
    ]


def build_proposal(repo_root: Path, matrix: dict[str, Any]) -> dict[str, Any]:
    atlas10 = _load_json(repo_root / "data/atlas/atlas10_selection.json")
    atlas10_digest = compact_digest(atlas10)
    _require(atlas10_digest == ATLAS10_SELECTION_SHA256, "inherited Atlas-10 selection digest differs")
    additions = [row["candidate_id"] for row in matrix["rows"] if row["decision"] == "propose_include"]
    excluded = [row["candidate_id"] for row in matrix["rows"] if row["decision"] == "exclude_blocked"]
    inherited_ids = atlas10["all_case_ids"]
    projected_representable = len(inherited_ids) + len(additions)
    candidate_surface_total = len(inherited_ids) + matrix["candidate_count"]
    percentage = projected_representable * 100 / candidate_surface_total
    return {
        "schema_version": PROPOSAL_SCHEMA_VERSION,
        "proposal_id": "atlas50.phase-a.fail-closed-panel.2026-07-14",
        "status": "proposal_not_selection_freeze",
        "baseline_commit": BASELINE_COMMIT,
        "mission": "The full useful catalytic-mechanism atlas; Atlas-50 is a representation checkpoint, not a benchmark destination.",
        "inherited_atlas10": {
            "selection_id": atlas10["selection_id"],
            "selection_sha256": atlas10_digest,
            "immutable": True,
            "scientific_exit_gate_treated_as_passed": True,
            "case_count": len(inherited_ids),
            "case_ids": inherited_ids,
        },
        "follow_on_surface": {
            "candidate_count": matrix["candidate_count"],
            "proposed_addition_count": len(additions),
            "excluded_blocked_count": len(excluded),
            "proposed_addition_ids": additions,
            "excluded_candidate_ids": excluded,
        },
        "proposed_panel": {
            "total_case_count": len(inherited_ids) + len(additions),
            "case_ids": inherited_ids + additions,
            "shortfall_from_50": 50 - (len(inherited_ids) + len(additions)),
            "forty_additions_emitted": len(additions) == 40,
            "fail_closed": True,
        },
        "representation_projection": {
            "denominator_description": "Immutable Atlas-10 plus all 40 proposed follow-on candidates before fail-closed exclusion.",
            "denominator_case_count": candidate_surface_total,
            "projected_representable_without_family_specific_ad_hoc_fields": projected_representable,
            "projected_percentage": percentage,
            "at_least_90_percent": percentage >= 90,
            "final_section_10_2_result": False,
            "requires_later_compilation_and_case_level_validation": True,
        },
        "pressure_inventory": _pressure_inventory(),
        "governance": {
            "registry_mutation_permitted": False,
            "expansion_freeze_lifted": False,
            "mechanism_compilation_performed": False,
            "gpu_hours": 0,
            "independent_review_claimed": False,
            "outreach_claimed": False,
            "benchmark_created": False,
        },
        "claim_boundary": [
            "The 94% value is a precompilation field-projection check over a deliberately proposed surface, not the final Section 10.2 result.",
            "The 47-case fail-closed proposal is not a frozen selection and contains no newly compiled mechanism objects.",
            "Pressure inventory records selection intent and explicit gaps; it is not an atlas-coverage, accuracy, validation, discovery, design, assay, or speed claim."
        ],
    }


def build_blocker_report(candidate_spec: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    rows = {row["source_identity"]["mcsa_id"]: row for row in matrix["rows"]}
    blockers: list[dict[str, Any]] = []
    for blocker in candidate_spec["blockers"]:
        row = rows[blocker["mcsa_id"]]
        blockers.append(
            {
                "blocker_id": blocker["blocker_id"],
                "candidate_id": row["candidate_id"],
                "mcsa_id": blocker["mcsa_id"],
                "gate": "representation",
                "missing_general_contract": blocker["missing_general_contract"],
                "why_material": blocker["why_material"],
                "unlock_condition": blocker["unlock_condition"],
                "current_disposition": "excluded_from_proposed_panel_pending_governing_contract",
                "convenience_choice_made": False,
            }
        )
    return {
        "schema_version": BLOCKER_SCHEMA_VERSION,
        "report_id": "atlas50.phase-a.blockers.2026-07-14",
        "status": "open_material_representation_blockers",
        "candidate_count": matrix["candidate_count"],
        "passing_candidate_count": matrix["proposed_include_count"],
        "blocked_candidate_count": len(blockers),
        "proposed_total_with_immutable_atlas10": 10 + matrix["proposed_include_count"],
        "shortfall_from_50": 40 - matrix["proposed_include_count"],
        "blockers": blockers,
        "next_action_boundary": "Do not add family-specific fields or compile these cases. A later explicit governing-contract decision is required before any blocked case can enter a selection freeze.",
    }


def validate_crosswalk(value: Any, registry: list[dict[str, Any]]) -> dict[str, int]:
    _require(value.get("schema_version") == CROSSWALK_SCHEMA_VERSION, "unsupported crosswalk output")
    _require(value.get("status") == "machine_draft_unreviewed", "crosswalk status cannot imply review")
    rows = value.get("rows")
    _require(isinstance(rows, list) and len(rows) == 57 and value.get("row_count") == 57, "crosswalk must contain exactly 57 rows")
    _require([row.get("fingerprint_id") for row in rows] == [row["id"] for row in registry], "crosswalk rows differ from protected registry order")
    for index, row in enumerate(rows):
        context = f"crosswalk.rows[{index}]"
        _require(row.get("review_status") == "unreviewed", f"{context} cannot be reviewed without real review")
        _require(row.get("reviewer") is None and row.get("reviewed_at") is None, f"{context} carries invented review metadata")
        _require(row.get("classification") in CLASSIFICATIONS, f"{context} classification is invalid")
        _require(isinstance(row.get("classification_rationale"), str) and len(row["classification_rationale"]) >= 80, f"{context} rationale is too weak")
        _require(isinstance(row.get("uncertainty"), str) and row["uncertainty"], f"{context} uncertainty is missing")
        links = row.get("source_links")
        _require(isinstance(links, dict) and set(links) == set(REQUIRED_SOURCE_KEYS), f"{context} source keys differ")
        for source_key, link in links.items():
            _require_exact_keys(link, {"gap_reason", "lookup_keys", "mapping_assertion", "records", "status", "uris"}, f"{context}.source_links.{source_key}")
            _require(link["mapping_assertion"] == "none_unreviewed_candidate_only", f"{context}.{source_key} asserts a mapping")
            _require(isinstance(link["records"], list) and isinstance(link["uris"], list) and isinstance(link["lookup_keys"], list), f"{context}.{source_key} link arrays are invalid")
            _require(link["records"] or link["uris"] or link["gap_reason"], f"{context}.{source_key} has neither a link nor an explicit gap")
    counts = Counter(row["classification"] for row in rows)
    expected = {classification: counts.get(classification, 0) for classification in CLASSIFICATIONS}
    _require(value.get("classification_counts") == expected, "crosswalk classification summary differs")
    return expected


def validate_candidate_matrix(value: Any) -> None:
    _require(value.get("schema_version") == CANDIDATE_MATRIX_SCHEMA_VERSION, "unsupported candidate matrix")
    _require(value.get("status") == "precompilation_feasibility_projection_unreviewed", "candidate matrix status is invalid")
    rows = value.get("rows")
    _require(isinstance(rows, list) and len(rows) == 40 and value.get("candidate_count") == 40, "candidate matrix must contain exactly 40 rows")
    decisions = Counter(row.get("decision") for row in rows)
    _require(decisions == Counter({"propose_include": 37, "exclude_blocked": 3}), "candidate matrix must fail closed at 37 passing and three blocked")
    _require(value.get("proposed_include_count") == 37 and value.get("excluded_blocked_count") == 3, "candidate summary differs")
    _require(value.get("mechanisms_compiled") == 0 and value.get("gpu_hours") == 0, "Phase A matrix cannot compile mechanisms or use GPUs")
    for index, row in enumerate(rows):
        context = f"candidate_matrix.rows[{index}]"
        _require(row.get("review_status") == "unreviewed", f"{context} cannot imply review")
        _require(row.get("mechanism_compiled") is False, f"{context} cannot compile a mechanism")
        _require(row.get("independent_review_claimed") is False, f"{context} cannot claim independent review")
        _require(row.get("phase_a_compute_ceiling", {}).get("gpu_hours_max") == 0, f"{context} GPU ceiling must be zero")
        _require(row.get("phase_a_compute_ceiling", {}).get("mechanism_compilation_permitted") is False, f"{context} permits mechanism compilation")
        gates = row.get("gates", {})
        _require(set(gates) == {"source", "diversity", "rights", "provenance", "representation"}, f"{context} gate set differs")
        failed = [key for key, gate in gates.items() if gate["outcome"] != "pass"]
        if row["decision"] == "propose_include":
            _require(not failed and row["inclusion_reasons"] and not row["exclusion_reasons"], f"{context} inclusion gate state differs")
        else:
            _require(failed == ["representation"] and row["exclusion_reasons"] and not row["inclusion_reasons"], f"{context} exclusion must be representation-only")
        prohibited = PROHIBITED_PHASE_A_KEYS & set(_walk_keys(row))
        _require(not prohibited, f"{context} contains prohibited compiled fields: {sorted(prohibited)}")


def validate_proposal(value: Any) -> None:
    _require(value.get("schema_version") == PROPOSAL_SCHEMA_VERSION, "unsupported proposal")
    _require(value.get("status") == "proposal_not_selection_freeze", "proposal cannot freeze selection")
    inherited = value.get("inherited_atlas10", {})
    _require(inherited.get("selection_sha256") == ATLAS10_SELECTION_SHA256, "proposal changed Atlas-10 hash")
    _require(inherited.get("immutable") is True and inherited.get("case_count") == 10, "proposal changed immutable Atlas-10")
    panel = value.get("proposed_panel", {})
    _require(panel.get("total_case_count") == 47 and panel.get("shortfall_from_50") == 3, "proposal must report the three-case shortfall")
    _require(panel.get("forty_additions_emitted") is False and panel.get("fail_closed") is True, "proposal did not fail closed")
    projection = value.get("representation_projection", {})
    _require(projection.get("denominator_case_count") == 50, "projection denominator must be the eventual 50-case surface")
    _require(projection.get("projected_representable_without_family_specific_ad_hoc_fields") == 47, "projection numerator differs")
    _require(projection.get("projected_percentage") == 94.0 and projection.get("at_least_90_percent") is True, "projection percentage differs")
    _require(projection.get("final_section_10_2_result") is False, "projection cannot claim final Section 10.2 completion")
    governance = value.get("governance", {})
    for field in ("registry_mutation_permitted", "expansion_freeze_lifted", "mechanism_compilation_performed", "independent_review_claimed", "outreach_claimed", "benchmark_created"):
        _require(governance.get(field) is False, f"proposal governance field {field} must be false")
    _require(governance.get("gpu_hours") == 0, "proposal used GPU work")


def validate_blocker_report(value: Any, matrix: dict[str, Any]) -> None:
    _require(value.get("schema_version") == BLOCKER_SCHEMA_VERSION, "unsupported blocker report")
    _require(value.get("blocked_candidate_count") == 3 and len(value.get("blockers", [])) == 3, "blocker report must contain three blockers")
    excluded = {row["candidate_id"] for row in matrix["rows"] if row["decision"] == "exclude_blocked"}
    _require({blocker["candidate_id"] for blocker in value["blockers"]} == excluded, "blockers differ from excluded rows")
    for blocker in value["blockers"]:
        _require(blocker["gate"] == "representation", "only the representation gate may block this proposal")
        _require(blocker["convenience_choice_made"] is False, "blocker cannot be resolved by convenience")
        _require(blocker["current_disposition"] == "excluded_from_proposed_panel_pending_governing_contract", "blocker disposition differs")


def _normalized_payload(path: Path) -> bytes:
    payload = path.read_bytes()
    if path.suffix.lower() in {".json", ".md", ".py", ".sql", ".toml", ".yaml", ".yml"}:
        return payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return payload


def _scope_content_digest(repo_root: Path, relative: str, kind: str) -> tuple[int, str]:
    tree = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD", "--", relative],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    items: list[tuple[str, str]] = []
    for row in tree:
        metadata, path = row.split("\t", 1)
        _mode, object_kind, object_id = metadata.split()
        _require(object_kind == "blob", f"unexpected Git object in inherited scope: {path}")
        items.append((path, object_id))
    if kind == "blob":
        _require(len(items) == 1 and items[0][0] == relative, f"inherited blob scope differs: {relative}")
    hasher = hashlib.sha256()
    for path, object_id in sorted(items):
        payload = subprocess.run(
            ["git", "cat-file", "-p", object_id],
            cwd=repo_root,
            check=True,
            capture_output=True,
        ).stdout
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".sql", ".toml", ".yaml", ".yml"}:
            payload = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        path_key = path.encode("utf-8")
        hasher.update(path_key + b"\0" + str(len(payload)).encode("ascii") + b"\0" + _sha256_bytes(payload).encode("ascii") + b"\n")
    return len(items), hasher.hexdigest()


def _head_git_object(repo_root: Path, relative: str) -> tuple[str, str]:
    result = subprocess.run(
        ["git", "ls-tree", "HEAD", "--", relative],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    _require(bool(result), f"inherited path is absent from HEAD: {relative}")
    metadata, path = result.split("\t", 1)
    _require(path == relative, f"git tree lookup returned the wrong path for {relative}")
    _mode, kind, object_id = metadata.split()
    return kind, object_id


def validate_inherited_baseline(repo_root: Path) -> dict[str, int]:
    baseline = _load_json(repo_root / PHASE_RELATIVE / "inherited_baseline.json")
    _require(baseline.get("schema_version") == BASELINE_SCHEMA_VERSION, "unsupported inherited baseline")
    _require(baseline.get("baseline_commit") == BASELINE_COMMIT, "inherited baseline commit differs")
    scopes = baseline.get("scopes")
    _require(isinstance(scopes, list) and len(scopes) == 9, "inherited baseline must contain nine scopes")
    total_files = 0
    for index, scope in enumerate(scopes):
        context = f"inherited_baseline.scopes[{index}]"
        _require_exact_keys(scope, {"content_set_sha256", "file_count", "git_object_sha1", "kind", "path"}, context)
        current_count, current_digest = _scope_content_digest(repo_root, scope["path"], scope["kind"])
        _require(current_count == scope["file_count"], f"{context} file count differs")
        _require(current_digest == scope["content_set_sha256"], f"{context} normalized content differs")
        head_kind, head_object = _head_git_object(repo_root, scope["path"])
        _require(head_kind == scope["kind"] and head_object == scope["git_object_sha1"], f"{context} Git object differs from baseline")
        scoped_status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", scope["path"]],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        _require(not scoped_status, f"{context} has staged, unstaged, or untracked changes")
        total_files += current_count

    freeze = _load_json(repo_root / "data/governance/expansion_freeze.json")
    _require(freeze.get("frozen") is True, "protected-registry expansion freeze was lifted")
    expected = freeze.get("expected_sha256", {})
    _require(baseline.get("protected_registry_lf_sha256") == expected, "baseline registry hashes differ from governance freeze")
    for relative, expected_sha in expected.items():
        actual = _sha256_bytes(_normalized_payload(repo_root / relative))
        _require(actual == expected_sha, f"protected registry changed: {relative}")
    return {"scopes": len(scopes), "inherited_files": total_files, "protected_registries": len(expected)}


def _validate_job_ledger(repo_root: Path) -> None:
    ledger = _load_json(repo_root / PHASE_RELATIVE / "job_ledger.json")
    _require(ledger.get("schema_version") == "catalytic-earth.atlas50-phase-a-job-ledger.v1", "unsupported job ledger")
    _require(ledger.get("baseline_commit") == BASELINE_COMMIT, "job ledger baseline differs")
    policy = ledger.get("policy", {})
    _require(policy == {"gpu_hours_max": 0, "registry_mutation_permitted": False, "mechanism_compilation_permitted": False, "performance_evaluation_permitted": False}, "job ledger policy differs")
    jobs = ledger.get("jobs")
    _require(isinstance(jobs, list) and len(jobs) == 4, "job ledger must contain four bounded jobs")
    for index, job in enumerate(jobs):
        for field in ("scientific_question", "cheapest_credible_method", "expected_information_gain", "budget", "reusable_outputs", "stop_condition"):
            _require(field in job and job[field], f"job_ledger.jobs[{index}].{field} is missing")
        _require(job["budget"].get("gpu_hours_max") == 0, f"job_ledger.jobs[{index}] GPU budget must be zero")


def build_phase_a_outputs(repo_root: Path) -> dict[str, dict[str, Any]]:
    phase_dir = repo_root / PHASE_RELATIVE
    registry = _load_json(repo_root / "data/registries/mechanism_fingerprints.json")
    _require(isinstance(registry, list) and len(registry) == 57, "protected fingerprint registry must contain 57 rows")
    crosswalk_spec = _load_json(phase_dir / "crosswalk_spec.json")
    candidate_spec = _load_json(phase_dir / "candidate_spec.json")
    source_catalog = _load_json(phase_dir / "source_catalog.json")
    validate_crosswalk_spec(crosswalk_spec, registry)
    validate_candidate_spec(candidate_spec)
    validate_source_catalog(source_catalog)
    _validate_job_ledger(repo_root)
    validate_inherited_baseline(repo_root)

    crosswalk = build_crosswalk(repo_root, registry, crosswalk_spec, candidate_spec, source_catalog)
    matrix = build_candidate_matrix(candidate_spec)
    proposal = build_proposal(repo_root, matrix)
    blockers = build_blocker_report(candidate_spec, matrix)
    validate_crosswalk(crosswalk, registry)
    validate_candidate_matrix(matrix)
    validate_proposal(proposal)
    validate_blocker_report(blockers, matrix)
    outputs = {
        "crosswalk_draft.json": crosswalk,
        "candidate_matrix.json": matrix,
        "proposed_panel.json": proposal,
        "blocker_report.json": blockers,
    }
    outputs["package_manifest.json"] = build_package_manifest(repo_root, outputs)
    return outputs


def build_package_manifest(
    repo_root: Path, generated: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    static_paths = [
        "data/atlas/atlas50/phase_a/job_ledger.json",
        "data/atlas/atlas50/phase_a/source_catalog.json",
        "data/atlas/atlas50/phase_a/crosswalk_spec.json",
        "data/atlas/atlas50/phase_a/candidate_spec.json",
        "data/atlas/atlas50/phase_a/inherited_baseline.json",
        "src/catalytic_earth/schemas/atlas50-crosswalk-draft-v1.schema.json",
        "src/catalytic_earth/schemas/atlas50-candidate-matrix-v1.schema.json",
        "src/catalytic_earth/schemas/atlas50-proposal-v1.schema.json",
        "src/catalytic_earth/schemas/atlas50-blocker-report-v1.schema.json",
    ]
    artifacts: list[dict[str, Any]] = []
    for relative in static_paths:
        payload = (repo_root / relative).read_bytes()
        artifacts.append(
            {
                "path": relative,
                "role": "input_or_contract",
                "bytes": len(payload),
                "sha256": _sha256_bytes(payload),
            }
        )
    for filename, value in generated.items():
        payload = canonical_json_bytes(value)
        artifacts.append(
            {
                "path": (PHASE_RELATIVE / filename).as_posix(),
                "role": "deterministic_generated_output",
                "bytes": len(payload),
                "sha256": _sha256_bytes(payload),
            }
        )
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "package_id": "atlas50.phase-a.precompilation.2026-07-14",
        "status": "deterministic_precompilation_package",
        "baseline_commit": BASELINE_COMMIT,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "self_hash_excluded": True,
        "governance": {
            "crosswalk_rows": 57,
            "candidate_rows": 40,
            "proposed_additions": 37,
            "proposed_total": 47,
            "open_blockers": 3,
            "reviewed_crosswalk_rows": 0,
            "compiled_follow_on_mechanisms": 0,
            "gpu_hours": 0,
        },
    }


def validate_phase_a_package(repo_root: Path) -> dict[str, Any]:
    expected = build_phase_a_outputs(repo_root)
    phase_dir = repo_root / PHASE_RELATIVE
    for filename, value in expected.items():
        path = phase_dir / filename
        _require(path.is_file(), f"missing generated Phase A artifact: {path.relative_to(repo_root)}")
        _require(path.read_bytes() == canonical_json_bytes(value), f"generated Phase A artifact is stale or nondeterministic: {path.relative_to(repo_root)}")
    manifest = expected["package_manifest.json"]
    _require(manifest["artifact_count"] == len(manifest["artifacts"]), "package manifest artifact count differs")
    return {
        "crosswalk_rows": 57,
        "candidate_rows": 40,
        "proposed_additions": 37,
        "proposed_total": 47,
        "blockers": 3,
        "projection_percentage": 94.0,
        "reviewed_crosswalk_rows": 0,
        "compiled_follow_on_mechanisms": 0,
        "gpu_hours": 0,
    }
