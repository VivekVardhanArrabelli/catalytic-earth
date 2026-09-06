"""Reviewed curated-reaction correspondence for source-scoped Atlas drafts.

The sidecar joins one source record and one declared proposal direction to a
curated directed reaction.  It does not promote the source record to a
canonical reaction, assign curated identities to source depictions, or add an
atom map, bond edits, a step trajectory, reverse steps, or residue roles.

Runtime validation checks the complete reviewed declaration and its manual
payload pin.  When ``repo_root`` is supplied, the same validator also checks
the retained Rhea, UniProt, M-CSA, project-projection, and computational-audit
bytes that support that declaration.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .atlas_drafts import validate_source_drafts
from .canonical_hash import canonical_file_sha256


REACTION_CORRESPONDENCE_SCHEMA_VERSION = (
    "catalytic-earth.atlas-reaction-correspondence.v1"
)
REACTION_CORRESPONDENCE_PROJECTION_SCHEMA_VERSION = (
    "catalytic-earth.reaction-correspondence-projection.v1"
)
REACTION_CORRESPONDENCE_STATUS = (
    "reviewed_curated_reaction_correspondence_not_mechanism_expansion"
)
REACTION_CORRESPONDENCE_REVIEWER_KIND = "same_model_computational_agents"
REACTION_CORRESPONDENCE_REVIEW_UPDATE_RULE = (
    "Do not automatically refresh this pin after reaction-correspondence changes. "
    "Repeat source-to-annotation review first."
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MCSA_RE = re.compile(r"^M[0-9]{4}$")
_RHEA_RE = re.compile(r"^RHEA:[1-9][0-9]*$")
_CHEBI_RE = re.compile(r"^CHEBI:[1-9][0-9]*$")
_BATCH_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

_TOP_LEVEL_FIELDS = {
    "schema_version",
    "annotation_set_id",
    "batch_id",
    "status",
    "source_bindings",
    "annotations",
    "review",
}
_SOURCE_BINDING_FIELDS = {"binding_id", "artifact_kind", "path", "sha256"}
_ANNOTATION_FIELDS = {
    "annotation_id",
    "annotation_kind",
    "record_binding",
    "proposal_binding",
    "projection_binding",
    "curated_reaction",
    "source_direction",
    "terminal_depiction",
    "atom_correspondence",
    "required_abstentions",
    "limitations",
    "scope_effect",
    "projection_excerpt",
}
_REVIEW_FIELDS = {
    "reviewed_on",
    "annotation_payload_sha256",
    "update_rule",
    "reviewer_kind",
    "same_model_agents",
    "blind_review",
    "statistically_independent",
    "correlated_error_risk",
    "human_reviewers",
    "domain_expert_review_claimed",
}
_SCOPE_EFFECT_FIELDS = {
    "record_evidence_tier_changed",
    "allowed_operations_changed",
    "source_record_canonical_reaction_promoted",
    "rhea_cross_reference_grounds_proposal",
    "rhea_cross_reference_grounds_step",
    "exact_reaction_instance_claimed",
    "atom_correspondence_added",
    "bond_edits_added",
    "source_step_trajectory_validated",
    "reverse_direction_steps_instantiated",
    "direction_specific_roles_validated",
    "depicted_species_normalized",
}
_REQUIRED_ABSTENTIONS = {
    "atom_correspondence",
    "step_to_canonical_reaction_atom_binding",
    "terminal_product_identity",
    "endpoint_microspecies_equivalence",
    "depiction_to_curated_identity",
    "all_panel_trajectory",
    "reverse_direction_step_instantiation",
    "direction_specific_role_assignment",
}
_ARTIFACT_KINDS = {
    "source_record_snapshot",
    "curated_protein_record",
    "official_reaction_query",
    "official_reaction_direction_map",
    "official_reaction_cross_reference_map",
    "official_reaction_rdf_query",
    "official_participant_structure",
    "computational_depiction_audit",
    "computational_depiction_audit_script",
    "project_reaction_projection",
    "acquisition_receipt_ledger",
    "source_inventory",
    "attribution",
}
_REQUIRED_SINGLE_ARTIFACT_KINDS = {
    "source_record_snapshot",
    "curated_protein_record",
    "official_reaction_query",
    "official_reaction_direction_map",
    "official_reaction_cross_reference_map",
    "official_reaction_rdf_query",
    "computational_depiction_audit",
    "computational_depiction_audit_script",
    "acquisition_receipt_ledger",
    "project_reaction_projection",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, context: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{context} must be an object")
    return value


def _exact(value: Any, fields: set[str], context: str) -> dict[str, Any]:
    result = _object(value, context)
    actual = set(result)
    _require(
        actual == fields,
        f"{context} fields differ; missing={sorted(fields - actual)}, "
        f"extra={sorted(actual - fields)}",
    )
    return result


def _string(value: Any, context: str) -> str:
    _require(
        isinstance(value, str) and bool(value.strip()),
        f"{context} must be nonempty text",
    )
    return value


def _sha256(value: Any, context: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{context} must be a lowercase SHA-256",
    )
    return value


def _positive_int(value: Any, context: str) -> int:
    _require(type(value) is int and value > 0, f"{context} must be a positive integer")
    return value


def _strings(value: Any, context: str, *, minimum: int = 0) -> list[str]:
    _require(isinstance(value, list), f"{context} must be an array")
    _require(len(value) >= minimum, f"{context} is incomplete")
    _require(
        all(isinstance(item, str) and bool(item.strip()) for item in value),
        f"{context} must contain nonempty strings",
    )
    _require(len(value) == len(set(value)), f"{context} contains duplicates")
    return value


def canonical_reaction_correspondence_payload_sha256(value: dict[str, Any]) -> str:
    """Hash every sidecar field except the manually maintained review block."""

    _require(isinstance(value, dict), "reaction-correspondence sidecar must be an object")
    payload = {key: item for key, item in value.items() if key != "review"}
    try:
        raw = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("reaction-correspondence payload must be canonical JSON") from exc
    return hashlib.sha256(raw).hexdigest()


def _validate_review(value: Any, payload_sha256: str) -> dict[str, Any]:
    review = _exact(value, _REVIEW_FIELDS, "review")
    _require(
        isinstance(review["reviewed_on"], str)
        and _DATE_RE.fullmatch(review["reviewed_on"]) is not None,
        "review.reviewed_on must be an ISO date",
    )
    _require(
        _sha256(review["annotation_payload_sha256"], "review.annotation_payload_sha256")
        == payload_sha256,
        "reviewed reaction-correspondence payload changed",
    )
    _require(
        review["update_rule"] == REACTION_CORRESPONDENCE_REVIEW_UPDATE_RULE,
        "review must prohibit automatic scientific pin refresh",
    )
    _require(
        review["reviewer_kind"] == REACTION_CORRESPONDENCE_REVIEWER_KIND
        and review["same_model_agents"] is True,
        "review must disclose same-model computational agents",
    )
    _require(review["blind_review"] is False, "review was informed, not blind")
    _require(
        review["statistically_independent"] is False,
        "review cannot claim statistical independence",
    )
    _require(
        review["correlated_error_risk"] is True,
        "review must disclose correlated-error risk",
    )
    _require(
        type(review["human_reviewers"]) is int and review["human_reviewers"] == 0,
        "review must disclose zero human reviewers",
    )
    _require(
        review["domain_expert_review_claimed"] is False,
        "review cannot claim domain-expert review",
    )
    return review


def _expected_bundle_id(batch_id: str) -> str:
    base = "atlas50.source-scoped-mechanism-drafts"
    return base if batch_id == "default" else f"{base}.{batch_id}"


def _validate_source_bindings(
    value: Any, *, repo_root: str | Path | None
) -> tuple[dict[str, dict[str, Any]], dict[str, Path]]:
    _require(isinstance(value, list) and value, "source_bindings must be nonempty")
    root = Path(repo_root).resolve() if repo_root is not None else None
    by_id: dict[str, dict[str, Any]] = {}
    resolved: dict[str, Path] = {}
    paths: list[str] = []
    digests: set[str] = set()
    kinds: dict[str, int] = {}
    for index, raw in enumerate(value):
        context = f"source_bindings[{index}]"
        binding = _exact(raw, _SOURCE_BINDING_FIELDS, context)
        binding_id = _string(binding["binding_id"], f"{context}.binding_id")
        _require(binding_id not in by_id, f"{context} repeats binding_id")
        kind = binding["artifact_kind"]
        _require(kind in _ARTIFACT_KINDS, f"{context}.artifact_kind is invalid")
        kinds[kind] = kinds.get(kind, 0) + 1
        path_text = _string(binding["path"], f"{context}.path")
        posix_path = PurePosixPath(path_text)
        windows_path = PureWindowsPath(path_text)
        _require(
            "\\" not in path_text
            and not posix_path.is_absolute()
            and not windows_path.is_absolute()
            and not windows_path.drive
            and path_text == posix_path.as_posix()
            and "." not in posix_path.parts
            and ".." not in posix_path.parts,
            f"{context}.path must be repository-relative",
        )
        digest = _sha256(binding["sha256"], f"{context}.sha256")
        _require(digest not in digests, f"{context} repeats a source digest")
        digests.add(digest)
        paths.append(path_text)
        by_id[binding_id] = binding
        if root is not None:
            path = (root / Path(*posix_path.parts)).resolve()
            _require(root in path.parents and path.is_file(), f"{context} is missing")
            _require(
                canonical_file_sha256(path) == digest,
                f"{context} source hash differs",
            )
            resolved[binding_id] = path
    _require(paths == sorted(set(paths)), "source_bindings must be unique and path-sorted")
    for kind in _REQUIRED_SINGLE_ARTIFACT_KINDS:
        _require(kinds.get(kind) == 1, f"source_bindings require exactly one {kind}")
    _require(
        kinds.get("official_participant_structure") == 2,
        "source_bindings require two official participant structures",
    )
    return by_id, resolved


def _one_binding_of_kind(
    by_id: dict[str, dict[str, Any]], kind: str
) -> tuple[str, dict[str, Any]]:
    rows = [(binding_id, row) for binding_id, row in by_id.items()
            if row["artifact_kind"] == kind]
    _require(len(rows) == 1, f"expected one {kind} binding")
    return rows[0]


def _bound_record(
    value: Any, *, record_by_id: dict[str, dict[str, Any]], context: str
) -> tuple[str, dict[str, Any]]:
    binding = _exact(
        value, {"record_id", "mcsa_id", "source_snapshot_sha256"}, context
    )
    record_id = _string(binding["record_id"], f"{context}.record_id")
    mcsa_id = _string(binding["mcsa_id"], f"{context}.mcsa_id")
    _require(_MCSA_RE.fullmatch(mcsa_id) is not None, f"{context}.mcsa_id is invalid")
    snapshot = _sha256(
        binding["source_snapshot_sha256"], f"{context}.source_snapshot_sha256"
    )
    record = record_by_id.get(record_id)
    _require(record is not None, f"{context} targets an unknown source-draft record")
    _require(record["mcsa_id"] == mcsa_id, f"{context} record/M-CSA identity differs")
    _require(
        record["source"]["snapshot_sha256"] == snapshot,
        f"{context} source snapshot binding is stale",
    )
    return record_id, record


def _bound_proposal(
    value: Any, *, record: dict[str, Any], context: str
) -> dict[str, Any]:
    binding = _exact(value, {"proposal_id", "source_mechanism_id"}, context)
    proposal_id = _string(binding["proposal_id"], f"{context}.proposal_id")
    mechanism_id = _positive_int(
        binding["source_mechanism_id"], f"{context}.source_mechanism_id"
    )
    proposals = [
        proposal for proposal in record["mechanism_proposals"]
        if proposal["proposal_id"] == proposal_id
        and proposal["source_mechanism_id"] == mechanism_id
    ]
    _require(len(proposals) == 1, f"{context} does not identify one source proposal")
    return proposals[0]


def _participant_rows(value: Any, context: str) -> list[dict[str, Any]]:
    _require(isinstance(value, list) and value, f"{context} must be nonempty")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        row_context = f"{context}[{index}]"
        row = _exact(raw, {"chebi_id", "name", "stoichiometry"}, row_context)
        chebi_id = _string(row["chebi_id"], f"{row_context}.chebi_id")
        _require(_CHEBI_RE.fullmatch(chebi_id) is not None, f"{row_context}.chebi_id is invalid")
        _require(chebi_id not in seen, f"{context} repeats a participant")
        seen.add(chebi_id)
        _string(row["name"], f"{row_context}.name")
        _positive_int(row["stoichiometry"], f"{row_context}.stoichiometry")
        rows.append(row)
    return rows


def _validate_curated_reaction(
    value: Any, *, record: dict[str, Any], context: str
) -> dict[str, Any]:
    reaction = _exact(
        value,
        {
            "provider",
            "master_id",
            "left_to_right_id",
            "right_to_left_id",
            "bidirectional_id",
            "selected_directed_id",
            "selected_direction_code",
            "master_equation",
            "directed_equation",
            "left_participants",
            "right_participants",
            "support_edge_ids",
        },
        context,
    )
    _require(reaction["provider"] == "Rhea", f"{context}.provider is unsupported")
    ids = [
        reaction[field] for field in (
            "master_id", "left_to_right_id", "right_to_left_id", "bidirectional_id"
        )
    ]
    _require(
        all(isinstance(item, str) and _RHEA_RE.fullmatch(item) for item in ids)
        and len(set(ids)) == 4,
        f"{context} Rhea quartet is invalid",
    )
    _require(
        reaction["selected_directed_id"] == reaction["left_to_right_id"]
        and reaction["selected_direction_code"] == "LR",
        f"{context} must select the left-to-right member",
    )
    _string(reaction["master_equation"], f"{context}.master_equation")
    _string(reaction["directed_equation"], f"{context}.directed_equation")
    left = _participant_rows(reaction["left_participants"], f"{context}.left_participants")
    right = _participant_rows(reaction["right_participants"], f"{context}.right_participants")
    _strings(reaction["support_edge_ids"], f"{context}.support_edge_ids", minimum=1)

    source_rows = record["reaction_context"]["participants"]
    expected_left = [
        (row["normalized_chebi_id"], row["source_count"])
        for row in source_rows if row["side"] == "left"
    ]
    expected_right = [
        (row["normalized_chebi_id"], row["source_count"])
        for row in source_rows if row["side"] == "right"
    ]
    actual_left = [(row["chebi_id"], row["stoichiometry"]) for row in left]
    actual_right = [(row["chebi_id"], row["stoichiometry"]) for row in right]
    _require(
        actual_left == expected_left and actual_right == expected_right,
        f"{context} participants differ from the exact source-record sides",
    )
    _require(
        record["reaction_context"]["canonical_reaction"] is False
        and record["reaction_context"]["exact_reaction_instance"] is False,
        f"{context} cannot replace the source record's reaction boundary",
    )
    return reaction


def _validate_source_direction(
    value: Any,
    *,
    record: dict[str, Any],
    proposal: dict[str, Any],
    reaction: dict[str, Any],
    context: str,
) -> dict[str, Any]:
    direction = _exact(
        value,
        {"record_cross_reference", "proposal_declared_direction", "agreement_status"},
        context,
    )
    crossref = _exact(
        direction["record_cross_reference"],
        {
            "support_edge_id",
            "mcsa_id",
            "rhea_directed_id",
            "rhea_master_id",
            "direction_code",
            "scope",
            "grounds_proposal",
            "grounds_step",
        },
        f"{context}.record_cross_reference",
    )
    _string(crossref["support_edge_id"], f"{context}.record_cross_reference.support_edge_id")
    _require(
        crossref["mcsa_id"] == record["mcsa_id"]
        and crossref["rhea_directed_id"] == reaction["selected_directed_id"]
        and crossref["rhea_master_id"] == reaction["master_id"]
        and crossref["direction_code"] == reaction["selected_direction_code"],
        f"{context}.record_cross_reference differs from the selected reaction",
    )
    _require(
        crossref["scope"] == "source_record_only"
        and crossref["grounds_proposal"] is False
        and crossref["grounds_step"] is False,
        f"{context}.record_cross_reference overstates its scope",
    )

    declared = _exact(
        direction["proposal_declared_direction"],
        {
            "support_edge_id",
            "field",
            "exact_text",
            "direction",
            "boundary_step_witnesses",
        },
        f"{context}.proposal_declared_direction",
    )
    _string(declared["support_edge_id"], f"{context}.proposal_declared_direction.support_edge_id")
    _require(declared["field"] == "mechanism_text", f"{context} direction field is invalid")
    exact_text = _string(declared["exact_text"], f"{context}.proposal_declared_direction.exact_text")
    _require(
        exact_text == proposal["mechanism_text"],
        f"{context} proposal direction witness differs",
    )
    _require(declared["direction"] == "left_to_right", f"{context} proposal direction is unsupported")

    witnesses = declared["boundary_step_witnesses"]
    _require(isinstance(witnesses, list) and len(witnesses) == 2, f"{context} requires two boundary witnesses")
    steps_by_id = {step["step_id"]: step for step in proposal["mechanism_steps"]}
    seen_roles: set[str] = set()
    seen_steps: set[str] = set()
    for index, raw in enumerate(witnesses):
        witness_context = f"{context}.proposal_declared_direction.boundary_step_witnesses[{index}]"
        witness = _exact(
            raw,
            {
                "role",
                "step_id",
                "source_step_id",
                "source_scheme_sha256",
                "field",
                "exact_text",
                "participant_side",
                "participant_chebi_id",
                "scope",
            },
            witness_context,
        )
        role = witness["role"]
        _require(
            role in {"initial_reactant_designation", "released_product_designation"},
            f"{witness_context}.role is invalid",
        )
        _require(role not in seen_roles, f"{context} repeats a boundary role")
        seen_roles.add(role)
        step_id = _string(witness["step_id"], f"{witness_context}.step_id")
        _require(step_id not in seen_steps, f"{context} repeats a boundary step")
        seen_steps.add(step_id)
        step = steps_by_id.get(step_id)
        _require(step is not None, f"{witness_context} targets an unknown proposal step")
        _require(
            step["source_step_id"] == _positive_int(witness["source_step_id"], f"{witness_context}.source_step_id")
            and step["source_scheme_sha256"] == _sha256(
                witness["source_scheme_sha256"], f"{witness_context}.source_scheme_sha256"
            ),
            f"{witness_context} source-step binding differs",
        )
        _require(witness["field"] == "summary", f"{witness_context}.field is invalid")
        _require(witness["exact_text"] == step["summary"], f"{witness_context}.exact_text differs")
        expected_side = "left" if role == "initial_reactant_designation" else "right"
        _require(witness["participant_side"] == expected_side, f"{witness_context}.participant_side differs")
        selected = reaction[f"{expected_side}_participants"]
        _require(
            witness["participant_chebi_id"] in {row["chebi_id"] for row in selected},
            f"{witness_context}.participant_chebi_id differs",
        )
        _require(
            witness["scope"] == "source_text_designation_only",
            f"{witness_context}.scope overclaims",
        )
    _require(
        seen_roles == {"initial_reactant_designation", "released_product_designation"},
        f"{context} boundary roles differ",
    )
    _require(
        direction["agreement_status"]
        == "independent_record_and_proposal_direction_witnesses_agree",
        f"{context}.agreement_status is invalid",
    )
    return direction


def _validate_endpoint(value: Any, context: str) -> dict[str, Any]:
    endpoint = _exact(
        value,
        {
            "source_step_id",
            "scheme_sha256",
            "fragment_atom_ids",
            "alpha_carbon_atom_id",
            "amine_nitrogen_atom_id",
            "carboxylate_oxygen_atom_id",
            "stereo_token",
            "amine_nitrogen_formal_charge",
            "amine_nitrogen_lone_pair",
            "carboxylate_oxygen_formal_charge",
            "fragment_formal_charge",
            "external_fragment_bond_count",
            "computed_cip",
        },
        context,
    )
    _positive_int(endpoint["source_step_id"], f"{context}.source_step_id")
    _sha256(endpoint["scheme_sha256"], f"{context}.scheme_sha256")
    atoms = _strings(endpoint["fragment_atom_ids"], f"{context}.fragment_atom_ids", minimum=1)
    for field in (
        "alpha_carbon_atom_id", "amine_nitrogen_atom_id", "carboxylate_oxygen_atom_id"
    ):
        atom_id = _string(endpoint[field], f"{context}.{field}")
        _require(atom_id in atoms, f"{context}.{field} is outside the fragment")
    _require(endpoint["stereo_token"] in {"W", "H"}, f"{context}.stereo_token is invalid")
    for field in ("amine_nitrogen_formal_charge", "amine_nitrogen_lone_pair"):
        _require(
            endpoint[field] is None or type(endpoint[field]) is int,
            f"{context}.{field} must be an integer or null",
        )
    _require(
        type(endpoint["carboxylate_oxygen_formal_charge"]) is int,
        f"{context}.carboxylate_oxygen_formal_charge must be an integer",
    )
    _require(type(endpoint["fragment_formal_charge"]) is int, f"{context}.fragment_formal_charge must be an integer")
    _require(
        type(endpoint["external_fragment_bond_count"]) is int
        and endpoint["external_fragment_bond_count"] >= 0,
        f"{context}.external_fragment_bond_count must be a nonnegative integer",
    )
    _require(endpoint["computed_cip"] in {"R", "S"}, f"{context}.computed_cip is invalid")
    return endpoint


def _validate_terminal_depiction(
    value: Any,
    *,
    record: dict[str, Any],
    proposal: dict[str, Any],
    reaction: dict[str, Any],
    context: str,
) -> dict[str, Any]:
    depiction = _exact(
        value,
        {
            "terminal_step_binding",
            "alanine_fragment_raw_source_labels",
            "endpoint_diagnostic",
            "all_panel_trajectory_status",
            "step_3_exception",
            "support_edge_ids",
        },
        context,
    )
    terminal = _exact(
        depiction["terminal_step_binding"],
        {
            "source_step_id",
            "scheme_sha256",
            "exact_text",
        },
        f"{context}.terminal_step_binding",
    )
    terminal_step_id = _positive_int(
        terminal["source_step_id"], f"{context}.terminal_step_binding.source_step_id"
    )
    terminal_sha = _sha256(
        terminal["scheme_sha256"],
        f"{context}.terminal_step_binding.scheme_sha256",
    )
    _string(terminal["exact_text"], f"{context}.terminal_step_binding.exact_text")
    inventory = [
        row for row in record["source"]["source_step_inventory"]
        if row["source_mechanism_id"] == proposal["source_mechanism_id"]
        and row["source_step_id"] == terminal_step_id
    ]
    _require(
        len(inventory) == 1
        and inventory[0]["is_terminal_state"] is True
        and inventory[0]["source_scheme_sha256"] == terminal_sha,
        f"{context}.terminal_step_binding differs from source inventory",
    )
    _require(
        terminal_step_id not in {step["source_step_id"] for step in proposal["mechanism_steps"]},
        f"{context}.terminal panel is unexpectedly compiled as a mechanism step",
    )
    raw_labels = _strings(
        depiction["alanine_fragment_raw_source_labels"],
        f"{context}.alanine_fragment_raw_source_labels",
        minimum=1,
    )
    _require(
        all(label.startswith("chebi:") for label in raw_labels),
        f"{context}.alanine_fragment_raw_source_labels are invalid",
    )
    expected_initial_labels = [
        row["chebi_id"].lower() for row in reaction["left_participants"]
    ]
    terminal_participant_labels = {
        row["chebi_id"].lower() for row in reaction["right_participants"]
    }
    _require(
        raw_labels == expected_initial_labels
        and not (set(raw_labels) & terminal_participant_labels),
        f"{context}.alanine_fragment_raw_source_labels must preserve the "
        "source-label/product conflict",
    )
    _strings(depiction["support_edge_ids"], f"{context}.support_edge_ids", minimum=1)
    diagnostic = _exact(
        depiction["endpoint_diagnostic"],
        {"status", "scope", "chemical_identity_status", "initial", "terminal"},
        f"{context}.endpoint_diagnostic",
    )
    _require(
        diagnostic["status"] == "endpoint_depictions_conflict_with_reported_direction"
        and diagnostic["scope"]
        == "reviewed_per_panel_computational_diagnostic_not_atom_mapping"
        and diagnostic["chemical_identity_status"] == "not_normalized",
        f"{context}.endpoint_diagnostic boundary differs",
    )
    initial = _validate_endpoint(diagnostic["initial"], f"{context}.endpoint_diagnostic.initial")
    final = _validate_endpoint(diagnostic["terminal"], f"{context}.endpoint_diagnostic.terminal")
    proposal_steps_by_source_id = {
        step["source_step_id"]: step for step in proposal["mechanism_steps"]
    }
    initial_step = proposal_steps_by_source_id.get(initial["source_step_id"])
    _require(
        initial_step is not None
        and initial_step["source_scheme_sha256"] == initial["scheme_sha256"]
        and final["source_step_id"] == terminal_step_id
        and final["scheme_sha256"] == terminal_sha,
        f"{context}.endpoint panels differ from proposal/terminal bindings",
    )
    _require(
        initial["computed_cip"] != final["computed_cip"],
        f"{context}.endpoint diagnostic does not preserve the reviewed conflict",
    )
    _require(
        depiction["all_panel_trajectory_status"] == "not_asserted",
        f"{context} cannot infer an all-panel trajectory",
    )
    exception = _exact(
        depiction["step_3_exception"],
        {
            "source_step_id",
            "scheme_sha256",
            "stereo_token",
            "explicit_alpha_hydrogen_atom_id",
            "computed_cip",
        },
        f"{context}.step_3_exception",
    )
    exception_step_id = _positive_int(
        exception["source_step_id"], f"{context}.step_3_exception.source_step_id"
    )
    exception_steps = [
        step for step in proposal["mechanism_steps"]
        if step["source_step_id"] == exception_step_id
    ]
    _require(
        len(exception_steps) == 1
        and exception_steps[0]["source_scheme_sha256"]
        == _sha256(exception["scheme_sha256"], f"{context}.step_3_exception.scheme_sha256"),
        f"{context}.step_3_exception differs from the proposal",
    )
    _require(exception["stereo_token"] in {"W", "H"}, f"{context}.step_3_exception.stereo_token is invalid")
    _string(
        exception["explicit_alpha_hydrogen_atom_id"],
        f"{context}.step_3_exception.explicit_alpha_hydrogen_atom_id",
    )
    _require(exception["computed_cip"] in {"R", "S"}, f"{context}.step_3_exception.computed_cip is invalid")
    return depiction


def _validate_atom_correspondence(value: Any, *, context: str) -> dict[str, Any]:
    atom = _exact(
        value,
        {
            "status",
            "rhea_participant_mol_mapping_numbers",
            "directed_rxn_capture_status",
            "scope",
            "support_edge_ids",
        },
        context,
    )
    _require(
        atom["status"] == "not_established"
        and atom["rhea_participant_mol_mapping_numbers"] == "all_zero"
        and atom["directed_rxn_capture_status"] == "unavailable_http_403_html"
        and atom["scope"] == "inspected_artifacts_only",
        f"{context} boundary differs",
    )
    _strings(atom["support_edge_ids"], f"{context}.support_edge_ids", minimum=1)
    return atom


def _validate_projection_excerpt(
    value: Any, *, binding_ids: set[str], context: str
) -> dict[str, Any]:
    excerpt = _exact(value, {"support_edges", "locators"}, context)
    for key, id_field in (("support_edges", "edge_id"), ("locators", "locator_id")):
        rows = excerpt[key]
        _require(isinstance(rows, list) and rows, f"{context}.{key} must be nonempty")
        ids: list[str] = []
        for index, raw in enumerate(rows):
            row = _object(raw, f"{context}.{key}[{index}]")
            row_id = _string(row.get(id_field), f"{context}.{key}[{index}].{id_field}")
            ids.append(row_id)
            source_ids = row.get("source_binding_ids")
            if source_ids is None and "source_binding_id" in row:
                source_ids = [row["source_binding_id"]]
            if source_ids is not None:
                cited = _strings(source_ids, f"{context}.{key}[{index}].source_binding_ids", minimum=1)
                _require(set(cited) <= binding_ids, f"{context}.{key}[{index}] cites unknown source bindings")
        _require(len(ids) == len(set(ids)), f"{context}.{key} IDs must be unique")
    return excerpt


def _validate_limits_and_scope(
    annotation: dict[str, Any], *, record: dict[str, Any], context: str
) -> None:
    required = _strings(
        annotation["required_abstentions"], f"{context}.required_abstentions", minimum=1
    )
    _require(set(required) == _REQUIRED_ABSTENTIONS, f"{context}.required_abstentions differ")
    limits = annotation["limitations"]
    _require(isinstance(limits, list) and limits, f"{context}.limitations must be nonempty")
    observed: list[str] = []
    for index, raw in enumerate(limits):
        limit_context = f"{context}.limitations[{index}]"
        limit = _exact(raw, {"limit_id", "status", "statement"}, limit_context)
        limit_id = _string(limit["limit_id"], f"{limit_context}.limit_id")
        observed.append(limit_id)
        _require(limit["status"] == "abstained", f"{limit_context}.status must be abstained")
        _string(limit["statement"], f"{limit_context}.statement")
    _require(len(observed) == len(set(observed)), f"{context}.limitations IDs must be unique")
    _require(set(observed) >= _REQUIRED_ABSTENTIONS, f"{context}.limitations omit required boundaries")
    source_limit_ids = {row["clause_id"] for row in record["mandatory_abstentions"]}
    _require(
        {"terminal_product_identity", "direction_specific_role_assignment"}
        <= source_limit_ids,
        f"{context} source record lacks required conflict abstentions",
    )
    scope = _exact(annotation["scope_effect"], _SCOPE_EFFECT_FIELDS, f"{context}.scope_effect")
    _require(
        all(scope[field] is False for field in _SCOPE_EFFECT_FIELDS),
        f"{context}.scope_effect attempts to expand the source draft",
    )


def _validate_projection_binding(
    value: Any, *, bindings: dict[str, dict[str, Any]], context: str
) -> dict[str, Any]:
    projection = _exact(value, {"binding_id", "projection_id", "sha256"}, context)
    binding_id = _string(projection["binding_id"], f"{context}.binding_id")
    _string(projection["projection_id"], f"{context}.projection_id")
    digest = _sha256(projection["sha256"], f"{context}.sha256")
    binding = bindings.get(binding_id)
    _require(
        binding is not None
        and binding["artifact_kind"] == "project_reaction_projection"
        and binding["sha256"] == digest,
        f"{context} does not bind the project reaction projection",
    )
    return projection


def _read_json(path: Path, context: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{context} is not valid UTF-8 JSON") from exc


def _read_tsv(path: Path, context: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = path.read_text(encoding="utf-8")
        reader = csv.DictReader(io.StringIO(text), delimiter="\t")
        fields = reader.fieldnames
        _require(fields is not None and all(fields), f"{context} lacks a TSV header")
        rows = list(reader)
        _require(all(None not in row for row in rows), f"{context} has malformed TSV rows")
        return list(fields), rows
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise ValueError(f"{context} is not valid UTF-8 TSV") from exc


def _binding_path(
    bindings: dict[str, dict[str, Any]], resolved: dict[str, Path], kind: str
) -> Path:
    binding_id, _ = _one_binding_of_kind(bindings, kind)
    path = resolved.get(binding_id)
    _require(path is not None, f"{kind} path was not resolved")
    return path


def _support_edge(annotation: dict[str, Any], edge_id: str) -> dict[str, Any]:
    matches = [
        row
        for row in annotation["projection_excerpt"]["support_edges"]
        if isinstance(row, dict) and row.get("edge_id") == edge_id
    ]
    _require(len(matches) == 1, f"projection excerpt lacks {edge_id}")
    return matches[0]


def _read_v2000_participant(path: Path) -> dict[str, Any]:
    """Read only the narrow V2000 facts declared by this sidecar."""

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError("official participant structure is not UTF-8 V2000") from exc
    _require(len(lines) >= 6 and lines[3].endswith("V2000"), "official participant structure is not V2000")
    chebi_id = lines[0].strip()
    _require(_CHEBI_RE.fullmatch(chebi_id) is not None, "official participant structure title is not a ChEBI ID")
    try:
        atom_count = int(lines[3][0:3])
        bond_count = int(lines[3][3:6])
    except (ValueError, IndexError) as exc:
        raise ValueError("official participant structure counts line is malformed") from exc
    atom_lines = lines[4 : 4 + atom_count]
    bond_lines = lines[4 + atom_count : 4 + atom_count + bond_count]
    _require(
        len(atom_lines) == atom_count and len(bond_lines) == bond_count,
        "official participant structure is truncated",
    )
    try:
        mapping_numbers = [int(line[60:63]) for line in atom_lines]
        bonds = [tuple(int(token) for token in line.split()[:4]) for line in bond_lines]
    except (ValueError, IndexError) as exc:
        raise ValueError("official participant structure atom/bond block is malformed") from exc
    alpha_n = [row for row in bonds if {row[0], row[1]} == {2, 5}]
    _require(len(alpha_n) == 1, "official participant structure lacks one bond 2-5")
    charge_rows = [line for line in lines if line.startswith("M  CHG")]
    _require(lines[-1] == "M  END", "official participant structure lacks M  END")
    return {
        "chebi_id": chebi_id,
        "atom_count": atom_count,
        "atom_mapping_numbers": "all_zero" if not any(mapping_numbers) else "nonzero_present",
        "alpha_c_n_mdl_stereo_code": alpha_n[0][3],
        "formal_charge_records": charge_rows,
    }


def _audit_participant_structures(
    annotation: dict[str, Any],
    *,
    bindings: dict[str, dict[str, Any]],
    resolved: dict[str, Path],
) -> None:
    edge = _support_edge(annotation, "edge:rhea-participant-forms")
    extracted = _object(edge.get("extracted_values"), "participant-form edge extracted_values")
    expected_rows = extracted.get("participants")
    _require(isinstance(expected_rows, list) and expected_rows, "participant-form edge is incomplete")
    expected_rows = [
        _object(row, f"participant-form edge participants[{index}]")
        for index, row in enumerate(expected_rows)
    ]
    actual_rows: list[dict[str, Any]] = []
    for binding_id, binding in bindings.items():
        if binding["artifact_kind"] != "official_participant_structure":
            continue
        path = resolved.get(binding_id)
        _require(path is not None, "official participant structure path was not resolved")
        actual_rows.append(_read_v2000_participant(path))
    _require(
        sorted(actual_rows, key=lambda row: row["chebi_id"])
        == sorted(expected_rows, key=lambda row: row.get("chebi_id", "")),
        "official participant structure facts differ from the reviewed excerpt",
    )
    _require(
        all(row["atom_mapping_numbers"] == "all_zero" for row in actual_rows)
        and annotation["atom_correspondence"][
            "rhea_participant_mol_mapping_numbers"
        ]
        == "all_zero",
        "official participant structures do not support the atom-map abstention",
    )


def _rdf_values(raw: Any, context: str) -> dict[str, dict[str, list[str]]]:
    top = _object(raw, context)
    results = _object(top.get("results"), f"{context}.results")
    rows = results.get("bindings")
    _require(isinstance(rows, list), f"{context}.results.bindings must be an array")
    by_reaction: dict[str, dict[str, list[str]]] = {}
    for index, raw_row in enumerate(rows):
        row_context = f"{context}.results.bindings[{index}]"
        row = _object(raw_row, row_context)
        _require(set(row) == {"rhea", "predicate", "object"}, f"{row_context} fields differ")
        values = []
        for field in ("rhea", "predicate", "object"):
            cell = _object(row[field], f"{row_context}.{field}")
            values.append(_string(cell.get("value"), f"{row_context}.{field}.value"))
        rhea_uri, predicate_uri, object_value = values
        _require(rhea_uri.startswith("http://rdf.rhea-db.org/"), f"{row_context}.rhea is invalid")
        rhea_id = rhea_uri.rsplit("/", 1)[-1]
        predicate = predicate_uri.rsplit("/", 1)[-1]
        by_reaction.setdefault(rhea_id, {}).setdefault(predicate, []).append(object_value)
    return by_reaction


def _require_rdf_value(
    values: dict[str, dict[str, list[str]]], rhea_id: str, predicate: str, expected: str
) -> None:
    actual = values.get(rhea_id, {}).get(predicate, [])
    _require(expected in actual, f"Rhea RDF lacks {rhea_id} {predicate} {expected}")


def _validate_uniprot_master(path: Path, reaction: dict[str, Any]) -> None:
    value = _object(_read_json(path, "curated protein record"), "curated protein record")
    activities = [
        comment.get("reaction") for comment in value.get("comments", [])
        if isinstance(comment, dict) and comment.get("commentType") == "CATALYTIC ACTIVITY"
        and isinstance(comment.get("reaction"), dict)
    ]
    matches = []
    expected_chebis = {
        row["chebi_id"] for side in ("left_participants", "right_participants")
        for row in reaction[side]
    }
    for activity in activities:
        refs = activity.get("reactionCrossReferences", [])
        rhea_ids = {row.get("id") for row in refs if row.get("database") == "Rhea"}
        chebi_ids = {row.get("id") for row in refs if row.get("database") == "ChEBI"}
        if reaction["master_id"] in rhea_ids and expected_chebis <= chebi_ids:
            matches.append(activity)
    _require(len(matches) == 1, "curated protein record lacks the exact master-reaction identity")


def _audit_rhea_sources(
    annotation: dict[str, Any], *, bindings: dict[str, dict[str, Any]], resolved: dict[str, Path]
) -> None:
    reaction = annotation["curated_reaction"]
    source_direction = annotation["source_direction"]
    record_binding = annotation["record_binding"]

    fields, rows = _read_tsv(
        _binding_path(bindings, resolved, "official_reaction_direction_map"),
        "Rhea direction map",
    )
    _require(
        fields == ["RHEA_ID_MASTER", "RHEA_ID_LR", "RHEA_ID_RL", "RHEA_ID_BI"],
        "Rhea direction-map header differs",
    )
    expected_direction_row = {
        "RHEA_ID_MASTER": reaction["master_id"].split(":", 1)[1],
        "RHEA_ID_LR": reaction["left_to_right_id"].split(":", 1)[1],
        "RHEA_ID_RL": reaction["right_to_left_id"].split(":", 1)[1],
        "RHEA_ID_BI": reaction["bidirectional_id"].split(":", 1)[1],
    }
    _require(rows.count(expected_direction_row) == 1, "Rhea direction quartet differs")

    fields, rows = _read_tsv(
        _binding_path(bindings, resolved, "official_reaction_cross_reference_map"),
        "Rhea M-CSA cross-reference map",
    )
    _require(fields == ["RHEA_ID", "DIRECTION", "MASTER_ID", "ID"], "Rhea cross-reference header differs")
    crossref = source_direction["record_cross_reference"]
    expected_crossref = {
        "RHEA_ID": crossref["rhea_directed_id"].split(":", 1)[1],
        "DIRECTION": crossref["direction_code"],
        "MASTER_ID": crossref["rhea_master_id"].split(":", 1)[1],
        "ID": crossref["mcsa_id"],
    }
    _require(rows.count(expected_crossref) == 1, "Rhea M-CSA cross-reference differs")

    fields, rows = _read_tsv(
        _binding_path(bindings, resolved, "official_reaction_query"),
        "Rhea master-reaction query",
    )
    _require(
        fields == ["Reaction identifier", "Equation", "ChEBI identifier", "EC number"],
        "Rhea master-query header differs",
    )
    expected_chebis = ";".join(
        row["chebi_id"]
        for side in ("left_participants", "right_participants")
        for row in reaction[side]
    )
    expected_query = {
        "Reaction identifier": reaction["master_id"],
        "Equation": reaction["master_equation"],
        "ChEBI identifier": expected_chebis,
        "EC number": "EC:" + annotation["_record"]["reaction_context"]["ec_numbers"][0],
    }
    _require(rows == [expected_query], "Rhea master reaction/participants differ")

    rdf = _rdf_values(
        _read_json(
            _binding_path(bindings, resolved, "official_reaction_rdf_query"),
            "Rhea quartet RDF query",
        ),
        "Rhea quartet RDF query",
    )
    numeric = {field: reaction[field].split(":", 1)[1] for field in (
        "master_id", "left_to_right_id", "right_to_left_id", "bidirectional_id"
    )}
    _require_rdf_value(rdf, numeric["master_id"], "accession", reaction["master_id"])
    _require_rdf_value(rdf, numeric["master_id"], "equation", reaction["master_equation"])
    _require_rdf_value(
        rdf, numeric["master_id"], "directionalReaction",
        f"http://rdf.rhea-db.org/{numeric['left_to_right_id']}",
    )
    _require_rdf_value(
        rdf, numeric["master_id"], "directionalReaction",
        f"http://rdf.rhea-db.org/{numeric['right_to_left_id']}",
    )
    _require_rdf_value(
        rdf, numeric["master_id"], "bidirectionalReaction",
        f"http://rdf.rhea-db.org/{numeric['bidirectional_id']}",
    )
    _require_rdf_value(
        rdf, numeric["left_to_right_id"], "equation", reaction["directed_equation"]
    )
    _require_rdf_value(
        rdf, numeric["left_to_right_id"], "substrates",
        f"http://rdf.rhea-db.org/{numeric['master_id']}_L",
    )
    _require_rdf_value(
        rdf, numeric["left_to_right_id"], "products",
        f"http://rdf.rhea-db.org/{numeric['master_id']}_R",
    )
    _require_rdf_value(
        rdf, numeric["right_to_left_id"], "substrates",
        f"http://rdf.rhea-db.org/{numeric['master_id']}_R",
    )
    _require_rdf_value(
        rdf, numeric["right_to_left_id"], "products",
        f"http://rdf.rhea-db.org/{numeric['master_id']}_L",
    )
    _require_rdf_value(
        rdf, numeric["bidirectional_id"], "substratesOrProducts",
        f"http://rdf.rhea-db.org/{numeric['master_id']}_L",
    )
    _require_rdf_value(
        rdf, numeric["bidirectional_id"], "substratesOrProducts",
        f"http://rdf.rhea-db.org/{numeric['master_id']}_R",
    )
    _require_rdf_value(
        rdf, numeric["left_to_right_id"], "rdf-schema#seeAlso",
        f"http://identifiers.org/macie/{record_binding['mcsa_id']}",
    )
    for rhea_id in numeric.values():
        _require_rdf_value(rdf, rhea_id, "status", "http://rdf.rhea-db.org/Approved")

    _validate_uniprot_master(
        _binding_path(bindings, resolved, "curated_protein_record"), reaction
    )


def _mrv_atoms_and_bonds(content: str, context: str) -> tuple[dict[str, dict[str, str]], list[dict[str, Any]]]:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise ValueError(f"{context} contains malformed MRV XML") from exc
    atoms: dict[str, dict[str, str]] = {}
    bonds: list[dict[str, Any]] = []
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "atom":
            atom_id = element.attrib.get("id")
            _require(atom_id is not None and atom_id not in atoms, f"{context} atom IDs differ")
            atoms[atom_id] = dict(element.attrib)
        elif tag == "bond":
            refs = element.attrib.get("atomRefs2", "").split()
            _require(len(refs) == 2, f"{context} bond atomRefs2 differs")
            stereo = None
            for child in element:
                if child.tag.rsplit("}", 1)[-1] == "bondStereo":
                    stereo = child.text
            bonds.append({"atom_refs": refs, "stereo": stereo})
    _require(atoms and bonds, f"{context} lacks atoms or bonds")
    return atoms, bonds


def _optional_int(raw: str | None, context: str) -> int | None:
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{context} is not an integer") from exc


def _audit_endpoint(
    endpoint: dict[str, Any],
    *,
    scheme: dict[str, Any],
    expected_source_labels: list[str],
    context: str,
) -> None:
    content = scheme.get("content_utf8")
    _require(isinstance(content, str), f"{context} source scheme lacks UTF-8 content")
    atoms, bonds = _mrv_atoms_and_bonds(content, context)
    fragment_ids = endpoint["fragment_atom_ids"]
    _require(set(fragment_ids) <= set(atoms), f"{context} fragment atoms differ")
    label_values = {
        atoms[atom_id].get("mrvExtraLabel") for atom_id in fragment_ids
        if atoms[atom_id].get("mrvExtraLabel") is not None
    }
    _require(
        label_values == set(expected_source_labels),
        f"{context} fragment source labels differ",
    )
    alpha_id = endpoint["alpha_carbon_atom_id"]
    nitrogen_id = endpoint["amine_nitrogen_atom_id"]
    oxygen_id = endpoint["carboxylate_oxygen_atom_id"]
    matches = [
        bond for bond in bonds if set(bond["atom_refs"]) == {alpha_id, nitrogen_id}
    ]
    _require(
        len(matches) == 1 and matches[0]["stereo"] == endpoint["stereo_token"],
        f"{context} alpha-carbon/nitrogen stereo differs",
    )
    _require(
        _optional_int(atoms[nitrogen_id].get("formalCharge"), f"{context} N charge")
        == endpoint["amine_nitrogen_formal_charge"]
        and _optional_int(atoms[nitrogen_id].get("lonePair"), f"{context} N lone pair")
        == endpoint["amine_nitrogen_lone_pair"]
        and _optional_int(atoms[oxygen_id].get("formalCharge"), f"{context} O charge")
        == endpoint["carboxylate_oxygen_formal_charge"],
        f"{context} endpoint charge/lone-pair attributes differ",
    )
    charge_sum = sum(
        _optional_int(atoms[atom_id].get("formalCharge"), f"{context} fragment charge") or 0
        for atom_id in fragment_ids
    )
    _require(charge_sum == endpoint["fragment_formal_charge"], f"{context} fragment charge differs")
    fragment = set(fragment_ids)
    external = sum(
        (bond["atom_refs"][0] in fragment) != (bond["atom_refs"][1] in fragment)
        for bond in bonds
    )
    _require(
        external == endpoint["external_fragment_bond_count"],
        f"{context} external-fragment bond count differs",
    )


def _audit_mcsa_source(
    annotation: dict[str, Any], *, bindings: dict[str, dict[str, Any]], resolved: dict[str, Path]
) -> None:
    raw = _object(
        _read_json(
            _binding_path(bindings, resolved, "source_record_snapshot"),
            "M-CSA source snapshot",
        ),
        "M-CSA source snapshot",
    )
    _require(raw.get("record_id") == annotation["record_binding"]["mcsa_id"], "M-CSA snapshot identity differs")
    entry = _object(raw.get("entry"), "M-CSA source snapshot.entry")
    reaction = _object(entry.get("reaction"), "M-CSA source snapshot.entry.reaction")
    compounds = reaction.get("compounds")
    _require(isinstance(compounds, list), "M-CSA source reaction compounds are missing")
    expected = []
    for side, source_type in (("left", "reactant"), ("right", "product")):
        for row in annotation["curated_reaction"][f"{side}_participants"]:
            expected.append((source_type, row["chebi_id"].split(":", 1)[1], row["stoichiometry"]))
    actual = [(row.get("type"), str(row.get("chebi_id")), row.get("count")) for row in compounds]
    _require(actual == expected, "M-CSA snapshot reaction participants differ")

    mechanisms = reaction.get("mechanisms")
    _require(isinstance(mechanisms, list), "M-CSA source mechanisms are missing")
    selected = [row for row in mechanisms if row.get("mechanism_id") == annotation["proposal_binding"]["source_mechanism_id"]]
    _require(len(selected) == 1, "M-CSA source proposal differs")
    mechanism = selected[0]
    declared = annotation["source_direction"]["proposal_declared_direction"]
    _require(
        declared["exact_text"] == mechanism.get("mechanism_text"),
        "M-CSA proposal direction text differs",
    )
    raw_steps = {row.get("step_id"): row for row in mechanism.get("steps", [])}
    for witness in declared["boundary_step_witnesses"]:
        raw_step = raw_steps.get(witness["source_step_id"])
        _require(
            isinstance(raw_step, dict) and raw_step.get("description") == witness["exact_text"],
            "M-CSA boundary-step source text differs",
        )
    terminal = annotation["terminal_depiction"]["terminal_step_binding"]
    raw_terminal = raw_steps.get(terminal["source_step_id"])
    _require(
        isinstance(raw_terminal, dict)
        and raw_terminal.get("description") == terminal["exact_text"]
        and raw_terminal.get("is_product") is True,
        "M-CSA terminal source step differs",
    )
    scheme_rows = {
        row.get("step_id"): row for row in raw.get("step_schemes", [])
        if row.get("mechanism_id") == annotation["proposal_binding"]["source_mechanism_id"]
    }
    for endpoint_name in ("initial", "terminal"):
        endpoint = annotation["terminal_depiction"]["endpoint_diagnostic"][endpoint_name]
        scheme = scheme_rows.get(endpoint["source_step_id"])
        _require(
            isinstance(scheme, dict)
            and scheme.get("content_sha256") == endpoint["scheme_sha256"],
            f"M-CSA {endpoint_name} scheme binding differs",
        )
        _audit_endpoint(
            endpoint,
            scheme=scheme,
            expected_source_labels=annotation["terminal_depiction"][
                "alanine_fragment_raw_source_labels"
            ],
            context=f"M-CSA {endpoint_name} endpoint",
        )
    exception = annotation["terminal_depiction"]["step_3_exception"]
    scheme = scheme_rows.get(exception["source_step_id"])
    _require(
        isinstance(scheme, dict) and scheme.get("content_sha256") == exception["scheme_sha256"],
        "M-CSA Step3 exception scheme differs",
    )
    atoms, bonds = _mrv_atoms_and_bonds(scheme["content_utf8"], "M-CSA Step3 exception")
    hydrogen_id = exception["explicit_alpha_hydrogen_atom_id"]
    _require(atoms.get(hydrogen_id, {}).get("elementType") == "H", "M-CSA Step3 explicit hydrogen differs")
    alpha_id = annotation["terminal_depiction"]["endpoint_diagnostic"]["initial"]["alpha_carbon_atom_id"]
    _require(
        any(set(row["atom_refs"]) == {alpha_id, hydrogen_id} for row in bonds),
        "M-CSA Step3 alpha-hydrogen bond differs",
    )
    exception_fragment = annotation["terminal_depiction"]["endpoint_diagnostic"][
        "initial"
    ]["fragment_atom_ids"]
    exception_labels = {
        atoms[atom_id].get("mrvExtraLabel")
        for atom_id in exception_fragment
        if atoms.get(atom_id, {}).get("mrvExtraLabel") is not None
    }
    _require(
        exception_labels
        == set(annotation["terminal_depiction"]["alanine_fragment_raw_source_labels"]),
        "M-CSA Step3 fragment source labels differ",
    )
    nitrogen_id = annotation["terminal_depiction"]["endpoint_diagnostic"]["initial"][
        "amine_nitrogen_atom_id"
    ]
    _require(
        any(
            set(row["atom_refs"]) == {alpha_id, nitrogen_id}
            and row["stereo"] == exception["stereo_token"]
            for row in bonds
        ),
        "M-CSA Step3 alpha-carbon/nitrogen stereo differs",
    )


def _audit_computational_depiction(
    annotation: dict[str, Any], *, bindings: dict[str, dict[str, Any]], resolved: dict[str, Path]
) -> None:
    value = _object(
        _read_json(
            _binding_path(bindings, resolved, "computational_depiction_audit"),
            "computational depiction audit",
        ),
        "computational depiction audit",
    )
    _require(
        value.get("source_snapshot_sha256") == annotation["record_binding"]["source_snapshot_sha256"],
        "computational depiction audit targets a different source snapshot",
    )
    script_id, script_binding = _one_binding_of_kind(
        bindings, "computational_depiction_audit_script"
    )
    _require(
        value.get("script_sha256") == script_binding["sha256"]
        and script_id in {
            binding_id for edge in annotation["projection_excerpt"]["support_edges"]
            for binding_id in edge.get("source_binding_ids", [])
            if edge.get("edge_id") == "edge:computational-endpoint-cip"
        },
        "computational depiction audit does not bind its retained script",
    )
    panels = value.get("panels")
    _require(isinstance(panels, list), "computational depiction audit panels are missing")
    by_step = {row.get("step_id"): row for row in panels if isinstance(row, dict)}
    _require(
        len(by_step) == len(panels) and set(by_step) == set(range(1, 8)),
        "computational depiction audit panel inventory differs",
    )
    diagnostic = annotation["terminal_depiction"]["endpoint_diagnostic"]
    for endpoint_name in ("initial", "terminal"):
        endpoint = diagnostic[endpoint_name]
        row = by_step.get(endpoint["source_step_id"])
        _require(
            isinstance(row, dict)
            and row.get("scheme_sha256") == endpoint["scheme_sha256"]
            and row.get("computed_cip") == endpoint["computed_cip"]
            and row.get("computed_endpoint_formal_charge")
            == endpoint["fragment_formal_charge"],
            f"computational {endpoint_name} endpoint diagnostic differs",
        )
    exception = annotation["terminal_depiction"]["step_3_exception"]
    row = by_step.get(exception["source_step_id"])
    _require(
        isinstance(row, dict)
        and row.get("scheme_sha256") == exception["scheme_sha256"]
        and row.get("computed_cip") == exception["computed_cip"],
        "computational Step3 exception diagnostic differs",
    )
    _require(
        value.get("exact_chebi_species_assigned") is False
        and value.get("reaction_atom_mapping_established") is False
        and value.get("intermediate_trajectory_status") == "not_asserted",
        "computational depiction audit overstates its result",
    )
    participant_bindings = {
        binding["sha256"]: (binding_id, Path(binding["path"]).name)
        for binding_id, binding in bindings.items()
        if binding["artifact_kind"] == "official_participant_structure"
    }
    references = value.get("references")
    _require(
        isinstance(references, list)
        and len(references) == len(participant_bindings),
        "computational depiction audit participant references differ",
    )
    reference_by_chebi: dict[str, dict[str, Any]] = {}
    for index, reference in enumerate(references):
        ref = _object(reference, f"computational depiction audit references[{index}]")
        binding_row = participant_bindings.get(ref.get("source_sha256"))
        chebi_id = ref.get("source_chebi_id")
        _require(
            binding_row is not None
            and ref.get("source_file") == binding_row[1]
            and chebi_id
            in {
                row["chebi_id"]
                for side in ("left_participants", "right_participants")
                for row in annotation["curated_reaction"][side]
            }
            and ref.get("computed_cip") in {"R", "S"}
            and type(ref.get("computed_formal_charge")) is int
            and chebi_id not in reference_by_chebi,
            "computational depiction audit participant reference differs",
        )
        reference_by_chebi[chebi_id] = ref
    left = annotation["curated_reaction"]["left_participants"]
    right = annotation["curated_reaction"]["right_participants"]
    _require(
        len(left) == len(right) == 1
        and reference_by_chebi[left[0]["chebi_id"]]["computed_cip"]
        != diagnostic["initial"]["computed_cip"]
        and reference_by_chebi[right[0]["chebi_id"]]["computed_cip"]
        != diagnostic["terminal"]["computed_cip"]
        and reference_by_chebi[left[0]["chebi_id"]]["computed_formal_charge"]
        != diagnostic["initial"]["fragment_formal_charge"]
        and reference_by_chebi[right[0]["chebi_id"]]["computed_formal_charge"]
        != diagnostic["terminal"]["fragment_formal_charge"],
        "computational endpoint conflict differs from the participant references",
    )


def _audit_projection(
    annotation: dict[str, Any], *, bindings: dict[str, dict[str, Any]], resolved: dict[str, Path]
) -> None:
    projection_path = _binding_path(bindings, resolved, "project_reaction_projection")
    projection = _exact(
        _read_json(projection_path, "reaction correspondence projection"),
        {
            "schema_version",
            "projection_id",
            "correspondence_id",
            "record_binding",
            "proposal_binding",
            "source_bindings",
            "curated_reaction",
            "source_direction",
            "terminal_depiction",
            "atom_correspondence",
            "support_edges",
            "locators",
            "limitations",
        },
        "reaction correspondence projection",
    )
    _require(
        projection["schema_version"] == REACTION_CORRESPONDENCE_PROJECTION_SCHEMA_VERSION,
        "unsupported reaction correspondence projection",
    )
    binding = annotation["projection_binding"]
    _require(
        projection["projection_id"] == binding["projection_id"]
        and projection["correspondence_id"] == annotation["annotation_id"],
        "reaction correspondence projection identity differs",
    )
    for field in (
        "record_binding", "proposal_binding", "curated_reaction", "source_direction",
        "terminal_depiction", "limitations",
    ):
        _require(projection[field] == annotation[field], f"reaction projection {field} differs")
    excerpt = {"support_edges": projection["support_edges"], "locators": projection["locators"]}
    _require(excerpt == annotation["projection_excerpt"], "reaction projection excerpt differs")
    atom = _exact(
        projection["atom_correspondence"],
        {
            "status",
            "rhea_participant_mol_mapping_numbers",
            "directed_rxn_capture_status",
            "scope",
        },
        "reaction correspondence projection.atom_correspondence",
    )
    _require(
        atom == {
            "status": "not_established",
            "rhea_participant_mol_mapping_numbers": "all_zero",
            "directed_rxn_capture_status": "unavailable_http_403_html",
            "scope": "inspected_artifacts_only",
        },
        "reaction projection atom-correspondence boundary differs",
    )
    _require(
        atom
        == {
            key: annotation["atom_correspondence"][key]
            for key in atom
        },
        "reaction projection atom-correspondence declaration differs",
    )
    projection_bindings = projection["source_bindings"]
    _require(isinstance(projection_bindings, list), "reaction projection source_bindings must be an array")
    for index, raw in enumerate(projection_bindings):
        row = _exact(raw, _SOURCE_BINDING_FIELDS, f"reaction projection source_bindings[{index}]")
        top = bindings.get(row["binding_id"])
        _require(top == row, "reaction projection cites a changed or unknown source binding")


def _audit_retained_sources(
    annotation: dict[str, Any], *, bindings: dict[str, dict[str, Any]], resolved: dict[str, Path]
) -> None:
    _audit_rhea_sources(annotation, bindings=bindings, resolved=resolved)
    _audit_participant_structures(annotation, bindings=bindings, resolved=resolved)
    _audit_mcsa_source(annotation, bindings=bindings, resolved=resolved)
    _audit_computational_depiction(annotation, bindings=bindings, resolved=resolved)
    _audit_projection(annotation, bindings=bindings, resolved=resolved)


def validate_reaction_correspondence(
    sidecar: Any,
    *,
    bundle: dict[str, Any],
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Validate a reviewed correspondence sidecar against one draft bundle."""

    validate_source_drafts(bundle)
    value = _exact(sidecar, _TOP_LEVEL_FIELDS, "reaction-correspondence sidecar")
    _require(
        value["schema_version"] == REACTION_CORRESPONDENCE_SCHEMA_VERSION,
        "unsupported reaction-correspondence schema",
    )
    annotation_set_id = _string(value["annotation_set_id"], "annotation_set_id")
    batch_id = _string(value["batch_id"], "batch_id")
    _require(_BATCH_RE.fullmatch(batch_id) is not None, "batch_id is invalid")
    _require(bundle.get("bundle_id") == _expected_bundle_id(batch_id), "sidecar batch/bundle differs")
    _require(value["status"] == REACTION_CORRESPONDENCE_STATUS, "sidecar status overclaims")
    bindings, resolved = _validate_source_bindings(value["source_bindings"], repo_root=repo_root)
    review = _validate_review(
        value["review"], canonical_reaction_correspondence_payload_sha256(value)
    )
    records = {record["record_id"]: record for record in bundle["records"]}
    annotations = value["annotations"]
    _require(isinstance(annotations, list) and annotations, "annotations must be nonempty")
    observed_order: list[tuple[str, str]] = []
    annotation_ids: set[str] = set()
    record_ids: set[str] = set()
    for index, raw_annotation in enumerate(annotations):
        context = f"annotations[{index}]"
        annotation = _exact(raw_annotation, _ANNOTATION_FIELDS, context)
        annotation_id = _string(annotation["annotation_id"], f"{context}.annotation_id")
        _require(annotation_id not in annotation_ids, "annotation IDs repeat")
        annotation_ids.add(annotation_id)
        _require(
            annotation["annotation_kind"] == "curated_reaction_correspondence",
            f"{context}.annotation_kind is unsupported",
        )
        record_id, record = _bound_record(
            annotation["record_binding"], record_by_id=records,
            context=f"{context}.record_binding",
        )
        proposal = _bound_proposal(
            annotation["proposal_binding"], record=record,
            context=f"{context}.proposal_binding",
        )
        projection = _validate_projection_binding(
            annotation["projection_binding"], bindings=bindings,
            context=f"{context}.projection_binding",
        )
        reaction = _validate_curated_reaction(
            annotation["curated_reaction"], record=record,
            context=f"{context}.curated_reaction",
        )
        _validate_source_direction(
            annotation["source_direction"], record=record, proposal=proposal,
            reaction=reaction, context=f"{context}.source_direction",
        )
        _validate_terminal_depiction(
            annotation["terminal_depiction"], record=record, proposal=proposal,
            reaction=reaction,
            context=f"{context}.terminal_depiction",
        )
        atom_correspondence = _validate_atom_correspondence(
            annotation["atom_correspondence"],
            context=f"{context}.atom_correspondence",
        )
        _validate_limits_and_scope(annotation, record=record, context=context)
        excerpt = _validate_projection_excerpt(
            annotation["projection_excerpt"], binding_ids=set(bindings),
            context=f"{context}.projection_excerpt",
        )
        support_ids = {row["edge_id"] for row in excerpt["support_edges"]}
        _require(
            set(reaction["support_edge_ids"]) <= support_ids,
            f"{context}.curated_reaction cites unknown support edges",
        )
        direction_edges = {
            annotation["source_direction"]["record_cross_reference"]["support_edge_id"],
            annotation["source_direction"]["proposal_declared_direction"]["support_edge_id"],
        }
        _require(direction_edges <= support_ids, f"{context}.source_direction cites unknown support edges")
        _require(
            set(annotation["terminal_depiction"]["support_edge_ids"]) <= support_ids,
            f"{context}.terminal_depiction cites unknown support edges",
        )
        _require(
            set(atom_correspondence["support_edge_ids"]) <= support_ids,
            f"{context}.atom_correspondence cites unknown support edges",
        )
        source_binding_id, source_binding = _one_binding_of_kind(
            bindings, "source_record_snapshot"
        )
        _require(
            source_binding["sha256"]
            == annotation["record_binding"]["source_snapshot_sha256"],
            f"{context}.record_binding does not match {source_binding_id}",
        )
        if repo_root is not None:
            # The private helper key is never part of the sidecar.  It lets the
            # build-time audit reuse the already validated record without
            # widening the persisted annotation shape.
            audit_annotation = dict(annotation)
            audit_annotation["_record"] = record
            _audit_retained_sources(audit_annotation, bindings=bindings, resolved=resolved)
        observed_order.append((record_id, annotation_id))
        record_ids.add(record_id)
        _require(
            projection["sha256"] == bindings[projection["binding_id"]]["sha256"],
            f"{context}.projection_binding digest differs",
        )
    _require(
        observed_order == sorted(observed_order),
        "annotations must be deterministically ordered by record and annotation ID",
    )
    ordered_record_ids = [
        record["record_id"] for record in bundle["records"] if record["record_id"] in record_ids
    ]
    return {
        "schema_version": value["schema_version"],
        "annotation_set_id": annotation_set_id,
        "annotation_payload_sha256": value["review"]["annotation_payload_sha256"],
        "annotation_count": len(annotations),
        "record_count": len(record_ids),
        "record_ids": ordered_record_ids,
        "reviewed_on": review["reviewed_on"],
    }
