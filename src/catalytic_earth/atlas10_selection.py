"""Machine-enforced selection contract for the Atlas-10 follow-on phase."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .atlas_selection import (
    _require_exact_keys,
    _require_nonempty_string,
    _require_string_list,
    _require_utc_datetime,
    _validate_budget,
)


SCHEMA_VERSION = "catalytic-earth.atlas10-selection.v1"
SELECTION_STATUS = "frozen_precompilation"
FROZEN_SELECTION_SHA256 = "9bc114aaf793c51ec3b6273466f62a83974512a2dcf969d95d8b97453dd2795e"
ATLAS3_SELECTION_ID = "atlas3.kernel.selection.2026-07-13"
ATLAS3_SELECTION_SHA256 = (
    "d24361bb9fc000d39d7209c5538bd23df845a94aa2dce1fb38c18d56dd8e1ada"
)
ATLAS3_CASE_IDS = (
    "atlas3.mcm-pfre.radical",
    "atlas3.mnsod-ecoli.redox",
    "atlas3.tem1-ecoli.covalent",
)
FOLLOW_ON_CASE_IDS = (
    "atlas10.caii-human.proton-relay",
    "atlas10.hewl-chicken.covalent-glycosidase",
    "atlas10.trypsin-fusarium.serine-protease",
    "atlas10.subtilisin-bpn-bacillus.serine-protease",
    "atlas10.mandelate-racemase-pputida.enolate",
    "atlas10.methylaspartate-lyase-ctetanomorphum.enolate",
    "atlas10.cyclophilin-a-human.isomerization",
)
ALL_CASE_IDS = ATLAS3_CASE_IDS + FOLLOW_ON_CASE_IDS
SELECTION_AXES = (
    "proton_relay_and_geometry",
    "alternative_mechanism_preservation",
    "convergent_strategy_unrelated_folds",
    "shared_fold_divergent_chemistry",
    "mandatory_detail_abstention",
)
REQUIRED_OUTPUTS = (
    "canonical_reaction_or_source_gap",
    "source_mechanism_or_abstention",
    "mechanism_hypothesis_or_abstention",
    "protein_site_grounding",
    "counterevidence_and_conflicts",
    "uncertainty_and_abstention",
    "provenance",
    "relationship_query_projection",
)
SOURCE_IDS = {"CATH", "DOI", "M-CSA", "PDB", "Rhea", "UniProtKB"}
EVIDENCE_ROLES = {
    "engineered_source_reference_structure",
    "experimental_structure",
    "fold_classification",
    "net_reaction",
    "official_net_reaction_search_gap",
    "primary_mechanism_evidence",
    "primary_structure_evidence",
    "protein_identity",
    "source_mechanism",
}
APPLICABILITY = {
    "direct",
    "direct_non_detailed",
    "engineered_source_reference",
    "source_gap",
}
SOURCE_DOMAINS = {
    "CATH": "www.cathdb.info",
    "DOI": "doi.org",
    "M-CSA": "www.ebi.ac.uk",
    "PDB": "www.rcsb.org",
    "Rhea": "www.rhea-db.org",
    "UniProtKB": "www.uniprot.org",
}
SOURCE_RECORD_PATTERNS = {
    "CATH": re.compile(r"^CATH:\d+(?:\.\d+){3}$"),
    "DOI": re.compile(r"^10\.\d{4,9}/\S+$"),
    "M-CSA": re.compile(r"^M\d{4}$"),
    "PDB": re.compile(r"^[0-9][A-Za-z0-9]{3}$"),
    "Rhea": re.compile(r"^(?:RHEA:\d+|EC:\d+\.\d+\.\d+\.\d+)$"),
    "UniProtKB": re.compile(r"^[A-Z0-9]{6,10}$"),
}

CONVERGENT_GROUP = "atlas10.relationship.convergent-serine-proteases"
DIVERGENT_GROUP = "atlas10.relationship.divergent-enolase-chemistry"
RELATIONSHIP_EXPECTATIONS = {
    CONVERGENT_GROUP: {
        "relationship_type": "convergent_strategy_unrelated_folds",
        "case_ids": (
            "atlas10.trypsin-fusarium.serine-protease",
            "atlas10.subtilisin-bpn-bacillus.serine-protease",
        ),
        "folds": ("CATH:2.40.10.10", "CATH:3.40.50.200"),
        "query_id": "atlas10.query.convergent-strategy",
    },
    DIVERGENT_GROUP: {
        "relationship_type": "shared_fold_divergent_chemistry",
        "case_ids": (
            "atlas10.mandelate-racemase-pputida.enolate",
            "atlas10.methylaspartate-lyase-ctetanomorphum.enolate",
        ),
        "folds": ("CATH:3.20.20.120",),
        "query_id": "atlas10.query.shared-fold-divergent-chemistry",
    },
}


def _sources(*values: tuple[str, str, str, str]) -> set[tuple[str, str, str, str]]:
    return set(values)


CASE_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "atlas10.caii-human.proton-relay": {
        "axis": "proton_relay_and_geometry",
        "target": "mechanism:caii-human-proton-relay-v1",
        "ec": "4.2.1.1",
        "fingerprint": "zinc_lyase_hydratase",
        "participants": {"CHEBI:17544", "CHEBI:15378", "CHEBI:16526", "CHEBI:15377"},
        "folds": {"CATH:3.10.200.10"},
        "groups": (),
        "mcsa": ("M0216", "detailed_direct", "compile_source_steps"),
        "sources": _sources(
            ("UniProtKB", "P00918", "protein_identity", "direct"),
            ("Rhea", "RHEA:10748", "net_reaction", "direct"),
            ("PDB", "1CA2", "experimental_structure", "direct"),
            ("M-CSA", "M0216", "source_mechanism", "direct"),
            ("DOI", "10.1021/bi0480279", "primary_mechanism_evidence", "direct"),
            ("CATH", "CATH:3.10.200.10", "fold_classification", "direct"),
        ),
    },
    "atlas10.hewl-chicken.covalent-glycosidase": {
        "axis": "alternative_mechanism_preservation",
        "target": "mechanism:hewl-chicken-covalent-glycosidase-v1",
        "ec": "3.2.1.17",
        "fingerprint": "glycoside_hydrolase",
        "participants": {"CHEBI:15377", "CHEBI:87004", "CHEBI:40729", "CHEBI:28009"},
        "folds": {"CATH:1.10.530.10"},
        "groups": (),
        "mcsa": (
            "M0203",
            "detailed_direct_with_alternatives",
            "preserve_competing_source_steps",
        ),
        "sources": _sources(
            ("UniProtKB", "P00698", "protein_identity", "direct"),
            ("Rhea", "EC:3.2.1.17", "official_net_reaction_search_gap", "source_gap"),
            ("PDB", "1DPX", "experimental_structure", "direct"),
            ("M-CSA", "M0203", "source_mechanism", "direct"),
            ("DOI", "10.1038/35090602", "primary_mechanism_evidence", "direct"),
            ("CATH", "CATH:1.10.530.10", "fold_classification", "direct"),
        ),
    },
    "atlas10.trypsin-fusarium.serine-protease": {
        "axis": "convergent_strategy_unrelated_folds",
        "target": "mechanism:trypsin-fusarium-serine-protease-v1",
        "ec": "3.4.21.4",
        "fingerprint": "ser_his_acid_hydrolase",
        "participants": {"CHEBI:15377", "CHEBI:90799", "CHEBI:59869"},
        "folds": {"CATH:2.40.10.10"},
        "groups": (CONVERGENT_GROUP,),
        "mcsa": ("M0173", "detailed_direct", "compile_source_steps"),
        "sources": _sources(
            ("UniProtKB", "P35049", "protein_identity", "direct"),
            ("Rhea", "EC:3.4.21.4", "official_net_reaction_search_gap", "source_gap"),
            ("PDB", "1PQ5", "experimental_structure", "direct"),
            ("M-CSA", "M0173", "source_mechanism", "direct"),
            ("DOI", "10.1074/jbc.m306944200", "primary_structure_evidence", "direct"),
            ("CATH", "CATH:2.40.10.10", "fold_classification", "direct"),
        ),
    },
    "atlas10.subtilisin-bpn-bacillus.serine-protease": {
        "axis": "convergent_strategy_unrelated_folds",
        "target": "mechanism:subtilisin-bpn-bacillus-serine-protease-v1",
        "ec": "3.4.21.62",
        "fingerprint": "ser_his_acid_hydrolase",
        "participants": {"CHEBI:15377", "CHEBI:90799", "CHEBI:59869"},
        "folds": {"CATH:3.40.50.200"},
        "groups": (CONVERGENT_GROUP,),
        "mcsa": ("M0723", "detailed_direct", "compile_source_steps"),
        "sources": _sources(
            ("UniProtKB", "P00782", "protein_identity", "direct"),
            ("Rhea", "EC:3.4.21.62", "official_net_reaction_search_gap", "source_gap"),
            ("PDB", "1SUP", "experimental_structure", "direct"),
            (
                "PDB",
                "1S01",
                "engineered_source_reference_structure",
                "engineered_source_reference",
            ),
            ("M-CSA", "M0723", "source_mechanism", "direct"),
            ("DOI", "10.1107/S0907444996007500", "primary_structure_evidence", "direct"),
            ("DOI", "10.1073/pnas.83.11.3743", "primary_mechanism_evidence", "direct"),
            ("CATH", "CATH:3.40.50.200", "fold_classification", "direct"),
        ),
    },
    "atlas10.mandelate-racemase-pputida.enolate": {
        "axis": "shared_fold_divergent_chemistry",
        "target": "mechanism:mandelate-racemase-pputida-enolate-v1",
        "ec": "5.1.2.2",
        "fingerprint": "metal_racemase_epimerase_non_plp",
        "participants": {"CHEBI:17756", "CHEBI:32382"},
        "folds": {"CATH:3.20.20.120"},
        "groups": (DIVERGENT_GROUP,),
        "mcsa": ("M0187", "detailed_direct", "compile_source_steps"),
        "sources": _sources(
            ("UniProtKB", "P11444", "protein_identity", "direct"),
            ("Rhea", "RHEA:13945", "net_reaction", "direct"),
            ("PDB", "1MNS", "experimental_structure", "direct"),
            ("M-CSA", "M0187", "source_mechanism", "direct"),
            ("DOI", "10.1021/bi00102a019", "primary_structure_evidence", "direct"),
            ("CATH", "CATH:3.20.20.120", "fold_classification", "direct"),
        ),
    },
    "atlas10.methylaspartate-lyase-ctetanomorphum.enolate": {
        "axis": "shared_fold_divergent_chemistry",
        "target": "mechanism:methylaspartate-lyase-ctetanomorphum-enolate-v1",
        "ec": "4.3.1.2",
        "fingerprint": None,
        "participants": {"CHEBI:58724", "CHEBI:36986", "CHEBI:28938"},
        "folds": {"CATH:3.20.20.120", "CATH:3.30.390.10"},
        "groups": (DIVERGENT_GROUP,),
        "mcsa": ("M0468", "detailed_direct", "compile_source_steps"),
        "sources": _sources(
            ("UniProtKB", "Q05514", "protein_identity", "direct"),
            ("Rhea", "RHEA:12829", "net_reaction", "direct"),
            ("PDB", "1KCZ", "experimental_structure", "direct"),
            ("M-CSA", "M0468", "source_mechanism", "direct"),
            ("DOI", "10.1074/jbc.m111180200", "primary_structure_evidence", "direct"),
            ("CATH", "CATH:3.20.20.120", "fold_classification", "direct"),
            ("CATH", "CATH:3.30.390.10", "fold_classification", "direct"),
        ),
    },
    "atlas10.cyclophilin-a-human.isomerization": {
        "axis": "mandatory_detail_abstention",
        "target": "mechanism:cyclophilin-a-human-isomerization-v1",
        "ec": "5.2.1.8",
        "fingerprint": None,
        "participants": {
            "CHEBI:83834",
            "CHEBI:83833",
            "RHEA-COMP:10747",
            "RHEA-COMP:10748",
        },
        "folds": {"CATH:2.40.100.10"},
        "groups": (),
        "mcsa": (
            "M0189",
            "non_detailed_direct",
            "mandatory_abstention_from_discrete_step_edits",
        ),
        "sources": _sources(
            ("UniProtKB", "P62937", "protein_identity", "direct"),
            ("Rhea", "RHEA:16237", "net_reaction", "direct"),
            ("PDB", "1M9C", "experimental_structure", "direct"),
            ("M-CSA", "M0189", "source_mechanism", "direct_non_detailed"),
            ("DOI", "10.1038/nsb927", "primary_structure_evidence", "direct"),
            ("CATH", "CATH:2.40.100.10", "fold_classification", "direct"),
        ),
    },
}


def _validate_source_handle(value: Any, context: str) -> tuple[str, str, str, str]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    _require_exact_keys(
        value,
        {
            "applicability",
            "evidence_role",
            "record_id",
            "source_id",
            "uri",
            "verification_note",
            "verified_at",
        },
        context,
    )
    source_id = value["source_id"]
    record_id = value["record_id"]
    role = value["evidence_role"]
    applicability = value["applicability"]
    if source_id not in SOURCE_IDS:
        raise ValueError(f"{context}.source_id is unsupported: {source_id!r}")
    if not isinstance(record_id, str) or not SOURCE_RECORD_PATTERNS[source_id].fullmatch(
        record_id
    ):
        raise ValueError(f"{context}.record_id is invalid for {source_id}: {record_id!r}")
    if role not in EVIDENCE_ROLES:
        raise ValueError(f"{context}.evidence_role is unsupported: {role!r}")
    if applicability not in APPLICABILITY:
        raise ValueError(f"{context}.applicability is unsupported: {applicability!r}")

    if applicability == "source_gap":
        if (source_id, role) != ("Rhea", "official_net_reaction_search_gap"):
            raise ValueError(f"{context} source gaps must be official Rhea EC queries")
        if not record_id.startswith("EC:"):
            raise ValueError(f"{context} Rhea source-gap record_id must preserve the EC query")
    elif role == "official_net_reaction_search_gap":
        raise ValueError(f"{context} reaction-search gaps cannot be marked direct")

    if applicability == "direct_non_detailed":
        if (source_id, role) != ("M-CSA", "source_mechanism"):
            raise ValueError(f"{context} non-detailed applicability is reserved for M-CSA")
    if applicability == "engineered_source_reference":
        if (source_id, role) != (
            "PDB",
            "engineered_source_reference_structure",
        ):
            raise ValueError(f"{context} engineered references must be PDB structures")
    elif role == "engineered_source_reference_structure":
        raise ValueError(f"{context} engineered structures cannot be marked direct")

    role_sources = {
        "fold_classification": {"CATH"},
        "net_reaction": {"Rhea"},
        "protein_identity": {"UniProtKB"},
        "source_mechanism": {"M-CSA"},
        "experimental_structure": {"PDB"},
    }
    if role in role_sources and source_id not in role_sources[role]:
        raise ValueError(f"{context}.{role} has the wrong authoritative source")

    uri = _require_nonempty_string(value["uri"], f"{context}.uri")
    parsed = urlparse(uri)
    if parsed.scheme != "https" or parsed.netloc != SOURCE_DOMAINS[source_id]:
        raise ValueError(f"{context}.uri is not on the authoritative {source_id} domain")
    if source_id == "DOI" and parsed.path.lstrip("/").lower() != record_id.lower():
        raise ValueError(f"{context}.uri does not resolve its DOI record_id")
    if source_id == "CATH" and not parsed.path.rstrip("/").endswith(
        record_id.removeprefix("CATH:")
    ):
        raise ValueError(f"{context}.uri does not resolve its CATH record_id")
    _require_utc_datetime(value["verified_at"], f"{context}.verified_at")
    _require_nonempty_string(value["verification_note"], f"{context}.verification_note")
    return source_id, record_id, role, applicability


def _validate_source_mechanism_contract(
    value: Any, context: str, expected: tuple[str, str, str]
) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    _require_exact_keys(
        value,
        {
            "annotation_level",
            "highest_target_tier",
            "mandatory_abstentions",
            "mcsa_record_id",
            "step_detail_policy",
        },
        context,
    )
    actual = (
        value["mcsa_record_id"],
        value["annotation_level"],
        value["step_detail_policy"],
    )
    if actual != expected:
        raise ValueError(f"{context} differs from the frozen source-granularity contract")
    if value["highest_target_tier"] != 2:
        raise ValueError(f"{context}.highest_target_tier must remain 2")
    _require_string_list(
        value["mandatory_abstentions"],
        f"{context}.mandatory_abstentions",
        minimum=2,
    )


def _validate_fingerprint(value: Any, context: str, expected: str | None) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    _require_exact_keys(value, {"fingerprint_id", "registry_write", "use"}, context)
    if value["fingerprint_id"] != expected:
        raise ValueError(f"{context}.fingerprint_id differs from the frozen crosswalk")
    if value["use"] != "historical_crosswalk_only_not_evidence":
        raise ValueError(f"{context}.use must keep fingerprints outside the evidence chain")
    if value["registry_write"] is not False:
        raise ValueError(f"{context}.registry_write cannot authorize registry mutation")


def _validate_case(value: Any, index: int, frozen_at: str) -> dict[str, Any]:
    context = f"follow_on_cases[{index}]"
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    _require_exact_keys(
        value,
        {
            "assay_candidate",
            "case_compute_budget",
            "case_id",
            "ec_number",
            "fingerprint_bridge",
            "fold_classification_ids",
            "known_ambiguities",
            "label",
            "organism",
            "reaction_participant_ids",
            "relationship_group_ids",
            "representation_axis",
            "representation_pressures",
            "required_outputs",
            "selection_rationale",
            "source_handles",
            "source_mechanism_contract",
            "stop_conditions",
            "success_condition",
            "target_evidence_tier",
            "target_record_id",
        },
        context,
    )
    case_id = _require_nonempty_string(value["case_id"], f"{context}.case_id")
    if case_id not in CASE_EXPECTATIONS:
        raise ValueError(f"{context}.case_id is outside the frozen Atlas-10 follow-on")
    expected = CASE_EXPECTATIONS[case_id]
    scalar_expectations = {
        "representation_axis": expected["axis"],
        "target_record_id": expected["target"],
        "ec_number": expected["ec"],
        "target_evidence_tier": 2,
        "assay_candidate": False,
    }
    for field, expected_value in scalar_expectations.items():
        if value[field] != expected_value:
            raise ValueError(f"{context}.{field} differs from the frozen selection")
    for field in ("label", "organism", "selection_rationale", "success_condition"):
        _require_nonempty_string(value[field], f"{context}.{field}")

    pressures = _require_string_list(
        value["representation_pressures"],
        f"{context}.representation_pressures",
        minimum=3,
    )
    if pressures[0] != expected["axis"]:
        raise ValueError(f"{context}.representation_pressures must lead with its axis")
    if tuple(value["relationship_group_ids"]) != expected["groups"]:
        raise ValueError(f"{context}.relationship_group_ids differ from the frozen selection")
    _validate_fingerprint(
        value["fingerprint_bridge"], f"{context}.fingerprint_bridge", expected["fingerprint"]
    )
    _validate_source_mechanism_contract(
        value["source_mechanism_contract"],
        f"{context}.source_mechanism_contract",
        expected["mcsa"],
    )
    participants = _require_string_list(
        value["reaction_participant_ids"],
        f"{context}.reaction_participant_ids",
        minimum=2,
    )
    if any(not re.fullmatch(r"(?:CHEBI|RHEA-COMP):\d+", item) for item in participants):
        raise ValueError(f"{context}.reaction_participant_ids contain unsupported identifiers")
    if set(participants) != expected["participants"]:
        raise ValueError(f"{context}.reaction_participant_ids differ from the frozen selection")
    folds = _require_string_list(
        value["fold_classification_ids"], f"{context}.fold_classification_ids"
    )
    if set(folds) != expected["folds"]:
        raise ValueError(f"{context}.fold_classification_ids differ from the frozen selection")
    if tuple(value["required_outputs"]) != REQUIRED_OUTPUTS:
        raise ValueError(f"{context}.required_outputs differ from the Atlas-10 contract")
    _require_string_list(value["known_ambiguities"], f"{context}.known_ambiguities", minimum=3)
    _require_string_list(value["stop_conditions"], f"{context}.stop_conditions", minimum=4)
    _validate_budget(value["case_compute_budget"], f"{context}.case_compute_budget")

    handles = value["source_handles"]
    if not isinstance(handles, list) or len(handles) < 5:
        raise ValueError(f"{context}.source_handles must contain at least five handles")
    source_keys = {
        _validate_source_handle(handle, f"{context}.source_handles[{handle_index}]")
        for handle_index, handle in enumerate(handles)
    }
    if len(source_keys) != len(handles):
        raise ValueError(f"{context}.source_handles contains duplicates")
    if source_keys != expected["sources"]:
        raise ValueError(f"{context}.source_handles differ from the frozen authoritative set")
    if any(handle["verified_at"] != frozen_at for handle in handles):
        raise ValueError(f"{context} source handles must share the selection freeze timestamp")
    return value


def _validate_relationships(value: Any, cases: dict[str, dict[str, Any]]) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("relationship_groups must contain exactly the two frozen groups")
    fields = {
        "case_ids",
        "comparison_claim",
        "fold_classification_ids",
        "group_id",
        "relationship_type",
        "required_query_id",
        "transfer_prohibition",
    }
    seen: set[str] = set()
    for index, group in enumerate(value):
        context = f"relationship_groups[{index}]"
        if not isinstance(group, dict):
            raise ValueError(f"{context} must be an object")
        _require_exact_keys(group, fields, context)
        group_id = group["group_id"]
        if group_id not in RELATIONSHIP_EXPECTATIONS or group_id in seen:
            raise ValueError(f"{context}.group_id differs from the frozen relationship set")
        seen.add(group_id)
        expected = RELATIONSHIP_EXPECTATIONS[group_id]
        if group["relationship_type"] != expected["relationship_type"]:
            raise ValueError(f"{context}.relationship_type differs")
        if tuple(group["case_ids"]) != expected["case_ids"]:
            raise ValueError(f"{context}.case_ids differ from the frozen pair")
        if tuple(group["fold_classification_ids"]) != expected["folds"]:
            raise ValueError(f"{context}.fold_classification_ids differ")
        if group["required_query_id"] != expected["query_id"]:
            raise ValueError(f"{context}.required_query_id differs")
        _require_nonempty_string(group["comparison_claim"], f"{context}.comparison_claim")
        _require_nonempty_string(
            group["transfer_prohibition"], f"{context}.transfer_prohibition"
        )
        for case_id in expected["case_ids"]:
            if group_id not in cases[case_id]["relationship_group_ids"]:
                raise ValueError(f"{context} is not reciprocally linked from {case_id}")
    if seen != set(RELATIONSHIP_EXPECTATIONS):
        raise ValueError("relationship group identities differ from the frozen set")


def _validate_queries(value: Any) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("query_contracts must contain exactly two frozen queries")
    fields = {
        "case_ids",
        "prohibited_shortcut",
        "query_id",
        "question",
        "relationship_group_id",
        "required_fields",
        "success_condition",
    }
    seen: set[str] = set()
    for index, query in enumerate(value):
        context = f"query_contracts[{index}]"
        if not isinstance(query, dict):
            raise ValueError(f"{context} must be an object")
        _require_exact_keys(query, fields, context)
        group_id = query["relationship_group_id"]
        if group_id not in RELATIONSHIP_EXPECTATIONS:
            raise ValueError(f"{context}.relationship_group_id differs")
        expected = RELATIONSHIP_EXPECTATIONS[group_id]
        if query["query_id"] != expected["query_id"] or query["query_id"] in seen:
            raise ValueError(f"{context}.query_id differs from the frozen query set")
        seen.add(query["query_id"])
        if tuple(query["case_ids"]) != expected["case_ids"]:
            raise ValueError(f"{context}.case_ids differ from its relationship group")
        _require_string_list(query["required_fields"], f"{context}.required_fields", minimum=7)
        for field in ("question", "success_condition", "prohibited_shortcut"):
            _require_nonempty_string(query[field], f"{context}.{field}")


def _validate_baseline(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("baseline_contract must be an object")
    _require_exact_keys(
        value,
        {
            "atlas_outputs_prohibited_as_inputs",
            "baseline_id",
            "claim_boundary",
            "comparator",
            "measurements",
            "same_source_budget_required",
            "status",
        },
        "baseline_contract",
    )
    if value["baseline_id"] != "atlas10.unintegrated-source-stack.v1":
        raise ValueError("baseline_contract.baseline_id differs from the frozen comparator")
    if value["status"] != "frozen_before_compilation":
        raise ValueError("baseline_contract must be frozen before compilation")
    if value["same_source_budget_required"] is not True:
        raise ValueError("baseline_contract must use the same source budget")
    if value["atlas_outputs_prohibited_as_inputs"] is not True:
        raise ValueError("baseline_contract cannot consume Atlas outputs")
    _require_string_list(value["measurements"], "baseline_contract.measurements", minimum=6)
    _require_nonempty_string(value["comparator"], "baseline_contract.comparator")
    _require_nonempty_string(value["claim_boundary"], "baseline_contract.claim_boundary")


def _validate_review(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("review_contract must be an object")
    _require_exact_keys(
        value,
        {
            "external_response_required_for_phase_exit",
            "external_review_attempt_required",
            "independent_reviewer_target",
            "micro_questions",
            "no_response_disposition",
            "packet_count_max",
            "packet_count_min",
            "review_unit",
            "status",
            "upstream_curation_counts_as_independent_review",
        },
        "review_contract",
    )
    expected = {
        "status": "frozen_before_compilation",
        "packet_count_min": 5,
        "packet_count_max": 10,
        "review_unit": "bounded_claim_packet",
        "independent_reviewer_target": True,
        "upstream_curation_counts_as_independent_review": False,
        "external_review_attempt_required": True,
        "external_response_required_for_phase_exit": False,
    }
    for field, expected_value in expected.items():
        if value[field] != expected_value:
            raise ValueError(f"review_contract.{field} differs from the frozen review boundary")
    questions = _require_string_list(
        value["micro_questions"], "review_contract.micro_questions", minimum=5
    )
    if len(questions) != 5:
        raise ValueError("review_contract must freeze exactly five micro-questions")
    _require_nonempty_string(
        value["no_response_disposition"], "review_contract.no_response_disposition"
    )


def _validate_assay_lane(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("assay_lane must be an object")
    _require_exact_keys(
        value,
        {
            "assay_name",
            "candidate_case_id",
            "decision_frozen_before_results",
            "external_execution_required",
            "inherited_from_selection_sha256",
            "materials_committed",
            "new_assay_candidates_permitted",
            "preregistration_required",
            "status",
            "stop_conditions",
        },
        "assay_lane",
    )
    expected = {
        "candidate_case_id": "atlas3.tem1-ecoli.covalent",
        "inherited_from_selection_sha256": ATLAS3_SELECTION_SHA256,
        "status": "candidate_only_not_started",
        "assay_name": "nitrocefin hydrolysis absorbance assay",
        "new_assay_candidates_permitted": False,
        "external_execution_required": True,
        "preregistration_required": True,
        "decision_frozen_before_results": True,
        "materials_committed": False,
    }
    for field, expected_value in expected.items():
        if value[field] != expected_value:
            raise ValueError(f"assay_lane.{field} differs from the inherited TEM-1 lane")
    _require_string_list(value["stop_conditions"], "assay_lane.stop_conditions", minimum=4)


def validate_atlas10_selection(value: Any) -> dict[str, int | str]:
    """Validate and summarize the frozen seven-case Atlas-10 extension."""
    if not isinstance(value, dict):
        raise ValueError("Atlas-10 selection must be an object")
    _require_exact_keys(
        value,
        {
            "all_case_ids",
            "assay_lane",
            "baseline_commit",
            "baseline_contract",
            "exit_gate",
            "follow_on_cases",
            "frozen_at",
            "inherited_selection",
            "namespace",
            "objective",
            "phase_compute_budget",
            "prohibited_claims",
            "query_contracts",
            "registry_mutation_permitted",
            "relationship_groups",
            "review_contract",
            "schema_version",
            "selection_axes",
            "selection_id",
            "status",
        },
        "selection",
    )
    if value["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported Atlas-10 selection schema: {value['schema_version']!r}")
    if value["status"] != SELECTION_STATUS:
        raise ValueError("Atlas-10 selection is not frozen before compilation")
    _require_nonempty_string(value["selection_id"], "selection_id")
    frozen_at = _require_utc_datetime(value["frozen_at"], "frozen_at")
    _require_nonempty_string(value["objective"], "objective")
    if not isinstance(value["baseline_commit"], str) or not re.fullmatch(
        r"[0-9a-f]{40}", value["baseline_commit"]
    ):
        raise ValueError("baseline_commit must be a full lowercase Git commit")
    if value["namespace"] != "data/atlas/atlas10":
        raise ValueError("Atlas-10 must compile in its lean atlas namespace")
    if value["registry_mutation_permitted"] is not False:
        raise ValueError("Atlas-10 selection cannot authorize protected registry mutation")

    inherited = value["inherited_selection"]
    if not isinstance(inherited, dict):
        raise ValueError("inherited_selection must be an object")
    _require_exact_keys(
        inherited, {"case_ids", "immutable", "selection_id", "selection_sha256"}, "inherited_selection"
    )
    if inherited != {
        "selection_id": ATLAS3_SELECTION_ID,
        "selection_sha256": ATLAS3_SELECTION_SHA256,
        "case_ids": list(ATLAS3_CASE_IDS),
        "immutable": True,
    }:
        raise ValueError("inherited_selection differs from the frozen Atlas-3 kernel")
    if tuple(value["all_case_ids"]) != ALL_CASE_IDS:
        raise ValueError("all_case_ids must preserve Atlas-3 and add exactly seven cases")
    if tuple(value["selection_axes"]) != SELECTION_AXES:
        raise ValueError("selection_axes differ from the frozen pressure set")

    phase_budget = _validate_budget(value["phase_compute_budget"], "phase_compute_budget")
    raw_cases = value["follow_on_cases"]
    if not isinstance(raw_cases, list) or len(raw_cases) != 7:
        raise ValueError("Atlas-10 requires exactly seven follow-on cases")
    cases = [_validate_case(case, index, frozen_at) for index, case in enumerate(raw_cases)]
    if tuple(case["case_id"] for case in cases) != FOLLOW_ON_CASE_IDS:
        raise ValueError("Atlas-10 follow-on cases differ from the frozen order and identities")
    by_id = {case["case_id"]: case for case in cases}
    for field in ("cpu_hours_max", "download_bytes_max", "external_requests_max"):
        total = sum(case["case_compute_budget"][field] for case in cases)
        if total > phase_budget[field]:
            raise ValueError(f"case {field} ceilings exceed the phase ceiling")
    if any(case["assay_candidate"] for case in cases):
        raise ValueError("Atlas-10 cannot select a new assay candidate")

    _validate_relationships(value["relationship_groups"], by_id)
    _validate_queries(value["query_contracts"])
    _validate_baseline(value["baseline_contract"])
    _validate_review(value["review_contract"])
    _validate_assay_lane(value["assay_lane"])
    _require_string_list(value["exit_gate"], "exit_gate", minimum=10)
    _require_string_list(value["prohibited_claims"], "prohibited_claims", minimum=8)

    canonical = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    if digest != FROZEN_SELECTION_SHA256:
        raise ValueError("Atlas-10 selection content differs from its frozen canonical digest")
    source_handles = [handle for case in cases for handle in case["source_handles"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": SELECTION_STATUS,
        "inherited_cases": 3,
        "follow_on_cases": 7,
        "total_cases": 10,
        "authoritative_source_handles": len(source_handles),
        "documented_rhea_gaps": sum(
            handle["applicability"] == "source_gap" for handle in source_handles
        ),
        "mandatory_detail_abstentions": sum(
            case["source_mechanism_contract"]["step_detail_policy"]
            == "mandatory_abstention_from_discrete_step_edits"
            for case in cases
        ),
        "relationship_groups": 2,
        "query_contracts": 2,
        "new_assay_candidates": 0,
        "gpu_hours_max": phase_budget["gpu_hours_max"],
        "selection_sha256": digest,
    }


def load_atlas10_selection(path: Path) -> dict[str, Any]:
    """Load and validate an Atlas-10 selection JSON file."""
    value = json.loads(path.read_text(encoding="utf-8"))
    validate_atlas10_selection(value)
    return value
