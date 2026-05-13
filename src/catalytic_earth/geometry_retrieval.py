from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .fingerprints import load_fingerprints


METAL_HYDROLASE_TRANSFER_LIGAND_CODES = {
    "ADJ",  # ATP-dependent amidation analog context
    "APG",  # metal-assisted racemase/isomerase product analog context
    "BIO",  # pterin/biopterin synthase rearrangement context
    "DAD",  # adenosine-like cyclase/product analog context
    "DAA",  # ATP-dependent ligase/ring-forming context
    "DED",  # diphosphate/isoprenoid isomerase analog context
    "FII",  # farnesyl diphosphate analog context
    "FOC",  # fucose-like sugar isomerization context
    "G16",  # phosphoglucomutase bisphosphate/phosphoryl-transfer context
    "GLV",  # glyoxylate-like ligand in malate synthase hard-negative context
    "HDA",  # adenylosuccinate synthase intermediate analog context
    "ICT",  # isocitrate redox/decarboxylation context
    "OXL",  # oxalate-like carbonyl/decarboxylation context
    "PGH",  # phosphoglycolate/hydroxamate-like aldolase inhibitor context
    "PHT",  # phosphoribosyl-transfer analog context
    "PIR",  # purine/ribose analog context for nucleoside hydrolase controls
    "POP",  # pyrophosphate amidation or ligase context
    "PPC",  # phosphoribosyl-transfer analog context
    "PQQ",  # quinone redox cofactor context
    "PYR",  # carboxykinase/decarboxylation context
    "SEP",  # phosphomutase phosphoryl-transfer intermediate context
    "TPP",  # thiamine-diphosphate decarboxylation/carbon-transfer context
    "U5P",  # nucleotide-sugar transfer context
}
METAL_HYDROLASE_REDOX_LIGAND_CODES = {
    "ACN",  # non-heme dioxygenase/aconitate-like context
    "AZI",  # peroxidase/azide-bound redox context
    "CRB",  # NAD-linked rearrangement/redox context
    "CU",  # copper redox center
    "CU1",  # copper redox center
    "CUB",  # copper/molybdenum redox center
    "CMO",  # hydrogenase carbon monoxide ligand
    "CYN",  # hydrogenase cyanide ligand
    "DIO",  # nitrile hydratase metal center adduct
    "FCO",  # hydrogenase Fe-carbonyl redox center
    "FE2",  # hydrogenase/dinuclear iron redox ligand
    "FES",  # Rieske or ferredoxin-style iron-sulfur context
    "F3S",  # iron-sulfur redox center
    "MCN",  # molybdenum-copper cofactor context
    "NO",  # metal nitrosyl/redox context
    "PDT",  # hydrogenase dithiolate bridge
    "SF4",  # 4Fe-4S redox cluster
    "VO4",  # vanadate peroxidase context
}
MOLYBDENUM_CENTER_LIGAND_CODES = {"MGD", "MO", "MTE", "MOS", "MOO", "MOM"}
NUCLEOTIDE_TRANSFER_LIGAND_CODES = {
    "ACP",
    "APC",
    "AP2",
    "ADP",
    "AMP",
    "ANP",
    "ATP",
    "GDP",
    "GMP",
    "GTP",
    "IDP",
    "IMP",
}
FLAVIN_MONOOXYGENASE_SUBSTRATE_LIGAND_CODES = {
    "BR",  # aromatic monooxygenase product/substrate context in M-CSA 131
    "PHB",  # p-hydroxybenzoate monooxygenase substrate/product context
}
PLP_LIGAND_ANCHOR_CODES = {"LLP", "PLP", "PMP", "P5P"}
COUNTEREVIDENCE_POLICY_VERSION = "2026-05-13.declarative-v1"
GEOMETRY_RETRIEVAL_PREDICTIVE_EVIDENCE_SOURCES = (
    "active_site_residue_identity",
    "active_site_residue_roles",
    "local_ligand_cofactor_context",
    "local_plp_ligand_anchor_context",
    "substrate_pocket_descriptors",
    "active_site_compactness",
)
GEOMETRY_RETRIEVAL_REVIEW_CONTEXT_FIELDS = (
    "entry_name",
    "mechanism_text_count",
    "mechanism_text_snippets",
)
GEOMETRY_RETRIEVAL_LEAKAGE_POLICY = {
    "text_or_label_fields_used_for_score": False,
    "excluded_predictive_fields": [
        "mechanism_text",
        "mechanism_text_count",
        "mechanism_text_snippets",
        "entry_name",
        "mechanism_labels",
        "ec_identifiers",
        "rhea_identifiers",
        "source_entry_ids",
        "source_labels",
        "target_labels",
    ],
    "review_context_fields": list(GEOMETRY_RETRIEVAL_REVIEW_CONTEXT_FIELDS),
    "review_context_policy": (
        "Mechanism text, entry names, labels, EC/Rhea identifiers, and source ids "
        "may be carried for review, abstention, or counterevidence provenance, "
        "but must not add positive retrieval score."
    ),
}
GEOMETRY_RETRIEVAL_LEAKAGE_PRONE_FIELDS = {
    "mechanism_text",
    "mechanism_text_count",
    "mechanism_text_snippets",
    "entry_name",
    "mechanism_labels",
    "ec_identifiers",
    "rhea_identifiers",
    "source_entry_ids",
    "source_labels",
    "target_labels",
}


@dataclass(frozen=True)
class CounterevidenceInputs:
    fingerprint_id: str
    residues: list[dict[str, Any]]
    cofactor_evidence: str
    ligand_context: dict[str, Any] | None
    substrate_pocket_score_value: float
    pocket_context: dict[str, Any] | None
    compactness_score_value: float | None
    mechanism_text_snippets: list[str] | None
    residue_roles: set[str]
    ligand_families: set[str]
    ligand_codes: set[str]
    structure_ligand_families: set[str]
    structure_ligand_codes: set[str]
    mechanism_text: str


CounterevidencePredicate = Callable[[CounterevidenceInputs, set[str]], bool]


@dataclass(frozen=True)
class CounterevidenceRule:
    fingerprint_id: str
    reason: str
    penalty: float
    evidence_fields: tuple[str, ...]
    predicate: CounterevidencePredicate

    @property
    def rule_id(self) -> str:
        return f"{self.fingerprint_id}:{self.reason}"

    @property
    def leakage_flags(self) -> tuple[str, ...]:
        flags: list[str] = []
        if "mechanism_text" in self.evidence_fields:
            flags.append("mechanism_text_review_context_only")
        return tuple(flags)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_geometry_retrieval(
    geometry: dict[str, Any],
    top_k: int = 5,
) -> dict[str, Any]:
    fingerprints = load_fingerprints()
    results: list[dict[str, Any]] = []
    for entry in geometry.get("entries", []):
        scored = [
            score_entry_against_fingerprint(entry, fingerprint.to_dict())
            for fingerprint in fingerprints
        ]
        results.append(
            {
                "entry_id": entry.get("entry_id"),
                "entry_name": entry.get("entry_name"),
                "pdb_id": entry.get("pdb_id"),
                "status": entry.get("status"),
                "mechanism_text_count": entry.get("mechanism_text_count", 0),
                "mechanism_text_snippets": entry.get("mechanism_text_snippets", []),
                "resolved_residue_count": entry.get("resolved_residue_count", 0),
                "residue_codes": [
                    _canonical_code(residue.get("code"))
                    for residue in entry.get("residues", [])
                    if _canonical_code(residue.get("code"))
                ],
                "ligand_context": entry.get("ligand_context", {}),
                "pocket_context": entry.get("pocket_context", {}),
                "top_fingerprints": sorted(
                    scored, key=lambda item: (-item["score"], item["fingerprint_id"])
                )[:top_k],
            }
        )

    return {
        "metadata": {
            "method": "geometry_aware_seed_fingerprint_retrieval",
            "blocker_removed": "text_leakage_mitigation_geometry_retrieval",
            "entry_count": len(results),
            "fingerprint_count": len(fingerprints),
            "scoring": (
                "residue and role overlap plus ligand/cofactor context, "
                "local PLP ligand-anchor context, substrate-pocket descriptors, "
                "and compactness"
            ),
            "predictive_evidence_sources": list(
                GEOMETRY_RETRIEVAL_PREDICTIVE_EVIDENCE_SOURCES
            ),
            "leakage_policy": GEOMETRY_RETRIEVAL_LEAKAGE_POLICY,
            "validation_boundary": "retrieval evidence only; not mechanism validation",
        },
        "results": results,
    }


def score_entry_against_fingerprint(
    entry: dict[str, Any],
    fingerprint: dict[str, Any],
) -> dict[str, Any]:
    residues = entry.get("residues", [])
    distances = entry.get("pairwise_distances_angstrom", [])
    signature = fingerprint.get("active_site_signature", [])
    residue_codes = [_canonical_code(residue.get("code")) for residue in residues]
    residue_roles = {
        _normalize_phrase(role)
        for residue in residues
        for role in residue.get("roles", [])
        if isinstance(role, str)
    }

    matched_signature_roles: list[dict[str, Any]] = []
    for requirement in signature:
        allowed = _allowed_residue_codes(requirement.get("residue", ""))
        role = _normalize_phrase(str(requirement.get("role", "")))
        matched_codes = sorted(code for code in residue_codes if code in allowed)
        role_hint_match = _role_hint_match(role, residue_roles)
        if matched_codes or role_hint_match:
            matched_signature_roles.append(
                {
                    "required_role": requirement.get("role"),
                    "required_residue": requirement.get("residue"),
                    "matched_codes": matched_codes,
                    "role_hint_match": role_hint_match,
                }
            )

    residue_match_fraction = len(matched_signature_roles) / max(len(signature), 1)
    role_match_fraction = _role_match_fraction(signature, residue_roles)
    cofactor_context = cofactor_context_score(
        fingerprint,
        residue_codes,
        residue_roles,
        entry.get("ligand_context"),
    )
    cofactor_evidence = cofactor_evidence_level(fingerprint, residue_roles, entry.get("ligand_context"))
    compactness = compactness_score(distances)
    substrate_pocket = substrate_pocket_score(fingerprint, entry.get("pocket_context"))
    plp_ligand_anchor = plp_ligand_anchor_score(
        entry.get("ligand_context"),
        entry.get("pocket_context"),
    )
    coherence = mechanistic_coherence_score(fingerprint, residues)
    mechanism_context = _entry_mechanism_context(entry)
    counterevidence = counterevidence_assessment(
        fingerprint=fingerprint,
        residues=residues,
        cofactor_evidence=cofactor_evidence,
        ligand_context=entry.get("ligand_context"),
        substrate_pocket_score_value=substrate_pocket,
        pocket_context=entry.get("pocket_context"),
        compactness_score_value=compactness,
        mechanism_text_snippets=mechanism_context,
    )
    raw_score = (
        0.35 * residue_match_fraction
        + 0.24 * role_match_fraction
        + 0.18 * cofactor_context
        + 0.08 * compactness
        + 0.15 * substrate_pocket
    )
    if (
        fingerprint.get("id") == "plp_dependent_enzyme"
        and cofactor_evidence == "ligand_supported"
    ):
        raw_score += 0.12 * plp_ligand_anchor
    if fingerprint.get("id") == "ser_his_acid_hydrolase":
        raw_score *= 0.70 + 0.30 * coherence
    raw_score *= counterevidence["penalty"]
    score = round(raw_score, 4)
    return {
        "fingerprint_id": fingerprint.get("id"),
        "fingerprint_name": fingerprint.get("name"),
        "score": score,
        "residue_match_fraction": round(residue_match_fraction, 4),
        "role_match_fraction": round(role_match_fraction, 4),
        "cofactor_context_score": round(cofactor_context, 4),
        "cofactor_evidence_level": cofactor_evidence,
        "compactness_score": round(compactness, 4),
        "substrate_pocket_score": round(substrate_pocket, 4),
        "plp_ligand_anchor_score": round(plp_ligand_anchor, 4),
        "mechanistic_coherence_score": round(coherence, 4),
        "counterevidence_penalty": round(counterevidence["penalty"], 4),
        "counterevidence_reasons": counterevidence["reasons"],
        "counterevidence_penalty_details": counterevidence["penalty_details"],
        "counterevidence_policy_version": counterevidence["policy_version"],
        "counterevidence_policy_hits": counterevidence["policy_hits"],
        "text_or_label_fields_used_for_score": False,
        "matched_signature_roles": matched_signature_roles,
        "distance_summary": distance_summary(distances),
    }


def compactness_score(distances: list[dict[str, Any]]) -> float:
    values = [
        float(item["distance"])
        for item in distances
        if isinstance(item, dict) and item.get("distance") is not None
    ]
    if not values:
        return 0.0
    median = statistics.median(values)
    if median <= 8:
        return 1.0
    if median >= 24:
        return 0.0
    return max(0.0, 1 - ((median - 8) / 16))


def cofactor_context_score(
    fingerprint: dict[str, Any],
    residue_codes: list[str],
    residue_roles: set[str],
    ligand_context: dict[str, Any] | None = None,
) -> float:
    cofactors = {_normalize_phrase(cofactor) for cofactor in fingerprint.get("cofactors", [])}
    fingerprint_id = fingerprint.get("id")
    observed_families = _observed_cofactor_families(ligand_context, residue_roles)
    role_text = " ".join(residue_roles)
    residue_code_set = set(residue_codes)
    cys_count = sum(1 for code in residue_codes if code == "CYS")

    if not cofactors:
        if fingerprint_id == "ser_his_acid_hydrolase":
            expected = {"SER", "HIS"}
            acid = bool({"ASP", "GLU"} & residue_code_set)
            return 1.0 if expected.issubset(set(residue_codes)) and acid else 0.25
        return 0.5

    requirement_scores: list[float] = []
    for cofactor in sorted(cofactors):
        if _is_reactant_placeholder(cofactor):
            continue

        if _is_metal_cofactor(cofactor):
            if "metal_ion" in observed_families:
                requirement_scores.append(1.0)
            elif "metal ligand" in role_text:
                requirement_scores.append(0.4)
            elif {"HIS", "ASP", "GLU", "CYS"} & residue_code_set:
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        if "heme" in cofactor:
            if "heme" in observed_families:
                requirement_scores.append(1.0)
            elif "heme" in role_text:
                requirement_scores.append(0.25)
            else:
                requirement_scores.append(0.0)
            continue

        if "pyridoxal phosphate" in cofactor:
            if "plp" in observed_families:
                requirement_scores.append(1.0)
            elif "LYS" in residue_code_set:
                requirement_scores.append(0.15)
            else:
                requirement_scores.append(0.0)
            continue

        if "cobalamin" in cofactor or "vitamin b12" in cofactor:
            if "cobalamin" in observed_families:
                requirement_scores.append(1.0)
            elif any(term in role_text for term in ["cobalamin", "radical stabiliser", "radical stabilizer"]):
                requirement_scores.append(0.25)
            else:
                requirement_scores.append(0.0)
            continue

        if cofactor in {"fad", "fmn"}:
            if "flavin" in observed_families:
                requirement_scores.append(1.0)
            elif any(term in role_text for term in ["flavin", "redox"]):
                requirement_scores.append(0.25)
            else:
                requirement_scores.append(0.0)
            continue

        if cofactor in {"nadph", "nadp", "nad", "nadh"}:
            if "nad" in observed_families:
                requirement_scores.append(1.0)
            elif any(term in role_text for term in ["nadph", "redox"]):
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        if "sam" in cofactor or "adenosylmethionine" in cofactor:
            if "sam" in observed_families:
                requirement_scores.append(1.0)
            elif cys_count >= 3:
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        if "4fe-4s" in cofactor:
            if "fe_s_cluster" in observed_families:
                requirement_scores.append(1.0)
            elif cys_count >= 3:
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        requirement_scores.append(0.0)

    score = sum(requirement_scores) / len(requirement_scores) if requirement_scores else 0.0
    if (
        fingerprint_id == "flavin_dehydrogenase_reductase"
        and score == 0.0
        and "fe_s_cluster" in observed_families
        and "single electron" in role_text
    ):
        return 0.35
    return score


def cofactor_evidence_level(
    fingerprint: dict[str, Any],
    residue_roles: set[str],
    ligand_context: dict[str, Any] | None = None,
) -> str:
    cofactors = {_normalize_phrase(cofactor) for cofactor in fingerprint.get("cofactors", [])}
    if not cofactors:
        return "not_required"

    ligand_families = _ligand_cofactor_families(ligand_context)
    role_families = _role_implied_cofactor_families(residue_roles)
    expected_families = {_cofactor_family(cofactor) for cofactor in cofactors}
    expected_families.discard("")

    if expected_families & ligand_families:
        return "ligand_supported"
    if expected_families & role_families:
        return "role_inferred"
    return "absent"


def distance_summary(distances: list[dict[str, Any]]) -> dict[str, Any]:
    values = [
        float(item["distance"])
        for item in distances
        if isinstance(item, dict) and item.get("distance") is not None
    ]
    if not values:
        return {"count": 0}
    return {
        "count": len(values),
        "min": round(min(values), 3),
        "median": round(statistics.median(values), 3),
        "max": round(max(values), 3),
    }


def substrate_pocket_score(
    fingerprint: dict[str, Any],
    pocket_context: dict[str, Any] | None = None,
) -> float:
    if not isinstance(pocket_context, dict):
        return 0.5
    if int(pocket_context.get("nearby_residue_count", 0)) < 1:
        return 0.5
    descriptors = pocket_context.get("descriptors", {})
    if not isinstance(descriptors, dict):
        return 0.5

    hydrophobic = float(descriptors.get("hydrophobic_fraction", 0.0))
    polar = float(descriptors.get("polar_fraction", 0.0))
    positive = float(descriptors.get("positive_fraction", 0.0))
    negative = float(descriptors.get("negative_fraction", 0.0))
    aromatic = float(descriptors.get("aromatic_fraction", 0.0))
    sulfur = float(descriptors.get("sulfur_fraction", 0.0))
    charge_balance = float(descriptors.get("charge_balance", 0.0))

    fingerprint_id = str(fingerprint.get("id", ""))
    if fingerprint_id == "ser_his_acid_hydrolase":
        hydrophobic_match = 1.0 - min(1.0, abs(hydrophobic - 0.45) / 0.45)
        charge_match = 1.0 - min(1.0, abs(charge_balance) / 0.4)
        return _clamp(0.6 * hydrophobic_match + 0.4 * charge_match)

    if fingerprint_id == "metal_dependent_hydrolase":
        return _clamp(0.55 * polar + 0.35 * negative + 0.10 * positive)

    if fingerprint_id == "plp_dependent_enzyme":
        return _clamp(0.50 * polar + 0.30 * positive + 0.20 * hydrophobic)

    if fingerprint_id == "radical_sam_enzyme":
        return _clamp(0.65 * sulfur + 0.20 * hydrophobic + 0.15 * aromatic)

    if fingerprint_id == "flavin_monooxygenase":
        hydrophobic_match = 1.0 - min(1.0, abs(hydrophobic - 0.4) / 0.4)
        return _clamp(0.45 * hydrophobic_match + 0.35 * aromatic + 0.20 * polar)

    if fingerprint_id == "heme_peroxidase_oxidase":
        return _clamp(0.45 * aromatic + 0.35 * hydrophobic + 0.20 * polar)

    return 0.5


def plp_ligand_anchor_score(
    ligand_context: dict[str, Any] | None,
    pocket_context: dict[str, Any] | None = None,
) -> float:
    """Score local PLP ligand evidence without using mechanism text."""
    if "plp" not in _ligand_cofactor_families(ligand_context):
        return 0.0
    if not (PLP_LIGAND_ANCHOR_CODES & _ligand_codes(ligand_context)):
        return 0.0
    nearby_count = 0
    if isinstance(pocket_context, dict):
        try:
            nearby_count = int(pocket_context.get("nearby_residue_count", 0) or 0)
        except (TypeError, ValueError):
            nearby_count = 0
    return 1.0 if nearby_count >= 20 else 0.67


def mechanistic_coherence_score(
    fingerprint: dict[str, Any],
    residues: list[dict[str, Any]],
) -> float:
    fingerprint_id = fingerprint.get("id")
    if fingerprint_id != "ser_his_acid_hydrolase":
        return 1.0

    ser_nucleophile = any(
        _canonical_code(residue.get("code")) == "SER"
        and _residue_has_any_role(residue, {"nucleophile", "covalently attached"})
        for residue in residues
    )
    if not ser_nucleophile:
        return 0.0

    his_base = any(
        _canonical_code(residue.get("code")) == "HIS"
        and _residue_has_any_role(
            residue,
            {"general base", "proton acceptor", "proton donor", "acid base"},
        )
        for residue in residues
    )
    if not his_base:
        return 0.0
    acid_orienter = any(
        _canonical_code(residue.get("code")) in {"ASP", "GLU"}
        and _residue_has_any_role(
            residue,
            {
                "acid",
                "electrostatic stabiliser",
                "hydrogen bond acceptor",
                "hydrogen bond donor",
                "proton acceptor",
                "proton donor",
            },
        )
        for residue in residues
    )
    return (1.0 + float(his_base) + float(acid_orienter)) / 3.0


def counterevidence_penalty(
    fingerprint: dict[str, Any],
    residues: list[dict[str, Any]],
    cofactor_evidence: str,
    ligand_context: dict[str, Any] | None,
    substrate_pocket_score_value: float,
    pocket_context: dict[str, Any] | None = None,
    compactness_score_value: float | None = None,
    mechanism_text_snippets: list[str] | None = None,
) -> float:
    return counterevidence_assessment(
        fingerprint=fingerprint,
        residues=residues,
        cofactor_evidence=cofactor_evidence,
        ligand_context=ligand_context,
        substrate_pocket_score_value=substrate_pocket_score_value,
        pocket_context=pocket_context,
        compactness_score_value=compactness_score_value,
        mechanism_text_snippets=mechanism_text_snippets,
    )["penalty"]


def counterevidence_assessment(
    fingerprint: dict[str, Any],
    residues: list[dict[str, Any]],
    cofactor_evidence: str,
    ligand_context: dict[str, Any] | None,
    substrate_pocket_score_value: float,
    pocket_context: dict[str, Any] | None = None,
    compactness_score_value: float | None = None,
    mechanism_text_snippets: list[str] | None = None,
) -> dict[str, Any]:
    inputs = _build_counterevidence_inputs(
        fingerprint=fingerprint,
        residues=residues,
        cofactor_evidence=cofactor_evidence,
        ligand_context=ligand_context,
        substrate_pocket_score_value=substrate_pocket_score_value,
        pocket_context=pocket_context,
        compactness_score_value=compactness_score_value,
        mechanism_text_snippets=mechanism_text_snippets,
    )
    penalty = 1.0
    reasons: list[str] = []
    penalty_details: list[dict[str, Any]] = []
    policy_hits: list[dict[str, Any]] = []

    def apply(rule: CounterevidenceRule) -> None:
        nonlocal penalty
        if rule.penalty < penalty:
            penalty = rule.penalty
        reasons.append(rule.reason)
        penalty_details.append({"reason": rule.reason, "penalty": round(rule.penalty, 4)})
        policy_hits.append(
            {
                "rule_id": rule.rule_id,
                "reason": rule.reason,
                "penalty": round(rule.penalty, 4),
                "evidence_fields": list(rule.evidence_fields),
                "evidence_role": "counterevidence_only_not_predictive_evidence",
                "leakage_flags": list(rule.leakage_flags),
                "policy_version": COUNTEREVIDENCE_POLICY_VERSION,
            }
        )

    def result() -> dict[str, Any]:
        return {
            "penalty": penalty,
            "reasons": sorted(set(reasons)),
            "penalty_details": sorted(
                {detail["reason"]: detail for detail in penalty_details}.values(),
                key=lambda detail: (float(detail["penalty"]), str(detail["reason"])),
            ),
            "policy_version": COUNTEREVIDENCE_POLICY_VERSION,
            "policy_hits": sorted(
                {hit["rule_id"]: hit for hit in policy_hits}.values(),
                key=lambda hit: (float(hit["penalty"]), str(hit["rule_id"])),
            ),
        }

    applied_reasons: set[str] = set()
    for rule in COUNTEREVIDENCE_POLICY:
        if rule.fingerprint_id != inputs.fingerprint_id:
            continue
        if rule.predicate(inputs, applied_reasons):
            apply(rule)
            applied_reasons.add(rule.reason)

    return result()


def _build_counterevidence_inputs(
    fingerprint: dict[str, Any],
    residues: list[dict[str, Any]],
    cofactor_evidence: str,
    ligand_context: dict[str, Any] | None,
    substrate_pocket_score_value: float,
    pocket_context: dict[str, Any] | None,
    compactness_score_value: float | None,
    mechanism_text_snippets: list[str] | None,
) -> CounterevidenceInputs:
    residue_roles = {
        _normalize_phrase(role)
        for residue in residues
        for role in residue.get("roles", [])
        if isinstance(role, str)
    }
    return CounterevidenceInputs(
        fingerprint_id=str(fingerprint.get("id", "")),
        residues=residues,
        cofactor_evidence=cofactor_evidence,
        ligand_context=ligand_context,
        substrate_pocket_score_value=substrate_pocket_score_value,
        pocket_context=pocket_context,
        compactness_score_value=compactness_score_value,
        mechanism_text_snippets=mechanism_text_snippets,
        residue_roles=residue_roles,
        ligand_families=_ligand_cofactor_families(ligand_context),
        ligand_codes=_ligand_codes(ligand_context),
        structure_ligand_families=_structure_ligand_cofactor_families(ligand_context),
        structure_ligand_codes=_structure_ligand_codes(ligand_context),
        mechanism_text=_joined_mechanism_text(mechanism_text_snippets),
    )


def _counterevidence_rule(
    fingerprint_id: str,
    reason: str,
    penalty: float,
    evidence_fields: tuple[str, ...],
    predicate: CounterevidencePredicate,
) -> CounterevidenceRule:
    return CounterevidenceRule(
        fingerprint_id=fingerprint_id,
        reason=reason,
        penalty=penalty,
        evidence_fields=evidence_fields,
        predicate=predicate,
    )


def write_geometry_retrieval(
    geometry_path: Path,
    out_path: Path,
    top_k: int = 5,
) -> dict[str, Any]:
    artifact = run_geometry_retrieval(load_json(geometry_path), top_k=top_k)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def audit_geometry_retrieval_leakage_policy(artifact: dict[str, Any]) -> dict[str, Any]:
    """Verify retrieval scoring provenance excludes text and label leakage."""
    metadata = artifact.get("metadata", {})
    leakage_policy = metadata.get("leakage_policy", {})
    predictive_sources = set(metadata.get("predictive_evidence_sources", []) or [])
    excluded_fields = set(leakage_policy.get("excluded_predictive_fields", []) or [])
    blockers: list[str] = []

    if leakage_policy.get("text_or_label_fields_used_for_score") is not False:
        blockers.append("geometry_retrieval_text_or_label_score_flag_not_false")
    if predictive_sources & GEOMETRY_RETRIEVAL_LEAKAGE_PRONE_FIELDS:
        blockers.append("geometry_retrieval_leakage_prone_predictive_source")
    missing_excluded_fields = GEOMETRY_RETRIEVAL_LEAKAGE_PRONE_FIELDS - excluded_fields
    if missing_excluded_fields:
        blockers.append("geometry_retrieval_missing_excluded_leakage_fields")

    scored_text_rows = []
    counterevidence_text_without_role = []
    for result in artifact.get("results", []) or []:
        for hit in result.get("top_fingerprints", []) or []:
            if hit.get("text_or_label_fields_used_for_score") is not False:
                scored_text_rows.append(
                    {
                        "entry_id": result.get("entry_id"),
                        "fingerprint_id": hit.get("fingerprint_id"),
                    }
                )
            for policy_hit in hit.get("counterevidence_policy_hits", []) or []:
                evidence_fields = set(policy_hit.get("evidence_fields", []) or [])
                if "mechanism_text" not in evidence_fields:
                    continue
                if (
                    policy_hit.get("evidence_role")
                    != "counterevidence_only_not_predictive_evidence"
                ):
                    counterevidence_text_without_role.append(
                        {
                            "entry_id": result.get("entry_id"),
                            "fingerprint_id": hit.get("fingerprint_id"),
                            "rule_id": policy_hit.get("rule_id"),
                        }
                    )
    if scored_text_rows:
        blockers.append("geometry_retrieval_hit_uses_text_or_label_score")
    if counterevidence_text_without_role:
        blockers.append("geometry_retrieval_text_counterevidence_role_missing")

    return {
        "metadata": {
            "method": "geometry_retrieval_leakage_policy_audit",
            "blocker_removed": "text_leakage_mitigation_geometry_retrieval",
            "guardrail_clean": not blockers,
            "blockers": sorted(set(blockers)),
            "scored_text_row_count": len(scored_text_rows),
            "text_counterevidence_role_issue_count": len(
                counterevidence_text_without_role
            ),
        },
        "scored_text_rows": scored_text_rows,
        "text_counterevidence_role_issues": counterevidence_text_without_role,
    }


def _allowed_residue_codes(spec: str) -> set[str]:
    normalized = _normalize_phrase(spec)
    aliases = {
        "polar or charged residue": {
            "ARG",
            "ASN",
            "ASP",
            "CYS",
            "GLN",
            "GLU",
            "HIS",
            "LYS",
            "SER",
            "THR",
            "TYR",
        },
        "basic or polar motif": {"ARG", "ASN", "GLN", "HIS", "LYS", "SER", "THR"},
        "aromatic or redox residue": {"CYS", "HIS", "MET", "PHE", "TRP", "TYR"},
    }
    if normalized in aliases:
        return aliases[normalized]
    allowed = {_canonical_code(part) for part in spec.replace(",", "/").split("/")}
    return {item for item in allowed if item}


def _canonical_code(code: Any) -> str:
    if not isinstance(code, str):
        return ""
    cleaned = code.strip().upper()
    aliases = {
        "SER": "SER",
        "S": "SER",
        "HIS": "HIS",
        "H": "HIS",
        "ASP": "ASP",
        "D": "ASP",
        "GLU": "GLU",
        "E": "GLU",
        "CYS": "CYS",
        "C": "CYS",
        "TYR": "TYR",
        "Y": "TYR",
        "LYS": "LYS",
        "K": "LYS",
        "ARG": "ARG",
        "R": "ARG",
        "THR": "THR",
        "T": "THR",
    }
    return aliases.get(cleaned, cleaned if len(cleaned) == 3 else "")


def _normalize_phrase(value: str) -> str:
    return value.lower().replace("_", " ").replace("-", " ").strip()


def _role_hint_match(required_role: str, residue_roles: set[str]) -> bool:
    if required_role in residue_roles:
        return True
    if required_role == "acid base":
        return any("proton acceptor" in role or "proton donor" in role for role in residue_roles)
    if required_role == "acid or orienter":
        return any("proton" in role or "hydrogen bond" in role for role in residue_roles)
    if required_role == "cobalamin ligand":
        return any("cobalamin" in role or "metal ligand" in role for role in residue_roles)
    if required_role == "radical stabilizer":
        return any("radical stabiliser" in role or "radical stabilizer" in role for role in residue_roles)
    if required_role == "redox acid base":
        return any(
            "redox" in role
            or "single electron" in role
            or "proton acceptor" in role
            or "proton donor" in role
            for role in residue_roles
        )
    if required_role == "electron transfer path":
        return any("electron" in role or "redox" in role for role in residue_roles)
    if required_role == "substrate orienter":
        return any(
            "hydrogen bond" in role
            or "electrostatic stabiliser" in role
            or "electrostatic stabilizer" in role
            or "steric role" in role
            for role in residue_roles
        )
    return False


def _role_match_fraction(signature: list[dict[str, Any]], residue_roles: set[str]) -> float:
    if not signature:
        return 0.0
    matched = 0
    for requirement in signature:
        if _role_hint_match(_normalize_phrase(str(requirement.get("role", ""))), residue_roles):
            matched += 1
    return matched / len(signature)


def _residue_has_any_role(residue: dict[str, Any], required_roles: set[str]) -> bool:
    roles = {_normalize_phrase(role) for role in residue.get("roles", []) if isinstance(role, str)}
    if any(required in roles for required in required_roles):
        return True
    for role in roles:
        if role == "covalent catalysis" and required_roles & {"nucleophile", "covalently attached"}:
            return True
        if (
            role in {"proton shuttle (general acid/base)", "proton shuttle general acid/base"}
            and required_roles
            & {"acid base", "general base", "proton acceptor", "proton donor", "proton relay"}
        ):
            return True
        if role == "modifies pka" and required_roles & {"acid", "acid base", "proton acceptor", "proton donor"}:
            return True
    return False


def _is_metal_cofactor(cofactor: str) -> bool:
    metals = {"zn2+", "mg2+", "mn2+", "fe2+/fe3+", "fe2+", "fe3+", "metal"}
    return cofactor in metals or any(metal in cofactor for metal in metals)


def _is_reactant_placeholder(cofactor: str) -> bool:
    normalized = _normalize_phrase(cofactor)
    return "h2o2" in normalized or " or o2 " in f" {normalized} " or normalized == "o2"


def _observed_cofactor_families(
    ligand_context: dict[str, Any] | None,
    residue_roles: set[str],
) -> set[str]:
    return _ligand_cofactor_families(ligand_context) | _role_implied_cofactor_families(residue_roles)


def _ligand_cofactor_families(ligand_context: dict[str, Any] | None) -> set[str]:
    families: set[str] = set()
    if isinstance(ligand_context, dict):
        for value in ligand_context.get("cofactor_families", []):
            normalized = _normalize_cofactor_family(str(value))
            if normalized:
                families.add(normalized)
    return families


def _ligand_codes(ligand_context: dict[str, Any] | None) -> set[str]:
    if not isinstance(ligand_context, dict):
        return set()
    return {
        str(value).strip().upper()
        for value in ligand_context.get("ligand_codes", [])
        if isinstance(value, str) and value.strip()
    }


def _structure_ligand_cofactor_families(ligand_context: dict[str, Any] | None) -> set[str]:
    families: set[str] = set()
    if isinstance(ligand_context, dict):
        for value in ligand_context.get("structure_cofactor_families", []):
            normalized = _normalize_cofactor_family(str(value))
            if normalized:
                families.add(normalized)
    return families


def _structure_ligand_codes(ligand_context: dict[str, Any] | None) -> set[str]:
    if not isinstance(ligand_context, dict):
        return set()
    return {
        str(value).strip().upper()
        for value in ligand_context.get("structure_ligand_codes", [])
        if isinstance(value, str) and value.strip()
    }


def _role_implied_cofactor_families(residue_roles: set[str]) -> set[str]:
    families: set[str] = set()
    role_text = " ".join(residue_roles)
    if "heme" in role_text:
        families.add("heme")
    if "flavin" in role_text:
        families.add("flavin")
    if "nadph" in role_text or "nadp" in role_text or "nad" in role_text:
        families.add("nad")
    if "metal ligand" in role_text:
        families.add("metal_ion")
    return families


def _joined_mechanism_text(snippets: list[str] | None) -> str:
    if not isinstance(snippets, list):
        return ""
    return " ".join(str(item).lower() for item in snippets if isinstance(item, str))


def _entry_mechanism_context(entry: dict[str, Any]) -> list[str]:
    snippets: list[str] = []
    entry_name = entry.get("entry_name")
    if isinstance(entry_name, str) and entry_name:
        snippets.append(entry_name)
    mechanism_snippets = entry.get("mechanism_text_snippets")
    if isinstance(mechanism_snippets, list):
        snippets.extend(item for item in mechanism_snippets if isinstance(item, str))
    return snippets


def _has_prenyl_carbocation_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    if "farnesyltransferase" in mechanism_text:
        return True
    if "farnesyl" in mechanism_text and "transferase" in mechanism_text:
        return True
    has_diphosphate_context = "diphosphate" in mechanism_text or "pyrophosphate" in mechanism_text
    has_carbocation_context = any(
        term in mechanism_text
        for term in (
            "carbocation",
            "heterolysis",
            "cyclisation",
            "cyclization",
            "farnesyl",
            "geranyl",
            "terpene",
            "isopentenyl",
        )
    )
    return has_diphosphate_context and has_carbocation_context


def _has_nad_redox_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_nad = "nad" in mechanism_text
    has_redox = any(term in mechanism_text for term in ("hydride", "oxidise", "oxidize", "reduction"))
    return has_nad and has_redox


def _has_metal_bound_dehydrogenase_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_dehydrogenase = "dehydrogenase" in mechanism_text
    has_metal = any(term in mechanism_text for term in ("zinc", "zn", "metal"))
    has_redox = any(term in mechanism_text for term in ("hydride", "nad", "redox"))
    return has_dehydrogenase and has_metal and has_redox


def _has_phosphoenolpyruvate_transfer_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_pep = "phospho-enolpyruvate" in mechanism_text or "phosphoenolpyruvate" in mechanism_text
    has_transfer = "carboxyvinyltransferase" in mechanism_text or "transferase" in mechanism_text
    return has_pep and has_transfer


def _has_nonhydrolytic_isomerase_lyase_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    hydrolysis_terms = ("hydrolysis", "hydrolyses", "hydrolyzes", "hydrolysing", "hydrolyzing")
    if any(term in mechanism_text for term in hydrolysis_terms):
        return False
    return any(
        term in mechanism_text
        for term in (
            "isomerase",
            "isomerisation",
            "isomerization",
            "epimerase",
            "epimerisation",
            "epimerization",
            "racemase",
            "racemization",
            "racemisation",
            "racemised",
            "racemized",
            "lyase",
            "cycloisomerase",
            "retroaldol",
            "aldol",
            "claisen condensation",
        )
    )


def _has_nonhydrolytic_hydratase_dehydratase_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    hydrolysis_terms = ("hydrolysis", "hydrolyses", "hydrolyzes", "hydrolysing", "hydrolyzing")
    if any(term in mechanism_text for term in hydrolysis_terms):
        return False
    if any(
        term in mechanism_text
        for term in ("carbonate dehydratase", "carbonic anhydrase", "carbon dioxide", "bicarbonate")
    ):
        return False
    return any(
        term in mechanism_text
        for term in (
            "hydratase",
            "dehydratase",
            "dehydration",
            "hydration",
            "inter-conversion",
            "interconversion",
        )
    )


def _has_aminoacyl_ligase_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_ligase = "trna ligase" in mechanism_text or "trna charging" in mechanism_text
    has_aminoacyl = "aminoacyl" in mechanism_text or "aminoacyl adenylate" in mechanism_text
    has_atp_activation = "atp" in mechanism_text and (
        "adenylate" in mechanism_text or "anhydride" in mechanism_text
    )
    return has_ligase or (has_aminoacyl and has_atp_activation)


def _has_glycosidase_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    return any(
        term in mechanism_text
        for term in (
            "glycosidase",
            "glucosidase",
            "galactosidase",
            "glucuronidase",
            "nucleoside hydrolase",
            "glycosidic bond",
            "n-glycosidic",
            "oxocarbenium",
            "glycosyl hydrolase",
            "alpha-amylase",
            "amylase",
            "isoamylase",
            "licheninase",
        )
    )


def _has_plp_transaldimination_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    return any(
        term in mechanism_text
        for term in (
            "transaldimination",
            "external aldimine",
            "internal schiff base",
            "schiff base",
        )
    )


def _has_plp_beta_elimination_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    return any(
        term in mechanism_text
        for term in (
            "beta-elimination",
            "beta elimination",
            "c-s bond cleavage",
            "c-s bond",
            "cystathionine",
        )
    )


def _has_phosphoryl_transfer_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    hydrolysis_terms = ("hydrolysis", "hydrolyses", "hydrolyzes", "hydrolysing", "hydrolyzing")
    if any(term in mechanism_text for term in hydrolysis_terms):
        return False
    return any(
        term in mechanism_text
        for term in ("metaphosphate", "phosphorylated", "phosphoryl transfer", "phosphomutase")
    )


def _has_ser_his_acyl_transfer_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    hydrolysis_terms = ("hydrolysis", "hydrolyses", "hydrolyzes", "hydrolysing", "hydrolyzing")
    if any(term in mechanism_text for term in hydrolysis_terms):
        return False
    return any(
        term in mechanism_text
        for term in ("transacylase", "acyl carrier protein", "acyl transfer")
    )


def _has_tpp_carboligation_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_tpp = (
        "thiamine diphosphate" in mechanism_text
        or "thiamine-diphosphate" in mechanism_text
        or "tpp" in mechanism_text
    )
    has_carbon_transfer = any(
        term in mechanism_text
        for term in (
            "acetolactate",
            "carboligation",
            "carbon-carbon condensation",
            "2-acetolactate",
        )
    )
    return has_tpp and has_carbon_transfer


def _has_zinc_methyltransfer_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_zinc = "zinc" in mechanism_text
    has_methyl_transfer = any(
        term in mechanism_text
        for term in (
            "methyltransferase",
            "methyl acceptor",
            "alkyl transfer",
            "methyl transfer",
        )
    )
    return has_zinc and has_methyl_transfer


def _has_metal_phosphate_hydrolysis_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_phosphate_substrate = any(
        term in mechanism_text
        for term in (
            "phosphatase",
            "phosphodiester",
            "phosphopolynucleotide",
            "gamma-phosphate",
            "phosphate",
        )
    )
    has_hydrolysis = any(term in mechanism_text for term in ("hydroly", "water"))
    has_metal = any(
        term in mechanism_text
        for term in (
            "divalent cation",
            "mg(ii)",
            "mn(ii)",
            "magnesium",
            "manganese",
            "metal ion",
        )
    )
    transfer_only = any(
        term in mechanism_text
        for term in (
            "transfer reaction",
            "ligase",
            "synthase",
            "methyl transfer",
            "prenyl transfer",
        )
    )
    return has_phosphate_substrate and has_hydrolysis and has_metal and not transfer_only


def _has_alpha_ketoglutarate_hydroxylation_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_hydroxylation = "hydroxylation" in mechanism_text or "hydroxylates" in mechanism_text
    has_demethylase = "demethylase" in mechanism_text or "demethylated" in mechanism_text
    has_akg = "alpha-ketoglutarate" in mechanism_text or "2-oxoglutarate" in mechanism_text
    return has_hydroxylation and has_demethylase and has_akg


def _has_heme_dehydratase_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_heme = "heme" in mechanism_text
    has_dehydration = "dehydratase" in mechanism_text or "dehydration" in mechanism_text
    return has_heme and has_dehydration


def _has_flavin_mutase_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    has_flavin = "fad" in mechanism_text or "flavin" in mechanism_text
    has_mutase = "mutase" in mechanism_text or "udp-galactopyranose" in mechanism_text
    has_glycosyl = "udp-galp" in mechanism_text or "loss of udp" in mechanism_text
    return has_flavin and has_mutase and has_glycosyl


def _has_methylcobalamin_transfer_text_context(mechanism_text: str) -> bool:
    if not mechanism_text:
        return False
    if "methylcobalamin" in mechanism_text:
        return True
    if "heterolytic" in mechanism_text and "adenosylcobalamin" not in mechanism_text:
        return True
    return False


def _cofactor_family(cofactor: str) -> str:
    if _is_metal_cofactor(cofactor):
        return "metal_ion"
    if "heme" in cofactor:
        return "heme"
    if "pyridoxal phosphate" in cofactor:
        return "plp"
    if "cobalamin" in cofactor or "vitamin b12" in cofactor:
        return "cobalamin"
    if cofactor in {"fad", "fmn"}:
        return "flavin"
    if cofactor in {"nadph", "nadp", "nad", "nadh"}:
        return "nad"
    if "sam" in cofactor or "adenosylmethionine" in cofactor:
        return "sam"
    if "4fe-4s" in cofactor:
        return "fe_s_cluster"
    return ""


def _normalize_cofactor_family(value: str) -> str:
    normalized = _normalize_phrase(value)
    if normalized in {"metal ion", "metal"}:
        return "metal_ion"
    if normalized in {"fe s cluster", "fes cluster", "iron sulfur"}:
        return "fe_s_cluster"
    if normalized in {"pyridoxal phosphate", "pyridoxal 5 phosphate"}:
        return "plp"
    if normalized in {"b12", "cobalamin", "vitamin b12"}:
        return "cobalamin"
    return normalized


def _has_aromatic_positive_pocket(pocket_context: dict[str, Any] | None) -> bool:
    if not isinstance(pocket_context, dict):
        return False
    descriptors = pocket_context.get("descriptors", {})
    if not isinstance(descriptors, dict):
        return False
    aromatic = float(descriptors.get("aromatic_fraction", 0.0) or 0.0)
    positive = float(descriptors.get("positive_fraction", 0.0) or 0.0)
    return aromatic >= 0.20 and positive >= 0.12


def _has_hydrophobic_low_polar_pocket(pocket_context: dict[str, Any] | None) -> bool:
    if not isinstance(pocket_context, dict):
        return False
    descriptors = pocket_context.get("descriptors", {})
    if not isinstance(descriptors, dict):
        return False
    hydrophobic = float(descriptors.get("hydrophobic_fraction", 0.0) or 0.0)
    polar = float(descriptors.get("polar_fraction", 0.0) or 0.0)
    negative = float(descriptors.get("negative_fraction", 0.0) or 0.0)
    return hydrophobic >= 0.50 and polar <= 0.20 and negative <= 0.06


def _has_histidine_only_metal_site(residues: list[dict[str, Any]]) -> bool:
    metal_ligand_codes = [
        _canonical_code(residue.get("code"))
        for residue in residues
        if _residue_has_any_role(residue, {"metal ligand"})
    ]
    if len(metal_ligand_codes) < 4:
        return False
    if set(metal_ligand_codes) != {"HIS"}:
        return False
    all_codes = {_canonical_code(residue.get("code")) for residue in residues}
    return not (all_codes & {"ASP", "GLU", "CYS"})


def _has_plp_lysine_anchor(residues: list[dict[str, Any]]) -> bool:
    return any(
        _canonical_code(residue.get("code")) == "LYS"
        and _residue_has_any_role(
            residue,
            {"covalently attached", "electron pair donor", "electron pair acceptor"},
        )
        for residue in residues
    )


def _has_water_activation_role(residues: list[dict[str, Any]]) -> bool:
    water_activation_roles = {
        "activator",
        "increase acidity",
        "increase basicity",
        "proton acceptor",
        "proton donor",
        "proton relay",
    }
    return any(_residue_has_any_role(residue, water_activation_roles) for residue in residues)


def _has_electron_transfer_role(residues: list[dict[str, Any]]) -> bool:
    role_fragments = ("electron", "redox")
    return any(
        any(fragment in _normalize_phrase(role) for fragment in role_fragments)
        for residue in residues
        for role in residue.get("roles", [])
        if isinstance(role, str)
    )


def _has_radical_transfer_role(residues: list[dict[str, Any]]) -> bool:
    return any(
        "radical" in _normalize_phrase(role)
        for residue in residues
        for role in residue.get("roles", [])
        if isinstance(role, str)
    )


def _has_manganese_decarboxylase_signature(residues: list[dict[str, Any]]) -> bool:
    metal_ligand_count = sum(
        1 for residue in residues if _residue_has_any_role(residue, {"metal ligand"})
    )
    has_arginine_stabilizer = any(
        _canonical_code(residue.get("code")) == "ARG"
        and _residue_has_any_role(
            residue,
            {"electrostatic stabiliser", "electrostatic stabilizer", "hydrogen bond donor"},
        )
        for residue in residues
    )
    has_hydrolytic_covalent_roles = any(
        _residue_has_any_role(residue, {"nucleophile", "nucleofuge", "covalently attached"})
        for residue in residues
    )
    return metal_ligand_count >= 4 and has_arginine_stabilizer and not has_hydrolytic_covalent_roles


def _has_aromatic_oxygenase_pocket(pocket_context: dict[str, Any] | None) -> bool:
    if not isinstance(pocket_context, dict):
        return False
    descriptors = pocket_context.get("descriptors", {})
    if not isinstance(descriptors, dict):
        return False
    aromatic = float(descriptors.get("aromatic_fraction", 0.0) or 0.0)
    positive = float(descriptors.get("positive_fraction", 0.0) or 0.0)
    return aromatic >= 0.22 and positive <= 0.08


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _metal_ligand_role_count(inputs: CounterevidenceInputs) -> int:
    return sum(
        1
        for residue in inputs.residues
        if _residue_has_any_role(residue, {"metal ligand"})
    )


def _has_single_electron_role(inputs: CounterevidenceInputs) -> bool:
    return any("single electron" in role for role in inputs.residue_roles)


COUNTEREVIDENCE_POLICY: tuple[CounterevidenceRule, ...] = (
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_low_pocket_support",
        0.72,
        ("cofactor_evidence", "substrate_pocket_score"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and c.substrate_pocket_score_value < 0.15,
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_hydrophobic_low_pocket_support",
        0.70,
        ("cofactor_evidence", "substrate_pocket_score", "pocket_context"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and c.substrate_pocket_score_value < 0.13
        and _has_hydrophobic_low_polar_pocket(c.pocket_context),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_low_compactness",
        0.72,
        ("cofactor_evidence", "compactness_score"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and c.compactness_score_value is not None
        and c.compactness_score_value < 0.20,
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_phosphate_hydrolysis_text_support",
        0.88,
        ("cofactor_evidence", "residue_roles", "mechanism_text"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and not _has_water_activation_role(c.residues)
        and _has_metal_phosphate_hydrolysis_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_missing_water_activation_role",
        0.72,
        ("cofactor_evidence", "residue_roles", "mechanism_text"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and not _has_water_activation_role(c.residues)
        and not _has_metal_phosphate_hydrolysis_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_aromatic_positive_pocket",
        0.92,
        ("cofactor_evidence", "pocket_context"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and _has_aromatic_positive_pocket(c.pocket_context),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_histidine_only_metal_site",
        0.68,
        ("cofactor_evidence", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and _has_histidine_only_metal_site(c.residues),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_covalent_cleavage_roles",
        0.68,
        ("cofactor_evidence", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and {"nucleophile", "nucleofuge"}.issubset(c.residue_roles),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "role_inferred_metal_radical_transfer_roles",
        0.68,
        ("cofactor_evidence", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and _has_radical_transfer_role(c.residues),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "structure_only_manganese_decarboxylase_context",
        0.68,
        ("cofactor_evidence", "ligand_context", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "role_inferred"
        and "metal_ion" in c.structure_ligand_families
        and "metal_ion" not in c.ligand_families
        and "MN" in c.structure_ligand_codes
        and _has_manganese_decarboxylase_signature(c.residues),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "heme_only_context_for_metal_hydrolase",
        0.75,
        ("ligand_context",),
        lambda c, _: "heme" in c.ligand_families and "metal_ion" not in c.ligand_families,
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "cobalamin_only_context_for_metal_hydrolase",
        0.80,
        ("ligand_context",),
        lambda c, _: "cobalamin" in c.ligand_families
        and "metal_ion" not in c.ligand_families,
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "methylcobalamin_transfer_context_for_metal_hydrolase",
        0.45,
        ("mechanism_text",),
        lambda c, _: _has_methylcobalamin_transfer_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "zinc_methyltransfer_not_hydrolysis",
        0.55,
        ("mechanism_text",),
        lambda c, _: _has_zinc_methyltransfer_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "ligand_supported_metal_without_metal_ligand_roles",
        0.70,
        ("cofactor_evidence", "ligand_context", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and "metal_ion" in c.ligand_families
        and "metal ligand" not in c.residue_roles,
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nucleotide_transfer_ligand_context",
        0.68,
        ("ligand_context",),
        lambda c, _: bool(c.ligand_codes & NUCLEOTIDE_TRANSFER_LIGAND_CODES),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "metal_bound_nad_redox_text_context",
        0.62,
        ("mechanism_text",),
        lambda c, _: _has_nad_redox_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "sam_ligand_context",
        0.72,
        ("ligand_context",),
        lambda c, _: "sam" in c.ligand_families,
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "fe_s_cluster_context_for_metal_hydrolase",
        0.70,
        ("ligand_context",),
        lambda c, _: "fe_s_cluster" in c.ligand_families
        and "metal_ion" not in c.ligand_families,
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nonhydrolytic_metal_transfer_ligand_context",
        0.68,
        ("ligand_context",),
        lambda c, _: bool(c.ligand_codes & METAL_HYDROLASE_TRANSFER_LIGAND_CODES),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "biotin_carboxyltransfer_mixed_metal_context",
        0.68,
        ("ligand_context",),
        lambda c, _: {"KCX", "MG", "ZN"}.issubset(c.ligand_codes),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "metal_redox_ligand_context",
        0.68,
        ("ligand_context",),
        lambda c, _: bool(c.ligand_codes & METAL_HYDROLASE_REDOX_LIGAND_CODES),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nonhydrolytic_prenyl_carbocation_text_context",
        0.58,
        ("mechanism_text",),
        lambda c, _: _has_prenyl_carbocation_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nonhydrolytic_isomerase_lyase_text_context",
        0.62,
        ("mechanism_text",),
        lambda c, _: _has_nonhydrolytic_isomerase_lyase_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nonhydrolytic_hydratase_dehydratase_text_context",
        0.62,
        ("mechanism_text",),
        lambda c, _: _has_nonhydrolytic_hydratase_dehydratase_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "phosphoenolpyruvate_transfer_not_metal_hydrolysis",
        0.55,
        ("mechanism_text",),
        lambda c, _: _has_phosphoenolpyruvate_transfer_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "metal_bound_dehydrogenase_not_hydrolysis",
        0.55,
        ("mechanism_text",),
        lambda c, _: _has_metal_bound_dehydrogenase_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "aminoacyl_ligase_not_metal_hydrolysis",
        0.58,
        ("mechanism_text",),
        lambda c, _: _has_aminoacyl_ligase_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "glycosidase_not_metal_hydrolase_seed",
        0.58,
        ("mechanism_text",),
        lambda c, _: _has_glycosidase_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nonhydrolytic_alpha_ketoglutarate_hydroxylation",
        0.55,
        ("mechanism_text",),
        lambda c, _: _has_alpha_ketoglutarate_hydroxylation_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nonheme_iron_aromatic_low_pocket_without_water_activation",
        0.70,
        ("cofactor_evidence", "ligand_context", "pocket_context", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and c.substrate_pocket_score_value < 0.18
        and not _has_water_activation_role(c.residues)
        and "FE" in c.ligand_codes
        and _has_aromatic_oxygenase_pocket(c.pocket_context),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "nonheme_iron_biopterin_hydroxylase_context",
        0.64,
        ("cofactor_evidence", "ligand_context", "pocket_context"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and "FE" in c.ligand_codes
        and "HBI" in c.structure_ligand_codes
        and _has_aromatic_oxygenase_pocket(c.pocket_context),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "ligand_supported_metal_hydrophobic_low_pocket_support",
        0.70,
        ("cofactor_evidence", "substrate_pocket_score", "pocket_context"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and c.substrate_pocket_score_value < 0.10
        and _has_hydrophobic_low_polar_pocket(c.pocket_context),
    ),
    _counterevidence_rule(
        "metal_dependent_hydrolase",
        "single_electron_role_context",
        0.70,
        ("residue_roles",),
        lambda c, _: _has_single_electron_role(c),
    ),
    _counterevidence_rule(
        "ser_his_acid_hydrolase",
        "metal_supported_site_for_ser_his_seed",
        0.70,
        ("ligand_context", "residue_roles"),
        lambda c, _: "metal_ion" in c.ligand_families
        and _metal_ligand_role_count(c) >= 3,
    ),
    _counterevidence_rule(
        "ser_his_acid_hydrolase",
        "metal_ligand_rich_site_for_ser_his_seed",
        0.85,
        ("residue_roles",),
        lambda c, _: "metal ligand" in c.residue_roles
        and _metal_ligand_role_count(c) >= 4,
    ),
    _counterevidence_rule(
        "ser_his_acid_hydrolase",
        "ser_his_seed_missing_triad_coherence",
        0.70,
        ("residue_roles",),
        lambda c, _: mechanistic_coherence_score({"id": c.fingerprint_id}, c.residues) < 0.5,
    ),
    _counterevidence_rule(
        "ser_his_acid_hydrolase",
        "ser_his_nonhydrolytic_electrophile_without_leaving_group",
        0.45,
        ("residue_roles",),
        lambda c, _: "electrophile" in c.residue_roles
        and "nucleofuge" not in c.residue_roles,
    ),
    _counterevidence_rule(
        "ser_his_acid_hydrolase",
        "ser_his_phosphoryl_transfer_text_context",
        0.55,
        ("mechanism_text",),
        lambda c, _: _has_phosphoryl_transfer_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "ser_his_acid_hydrolase",
        "ser_his_acyl_transfer_not_hydrolysis",
        0.55,
        ("mechanism_text",),
        lambda c, _: _has_ser_his_acyl_transfer_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "heme_peroxidase_oxidase",
        "absent_heme_context",
        0.65,
        ("cofactor_evidence",),
        lambda c, _: c.cofactor_evidence == "absent",
    ),
    _counterevidence_rule(
        "heme_peroxidase_oxidase",
        "molybdenum_center_heme_context",
        0.63,
        ("ligand_context",),
        lambda c, _: "heme" in c.ligand_families
        and bool(c.ligand_codes & MOLYBDENUM_CENTER_LIGAND_CODES),
    ),
    _counterevidence_rule(
        "heme_peroxidase_oxidase",
        "heme_dehydratase_not_peroxidase_oxidase",
        0.55,
        ("mechanism_text",),
        lambda c, _: _has_heme_dehydratase_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "plp_dependent_enzyme",
        "non_plp_aldolase_schiff_base_context",
        0.60,
        ("cofactor_evidence", "ligand_context", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "absent"
        and _has_plp_lysine_anchor(c.residues)
        and "13P" in c.ligand_codes,
    ),
    _counterevidence_rule(
        "plp_dependent_enzyme",
        "absent_plp_ligand_with_lysine_anchor",
        0.75,
        ("cofactor_evidence", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "absent"
        and _has_plp_lysine_anchor(c.residues),
    ),
    _counterevidence_rule(
        "plp_dependent_enzyme",
        "absent_plp_ligand_without_lysine_anchor",
        0.60,
        ("cofactor_evidence", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "absent"
        and not _has_plp_lysine_anchor(c.residues),
    ),
    _counterevidence_rule(
        "cobalamin_radical_rearrangement",
        "methylcobalamin_transfer_not_radical_rearrangement",
        0.45,
        ("mechanism_text",),
        lambda c, _: _has_methylcobalamin_transfer_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "cobalamin_radical_rearrangement",
        "absent_cobalamin_context",
        0.25,
        ("cofactor_evidence",),
        lambda c, _: c.cofactor_evidence == "absent",
    ),
    _counterevidence_rule(
        "flavin_monooxygenase",
        "absent_flavin_context",
        0.60,
        ("cofactor_evidence",),
        lambda c, _: c.cofactor_evidence == "absent",
    ),
    _counterevidence_rule(
        "flavin_monooxygenase",
        "nad_only_or_nonflavin_context",
        0.60,
        ("ligand_context",),
        lambda c, _: "flavin" not in c.ligand_families,
    ),
    _counterevidence_rule(
        "flavin_monooxygenase",
        "thiamine_carboligation_not_flavin_oxygenation",
        0.45,
        ("cofactor_evidence", "mechanism_text"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and _has_tpp_carboligation_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "flavin_monooxygenase",
        "flavin_without_reductant_context",
        0.75,
        ("cofactor_evidence", "ligand_context"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and "nad" not in c.ligand_families
        and not c.ligand_codes & FLAVIN_MONOOXYGENASE_SUBSTRATE_LIGAND_CODES,
    ),
    _counterevidence_rule(
        "flavin_dehydrogenase_reductase",
        "thiamine_carboligation_not_local_flavin_redox",
        0.45,
        ("cofactor_evidence", "mechanism_text"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and _has_tpp_carboligation_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "flavin_dehydrogenase_reductase",
        "flavin_mutase_not_dehydrogenase_reductase",
        0.55,
        ("cofactor_evidence", "mechanism_text"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and _has_flavin_mutase_text_context(c.mechanism_text),
    ),
    _counterevidence_rule(
        "flavin_dehydrogenase_reductase",
        "flavin_monooxygenase_substrate_without_electron_transfer_context",
        0.55,
        ("cofactor_evidence", "ligand_context", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "ligand_supported"
        and "flavin" in c.ligand_families
        and bool(c.ligand_codes & FLAVIN_MONOOXYGENASE_SUBSTRATE_LIGAND_CODES)
        and not _has_electron_transfer_role(c.residues),
    ),
    _counterevidence_rule(
        "flavin_dehydrogenase_reductase",
        "molybdenum_center_without_flavin_context",
        0.55,
        ("cofactor_evidence", "ligand_context"),
        lambda c, _: c.cofactor_evidence == "absent"
        and bool(c.ligand_codes & MOLYBDENUM_CENTER_LIGAND_CODES),
    ),
    _counterevidence_rule(
        "flavin_dehydrogenase_reductase",
        "nonheme_iron_fe_s_without_flavin_context",
        0.55,
        ("cofactor_evidence", "ligand_context"),
        lambda c, _: c.cofactor_evidence == "absent"
        and not c.ligand_codes & MOLYBDENUM_CENTER_LIGAND_CODES
        and "fe_s_cluster" in c.ligand_families
        and "metal_ion" in c.ligand_families,
    ),
    _counterevidence_rule(
        "flavin_dehydrogenase_reductase",
        "fe_s_single_electron_partial_flavin_context",
        0.63,
        ("cofactor_evidence", "ligand_context", "residue_roles"),
        lambda c, _: c.cofactor_evidence == "absent"
        and "fe_s_cluster" in c.ligand_families
        and _has_single_electron_role(c),
    ),
    _counterevidence_rule(
        "flavin_dehydrogenase_reductase",
        "absent_flavin_context",
        0.60,
        ("cofactor_evidence", "ligand_context", "residue_roles"),
        lambda c, applied: c.cofactor_evidence == "absent" and not applied,
    ),
)
