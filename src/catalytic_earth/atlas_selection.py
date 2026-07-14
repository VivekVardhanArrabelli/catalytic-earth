"""Machine-enforced precompilation contract for the first biological atlas kernel."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCHEMA_VERSION = "catalytic-earth.atlas3-selection.v1"
SELECTION_STATUS = "frozen_precompilation"
FROZEN_SELECTION_SHA256 = "d24361bb9fc000d39d7209c5538bd23df845a94aa2dce1fb38c18d56dd8e1ada"
SELECTION_AXES = (
    "radical_rearrangement",
    "metal_redox_pcet",
    "covalent_acyl_enzyme",
)
REQUIRED_OUTPUTS = (
    "canonical_reaction",
    "source_mechanism",
    "mechanism_hypothesis",
    "protein_site_grounding",
    "counterevidence_and_conflicts",
    "uncertainty_and_abstention",
    "provenance",
)
SOURCE_IDS = {"DOI", "M-CSA", "PDB", "PMCID", "Rhea", "UniProtKB"}
EVIDENCE_ROLES = {
    "assay_precedent",
    "experimental_structure",
    "net_reaction",
    "primary_mechanism_evidence",
    "primary_structure_evidence",
    "protein_identity",
    "same_ec_counterexample",
    "source_mechanism",
}
APPLICABILITY = {"direct", "counterexample_same_ec"}
SOURCE_DOMAINS = {
    "DOI": "doi.org",
    "M-CSA": "www.ebi.ac.uk",
    "PDB": "www.rcsb.org",
    "PMCID": "pmc.ncbi.nlm.nih.gov",
    "Rhea": "www.rhea-db.org",
    "UniProtKB": "www.uniprot.org",
}
SOURCE_RECORD_PATTERNS = {
    "DOI": re.compile(r"^10\.\d{4,9}/\S+$"),
    "M-CSA": re.compile(r"^M\d{4}$"),
    "PDB": re.compile(r"^[0-9][A-Za-z0-9]{3}$"),
    "PMCID": re.compile(r"^PMC\d+$"),
    "Rhea": re.compile(r"^RHEA:\d+$"),
    "UniProtKB": re.compile(r"^[A-Z0-9]{6,10}$"),
}
CASE_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "atlas3.mcm-pfre.radical": {
        "axis": "radical_rearrangement",
        "target_record_id": "mechanism:mcm-pfre-radical-v1",
        "fingerprint_bridge": "cobalamin_radical_rearrangement",
        "reaction_participants": {"CHEBI:57292", "CHEBI:57326"},
        "sources": {
            ("UniProtKB", "P11653", "protein_identity", "direct"),
            ("UniProtKB", "P11652", "protein_identity", "direct"),
            ("Rhea", "RHEA:22888", "net_reaction", "direct"),
            ("PDB", "1REQ", "experimental_structure", "direct"),
            ("M-CSA", "M0062", "source_mechanism", "direct"),
            (
                "DOI",
                "10.1016/s0969-2126(96)00037-8",
                "primary_structure_evidence",
                "direct",
            ),
        },
    },
    "atlas3.mnsod-ecoli.redox": {
        "axis": "metal_redox_pcet",
        "target_record_id": "mechanism:mnsod-ecoli-redox-v1",
        "fingerprint_bridge": "manganese_iron_superoxide_dismutase",
        "reaction_participants": {
            "CHEBI:15378",
            "CHEBI:15379",
            "CHEBI:16240",
            "CHEBI:18421",
        },
        "sources": {
            ("UniProtKB", "P00448", "protein_identity", "direct"),
            ("Rhea", "RHEA:20696", "net_reaction", "direct"),
            ("PDB", "1D5N", "experimental_structure", "direct"),
            (
                "DOI",
                "10.1006/jmbi.1999.3506",
                "primary_structure_evidence",
                "direct",
            ),
            (
                "DOI",
                "10.1021/bi9704212",
                "primary_mechanism_evidence",
                "direct",
            ),
            (
                "M-CSA",
                "M0138",
                "same_ec_counterexample",
                "counterexample_same_ec",
            ),
        },
    },
    "atlas3.tem1-ecoli.covalent": {
        "axis": "covalent_acyl_enzyme",
        "target_record_id": "mechanism:tem1-ecoli-covalent-v1",
        "fingerprint_bridge": "serine_beta_lactamase",
        "reaction_participants": {"CHEBI:15377", "CHEBI:35627", "CHEBI:140347"},
        "sources": {
            ("UniProtKB", "P62593", "protein_identity", "direct"),
            ("Rhea", "RHEA:20401", "net_reaction", "direct"),
            ("PDB", "1BTL", "experimental_structure", "direct"),
            ("M-CSA", "M0002", "source_mechanism", "direct"),
            (
                "DOI",
                "10.1073/pnas.060027897",
                "primary_mechanism_evidence",
                "direct",
            ),
            ("PMCID", "PMC14582", "assay_precedent", "direct"),
        },
    },
}


def _require_exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"{context} keys differ; missing={missing}, extra={extra}")


def _require_nonempty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a non-empty string")
    return value


def _require_utc_datetime(value: Any, context: str) -> str:
    text = _require_nonempty_string(value, context)
    if not text.endswith("Z"):
        raise ValueError(f"{context} must use an explicit UTC Z suffix")
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{context} must be an ISO-8601 date-time") from exc
    if parsed.tzinfo != timezone.utc:
        raise ValueError(f"{context} must be UTC")
    return text


def _require_string_list(value: Any, context: str, *, minimum: int = 1) -> list[str]:
    if (
        not isinstance(value, list)
        or len(value) < minimum
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise ValueError(f"{context} must contain at least {minimum} non-empty strings")
    if len(set(value)) != len(value):
        raise ValueError(f"{context} contains duplicates")
    return value


def _validate_budget(value: Any, context: str) -> dict[str, int | bool]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    _require_exact_keys(
        value,
        {
            "cpu_hours_max",
            "download_bytes_max",
            "external_requests_max",
            "gpu_hours_max",
            "reuse_required",
            "stop_if_exceeded",
        },
        context,
    )
    for field in (
        "cpu_hours_max",
        "download_bytes_max",
        "external_requests_max",
        "gpu_hours_max",
    ):
        number = value[field]
        if not isinstance(number, int) or isinstance(number, bool) or number < 0:
            raise ValueError(f"{context}.{field} must be a non-negative integer")
    if value["cpu_hours_max"] == 0 or value["download_bytes_max"] == 0:
        raise ValueError(f"{context} must permit bounded CPU and download work")
    if value["gpu_hours_max"] != 0:
        raise ValueError(f"{context}.gpu_hours_max must remain zero for Atlas-3")
    if value["reuse_required"] is not True or value["stop_if_exceeded"] is not True:
        raise ValueError(f"{context} must require reuse and stop at its ceiling")
    return value


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
    if applicability == "counterexample_same_ec" and role != "same_ec_counterexample":
        raise ValueError(f"{context} counterexamples require same_ec_counterexample role")
    if role == "same_ec_counterexample" and applicability != "counterexample_same_ec":
        raise ValueError(f"{context} same-EC counterexamples cannot be marked direct")
    uri = _require_nonempty_string(value["uri"], f"{context}.uri")
    parsed = urlparse(uri)
    if parsed.scheme != "https" or parsed.netloc != SOURCE_DOMAINS[source_id]:
        raise ValueError(f"{context}.uri is not on the authoritative {source_id} domain")
    if source_id == "DOI" and not parsed.path.lstrip("/").lower() == record_id.lower():
        raise ValueError(f"{context}.uri does not resolve its DOI record_id")
    _require_utc_datetime(value["verified_at"], f"{context}.verified_at")
    _require_nonempty_string(value["verification_note"], f"{context}.verification_note")
    return source_id, record_id, role, applicability


def _validate_case(value: Any, index: int) -> dict[str, Any]:
    context = f"cases[{index}]"
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    _require_exact_keys(
        value,
        {
            "assay_candidate",
            "case_compute_budget",
            "case_id",
            "fingerprint_bridge",
            "known_ambiguities",
            "label",
            "organism",
            "reaction_participant_ids",
            "representation_axis",
            "representation_pressures",
            "required_outputs",
            "selection_rationale",
            "source_handles",
            "stop_conditions",
            "success_condition",
            "target_evidence_tier",
            "target_record_id",
        },
        context,
    )
    case_id = _require_nonempty_string(value["case_id"], f"{context}.case_id")
    if case_id not in CASE_EXPECTATIONS:
        raise ValueError(f"{context}.case_id is outside the frozen Atlas-3 selection")
    expected = CASE_EXPECTATIONS[case_id]
    if value["representation_axis"] != expected["axis"]:
        raise ValueError(f"{context}.representation_axis differs from the frozen selection")
    if value["target_record_id"] != expected["target_record_id"]:
        raise ValueError(f"{context}.target_record_id differs from the frozen selection")
    if value["fingerprint_bridge"] != expected["fingerprint_bridge"]:
        raise ValueError(f"{context}.fingerprint_bridge differs from the frozen selection")
    _require_nonempty_string(value["label"], f"{context}.label")
    _require_nonempty_string(value["organism"], f"{context}.organism")
    _require_nonempty_string(value["selection_rationale"], f"{context}.selection_rationale")
    _require_nonempty_string(value["success_condition"], f"{context}.success_condition")
    if value["target_evidence_tier"] != 2:
        raise ValueError(f"{context}.target_evidence_tier must be 2")
    if not isinstance(value["assay_candidate"], bool):
        raise ValueError(f"{context}.assay_candidate must be boolean")
    pressures = _require_string_list(
        value["representation_pressures"], f"{context}.representation_pressures", minimum=2
    )
    if pressures[0] != expected["axis"]:
        raise ValueError(f"{context}.representation_pressures must lead with its frozen axis")
    outputs = _require_string_list(value["required_outputs"], f"{context}.required_outputs")
    if tuple(outputs) != REQUIRED_OUTPUTS:
        raise ValueError(f"{context}.required_outputs differs from the Atlas-3 exit contract")
    participants = _require_string_list(
        value["reaction_participant_ids"], f"{context}.reaction_participant_ids", minimum=2
    )
    if any(not re.fullmatch(r"CHEBI:\d+", item) for item in participants):
        raise ValueError(f"{context}.reaction_participant_ids must be ChEBI identifiers")
    if set(participants) != expected["reaction_participants"]:
        raise ValueError(f"{context}.reaction_participant_ids differ from the frozen selection")
    _require_string_list(value["known_ambiguities"], f"{context}.known_ambiguities")
    _require_string_list(value["stop_conditions"], f"{context}.stop_conditions", minimum=3)
    _validate_budget(value["case_compute_budget"], f"{context}.case_compute_budget")
    handles = value["source_handles"]
    if not isinstance(handles, list) or not handles:
        raise ValueError(f"{context}.source_handles must be a non-empty list")
    source_keys = {
        _validate_source_handle(handle, f"{context}.source_handles[{handle_index}]")
        for handle_index, handle in enumerate(handles)
    }
    if len(source_keys) != len(handles):
        raise ValueError(f"{context}.source_handles contains duplicates")
    if source_keys != expected["sources"]:
        raise ValueError(f"{context}.source_handles differ from the frozen authoritative set")
    if not any(key[0] == "UniProtKB" and key[3] == "direct" for key in source_keys):
        raise ValueError(f"{context} requires a direct UniProtKB identity")
    if not any(key[0] == "Rhea" and key[3] == "direct" for key in source_keys):
        raise ValueError(f"{context} requires a direct Rhea reaction")
    if not any(key[0] == "PDB" and key[3] == "direct" for key in source_keys):
        raise ValueError(f"{context} requires a direct experimental PDB structure")
    return value


def _validate_assay_lane(value: Any, selected_case_ids: set[str]) -> None:
    if not isinstance(value, dict):
        raise ValueError("assay_lane must be an object")
    _require_exact_keys(
        value,
        {
            "assay_name",
            "candidate_case_id",
            "decision_frozen_before_results",
            "existing_assay_only",
            "external_execution_required",
            "materials_committed",
            "preregistration_required",
            "selection_reason",
            "status",
            "stop_conditions",
        },
        "assay_lane",
    )
    if value["candidate_case_id"] not in selected_case_ids:
        raise ValueError("assay_lane candidate is not one of the selected cases")
    if value["candidate_case_id"] != "atlas3.tem1-ecoli.covalent":
        raise ValueError("the frozen Atlas-3 assay candidate must be TEM-1")
    if value["status"] != "candidate_only_not_started":
        raise ValueError("assay_lane status must remain candidate_only_not_started")
    if value["assay_name"] != "nitrocefin hydrolysis absorbance assay":
        raise ValueError("assay_lane assay differs from the frozen candidate")
    for field in (
        "decision_frozen_before_results",
        "existing_assay_only",
        "external_execution_required",
        "preregistration_required",
    ):
        if value[field] is not True:
            raise ValueError(f"assay_lane.{field} must be true")
    if value["materials_committed"] is not False:
        raise ValueError("assay_lane.materials_committed must remain false at selection")
    _require_nonempty_string(value["selection_reason"], "assay_lane.selection_reason")
    _require_string_list(value["stop_conditions"], "assay_lane.stop_conditions", minimum=3)


def validate_atlas3_selection(value: Any) -> dict[str, int | str]:
    """Validate and summarize the frozen Atlas-3 selection contract."""
    if not isinstance(value, dict):
        raise ValueError("Atlas-3 selection must be an object")
    _require_exact_keys(
        value,
        {
            "assay_lane",
            "baseline_commit",
            "cases",
            "exit_gate",
            "frozen_at",
            "namespace",
            "objective",
            "phase_compute_budget",
            "prohibited_claims",
            "registry_mutation_permitted",
            "schema_version",
            "selection_axes",
            "selection_id",
            "status",
        },
        "selection",
    )
    if value["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported Atlas-3 selection schema: {value['schema_version']!r}")
    if value["status"] != SELECTION_STATUS:
        raise ValueError("Atlas-3 selection is not frozen before compilation")
    _require_nonempty_string(value["selection_id"], "selection_id")
    frozen_at = _require_utc_datetime(value["frozen_at"], "frozen_at")
    _require_nonempty_string(value["objective"], "objective")
    if not isinstance(value["baseline_commit"], str) or not re.fullmatch(
        r"[0-9a-f]{40}", value["baseline_commit"]
    ):
        raise ValueError("baseline_commit must be a full lowercase Git commit")
    if value["namespace"] != "data/atlas/atlas3":
        raise ValueError("Atlas-3 must compile outside protected registries and governance data")
    if value["registry_mutation_permitted"] is not False:
        raise ValueError("Atlas-3 selection cannot authorize protected registry mutation")
    axes = _require_string_list(value["selection_axes"], "selection_axes", minimum=3)
    if tuple(axes) != SELECTION_AXES:
        raise ValueError("selection_axes differ from the frozen pressure set")
    phase_budget = _validate_budget(value["phase_compute_budget"], "phase_compute_budget")
    cases = value["cases"]
    if not isinstance(cases, list) or len(cases) != 3:
        raise ValueError("Atlas-3 requires exactly three selected cases")
    validated_cases = [_validate_case(case, index) for index, case in enumerate(cases)]
    case_ids = [case["case_id"] for case in validated_cases]
    if set(case_ids) != set(CASE_EXPECTATIONS) or len(set(case_ids)) != 3:
        raise ValueError("Atlas-3 case identities differ from the frozen trio")
    if [case["representation_axis"] for case in validated_cases] != list(SELECTION_AXES):
        raise ValueError("Atlas-3 cases must follow the frozen pressure order")
    if any(
        handle["verified_at"] != frozen_at
        for case in validated_cases
        for handle in case["source_handles"]
    ):
        raise ValueError("every frozen source handle must share the selection freeze timestamp")
    if sum(case["assay_candidate"] for case in validated_cases) != 1:
        raise ValueError("Atlas-3 requires exactly one assay candidate")
    for field in ("cpu_hours_max", "download_bytes_max", "external_requests_max"):
        case_total = sum(case["case_compute_budget"][field] for case in validated_cases)
        if case_total > phase_budget[field]:
            raise ValueError(f"case {field} ceilings exceed the phase ceiling")
    _validate_assay_lane(value["assay_lane"], set(case_ids))
    _require_string_list(value["exit_gate"], "exit_gate", minimum=4)
    _require_string_list(value["prohibited_claims"], "prohibited_claims", minimum=4)
    canonical = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    if digest != FROZEN_SELECTION_SHA256:
        raise ValueError("Atlas-3 selection content differs from its frozen canonical digest")
    return {
        "schema_version": SCHEMA_VERSION,
        "status": SELECTION_STATUS,
        "cases": 3,
        "authoritative_source_handles": sum(
            len(case["source_handles"]) for case in validated_cases
        ),
        "assay_candidates": 1,
        "gpu_hours_max": phase_budget["gpu_hours_max"],
        "selection_sha256": digest,
    }


def load_atlas3_selection(path: Path) -> dict[str, Any]:
    """Load a selection contract from JSON and validate it before returning it."""
    value = json.loads(path.read_text(encoding="utf-8"))
    validate_atlas3_selection(value)
    return value
