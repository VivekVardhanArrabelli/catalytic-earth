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
KINDS = {"numeric", "nondetection", "source_conflict", "unassessed", "qualitative"}


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
    selected = {role: rows[row_id] for role, row_id in request["roles"].items()}
    reasons = list(request.get("source_blocks", []))
    if operation == "unassessed":
        reasons.append("matched_perturbation_control_unassessed")
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
        result["interpretation_limit"] = "No matched perturbation comparison was evaluated; an unassessed control is neither a measured effect nor nondetection."
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
    required = {SPEC_PATH, "src/catalytic_earth/atlas_perturbations.py",
                "scripts/query_atlas_perturbations.py"}
    if not required <= set(review["reviewed_bindings"]):
        raise ValueError("review does not bind projection and public consumers")
    for relative, digest in review["reviewed_bindings"].items():
        path = (repo_root / relative).resolve()
        if not path.is_relative_to(repo_root):
            raise ValueError("review binding escapes repository")
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"reviewed binding differs: {relative}; renewed source review required")
    accepted = json.loads((repo_root / SPEC_PATH).read_text(encoding="utf-8"))
    if spec is not None and spec != accepted:
        raise ValueError("candidate differs from reviewed projection; use internal development path")
    result = _project_candidate(repo_root, accepted)
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
