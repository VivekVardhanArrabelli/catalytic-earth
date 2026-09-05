"""Deterministic, computationally provisional Atlas-50 crosswalk v2 builder.

The builder consumes the frozen Phase-A draft and its computational source
audit.  It deliberately does not consume the historical curated-702 labels:
those labels are discovery locators, not adjudicated mechanism mappings.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


PHASE_A_RELATIVE = Path("data/atlas/atlas50/phase_a/crosswalk_draft.json")
REVIEW_RELATIVE = Path(
    "data/atlas/atlas50/computational_review/crosswalk_review.json"
)
OUTPUT_RELATIVE = Path("data/atlas/atlas50/crosswalk_v2")

EXPECTED_INPUT_SHA256 = {
    PHASE_A_RELATIVE.as_posix(): (
        "838d74b142fc82c81183daa8d469db9e2baab52ffade4c8c6cf0b07826da1dac"
    ),
    REVIEW_RELATIVE.as_posix(): (
        "84150aff2cb563c1f624aa3ce000c91c3588c520604715e81197f87e77d8ad4e"
    ),
}

CLASSIFICATIONS = (
    "exact_duplicate",
    "aggregation",
    "specialization",
    "interoperability_bridge",
    "genuinely_missing_concept",
    "unsupported_or_ill_defined",
    "unresolved",
)
RELATIONS = (
    "exact_duplicate",
    "aggregation",
    "specialization",
    "interoperability_bridge",
    "scope_probe",
    "counterevidence",
    "scope_exclusion",
    "rejected_mapping",
)
POSITIVE_APPLICABILITY = {
    "exact_scope_supported",
    "representative_scope_only",
    "supported_branch",
    "representative_non_detailed",
}
EXACT_SCOPE_ALLOWLIST = {
    (
        "dihydrofolate_reductase",
        "M0112",
        "reaction_core: EC 1.5.1.3 NADPH-dependent DHF-to-THF chemistry",
    )
}
REVIEW_INDEPENDENCE = {
    "reviewer_kind": "same_model_computational_agents",
    "statistically_independent": False,
    "correlated_error_risk": True,
    "independent_human_reviewer_count": 0,
    "experimental_validation_count": 0,
}

_MCSA_RE = re.compile(r"^M[0-9]{4}$")
_INTERNAL_RE = re.compile(r"^atlas50:[a-z0-9_]+$")


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _load_pinned_json(repo_root: Path, relative: Path) -> tuple[dict[str, Any], str]:
    payload = (repo_root / relative).read_bytes()
    digest = _sha256(payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    expected = EXPECTED_INPUT_SHA256[relative.as_posix()]
    if digest != expected:
        raise ValueError(
            f"Atlas-50 v2 input hash differs for {relative.as_posix()}: "
            f"expected {expected}, found {digest}"
        )
    return json.loads(payload), digest


def _mcsa_identity(
    target_id: str,
    name: str,
    *,
    ec: str | None = None,
    detail: str | None = None,
    origin: str = "direct_official_source_check_2026-09-05",
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "status": "official_entry_checked",
        "name": name,
        "uri": (
            "https://www.ebi.ac.uk/thornton-srv/m-csa/entry/"
            f"{int(target_id[1:])}/"
        ),
        "checked_at": "2026-09-05",
        "origin": origin,
    }
    if ec is not None:
        value["ec"] = ec
    if detail is not None:
        value["mechanism_detail"] = detail
    return value


# Replacement identities below were checked directly against the current
# official M-CSA entry pages.  They are evidence of source identity; their
# mechanistic applicability is stated separately in each relation target.
DIRECT_MCSA_IDENTITIES: dict[str, dict[str, Any]] = {
    "M0002": _mcsa_identity(
        "M0002", "beta-lactamase (Class A)", ec="3.5.2.6", detail="detailed"
    ),
    "M0006": _mcsa_identity(
        "M0006", "glutathione-disulfide reductase", ec="1.8.1.7", detail="detailed"
    ),
    "M0015": _mcsa_identity(
        "M0015",
        "beta-lactamase (Class B1), dimetallic mechanism",
        ec="3.5.2.6",
        detail="detailed",
    ),
    "M0016": _mcsa_identity(
        "M0016",
        "beta-lactamase (Class B1), monometallic mechanism",
        ec="3.5.2.6",
        detail="detailed",
    ),
    "M0049": _mcsa_identity(
        "M0049",
        "histidine decarboxylase (pyruvoyl-dependent)",
        ec="4.1.1.22",
        detail="detailed",
    ),
    "M0052": _mcsa_identity(
        "M0052",
        "fructose-bisphosphate aldolase (Class II)",
        ec="4.1.2.13",
        detail="detailed",
    ),
    "M0066": _mcsa_identity(
        "M0066", "D-alanine transaminase", ec="2.6.1.21", detail="detailed"
    ),
    "M0112": _mcsa_identity(
        "M0112", "dihydrofolate reductase (bacterial)", ec="1.5.1.3", detail="detailed"
    ),
    "M0133": _mcsa_identity(
        "M0133", "camphor 5-monooxygenase (P450cam)", ec="1.14.15.1", detail="detailed"
    ),
    "M0135": _mcsa_identity(
        "M0135", "peptidylglycine monooxygenase", ec="1.14.17.3", detail="detailed"
    ),
    "M0138": _mcsa_identity(
        "M0138", "copper/zinc superoxide dismutase", ec="1.15.1.1", detail="detailed"
    ),
    "M0150": _mcsa_identity(
        "M0150", "nucleoside-diphosphate kinase", ec="2.7.4.6", detail="detailed"
    ),
    "M0186": _mcsa_identity(
        "M0186", "L-serine ammonia-lyase", ec="4.3.1.17", detail="detailed"
    ),
    "M0210": _mcsa_identity(
        "M0210", "beta-lactamase (Class D)", ec="3.5.2.6", detail="detailed"
    ),
    "M0213": _mcsa_identity(
        "M0213", "alanine racemase", ec="5.1.1.1", detail="detailed"
    ),
    "M0222": _mcsa_identity(
        "M0222",
        "fructose-bisphosphate aldolase (Class I)",
        ec="4.1.2.13",
        detail="detailed",
    ),
    "M0239": _mcsa_identity(
        "M0239", "horseradish peroxidase C", ec="1.11.1.7", detail="detailed"
    ),
    "M0257": _mcsa_identity(
        "M0257", "beta-lactamase (Class C)", ec="3.5.2.6", detail="detailed"
    ),
    "M0381": _mcsa_identity(
        "M0381", "thioredoxin reductase", ec="1.8.1.9", detail="summary_only"
    ),
    "M0390": _mcsa_identity(
        "M0390", "laccase", ec="1.10.3.2", detail="summary_only"
    ),
    "M0482": _mcsa_identity(
        "M0482",
        "2,2-dialkylglycine decarboxylase (pyruvate)",
        ec="4.1.1.64",
        detail="summary_only_no_ordered_steps",
    ),
}


CLASSIFICATION_OVERRIDES = {
    "plp_dependent_enzyme": "aggregation",
    "heme_peroxidase_oxidase": "aggregation",
    "copper_oxidoreductase": "aggregation",
    "class_ii_metal_aldolase": "specialization",
    "serine_beta_lactamase": "aggregation",
    "metallo_beta_lactamase": "aggregation",
    "flavin_disulfide_reductase": "aggregation",
    "dihydrofolate_reductase": "exact_duplicate",
}

SCOPE_CORRECTIONS = {
    "plp_dependent_enzyme": (
        "Broad PLP aggregation represented by separately named transamination, "
        "racemization, elimination, and decarboxylation branches; pyruvoyl M0049 "
        "is outside PLP scope."
    ),
    "heme_peroxidase_oxidase": (
        "Heme peroxidase/oxidase scope anchored by a direct heme-peroxidase "
        "object; cytochrome P450 and copper laccase remain in rows 13 and 18."
    ),
    "cytochrome_p450_monooxygenase": (
        "Cytochrome P450 heme-thiolate monooxygenases; direct heme peroxidases "
        "and copper laccases are excluded."
    ),
    "copper_oxidoreductase": (
        "Copper oxidoreductases include copper monooxygenase and multicopper "
        "laccase branches; heme enzymes are excluded."
    ),
    "class_ii_metal_aldolase": (
        "Metal-dependent class-II aldolases. Same-EC class-I Schiff-base "
        "aldolase M0222 is mandatory counterevidence."
    ),
    "nucleoside_diphosphate_kinase": (
        "NDPK chemistry includes a phosphohistidine ping-pong intermediate; "
        "species-general equivalence to M0150 remains unresolved."
    ),
    "manganese_iron_superoxide_dismutase": (
        "Mn/Fe SOD only. M0138 is a Cu/Zn SOD counterexample, not positive "
        "coverage for this fingerprint."
    ),
    "serine_beta_lactamase": (
        "Aggregation of serine beta-lactamase Classes A, C, and D with "
        "class-specific catalytic networks retained."
    ),
    "metallo_beta_lactamase": (
        "Broad class-B metallo-beta-lactamase aggregation. M0015 and M0016 "
        "cover dimetallic and monometallic Class-B1 mechanisms only; B2/B3 "
        "remain unrepresented."
    ),
    "flavin_disulfide_reductase": (
        "Aggregation of FAD-dependent disulfide-reductase branches with "
        "distinct substrate relays and domain arrangements."
    ),
    "dihydrofolate_reductase": (
        "Exact duplicate of M0112 only at reaction-core granularity: EC 1.5.1.3 "
        "NADPH-dependent DHF-to-THF chemistry. Protein, organism, resistance, "
        "fusion, and structure applicability remain narrower than that relation. "
        "Conserved water donates the N5 proton while Asp26 tunes the hydrogen-bond "
        "network and pKa."
    ),
}

RATIONALE_OVERRIDES = {
    "dihydrofolate_reductase": (
        "Keep exact_duplicate only at the declared EC 1.5.1.3 reaction-core "
        "granularity. Correct N5 protonation to conserved-water donation with "
        "Asp26 organizing and tuning the hydrogen-bond network; do not transfer "
        "protein, organism, resistance, fusion, or structure applicability."
    )
}

CHANGE_REASON_OVERRIDES = {
    "dihydrofolate_reductase": (
        "The Phase-A exact relation lacked an explicit granularity and assigned "
        "direct N5 proton donation to Asp/Glu. M0112 supports the reaction core, "
        "with conserved water as proton donor and Asp26 as network/pKa organizer; "
        "broader applicability is not asserted."
    )
}


def _target(
    target_id: str,
    relation: str,
    applicability_status: str,
    scope: str,
    rationale: str,
    *,
    identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if identity is None:
        identity = DIRECT_MCSA_IDENTITIES[target_id]
    return {
        "source_key": "mcsa" if _MCSA_RE.fullmatch(target_id) else "atlas50_fingerprint",
        "target_id": target_id,
        "relation": relation,
        "relation_direction": "fingerprint_to_target",
        "source_identity": dict(identity),
        "mechanistic_applicability": {
            "status": applicability_status,
            "scope": scope,
            "rationale": rationale,
        },
    }


def _internal_target(
    fingerprint_id: str, relation: str, scope: str, rationale: str
) -> dict[str, Any]:
    target_id = f"atlas50:{fingerprint_id}"
    return _target(
        target_id,
        relation,
        "scope_unresolved",
        scope,
        rationale,
        identity={
            "status": "frozen_fingerprint_identity",
            "name": fingerprint_id,
            "uri": None,
            "checked_at": "2026-09-05",
            "origin": "frozen_phase_a_row_identity",
        },
    )


SPECIAL_RELATION_TARGETS: dict[str, list[dict[str, Any]]] = {
    "plp_dependent_enzyme": [
        _target(
            "M0049",
            "rejected_mapping",
            "contradicted",
            "PLP fingerprint",
            "Official identity is pyruvoyl-dependent histidine decarboxylase. "
            "M0049 remains a valid source object outside this PLP mapping.",
        ),
        _target(
            "M0066", "aggregation", "supported_branch", "PLP transamination branch",
            "Official entry identifies PLP-dependent D-amino-acid transamination.",
        ),
        _target(
            "M0213", "aggregation", "supported_branch", "PLP racemization branch",
            "Official entry identifies PLP-dependent alanine racemization.",
        ),
        _target(
            "M0186", "aggregation", "supported_branch", "PLP elimination branch",
            "Official entry identifies PLP-dependent serine ammonia elimination.",
        ),
        _target(
            "M0482", "aggregation", "representative_non_detailed",
            "PLP decarboxylation/transamination branch",
            "Official identity and PLP cofactor are explicit, but the entry has "
            "summary-level rather than ordered-step mechanism content.",
        ),
    ],
    "heme_peroxidase_oxidase": [
        _target(
            "M0239", "aggregation", "supported_branch", "heme peroxidase branch",
            "Official entry is a heme-b peroxidase using hydrogen peroxide.",
        ),
        _target(
            "M0133", "scope_exclusion", "out_of_scope", "cytochrome P450 branch",
            "P450cam belongs to the dedicated P450 fingerprint, not direct "
            "peroxidase coverage.",
        ),
        _target(
            "M0390", "scope_exclusion", "out_of_scope", "copper laccase branch",
            "Official laccase entry uses a multicopper centre and belongs in row 18.",
        ),
    ],
    "cytochrome_p450_monooxygenase": [
        _target(
            "M0133", "specialization", "representative_scope_only",
            "P450 heme-thiolate monooxygenation",
            "Official entry identifies P450cam with heme b and a cysteine axial ligand.",
        ),
        _target(
            "M0239", "scope_exclusion", "out_of_scope", "direct heme peroxidase",
            "Peroxidase chemistry remains in row 12.",
        ),
        _target(
            "M0390", "scope_exclusion", "out_of_scope", "multicopper laccase",
            "Laccase chemistry remains in row 18.",
        ),
    ],
    "copper_oxidoreductase": [
        _target(
            "M0135", "aggregation", "supported_branch", "copper monooxygenase branch",
            "Official entry identifies a two-copper peptidylglycine monooxygenase.",
        ),
        _target(
            "M0390", "aggregation", "supported_branch", "multicopper oxidase branch",
            "Official entry identifies a four-copper laccase and oxygen reduction.",
        ),
        _target(
            "M0239", "scope_exclusion", "out_of_scope", "heme peroxidase branch",
            "Heme peroxidase chemistry remains in row 12.",
        ),
    ],
    "class_ii_metal_aldolase": [
        _target(
            "M0052", "specialization", "representative_scope_only",
            "metal-dependent class-II fructose-bisphosphate aldolase",
            "Official entry explicitly requires divalent metal and identifies Class II.",
        ),
        _target(
            "M0222", "counterevidence", "counterexample_only",
            "same EC, class-I Schiff-base mechanism",
            "Official entry has the same EC 4.1.2.13 but a distinct Class-I mechanism.",
        ),
    ],
    "nucleoside_diphosphate_kinase": [
        _target(
            "M0150", "exact_duplicate", "scope_unresolved",
            "NDPK overall reaction and phosphohistidine mechanism",
            "The direct exact-reaction locator exists, but species-general "
            "fingerprint equivalence has not been established.",
        )
    ],
    "manganese_iron_superoxide_dismutase": [
        _target(
            "M0138", "counterevidence", "counterexample_only", "Cu/Zn SOD",
            "Official identity and metal centre contradict positive Mn/Fe coverage.",
        )
    ],
    "serine_beta_lactamase": [
        _target(
            "M0002", "aggregation", "supported_branch", "Ambler Class A",
            "Class-A serine acyl-enzyme mechanism only.",
        ),
        _target(
            "M0257", "aggregation", "supported_branch", "Ambler Class C",
            "Class-C serine mechanism uses a distinct Tyr150-centred network.",
        ),
        _target(
            "M0210", "aggregation", "supported_branch", "Ambler Class D",
            "Class-D serine mechanism uses a carboxylated lysine network.",
        ),
    ],
    "metallo_beta_lactamase": [
        _target(
            "M0015", "aggregation", "supported_branch",
            "Ambler Class B1, dimetallic mechanism",
            "Official entry explicitly describes a two-zinc Class-B1 mechanism.",
        ),
        _target(
            "M0016", "aggregation", "supported_branch",
            "Ambler Class B1, monometallic mechanism",
            "Official entry explicitly describes a one-zinc Class-B1 mechanism.",
        ),
    ],
    "flavin_disulfide_reductase": [
        _target(
            "M0006", "aggregation", "supported_branch", "glutathione reductase relay",
            "Official entry describes NADPH-to-FAD-to-active-site-disulfide transfer.",
        ),
        _target(
            "M0381", "aggregation", "representative_non_detailed",
            "thioredoxin reductase relay",
            "Official entry identifies the FAD/NADPH domains and distinct domain motion, "
            "but provides only summary-level steps.",
        ),
    ],
    "dihydrofolate_reductase": [
        _target(
            "M0112", "exact_duplicate", "exact_scope_supported",
            "reaction_core: EC 1.5.1.3 NADPH-dependent DHF-to-THF chemistry",
            "M0112 matches hydride transfer to C6 with concomitant N5 protonation "
            "at reaction-core granularity. Protein, organism, resistance, fusion, "
            "and structure applicability are not asserted equivalent.",
        ),
    ],
}


INTERNAL_TARGETS = {
    "had_like_phosphatase": [
        _internal_target(
            "metallophosphomonoesterase", "specialization", "putative parent row",
            "The parent is now named, but source-supported applicability remains unresolved.",
        )
    ],
    "alpha_beta_hydrolase_esterase_lipase": [
        _internal_target(
            "ser_his_acid_hydrolase", "specialization", "putative parent row",
            "The parent is named; fold-to-mechanism transfer is still unresolved.",
        )
    ],
    "ser_thr_protein_phosphatase": [
        _internal_target(
            "metallophosphomonoesterase", "specialization", "putative parent row",
            "The parent is named; PPP/PPM applicability is still unresolved.",
        )
    ],
    "short_chain_dehydrogenase_reductase": [
        _internal_target(
            "nad_p_dehydrogenase", "specialization", "putative parent row",
            "The parent is named; reaction-specific applicability remains unresolved.",
        )
    ],
    "aldo_keto_reductase": [
        _internal_target(
            "nad_p_dehydrogenase", "specialization", "putative parent row",
            "The parent is named; reaction-specific applicability remains unresolved.",
        )
    ],
    "aminoglycoside_acetyltransferase": [
        _internal_target(
            "coa_acyltransferase", "specialization", "putative parent row",
            "The parent is named; GNAT/AAC relation remains unresolved.",
        )
    ],
}


def _identity_from_review(check: dict[str, Any]) -> dict[str, Any]:
    target_id = check["mcsa_id"]
    if target_id in DIRECT_MCSA_IDENTITIES:
        return dict(DIRECT_MCSA_IDENTITIES[target_id])
    return {
        "status": "official_entry_checked",
        "name": check["official_name"],
        "uri": check["source_uri"],
        "checked_at": "2026-09-05",
        "origin": "computational_review_official_check",
        "mechanism_detail": check.get("mechanism_detail"),
    }


def _generic_relation_targets(
    phase_row: dict[str, Any], review_row: dict[str, Any], classification: str
) -> list[dict[str, Any]]:
    relation_class = (
        classification
        if classification != "unresolved"
        else phase_row["classification"]
    )
    relation = (
        relation_class
        if relation_class in {"aggregation", "specialization", "interoperability_bridge"}
        else "scope_probe"
    )
    targets: list[dict[str, Any]] = []
    for check in review_row["authoritative_mcsa_checks"]:
        assessment = check["fit_assessment"]
        if assessment == "contradicts_fingerprint_cofactor":
            target_relation, status = "rejected_mapping", "contradicted"
        elif assessment == "correct_counterexample_only":
            target_relation, status = "counterevidence", "counterexample_only"
        elif assessment == "overlap_subtype_not_peroxidase_representative":
            target_relation, status = "scope_exclusion", "out_of_scope"
        elif review_row["computational_disposition"] == "unresolved_insufficient_source_targets":
            target_relation, status = relation, "scope_unresolved"
        elif assessment == "representative_only_non_detailed":
            target_relation, status = relation, "representative_non_detailed"
        elif assessment == "reaction_match_but_fingerprint_scope_broader":
            target_relation, status = relation, "representative_scope_only"
        else:
            target_relation, status = relation, "representative_scope_only"
        targets.append(
            _target(
                check["mcsa_id"],
                target_relation,
                status,
                phase_row["fingerprint_name"],
                review_row["issue"],
                identity=_identity_from_review(check),
            )
        )
    for locator in review_row["additional_mcsa_review_locators"]:
        if locator.get("evidence_status") != "official_entry_checked":
            continue
        target_id = locator["mcsa_id"]
        if any(target["target_id"] == target_id for target in targets):
            continue
        identity = (
            dict(DIRECT_MCSA_IDENTITIES[target_id])
            if target_id in DIRECT_MCSA_IDENTITIES
            else {
                "status": "official_entry_checked",
                "name": locator["official_name"],
                "uri": locator["source_uri"],
                "checked_at": "2026-09-05",
                "origin": "computational_review_official_check",
            }
        )
        targets.append(
            _target(
                target_id,
                relation,
                "scope_unresolved",
                locator.get("role", "candidate relation target"),
                "Official identity is checked; fingerprint-wide applicability remains unresolved.",
                identity=identity,
            )
        )
    targets.extend(INTERNAL_TARGETS.get(phase_row["fingerprint_id"], []))
    return targets


def _flatten_source_bundle(phase_row: dict[str, Any]) -> list[dict[str, Any]]:
    bundle = []
    for source_key, link in sorted(phase_row["source_links"].items()):
        record_ids = sorted(
            {
                record["record_id"]
                for record in link.get("records", [])
                if isinstance(record, dict) and isinstance(record.get("record_id"), str)
            }
        )
        lookup_keys = sorted(
            key for key in link.get("lookup_keys", []) if isinstance(key, str)
        )
        uris = sorted(uri for uri in link.get("uris", []) if isinstance(uri, str))
        if record_ids or lookup_keys or uris:
            bundle.append(
                {
                    "source_key": source_key,
                    "record_ids": record_ids,
                    "lookup_keys": lookup_keys,
                    "uris": uris,
                }
            )
    return bundle


def _classification_for(review_row: dict[str, Any]) -> str:
    fingerprint_id = review_row["fingerprint_id"]
    if fingerprint_id in CLASSIFICATION_OVERRIDES:
        return CLASSIFICATION_OVERRIDES[fingerprint_id]
    if review_row["computational_disposition"] == "provisional_support":
        return review_row["proposed_classification"]
    return "unresolved"


def _build_row(
    phase_row: dict[str, Any], review_row: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    fingerprint_id = phase_row["fingerprint_id"]
    classification = _classification_for(review_row)
    targets = SPECIAL_RELATION_TARGETS.get(fingerprint_id)
    if targets is None:
        targets = _generic_relation_targets(phase_row, review_row, classification)
    else:
        targets = [json.loads(json.dumps(target)) for target in targets]

    rejected_bundle: list[dict[str, Any]] = []
    if fingerprint_id == "plp_dependent_enzyme":
        rejected_bundle = [
            {
                "anchor_id": "M0049",
                "reason": (
                    "The official M0049 identity is pyruvoyl-dependent; no source "
                    "handle inherited through that anchor is positive PLP evidence."
                ),
                "anchor_valid_outside_this_mapping": True,
                "propagation_policy": "drop_entire_anchor_derived_bundle",
                "removed_source_bundle": _flatten_source_bundle(phase_row),
            }
        ]

    status = (
        "computational_provisional_relation"
        if classification != "unresolved"
        else "computational_unresolved"
    )
    row = {
        "ordinal": phase_row["ordinal"],
        "fingerprint_id": fingerprint_id,
        "fingerprint_name": phase_row["fingerprint_name"],
        "prior_classification": phase_row["classification"],
        "computational_classification": classification,
        "status": status,
        "relation_targets": targets,
        "scope_statement": SCOPE_CORRECTIONS.get(
            fingerprint_id,
            f"Scope inherited for computational comparison only: {phase_row['fingerprint_name']}.",
        ),
        "rationale": RATIONALE_OVERRIDES.get(
            fingerprint_id, review_row["proposed_correction"]
        ),
        "unresolved_reason": (
            review_row["issue"] if classification == "unresolved" else None
        ),
        "rejected_source_mappings": rejected_bundle,
        "claim_boundary": (
            "Computational proposal only; no independent-human review, experimental "
            "validation, registry admission, tier lift, or Phase-A/Phase-B change."
        ),
    }

    old_target_ids = sorted(
        {
            record["record_id"]
            for link in phase_row["source_links"].values()
            for record in link.get("records", [])
            if isinstance(record, dict) and isinstance(record.get("record_id"), str)
        }
    )
    new_targets = [
        {
            "source_key": target["source_key"],
            "target_id": target["target_id"],
            "relation": target["relation"],
            "applicability_status": target["mechanistic_applicability"]["status"],
            "scope": target["mechanistic_applicability"]["scope"],
        }
        for target in targets
    ]
    change = {
        "ordinal": phase_row["ordinal"],
        "fingerprint_id": fingerprint_id,
        "old_classification": phase_row["classification"],
        "new_classification": classification,
        "classification_changed": phase_row["classification"] != classification,
        "old_named_record_ids": old_target_ids,
        "new_relation_targets": new_targets,
        "change_kind": (
            "source_and_or_scope_correction"
            if review_row["computational_disposition"] == "correction_required"
            else "unresolved_relation"
            if classification == "unresolved"
            else "provisional_target_normalization"
        ),
        "reason": CHANGE_REASON_OVERRIDES.get(fingerprint_id, review_row["issue"]),
        "wrong_anchor_bundle_removed": bool(rejected_bundle),
    }
    return row, change


def build_crosswalk_v2_documents(
    phase_a: dict[str, Any],
    review: dict[str, Any],
    *,
    input_hashes: dict[str, str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build v2 documents from decoded inputs.

    This pure entry point is intentionally available for adversarial fixture
    tests. Repository publication goes through the pinned-input wrapper below.
    """

    phase_rows = phase_a.get("rows")
    review_rows = review.get("rows")
    if not isinstance(phase_rows, list) or len(phase_rows) != 57:
        raise ValueError("Phase-A crosswalk must contain exactly 57 rows")
    if not isinstance(review_rows, list) or len(review_rows) != 57:
        raise ValueError("computational review must contain exactly 57 rows")
    phase_ids = [row.get("fingerprint_id") for row in phase_rows]
    review_ids = [row.get("fingerprint_id") for row in review_rows]
    if phase_ids != review_ids or len(set(phase_ids)) != 57:
        raise ValueError("Phase-A and review row identities/order differ")

    rows: list[dict[str, Any]] = []
    changes: list[dict[str, Any]] = []
    for phase_row, review_row in zip(phase_rows, review_rows, strict=True):
        row, change = _build_row(phase_row, review_row)
        rows.append(row)
        changes.append(change)

    counts = dict(sorted(Counter(row["computational_classification"] for row in rows).items()))
    inputs = [
        {"path": path, "sha256": digest}
        for path, digest in sorted((input_hashes or {}).items())
    ]
    crosswalk = {
        "schema_version": "catalytic-earth.atlas50-crosswalk-v2.v1",
        "draft_id": "atlas50.crosswalk-v2.computational.2026-09-05.v1",
        "generated_at": "2026-09-05",
        "status": "computational_provisional_not_human_or_experimental_review",
        "row_count": len(rows),
        "classification_vocabulary": list(CLASSIFICATIONS),
        "classification_counts": counts,
        "inputs": inputs,
        "source_policy": {
            "historical_curated_702_used_as_truth": False,
            "replacement_identifiers_checked_against_official_source": True,
            "source_identity_does_not_imply_mechanistic_applicability": True,
            "targetless_relations_resolve_to_unresolved": True,
        },
        "review_independence": dict(REVIEW_INDEPENDENCE),
        "rows": rows,
        "claim_boundary": [
            "This is a computational development successor, not a human or expert review.",
            "Same-model computational agents have correlated errors and are not statistically independent reviewers.",
            "It does not modify frozen Phase A/B, protected registries, tiers, or selection.",
            "It makes no experimental, independent-annotation, or scientific-completion claim.",
        ],
    }
    change_map = {
        "schema_version": "catalytic-earth.atlas50-crosswalk-v2-change-map.v1",
        "change_map_id": "atlas50.crosswalk-v2.change-map.2026-09-05.v1",
        "status": "computational_provisional_not_human_review",
        "from_draft_id": phase_a.get("draft_id"),
        "to_draft_id": crosswalk["draft_id"],
        "row_count": len(changes),
        "changes": changes,
        "review_independence": dict(REVIEW_INDEPENDENCE),
        "claim_boundary": (
            "Old-to-new trace only; same-model agent results are correlated and not "
            "statistically independent, and this is not a Phase-B decision or registry mutation."
        ),
    }
    validate_crosswalk_v2(crosswalk)
    validate_change_map(change_map, crosswalk)
    return crosswalk, change_map


def validate_crosswalk_v2(value: dict[str, Any]) -> dict[str, int]:
    if value.get("schema_version") != "catalytic-earth.atlas50-crosswalk-v2.v1":
        raise ValueError("unsupported Atlas-50 crosswalk v2 schema")
    if value.get("review_independence") != REVIEW_INDEPENDENCE:
        raise ValueError("Atlas-50 crosswalk v2 must disclose correlated same-model review")
    rows = value.get("rows")
    if not isinstance(rows, list) or len(rows) != 57:
        raise ValueError("Atlas-50 crosswalk v2 must contain exactly 57 rows")
    if [row.get("ordinal") for row in rows] != list(range(1, 58)):
        raise ValueError("Atlas-50 crosswalk v2 ordinals must be 1..57")
    if len({row.get("fingerprint_id") for row in rows}) != 57:
        raise ValueError("Atlas-50 crosswalk v2 fingerprint IDs must be unique")

    for row in rows:
        fingerprint_id = row["fingerprint_id"]
        classification = row.get("computational_classification")
        if classification not in CLASSIFICATIONS:
            raise ValueError(f"{fingerprint_id} has unsupported classification")
        expected_status = (
            "computational_unresolved"
            if classification == "unresolved"
            else "computational_provisional_relation"
        )
        if row.get("status") != expected_status:
            raise ValueError(f"{fingerprint_id} status/classification mismatch")
        targets = row.get("relation_targets")
        if not isinstance(targets, list):
            raise ValueError(f"{fingerprint_id} relation_targets must be an array")
        seen: set[tuple[str, str, str]] = set()
        for target in targets:
            source_key = target.get("source_key")
            target_id = target.get("target_id")
            relation = target.get("relation")
            identity = target.get("source_identity")
            applicability = target.get("mechanistic_applicability")
            if source_key not in {"mcsa", "atlas50_fingerprint"}:
                raise ValueError(f"{fingerprint_id} relation target has unknown source")
            if not isinstance(target_id, str) or not (
                _MCSA_RE.fullmatch(target_id) or _INTERNAL_RE.fullmatch(target_id)
            ):
                raise ValueError(f"{fingerprint_id} relation target has invalid ID")
            if relation not in RELATIONS:
                raise ValueError(f"{fingerprint_id} relation target has invalid relation")
            if not isinstance(identity, dict) or not identity.get("name"):
                raise ValueError(f"{fingerprint_id} source identity is not explicit")
            if identity.get("status") not in {
                "official_entry_checked",
                "frozen_fingerprint_identity",
            }:
                raise ValueError(f"{fingerprint_id} source identity is not checked")
            if not isinstance(applicability, dict) or not applicability.get("status"):
                raise ValueError(
                    f"{fingerprint_id} mechanistic applicability is not explicit"
                )
            key = (source_key, target_id, relation)
            if key in seen:
                raise ValueError(f"{fingerprint_id} has duplicate relation target")
            seen.add(key)
            if (
                relation == "exact_duplicate"
                and applicability["status"] == "exact_scope_supported"
                and (
                    fingerprint_id,
                    target_id,
                    applicability.get("scope"),
                )
                not in EXACT_SCOPE_ALLOWLIST
            ):
                raise ValueError(
                    f"{fingerprint_id} exact equivalence is not supported at that scope"
                )

        if classification in {
            "aggregation",
            "specialization",
            "interoperability_bridge",
        }:
            if not any(
                target["relation"] == classification
                and target["mechanistic_applicability"]["status"]
                in POSITIVE_APPLICABILITY
                for target in targets
            ):
                raise ValueError(
                    f"{fingerprint_id} non-unresolved relation lacks a named, "
                    "applicable target"
                )
        if classification == "exact_duplicate":
            if not any(
                target["relation"] == "exact_duplicate"
                and target["mechanistic_applicability"]["status"]
                == "exact_scope_supported"
                for target in targets
            ):
                raise ValueError(
                    f"{fingerprint_id} exact_duplicate requires a source-checked "
                    "target with exact supported scope"
                )
        if fingerprint_id == "plp_dependent_enzyme":
            positive_m0049 = [
                target
                for target in targets
                if target["target_id"] == "M0049"
                and target["relation"] != "rejected_mapping"
            ]
            if positive_m0049:
                raise ValueError("M0049 cannot be positive PLP evidence")

    counts = Counter(row["computational_classification"] for row in rows)
    if dict(sorted(counts.items())) != value.get("classification_counts"):
        raise ValueError("Atlas-50 crosswalk v2 classification counts differ")
    if value.get("row_count") != 57:
        raise ValueError("Atlas-50 crosswalk v2 row_count differs")
    return dict(counts)


def validate_change_map(
    value: dict[str, Any], crosswalk: dict[str, Any]
) -> None:
    if value.get("schema_version") != (
        "catalytic-earth.atlas50-crosswalk-v2-change-map.v1"
    ):
        raise ValueError("unsupported Atlas-50 v2 change-map schema")
    if value.get("review_independence") != REVIEW_INDEPENDENCE:
        raise ValueError("Atlas-50 v2 change map must disclose correlated same-model review")
    changes = value.get("changes")
    if not isinstance(changes, list) or len(changes) != 57:
        raise ValueError("Atlas-50 v2 change map must contain exactly 57 rows")
    crosswalk_ids = [row["fingerprint_id"] for row in crosswalk["rows"]]
    if [change.get("fingerprint_id") for change in changes] != crosswalk_ids:
        raise ValueError("Atlas-50 v2 change map row order differs")
    if not all(change.get("reason") for change in changes):
        raise ValueError("Atlas-50 v2 change map requires a reason for every row")


def build_crosswalk_v2_outputs(repo_root: Path) -> dict[str, dict[str, Any]]:
    phase_a, phase_digest = _load_pinned_json(repo_root, PHASE_A_RELATIVE)
    review, review_digest = _load_pinned_json(repo_root, REVIEW_RELATIVE)
    input_hashes = {
        PHASE_A_RELATIVE.as_posix(): phase_digest,
        REVIEW_RELATIVE.as_posix(): review_digest,
    }
    crosswalk, change_map = build_crosswalk_v2_documents(
        phase_a, review, input_hashes=input_hashes
    )
    outputs = {
        "crosswalk.json": crosswalk,
        "change_map.json": change_map,
    }
    manifest = {
        "schema_version": "catalytic-earth.atlas50-crosswalk-v2-manifest.v1",
        "manifest_id": "atlas50.crosswalk-v2.manifest.2026-09-05.v1",
        "status": "computational_provisional_not_human_review",
        "inputs": [
            {"path": path, "sha256": digest}
            for path, digest in sorted(input_hashes.items())
        ],
        "outputs": [
            {"path": filename, "sha256": _sha256(canonical_json_bytes(value))}
            for filename, value in sorted(outputs.items())
        ],
        "row_count": 57,
        "frozen_phase_a_or_b_modified": False,
        "protected_registry_modified": False,
        "independent_human_review_claimed": False,
        "experimental_validation_claimed": False,
        "review_independence": dict(REVIEW_INDEPENDENCE),
    }
    outputs["manifest.json"] = manifest
    return outputs
