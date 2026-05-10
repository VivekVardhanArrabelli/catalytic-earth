from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints


METAL_HYDROLASE_TRANSFER_LIGAND_CODES = {
    "ADJ",  # ATP-dependent amidation analog context
    "APG",  # metal-assisted racemase/isomerase product analog context
    "BIO",  # pterin/biopterin synthase rearrangement context
    "DAD",  # adenosine-like cyclase/product analog context
    "DAA",  # ATP-dependent ligase/ring-forming context
    "DED",  # diphosphate/isoprenoid isomerase analog context
    "FOC",  # fucose-like sugar isomerization context
    "G16",  # phosphoglucomutase bisphosphate/phosphoryl-transfer context
    "GLV",  # glyoxylate-like ligand in malate synthase hard-negative context
    "HDA",  # adenylosuccinate synthase intermediate analog context
    "ICT",  # isocitrate redox/decarboxylation context
    "OXL",  # oxalate-like carbonyl/decarboxylation context
    "PGH",  # phosphoglycolate/hydroxamate-like aldolase inhibitor context
    "PHT",  # phosphoribosyl-transfer analog context
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
                "pdb_id": entry.get("pdb_id"),
                "status": entry.get("status"),
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
            "entry_count": len(results),
            "fingerprint_count": len(fingerprints),
            "scoring": "residue and role overlap plus ligand/cofactor context, substrate-pocket descriptors, and compactness",
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
    coherence = mechanistic_coherence_score(fingerprint, residues)
    counterevidence = counterevidence_assessment(
        fingerprint=fingerprint,
        residues=residues,
        cofactor_evidence=cofactor_evidence,
        ligand_context=entry.get("ligand_context"),
        substrate_pocket_score_value=substrate_pocket,
        pocket_context=entry.get("pocket_context"),
        compactness_score_value=compactness,
    )
    raw_score = (
        0.35 * residue_match_fraction
        + 0.24 * role_match_fraction
        + 0.18 * cofactor_context
        + 0.08 * compactness
        + 0.15 * substrate_pocket
    )
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
        "mechanistic_coherence_score": round(coherence, 4),
        "counterevidence_penalty": round(counterevidence["penalty"], 4),
        "counterevidence_reasons": counterevidence["reasons"],
        "counterevidence_penalty_details": counterevidence["penalty_details"],
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
) -> float:
    return counterevidence_assessment(
        fingerprint=fingerprint,
        residues=residues,
        cofactor_evidence=cofactor_evidence,
        ligand_context=ligand_context,
        substrate_pocket_score_value=substrate_pocket_score_value,
        pocket_context=pocket_context,
        compactness_score_value=compactness_score_value,
    )["penalty"]


def counterevidence_assessment(
    fingerprint: dict[str, Any],
    residues: list[dict[str, Any]],
    cofactor_evidence: str,
    ligand_context: dict[str, Any] | None,
    substrate_pocket_score_value: float,
    pocket_context: dict[str, Any] | None = None,
    compactness_score_value: float | None = None,
) -> dict[str, Any]:
    fingerprint_id = str(fingerprint.get("id", ""))
    residue_roles = {
        _normalize_phrase(role)
        for residue in residues
        for role in residue.get("roles", [])
        if isinstance(role, str)
    }
    ligand_families = _ligand_cofactor_families(ligand_context)
    ligand_codes = _ligand_codes(ligand_context)
    penalty = 1.0
    reasons: list[str] = []
    penalty_details: list[dict[str, Any]] = []

    def apply(value: float, reason: str) -> None:
        nonlocal penalty
        if value < penalty:
            penalty = value
        reasons.append(reason)
        penalty_details.append({"reason": reason, "penalty": round(value, 4)})

    def result() -> dict[str, Any]:
        return {
            "penalty": penalty,
            "reasons": sorted(set(reasons)),
            "penalty_details": sorted(
                {detail["reason"]: detail for detail in penalty_details}.values(),
                key=lambda detail: (float(detail["penalty"]), str(detail["reason"])),
            ),
        }

    if fingerprint_id == "metal_dependent_hydrolase":
        if cofactor_evidence == "role_inferred" and substrate_pocket_score_value < 0.15:
            apply(0.72, "role_inferred_metal_low_pocket_support")
        if (
            cofactor_evidence == "role_inferred"
            and substrate_pocket_score_value < 0.13
            and _has_hydrophobic_low_polar_pocket(pocket_context)
        ):
            apply(0.70, "role_inferred_metal_hydrophobic_low_pocket_support")
        if cofactor_evidence == "role_inferred" and compactness_score_value is not None:
            if compactness_score_value < 0.20:
                apply(0.72, "role_inferred_metal_low_compactness")
        if cofactor_evidence == "role_inferred" and not _has_water_activation_role(residues):
            apply(0.72, "role_inferred_metal_missing_water_activation_role")
        if cofactor_evidence == "role_inferred" and _has_aromatic_positive_pocket(pocket_context):
            apply(0.92, "role_inferred_metal_aromatic_positive_pocket")
        if cofactor_evidence == "role_inferred" and _has_histidine_only_metal_site(residues):
            apply(0.68, "role_inferred_histidine_only_metal_site")
        if (
            cofactor_evidence == "role_inferred"
            and {"nucleophile", "nucleofuge"}.issubset(residue_roles)
        ):
            apply(0.68, "role_inferred_metal_covalent_cleavage_roles")
        if cofactor_evidence == "role_inferred" and _has_radical_transfer_role(residues):
            apply(0.68, "role_inferred_metal_radical_transfer_roles")
        if "heme" in ligand_families and "metal_ion" not in ligand_families:
            apply(0.75, "heme_only_context_for_metal_hydrolase")
        if "cobalamin" in ligand_families and "metal_ion" not in ligand_families:
            apply(0.80, "cobalamin_only_context_for_metal_hydrolase")
        if (
            cofactor_evidence == "ligand_supported"
            and "metal_ion" in ligand_families
            and "metal ligand" not in residue_roles
        ):
            apply(0.70, "ligand_supported_metal_without_metal_ligand_roles")
        if ligand_codes & NUCLEOTIDE_TRANSFER_LIGAND_CODES:
            apply(0.68, "nucleotide_transfer_ligand_context")
        if "sam" in ligand_families:
            apply(0.72, "sam_ligand_context")
        if "fe_s_cluster" in ligand_families and "metal_ion" not in ligand_families:
            apply(0.70, "fe_s_cluster_context_for_metal_hydrolase")
        if ligand_codes & METAL_HYDROLASE_TRANSFER_LIGAND_CODES:
            apply(0.68, "nonhydrolytic_metal_transfer_ligand_context")
        if {"KCX", "MG", "ZN"}.issubset(ligand_codes):
            apply(0.68, "biotin_carboxyltransfer_mixed_metal_context")
        if ligand_codes & METAL_HYDROLASE_REDOX_LIGAND_CODES:
            apply(0.68, "metal_redox_ligand_context")
        if (
            cofactor_evidence == "ligand_supported"
            and substrate_pocket_score_value < 0.18
            and not _has_water_activation_role(residues)
            and "FE" in ligand_codes
            and _has_aromatic_oxygenase_pocket(pocket_context)
        ):
            apply(0.70, "nonheme_iron_aromatic_low_pocket_without_water_activation")
        if (
            cofactor_evidence == "ligand_supported"
            and substrate_pocket_score_value < 0.10
            and _has_hydrophobic_low_polar_pocket(pocket_context)
        ):
            apply(0.70, "ligand_supported_metal_hydrophobic_low_pocket_support")
        if any("single electron" in role for role in residue_roles):
            apply(0.70, "single_electron_role_context")
        return result()

    if fingerprint_id == "ser_his_acid_hydrolase":
        metal_ligand_roles = sum(
            1
            for residue in residues
            if _residue_has_any_role(residue, {"metal ligand"})
        )
        if "metal_ion" in ligand_families and metal_ligand_roles >= 3:
            apply(0.70, "metal_supported_site_for_ser_his_seed")
        if "metal ligand" in residue_roles and metal_ligand_roles >= 4:
            apply(0.85, "metal_ligand_rich_site_for_ser_his_seed")
        if mechanistic_coherence_score(fingerprint, residues) < 0.5:
            apply(0.70, "ser_his_seed_missing_triad_coherence")
        if "electrophile" in residue_roles and "nucleofuge" not in residue_roles:
            apply(0.45, "ser_his_nonhydrolytic_electrophile_without_leaving_group")
        return result()

    if fingerprint_id == "heme_peroxidase_oxidase":
        if cofactor_evidence == "absent":
            apply(0.65, "absent_heme_context")
        if "heme" in ligand_families and ligand_codes & MOLYBDENUM_CENTER_LIGAND_CODES:
            apply(0.63, "molybdenum_center_heme_context")
        return result()

    if fingerprint_id == "plp_dependent_enzyme":
        if cofactor_evidence == "absent":
            if _has_plp_lysine_anchor(residues):
                apply(0.75, "absent_plp_ligand_with_lysine_anchor")
            else:
                apply(0.60, "absent_plp_ligand_without_lysine_anchor")
        return result()

    if fingerprint_id == "cobalamin_radical_rearrangement":
        if cofactor_evidence == "absent":
            apply(0.25, "absent_cobalamin_context")
        return result()

    if fingerprint_id == "flavin_monooxygenase":
        if cofactor_evidence == "absent":
            apply(0.60, "absent_flavin_context")
        if "flavin" not in ligand_families:
            apply(0.60, "nad_only_or_nonflavin_context")
        if (
            cofactor_evidence == "ligand_supported"
            and "nad" not in ligand_families
            and not ligand_codes & FLAVIN_MONOOXYGENASE_SUBSTRATE_LIGAND_CODES
        ):
            apply(0.75, "flavin_without_reductant_context")
        return result()

    if fingerprint_id == "flavin_dehydrogenase_reductase":
        if (
            cofactor_evidence == "ligand_supported"
            and "flavin" in ligand_families
            and ligand_codes & FLAVIN_MONOOXYGENASE_SUBSTRATE_LIGAND_CODES
            and not _has_electron_transfer_role(residues)
        ):
            apply(0.55, "flavin_monooxygenase_substrate_without_electron_transfer_context")
        if cofactor_evidence == "absent":
            if ligand_codes & MOLYBDENUM_CENTER_LIGAND_CODES:
                apply(0.55, "molybdenum_center_without_flavin_context")
            elif "fe_s_cluster" in ligand_families and "metal_ion" in ligand_families:
                apply(0.55, "nonheme_iron_fe_s_without_flavin_context")
            if "fe_s_cluster" in ligand_families and any(
                "single electron" in role for role in residue_roles
            ):
                apply(0.63, "fe_s_single_electron_partial_flavin_context")
            elif not reasons:
                apply(0.60, "absent_flavin_context")
        return result()

    return result()


def write_geometry_retrieval(
    geometry_path: Path,
    out_path: Path,
    top_k: int = 5,
) -> dict[str, Any]:
    artifact = run_geometry_retrieval(load_json(geometry_path), top_k=top_k)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


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
    return any(required in roles for required in required_roles)


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
