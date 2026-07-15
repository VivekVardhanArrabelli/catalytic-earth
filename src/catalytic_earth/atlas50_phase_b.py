"""Deterministic Atlas-50 Phase B review and selection-freeze readiness."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .atlas50_phase_a import validate_phase_a_package


PHASE_A_RELATIVE = Path("data/atlas/atlas50/phase_a")
PHASE_B_RELATIVE = Path("data/atlas/atlas50/phase_b")
BASELINE_COMMIT = "375548419e7435efa2bffc89be5e32aa70864875"
TEXT_SUFFIXES = {".json", ".md", ".py", ".sql", ".toml", ".yaml", ".yml"}
PROHIBITED_COMPILED_FIELDS = {
    "atom_map",
    "atom_maps",
    "bond_edit",
    "bond_edits",
    "catalytic_roles",
    "compiled_mechanism",
    "mechanism_steps",
    "site_assignments",
}
REQUIRED_CROSSWALK_SOURCE_KEYS = {
    "cath",
    "chebi",
    "ec",
    "ec_blast",
    "enzymemap",
    "enzymm",
    "ezmechanism",
    "interpro",
    "mcsa",
    "mcsa_arrow_environments",
    "mechfind",
    "pfam",
    "rhea",
}

GENERATED_FILENAMES = (
    "crosswalk_review_queue.json",
    "panel_review_queue.json",
    "review_attempts.json",
    "freeze_candidate.json",
    "source_reacquisition_plan.json",
    "inheritance_proof.json",
    "readiness_report.json",
    "package_manifest.json",
)

SCHEMA_PATHS = (
    "src/catalytic_earth/schemas/atlas50-review-queue-v1.schema.json",
    "src/catalytic_earth/schemas/atlas50-review-submission-v1.schema.json",
    "src/catalytic_earth/schemas/atlas50-freeze-candidate-v1.schema.json",
    "src/catalytic_earth/schemas/atlas50-source-reacquisition-plan-v1.schema.json",
    "src/catalytic_earth/schemas/atlas50-readiness-report-v1.schema.json",
)

SOURCE_LANES = (
    {
        "lane_id": "mcsa_mechanism_and_arrow_environment",
        "source_keys": ["mcsa", "mcsa_arrow_environments"],
        "scientific_question": "What mechanism detail and electron-flow representation does the exact M-CSA entry expose for this case?",
        "cheapest_credible_method": "Retrieve the exact entry and permitted scheme metadata after freeze; hash the response and retain detailed versus non-detailed status.",
        "required_output": "Content-bound entry metadata, detail status, mechanism alternatives, and explicit arrow-environment availability or gap.",
        "stop_condition": "Stop if the entry cannot be bound by an exact identifier, content hash, version boundary, and redistribution rule; never infer missing steps.",
    },
    {
        "lane_id": "rhea_and_chebi_reaction",
        "source_keys": ["rhea", "chebi"],
        "scientific_question": "Is there a directly supported balanced reaction and participant/microspecies mapping for this exact case?",
        "cheapest_credible_method": "Query authoritative Rhea surfaces using the frozen candidate handles, then verify ChEBI participants without promoting query keys to canonical mappings.",
        "required_output": "Direct Rhea record and ChEBI bindings, or a content-bound zero-result/ambiguity gap.",
        "stop_condition": "Stop rather than select a reaction or microspecies when multiple records remain applicable or no direct record is supported.",
    },
    {
        "lane_id": "uniprot_protein",
        "source_keys": ["uniprot"],
        "scientific_question": "Do the source-reported protein handles identify the intended natural protein and evidence-bearing site context?",
        "cheapest_credible_method": "Retrieve exact UniProt entries after freeze and verify sequence, organism, evidence, catalytic annotations, and isoform boundaries.",
        "required_output": "Versioned protein records and explicit applicability/site gaps.",
        "stop_condition": "Stop on isoform, organism, sequence, numbering, or applicability ambiguity.",
    },
    {
        "lane_id": "pdb_and_cath_structure",
        "source_keys": ["pdb", "cath"],
        "scientific_question": "Which exact structures and fold/domain assignments support or limit the case?",
        "cheapest_credible_method": "Retrieve reported PDB/mmCIF and CATH records, then bind author, label, and natural-protein numbering without transfer by fold alone.",
        "required_output": "Content-addressed structure/domain records, numbering crosswalks, and engineered/missing-state warnings.",
        "stop_condition": "Stop if residue identity, construct provenance, ligand/state applicability, or domain assignment cannot be reconciled.",
    },
    {
        "lane_id": "ec_interpro_pfam_function",
        "source_keys": ["ec", "interpro", "pfam"],
        "scientific_question": "What functional and family context is supported without treating EC or family membership as a unique mechanism?",
        "cheapest_credible_method": "Retrieve exact EC, InterPro, and Pfam records for frozen handles and preserve specificity limits.",
        "required_output": "Versioned functional/family context and explicit non-uniqueness/applicability boundaries.",
        "stop_condition": "Stop any mechanism transfer justified only by EC, domain, family, or fold membership.",
    },
    {
        "lane_id": "ec_blast_bond_change",
        "source_keys": ["ec_blast"],
        "scientific_question": "Does an applicable EC-BLAST result provide supported net bond changes for the exact reaction?",
        "cheapest_credible_method": "Run only after a balanced reaction is frozen and record tool/version, inputs, outputs, rights, and failures.",
        "required_output": "Content-bound bond-change result or explicit inapplicability/failure.",
        "stop_condition": "Do not run on an unfrozen or ambiguous reaction and do not reinterpret net edits as mechanism steps.",
    },
    {
        "lane_id": "enzymemap_atom_mapping",
        "source_keys": ["enzymemap"],
        "scientific_question": "Is an applicable EnzymeMap reaction and atom mapping available for the frozen reaction?",
        "cheapest_credible_method": "Match only by supported identifiers/reaction evidence and retain dataset version, mapping provenance, and licensing boundary.",
        "required_output": "Versioned candidate mapping or explicit no-match/ambiguity record.",
        "stop_condition": "Never invent or repair atom maps to force a match.",
    },
    {
        "lane_id": "mechfind_and_ezmechanism_hypotheses",
        "source_keys": ["mechfind", "ezmechanism"],
        "scientific_question": "Which tool-supported hypotheses or rules apply to the frozen inputs, and where do they conflict or abstain?",
        "cheapest_credible_method": "Use reference-only boundaries and exact supported inputs; record tool versions, parameters, outputs, conflicts, and failures.",
        "required_output": "Reference-bound hypothesis identifiers/results or explicit unsupported-input/rights gaps.",
        "stop_condition": "Stop when rights prohibit redistribution or tool applicability/input requirements are unmet; do not call a hypothesis reviewed truth.",
    },
    {
        "lane_id": "enzymm_template",
        "source_keys": ["enzymm"],
        "scientific_question": "Is an applicable EnzyMM template available at the supported granularity?",
        "cheapest_credible_method": "Query documented template surfaces only after reaction and source mechanism identities are frozen.",
        "required_output": "Template identifier/version and applicability boundary, or an explicit gap.",
        "stop_condition": "Do not adapt a template across unsupported chemistry, cofactors, sites, or substrate states.",
    },
    {
        "lane_id": "primary_literature_claims",
        "source_keys": ["primary_literature"],
        "scientific_question": "What primary claims, alternatives, conflicts, and unresolved mechanism details govern this case?",
        "cheapest_credible_method": "Acquire only permitted metadata/full text after freeze, bind claim-level citations, and preserve conflicting interpretations.",
        "required_output": "Claim-level evidence/counterevidence references, rights boundaries, and unresolved alternatives.",
        "stop_condition": "Stop on unavailable permission or inaccessible evidence; never fill the gap from secondary summaries alone.",
    },
)


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _canonical_payload(path: Path) -> bytes:
    payload = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        payload = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return payload


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _json_digest(value: Any) -> str:
    return _sha256(canonical_json_bytes(value))


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _assert_no_compiled_fields(value: Any, context: str) -> None:
    if isinstance(value, dict):
        prohibited = PROHIBITED_COMPILED_FIELDS.intersection(value)
        _require(not prohibited, f"{context} contains prohibited compiled fields: {sorted(prohibited)}")
        for key, item in value.items():
            _assert_no_compiled_fields(item, f"{context}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _assert_no_compiled_fields(item, f"{context}[{index}]")


def validate_review_spec(spec: dict[str, Any]) -> None:
    _require(
        spec.get("schema_version")
        == "catalytic-earth.atlas50-phase-b-review-spec.v1",
        "unsupported Phase B review spec schema",
    )
    _require(spec.get("baseline_commit") == BASELINE_COMMIT, "Phase B baseline changed")
    _require(
        spec.get("status") == "review_readiness_not_review_or_selection_freeze",
        "Phase B spec status changed",
    )
    phase_a = spec.get("phase_a_contract", {})
    _require(
        (phase_a.get("crosswalk_rows"), phase_a.get("candidate_rows")) == (57, 40),
        "Phase A review surface changed",
    )
    _require(
        (phase_a.get("proposed_additions"), phase_a.get("proposed_total"))
        == (37, 47),
        "Phase A proposed panel changed",
    )
    crosswalk = spec.get("crosswalk_review_contract", {})
    _require(crosswalk.get("expected_packet_count") == 57, "crosswalk packet contract changed")
    _require(
        set(crosswalk.get("required_source_keys", []))
        == REQUIRED_CROSSWALK_SOURCE_KEYS,
        "crosswalk source contract changed",
    )
    _require(crosswalk.get("upstream_curation_is_review") is False, "upstream curation promoted to review")
    _require(crosswalk.get("agent_or_builder_output_is_review") is False, "agent output promoted to review")
    panel = spec.get("panel_review_contract", {})
    _require(panel.get("expected_packet_count") == 40, "panel packet contract changed")
    reviewer = spec.get("reviewer_evidence_contract", {})
    _require(
        reviewer.get("section_10_3_independent_annotation_satisfied_by_this_contract")
        is False,
        "Phase B spec promoted readiness to independent annotation",
    )
    submission = spec.get("review_submission_contract", {})
    _require(submission.get("current_submission_count") == 0, "review submissions were invented")
    _require(submission.get("append_only") is True, "review submissions are not append-only")
    freeze = spec.get("selection_freeze_gate", {})
    _require(freeze.get("selection_frozen_by_this_spec") is False, "spec froze selection")
    _require(freeze.get("round_number_completion_permitted") is False, "spec permits forced panel completion")
    source = spec.get("source_reacquisition_contract", {})
    _require(source.get("planned_follow_on_case_count") == 37, "source plan surface changed")
    _require(source.get("may_execute_before_selection_freeze") is False, "pre-freeze acquisition permitted")
    _require(source.get("pre_freeze_external_requests_max") == 0, "pre-freeze requests permitted")
    _require(source.get("gpu_hours_max") == 0, "GPU work introduced")


def validate_job_ledger(ledger: dict[str, Any]) -> None:
    _require(
        ledger.get("schema_version")
        == "catalytic-earth.atlas50-phase-b-job-ledger.v1",
        "unsupported Phase B job ledger schema",
    )
    _require(ledger.get("baseline_commit") == BASELINE_COMMIT, "job ledger baseline changed")
    jobs = ledger.get("jobs", [])
    _require(len(jobs) == 3, "Phase B job ledger count changed")
    _require(
        jobs[0].get("status")
        == "completed_with_review_and_freeze_gates_still_blocked",
        "readiness build completion state changed",
    )
    actual = jobs[0].get("actual_usage", {})
    _require(actual.get("review_packets_generated") == 97, "readiness packet usage changed")
    _require(actual.get("review_submissions") == 0, "readiness job invented reviews")
    _require(actual.get("source_records_acquired") == 0, "readiness job invented sources")
    _require(
        all(str(job.get("status", "")).startswith("blocked_not_started") for job in jobs[1:]),
        "review or acquisition job was started without its gate",
    )
    for job in jobs:
        _require(job.get("budget", {}).get("gpu_hours_max") == 0, "job ledger permits GPU work")
    _require(
        jobs[1]["budget"]["external_messages_max_before_explicit_outreach_approval"]
        == 0,
        "job ledger permits unapproved outreach",
    )
    _require(
        jobs[2]["budget"]["external_requests_max_before_selection_freeze"] == 0,
        "job ledger permits pre-freeze acquisition",
    )


def _git_blob(repo_root: Path, commit: str, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(f"missing baseline Git blob: {commit}:{relative}")
    payload = result.stdout
    if Path(relative).suffix.lower() in TEXT_SUFFIXES:
        payload = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return payload


def _phase_a_paths(repo_root: Path) -> list[str]:
    result = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            BASELINE_COMMIT,
            "--",
            PHASE_A_RELATIVE.as_posix(),
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return sorted(line.strip() for line in result.stdout.splitlines() if line.strip())


def _build_crosswalk_queue(
    crosswalk: dict[str, Any], spec: dict[str, Any]
) -> dict[str, Any]:
    packets = []
    for row in crosswalk["rows"]:
        packets.append(
            {
                "packet_id": f"atlas50.phase-b.crosswalk.{row['fingerprint_id']}",
                "packet_type": "crosswalk",
                "ordinal": row["ordinal"],
                "fingerprint_id": row["fingerprint_id"],
                "fingerprint_name": row["fingerprint_name"],
                "phase_a_row_sha256": _json_digest(row),
                "machine_draft": {
                    "classification": row["classification"],
                    "classification_rationale": row["classification_rationale"],
                    "uncertainty": row["uncertainty"],
                    "source_links": row["source_links"],
                },
                "review_requirements": {
                    "classification_decisions": spec["crosswalk_review_contract"][
                        "permitted_classification_decisions"
                    ],
                    "source_decisions": spec["crosswalk_review_contract"][
                        "permitted_source_decisions"
                    ],
                    "required_source_keys": spec["crosswalk_review_contract"][
                        "required_source_keys"
                    ],
                    "revision_evidence_required": True,
                    "conflicts_and_gaps_must_be_preserved": True,
                },
                "review_state": {
                    "status": "unreviewed",
                    "review_attempted": False,
                    "submission_ids": [],
                    "reviewer_count": 0,
                },
            }
        )
    return {
        "schema_version": "catalytic-earth.atlas50-review-queue.v1",
        "queue_id": "atlas50.phase-b.crosswalk-review-queue.2026-07-14",
        "queue_type": "crosswalk",
        "status": "ready_for_real_review_no_review_attempted",
        "baseline_commit": BASELINE_COMMIT,
        "phase_a_source": {
            "path": f"{PHASE_A_RELATIVE.as_posix()}/crosswalk_draft.json",
            "sha256": _json_digest(crosswalk),
        },
        "packet_count": len(packets),
        "reviewed_packet_count": 0,
        "review_attempted": False,
        "independent_review_claimed": False,
        "submission_schema": spec["review_submission_contract"]["schema_path"],
        "packets": packets,
        "claim_boundary": [
            "These packets reproduce machine-draft content for inspection; they are not reviewed rows.",
            "Every review state remains unreviewed until an attributable submission is added separately.",
        ],
    }


def _build_panel_queue(
    matrix: dict[str, Any], blockers: dict[str, Any], spec: dict[str, Any]
) -> dict[str, Any]:
    blocker_by_id = {item["blocker_id"]: item for item in blockers["blockers"]}
    packets = []
    for row in matrix["rows"]:
        blocker_id = row["gates"]["representation"].get("blocker_id")
        packets.append(
            {
                "packet_id": f"atlas50.phase-b.panel.{row['candidate_id']}",
                "packet_type": "panel",
                "ordinal": row["ordinal"],
                "candidate_id": row["candidate_id"],
                "label": row["label"],
                "phase_a_row_sha256": _json_digest(row),
                "machine_draft": {
                    "proposed_disposition": row["decision"],
                    "inclusion_reasons": row["inclusion_reasons"],
                    "exclusion_reasons": row["exclusion_reasons"],
                    "gates": row["gates"],
                    "source_identity": row["source_identity"],
                    "source_availability": row["source_availability"],
                    "licensing": row["licensing"],
                    "representation_pressures": row["representation_pressures"],
                    "expected_object_tiers": row["expected_object_tiers"],
                    "uncertainties": row["uncertainties"],
                    "stop_conditions": row["stop_conditions"],
                    "representation_blocker": (
                        blocker_by_id[blocker_id] if blocker_id else None
                    ),
                },
                "review_requirements": {
                    "disposition_decisions": spec["panel_review_contract"][
                        "permitted_disposition_decisions"
                    ],
                    "review_dimensions": spec["panel_review_contract"][
                        "review_dimensions"
                    ],
                    "revision_evidence_required": True,
                    "family_specific_fields_permitted": False,
                    "mechanism_compilation_permitted": False,
                },
                "review_state": {
                    "status": "unreviewed",
                    "review_attempted": False,
                    "submission_ids": [],
                    "reviewer_count": 0,
                },
            }
        )
    return {
        "schema_version": "catalytic-earth.atlas50-review-queue.v1",
        "queue_id": "atlas50.phase-b.panel-review-queue.2026-07-14",
        "queue_type": "panel",
        "status": "ready_for_real_review_no_review_attempted",
        "baseline_commit": BASELINE_COMMIT,
        "phase_a_source": {
            "path": f"{PHASE_A_RELATIVE.as_posix()}/candidate_matrix.json",
            "sha256": _json_digest(matrix),
        },
        "packet_count": len(packets),
        "reviewed_packet_count": 0,
        "review_attempted": False,
        "independent_review_claimed": False,
        "submission_schema": spec["review_submission_contract"]["schema_path"],
        "packets": packets,
        "claim_boundary": [
            "The proposed dispositions are Phase A machine-draft gate outcomes, not reviewed selection decisions.",
            "Unresolved or unsupported rows must fail closed at a later freeze rather than being forced into the panel.",
        ],
    }


def _build_review_attempts(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "catalytic-earth.atlas50-review-attempts.v1",
        "ledger_id": "atlas50.phase-b.review-attempts.2026-07-14",
        "status": "no_review_or_outreach_attempted",
        "baseline_commit": BASELINE_COMMIT,
        "submission_directory": spec["review_submission_contract"][
            "submission_directory"
        ],
        "attempts": [],
        "attempt_count": 0,
        "submission_count": 0,
        "identified_reviewer_count": 0,
        "external_messages_sent": 0,
        "review_claimed": False,
        "independent_annotation_claimed": False,
        "claim_boundary": [
            "Packet preparation is not outreach or review.",
            "No reviewer has been contacted, agreed, submitted a decision, or been counted as independent.",
        ],
    }


def _build_freeze_candidate(
    proposal: dict[str, Any], blockers: dict[str, Any]
) -> dict[str, Any]:
    gate_outcomes = {
        "phase_a_and_protected_inheritance_unchanged": "pass",
        "all_57_crosswalk_packets_reviewed": "blocked_no_submissions",
        "all_40_panel_packets_reviewed": "blocked_no_submissions",
        "revisions_conflicts_and_unresolved_fields_preserved": "blocked_no_submissions",
        "generic_contract_dispositions_reviewed": "blocked_no_reviewed_dispositions",
        "post_freeze_source_budget_approved": "blocked_budget_unset",
        "explicit_selection_freeze_approval_recorded": "blocked_no_approval_artifact",
    }
    blocker_dispositions = [
        {
            "blocker_id": row["blocker_id"],
            "candidate_id": row["candidate_id"],
            "mcsa_id": row["mcsa_id"],
            "current_disposition": "remain_excluded_pending_reviewed_generic_contract_disposition",
            "reviewed": False,
            "generic_contract_validated": False,
            "convenience_choice_made": False,
        }
        for row in blockers["blockers"]
    ]
    return {
        "schema_version": "catalytic-earth.atlas50-freeze-candidate.v1",
        "candidate_id": "atlas50.phase-b.selection-freeze-candidate.2026-07-14",
        "status": "unfrozen_blocked_pending_real_review_budget_and_approval",
        "baseline_commit": BASELINE_COMMIT,
        "selection_frozen": False,
        "phase_a_proposal": {
            "path": f"{PHASE_A_RELATIVE.as_posix()}/proposed_panel.json",
            "sha256": _json_digest(proposal),
        },
        "candidate_panel": proposal["proposed_panel"],
        "inherited_atlas10": proposal["inherited_atlas10"],
        "representation_projection": proposal["representation_projection"],
        "review_state": {
            "crosswalk_packets": 57,
            "crosswalk_reviewed": 0,
            "panel_packets": 40,
            "panel_reviewed": 0,
            "review_attempts": 0,
            "review_submissions": 0,
            "independent_annotation_claimed": False,
        },
        "blocker_dispositions": blocker_dispositions,
        "freeze_gate": {
            "ready": False,
            "outcomes": gate_outcomes,
            "blocked_condition_count": sum(
                outcome != "pass" for outcome in gate_outcomes.values()
            ),
        },
        "compiled_follow_on_mechanisms": 0,
        "gpu_hours": 0,
        "claim_boundary": [
            "This is an exact unfrozen candidate inherited from Phase A, not an Atlas-50 selection.",
            "The 47-of-50 value remains a precompilation projection and not the final Section 10.2 result.",
            "No review, agreement, source reacquisition, mechanism compilation, or independent annotation is claimed.",
        ],
    }


def _build_source_plan(
    matrix: dict[str, Any], source_catalog: dict[str, Any]
) -> dict[str, Any]:
    included = [row for row in matrix["rows"] if row["decision"] == "propose_include"]
    resource_by_key = {
        resource["source_key"]: resource for resource in source_catalog["resources"]
    }
    lanes = []
    for lane in SOURCE_LANES:
        boundaries = []
        for key in lane["source_keys"]:
            resource = resource_by_key.get(key)
            if resource:
                boundaries.append(
                    {
                        "source_key": key,
                        "rights": resource["rights"],
                        "redistribution_boundary": resource["redistribution_boundary"],
                    }
                )
            else:
                boundaries.append(
                    {
                        "source_key": key,
                        "rights": "not_recorded_in_phase_a_catalog",
                        "redistribution_boundary": "Do not acquire or redistribute until rights and provenance are recorded.",
                    }
                )
        lanes.append({**lane, "rights_boundaries": boundaries})
    cases = []
    for row in included:
        cases.append(
            {
                "candidate_id": row["candidate_id"],
                "label": row["label"],
                "mcsa_id": row["source_identity"]["mcsa_id"],
                "source_identity": row["source_identity"],
                "source_availability": row["source_availability"],
                "required_lane_ids": [lane["lane_id"] for lane in SOURCE_LANES],
                "mandatory_abstentions": row["expected_object_tiers"][
                    "mandatory_abstentions"
                ],
                "phase_a_uncertainties": row["uncertainties"],
                "status": "not_started_pending_reviewed_selection_freeze",
                "acquisitions": [],
                "executed_external_requests": 0,
                "downloaded_bytes": 0,
                "gpu_hours": 0,
                "post_freeze_budget": None,
                "stop_conditions": row["stop_conditions"],
            }
        )
    return {
        "schema_version": "catalytic-earth.atlas50-source-reacquisition-plan.v1",
        "plan_id": "atlas50.phase-b.post-freeze-source-reacquisition.2026-07-14",
        "status": "planned_not_authorized_pending_reviewed_selection_freeze_and_budget",
        "baseline_commit": BASELINE_COMMIT,
        "may_execute": False,
        "selection_frozen": False,
        "planned_case_count": len(cases),
        "shared_lane_count": len(lanes),
        "shared_lanes": lanes,
        "cases": cases,
        "budget": {
            "pre_freeze_external_requests_max": 0,
            "pre_freeze_download_mib_max": 0,
            "post_freeze_cpu_hours_max": None,
            "post_freeze_external_requests_max": None,
            "post_freeze_download_mib_max": None,
            "gpu_hours_max": 0,
            "post_freeze_budget_status": "unset_requires_explicit_freeze_approval",
        },
        "actual_usage": {
            "external_requests": 0,
            "downloaded_bytes": 0,
            "cpu_hours": 0,
            "gpu_hours": 0,
            "source_records_acquired": 0,
        },
        "claim_boundary": [
            "This artifact is a source plan, not a source manifest.",
            "No source record has been reacquired or verified in Phase B readiness work.",
            "A source gap remains a gap and cannot be filled by a query key, family transfer, or invented identifier.",
        ],
    }


def _build_inheritance_proof(repo_root: Path) -> dict[str, Any]:
    files = []
    for relative in _phase_a_paths(repo_root):
        baseline_payload = _git_blob(repo_root, BASELINE_COMMIT, relative)
        current_payload = _canonical_payload(repo_root / relative)
        _require(
            current_payload == baseline_payload,
            f"Phase A file changed after merge baseline: {relative}",
        )
        files.append(
            {
                "path": relative,
                "bytes": len(baseline_payload),
                "sha256": _sha256(baseline_payload),
                "unchanged": True,
            }
        )
    phase_a_summary = validate_phase_a_package(repo_root)
    return {
        "schema_version": "catalytic-earth.atlas50-phase-b-inheritance-proof.v1",
        "proof_id": "atlas50.phase-b.inheritance.2026-07-14",
        "baseline_commit": BASELINE_COMMIT,
        "phase_a_path": PHASE_A_RELATIVE.as_posix(),
        "phase_a_file_count": len(files),
        "phase_a_files": files,
        "phase_a_validation": phase_a_summary,
        "phase_a_unchanged": True,
        "atlas3_atlas10_and_protected_registries_unchanged": True,
    }


def _build_readiness_report(
    crosswalk_queue: dict[str, Any],
    panel_queue: dict[str, Any],
    attempts: dict[str, Any],
    freeze_candidate: dict[str, Any],
    source_plan: dict[str, Any],
) -> dict[str, Any]:
    blockers = [
        {
            "blocker_id": "atlas50.phase-b.real-crosswalk-review",
            "missing": 57 - crosswalk_queue["reviewed_packet_count"],
            "required_evidence": "Attributable valid review submissions for every crosswalk packet.",
        },
        {
            "blocker_id": "atlas50.phase-b.real-panel-review",
            "missing": 40 - panel_queue["reviewed_packet_count"],
            "required_evidence": "Attributable valid review submissions for every panel packet.",
        },
        {
            "blocker_id": "atlas50.phase-b.reviewer-and-outreach-authority",
            "missing": 1,
            "required_evidence": "Explicit authority and identified reviewer context before any external message or claimed attempt.",
        },
        {
            "blocker_id": "atlas50.phase-b.post-freeze-source-budget",
            "missing": 1,
            "required_evidence": "A bounded approved post-freeze CPU/request/download budget.",
        },
        {
            "blocker_id": "atlas50.phase-b.selection-freeze-approval",
            "missing": 1,
            "required_evidence": "An explicit approval artifact after all review and fail-closed dispositions are incorporated.",
        },
    ]
    return {
        "schema_version": "catalytic-earth.atlas50-readiness-report.v1",
        "report_id": "atlas50.phase-b.review-freeze-readiness.2026-07-14",
        "status": "ready_for_review_blocked_for_selection_freeze",
        "baseline_commit": BASELINE_COMMIT,
        "queues": {
            "crosswalk_packets": crosswalk_queue["packet_count"],
            "crosswalk_reviewed": crosswalk_queue["reviewed_packet_count"],
            "panel_packets": panel_queue["packet_count"],
            "panel_reviewed": panel_queue["reviewed_packet_count"],
        },
        "review_activity": {
            "attempts": attempts["attempt_count"],
            "submissions": attempts["submission_count"],
            "identified_reviewers": attempts["identified_reviewer_count"],
            "external_messages_sent": attempts["external_messages_sent"],
        },
        "freeze_candidate": {
            "proposed_total": freeze_candidate["candidate_panel"]["total_case_count"],
            "shortfall_from_50": freeze_candidate["candidate_panel"][
                "shortfall_from_50"
            ],
            "selection_frozen": freeze_candidate["selection_frozen"],
            "freeze_ready": freeze_candidate["freeze_gate"]["ready"],
            "blocked_gate_conditions": freeze_candidate["freeze_gate"][
                "blocked_condition_count"
            ],
        },
        "source_reacquisition": {
            "planned_cases": source_plan["planned_case_count"],
            "planned_lanes": source_plan["shared_lane_count"],
            "may_execute": source_plan["may_execute"],
            "records_acquired": source_plan["actual_usage"][
                "source_records_acquired"
            ],
        },
        "open_blocker_count": len(blockers),
        "blockers": blockers,
        "next_action_boundary": "Obtain explicit reviewer/outreach authority and attributable submissions; do not freeze selection or execute source acquisition before all gates and a bounded budget are satisfied.",
        "compiled_follow_on_mechanisms": 0,
        "gpu_hours": 0,
        "claims_not_supported": [
            "review completion",
            "expert agreement",
            "independent annotation",
            "selection freeze",
            "source reacquisition",
            "mechanism compilation",
            "accuracy, speedup, discovery, assay, design-readiness, or atlas coverage",
        ],
    }


def _build_package_manifest(
    repo_root: Path, outputs: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    artifacts = []
    static_paths = [
        f"{PHASE_B_RELATIVE.as_posix()}/job_ledger.json",
        f"{PHASE_B_RELATIVE.as_posix()}/review_spec.json",
        *SCHEMA_PATHS,
    ]
    for relative in static_paths:
        payload = _canonical_payload(repo_root / relative)
        artifacts.append(
            {
                "path": relative,
                "role": "input_or_contract",
                "bytes": len(payload),
                "sha256": _sha256(payload),
            }
        )
    for filename, value in outputs.items():
        payload = canonical_json_bytes(value)
        artifacts.append(
            {
                "path": f"{PHASE_B_RELATIVE.as_posix()}/{filename}",
                "role": "deterministic_generated_output",
                "bytes": len(payload),
                "sha256": _sha256(payload),
            }
        )
    return {
        "schema_version": "catalytic-earth.atlas50-phase-b-package-manifest.v1",
        "package_id": "atlas50.phase-b.review-freeze-readiness.2026-07-14",
        "status": "deterministic_review_readiness_not_review_or_freeze",
        "baseline_commit": BASELINE_COMMIT,
        "self_hash_excluded": True,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "governance": {
            "crosswalk_packets": 57,
            "panel_packets": 40,
            "review_attempts": 0,
            "review_submissions": 0,
            "selection_frozen": False,
            "proposed_total": 47,
            "planned_source_cases": 37,
            "source_records_acquired": 0,
            "compiled_follow_on_mechanisms": 0,
            "gpu_hours": 0,
        },
    }


def build_phase_b_outputs(repo_root: Path) -> dict[str, dict[str, Any]]:
    phase_a = repo_root / PHASE_A_RELATIVE
    phase_b = repo_root / PHASE_B_RELATIVE
    spec = _load_json(phase_b / "review_spec.json")
    crosswalk = _load_json(phase_a / "crosswalk_draft.json")
    matrix = _load_json(phase_a / "candidate_matrix.json")
    proposal = _load_json(phase_a / "proposed_panel.json")
    blockers = _load_json(phase_a / "blocker_report.json")
    source_catalog = _load_json(phase_a / "source_catalog.json")
    ledger = _load_json(phase_b / "job_ledger.json")

    validate_review_spec(spec)
    validate_job_ledger(ledger)

    crosswalk_queue = _build_crosswalk_queue(crosswalk, spec)
    panel_queue = _build_panel_queue(matrix, blockers, spec)
    attempts = _build_review_attempts(spec)
    freeze_candidate = _build_freeze_candidate(proposal, blockers)
    source_plan = _build_source_plan(matrix, source_catalog)
    inheritance = _build_inheritance_proof(repo_root)
    readiness = _build_readiness_report(
        crosswalk_queue, panel_queue, attempts, freeze_candidate, source_plan
    )
    outputs = {
        "crosswalk_review_queue.json": crosswalk_queue,
        "panel_review_queue.json": panel_queue,
        "review_attempts.json": attempts,
        "freeze_candidate.json": freeze_candidate,
        "source_reacquisition_plan.json": source_plan,
        "inheritance_proof.json": inheritance,
        "readiness_report.json": readiness,
    }
    outputs["package_manifest.json"] = _build_package_manifest(repo_root, outputs)
    return outputs


def validate_review_queue(
    queue: dict[str, Any], phase_a_rows: list[dict[str, Any]], queue_type: str
) -> None:
    _require(
        queue.get("schema_version") == "catalytic-earth.atlas50-review-queue.v1",
        "unsupported review queue schema",
    )
    _require(queue.get("queue_type") == queue_type, "review queue type changed")
    _assert_no_compiled_fields(queue, f"{queue_type} review queue")
    expected_count = 57 if queue_type == "crosswalk" else 40
    _require(queue.get("packet_count") == expected_count, "review packet count changed")
    _require(len(queue.get("packets", [])) == expected_count, "review packets missing")
    _require(queue.get("reviewed_packet_count") == 0, "review was claimed without submissions")
    _require(queue.get("review_attempted") is False, "review attempt was invented")
    _require(
        queue.get("independent_review_claimed") is False,
        "independent review was invented",
    )
    seen = []
    for packet, row in zip(queue["packets"], phase_a_rows, strict=True):
        state = packet.get("review_state", {})
        _require(state.get("status") == "unreviewed", "packet review status was upgraded")
        _require(state.get("review_attempted") is False, "packet review attempt was invented")
        _require(state.get("submission_ids") == [], "packet has invented submissions")
        _require(state.get("reviewer_count") == 0, "packet has invented reviewers")
        _require(packet.get("phase_a_row_sha256") == _json_digest(row), "packet drifted from Phase A")
        if queue_type == "crosswalk":
            _require(packet.get("fingerprint_id") == row["fingerprint_id"], "crosswalk packet order changed")
            _require(packet["machine_draft"]["source_links"] == row["source_links"], "crosswalk source links changed")
            _require(len(packet["machine_draft"]["source_links"]) == 13, "crosswalk source decisions incomplete")
            seen.append(packet["fingerprint_id"])
        else:
            _require(packet.get("candidate_id") == row["candidate_id"], "panel packet order changed")
            _require(packet["machine_draft"]["proposed_disposition"] == row["decision"], "panel disposition changed")
            _require(packet["review_requirements"]["mechanism_compilation_permitted"] is False, "panel packet permits compilation")
            seen.append(packet["candidate_id"])
    expected_ids = [
        row["fingerprint_id"] if queue_type == "crosswalk" else row["candidate_id"]
        for row in phase_a_rows
    ]
    _require(seen == expected_ids, "review queue identifiers changed")


def validate_review_submission(
    value: dict[str, Any], packet: dict[str, Any], spec: dict[str, Any]
) -> None:
    _require(
        value.get("schema_version")
        == "catalytic-earth.atlas50-review-submission.v1",
        "unsupported review submission schema",
    )
    _require(value.get("packet_id") == packet["packet_id"], "submission packet id changed")
    _require(bool(value.get("submission_id")), "submission id missing")
    _require(bool(value.get("submitted_at")), "submission timestamp missing")
    _require(value.get("packet_type") == packet["packet_type"], "submission packet type changed")
    _require(value.get("packet_sha256") == _json_digest(packet), "submission packet hash changed")
    reviewer = value.get("reviewer", {})
    for field in spec["reviewer_evidence_contract"]["required_identity_fields"]:
        _require(bool(reviewer.get(field)), f"submission reviewer field missing: {field}")
    _require("project_author" in reviewer, "submission project-author flag missing")
    _require(
        value.get("attestation")
        == spec["reviewer_evidence_contract"]["required_attestation"],
        "review attestation changed",
    )
    _require(
        value.get("independent_annotation_claimed") is False,
        "Phase B submission cannot claim Section 10.3 independent annotation",
    )
    decision = value.get("decision", {})
    field_decisions = decision.get("field_decisions", {})
    if packet["packet_type"] == "crosswalk":
        permitted_outcomes = set(
            spec["crosswalk_review_contract"]["permitted_classification_decisions"]
        )
        _require(decision.get("outcome") in permitted_outcomes, "invalid crosswalk review outcome")
        _require(
            set(field_decisions) == {"classification", "source_links"},
            "crosswalk review field decisions incomplete",
        )
        _require(
            field_decisions["classification"] in permitted_outcomes,
            "invalid classification decision",
        )
        source_decisions = field_decisions["source_links"]
        _require(
            set(source_decisions)
            == set(spec["crosswalk_review_contract"]["required_source_keys"]),
            "crosswalk source decisions must cover all thirteen source families",
        )
        permitted_source = set(
            spec["crosswalk_review_contract"]["permitted_source_decisions"]
        )
        _require(
            set(source_decisions.values()) <= permitted_source,
            "invalid crosswalk source decision",
        )
        revision_present = decision.get("outcome") == "revise_classification" or any(
            item in {"reject_candidate_mapping", "replace_with_supported_mapping"}
            for item in source_decisions.values()
        )
    else:
        permitted_outcomes = set(
            spec["panel_review_contract"]["permitted_disposition_decisions"]
        )
        _require(decision.get("outcome") in permitted_outcomes, "invalid panel review outcome")
        _require(
            set(field_decisions)
            == set(spec["panel_review_contract"]["review_dimensions"]),
            "panel review field decisions incomplete",
        )
        permitted_dimensions = set(
            spec["panel_review_contract"]["permitted_dimension_decisions"]
        )
        _require(
            set(field_decisions.values()) <= permitted_dimensions,
            "invalid panel dimension decision",
        )
        revision_present = decision.get("outcome") == "revise_with_evidence" or any(
            item == "revise_with_evidence" for item in field_decisions.values()
        )
    _require(bool(decision.get("rationale")), "review rationale missing")
    _require(isinstance(decision.get("uncertainty"), list), "review uncertainty missing")
    _require(isinstance(value.get("conflicts"), list), "review conflicts missing")
    evidence = value.get("evidence_references")
    _require(isinstance(evidence, list), "review evidence references missing")
    if revision_present:
        _require(bool(evidence), "review revisions require evidence references")


def validate_freeze_candidate(value: dict[str, Any], proposal: dict[str, Any]) -> None:
    _require(
        value.get("schema_version") == "catalytic-earth.atlas50-freeze-candidate.v1",
        "unsupported freeze candidate schema",
    )
    _require(value.get("selection_frozen") is False, "selection was frozen without review")
    _require(value.get("candidate_panel") == proposal["proposed_panel"], "candidate panel drifted from Phase A")
    _require(value["candidate_panel"]["total_case_count"] == 47, "candidate total changed")
    _require(value["candidate_panel"]["shortfall_from_50"] == 3, "shortfall changed")
    _require(value["freeze_gate"]["ready"] is False, "freeze gate passed without review")
    _require(value["freeze_gate"]["blocked_condition_count"] == 6, "freeze blockers changed")
    _require(value["review_state"]["crosswalk_reviewed"] == 0, "crosswalk review invented")
    _require(value["review_state"]["panel_reviewed"] == 0, "panel review invented")
    _require(value["review_state"]["independent_annotation_claimed"] is False, "independent annotation invented")
    _require(len(value["blocker_dispositions"]) == 3, "representation blockers changed")
    for row in value["blocker_dispositions"]:
        _require(row["reviewed"] is False, "blocker disposition was called reviewed")
        _require(row["generic_contract_validated"] is False, "generic contract was invented")
        _require(row["convenience_choice_made"] is False, "blocker was resolved for convenience")
    _require(value["compiled_follow_on_mechanisms"] == 0, "mechanisms were compiled")
    _require(value["gpu_hours"] == 0, "GPU use was introduced")


def validate_source_plan(value: dict[str, Any], matrix: dict[str, Any]) -> None:
    _require(
        value.get("schema_version") == "catalytic-earth.atlas50-source-reacquisition-plan.v1",
        "unsupported source plan schema",
    )
    included = [row for row in matrix["rows"] if row["decision"] == "propose_include"]
    _require(value.get("planned_case_count") == 37, "source plan case count changed")
    _require(value.get("shared_lane_count") == 10, "source lane count changed")
    _require(value.get("may_execute") is False, "source plan was authorized before freeze")
    _require(value.get("selection_frozen") is False, "source plan claims a frozen selection")
    _require(
        [row["candidate_id"] for row in value["cases"]]
        == [row["candidate_id"] for row in included],
        "source plan cases changed",
    )
    _require(value["budget"]["pre_freeze_external_requests_max"] == 0, "pre-freeze requests permitted")
    _require(value["budget"]["post_freeze_external_requests_max"] is None, "post-freeze budget invented")
    _require(set(value["actual_usage"].values()) == {0}, "source acquisition usage was invented")
    for case in value["cases"]:
        _require(case["acquisitions"] == [], "case contains invented acquisitions")
        _require(case["post_freeze_budget"] is None, "case budget was invented")
        _require(case["gpu_hours"] == 0, "case contains GPU use")


def validate_phase_b_package(repo_root: Path) -> dict[str, Any]:
    phase_a_summary = validate_phase_a_package(repo_root)
    outputs = build_phase_b_outputs(repo_root)
    phase_b = repo_root / PHASE_B_RELATIVE
    for filename, expected in outputs.items():
        path = phase_b / filename
        _require(path.is_file(), f"missing Phase B artifact: {filename}")
        _require(path.read_bytes() == canonical_json_bytes(expected), f"stale Phase B artifact: {filename}")

    crosswalk = _load_json(repo_root / PHASE_A_RELATIVE / "crosswalk_draft.json")
    matrix = _load_json(repo_root / PHASE_A_RELATIVE / "candidate_matrix.json")
    proposal = _load_json(repo_root / PHASE_A_RELATIVE / "proposed_panel.json")
    crosswalk_queue = outputs["crosswalk_review_queue.json"]
    panel_queue = outputs["panel_review_queue.json"]
    attempts = outputs["review_attempts.json"]
    freeze_candidate = outputs["freeze_candidate.json"]
    source_plan = outputs["source_reacquisition_plan.json"]
    readiness = outputs["readiness_report.json"]
    spec = _load_json(phase_b / "review_spec.json")
    ledger = _load_json(phase_b / "job_ledger.json")

    validate_review_spec(spec)
    validate_job_ledger(ledger)
    validate_review_queue(crosswalk_queue, crosswalk["rows"], "crosswalk")
    validate_review_queue(panel_queue, matrix["rows"], "panel")
    validate_freeze_candidate(freeze_candidate, proposal)
    validate_source_plan(source_plan, matrix)
    _require(attempts["attempt_count"] == 0, "review attempt was invented")
    _require(attempts["external_messages_sent"] == 0, "outreach was invented")
    _require(readiness["open_blocker_count"] == 5, "readiness blocker count changed")
    _require(readiness["freeze_candidate"]["selection_frozen"] is False, "readiness claims freeze")
    _require(outputs["inheritance_proof.json"]["phase_a_unchanged"] is True, "Phase A changed")
    _require(outputs["package_manifest.json"]["artifact_count"] == 14, "package artifact count changed")
    return {
        "crosswalk_packets": 57,
        "crosswalk_reviewed": 0,
        "panel_packets": 40,
        "panel_reviewed": 0,
        "review_attempts": 0,
        "selection_frozen": False,
        "proposed_total": 47,
        "planned_source_cases": 37,
        "source_records_acquired": 0,
        "compiled_follow_on_mechanisms": 0,
        "gpu_hours": 0,
        "phase_a_crosswalk_rows": phase_a_summary["crosswalk_rows"],
    }


__all__ = [
    "BASELINE_COMMIT",
    "GENERATED_FILENAMES",
    "PHASE_B_RELATIVE",
    "build_phase_b_outputs",
    "canonical_json_bytes",
    "validate_freeze_candidate",
    "validate_phase_b_package",
    "validate_job_ledger",
    "validate_review_queue",
    "validate_review_spec",
    "validate_review_submission",
    "validate_source_plan",
]
