"""Project source-annotation projection and conservative comparison eligibility.

The projection contains the source-specific field mappings and chemical facts.
This consumer knows only references, observation kinds and comparison operations.
It does not admit records into the frozen Atlas kernel or repair source values.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
from typing import Any


SPEC_PATH = "data/atlas/perturbations/projection.json"
REVIEW_PATH = "data/atlas/perturbations/review.json"
KINDS = {"numeric", "nondetection", "unavailable", "source_conflict", "unassessed", "qualitative"}


def pointer(document: Any, path: str) -> Any:
    """Resolve a strict JSON pointer, including escaped source construct IDs."""
    if path == "":
        return document
    if not path.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {path}")
    for token in path[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(document, list):
            if not token.isdecimal() or str(int(token)) != token:
                raise ValueError(f"invalid array index in pointer: {path}")
            document = document[int(token)]
        elif isinstance(document, dict):
            document = document[token]
        else:
            raise ValueError(f"pointer traverses a scalar: {path}")
    return document


def _pick(document: Any, selector: dict[str, Any]) -> Any:
    if set(selector) == {"pointer"}:
        return deepcopy(pointer(document, selector["pointer"]))
    if set(selector) == {"literal"}:
        return deepcopy(selector["literal"])
    if set(selector) == {"first_present"}:
        for option in selector["first_present"]:
            try:
                return _pick(document, option)
            except KeyError:
                continue
        raise ValueError("no present field in selector")
    raise ValueError("selector must contain exactly one pointer or literal")


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _unique(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result = {item[key]: item for item in items}
    if len(result) != len(items):
        raise ValueError(f"duplicate {key}")
    return result


def _connectivity_relation(annotation: dict[str, Any], reaction: dict[str, Any],
                           binding: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    """Replay a reviewed partial drawing projection, without completing its chemistry.

    Locators and omitted chemical context require source review. The existing
    graph engine checks literal edits, not raster interpretation, valence, CIP,
    double-bond geometry, physical atom identity or a reaction mechanism.
    """
    from .atlas_transformations import replay_graph_edits

    if annotation.get("schema_version") != "catalytic-earth.source-connectivity-replay.v1":
        raise ValueError("unsupported source connectivity relation")
    fields = {"schema_version", "relation_id", "reaction_binding", "scope", "sources",
              "panel_correspondence", "edit_interpretation", "atom_locators", "atom_locator_scope",
              "boundary_attachments", "source_stereochemistry", "source_state_conflict", "limitations",
              "acquisition", "project_difference_id"}
    if set(annotation) != fields:
        raise ValueError("source connectivity relation fields differ")
    if not isinstance(annotation["relation_id"], str) or not annotation["relation_id"].strip():
        raise ValueError("connectivity relation requires an identity")
    expected = {**binding, "reaction_id": reaction["reaction_id"]}
    if annotation["reaction_binding"] != expected:
        raise ValueError("connectivity reaction binding differs")
    scope = annotation["scope"]
    withheld = {"full_atom_map", "balanced_reaction", "atom_stereochemistry",
                "double_bond_stereochemistry", "complete_hydrogen_inventory", "mechanism_path",
                "source_electron_flow", "radical_state", "full_valence",
                "external_boundary_bonds_in_graph", "map_unique_from_core_alone",
                "upstream_atom_map", "physical_atom_identity", "concerted_mechanism"}
    if (set(scope) != withheld | {"kind"}
            or scope["kind"] != "partial_source_depicted_connectivity"
            or any(scope[key] is not False for key in withheld)):
        raise ValueError("connectivity projection cannot establish complete chemistry or stereochemistry")
    witnesses = _unique(annotation["sources"], "source_id")
    available = _unique(source["sources"], "source_id")
    if not witnesses or any(available.get(key) != value for key, value in witnesses.items()):
        raise ValueError("connectivity source witnesses differ")
    stereo = annotation["source_stereochemistry"]
    if set(stereo) != {"input", "product", "source_product_labels", "mapped_atom_configurations",
                       "computed_target_selection", "source_product_observation_pointer",
                       "source_product_observation_context_id", "scope"}:
        raise ValueError("connectivity source stereochemistry fields differ")
    if any(key not in stereo or stereo[key] is not None
           for key in ("mapped_atom_configurations", "computed_target_selection")):
        raise ValueError("connectivity source context cannot assert mapped stereochemistry or target selection")
    product_observation = pointer(source, stereo["source_product_observation_pointer"])
    if (not isinstance(product_observation, dict)
            or product_observation.get("reaction_id") != reaction["reaction_id"]
            or not isinstance(stereo["source_product_observation_context_id"], str)
            or not stereo["source_product_observation_context_id"].strip()
            or product_observation.get("context_id") != stereo["source_product_observation_context_id"]):
        raise ValueError("connectivity product observation has a different reaction or context identity")
    participants = _unique(reaction["participants"], "participant_id")
    panel = annotation["panel_correspondence"]
    if set(panel) != {"before_graph", "after_graph", "graph_edits", "atom_map"}:
        raise ValueError("connectivity panel fields differ")
    for stage, side in (("before", "reactant"), ("after", "product")):
        graph = panel[stage + "_graph"]
        locators = _unique(annotation["atom_locators"][stage], "atom_id")
        if set(locators) != {atom["atom_id"] for atom in graph["atoms"]}:
            raise ValueError("connectivity locators must cover the complete selected graph")
        if {locator["participant_id"] for locator in locators.values()} != {
                key for key, value in participants.items() if value["side"] == side}:
            raise ValueError("connectivity locators do not cover the source reaction participants")
        for locator in locators.values():
            participant = participants.get(locator["participant_id"])
            if (participant is None or participant["side"] != side
                    or locator["source_id"] not in witnesses
                    or not isinstance(locator["description"], str) or not locator["description"].strip()):
                raise ValueError("connectivity locator has an unbound participant, side or source")
        if any(atom["stereochemistry"] is not None for atom in graph["atoms"]):
            raise ValueError("connectivity-only graph cannot carry atom stereochemistry")
    edits = panel["graph_edits"]
    difference_id = annotation["project_difference_id"]
    if (not isinstance(difference_id, str) or not difference_id.startswith("project-difference:")
            or any(edit["source_flow_id"] != difference_id for edit in edits)):
        raise ValueError("connectivity edits require the declared project-difference locator, not source arrows")
    if any(edit["operation"] not in {"add_bond", "remove_bond", "set_bond_order"} for edit in edits):
        raise ValueError("connectivity-only replay permits bond edits only")
    if not replay_graph_edits(panel["before_graph"], edits, panel["after_graph"], panel["atom_map"]):
        raise ValueError("connectivity edits do not reproduce the declared source product projection")
    mapping = {row["before_atom_id"]: row["after_atom_id"] for row in panel["atom_map"]}
    boundaries = _unique(annotation["boundary_attachments"], "boundary_id")
    if not boundaries:
        raise ValueError("partial connectivity requires source-reviewed boundary anchors")
    for boundary in boundaries.values():
        if (not isinstance(boundary["before_atom_id"], str)
                or not isinstance(boundary["after_atom_id"], str)
                or boundary["before_atom_id"] not in mapping
                or boundary["after_atom_id"] not in mapping.values()
                or mapping[boundary["before_atom_id"]] != boundary["after_atom_id"]
                or boundary["source_id"] not in witnesses
                or not isinstance(boundary["external_group_description"], str)
                or not boundary["external_group_description"].strip()
                or type(boundary["order"]) is not int or boundary["order"] not in {1, 2, 3}):
            raise ValueError("connectivity boundary anchor differs from the mapped source projection")
    anchored = [boundary["before_atom_id"] for boundary in boundaries.values()]
    before_locators = _unique(annotation["atom_locators"]["before"], "atom_id")
    if (len(set(anchored)) != len(anchored)
            or {before_locators[atom]["participant_id"] for atom in anchored} != {
                key for key, value in participants.items() if value["side"] == "reactant"}):
        raise ValueError("connectivity boundary anchors must be distinct and cover each input participant")
    return {"source_annotation": deepcopy(annotation), "replay_verified": True,
            "source_product_observation": deepcopy(product_observation),
            "verification_scope": "Literal selected-graph replay under a source-reviewed project map; no complete chemistry or stereochemical inference.",
            "computed_atom_stereochemistry": None, "computed_product_stereoisomer": None,
            "map_uniqueness_established": False}


def compare(rows: dict[str, dict[str, Any]], request: dict[str, Any]) -> dict[str, Any]:
    """Return an eligible descriptive comparison or explicit abstention.

    Identical names, units or sequences do not authorize a cross-study assay join.
    Missing exact sequences do not preclude a source-defined within-study contrast.
    """
    operation = request["operation"]
    roles_required = {
        "ratio": {"numerator", "denominator"},
        "preference": {"numerator", "denominator"},
        "multiplicative": {"parent", "A", "B", "double"},
        "unassessed": set(),
    }
    if operation not in roles_required or set(request["roles"]) != roles_required[operation]:
        raise ValueError("unknown comparison operation or incomplete roles")
    assessment_fields = ("source_discriminant_assessed", "arithmetic_requested")
    if any(field in request for field in assessment_fields):
        if (any(type(request.get(field)) is not bool for field in assessment_fields)
                or operation != "unassessed" or request["arithmetic_requested"]):
            raise ValueError("context assessment requires two booleans and unrequested arithmetic")
    source_assessed = request.get("source_discriminant_assessed") is True
    selected = {role: rows[row_id] for role, row_id in request["roles"].items()}
    reasons = list(request.get("source_blocks", []))
    if operation == "unassessed":
        reasons.append("arithmetic_not_requested" if source_assessed
                       else "matched_perturbation_control_unassessed")
    values = list(selected.values())
    if any(row["study_id"] != request["study_id"] for row in values):
        reasons.append("request_study_differs_from_observations")
    equal_fields = ["study_id", "assay_id", "endpoint_kind", "parameter", "unit", "reaction_direction", "reaction_id"]
    if operation != "preference":
        equal_fields.extend(["substrate_id", "background_id"])
    else:
        equal_fields.append("construct_id")
    for field in equal_fields:
        field_values = [row.get(field) if field == "reaction_id" else row[field] for row in values]
        if field_values and any(value != field_values[0] for value in field_values[1:]):
            reasons.append(f"mismatched_{field}")
    for row in values:
        if row["result_kind"] != "numeric":
            reasons.append(f"{row['result_kind']}:{row['id']}")
        elif not _number(row["value"]) or row["value"] < 0:
            reasons.append(f"invalid_numeric_value:{row['id']}")
        if not row["assay_qualified"]:
            reasons.append(f"unresolved_assay:{row['id']}")
        if row["unit"] is None:
            reasons.append(f"unresolved_unit:{row['id']}")
        reasons.extend(row["comparison_blocks"])
    if operation == "ratio" and len(selected) == 2:
        numerator, denominator = selected["numerator"], selected["denominator"]
        if denominator["construct_id"] != numerator["background_id"]:
            reasons.append("control_is_not_declared_perturbation_background")
        if not numerator["perturbation"] or denominator["perturbation"]:
            reasons.append("not_a_mutant_over_unperturbed_background_contrast")
    if operation == "multiplicative":
        parent, a, b, double = (selected[key] for key in ("parent", "A", "B", "double"))
        pa, pb = set(a["perturbation"]), set(b["perturbation"])
        if (parent["perturbation"] or parent["construct_id"] != a["background_id"]
                or len(pa) != 1 or len(pb) != 1 or pa & pb
                or set(double["perturbation"]) != pa | pb):
            reasons.append("incomplete_or_mismatched_perturbation_square")
    if operation == "preference":
        if len({row["substrate_id"] for row in values}) != 2:
            reasons.append("preference_requires_distinct_substrate_states")
        if not request.get("substrate_pair_source"):
            reasons.append("unbound_substrate_pair")
    result = {
        **deepcopy(request), "eligible": False, "reasons": sorted(set(reasons)),
        "value": None, "unit": "dimensionless", "uncertainty": None,
        "interpretation_limit": "Source-rounded descriptive arithmetic only; no significance, equivalence, causal chemical role, pooled activity ranking or design-success estimate.",
    }
    if operation == "unassessed":
        result["unit"] = None
        result["interpretation_limit"] = (
            "Source-scoped control discrimination was assessed; no scalar comparison was requested or computed. Interpretation remains limited by the attached source evidence."
            if source_assessed else
            "No matched perturbation comparison was evaluated; an unassessed control is neither a measured effect nor nondetection."
        )
    if reasons:
        return result
    if operation in {"ratio", "preference"}:
        denominator = selected["denominator"]["value"]
        if denominator <= 0:
            result["reasons"] = ["nonpositive_denominator"]
            return result
        result["value"] = selected["numerator"]["value"] / denominator
        if operation == "preference":
            if result["value"] == 1:
                result["preferred_substrate_id"] = None
            else:
                role = "numerator" if result["value"] > 1 else "denominator"
                result["preferred_substrate_id"] = selected[role]["substrate_id"]
    elif operation == "multiplicative":
        if any(selected[key]["value"] <= 0 for key in ("parent", "A", "B")):
            result["reasons"] = ["nonpositive_multiplicative_reference"]
            return result
        expected = selected["A"]["value"] * selected["B"]["value"] / selected["parent"]["value"]
        result["expected_double"] = expected
        result["value"] = selected["double"]["value"] / expected
    result["eligible"] = True
    return result


def control_relation(context, resolve):
    """Compare two source-bound systems without assigning genetic or causal roles.

    The source review supplies the condition vectors and normalization meaning.
    Equality here checks those declarations, not every physical property of the
    preparations or their effective reactive-phase concentrations.
    """
    if (context.get("schema_version") != "catalytic-earth.system-control-relation.v1"
            or context.get("operation") != "system_ratio"
            or set(context.get("arms", {})) != {"numerator", "denominator"}):
        raise ValueError("unsupported system control relation")
    if type(context["source_qualified"]) is not bool:
        raise ValueError("system control qualification must be boolean")
    reported = context["source_reported_ratio"]
    if ((reported is None) != (context["source_reported_ratio_locator"] is None)
            or (reported is not None and
                (not _number(reported) or reported < 0 or not context["source_reported_ratio_locator"]))):
        raise ValueError("source-reported ratio requires a finite value and locator")
    reasons = list(context["source_blocks"])
    if not context["source_qualified"]:
        reasons.append("source_comparison_unqualified")
    evidence = [resolve(ref) for ref in context["evidence"]]
    if not evidence or not context["interpretation_limit"]:
        raise ValueError("system control requires source evidence and interpretation limit")
    arms = {}
    for role, arm in context["arms"].items():
        if (type(arm["assay_qualified"]) is not bool
                or len({arm[key]["source"] for key in
                        ("observation_provider", "system_provider", "assay_provider")}) != 1):
            raise ValueError("system control arm must use one source and explicit assay qualification")
        row = resolve(arm["observation_provider"])
        system = resolve(arm["system_provider"])
        assay = resolve(arm["assay_provider"])
        identity_field = arm["system_identity_field"]
        if (identity_field not in {"system_id", "construct_id"}
                or row["row_id"] != arm["source_row_id"]
                or row[identity_field] != system[identity_field]
                or row["assay_id"] != assay["assay_id"]):
            raise ValueError("system control row, system or assay identity differs")
        parameter = pointer(row, arm["parameter_pointer"])
        if parameter["parameter"] != arm["parameter"]:
            raise ValueError("system control parameter identity differs")
        kind, value, unit = (parameter[key] for key in ("status", "value", "unit"))
        if kind not in KINDS:
            raise ValueError("unknown system control result kind")
        if kind != "numeric":
            if value is not None:
                raise ValueError("nonnumeric system control cannot carry a numeric value")
            reasons.append(f"{kind}:{role}")
        elif not _number(value) or value < 0 or not unit:
            reasons.append(f"invalid_numeric_parameter:{role}")
        error = parameter["uncertainty"]
        if (error["unreported_is_zero"] is not False
                or (error["value"] is not None and
                    (not _number(error["value"]) or error["value"] < 0
                     or error["kind"] in {None, "not_reported"}))):
            raise ValueError("invalid system control uncertainty")
        required = {"study_id", "substrate_id", "reaction_direction", "endpoint", "normalization"}
        invariant = arm["reviewed_invariants"]
        if set(invariant) != required or any(not invariant[key] for key in required):
            raise ValueError("system control requires explicit comparison invariants")
        if invariant["study_id"] != context["study_id"]:
            reasons.append(f"mismatched_study_id:{role}")
        if not arm["assay_qualified"]:
            reasons.append(f"unresolved_assay:{role}")
        if set(arm["invariant_evidence"]) != {"substrate", "normalization"}:
            raise ValueError("system control requires substrate and normalization evidence")
        if any(ref["source"] != arm["observation_provider"]["source"]
               for ref in arm["invariant_evidence"].values()):
            raise ValueError("system control invariant evidence must use the arm source")
        invariant_evidence = {key: resolve(ref) for key, ref in arm["invariant_evidence"].items()}
        if any(not value for value in invariant_evidence.values()):
            raise ValueError("empty system control invariant evidence")
        selected = {"system": system, "assay": assay, "observation": row, "parameter": parameter}
        # Concrete condition values come from the original source objects. Their
        # chemical interpretation still requires the enclosing source review.
        conditions = {}
        for key, selector in arm["condition_fields"].items():
            if set(selector) != {"pointer"} or not selector["pointer"].startswith("/system/"):
                raise ValueError("system condition requires a source system pointer")
            conditions[key] = _pick(selected, selector)
        arms[role] = {**deepcopy(arm), "source_observation": row,
                      "source_system": system, "source_assay": assay,
                      "source_parameter": parameter, "condition_vector": conditions,
                      "resolved_invariant_evidence": invariant_evidence}
    numerator, denominator = arms["numerator"], arms["denominator"]
    for field in ("condition_fields", "parameter_pointer", "system_identity_field"):
        if numerator[field] != denominator[field]:
            reasons.append(f"mismatched_{field}")
    for field in numerator["reviewed_invariants"]:
        if numerator["reviewed_invariants"][field] != denominator["reviewed_invariants"][field]:
            reasons.append(f"mismatched_{field}")
    for field in ("parameter", "unit"):
        if numerator["source_parameter"][field] != denominator["source_parameter"][field]:
            reasons.append(f"mismatched_{field}")
    # A common nominal protocol is a source-scoped association, not specimen identity.
    if numerator["assay_provider"] != denominator["assay_provider"]:
        reasons.append("mismatched_assay_provider")
    if numerator["observation_provider"]["source"] != denominator["observation_provider"]["source"]:
        reasons.append("cross_source_observations")
    for field in ("substrate", "normalization"):
        if (numerator["invariant_evidence"][field] != denominator["invariant_evidence"][field]
                or numerator["resolved_invariant_evidence"][field] != denominator["resolved_invariant_evidence"][field]):
            reasons.append(f"mismatched_{field}_evidence")
    states = [arm["condition_vector"] for arm in (numerator, denominator)]
    changed, held = context["changed_axes"], context["held_constant_axes"]
    if (not changed or len(set(changed)) != len(changed) or len(set(held)) != len(held)
            or set(changed) & set(held) or set(states[0]) != set(states[1])
            or set(changed) | set(held) != set(states[0])):
        raise ValueError("system control axes must partition the declared condition vector")
    actual = {key for key in states[0] if states[0][key] != states[1][key]}
    if actual != set(changed):
        reasons.append("declared_condition_changes_differ")
    value = None
    if not reasons:
        if denominator["source_parameter"]["value"] <= 0:
            reasons.append("nonpositive_denominator")
        else:
            value = numerator["source_parameter"]["value"] / denominator["source_parameter"]["value"]
            if not math.isfinite(value):
                reasons.append("nonfinite_ratio")
                value = None
    return {**deepcopy(context), "arms": arms, "source_evidence": evidence,
            "eligible": not reasons, "reasons": sorted(set(reasons)), "value": value,
            "unit": "dimensionless", "uncertainty": None,
            "causal_component_established": False, "physical_condition_equality_established": False}


def _model_link(context, link, constructs, rows, assays, source_bindings, resolve):
    """Bind source-model transitions to evidence without inventing atomic steps.

    The source review supplies transition meaning. These checks enforce its
    exact directional parameter references, state observations and identity
    scope; they cannot authenticate chemistry from labels or fitted numbers.
    """
    if context.get("schema_version") != "catalytic-earth.source-model-context.v1":
        raise ValueError("unsupported source-model context")
    construct = constructs[link["construct_id"]]

    def ref(local):
        binding = context["source_bindings"][local["provider"]]
        matches = [key for key, value in source_bindings.items() if value == binding]
        if len(matches) != 1:
            raise ValueError("model provider must match one bound source")
        return {"source": matches[0], "pointer": local["pointer"]}

    def get(local):
        return resolve(ref(local))

    expected = {"construct": construct["source_construct_id"], "study": context["study"]["doi"]}
    if context["study"]["reported_variant"] != expected["construct"]:
        raise ValueError("model construct identity differs")
    identities = context["identity_bindings"]
    if {(item["provider"], item["identity_kind"]) for item in identities} != {
            (provider, kind) for provider in context["source_bindings"] for kind in expected}:
        raise ValueError("model requires source study and construct identities")
    if any(get(item) != expected[item["identity_kind"]] for item in identities):
        raise ValueError("model source identity differs")
    model = context["source_model"]
    if (any(model[key] is not False for key in
            ("elementary_step_sequence_established", "complete_reacted_graph_established",
             "equilibrium_constant_transfer_between_assays_established", "graph_replay_verified"))
            or model["before_state_atom_map"] is not None):
        raise ValueError("source-model links cannot establish elementary chemistry or replay")
    states = _unique(model["states"], "state_id")
    transitions = _unique(model["transitions"], "transition_id")
    # A reaction branch follows an input into chemically different products;
    # its identity is not the identity of the ligand present in each state.
    reaction_branch = "reaction_branch_bindings" in context
    if reaction_branch and "ligand_bindings" in context:
        raise ValueError("model cannot mix ligand and reaction-branch identity declarations")
    branch_key = "reaction_branch_id" if reaction_branch else "ligand_id"
    other_key = "ligand_id" if reaction_branch else "reaction_branch_id"
    ligands = context.get("reaction_branch_bindings" if reaction_branch else "ligand_bindings", {})
    for item in ligands.values():
        if get(item["binding"]) != item["source_name"]:
            raise ValueError("model ligand differs from its source identity")
    if ligands and any(state.get(branch_key) not in ligands for state in states.values()):
        raise ValueError("model states require bound ligand identities")
    fits = _unique(model.get("fit_models", []), "fit_id")
    if any(other_key in item for item in [*states.values(), *transitions.values(), *fits.values()]):
        raise ValueError("model cannot mix ligand and reaction-branch state identities")
    if fits and (not context.get("enzyme_identity_binding")
                 or get(context["enzyme_identity_binding"]) != context["study"]["reported_enzyme"]):
        raise ValueError("model enzyme differs from its source identity")
    if not ligands and (fits or any(branch_key in item for item in [*states.values(), *transitions.values()])):
        raise ValueError("model ligand declarations require source bindings")
    resolved_fits = []
    for fit in fits.values():
        covered = fit["transition_ids"]
        phase = fit["phase_transition_ids"]
        if (not covered or len(covered) != len(set(covered)) or not set(covered) <= set(transitions)
                or len(phase) != len(set(phase)) or not set(phase) <= set(covered)):
            raise ValueError("model fit requires distinct declared transitions and a contained phase")
        if fit["kind"] == "multistep_reporter_response":
            if len(phase) < 2 or any(transitions[left]["to_state"] != transitions[right]["from_state"]
                                     for left, right in zip(phase, phase[1:])):
                raise ValueError("multistep reporter phase requires a connected path of multiple transitions")
        elif fit["kind"] == "two_state_equilibrium":
            if len(covered) != 1 or phase or transitions[covered[0]]["reversible_in_source"] is not True:
                raise ValueError("two-state equilibrium fit requires one reversible transition")
        elif fit["kind"] == "steady_state_population_inference":
            if (covered != phase or len(phase) < 2
                    or any(transitions[left]["to_state"] != transitions[right]["from_state"]
                           for left, right in zip(phase, phase[1:]))):
                raise ValueError("steady-state population inference requires one connected ordered phase")
            basis = fit.get("inference_basis")
            basis_fields = {
                "steady_state", "substrate_regime", "turnover_and_population_inputs",
                "source_equations", "raw_population_fractions_available",
                "forward_net_rate_definition", "direct_microscopic_rates_established",
            }
            equations = basis.get("source_equations") if isinstance(basis, dict) else None
            if (not isinstance(basis, dict) or set(basis) != basis_fields
                    or basis["steady_state"] is not True
                    or basis["turnover_and_population_inputs"] is not True
                    or basis["direct_microscopic_rates_established"] is not False
                    or type(basis["raw_population_fractions_available"]) is not bool
                    or any(not isinstance(basis[field], str) or not basis[field].strip()
                           for field in ("substrate_regime", "forward_net_rate_definition"))
                    or not isinstance(equations, list) or not equations
                    or any(not isinstance(equation, str) or not equation.strip()
                           for equation in equations)
                    or len({equation.strip() for equation in equations}) != len(equations)):
                raise ValueError("steady-state population inference requires its exact source inference basis")
            for transition_id in covered:
                transition = transitions[transition_id]
                slots = transition.get("parameter_slots", {})
                if (set(slots) != {"forward", "reverse"}
                        or any(slot.get("status") != "unassigned_in_selected_source_model"
                               for slot in slots.values())
                        or transition.get("parameter_roles") or transition.get("parameter_units")):
                    raise ValueError("steady-state population inference cannot assign directional transition rates")
        else:
            raise ValueError("unsupported source-model fit kind")
        assay_ref = ref(fit["assay_binding"])
        if any(ref(transitions[key]["assay_binding"]) != assay_ref for key in covered):
            raise ValueError("model fit cannot combine transitions from different assays")
        if ligands and any(transitions[key].get(branch_key) != fit[branch_key] for key in covered):
            raise ValueError("model fit cannot combine different ligand branches")
        parameters = {}
        if fit["kind"] == "two_state_equilibrium":
            roles = {"apparent_equilibrium_constant": {"M", "mM", "uM"}}
        elif fit["kind"] == "steady_state_population_inference":
            roles = {"steady_state_turnover_rate": {"s^-1"}, "forward_net_rate": {"s^-1"}}
        else:
            roles = {"saturated_multistep_rate": {"s^-1"},
                     "observed_second_order_initial_rate": {"M^-1 s^-1"},
                     "cooperative_response_midpoint": {"M", "mM", "uM"},
                     "hill_coefficient": {"dimensionless"}}
        for key, item in fit["parameter_bindings"].items():
            value = get(item["binding"])
            if (item["role"] not in roles or item["unit"] not in roles[item["role"]]
                    or value["unit"] != item["unit"] or value["parameter"] != key):
                raise ValueError("model fit parameter requires source role, name and matching unit")
            if fit["kind"] == "steady_state_population_inference":
                affected = item.get("affected_transition_ids")
                if (set(item) != {"binding", "role", "unit", "affected_transition_ids"}
                        or not isinstance(affected, list) or not affected
                        or any(not isinstance(transition_id, str) for transition_id in affected)
                        or len(affected) != len(set(affected)) or not set(affected) <= set(phase)):
                    raise ValueError("population-inferred parameter requires distinct affected phase transitions")
            parameters[key] = value
        if not parameters:
            raise ValueError("model fit requires bound source parameters")
        if fit["kind"] == "steady_state_population_inference":
            turnover = [item for item in fit["parameter_bindings"].values()
                        if item["role"] == "steady_state_turnover_rate"]
            net_rates = [item for item in fit["parameter_bindings"].values()
                         if item["role"] == "forward_net_rate"]
            net_transitions = [item["affected_transition_ids"][0] for item in net_rates
                               if len(item["affected_transition_ids"]) == 1]
            if (len(turnover) != 1 or turnover[0]["affected_transition_ids"] != phase
                    or len(net_rates) != len(phase) or len(net_transitions) != len(net_rates)
                    or len(set(net_transitions)) != len(net_transitions)
                    or set(net_transitions) != set(phase)):
                raise ValueError(
                    "population inference requires one turnover rate and one net rate per phase transition")
        if any(item["role"] == "observed_second_order_initial_rate"
               for item in fit["parameter_bindings"].values()):
            boundary = fit.get("measurement_boundary", {})
            if (len(parameters) != 1
                    or set(boundary) != {"from_state", "to_state"} or covered != phase
                    or boundary["from_state"] != transitions[phase[0]]["from_state"]
                    or boundary["to_state"] != transitions[phase[-1]]["to_state"]):
                raise ValueError("initial-rate fit must cover exactly its declared measurement boundary")
        resolved_fits.append({**deepcopy(fit), "resolved_parameters": parameters,
                              "assay": resolve(assay_ref)})
    resolved_transitions = []
    for transition in transitions.values():
        if (transition["from_state"] not in states or transition["to_state"] not in states
                or transition["from_state"] == transition["to_state"]):
            raise ValueError("model transition requires distinct declared states")
        if ligands and (transition.get(branch_key) not in ligands or any(
                states[transition[key]][branch_key] != transition[branch_key]
                for key in ("from_state", "to_state"))):
            raise ValueError("model transition cannot cross ligand branches")
        slots = transition["parameter_slots"]
        if set(slots) != {"forward", "reverse"}:
            raise ValueError("model requires explicit forward and reverse parameter slots")
        bound_directions = {key for key, slot in slots.items() if slot["status"] == "bound_source_parameter"}
        if bound_directions and (ligands or "parameter_roles" in transition or "parameter_units" in transition):
            if (set(transition.get("parameter_roles", {})) != bound_directions
                    or set(transition.get("parameter_units", {})) != bound_directions):
                raise ValueError("model bound directions require complete kinetic roles and units")
        parameters = {}
        for direction, slot in slots.items():
            if slot["is_zero"] is not False:
                raise ValueError("an unassigned model parameter is not zero")
            if slot["status"] == "unassigned_in_selected_source_model":
                if set(slot) != {"status", "binding", "is_zero", "reason"} or slot["binding"] is not None or not slot["reason"]:
                    raise ValueError("unassigned model parameter requires an explicit abstention")
                parameters[direction] = None
            elif slot["status"] == "bound_source_parameter":
                if set(slot) != {"status", "binding", "is_zero"} or not slot["binding"]:
                    raise ValueError("model parameter requires an exact source binding")
                if direction == "reverse" and transition["reversible_in_source"] is not True:
                    raise ValueError("reverse parameter requires a reversible source transition")
                parameters[direction] = get(slot["binding"])
                if "parameter_units" in transition and parameters[direction]["unit"] != transition["parameter_units"][direction]:
                    raise ValueError("model directional parameter unit differs")
                if "parameter_roles" in transition:
                    role_units = {"second_order_association": {"M^-1 s^-1", "mM^-1 s^-1"},
                                  "first_order_dissociation": {"s^-1"}}
                    role = transition["parameter_roles"][direction]
                    if role not in role_units or parameters[direction]["unit"] not in role_units[role]:
                        raise ValueError("model directional role differs from its kinetic order")
                if any(slot["binding"] == item["binding"] for fit in fits.values()
                       for item in fit["parameter_bindings"].values()):
                    raise ValueError("fit-level parameter cannot become an individual transition rate")
            else:
                raise ValueError("unknown model parameter status")
        resolved_transitions.append({**deepcopy(transition), "resolved_parameters": parameters,
            "direction_endpoints": {"forward": [transition["from_state"], transition["to_state"]],
                                    "reverse": [transition["to_state"], transition["from_state"]]
                                    if transition["reversible_in_source"] else None},
            "missing_parameter_is_zero": False})
    ids = link["observation_ids"]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("model link requires unique existing observations")
    if any(row_id not in rows or rows[row_id]["construct_id"] != link["construct_id"]
           or rows[row_id]["study_id"] != link["study_id"] for row_id in ids):
        raise ValueError("model observation study or construct differs")
    endpoints = _unique(context["endpoint_relations"], "relation_id")
    if {item["observation_id"] for item in endpoints.values()
            if item["observation_id"] is not None} != set(ids):
        raise ValueError("model observation coverage differs")
    resolved_endpoints = []
    original_assays = {}
    for endpoint in endpoints.values():
        original = None
        if "original_observation_binding" in endpoint:
            original = get(endpoint["original_observation_binding"])
            if original["observation_id"] != endpoint["original_observation_id"]:
                raise ValueError("model original observation identity differs")
        elif (context["deposit_association"] is not None or endpoint["observation_id"] is None
              or "original_observation_id" in endpoint):
            raise ValueError("model endpoint requires original evidence or an existing projected observation")
        if sum(key in endpoint for key in ("transition_id", "state_id", "fit_id")) != 1:
            raise ValueError("model endpoint must identify one transition, state or fit")
        if "transition_id" in endpoint:
            if endpoint["kind"] != "transition_parameter":
                raise ValueError("state observations are not transition parameters")
            transition = transitions[endpoint["transition_id"]]
            direction = endpoint["transition_direction"]
            if direction not in {"forward", "reverse"}:
                raise ValueError("model parameter direction is invalid")
            parameter = {"provider": endpoint["provider"], "pointer": endpoint["parameter_pointer"]}
            slot = transition["parameter_slots"][direction]
            if slot["status"] != "bound_source_parameter" or slot["binding"] != parameter:
                raise ValueError("parameter is not bound to this transition and direction")
            assay_ref = ref({"provider": endpoint["provider"], "pointer": endpoint["assay_pointer"]})
            if "assay_binding" in transition and ref(transition["assay_binding"]) != assay_ref:
                raise ValueError("model transition assay differs from its parameter")
            if original is not None:
                original_id = endpoint["original_observation_id"]
                if original_id in original_assays and original_assays[original_id] != assay_ref:
                    raise ValueError("one original observation cannot acquire different assays")
                original_assays[original_id] = assay_ref
            resolved = {"parameter": get(parameter), "assay": resolve(assay_ref)}
        elif "fit_id" in endpoint:
            if endpoint["kind"] != "fit_parameter" or endpoint["fit_id"] not in fits:
                raise ValueError("model endpoint requires a declared fit")
            fit = fits[endpoint["fit_id"]]
            parameter = {"provider": endpoint["provider"], "pointer": endpoint["parameter_pointer"]}
            if (endpoint["parameter_key"] not in fit["parameter_bindings"]
                    or fit["parameter_bindings"][endpoint["parameter_key"]]["binding"] != parameter):
                raise ValueError("parameter is not bound to this model fit")
            assay_ref = ref({"provider": endpoint["provider"], "pointer": endpoint["assay_pointer"]})
            if assay_ref != ref(fit["assay_binding"]):
                raise ValueError("model fit assay differs from its parameter")
            resolved = {"parameter": get(parameter), "assay": resolve(assay_ref)}
        else:
            if endpoint["kind"] != "state_observation":
                raise ValueError("transition parameters are not state observations")
            state = states[endpoint["state_id"]]
            if endpoint["projected_parameter"] not in state.get("observation_bindings", []):
                raise ValueError("observation is not bound to this source-model state")
            resolved = {"source_observation": get(
                {"provider": endpoint["provider"], "pointer": endpoint["observation_pointer"]})}
            if resolved["source_observation"] != original:
                raise ValueError("model state observation differs from original observation")
        row_id = endpoint["observation_id"]
        if row_id is not None:
            parameter_ref = ref(endpoint["projected_parameter"])
            if parameter_ref != rows[row_id]["parameter_provider"]:
                raise ValueError("model endpoint differs from the exact existing observation")
            if endpoint["kind"] in {"transition_parameter", "fit_parameter"} and parameter_ref != ref(parameter):
                raise ValueError("model parameter differs from its projected observation")
            if endpoint["kind"] in {"transition_parameter", "fit_parameter"} and assay_ref != assays[rows[row_id]["assay_id"]]["provider"]:
                raise ValueError("model assay differs from the existing parameter observation")
            target = (transitions[endpoint["transition_id"]] if "transition_id" in endpoint
                      else fits[endpoint["fit_id"]] if "fit_id" in endpoint else states[endpoint["state_id"]])
            if ligands and target[branch_key] != rows[row_id]["substrate_id"]:
                raise ValueError("model ligand differs from the existing observation")
        resolved_endpoints.append({**deepcopy(endpoint), **resolved})
    bound_slots = {(key, direction, slot["binding"]["provider"], slot["binding"]["pointer"])
                   for key, transition in transitions.items()
                   for direction, slot in transition["parameter_slots"].items()
                   if slot["status"] == "bound_source_parameter"}
    bound_endpoints = [(item["transition_id"], item["transition_direction"], item["provider"], item["parameter_pointer"])
                       for item in endpoints.values() if item["kind"] == "transition_parameter"]
    if set(bound_endpoints) != bound_slots or len(bound_endpoints) != len(bound_slots):
        raise ValueError("every bound transition parameter requires exactly one endpoint relation")
    fit_slots = {(key, name, item["binding"]["provider"], item["binding"]["pointer"])
                 for key, fit in fits.items() for name, item in fit["parameter_bindings"].items()}
    fit_endpoints = [(item["fit_id"], item["parameter_key"], item["provider"], item["parameter_pointer"])
                     for item in endpoints.values() if item["kind"] == "fit_parameter"
                     and item["observation_id"] is not None]
    if set(fit_endpoints) != fit_slots or len(fit_endpoints) != len(fit_slots):
        raise ValueError("every fit parameter requires exactly one existing projected endpoint")
    contextual_output = {}
    if "context_evidence_bindings" in context:
        contextual = _unique(context["context_evidence_bindings"], "evidence_id")
        resolved_context = []
        for item in contextual.values():
            if (not isinstance(item["evidence_id"], str) or not item["evidence_id"].strip()
                    or not item["transition_ids"] and not item["fit_ids"]
                    or len(item["transition_ids"]) != len(set(item["transition_ids"]))
                    or len(item["fit_ids"]) != len(set(item["fit_ids"]))
                    or not set(item["transition_ids"]) <= set(transitions)
                    or not set(item["fit_ids"]) <= set(fits)):
                raise ValueError("model contextual evidence requires declared transition or fit references")
            evidence = get(item["binding"])
            if not isinstance(evidence, dict) or not evidence:
                raise ValueError("model contextual evidence requires a source object, not a bare scalar")
            resolved_context.append({**deepcopy(item), "evidence": evidence})
        contextual_output["context_evidence"] = resolved_context
    association = context["deposit_association"]
    if association is None:
        absence_reason = context.get("deposit_absence_reason")
        if (not isinstance(absence_reason, str) or not absence_reason.strip()
                or any(state.get("arrangement_bindings") for state in states.values())
                or any(transition["bond_annotations"] for transition in transitions.values())):
            raise ValueError("absent model arrangement requires a reason and no deposited atom bindings")
        return {**deepcopy(link), **contextual_output, "source_context": deepcopy(context),
                "transitions": resolved_transitions, "endpoints": resolved_endpoints,
                "fit_models": resolved_fits, "arrangement": None,
                "existing_state_observation_relations": [],
                "identity_scope": "source-reported construct association; exact sequence/preparation not established",
                "verification_scope": "Source-pinned identity, transition/fit scope and evidence references; no chemical graph or causal validation."}
    arrangement_ref = {"provider": association["provider"], "pointer": association["arrangement_pointer"]}
    if arrangement_ref not in states[association["source_model_state_id"]].get("arrangement_bindings", []):
        raise ValueError("arrangement is not bound to this source-model state")
    if any(association[key] is not False for key in
           ("exact_preparation_identity_established", "solution_conformer_identity_established",
            "geometry_to_rate_causation_established")):
        raise ValueError("source-model association cannot promote physical identity or cause")
    arrangement = get(arrangement_ref)
    atom_map = _unique(association["atom_correspondence"], "source_atom_label")
    _unique(association["atom_correspondence"], "deposit_atom_id")
    bond_annotations = _unique(association["bond_annotations"], "role")
    for transition in transitions.values():
        for bond in transition["bond_annotations"]:
            labels = bond["source_atom_labels"]
            if (any(label not in atom_map for label in labels)
                    or bond["role"] not in bond_annotations
                    or [atom_map[label]["deposit_atom_id"] for label in labels]
                    != bond_annotations[bond["role"]]["atom_ids"]):
                raise ValueError("model transition bond differs from source/deposit correspondence")
    for bond in association["bond_annotations"]:
        dictionary = get({"provider": association["provider"], "pointer": bond["dictionary_bond_pointer"]})
        metric = get({"provider": association["provider"], "pointer": bond["coordinate_metric_pointer"]})
        if dictionary["atom_ids"] != bond["atom_ids"] or metric["atom_ids"] != bond["atom_ids"]:
            raise ValueError("model bond locator differs from the bound arrangement")
    relations = [get({"provider": association["provider"], "pointer": p})
                 for p in association["existing_relation_pointers"]]
    _unique(relations, "observation_id")
    if ({item["observation_id"] for item in relations}
            != {item["original_observation_id"] for item in endpoints.values()}
            or any(item["arrangement_id"] != association["arrangement_id"] for item in relations)):
        raise ValueError("model differs from original arrangement/observation relations")
    return {**deepcopy(link), **contextual_output, "source_context": deepcopy(context),
            "transitions": resolved_transitions, "endpoints": resolved_endpoints,
            **({"fit_models": resolved_fits} if fits else {}),
            "arrangement": arrangement,
            "existing_state_observation_relations": relations,
            "identity_scope": "source-reported construct association; exact sequence/preparation not established",
            "verification_scope": "Source-pinned identity, transition direction and evidence references; no chemical graph or causal validation."}


def _project_candidate(repo_root: Path, spec: dict[str, Any] | None = None) -> dict[str, Any]:
    """Internal development projection; its arithmetic has no reviewed authority."""
    repo_root = repo_root.resolve()
    if spec is None:
        spec = json.loads((repo_root / SPEC_PATH).read_text(encoding="utf-8"))
    if spec.get("schema_version") != "catalytic-earth.perturbation-projection.v1":
        raise ValueError("unsupported perturbation projection")
    sources = {}
    for source_id, binding in spec["sources"].items():
        path = (repo_root / binding["path"]).resolve()
        if not path.is_relative_to(repo_root):
            raise ValueError("source path escapes repository")
        # Git-tracked JSON uses canonical LF bytes on Windows as in other source queries.
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(raw).hexdigest() != binding["sha256"]:
            raise ValueError(f"source hash differs: {source_id}")
        sources[source_id] = json.loads(raw)

    def resolve(ref: dict[str, str]) -> Any:
        return deepcopy(pointer(sources[ref["source"]], ref["pointer"]))

    constructs = {}
    for key, item in spec["constructs"].items():
        source_record = resolve(item["provider"])
        if source_record["construct_id"] != item["source_construct_id"]:
            raise ValueError(f"construct provider identity differs: {key}")
        if item["background_id"] not in spec["constructs"]:
            raise ValueError(f"unbound perturbation background: {key}")
        if item["perturbation"]:
            if resolve(item["perturbation_provider"]) != item["perturbation"]:
                raise ValueError(f"perturbation differs from source: {key}")
            background = spec["constructs"][item["background_id"]]
            if resolve(item["background_provider"]) != background["source_construct_id"]:
                raise ValueError(f"background differs from source: {key}")
        elif item["background_id"] != key:
            raise ValueError("unperturbed reference must be its own comparison background")
        sequence_record = resolve(item["sequence_provider"])
        if sequence_record["construct_id"] != source_record["construct_id"]:
            raise ValueError(f"sequence provider construct differs: {key}")
        sequence = sequence_record.get("sequence")
        digest = sequence_record.get("sequence_sha256")
        if sequence is not None:
            if hashlib.sha256(sequence.encode("ascii")).hexdigest() != digest:
                raise ValueError(f"sequence hash differs: {key}")
        elif digest is not None:
            raise ValueError("sequence hash without sequence")
        constructs[key] = {
            **deepcopy(item), "source_record": source_record,
            "sequence": sequence, "sequence_sha256": digest,
            "sequence_status": sequence_record["sequence_status"],
            "sequence_identity_available": sequence is not None,
            "assay_specimen_sequence_verified": False,
        }
    assays = {}
    for key, item in spec["assays"].items():
        source_record = resolve(item["provider"])
        if source_record["assay_id"] != item["source_assay_id"]:
            raise ValueError(f"assay provider identity differs: {key}")
        assays[key] = {**deepcopy(item), "source_record": source_record}
    reactions = {}
    for key, item in spec.get("reactions", {}).items():
        source_record = resolve(item["provider"])
        if source_record["reaction_id"] != item["source_reaction_id"]:
            raise ValueError("reaction provider identity differs")
        participants = source_record["participants"]
        _unique(participants, "participant_id")
        if {participant["side"] for participant in participants} != {"reactant", "product"}:
            raise ValueError("reaction requires distinct reactant and product sides")
        if any(not participant.get("name") or not participant.get("role") for participant in participants):
            raise ValueError("reaction participant requires a source name and role")
        if item["reactant_substrate_id"] not in spec["substrates"]:
            raise ValueError("unbound reaction reactant substrate")
        reactant_ids = {participant["participant_id"] for participant in participants
                        if participant["side"] == "reactant"}
        input_ids = spec["substrates"][item["reactant_substrate_id"]].get("participant_ids", [])
        if len(input_ids) != len(set(input_ids)) or set(input_ids) != reactant_ids:
            raise ValueError("substrate participant IDs differ from source reaction reactants")
        reactions[key] = {**deepcopy(item), "source_record": source_record}
        if item.get("connectivity_providers"):
            provider = item["provider"]["source"]
            relations = [_connectivity_relation(resolve(ref), source_record,
                         spec["sources"][provider], sources[provider])
                         for ref in item["connectivity_providers"]]
            _unique([relation["source_annotation"] for relation in relations], "relation_id")
            reactions[key]["connectivity_relations"] = relations
    observations = []
    for panel in spec["panels"]:
        source = sources[panel["source"]]
        source_rows = pointer(source, panel["rows_pointer"])
        indices = panel.get("row_indices", list(range(len(source_rows))))
        for index in indices:
            source_row = source_rows[index]
            fields = {key: _pick(source_row, selector) for key, selector in panel["fields"].items()}
            comparison_blocks = [check["reason"] for check in panel.get("row_checks", [])
                                 if _pick(source_row, check["selector"]) != check["expected"]]
            construct_id = panel["study_id"] + ":" + fields["construct_id"]
            assay_id = panel["study_id"] + ":" + fields["assay_id"]
            construct, assay = constructs[construct_id], assays[assay_id]
            substrate = spec["substrates"][fields["substrate_id"]]
            reaction_id = panel.get("reaction_id")
            reaction = reactions[reaction_id] if reaction_id is not None else None
            if reaction is not None:
                if fields["substrate_id"] != reaction["reactant_substrate_id"]:
                    raise ValueError("reaction reactants differ from observation substrate")
                if (assay["source_record"].get("reaction_id") != reaction["source_reaction_id"]
                        or assay["reaction_direction"] != reaction["source_record"]["direction"]):
                    raise ValueError("reaction differs from source assay identity or direction")
            for parameter in panel["parameters"]:
                raw_parameter = pointer(source_row, parameter["pointer"])
                contract = spec["parameter_contracts"][parameter["id"]]
                source_field = parameter["pointer"].split("/")[-1]
                if source_field not in contract["source_fields"]:
                    raise ValueError("parameter source field differs from contract")
                for field, allowed in contract.get("source_markers", {}).items():
                    if raw_parameter.get(field) not in allowed:
                        raise ValueError("parameter source marker differs from contract")
                kind = _pick(raw_parameter, parameter["kind"])
                if "status_kinds" in parameter:
                    kind = parameter["status_kinds"][kind]
                value = _pick(raw_parameter, parameter["value"])
                unit = _pick(raw_parameter, parameter["unit"])
                if kind not in KINDS:
                    raise ValueError(f"unknown result kind: {kind}")
                if kind == "numeric" and (not _number(value) or value < 0 or not unit):
                    raise ValueError("numeric result requires finite nonnegative value and unit")
                if kind == "numeric" and unit not in contract["units"]:
                    raise ValueError("parameter unit differs from contract")
                if kind != "numeric" and value is not None:
                    raise ValueError("nonnumeric result must not be coerced to a value")
                uncertainty = {key: _pick(raw_parameter, selector)
                               for key, selector in parameter["uncertainty"].items()}
                error = uncertainty["value"]
                if error is not None and (not _number(error) or error < 0):
                    raise ValueError("uncertainty must be finite nonnegative numeric or null")
                if error is not None and uncertainty["kind"] in {None, "not_reported"}:
                    raise ValueError("reported uncertainty requires a kind or explicit unresolved kind")
                if uncertainty["unreported_is_zero"] is not False:
                    raise ValueError("unreported uncertainty is not zero")
                nondetection = None
                if kind == "nondetection":
                    nondetection = {key: _pick(source_row, selector)
                                    for key, selector in panel["nondetection"].items()}
                    if not nondetection["scope"] or not nondetection["source_token"]:
                        raise ValueError("nondetection requires source token and endpoint scope")
                    if nondetection["is_zero_rate"] is not False:
                        raise ValueError("nondetection is not a zero rate")
                result_detail = {}
                if kind in {"unavailable", "qualitative"}:
                    detail_field = "unavailability" if kind == "unavailable" else "qualitative_result"
                    detail = {key: _pick(raw_parameter, selector)
                              for key, selector in parameter[detail_field].items()}
                    required = ("source_token", "scope", "reason") if kind == "unavailable" else ("source_token", "scope")
                    if not all(detail.get(key) for key in required):
                        raise ValueError(f"{kind} result requires source token and scope, and a reason if unavailable")
                    if kind == "unavailable" and detail.get("is_zero_rate") is not False:
                        raise ValueError("unavailable result is not a zero rate")
                    result_detail[detail_field] = detail
                row_id = f"{panel['id']}:{fields['row_id']}:{parameter['id']}"
                source_pointer = f"{panel['rows_pointer']}/{index}"
                observations.append({
                    "id": row_id, "study_id": panel["study_id"],
                    "source_row_id": fields["row_id"], "construct_id": construct_id,
                    "background_id": construct["background_id"],
                    "perturbation": deepcopy(construct["perturbation"]),
                    "assay_id": assay_id, "assay_qualified": assay["qualified"],
                    "endpoint_kind": assay["endpoint_kind"],
                    "reaction_direction": assay["reaction_direction"],
                    "reaction_id": reaction_id, "reaction_context": deepcopy(reaction),
                    "substrate_id": fields["substrate_id"], "substrate": deepcopy(substrate),
                    "parameter": parameter["id"], "result_kind": kind,
                    "value": value, "unit": unit,
                    "uncertainty": uncertainty, "nondetection": nondetection,
                    **result_detail,
                    "uncertainty_context": deepcopy(assay["uncertainty_context"]),
                    "sequence_identity_available": construct["sequence_identity_available"],
                    "comparison_blocks": comparison_blocks,
                    "source_locator": fields["source_locator"],
                    "provider": {"source": panel["source"], "pointer": source_pointer},
                    "parameter_provider": {"source": panel["source"], "pointer": source_pointer + parameter["pointer"]},
                    "source_parameter": deepcopy(raw_parameter),
                    "source_record": deepcopy(source_row),
                })
    rows = _unique(observations, "id")
    state_links = []
    for link in spec.get("state_links", []):
        construct = constructs[link["construct_id"]]
        context = resolve(link["context_provider"])
        if context["schema_version"] != "catalytic-earth.construct-chemical-state-context.v1":
            raise ValueError("state link context schema differs")
        if context["construct_id"] != construct["source_construct_id"]:
            raise ValueError("state link source construct differs")
        source_states = _unique(context["states"], "state_id")
        ids = link["observation_ids"]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError("state link requires unique observations")
        if any(row_id not in rows or rows[row_id]["construct_id"] != link["construct_id"]
               or rows[row_id]["study_id"] != link["study_id"] for row_id in ids):
            raise ValueError("state link observation construct or study differs")
        functional = context["functional_context"]
        for row_id in ids:
            provider = rows[row_id]["provider"]
            if (spec["sources"][provider["source"]] != functional["provider"] or
                    provider["pointer"] != functional["row_pointer"]):
                raise ValueError("state link functional source row differs")
        if {rows[row_id]["parameter"] for row_id in ids} != set(functional["parameter_ids"]):
            raise ValueError("state link functional parameters differ")
        states = []
        for state in link["states"]:
            deposit = resolve(state["provider"])
            if (deposit["packet_id"] != state["packet_id"] or
                    source_states[state["state_id"]]["deposit_packet_id"] != state["packet_id"]):
                raise ValueError("state link deposit packet differs")
            if deposit["schema_version"] != "catalytic-earth.deposit-context.v1":
                raise ValueError("state link deposit schema differs")
            entries = [row for selection in deposit["row_selections"]
                       if selection["category"] == "_entry" for row in selection["rows"]]
            if len(entries) != 1 or entries[0]["id"] != source_states[state["state_id"]]["pdb_id"]:
                raise ValueError("state link PDB entry differs")
            selections = _unique(deposit["row_selections"], "selection_id")
            selection = selections[state["polymer_selection_id"]]
            if selection["category"] != "_entity_poly" or len(selection["rows"]) != 1:
                raise ValueError("state link requires one deposited polymer sequence")
            polymer = selection["rows"][0]
            canonical = "".join(polymer["pdbx_seq_one_letter_code_can"].split())
            if not construct["sequence"] or canonical != construct["sequence"]:
                raise ValueError("state link canonical sequence differs from construct")
            states.append({**deepcopy(state), "canonical_sequence_equal": True,
                           "canonical_sequence_sha256": construct["sequence_sha256"],
                           "deposit_context": deposit})
        if not states:
            raise ValueError("state link requires deposited states")
        _unique(states, "packet_id")
        _unique(states, "state_id")
        state_links.append({**deepcopy(link), "states": states, "source_context": context,
                            "identity_scope": "source-named construct and full canonical sequence equality",
                            "physical_preparation_identity_established": False,
                            "chemical_state_identity_from_sequence": False})
    _unique(state_links, "id")
    model_links = [_model_link(resolve(link["context_provider"]), link, constructs, rows, assays,
                               spec["sources"], resolve)
                   for link in spec.get("model_links", [])]
    _unique(model_links, "id")
    comparisons = []
    for request in spec["comparisons"]:
        if not request["evidence"]:
            raise ValueError("comparison requires bound source evidence")
        for row_id in request.get("context_observations", []):
            if row_id not in rows or rows[row_id]["study_id"] != request["study_id"]:
                raise ValueError("unbound or cross-study context observation")
        resolved_request = deepcopy(request)
        resolved_request["source_evidence"] = [resolve(ref) for ref in request["evidence"]]
        if request.get("substrate_pair_source"):
            pair = resolve(request["substrate_pair_source"])
            bound_ids = {item["substrate_id"] for item in pair}
            if {rows[row_id]["substrate_id"] for row_id in request["roles"].values()} != bound_ids:
                raise ValueError("comparison substrate pair differs from source")
        comparisons.append(compare(rows, resolved_request))
    _unique(comparisons, "id")
    control_relations = []
    for link in spec.get("control_relations", []):
        context = resolve(link["provider"])
        if context["id"] != link["id"] or context["study_id"] != link["study_id"]:
            raise ValueError("system control provider identity differs")
        control_relations.append(control_relation(context, resolve))
    _unique(control_relations, "id")
    for witness in spec.get("source_witnesses", []):
        if not witness["source_bindings"]:
            raise ValueError("source witness requires a binding")
        for ref in witness["source_bindings"]:
            record = resolve(ref)
            if record["sha256"] != witness["sha256"]:
                raise ValueError("source witness hash differs from binding")
            length = record.get("bytes", record.get("response_body_bytes"))
            if length is not None and length != witness["bytes"]:
                raise ValueError("source witness byte count differs from binding")
    for row in observations:
        row["comparison_memberships"] = [
            {"comparison_id": item["id"], "roles": [role for role, row_id in item["roles"].items()
                                                    if row_id == row["id"]],
             "matched_control_observation": item["roles"].get("denominator", item["roles"].get("parent")),
             "eligible": item["eligible"], "reasons": item["reasons"]}
            for item in comparisons if row["id"] in item["roles"].values()
        ]
    return {
        "schema_version": "catalytic-earth.perturbation-relation.v1",
        "review_status": "internal_unreviewed_candidate; eligibility means proposed arithmetic only",
        "scope": deepcopy(spec["scope"]), "sources": deepcopy(spec["sources"]),
        "constructs": constructs, "assays": assays, "substrates": deepcopy(spec["substrates"]),
        "reactions": reactions,
        "observations": observations, "comparisons": comparisons,
        "state_links": state_links,
        "model_links": model_links,
        "control_relations": control_relations,
        "evidence_context": {key: [resolve(ref) for ref in refs]
                             for key, refs in spec["evidence_context"].items()},
        "source_witnesses": deepcopy(spec.get("source_witnesses", [])),
        "source_witness_cache_status": "not_checked_by_projection; use --verify-witnesses for local bytes",
    }


def project(repo_root: Path, spec: dict[str, Any] | None = None) -> dict[str, Any]:
    """Resolve the exact computationally source-reviewed projection, or fail closed.

    Curated type/assay/direction mappings interpret source prose. Their authority
    comes from a versioned source review, not from duplicating those labels in a
    second mutable contract or pretending to derive them from a matching hash.
    """
    repo_root = repo_root.resolve()
    review = json.loads((repo_root / REVIEW_PATH).read_text(encoding="utf-8"))
    if review.get("status") != "source_reviewed_computational":
        raise ValueError("perturbation projection review is not accepted")
    accepted = json.loads((repo_root / SPEC_PATH).read_text(encoding="utf-8"))
    required = {SPEC_PATH, "src/catalytic_earth/atlas_perturbations.py",
                "scripts/query_atlas_perturbations.py"}
    if any(item.get("connectivity_providers") for item in accepted.get("reactions", {}).values()):
        required.add("src/catalytic_earth/atlas_transformations.py")
    if not required <= set(review["reviewed_bindings"]):
        raise ValueError("review does not bind projection and public consumers")
    for relative, digest in review["reviewed_bindings"].items():
        path = (repo_root / relative).resolve()
        if not path.is_relative_to(repo_root):
            raise ValueError("review binding escapes repository")
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"reviewed binding differs: {relative}; renewed source review required")
    if spec is not None and spec != accepted:
        raise ValueError("candidate differs from reviewed projection; use internal development path")
    result = _project_candidate(repo_root, accepted)
    if result["state_links"]:
        from .atlas_deposit_context import check_deposit_context
        checked = {}
        for link in result["state_links"]:
            for state in link["states"]:
                relative = accepted["sources"][state["provider"]["source"]]["path"]
                if relative not in checked:
                    checked[relative] = check_deposit_context(Path(relative).parent, repo_root)
                if checked[relative] != state["deposit_context"]:
                    raise ValueError("state link differs from reviewed deposit reconstruction")
    result["review_status"] = "source_reviewed_computational; not independent human or experimental validation"
    result["review"] = review
    return result


def verify_witnesses(common_dir: Path, view: dict[str, Any]) -> dict[str, int]:
    """Verify locally retained primary bytes without fetching or redistributing."""
    common_dir = common_dir.resolve()
    for witness in view["source_witnesses"]:
        path = (common_dir / witness["git_common_dir_relative_path"]).resolve()
        if not path.is_relative_to(common_dir):
            raise ValueError("source witness cache path escapes Git common directory")
        raw = path.read_bytes()
        if len(raw) != witness["bytes"] or hashlib.sha256(raw).hexdigest() != witness["sha256"]:
            raise ValueError("local source witness bytes differ")
    return {"verified_files": len(view["source_witnesses"]),
            "verified_bytes": sum(item["bytes"] for item in view["source_witnesses"])}
