"""High-yield family lane scout and reusable source-lane factory.

This module is intentionally metadata-only. It creates no labels and writes no
registry rows. Its job is to keep scaleout agents from spending a run on tiny
top-ups when the current fingerprint universe cannot admit a >=150-row batch.

Each lane spec declares the source query, the non-EC mechanism corroborator
query, disambiguation holds, cap policy, and the preview/apply work that would
be needed before a future registry mutation. EC remains scope-only throughout.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_uniprot_query_count
from .external_scaleout_bronze_import import (
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
)
from .registry_io import load_json

ARTIFACT_ID = "v3_high_yield_family_lane_factory_current702"
SCHEMA_VERSION = "high_yield_family_lane_factory.v1"

MIN_HIGH_YIELD_ADMITS = 150
DEFAULT_CONFUSABLE_CAP = 150
DEFAULT_CLEAN_CAP = 250


def _spec(
    *,
    family_id: str,
    display_name: str,
    scope_query: str,
    corroborator_query: str,
    required_non_ec_corroborators: tuple[str, ...],
    disambiguation_holds: tuple[str, ...],
    cap_ceiling: int,
    chemistry_confusable: bool,
    novelty_keep_factor: float,
    rationale_template: str,
    existing_fingerprint_id: str | None = None,
    current_runner: str | None = None,
    ambiguity_with_existing: tuple[str, ...] = (),
    oos_preregistration_required: bool = True,
    source_wall_rule_status: str | None = None,
    known_blockers: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "family_id": family_id,
        "display_name": display_name,
        "scope_query": scope_query,
        "corroborator_query": corroborator_query,
        "required_non_ec_corroborators": list(required_non_ec_corroborators),
        "disambiguation_holds": list(disambiguation_holds),
        "cap_ceiling": cap_ceiling,
        "chemistry_confusable": chemistry_confusable,
        "novelty_keep_factor": novelty_keep_factor,
        "rationale_template": rationale_template,
        "existing_fingerprint_id": existing_fingerprint_id,
        "current_runner": current_runner,
        "ambiguity_with_existing": list(ambiguity_with_existing),
        "oos_preregistration_required": oos_preregistration_required,
        "source_wall_rule_status": (
            source_wall_rule_status
            or ("implemented_existing_fingerprint" if existing_fingerprint_id else "not_implemented")
        ),
        "known_blockers": list(known_blockers),
    }


HIGH_YIELD_FAMILY_SPECS: tuple[dict[str, Any], ...] = (
    _spec(
        family_id="terpene_cyclase_synthase",
        display_name="Terpene cyclase/synthase",
        scope_query="(reviewed:true) AND (ec:4.2.3.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:4.2.3.*) AND "
            "((keyword:Terpene) OR (protein_name:cyclase) OR (protein_name:synthase) "
            "OR (cc_cofactor:magnesium) OR (cc_cofactor:manganese))"
        ),
        required_non_ec_corroborators=(
            "terpene/cyclase functional keyword or protein-name handle",
            "Mg/Mn diphosphate-binding handle or active-site metal context",
            "Rhea reaction participant showing diphosphate release/cyclization where available",
        ),
        disambiguation_holds=(
            "prenyltransferase chain-extension rows",
            "lyase/hydratase rows without terpene cyclization evidence",
            "multi-fingerprint metal-lyase signal rows",
        ),
        cap_ceiling=DEFAULT_CLEAN_CAP,
        chemistry_confusable=False,
        novelty_keep_factor=0.45,
        existing_fingerprint_id="terpene_cyclase_synthase",
        current_runner="scripts/source_terpene_cyclase_synthase_family.py",
        oos_preregistration_required=False,
        rationale_template=(
            "Clean carbocation cyclization chemistry outside the current atlas; "
            "prefer reviewed EC 4.2.3 rows with metal/diphosphate corroboration."
        ),
    ),
    _spec(
        family_id="alpha_beta_hydrolase_esterase_lipase",
        display_name="Alpha/beta hydrolase esterase/lipase",
        scope_query="(reviewed:true) AND (ec:3.1.1.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:3.1.1.*) AND "
            "((keyword:Esterase) OR (keyword:Lipase) OR (protein_name:esterase) "
            "OR (protein_name:lipase))"
        ),
        required_non_ec_corroborators=(
            "Ser-His-Asp/Glu catalytic triad active-site or binding-site evidence",
            "esterase/lipase family keyword or protein-name handle",
            "Rhea ester hydrolysis participant/equation where available",
        ),
        disambiguation_holds=(
            "protease/amidase rows",
            "glycoside hydrolase/transglycosylase rows",
            "metal hydrolase rows",
            "EC-only rows without active-site or family corroboration",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.35,
        existing_fingerprint_id="alpha_beta_hydrolase_esterase_lipase",
        current_runner="scripts/source_alpha_beta_hydrolase_esterase_lipase_family.py",
        oos_preregistration_required=False,
        ambiguity_with_existing=("ser_his_acid_hydrolase", "metal_dependent_hydrolase"),
        rationale_template=(
            "High-supply hydrolytic family but confusable with existing ser-his and "
            "metal hydrolase lanes; requires a split before import."
        ),
    ),
    _spec(
        family_id="ser_thr_protein_phosphatase",
        display_name="Ser/Thr protein phosphatase",
        scope_query="(reviewed:true) AND ((ec:3.1.3.16) OR (ec:3.1.3.48))",
        corroborator_query=(
            "(reviewed:true) AND ((ec:3.1.3.16) OR (ec:3.1.3.48)) AND "
            "((protein_name:\"protein phosphatase\") OR (keyword:Phosphoprotein) "
            "OR (cc_cofactor:manganese) OR (cc_cofactor:iron))"
        ),
        required_non_ec_corroborators=(
            "protein-phosphatase family/name handle",
            "dinuclear metal binding-site/cofactor context",
            "Rhea phosphoprotein dephosphorylation equation where available",
        ),
        disambiguation_holds=(
            "small-molecule phosphomonoesterase rows",
            "protein kinase rows",
            "HAD-like Asp-phosphatase rows",
            "EC-only rows without protein substrate or metal corroboration",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.4,
        existing_fingerprint_id="ser_thr_protein_phosphatase",
        current_runner="scripts/source_ser_thr_protein_phosphatase_family.py",
        oos_preregistration_required=False,
        ambiguity_with_existing=("metallophosphomonoesterase",),
        rationale_template=(
            "Mechanistically useful protein-substrate phosphatase split, but it overlaps "
            "the existing metal phosphomonoesterase chemistry without a new rule."
        ),
    ),
    _spec(
        family_id="had_like_phosphatase",
        display_name="HAD-like phosphatase",
        scope_query="(reviewed:true) AND (ec:3.1.3.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:3.1.3.*) AND "
            "((protein_name:HAD) OR (protein_name:phosphatase) OR (keyword:Phosphatase) "
            "OR (cc_cofactor:magnesium))"
        ),
        required_non_ec_corroborators=(
            "HAD family/domain/name handle",
            "Asp nucleophile or Mg binding-site evidence",
            "Rhea phosphomonoester hydrolysis equation where available",
        ),
        disambiguation_holds=(
            "protein phosphatase rows",
            "metal phosphomonoesterase rows with no HAD signal",
            "phosphodiesterase/nuclease side rows",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.3,
        existing_fingerprint_id="had_like_phosphatase",
        current_runner="scripts/source_had_like_phosphatase_family.py",
        oos_preregistration_required=False,
        ambiguity_with_existing=("metallophosphomonoesterase",),
        rationale_template=(
            "Large phosphatase lane; only useful at scale after a HAD-specific split "
            "separates Asp-phosphoenzyme chemistry from metal phosphatases."
        ),
    ),
    _spec(
        family_id="serine_beta_lactamase",
        display_name="Serine beta-lactamase",
        scope_query="(reviewed:true) AND (ec:3.5.2.6)",
        corroborator_query=(
            "(reviewed:true) AND (ec:3.5.2.6) AND "
            "((keyword:\"Beta-lactamase\") OR (protein_name:\"beta-lactamase\")) "
            "NOT (protein_name:metallo)"
        ),
        required_non_ec_corroborators=(
            "beta-lactamase keyword/name handle",
            "active-site Ser/Lys/Glu beta-lactamase motif evidence",
            "Rhea beta-lactam hydrolysis equation where available",
        ),
        disambiguation_holds=(
            "metallo-beta-lactamase zinc rows",
            "general amidohydrolase rows",
            "resistance proteins without catalytic beta-lactamase evidence",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.45,
        existing_fingerprint_id="serine_beta_lactamase",
        current_runner="scripts/source_serine_beta_lactamase_family.py",
        oos_preregistration_required=False,
        source_wall_rule_status="implemented_existing_fingerprint",
        ambiguity_with_existing=("metallo_amidohydrolase_deaminase", "ser_his_acid_hydrolase"),
        rationale_template=(
            "Resistance-relevant covalent acyl-enzyme hydrolase split; keep separate "
            "from zinc metallo-beta-lactamases and generic amidohydrolases."
        ),
    ),
    _spec(
        family_id="metal_independent_phosphodiesterase",
        display_name="Metal-independent phosphodiesterase",
        scope_query=(
            "(reviewed:true) AND ((ec:3.1.4.*) OR (ec:4.6.1.*))"
        ),
        corroborator_query=(
            "(reviewed:true) AND ((ec:3.1.4.*) OR (ec:4.6.1.*)) AND "
            "((protein_name:phosphodiesterase) OR (protein_name:phospholipase) "
            "OR (keyword:Hydrolase) OR (ft_act_site:*) OR (ft_binding:*)) NOT "
            "((cc_cofactor:magnesium) OR (cc_cofactor:manganese) OR "
            "(cc_cofactor:zinc) OR (cc_cofactor:metal) OR (keyword:\"Metal-binding\"))"
        ),
        required_non_ec_corroborators=(
            "phosphodiesterase/nuclease/phospholipase family or protein-name handle",
            "Rhea phosphodiester or cyclic-nucleotide P-O cleavage reaction where available",
            "active-site acid/base or substrate-binding evidence independent of EC scope",
        ),
        disambiguation_holds=(
            "metal-dependent phosphodiesterase/nuclease rows",
            "phosphomonoesterase and protein phosphatase rows",
            "phospholipase C lyase rows without hydrolytic phosphodiester cleavage",
            "EC-only rows without family, active-site, binding-site, or Rhea corroboration",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.03,
        existing_fingerprint_id="metal_independent_phosphodiesterase",
        current_runner="scripts/source_metal_independent_phosphodiesterase_family.py",
        oos_preregistration_required=False,
        ambiguity_with_existing=(
            "metallophosphoesterase_nuclease",
            "metallophosphomonoesterase",
            "had_like_phosphatase",
        ),
        known_blockers=(
            "2026-06-15 discovery compass surfaced a replicated metal-independent "
            "phosphodiesterase coverage gap, not world-new chemistry",
            "2026-06-15 source-wall rule exists in preview-only form and treats metal "
            "presence as a hold/filter, not metal absence as counted corroboration",
            "2026-06-15 43fp runner preview fetched 265 rows but admitted only 14; "
            "additional CNPase/2',3'-cyclic-nucleotide/EC 4.6.1 handle preview "
            "fetched 130 rows and admitted 0",
        ),
        source_wall_rule_status="implemented_existing_fingerprint_runner_subscale_preview",
        rationale_template=(
            "Discovery-compass ontology gap: phosphodiester P-O cleavage without the "
            "two-metal architecture covered by the existing metal phosphoesterase family."
        ),
    ),
    _spec(
        family_id="n_ribosyl_hydrolase",
        display_name="N-ribosyl / nucleoside hydrolase",
        existing_fingerprint_id="n_ribosyl_hydrolase",
        current_runner="scripts/source_n_ribosyl_hydrolase_family.py",
        scope_query=(
            "(reviewed:true) AND ((ec:3.2.2.*) OR (protein_name:\"nucleoside hydrolase\") "
            "OR (protein_name:\"N-ribosylhydrolase\") OR (protein_name:\"N-ribosidase\"))"
        ),
        corroborator_query=(
            "(reviewed:true) AND ((ec:3.2.2.*) OR (protein_name:\"nucleoside hydrolase\") "
            "OR (protein_name:\"N-ribosylhydrolase\") OR (protein_name:\"N-ribosidase\")) "
            "AND ((protein_name:\"nucleoside hydrolase\") OR "
            "(protein_name:\"N-ribosylhydrolase\") OR (protein_name:\"N-ribosidase\") "
            "OR (keyword:Hydrolase) OR (ft_act_site:*) OR (ft_binding:*))"
        ),
        required_non_ec_corroborators=(
            "nucleoside hydrolase, N-ribosylhydrolase, or N-ribosidase family/name handle",
            "Rhea N-glycosidic bond hydrolysis reaction with ribose/deoxyribose product",
            "active-site acid/base or ribose/base-binding residue evidence where available",
        ),
        disambiguation_holds=(
            "O-glycosidase/glycoside hydrolase rows",
            "nucleoside phosphorylase phosphorolysis rows",
            "nucleoside kinase or nucleotidyltransferase side rows",
            "EC-only rows without N-ribosyl hydrolysis corroboration",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.45,
        ambiguity_with_existing=(
            "glycoside_hydrolase",
            "deoxynucleoside_kinase",
            "nucleoside_diphosphate_kinase",
        ),
        known_blockers=(
            "2026-06-15 discovery compass found known N-ribosyl hydrolase chemistry "
            "as an unmodeled reaction-center vocabulary gap",
            "2026-06-15 source-wall rule exists in preview-only form for N-glycosidic "
            "bond hydrolysis with phosphorylase/kinase/transferase/O-glycosidase holds",
            "requires fingerprint, ontology node, OOS preregistration, source runner, "
            "bounded preview, row audit, and explicit apply gate before any labels",
        ),
        source_wall_rule_status="implemented_preview_only",
        rationale_template=(
            "Discovery-compass ontology gap: N-glycosidic bond hydrolysis is distinct "
            "from O-glycoside hydrolase, kinase, and phosphorylase chemistry."
        ),
    ),
    _spec(
        family_id="metallo_beta_lactamase",
        display_name="Metallo-beta-lactamase",
        scope_query="(reviewed:true) AND (ec:3.5.2.6)",
        corroborator_query=(
            "(reviewed:true) AND (ec:3.5.2.6) AND "
            "((protein_name:metallo) OR (cc_cofactor:zinc) OR (keyword:Zinc))"
        ),
        required_non_ec_corroborators=(
            "metallo-beta-lactamase name/family handle",
            "Zn binding-site/cofactor context",
            "Rhea beta-lactam hydrolysis equation where available",
        ),
        disambiguation_holds=(
            "serine beta-lactamase rows",
            "non-beta-lactam amidohydrolase rows",
            "EC-only rows without zinc/metallo evidence",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.45,
        ambiguity_with_existing=("metallo_amidohydrolase_deaminase",),
        existing_fingerprint_id="metallo_beta_lactamase",
        current_runner="scripts/source_metallo_beta_lactamase_family.py",
        oos_preregistration_required=False,
        source_wall_rule_status="implemented_new_fingerprint_runner",
        rationale_template=(
            "Mechanistically distinct zinc beta-lactam hydrolysis family; the dedicated "
            "metallo_beta_lactamase fingerprint (di-zinc, EC 3.5.2.6 shared with serine "
            "beta-lactamase) and MBL-vs-serine/amidohydrolase disambiguation rule are "
            "implemented (2026-06-17)."
        ),
    ),
    _spec(
        family_id="peroxiredoxin_thiol_peroxidase",
        display_name="Peroxiredoxin / thiol-peroxidase",
        scope_query="(reviewed:true) AND (ec:1.11.1.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:1.11.1.*) AND "
            "((protein_name:peroxiredoxin) OR (protein_name:\"glutathione peroxidase\") "
            "OR (protein_name:\"thiol peroxidase\") OR (protein_name:\"alkyl hydroperoxide\"))"
        ),
        required_non_ec_corroborators=(
            "peroxiredoxin / glutathione-peroxidase / thiol-peroxidase family/name handle",
            "peroxidatic cysteine/selenocysteine thiol-redox context",
            "Rhea peroxide (H2O2 / hydroperoxide) reduction equation where available",
        ),
        disambiguation_holds=(
            "heme peroxidase / catalase rows",
            "FAD-dependent NADH peroxidase rows",
            "vanadium/non-heme haloperoxidase / superoxide dismutase rows",
            "EC-only rows without thiol-peroxidase evidence",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.45,
        ambiguity_with_existing=("heme_peroxidase_oxidase",),
        existing_fingerprint_id="peroxiredoxin_thiol_peroxidase",
        current_runner="scripts/source_peroxiredoxin_thiol_peroxidase_family.py",
        oos_preregistration_required=False,
        source_wall_rule_status="implemented_new_fingerprint_runner",
        rationale_template=(
            "Large uncovered EC 1.11.1 thiol/selenol peroxidase subclass (peroxiredoxins, "
            "glutathione peroxidases, thiol peroxidases); the dedicated "
            "peroxiredoxin_thiol_peroxidase fingerprint (peroxidatic Cys/Sec, no heme, EC "
            "1.11.1 shared with heme_peroxidase_oxidase) and its disambiguation rule are "
            "implemented (2026-06-18)."
        ),
    ),
    _spec(
        family_id="aldo_keto_reductase",
        display_name="Aldo-keto reductase",
        scope_query="(reviewed:true) AND (ec:1.1.1.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:1.1.1.*) AND "
            "((protein_name:\"aldo-keto reductase\") OR (protein_name:\"aldose reductase\") "
            "OR (protein_name:AKR))"
        ),
        required_non_ec_corroborators=(
            "aldo-keto reductase family/name handle",
            "NADP/NADPH cosubstrate participant or binding-site context",
            "active-site Tyr/Lys/Asp catalytic tetrad evidence where available",
        ),
        disambiguation_holds=(
            "short-chain dehydrogenase/reductase rows",
            "medium-chain zinc alcohol dehydrogenase rows",
            "flavin/metal redox rows",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.35,
        ambiguity_with_existing=("nad_p_dehydrogenase",),
        existing_fingerprint_id="aldo_keto_reductase",
        current_runner="scripts/source_aldo_keto_reductase_family.py",
        oos_preregistration_required=False,
        source_wall_rule_status="implemented_new_fingerprint_runner",
        rationale_template=(
            "Large NAD(P) hydride-transfer subclass; the dedicated aldo_keto_reductase "
            "fingerprint (Tyr-Lys-His-Asp TIM-barrel) and AKR-vs-SDR/MDR disambiguation "
            "rule are implemented (2026-06-17, +28 first lane)."
        ),
    ),
    _spec(
        family_id="short_chain_dehydrogenase_reductase",
        display_name="Short-chain dehydrogenase/reductase",
        scope_query="(reviewed:true) AND (ec:1.1.1.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:1.1.1.*) AND "
            "((protein_name:\"short-chain dehydrogenase\") OR "
            "(protein_name:\"short chain dehydrogenase\") OR "
            "(protein_name:\"short-chain dehydrogenase/reductase\") OR "
            "(protein_name:SDR)) AND ((keyword:NAD) OR (keyword:NADP))"
        ),
        required_non_ec_corroborators=(
            "SDR family/name/domain handle",
            "NAD(P) participant or Rossmann binding-site context",
            "Ser-Tyr-Lys/Asn active-site evidence where available",
        ),
        disambiguation_holds=(
            "AKR rows",
            "zinc medium-chain alcohol dehydrogenase rows",
            "flavin/metal redox rows",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.35,
        existing_fingerprint_id="short_chain_dehydrogenase_reductase",
        current_runner="scripts/source_short_chain_dehydrogenase_reductase_family.py",
        oos_preregistration_required=False,
        source_wall_rule_status="implemented_existing_fingerprint_runner_subscale_preview",
        ambiguity_with_existing=("nad_p_dehydrogenase",),
        known_blockers=(
            "2026-05 SDR/AKR/NAD(P) control tranche is review-only with 0 import-ready rows",
            "SDR source-free full axis and NAD(P) pocket proxy are not production-ready",
        ),
        rationale_template=(
            "Very large hydride-transfer family, but current source handles are weak; "
            "requires an SDR-specific rule instead of broad EC 1.1.1 padding."
        ),
    ),
    _spec(
        family_id="aldehyde_dehydrogenase",
        display_name="Aldehyde dehydrogenase",
        scope_query="(reviewed:true) AND (ec:1.2.1.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:1.2.1.*) AND "
            "((protein_name:\"aldehyde dehydrogenase\") OR (keyword:NAD) "
            "OR (keyword:NADP))"
        ),
        required_non_ec_corroborators=(
            "aldehyde dehydrogenase family/name handle",
            "NAD(P) cosubstrate participant or binding-site context",
            "catalytic Cys/Glu active-site evidence where available",
        ),
        disambiguation_holds=(
            "molybdopterin aldehyde oxidoreductase rows",
            "flavin aldehyde oxidase rows",
            "generic NAD(P) dehydrogenase rows without ALDH signal",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.35,
        existing_fingerprint_id="aldehyde_dehydrogenase",
        current_runner="scripts/source_aldehyde_dehydrogenase_family.py",
        oos_preregistration_required=False,
        ambiguity_with_existing=("nad_p_dehydrogenase", "molybdopterin_oxidoreductase"),
        rationale_template=(
            "Cys-thiohemiacetal hydride-transfer mechanism; a clean split is needed "
            "from generic NAD(P) and Mo/flavin aldehyde oxidoreductases."
        ),
    ),
    _spec(
        family_id="protein_kinase_ser_thr_tyr",
        display_name="Ser/Thr/Tyr protein kinase",
        scope_query="(reviewed:true) AND ((ec:2.7.10.*) OR (ec:2.7.11.*))",
        corroborator_query=(
            "(reviewed:true) AND ((ec:2.7.10.*) OR (ec:2.7.11.*)) AND "
            "((keyword:\"Protein kinase\") OR (protein_name:\"protein kinase\") "
            "OR (cc_cofactor:magnesium) OR (cc_cofactor:ATP))"
        ),
        required_non_ec_corroborators=(
            "protein kinase family/name/domain handle",
            "ATP/Mg binding-site or cofactor/cosubstrate context",
            "protein-substrate phosphorylation Rhea equation where available",
        ),
        disambiguation_holds=(
            "small-molecule kinase rows",
            "histidine kinase/two-component rows",
            "ATPase or ligase rows",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.35,
        existing_fingerprint_id="protein_kinase_ser_thr_tyr",
        current_runner="scripts/source_protein_kinase_family.py",
        oos_preregistration_required=False,
        ambiguity_with_existing=(
            "pfka_phosphofructokinase",
            "pfkb_ribokinase_family",
            "nucleoside_diphosphate_kinase",
            "atp_amide_ligase",
        ),
        rationale_template=(
            "Massive ATP/Mg phosphoryl-transfer family; only useful after a protein-"
            "substrate kinase split and explicit histidine-kinase holds."
        ),
    ),
    _spec(
        family_id="aminoglycoside_acetyltransferase",
        display_name="Aminoglycoside acetyltransferase",
        scope_query="(reviewed:true) AND (ec:2.3.1.*)",
        corroborator_query=(
            "(reviewed:true) AND (ec:2.3.1.*) AND "
            "((protein_name:aminoglycoside) OR (protein_name:acetyltransferase)) "
            "AND ((keyword:Antibiotic) OR (keyword:Acetyltransferase) OR (cc_cofactor:coa))"
        ),
        required_non_ec_corroborators=(
            "aminoglycoside acetyltransferase name/family handle",
            "acetyl-CoA/CoA participant or binding-site context",
            "aminoglycoside acceptor reaction evidence where available",
        ),
        disambiguation_holds=(
            "generic CoA acyltransferase rows",
            "non-aminoglycoside acetyltransferases",
            "aminoglycoside phosphotransferase/nucleotidyltransferase rows",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.4,
        ambiguity_with_existing=("coa_acyltransferase",),
        existing_fingerprint_id="aminoglycoside_acetyltransferase",
        current_runner="scripts/source_aminoglycoside_acetyltransferase_family.py",
        oos_preregistration_required=False,
        source_wall_rule_status="implemented_new_fingerprint_runner",
        rationale_template=(
            "Resistance-relevant CoA acyl-transfer split; the dedicated "
            "aminoglycoside_acetyltransferase fingerprint (GNAT acetyl-CoA) and "
            "AAC-vs-coa_acyltransferase/APH/ANT disambiguation rule are implemented "
            "(2026-06-17, +32 first lane)."
        ),
    ),
    _spec(
        family_id="aminoglycoside_phosphotransferase",
        display_name="Aminoglycoside phosphotransferase",
        existing_fingerprint_id="aminoglycoside_phosphotransferase",
        current_runner="scripts/source_aminoglycoside_phosphotransferase_family.py",
        oos_preregistration_required=False,
        source_wall_rule_status="implemented_existing_fingerprint",
        scope_query=(
            "(reviewed:true) AND ((ec:2.7.1.95) OR (ec:2.7.1.72) OR "
            "(ec:2.7.1.87) OR (ec:2.7.1.119) OR (ec:2.7.1.163))"
        ),
        corroborator_query=(
            "(reviewed:true) AND ((ec:2.7.1.95) OR (ec:2.7.1.72) OR "
            "(ec:2.7.1.87) OR (ec:2.7.1.119) OR (ec:2.7.1.163)) AND "
            "((ft_binding:*) OR (ft_act_site:*) OR (cc_cofactor:ATP) OR "
            "(cc_cofactor:magnesium) OR (keyword:Kinase) OR (keyword:Transferase))"
        ),
        required_non_ec_corroborators=(
            "aminoglycoside phosphotransferase family/name handle",
            "ATP/Mg participant or binding-site context",
            "aminoglycoside phosphorylation reaction evidence where available",
        ),
        disambiguation_holds=(
            "protein kinase rows",
            "small-molecule kinase rows",
            "aminoglycoside acetyltransferase/nucleotidyltransferase rows",
        ),
        cap_ceiling=DEFAULT_CONFUSABLE_CAP,
        chemistry_confusable=True,
        novelty_keep_factor=0.4,
        ambiguity_with_existing=(
            "pfka_phosphofructokinase",
            "pfkb_ribokinase_family",
            "nucleoside_diphosphate_kinase",
            "protein_kinase_ser_thr_tyr",
        ),
        known_blockers=(
            "2026-06-15 source inspection showed EC 2.7.1.130 and 2.7.1.192 are "
            "lipid-A and PTS MurNAc kinases, not APH; keep APH scope restricted to "
            "reviewed aminoglycoside phosphotransferase/kinase ECs and broaden only "
            "with APH family/name/reaction handles.",
        ),
        rationale_template=(
            "Resistance-relevant ATP phosphoryl transfer; needs explicit separation "
            "from protein and small-molecule kinase fingerprints."
        ),
    ),
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: Path) -> Any:
    return load_json(path)


def _fingerprint_counts(rows: list[dict[str, Any]]) -> Counter:
    return Counter(
        row.get("fingerprint_id")
        for row in rows
        if isinstance(row, dict) and row.get("fingerprint_id")
    )


def _count_positive(rows: list[dict[str, Any]]) -> int:
    return sum(
        1
        for row in rows
        if isinstance(row, dict) and row.get("label_type") == "seed_fingerprint"
    )


def _fetch_total(
    query: str,
    *,
    count_fetcher: Callable[[str], dict[str, Any]],
) -> tuple[int, dict[str, Any] | None]:
    try:
        payload = count_fetcher(query)
    except Exception as exc:  # pragma: no cover - live network guard
        return 0, {"type": type(exc).__name__, "message": str(exc)}
    return int(payload.get("total_results") or 0), None


def evaluate_family_lane_spec(
    spec: dict[str, Any],
    *,
    registry_counts: Counter,
    count_fetcher: Callable[[str], dict[str, Any]],
    min_high_yield_admits: int = MIN_HIGH_YIELD_ADMITS,
) -> dict[str, Any]:
    """Evaluate one family lane spec with live/injected count probes."""
    scope_supply, scope_error = _fetch_total(spec["scope_query"], count_fetcher=count_fetcher)
    corroborated_supply, corroborator_error = _fetch_total(
        spec["corroborator_query"], count_fetcher=count_fetcher
    )
    existing_fp = spec.get("existing_fingerprint_id") or None
    current_count = registry_counts.get(existing_fp or spec["family_id"], 0)
    cap = int(spec["cap_ceiling"])
    cap_room = max(cap - current_count, 0) if existing_fp else cap
    novelty_keep = float(spec["novelty_keep_factor"])
    projected_from_supply = int(round(corroborated_supply * novelty_keep))
    projected_clean_admits = min(cap_room, projected_from_supply)
    corroboration_rate = (
        round(corroborated_supply / scope_supply, 3) if scope_supply else 0.0
    )

    fingerprint_status = "existing" if existing_fp else "new_fingerprint_required"
    runner_status = "existing_runner" if spec.get("current_runner") else "no_runner_yet"
    source_wall_rule_status = str(spec.get("source_wall_rule_status") or "not_implemented")
    source_wall_rule_ready = existing_fp is not None or source_wall_rule_status.startswith(
        "implemented"
    )
    if scope_error or corroborator_error:
        gate_status = "blocked_source_count_fetch_failed"
    elif existing_fp and cap_room < min_high_yield_admits:
        gate_status = "blocked_existing_cap_room_below_150"
    elif not existing_fp and source_wall_rule_ready:
        gate_status = "blocked_new_fingerprint_oos_prereg_and_runner_required"
    elif not existing_fp:
        gate_status = "blocked_new_fingerprint_oos_prereg_and_rule_required"
    elif not spec.get("current_runner"):
        gate_status = "blocked_existing_fingerprint_missing_runner"
    elif projected_clean_admits >= min_high_yield_admits:
        gate_status = "ready_for_preview_not_apply"
    else:
        gate_status = "blocked_projected_clean_admits_below_150"

    return {
        "family_id": spec["family_id"],
        "display_name": spec["display_name"],
        "fingerprint_status": fingerprint_status,
        "existing_fingerprint_id": existing_fp,
        "source_tier": "source_tier_0_reviewed_swissprot",
        "scope_query": spec["scope_query"],
        "corroborator_query": spec["corroborator_query"],
        "reviewed_scope_supply": scope_supply,
        "reviewed_non_ec_corroborated_supply": corroborated_supply,
        "non_ec_mechanism_corroboration_rate_estimate": corroboration_rate,
        "mechanism_corroboration_basis": (
            "UniProt reviewed count for scope EC query versus the same scope plus "
            "non-EC family/cofactor/keyword/name handles. This is a source-supply "
            "estimate, not an admission preview."
        ),
        "novelty_keep_factor": novelty_keep,
        "projected_clean_admits": projected_clean_admits,
        "current_combined_count": current_count,
        "cap_ceiling": cap,
        "cap_room": cap_room,
        "cap_class": (
            "chemistry_confusable_cap_150"
            if spec["chemistry_confusable"]
            else "clean_nonconfusable_cap_250"
        ),
        "chemistry_confusable": bool(spec["chemistry_confusable"]),
        "ambiguity_with_existing_fingerprints": list(spec["ambiguity_with_existing"]),
        "known_blockers": list(spec.get("known_blockers") or []),
        "required_non_ec_corroborators": list(spec["required_non_ec_corroborators"]),
        "disambiguation_holds": list(spec["disambiguation_holds"]),
        "oos_preregistration_required": bool(spec["oos_preregistration_required"]),
        "source_wall_rule_status": source_wall_rule_status,
        "mechanism_rule_required": not source_wall_rule_ready,
        "runner_status": runner_status,
        "current_runner": spec.get("current_runner"),
        "batch_gate_status": gate_status,
        "passes_150_batch_gate_now": gate_status == "ready_for_preview_not_apply",
        "source_count_errors": {
            "scope": scope_error,
            "corroborator": corroborator_error,
        },
        "rationale": spec["rationale_template"],
        "factory_declaration": {
            "scope_query": spec["scope_query"],
            "exclusion_query": " OR ".join(spec["disambiguation_holds"]),
            "required_non_ec_corroborators": list(spec["required_non_ec_corroborators"]),
            "cap_ceiling": cap,
            "source_tier": "source_tier_0",
            "row_guardrail_audit_required": True,
            "preview_command_template": (
                "PYTHONPATH=src python scripts/source_<family>_family.py "
                "--max-records-per-lane <N> --out artifacts/<name>.json "
                "--report work/<name>.md"
            ),
            "apply_command_template": (
                "Only after preview gates pass: rerun the same command with --apply; "
                "the runner must print frozen current702 sha256 before/after."
            ),
        },
    }


def build_high_yield_family_lane_factory(
    *,
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
    specs: tuple[dict[str, Any], ...] = HIGH_YIELD_FAMILY_SPECS,
    count_fetcher: Callable[[str], dict[str, Any]] | None = None,
    created_utc: str | None = None,
    min_high_yield_admits: int = MIN_HIGH_YIELD_ADMITS,
) -> dict[str, Any]:
    """Rank candidate family lanes and expose reusable source-lane declarations."""
    created = created_utc or _utc_now_iso()
    count_fetcher = count_fetcher or fetch_uniprot_query_count
    registry_rows = list(frozen_benchmark_payload) + list(expansion_payload)
    counts = _fingerprint_counts(registry_rows)
    lane_evaluations = [
        evaluate_family_lane_spec(
            spec,
            registry_counts=counts,
            count_fetcher=count_fetcher,
            min_high_yield_admits=min_high_yield_admits,
        )
        for spec in specs
    ]
    ranked = sorted(
        lane_evaluations,
        key=lambda row: (
            row["passes_150_batch_gate_now"],
            row["projected_clean_admits"],
            row["reviewed_non_ec_corroborated_supply"],
            not row["chemistry_confusable"],
        ),
        reverse=True,
    )
    ready = [row for row in ranked if row["passes_150_batch_gate_now"]]
    high_yield_blocked = [
        row
        for row in ranked
        if row["projected_clean_admits"] >= min_high_yield_admits
        and not row["passes_150_batch_gate_now"]
    ]
    existing_cap_limited = [
        row for row in ranked if row["batch_gate_status"] == "blocked_existing_cap_room_below_150"
    ]
    fetch_failed = [
        row for row in ranked if row["batch_gate_status"] == "blocked_source_count_fetch_failed"
    ]
    positive_bronze = _count_positive(expansion_payload)
    oos_bronze = sum(
        1 for row in expansion_payload if row.get("label_type") == "out_of_scope"
    )

    if ready:
        next_action = (
            "Run non-destructive previews for ready existing-runner lanes in ranking order; "
            "apply only after trust-tier, novelty, cap, dedup, and leakage gates pass."
        )
    elif high_yield_blocked:
        top_row = high_yield_blocked[0]
        top = top_row["family_id"]
        mechanism_rule_step = (
            "mechanism disambiguation rule, "
            if top_row["mechanism_rule_required"]
            else ""
        )
        next_action = (
            f"No existing lane has >=150 cap room. Build the `{top}` fingerprint/source "
            f"runner first: ontology node, {mechanism_rule_step}OOS preregistration, "
            "row guardrail audit, preview, tests, then apply only if gates pass."
        )
    else:
        next_action = (
            "No candidate projects >=150 clean rows under current source handles; improve "
            "source handles or add external sources before registry mutation."
        )

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_family_lane_factory_no_labels_or_registry_written",
        "purpose": (
            "Rank high-yield candidate families and materialize reusable lane declarations "
            "so future agents can build source runners without repeating small top-ups."
        ),
        "guardrails": {
            "registry_written": False,
            "labels_created": False,
            "frozen_current702_benchmark_preserved": True,
            "ec_scope_only_never_predictive": True,
            "non_ec_handles_are_scope_admission_only": True,
            "predictive_evidence_created": False,
            "tier_for_future_labels": "bronze",
            "review_status_for_future_labels": "automation_curated",
            "future_entry_namespace": "uniprot",
            "source_trust_policy": (
                "Use source_trust_tiers.evaluate_corroboration; tier_0 requires at "
                "least one counted mechanism axis and EC is never counted."
            ),
            "dedup_against_curated_and_external_required": True,
            "multi_fingerprint_signal_rows_held": True,
        },
        "baseline": {
            "combined_label_surface": len(registry_rows),
            "combined_seed_fingerprint_surface": _count_positive(registry_rows),
            "external_bronze_count": len(expansion_payload),
            "positive_bronze_count": positive_bronze,
            "oos_bronze_count": oos_bronze,
            "silver_ready_count": 0,
            "silver_confirmed_count": 17,
            "projected_provisional_count": 0,
            "fingerprint_count": len(counts),
        },
        "counts": {
            "candidate_families_ranked": len(ranked),
            "ready_existing_lanes_ge_150": len(ready),
            "high_yield_blocked_new_or_infra": len(high_yield_blocked),
            "existing_lanes_cap_room_below_150": len(existing_cap_limited),
            "source_count_fetch_failures": len(fetch_failed),
            "projected_clean_admits_top_family": (
                ranked[0]["projected_clean_admits"] if ranked else 0
            ),
            "remaining_gap_to_10k_seed_surface": max(10_000 - _count_positive(registry_rows), 0),
        },
        "ranking": ranked,
        "ready_lanes": ready,
        "blocked_high_yield_lanes": high_yield_blocked,
        "existing_cap_limited_lanes": existing_cap_limited,
        "next_action": next_action,
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    b = audit["baseline"]
    lines = [
        "# High-Yield Family Lane Factory Scout",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Non-destructive scout/factory artifact. No labels or registries were written.",
        "EC is used only for scope; corroborator handles are admission/source planning only.",
        "",
        "## Result",
        "",
        f"- Candidate families ranked: {c['candidate_families_ranked']}.",
        f"- Ready existing lanes with >=150 projected clean admits: {c['ready_existing_lanes_ge_150']}.",
        f"- High-yield lanes blocked by new fingerprint/preregistration/runner/rule infrastructure: {c['high_yield_blocked_new_or_infra']}.",
        f"- Existing lanes blocked by <150 cap room: {c['existing_lanes_cap_room_below_150']}.",
        f"- Combined label surface: {b['combined_label_surface']}.",
        f"- Combined seed-fingerprint surface: {b['combined_seed_fingerprint_surface']}.",
        f"- Remaining gap to 10k seed surface: {c['remaining_gap_to_10k_seed_surface']}.",
        "",
        "## Ranking",
        "",
        "| Rank | Family | status | scope supply | non-EC corroborated supply | corr. rate | projected clean admits | cap room | cap class |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for idx, row in enumerate(audit["ranking"], start=1):
        lines.append(
            f"| {idx} | {row['family_id']} | {row['batch_gate_status']} | "
            f"{row['reviewed_scope_supply']} | {row['reviewed_non_ec_corroborated_supply']} | "
            f"{row['non_ec_mechanism_corroboration_rate_estimate']} | "
            f"{row['projected_clean_admits']} | {row['cap_room']} | {row['cap_class']} |"
        )
    lines.extend(
        [
            "",
            "## Top Lane Requirements",
            "",
        ]
    )
    for row in audit["ranking"][:5]:
        lines.append(f"### {row['family_id']}")
        lines.append(f"- Status: {row['batch_gate_status']}.")
        lines.append(f"- Source-wall rule status: {row['source_wall_rule_status']}.")
        lines.append(
            "- Required non-EC corroborators: "
            + "; ".join(row["required_non_ec_corroborators"])
            + "."
        )
        lines.append(
            "- Holds: " + "; ".join(row["disambiguation_holds"]) + "."
        )
        lines.append(f"- Rationale: {row['rationale']}")
        lines.append("")
    lines.extend(
        [
            "## Guardrails",
            "",
            f"- Registry written: {audit['guardrails']['registry_written']}.",
            f"- Labels created: {audit['guardrails']['labels_created']}.",
            f"- EC scope-only / never predictive: {audit['guardrails']['ec_scope_only_never_predictive']}.",
            f"- Future labels must be {audit['guardrails']['tier_for_future_labels']} / "
            f"{audit['guardrails']['review_status_for_future_labels']} in the "
            f"{audit['guardrails']['future_entry_namespace']} namespace.",
            "- Dedup against current702 and external bronze is required before apply.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_high_yield_family_lane_factory(
    *,
    out_path: Path,
    report_path: Path | None = None,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    specs: tuple[dict[str, Any], ...] = HIGH_YIELD_FAMILY_SPECS,
    count_fetcher: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    audit = build_high_yield_family_lane_factory(
        frozen_benchmark_payload=_read_json(Path(frozen_benchmark_path)),
        expansion_payload=_read_json(expansion_path) if expansion_path.exists() else [],
        specs=specs,
        count_fetcher=count_fetcher,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
