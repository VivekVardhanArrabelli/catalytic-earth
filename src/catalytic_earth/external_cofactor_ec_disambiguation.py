"""Cofactor/EC disambiguation for the held redox and radical-SAM/cobalamin lanes.

The scale-out drain HELD two families of rows -- do not guess:
- the entire ``redox_cofactor_confounded`` pool (cofactor-confounded redox), and
- the secondary-probe radical-SAM / cobalamin lanes.

This module makes a high-precision subset of them *countable* by corroborating
the annotated cofactor identity against the reviewed reaction/EC class. Scope is
still decided ONLY from reviewed Swiss-Prot/EC/Rhea/cofactor annotation -- the
same field-standard bronze basis -- and EC stays in ``excluded_context``, never a
predictive feature (the benchmark scorer never sees it). Using EC + cofactor to
*decide a label's scope* is exactly what the annotation-anchored basis permits;
the leakage wall (EC/name/prose are never predictive) is unchanged.

A row is disambiguated to a fingerprint only when an annotated cofactor AND a
uniquely matching reaction class agree, and no *other* fingerprint's rule also
fires (multi-signal rows stay held). Each rule below is the textbook cofactor +
EC-class signature of one of the eight fingerprints:

- ``heme_peroxidase_oxidase``  : heme cofactor + EC 1.11.1 (peroxidase).
- ``flavin_monooxygenase``     : flavin (FAD/FMN), no heme + EC 1.14.13/1.14.14
                                 (NAD(P)H- or reduced-flavin-dependent, one O
                                 inserted).
- ``flavin_dehydrogenase_reductase`` : flavin, no heme + EC 1.3 (CH-CH donor),
                                 1.6 (on NAD(P)H), or 1.8.1 (disulfide reductase)
                                 -- hydride/electron transfer, no oxygen insertion.
- ``radical_sam_enzyme``       : CX3CX2C radical-SAM motif, or [4Fe-4S] + SAM
                                 both annotated.
- ``cobalamin_radical_rearrangement`` : adenosylcobalamin/B12 + a mutase /
                                 eliminase EC (5.4.99, 5.4.3, 4.2.1.28/30,
                                 4.3.1.7).

Output is NON-DESTRUCTIVE: a preview artifact in the engine's preview schema
(``applied_labels`` ready for ``apply-external-annotation-anchored-import``, which
appends to the SEPARATE ``external_bronze_labels.json`` expansion registry and
never touches the frozen current702 benchmark).
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from .external_annotation_anchored_import import (
    _build_label,
    _load_json,
    _preview_rows,
    _utc_now_iso,
    cofactor_classes,
)
from .external_scaleout_bronze_import import (
    DEFAULT_CURRENT_MANIFEST_PATH,
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
    _clean_accession,
    build_current702_reference_index,
    rerun_current702_duplicate_screen,
)
from .source_trust_tiers import evaluate_corroboration

# ChEBI ids used only to record a synthesized cofactor on rows that carry their
# cofactor evidence as family flags + residue ligands rather than a cofactor list.
_FE4S4_CHEBI = "CHEBI:49883"
_SAM_CHEBI = "CHEBI:59789"
_ADOCBL_CHEBI = "CHEBI:18408"

# The held pools this module re-examines (all classified "hold" by the scale-out
# drain). ``schema`` selects normalization; ``lanes`` (when present) restricts a
# shard to its secondary-probe lanes.
DISAMBIGUATION_POOLS: tuple[dict[str, Any], ...] = (
    {
        "pool": "redox_cofactor_confounded",
        "schema": "shard",
        "path": (
            "artifacts/v3_external_scaleout_shard_redox_cofactor_confounded"
            "_import_ready_preview_current702_20260609.json"
        ),
    },
    {
        "pool": "plp_radical_cobalamin",
        "schema": "shard",
        "path": (
            "artifacts/v3_external_scaleout_shard_plp_radical_cobalamin"
            "_import_ready_preview_current702_20260609.json"
        ),
        "lanes": (
            "B12 adenosylcobalamin enzymes",
            "B12/cobalamin broad enzymes",
            "cobalamin radical rearrangement",
            "coupled PLP adenosylcobalamin aminomutase",
            "radical SAM named families",
            "radical SAM iron-sulfur",
            "SAM-dependent radical-like boundary",
        ),
    },
    {
        "pool": "wave2_held_redox_radical",
        "schema": "wave2",
        "path": (
            "artifacts/"
            "v3_external_materialization_wave2_import_ready_preview_current702_20260609.json"
        ),
        "lanes": ("redox oxygen/sulfur", "radical-SAM/cobalamin"),
        "only_unscreened": True,
    },
)


def _ec_numbers(row: dict[str, Any]) -> list[str]:
    return [
        str(e)
        for e in (row.get("rhea_ec_provenance") or {}).get("ec_numbers") or []
    ]


def _ec_has_prefix(row: dict[str, Any], prefixes: tuple[str, ...]) -> bool:
    return any(ec.startswith(p) for ec in _ec_numbers(row) for p in prefixes)


def _ligand_names(row: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for locator in row.get("residue_locators") or []:
        if isinstance(locator, dict) and locator.get("ligand_name"):
            names.append(str(locator["ligand_name"]).lower())
    return names


def cofactor_evidence(row: dict[str, Any]) -> dict[str, bool]:
    """Annotated cofactor evidence, fused across the row's evidence channels.

    Reads cofactor names, the shard ``cofactor_family_flags``, and the active-site
    residue ligand names so a row's cofactor identity is detected however the
    materialization pipeline recorded it.
    """
    names = [
        str(c.get("name") or "").lower()
        for c in (row.get("cofactor_provenance") or [])
    ] + _ligand_names(row)
    flags = row.get("cofactor_family_flags") or {}

    def any_name(*keys: str) -> bool:
        return any(any(k in n for k in keys) for n in names)

    return {
        # Catalytic divalent metal (Zn/Mn/Mg/Fe/Ni/Co/Cu/Ca/Cd). UniProt spells the
        # oxidation state inline ("Zn(2+)", "Co(2+)"), so match the element stems.
        # "cob(...)alamin" is matched by the cobalamin key below, not here ("cob" !=
        # "cobalt"), so B12 enzymes do not read as bare metal.
        "metal": any_name(
            "zn",
            "zinc",
            "mn",
            "manganese",
            "mg",
            "magnesium",
            "fe(",
            "fe2",
            "fe3",
            "iron",
            "ni(",
            "nickel",
            "cobalt",
            "co(2",
            "cu",
            "copper",
            "ca(2",
            "calcium",
            "cadmium",
            "divalent metal",
        ),
        "heme": any_name("heme", "haem"),
        "flavin": any_name("fad", "fmn", "flavin"),
        "fe_s": any_name("fe-s", "4fe-4s", "2fe-2s", "3fe-4s", "iron-sulfur")
        or bool(flags.get("sf4_or_fe_s_evidence_present")),
        "sam": any_name("s-adenosyl-l-methionine", "adenosylmethionine", "adomet")
        or bool(flags.get("sam_or_adomet_evidence_present")),
        "cx3cx2c_motif": bool(flags.get("cx3cx2c_motif_evidence_present")),
        # UniProt records B12 cofactors with the cobalt oxidation state spelled
        # inline -- "adenosylcob(III)alamin", "cob(II)alamin", "methylcob(III)alamin"
        # -- so the bare substring "cobalamin" never matches the canonical names.
        # Match the cob(I/II/III)alamin stems too (scope-only annotation read).
        "cobalamin": any_name(
            "cobalamin",
            "adenosylcobalamin",
            "b12",
            "cobamamide",
            "cob(i)alamin",
            "cob(ii)alamin",
            "cob(iii)alamin",
        )
        or bool(flags.get("cobalamin_or_b12_evidence_present")),
        "molybdopterin": any_name(
            "molybdopterin",
            "molybdenum cofactor",
            "mo-molybdopterin",
            "moco",
        )
        or bool(flags.get("molybdopterin_or_moco_evidence_present")),
        "copper": any_name("copper", "cu cation", "cu(2", "cu2", "cu+")
        or bool(flags.get("copper_or_cu_evidence_present")),
        "zinc": any_name("zinc", "zn", "zn(2", "zn2")
        or bool(flags.get("zinc_or_zn_evidence_present")),
        "plp": any_name(
            "pyridoxal",
            "pyridoxal phosphate",
            "pyridoxal 5'-phosphate",
            "pyridoxal-5'-phosphate",
            "plp",
        )
        or bool(flags.get("plp_or_pyridoxal_evidence_present")),
        "thdp": any_name(
            "thiamine",
            "thiamine diphosphate",
            "thiamine pyrophosphate",
            "thdp",
            "tpp",
        )
        or bool(flags.get("thdp_or_thiamine_evidence_present")),
    }


# ---------------------------------------------------------------------------
# Broadened MECHANISM corroborators (the per-family generalization, 2026-06-12).
#
# This engine originally corroborated family scope ONLY via the UniProt COFACTOR comment
# (`cofactor_evidence`). Many families annotate their defining mechanism evidence elsewhere:
# NAD(P) dehydrogenases record NAD(P) as a *cosubstrate* (a Rhea reaction participant + the
# KW-0520/0521 keyword, NOT a cofactor comment), and glycosyltransferases record a
# *sugar-nucleotide donor* (a Rhea participant) plus the Glycosyltransferase keyword. These
# readers add cosubstrate / functional-keyword / binding-or-active-site presence as
# corroborator axes so a family whose defining evidence is NOT a cofactor comment can still
# be admitted honestly (the same lesson as cofactorless ser_his, which needed a triad route).
#
# Every axis is reviewed annotation used for SCOPE/admission ONLY -- it goes in
# `excluded_context`, never a predictive feature, exactly like the cofactor handle. EC stays
# the SCOPE selector (which lane); a mechanism axis CONFIRMS membership. EC is NEVER counted
# toward corroboration (`source_trust_tiers.NON_COUNTED_SCOPE_AXES`).

# NAD(P) nicotinamide cosubstrate token (Rhea reaction participant text / functional keyword).
# "nad" as a substring covers NAD(+)/NADP(+)/NADH/NADPH; reaction equations effectively never
# contain "nad" for any other reason.
_NAD_P_COSUBSTRATE_TOKEN = "nad"
# Nucleotide-sugar donor tokens -- the glycosyltransferase donor (UDP-/GDP-/dTDP-/CDP-/CMP-sugar)
# or the released nucleotide diphosphate. Matched in the Rhea reaction participant text.
_SUGAR_NUCLEOTIDE_DONOR_TOKENS = (
    "udp-",
    "gdp-",
    "dtdp-",
    "cdp-",
    "cmp-",
    "ump-",
    "adp-d-glucose",
    "+ udp",
    "+ gdp",
    "+ dtdp",
    "+ cmp",
)
# SAM/SAH methyl-donor/product tokens. These are Rhea reaction participants, so they are
# mechanism evidence for admission only. They are never predictive features.
_SAM_SAH_METHYL_DONOR_TOKENS = (
    "s-adenosyl-l-methionine",
    "s-adenosylmethionine",
    "adomet",
    "s-adenosyl-l-homocysteine",
    "s-adenosylhomocysteine",
    "adohcy",
)
# Cytochrome P450 monooxygenase handles. EC 1.14 selects scope only; counted mechanism
# corroboration comes from heme, O2/Rhea participant text, P450/monooxygenase keyword,
# or heme-thiolate binding evidence. Peroxide/peroxidase rows are guarded out.
_P450_KEYWORD_TOKENS = ("cytochrome p450", "p450")
_MONOOXYGENASE_KEYWORD_TOKENS = ("monooxygenase", "hydroxylase")
_OXYGENASE_REACTION_TOKENS = (" o2", "o(2)", "dioxygen", "oxygen")
_PEROXIDE_REACTION_TOKENS = ("h2o2", "hydrogen peroxide", "peroxide")
# Non-heme Fe(II)/2-oxoglutarate dioxygenase handles.
_DIOXYGENASE_KEYWORD_TOKENS = ("dioxygenase", "2-oxoglutarate")
_TWO_OG_REACTION_TOKENS = (
    "2-oxoglutarate",
    "2-oxoglutarate(2-)",
    "2-oxoglutaric",
    "alpha-ketoglutarate",
    "oxoglutarate",
)
_TWO_OG_PRODUCT_TOKENS = ("succinate", "co2", "co(2)", "carbon dioxide")
# CoA acyltransferase handles. EC 2.3.1 selects scope only; counted mechanism
# corroboration comes from CoA/acyl-CoA Rhea participant text, CoA binding feature
# text, the Acyltransferase keyword/domain handle, or active-/binding-site
# residue annotations. Hydrolase side-EC rows stay held.
_COA_ACYL_COA_TOKENS = (
    "coenzyme a",
    "coa",
    "acyl-coa",
    "acetyl-coa",
    "malonyl-coa",
    "succinyl-coa",
    "butyryl-coa",
    "propionyl-coa",
    "palmitoyl-coa",
    "benzoyl-coa",
    "hydroxycinnamoyl-coa",
    "3-oxoacyl-coa",
)
_ACYLTRANSFERASE_KEYWORD_TOKENS = ("acyltransferase",)
# Cofactor-independent isomerase handles. EC 5.3 selects scope only; counted
# mechanism corroboration comes from Rhea isomerization equation text, the Isomerase
# keyword/domain handle, or active-/binding-site residue annotations. Rows with
# non-5.3 side ECs stay held until a subclass rule explicitly owns them.
_ISOMERASE_KEYWORD_TOKENS = ("isomerase",)
_ISOMERIZATION_REACTION_TOKENS = (" = ", "isomer", "epimer", "racem", "mutase")
# Molybdopterin/Mo-cofactor oxidoreductase handles. EC 1.* scopes the candidate pool
# only; counted mechanism corroboration comes from Mo-cofactor/molybdopterin annotation,
# Mo-pterin feature text, Rhea redox/oxo-transfer participants, Molybdenum keyword/domain,
# or active-/binding-/metal-site residue evidence. Heme/flavin/copper electron relays can
# be legitimate subclass context, but if they independently satisfy another fingerprint the
# existing multi-fingerprint conflict guard holds the row.
_MOLYBDOPTERIN_TOKENS = (
    "molybdopterin",
    "molybdenum cofactor",
    "mo-molybdopterin",
    "moco",
    "molybd",
)
_MOLYBDENUM_KEYWORD_TOKENS = ("molybdenum", "molybdopterin")
_MOLYBDOPTERIN_REDOX_REACTION_TOKENS = (
    "nad(+)",
    "nadp(+)",
    "nadh",
    "nadph",
    "quinone",
    "quinol",
    "cytochrome",
    "ferredoxin",
    "electron",
    "reduced",
    "oxidized",
    "acceptor",
    "donor",
)
_MOLYBDOPTERIN_OXO_TRANSFER_REACTION_TOKENS = (
    "nitrate",
    "nitrite",
    "formate",
    "co2",
    "co(2)",
    "sulfite",
    "sulfate",
    "dimethyl sulfoxide",
    "dimethyl sulfide",
    "trimethylamine n-oxide",
    "xanthine",
    "uric acid",
    "h2o",
    "h(2)o",
)
# Copper oxidoreductase handles. EC 1.10.3 / 1.4.3 scopes the reviewed copper supply only;
# counted mechanism corroboration comes from copper cofactor/feature evidence, Copper keyword,
# Rhea oxygen/redox equation text, or active-/binding-/metal-site evidence. Heme/flavin/Mo and
# non-oxidoreductase side rows stay held.
_COPPER_KEYWORD_TOKENS = ("copper",)
_COPPER_FEATURE_TOKENS = ("copper", "cu cation", "cu(2", "cu2", "cu+")
_COPPER_REDOX_REACTION_TOKENS = (
    " o2",
    "o(2)",
    "h2o2",
    "hydrogen peroxide",
    "quinone",
    "quinol",
    "oxidized",
    "reduced",
    "electron",
    "radical",
    "aldehyde",
    "nh4",
)
_COPPER_OXIDASE_REACTION_TOKENS = (
    "oxidase",
    "amine",
    "laccase",
    "ascorbate",
    "catechol",
    "hydroquinone",
    "dioxygen",
)
# Non-PLP racemase/epimerase handles. EC 5.1 scopes the candidate supply only;
# counted mechanism corroboration comes from racemase/epimerase/mutarotase text,
# Rhea isomerization/racemization equations, active-/binding-site annotations,
# metal context, or explicit cofactorless context. PLP and side-EC rows stay held.
_RACEMASE_EPIMERASE_TEXT_TOKENS = ("racem", "epimer", "mutarot")
# ATP-dependent amide ligase handles. EC 6.3 scopes the candidate supply only;
# counted mechanism corroboration comes from ATP/ADP/phosphate or Mg context,
# Ligase/ATP-grasp family text, C-N/amide ligation reaction text, acyl-phosphate
# intermediate text, or active-/binding-site annotations. Biotin carboxylases,
# kinases/phosphotransferases, hydrolase/transferase side rows, and generic side-EC
# rows stay held.
_ATP_LIGASE_NUCLEOTIDE_TOKENS = (
    "atp",
    "adenosine 5'-triphosphate",
    "adenosine triphosphate",
    "adp",
    "adenosine 5'-diphosphate",
    "orthophosphate",
    "phosphate",
)
_ATP_LIGASE_MAGNESIUM_TOKENS = ("magnesium", "mg(2", "mg2")
_ATP_LIGASE_TEXT_TOKENS = ("ligase",)
_ATP_GRASP_TEXT_TOKENS = ("atp-grasp", "atp grasp")
_ATP_AMIDE_LIGATION_TOKENS = (
    "amide",
    "peptide",
    "glutamine",
    "glutamate",
    "asparagine",
    "aspartate",
    "carboxylate",
    "carboxy-",
    "c-n bond",
    "c-n",
)
_ATP_ACYL_PHOSPHATE_TOKENS = (
    "acyl phosphate",
    "acyl-phosphate",
    "phosphorylated intermediate",
    "carboxyphosphate",
    "carboxyl phosphate",
)
_BIOTIN_CARBOXYLASE_BOUNDARY_TOKENS = ("biotin", "carboxylase", "carboxybiotin")
_KINASE_BOUNDARY_TOKENS = ("kinase", "phosphotransferase")
# Class-II metal aldolase handles. EC 4.1.2/4.1.3 scopes lyase candidates only;
# counted corroboration comes from metal cofactor/site evidence, Lyase/aldolase
# family text, Rhea C-C/oxoacid reaction context, or active-/binding-/metal-site
# evidence. PLP, ThDP, class-I Schiff-base, hydrolase/transferase/oxidoreductase,
# and side-EC rows stay held.
_CLASS_II_ALDOLASE_TEXT_TOKENS = (
    "aldolase",
    "aldol",
    "dehydro-deoxy",
    "keto",
    "aldehyde",
    "pyruvate",
    "oxaloacetate",
)
_LYASE_TEXT_TOKENS = ("lyase",)
_CLASS_II_ALDOLASE_CC_TOKENS = (
    "carbon-carbon",
    "c-c",
    "deoxyribose",
    "fructose",
    "tagatose",
    "keto",
    "aldehyde",
    "acetaldehyde",
    "pyruvate",
)
_THDP_BOUNDARY_TOKENS = (
    "thiamine",
    "thdp",
    "tpp",
    "thiamine diphosphate",
    "thiamine pyrophosphate",
)
_THDP_MG_TOKENS = ("magnesium", "mg(2", "mg2")
_THDP_FAMILY_TEXT_TOKENS = (
    "thiamine",
    "thdp",
    "tpp",
    "transketolase",
    "decarboxylase",
    "2-oxoacid",
    "2-oxoglutarate dehydrogenase",
    "pyruvate dehydrogenase",
    "acetolactate synthase",
    "acetohydroxyacid synthase",
    "phosphoketolase",
    "benzaldehyde lyase",
    "glyoxylate carboligase",
)
_THDP_REACTION_TOKENS = (
    "thiamine diphosphate",
    "thiamine pyrophosphate",
    "2-hydroxyethyl-thdp",
    "hydroxyethyl-thiamine",
    "co2",
    "co(2)",
    "carbon dioxide",
    "acetaldehyde",
    "glycolaldehyde",
    "glyoxylate",
    "2-oxoglutarate",
    "2-oxoglutarate(2-)",
    "pyruvate",
)
_THDP_KINASE_HYDROLASE_BOUNDARY_TOKENS = (
    "kinase",
    "phosphotransferase",
    "hydrolase",
)
_SCHIFF_CLASS_I_BOUNDARY_TOKENS = ("schiff", "class i aldolase")
# Zinc hydratase / hydro-lyase handles. EC 4.2.1 scopes reviewed hydro-lyase
# candidates only; counted mechanism corroboration comes from Zn cofactor/site,
# Rhea water elimination/addition/carbonic chemistry, lyase/hydratase family text,
# or active-/binding-/metal-site evidence. PLP/ThDP, hydrolase/transferase/
# aldolase/isomerase boundary rows, and non-4.2.1 side ECs stay held.
_ZINC_FEATURE_TOKENS = ("zinc", "zn", "zn(2", "zn2")
_ZINC_LYASE_HYDRATASE_TEXT_TOKENS = (
    "lyase",
    "hydratase",
    "dehydratase",
    "anhydrase",
    "hydro-lyase",
    "hydro lyase",
    "carbonate dehydratase",
)
_ZINC_HYDRATION_REACTION_TOKENS = (
    "h2o",
    "h(2)o",
    "water",
    "hydrogencarbonate",
    "bicarbonate",
    "co2",
    "co(2)",
    "carbon dioxide",
    "cyanamide",
)
_ZINC_LYASE_BOUNDARY_TEXT_TOKENS = (
    "hydrolase",
    "transferase",
    "aldolase",
    "isomerase",
)
# Feature codes that count as an annotated active-site / binding / metal residue role.
_ACTIVE_OR_BINDING_FEATURE_CODES = frozenset({"ACT_SITE", "BINDING", "METAL"})


def _row_keywords(row: dict[str, Any]) -> list[str]:
    return [str(k).lower() for k in (row.get("keywords") or []) if k]


def _reaction_texts(row: dict[str, Any]) -> list[str]:
    """Lower-cased Rhea reaction-participant text already on the ingestion row.

    Reads both the UniProt catalytic-activity ``reaction`` name and the Rhea fallback
    ``equation`` -- the cosubstrate / nucleotide-sugar donor is a reaction PARTICIPANT, so
    it is mechanism evidence (NOT EC), readable without an extra fetch.
    """
    texts: list[str] = []
    for rec in (row.get("rhea_ec_provenance") or {}).get("rhea_records") or []:
        if not isinstance(rec, dict):
            continue
        for key in ("reaction", "equation"):
            value = rec.get(key)
            if value:
                texts.append(str(value).lower())
    return texts


def _feature_codes(row: dict[str, Any]) -> set[str]:
    return {
        str(loc.get("feature_code") or "")
        for loc in (row.get("residue_locators") or [])
        if isinstance(loc, dict)
    }


def _feature_texts(row: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    for feature in row.get("source_evidence_features") or []:
        if not isinstance(feature, dict):
            continue
        for key in ("description", "ligand_name", "ligand_note", "feature_type"):
            value = feature.get(key)
            if value:
                texts.append(str(value).lower())
    for locator in row.get("residue_locators") or []:
        if not isinstance(locator, dict):
            continue
        for key in ("ligand_name", "feature_type"):
            value = locator.get(key)
            if value:
                texts.append(str(value).lower())
    return texts


def mechanism_corroborator_axes(row: dict[str, Any]) -> dict[str, bool]:
    """Annotated mechanism evidence fused across cofactor + cosubstrate + keyword + residue.

    Returns the existing `cofactor_evidence` booleans PLUS the broadened axes the new families
    need. The broadened axes are reviewed annotation read for SCOPE/admission only.
    """
    evidence = dict(cofactor_evidence(row))
    keywords = _row_keywords(row)
    reactions = _reaction_texts(row)
    cofactor_names = [
        str(c.get("name") or "").lower() for c in (row.get("cofactor_provenance") or [])
    ]
    feature_texts = _feature_texts(row)
    protein_name = str(row.get("protein_name") or "").lower()

    def in_any(haystacks: list[str], *tokens: str) -> bool:
        return any(any(tok in text for tok in tokens) for text in haystacks)

    keyword_nad_p = any(_NAD_P_COSUBSTRATE_TOKEN in kw for kw in keywords)
    cosubstrate_nad_p_reaction = in_any(reactions, _NAD_P_COSUBSTRATE_TOKEN)
    cosubstrate_nad_p = (
        keyword_nad_p
        or cosubstrate_nad_p_reaction
        or in_any(cofactor_names, _NAD_P_COSUBSTRATE_TOKEN)
    )
    sugar_nucleotide_donor = in_any(reactions, *_SUGAR_NUCLEOTIDE_DONOR_TOKENS)
    keyword_glycosyltransferase = any("glycosyltransferase" in kw for kw in keywords)
    sam_sah_methyl_donor_reaction = in_any(reactions, *_SAM_SAH_METHYL_DONOR_TOKENS)
    keyword_methyltransferase = any("methyltransferase" in kw for kw in keywords)
    keyword_p450 = in_any(keywords, *_P450_KEYWORD_TOKENS)
    keyword_monooxygenase = in_any(keywords, *_MONOOXYGENASE_KEYWORD_TOKENS)
    oxygenase_reaction = in_any(reactions, *_OXYGENASE_REACTION_TOKENS)
    peroxide_reaction = in_any(reactions, *_PEROXIDE_REACTION_TOKENS)
    heme_thiolate_binding = bool(evidence.get("heme")) and any(
        "thiolate" in text
        or ("heme" in text and ("cys" in text or "cysteine" in text))
        for text in feature_texts + cofactor_names
    )
    keyword_dioxygenase = in_any(keywords, *_DIOXYGENASE_KEYWORD_TOKENS)
    two_og_reaction = in_any(reactions, *_TWO_OG_REACTION_TOKENS)
    succinate_co2_product = in_any(reactions, *_TWO_OG_PRODUCT_TOKENS)
    coa_acyl_coa_reaction = in_any(reactions, *_COA_ACYL_COA_TOKENS)
    coa_acyl_coa_feature = in_any(feature_texts + cofactor_names, *_COA_ACYL_COA_TOKENS)
    keyword_acyltransferase = in_any(keywords, *_ACYLTRANSFERASE_KEYWORD_TOKENS)
    hydrolase_side_ec = _ec_has_prefix(row, ("3.1.", "3.4.", "3.5."))
    keyword_isomerase = in_any(keywords, *_ISOMERASE_KEYWORD_TOKENS)
    isomerization_reaction = in_any(reactions, *_ISOMERIZATION_REACTION_TOKENS)
    racemase_epimerase_text = in_any(
        reactions + keywords + [protein_name], *_RACEMASE_EPIMERASE_TEXT_TOKENS
    )
    non_5_3_side_ec = any(ec and not ec.startswith("5.3") for ec in _ec_numbers(row))
    non_5_1_side_ec = any(ec and not ec.startswith("5.1") for ec in _ec_numbers(row))
    transferase_side_ec = any(ec.startswith("2.") for ec in _ec_numbers(row))
    oxidoreductase_side_ec = any(ec.startswith("1.") for ec in _ec_numbers(row))
    keyword_molybdenum = in_any(keywords, *_MOLYBDENUM_KEYWORD_TOKENS)
    molybdopterin_moco = bool(evidence.get("molybdopterin")) or in_any(
        cofactor_names + feature_texts, *_MOLYBDOPTERIN_TOKENS
    )
    molybdopterin_feature_or_ligand = in_any(feature_texts, *_MOLYBDOPTERIN_TOKENS)
    molybdopterin_redox_reaction = in_any(
        reactions, *_MOLYBDOPTERIN_REDOX_REACTION_TOKENS
    )
    molybdopterin_oxo_transfer_reaction = in_any(
        reactions, *_MOLYBDOPTERIN_OXO_TRANSFER_REACTION_TOKENS
    )
    non_oxidoreductase_side_ec = any(
        ec and not ec.startswith("1.") for ec in _ec_numbers(row)
    )
    molybdopterin_biosynthesis_boundary = any(
        token in protein_name
        for token in (
            "cofactor biosynthesis",
            "molybdopterin synthase",
            "molybdopterin adenylyltransferase",
            "molybdenum cofactor sulfurase",
            "moco sulfurase",
        )
    ) and not any("oxidoreductase" in kw for kw in keywords)
    keyword_copper = in_any(keywords, *_COPPER_KEYWORD_TOKENS)
    copper_feature_or_ligand = bool(evidence.get("copper")) or in_any(
        cofactor_names + feature_texts, *_COPPER_FEATURE_TOKENS
    )
    copper_redox_reaction = in_any(reactions, *_COPPER_REDOX_REACTION_TOKENS)
    copper_oxidase_reaction = in_any(reactions + keywords + [protein_name], *_COPPER_OXIDASE_REACTION_TOKENS)
    copper_boundary_heme_flavin_molybdopterin = (
        evidence.get("heme", False)
        or evidence.get("flavin", False)
        or molybdopterin_moco
    )
    atp_ligase_atp_or_adp_phosphate = in_any(
        reactions + cofactor_names + feature_texts, *_ATP_LIGASE_NUCLEOTIDE_TOKENS
    )
    atp_ligase_mg_context = in_any(
        cofactor_names + feature_texts, *_ATP_LIGASE_MAGNESIUM_TOKENS
    )
    keyword_ligase = in_any(keywords + [protein_name], *_ATP_LIGASE_TEXT_TOKENS)
    atp_grasp_family_text = in_any(
        keywords + [protein_name] + feature_texts, *_ATP_GRASP_TEXT_TOKENS
    )
    atp_amide_ligation_text = in_any(
        reactions + [protein_name], *_ATP_AMIDE_LIGATION_TOKENS
    )
    atp_acyl_phosphate_intermediate = in_any(
        reactions + feature_texts + [protein_name], *_ATP_ACYL_PHOSPHATE_TOKENS
    )
    biotin_carboxylase_boundary = (
        in_any(cofactor_names + feature_texts + keywords + [protein_name], *_BIOTIN_CARBOXYLASE_BOUNDARY_TOKENS)
        or _ec_has_prefix(row, ("6.3.4", "6.4.1"))
    )
    kinase_boundary = in_any(keywords + [protein_name], *_KINASE_BOUNDARY_TOKENS) or _ec_has_prefix(
        row, ("2.7.",)
    )
    non_6_3_side_ec = any(ec and not ec.startswith("6.3") for ec in _ec_numbers(row))
    class_ii_metal_aldolase_text = in_any(
        reactions + keywords + [protein_name], *_CLASS_II_ALDOLASE_TEXT_TOKENS
    )
    keyword_lyase = in_any(keywords + [protein_name], *_LYASE_TEXT_TOKENS)
    class_ii_aldolase_cc_reaction = in_any(reactions, *_CLASS_II_ALDOLASE_CC_TOKENS)
    thdp_boundary_signal = in_any(
        cofactor_names + feature_texts + keywords + [protein_name], *_THDP_BOUNDARY_TOKENS
    ) or bool(evidence.get("thdp"))
    thdp_mg_context = in_any(cofactor_names + feature_texts, *_THDP_MG_TOKENS)
    thdp_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts, *_THDP_FAMILY_TEXT_TOKENS
    )
    thdp_reaction_context = in_any(reactions, *_THDP_REACTION_TOKENS)
    thdp_kinase_hydrolase_boundary = in_any(
        keywords + [protein_name], *_THDP_KINASE_HYDROLASE_BOUNDARY_TOKENS
    )
    zinc_feature_or_ligand = bool(evidence.get("zinc")) or in_any(
        cofactor_names + feature_texts, *_ZINC_FEATURE_TOKENS
    )
    zinc_lyase_hydratase_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_ZINC_LYASE_HYDRATASE_TEXT_TOKENS,
    )
    zinc_hydration_elimination_reaction = in_any(
        reactions, *_ZINC_HYDRATION_REACTION_TOKENS
    )
    zinc_lyase_boundary_text = in_any(
        keywords + [protein_name], *_ZINC_LYASE_BOUNDARY_TEXT_TOKENS
    )
    non_4_2_1_side_ec = any(ec and not ec.startswith("4.2.1") for ec in _ec_numbers(row))
    non_thdp_scope_side_ec = any(
        ec
        and not (
            ec.startswith("2.2.1")
            or ec.startswith("4.1.1")
            or ec.startswith("1.2.4")
        )
        for ec in _ec_numbers(row)
    )
    schiff_class_i_boundary_signal = in_any(
        feature_texts + keywords + [protein_name], *_SCHIFF_CLASS_I_BOUNDARY_TOKENS
    )
    non_4_1_2_or_4_1_3_side_ec = any(
        ec and not (ec.startswith("4.1.2") or ec.startswith("4.1.3"))
        for ec in _ec_numbers(row)
    )
    cofactorless_context = not any(
        evidence.get(key, False)
        for key in (
            "heme",
            "flavin",
            "fe_s",
            "sam",
            "cobalamin",
            "molybdopterin",
            "copper",
            "plp",
            "thdp",
        )
    )

    evidence.update(
        {
            "keyword_nad_p": keyword_nad_p,
            # NAD(P) read specifically from a reaction participant (mechanism, not EC/keyword).
            "cosubstrate_nad_p_reaction": cosubstrate_nad_p_reaction,
            "cosubstrate_nad_p": cosubstrate_nad_p,
            "sugar_nucleotide_donor": sugar_nucleotide_donor,
            "keyword_glycosyltransferase": keyword_glycosyltransferase,
            "sam_sah_methyl_donor_reaction": sam_sah_methyl_donor_reaction,
            "sam_sah_methyl_donor": sam_sah_methyl_donor_reaction
            or evidence.get("sam", False),
            "keyword_methyltransferase": keyword_methyltransferase,
            "keyword_p450": keyword_p450,
            "keyword_monooxygenase": keyword_monooxygenase,
            "oxygenase_reaction": oxygenase_reaction,
            "peroxide_reaction": peroxide_reaction,
            "heme_thiolate_binding": heme_thiolate_binding,
            "keyword_dioxygenase": keyword_dioxygenase,
            "two_og_reaction": two_og_reaction,
            "succinate_co2_product": succinate_co2_product,
            "coa_acyl_coa_reaction": coa_acyl_coa_reaction,
            "coa_acyl_coa_feature": coa_acyl_coa_feature,
            "keyword_acyltransferase": keyword_acyltransferase,
            "hydrolase_side_ec": hydrolase_side_ec,
            "keyword_isomerase": keyword_isomerase,
            "isomerization_reaction": isomerization_reaction,
            "racemase_epimerase_text": racemase_epimerase_text,
            "non_5_3_side_ec": non_5_3_side_ec,
            "non_5_1_side_ec": non_5_1_side_ec,
            "transferase_side_ec": transferase_side_ec,
            "oxidoreductase_side_ec": oxidoreductase_side_ec,
            "keyword_molybdenum": keyword_molybdenum,
            "molybdopterin_moco": molybdopterin_moco,
            "molybdopterin_feature_or_ligand": molybdopterin_feature_or_ligand,
            "molybdopterin_redox_reaction": molybdopterin_redox_reaction,
            "molybdopterin_oxo_transfer_reaction": molybdopterin_oxo_transfer_reaction,
            "non_oxidoreductase_side_ec": non_oxidoreductase_side_ec,
            "molybdopterin_biosynthesis_boundary": molybdopterin_biosynthesis_boundary,
            "keyword_copper": keyword_copper,
            "copper_feature_or_ligand": copper_feature_or_ligand,
            "copper_redox_reaction": copper_redox_reaction,
            "copper_oxidase_reaction": copper_oxidase_reaction,
            "copper_boundary_heme_flavin_molybdopterin": copper_boundary_heme_flavin_molybdopterin,
            "atp_ligase_atp_or_adp_phosphate": atp_ligase_atp_or_adp_phosphate,
            "atp_ligase_mg_context": atp_ligase_mg_context,
            "keyword_ligase": keyword_ligase,
            "atp_grasp_family_text": atp_grasp_family_text,
            "atp_amide_ligation_text": atp_amide_ligation_text,
            "atp_acyl_phosphate_intermediate": atp_acyl_phosphate_intermediate,
            "biotin_carboxylase_boundary": biotin_carboxylase_boundary,
            "kinase_boundary": kinase_boundary,
            "non_6_3_side_ec": non_6_3_side_ec,
            "class_ii_metal_aldolase_text": class_ii_metal_aldolase_text,
            "keyword_lyase": keyword_lyase,
            "class_ii_aldolase_cc_reaction": class_ii_aldolase_cc_reaction,
            "thdp_boundary_signal": thdp_boundary_signal,
            "thdp_mg_context": thdp_mg_context,
            "thdp_family_text": thdp_family_text,
            "thdp_reaction_context": thdp_reaction_context,
            "thdp_kinase_hydrolase_boundary": thdp_kinase_hydrolase_boundary,
            "zinc_feature_or_ligand": zinc_feature_or_ligand,
            "zinc_lyase_hydratase_text": zinc_lyase_hydratase_text,
            "zinc_hydration_elimination_reaction": zinc_hydration_elimination_reaction,
            "zinc_lyase_boundary_text": zinc_lyase_boundary_text,
            "non_4_2_1_side_ec": non_4_2_1_side_ec,
            "non_thdp_scope_side_ec": non_thdp_scope_side_ec,
            "schiff_class_i_boundary_signal": schiff_class_i_boundary_signal,
            "non_4_1_2_or_4_1_3_side_ec": non_4_1_2_or_4_1_3_side_ec,
            "plp_boundary_signal": evidence.get("plp", False),
            "cofactorless_context": cofactorless_context,
            "active_or_binding_site_present": bool(
                _feature_codes(row) & _ACTIVE_OR_BINDING_FEATURE_CODES
            ),
        }
    )
    return evidence


def corroborator_axes_present(evidence: dict[str, bool], row: dict[str, Any]) -> list[str]:
    """Trust-tier corroborator axes a row satisfies + the non-counted EC scope hint.

    Maps the row's annotated mechanism evidence onto `source_trust_tiers.CORROBORATOR_AXES`
    (counted) plus `ec_scope_hint` (recognized but NEVER counted toward the N-of-M rule).
    """
    axes: set[str] = set()
    if (
        evidence.get("metal")
        or evidence.get("heme")
        or evidence.get("flavin")
        or evidence.get("fe_s")
        or evidence.get("sam")
        or evidence.get("cobalamin")
        or evidence.get("cosubstrate_nad_p")
        or evidence.get("sugar_nucleotide_donor")
        or evidence.get("sam_sah_methyl_donor")
        or evidence.get("two_og_reaction")
        or evidence.get("coa_acyl_coa_reaction")
        or evidence.get("coa_acyl_coa_feature")
        or evidence.get("molybdopterin_moco")
        or evidence.get("copper_feature_or_ligand")
        or evidence.get("atp_ligase_atp_or_adp_phosphate")
        or evidence.get("atp_ligase_mg_context")
        or evidence.get("thdp")
        or evidence.get("thdp_mg_context")
        or evidence.get("zinc_feature_or_ligand")
        or (
            evidence.get("metal")
            and (evidence.get("class_ii_metal_aldolase_text") or evidence.get("class_ii_aldolase_cc_reaction"))
        )
    ):
        axes.add("cofactor_or_cosubstrate")
    if (
        evidence.get("cosubstrate_nad_p_reaction")
        or evidence.get("sugar_nucleotide_donor")
        or evidence.get("sam_sah_methyl_donor_reaction")
        or evidence.get("oxygenase_reaction")
        or evidence.get("two_og_reaction")
        or evidence.get("succinate_co2_product")
        or evidence.get("coa_acyl_coa_reaction")
        or evidence.get("isomerization_reaction")
        or evidence.get("molybdopterin_redox_reaction")
        or evidence.get("molybdopterin_oxo_transfer_reaction")
        or evidence.get("copper_redox_reaction")
        or evidence.get("copper_oxidase_reaction")
        or evidence.get("racemase_epimerase_text")
        or evidence.get("atp_ligase_atp_or_adp_phosphate")
        or evidence.get("atp_amide_ligation_text")
        or evidence.get("atp_acyl_phosphate_intermediate")
        or evidence.get("class_ii_aldolase_cc_reaction")
        or evidence.get("class_ii_metal_aldolase_text")
        or evidence.get("thdp_reaction_context")
        or evidence.get("zinc_hydration_elimination_reaction")
    ):
        axes.add("rhea_reaction_or_participant_pattern")
    if (
        evidence.get("active_or_binding_site_present")
        or evidence.get("cx3cx2c_motif")
        or evidence.get("heme_thiolate_binding")
        or evidence.get("molybdopterin_feature_or_ligand")
        or evidence.get("copper_feature_or_ligand")
        or evidence.get("zinc_feature_or_ligand")
    ):
        axes.add("active_site_motif_or_residue_role")
    if (
        evidence.get("keyword_glycosyltransferase")
        or evidence.get("keyword_nad_p")
        or evidence.get("keyword_methyltransferase")
        or evidence.get("keyword_p450")
        or evidence.get("keyword_monooxygenase")
        or evidence.get("keyword_dioxygenase")
        or evidence.get("keyword_acyltransferase")
        or evidence.get("keyword_isomerase")
        or evidence.get("keyword_molybdenum")
        or evidence.get("keyword_copper")
        or evidence.get("racemase_epimerase_text")
        or evidence.get("keyword_ligase")
        or evidence.get("atp_grasp_family_text")
        or evidence.get("keyword_lyase")
        or evidence.get("class_ii_metal_aldolase_text")
        or evidence.get("thdp_family_text")
        or evidence.get("zinc_lyase_hydratase_text")
    ):
        axes.add("domain_or_family_profile")
    if _ec_numbers(row):
        axes.add("ec_scope_hint")  # non-counted: EC decides scope only
    return sorted(axes)


# EC-prefix signatures for the metal_dependent_hydrolase v2 sub-families (Stage 2).
# Mutually exclusive prefixes + an annotated catalytic metal keep "exactly one rule
# fires"; the metal requirement excludes Ser/Cys peptidases (3.4.21/22/23), Cys-based
# protein-tyrosine phosphatases (3.1.3.48 carry no catalytic metal), and serine
# amidases. EC is used for SCOPE only and stays in excluded_context (never predictive).
_METALLOPEPTIDASE_EC = ("3.4.24", "3.4.17", "3.4.11")
_METALLOPHOSPHOESTERASE_NUCLEASE_EC = (
    "3.1.4",
    "3.1.11",
    "3.1.12",
    "3.1.13",
    "3.1.14",
    "3.1.15",
    "3.1.16",
    "3.1.21",
    "3.1.22",
    "3.1.23",
    "3.1.24",
    "3.1.25",
    "3.1.26",
    "3.1.27",
    "3.1.30",
    "3.1.31",
)
_METALLOPHOSPHOMONOESTERASE_EC = ("3.1.3",)
_METALLO_AMIDOHYDROLASE_DEAMINASE_EC = ("3.5.2", "3.5.4", "3.5.1")

# EC scope selectors for the broadened-handle families (2026-06-12). The mechanism
# corroborator (NAD(P) cosubstrate / sugar-nucleotide donor + keyword) confirms membership;
# the EC prefix only selects the lane and stays in excluded_context (never predictive).
_NAD_P_DEHYDROGENASE_EC = ("1.1.1",)  # CH-OH donor, NAD(P) acceptor
_GLYCOSYLTRANSFERASE_EC = ("2.4",)    # glycosyl/hexosyl/pentosyl/sialyl transferases
_SAM_METHYLTRANSFERASE_EC = ("2.1.1",)  # methyl group transfer, mostly SAM/SAH donor/product
_P450_MONOOXYGENASE_EC = ("1.14.",)  # paired-donor oxidoreductases incorporating one O atom
_NON_HEME_IRON_2OG_EC = ("1.14.11",)  # 2-oxoglutarate-dependent dioxygenases
_COA_ACYLTRANSFERASE_EC = ("2.3.1",)  # acyltransferases using CoA/acyl-CoA donors
_COFACTOR_INDEPENDENT_ISOMERASE_EC = ("5.3.",)  # intramolecular isomerases
_MOLYBDOPTERIN_OXIDOREDUCTASE_EC = ("1.",)  # oxidoreductases; Mo-cofactor handles confirm
_COPPER_OXIDOREDUCTASE_EC = (
    "1.10.3",
    "1.4.3",
)  # copper oxidases; copper/Rhea handles confirm
_METAL_RACEMASE_EPIMERASE_NON_PLP_EC = ("5.1.",)  # racemase/epimerase scope only
_ATP_AMIDE_LIGASE_EC = ("6.3.",)  # C-N ligases; ATP/Mg/Rhea handles confirm
_CLASS_II_METAL_ALDOLASE_EC = ("4.1.2", "4.1.3")  # metal aldol lyases; EC is scope only
_THIAMINE_DIPHOSPHATE_ENZYME_EC = (
    "2.2.1",
    "4.1.1",
    "1.2.4",
)  # ThDP ylide/carbonyl chemistry; EC is scope only
_ZINC_LYASE_HYDRATASE_EC = ("4.2.1",)  # zinc hydro-lyases; EC is scope only


# Each rule: fingerprint id -> predicate over (cofactor_evidence, row).
DISAMBIGUATION_RULES: tuple[tuple[str, Callable[[dict[str, bool], dict[str, Any]], bool]], ...] = (
    (
        "heme_peroxidase_oxidase",
        lambda c, row: c["heme"] and _ec_has_prefix(row, ("1.11.1",)),
    ),
    (
        "metallopeptidase",
        lambda c, row: c["metal"] and _ec_has_prefix(row, _METALLOPEPTIDASE_EC),
    ),
    (
        "metallophosphoesterase_nuclease",
        lambda c, row: c["metal"]
        and _ec_has_prefix(row, _METALLOPHOSPHOESTERASE_NUCLEASE_EC),
    ),
    (
        "metallophosphomonoesterase",
        lambda c, row: c["metal"] and _ec_has_prefix(row, _METALLOPHOSPHOMONOESTERASE_EC),
    ),
    (
        "metallo_amidohydrolase_deaminase",
        lambda c, row: c["metal"]
        and _ec_has_prefix(row, _METALLO_AMIDOHYDROLASE_DEAMINASE_EC),
    ),
    (
        "flavin_monooxygenase",
        lambda c, row: c["flavin"]
        and not c["heme"]
        and _ec_has_prefix(row, ("1.14.13", "1.14.14")),
    ),
    (
        "flavin_dehydrogenase_reductase",
        lambda c, row: c["flavin"]
        and not c["heme"]
        and _ec_has_prefix(row, ("1.3.", "1.6.", "1.8.1")),
    ),
    (
        "cytochrome_p450_monooxygenase",
        lambda c, row: c["heme"]
        and _ec_has_prefix(row, _P450_MONOOXYGENASE_EC)
        and not _ec_has_prefix(row, ("1.11.1",))
        and not c["peroxide_reaction"]
        and (
            c["keyword_p450"]
            or c["heme_thiolate_binding"]
            or (c["keyword_monooxygenase"] and c["oxygenase_reaction"])
        ),
    ),
    (
        "non_heme_iron_2og_dioxygenase",
        lambda c, row: c["metal"]
        and not c["heme"]
        and not c["flavin"]
        and not c["peroxide_reaction"]
        and _ec_has_prefix(row, _NON_HEME_IRON_2OG_EC)
        and (c["two_og_reaction"] or c["keyword_dioxygenase"])
    ),
    (
        "radical_sam_enzyme",
        lambda c, row: c["cx3cx2c_motif"] or (c["fe_s"] and c["sam"]),
    ),
    (
        "cobalamin_radical_rearrangement",
        lambda c, row: c["cobalamin"]
        and _ec_has_prefix(row, ("5.4.99", "5.4.3", "4.2.1.28", "4.2.1.30", "4.3.1.7")),
    ),
    # Broadened-handle families: the corroborator is a COSUBSTRATE / functional keyword, not a
    # cofactor comment. NAD(P) is read as a Rhea reaction participant or NAD/NADP keyword;
    # the sugar-nucleotide donor as a Rhea participant or the Glycosyltransferase keyword.
    # EC 1.1.1 / 2.4 select the lane only (scope, never predictive).
    (
        "nad_p_dehydrogenase",
        lambda c, row: c["cosubstrate_nad_p"]
        and _ec_has_prefix(row, _NAD_P_DEHYDROGENASE_EC),
    ),
    (
        "glycosyltransferase",
        lambda c, row: (c["sugar_nucleotide_donor"] or c["keyword_glycosyltransferase"])
        and _ec_has_prefix(row, _GLYCOSYLTRANSFERASE_EC),
    ),
    (
        "sam_methyltransferase",
        lambda c, row: (c["sam_sah_methyl_donor"] or c["keyword_methyltransferase"])
        and not c["fe_s"]
        and not c["cx3cx2c_motif"]
        and _ec_has_prefix(row, _SAM_METHYLTRANSFERASE_EC),
    ),
    (
        "coa_acyltransferase",
        lambda c, row: _ec_has_prefix(row, _COA_ACYLTRANSFERASE_EC)
        and not c["hydrolase_side_ec"]
        and c["keyword_acyltransferase"]
        and (
            c["coa_acyl_coa_reaction"]
            or c["coa_acyl_coa_feature"]
            or c["active_or_binding_site_present"]
        ),
    ),
    (
        "cofactor_independent_isomerase",
        lambda c, row: _ec_has_prefix(row, _COFACTOR_INDEPENDENT_ISOMERASE_EC)
        and not c["non_5_3_side_ec"]
        and c["keyword_isomerase"]
        and (c["isomerization_reaction"] or c["active_or_binding_site_present"]),
    ),
    (
        "molybdopterin_oxidoreductase",
        lambda c, row: _ec_has_prefix(row, _MOLYBDOPTERIN_OXIDOREDUCTASE_EC)
        and c["molybdopterin_moco"]
        and not c["hydrolase_side_ec"]
        and not c["non_oxidoreductase_side_ec"]
        and not c["peroxide_reaction"]
        and not c["molybdopterin_biosynthesis_boundary"]
        and (
            c["molybdopterin_redox_reaction"]
            or c["molybdopterin_oxo_transfer_reaction"]
            or c["molybdopterin_feature_or_ligand"]
            or c["keyword_molybdenum"]
            or c["active_or_binding_site_present"]
        ),
    ),
    (
        "copper_oxidoreductase",
        lambda c, row: _ec_has_prefix(row, _COPPER_OXIDOREDUCTASE_EC)
        and c["keyword_copper"]
        and not c["copper_boundary_heme_flavin_molybdopterin"]
        and not c["hydrolase_side_ec"]
        and not c["non_oxidoreductase_side_ec"]
        and (
            c["copper_feature_or_ligand"]
            or c["copper_redox_reaction"]
            or c["copper_oxidase_reaction"]
            or c["active_or_binding_site_present"]
        ),
    ),
    (
        "metal_racemase_epimerase_non_plp",
        lambda c, row: _ec_has_prefix(row, _METAL_RACEMASE_EPIMERASE_NON_PLP_EC)
        and c["keyword_isomerase"]
        and c["racemase_epimerase_text"]
        and not c["plp_boundary_signal"]
        and not c["non_5_1_side_ec"]
        and not c["transferase_side_ec"]
        and not c["hydrolase_side_ec"]
        and not c["oxidoreductase_side_ec"]
        and (c["isomerization_reaction"] or c["active_or_binding_site_present"])
        and (
            c["active_or_binding_site_present"]
            or c["metal"]
            or c["cofactorless_context"]
        ),
    ),
    (
        "atp_amide_ligase",
        lambda c, row: _ec_has_prefix(row, _ATP_AMIDE_LIGASE_EC)
        and c["keyword_ligase"]
        and (c["atp_ligase_atp_or_adp_phosphate"] or c["atp_ligase_mg_context"])
        and (
            c["atp_amide_ligation_text"]
            or c["atp_acyl_phosphate_intermediate"]
            or c["active_or_binding_site_present"]
        )
        and not c["biotin_carboxylase_boundary"]
        and not c["kinase_boundary"]
        and not c["hydrolase_side_ec"]
        and not c["transferase_side_ec"]
        and not c["non_6_3_side_ec"],
    ),
    (
        "class_ii_metal_aldolase",
        lambda c, row: _ec_has_prefix(row, _CLASS_II_METAL_ALDOLASE_EC)
        and c["metal"]
        and c["keyword_lyase"]
        and c["keyword_ligase"] is False
        and c["keyword_isomerase"] is False
        and not c["plp_boundary_signal"]
        and not c["thdp_boundary_signal"]
        and not c["schiff_class_i_boundary_signal"]
        and not c["hydrolase_side_ec"]
        and not c["transferase_side_ec"]
        and not c["oxidoreductase_side_ec"]
        and not c["non_4_1_2_or_4_1_3_side_ec"]
        and (
            c["class_ii_metal_aldolase_text"]
            or c["class_ii_aldolase_cc_reaction"]
            or c["active_or_binding_site_present"]
        ),
    ),
    (
        "thiamine_diphosphate_enzyme",
        lambda c, row: _ec_has_prefix(row, _THIAMINE_DIPHOSPHATE_ENZYME_EC)
        and c["thdp"]
        and (c["thdp_mg_context"] or c["active_or_binding_site_present"])
        and not c["plp_boundary_signal"]
        and not c["molybdopterin_moco"]
        and not c["flavin"]
        and not c["heme"]
        and not c["thdp_kinase_hydrolase_boundary"]
        and not c["hydrolase_side_ec"]
        and not c["non_thdp_scope_side_ec"]
        and (
            c["thdp_reaction_context"]
            or c["thdp_family_text"]
            or c["active_or_binding_site_present"]
        ),
    ),
    (
        "zinc_lyase_hydratase",
        lambda c, row: _ec_has_prefix(row, _ZINC_LYASE_HYDRATASE_EC)
        and c["zinc_feature_or_ligand"]
        and c["zinc_lyase_hydratase_text"]
        and not c["plp_boundary_signal"]
        and not c["thdp_boundary_signal"]
        and not c["hydrolase_side_ec"]
        and not c["transferase_side_ec"]
        and not c["keyword_isomerase"]
        and not c["zinc_lyase_boundary_text"]
        and not c["non_4_2_1_side_ec"]
        and (
            c["zinc_hydration_elimination_reaction"]
            or c["active_or_binding_site_present"]
        ),
    ),
)


def disambiguate_row(row: dict[str, Any]) -> dict[str, Any]:
    """Assign a fingerprint only when exactly one rule fires (else stay held).

    Scope is selected by the EC-prefix predicate; membership is CONFIRMED by a mechanism
    corroborator (cofactor OR cosubstrate/Rhea participant OR functional keyword OR
    active-site/binding residue). The trust-tier N-of-M rule
    (`source_trust_tiers.evaluate_corroboration`, source_tier_0) must ADMIT -- i.e. at least
    one counted MECHANISM axis is present -- before the row can be built into a label. EC is
    a scope hint and never counts toward N-of-M.
    """
    evidence = mechanism_corroborator_axes(row)
    matched = [fp for fp, rule in DISAMBIGUATION_RULES if rule(evidence, row)]
    distinct = sorted(set(matched))
    if not distinct:
        return {"decision": "hold", "reason": "no_mechanism_corroboration"}
    if len(distinct) > 1:
        return {
            "decision": "hold",
            "reason": "multi_fingerprint_signal_conflict",
            "candidates": distinct,
        }
    present_axes = corroborator_axes_present(evidence, row)
    corroboration = evaluate_corroboration(
        source_tier="source_tier_0", present_axes=present_axes
    )
    if not str(corroboration["decision"]).startswith("admit"):
        return {
            "decision": "hold",
            "reason": "trust_tier_corroboration_insufficient",
            "candidates": distinct,
            "present_axes": present_axes,
            "corroboration": corroboration,
        }
    return {
        "decision": "import",
        "fingerprint_id": distinct[0],
        "cofactor_evidence": evidence,
        "present_axes": present_axes,
        "corroboration": corroboration,
    }


def _synthesize_cofactor_provenance(
    row: dict[str, Any], fingerprint: str, evidence: dict[str, bool]
) -> list[dict[str, Any]]:
    """Surface a synthesized cofactor record when the row carries none.

    Honest provenance: the cofactor was read from reviewed family-flag / residue
    ligand evidence; each record is tagged with that derivation.
    """
    existing = row.get("cofactor_provenance") or []
    if existing:
        return list(existing)
    tag = "derived_from_reviewed_cofactor_family_flags_and_residue_ligands"
    records: list[dict[str, Any]] = []
    if fingerprint == "radical_sam_enzyme":
        records = [
            {"name": "[4Fe-4S] cluster", "cross_reference": {"id": _FE4S4_CHEBI}},
            {"name": "S-adenosyl-L-methionine", "cross_reference": {"id": _SAM_CHEBI}},
        ]
    elif fingerprint == "cobalamin_radical_rearrangement":
        records = [{"name": "adenosylcobalamin", "cross_reference": {"id": _ADOCBL_CHEBI}}]
    elif evidence.get("heme"):
        records = [{"name": "heme", "cross_reference": {"id": None}}]
    elif evidence.get("flavin"):
        records = [{"name": "FAD", "cross_reference": {"id": None}}]
    elif fingerprint == "copper_oxidoreductase" and evidence.get("copper_feature_or_ligand"):
        records = [{"name": "copper", "cross_reference": {"id": None}}]
    elif fingerprint == "thiamine_diphosphate_enzyme" and evidence.get("thdp"):
        records = [{"name": "thiamine diphosphate", "cross_reference": {"id": None}}]
    elif fingerprint == "zinc_lyase_hydratase" and evidence.get("zinc_feature_or_ligand"):
        records = [{"name": "zinc", "cross_reference": {"id": None}}]
    elif evidence.get("metal"):
        records = [{"name": "catalytic divalent metal", "cross_reference": {"id": None}}]
    for record in records:
        record["evidence_codes"] = []
        record["provenance"] = tag
    return records


def _normalize_row(
    row: dict[str, Any], *, fingerprint: str, evidence: dict[str, bool], index
) -> dict[str, Any]:
    normalized = dict(row)
    screen = rerun_current702_duplicate_screen(row, index=index)
    normalized["duplicate_current_registry_conflict_status"] = screen[
        "duplicate_current_registry_conflict_status"
    ]
    normalized["cofactor_provenance"] = _synthesize_cofactor_provenance(
        row, fingerprint, evidence
    )
    return normalized


def _build_decision(
    row: dict[str, Any], fingerprint: str
) -> dict[str, Any]:
    classes = sorted(cofactor_classes(row))
    ec = _ec_numbers(row)
    return {
        "decision": "import",
        "label_type": "seed_fingerprint",
        "fingerprint_id": fingerprint,
        "reason": (
            f"cofactor_ec_disambiguation_to_{fingerprint}_"
            f"from_annotated_cofactor_and_ec_class_{ec or 'n/a'}"
        ),
        "cofactor_classes": classes,
    }


def build_cofactor_ec_disambiguation(
    *,
    pools: list[dict[str, Any]],
    registry: list[dict[str, Any]],
    index,
) -> dict[str, Any]:
    existing_entry_ids = {str(label.get("entry_id")) for label in registry}
    seen_accessions: set[str] = set()

    new_labels: list[dict[str, Any]] = []
    holds: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []

    decision_counts: Counter[str] = Counter()
    fingerprint_counts: Counter[str] = Counter()
    confidence_counts: Counter[str] = Counter()
    hold_reasons: Counter[str] = Counter()
    per_pool: dict[str, Counter[str]] = {}
    lane_scope: dict[str, Counter[str]] = {}

    total_rows = 0
    for spec in pools:
        pool = str(spec["pool"])
        source_artifact = Path(str(spec["path"])).stem
        per_pool.setdefault(pool, Counter())
        for raw in spec["rows"]:
            total_rows += 1
            verdict = disambiguate_row(raw)
            if verdict["decision"] == "hold":
                decision_counts["hold"] += 1
                per_pool[pool]["hold"] += 1
                hold_reasons[verdict["reason"]] += 1
                holds.append(
                    {
                        "accession": _clean_accession(raw.get("accession")),
                        "pool": pool,
                        "lane": raw.get("target_family_lane"),
                        "reason": verdict["reason"],
                        "candidates": verdict.get("candidates"),
                    }
                )
                continue

            fingerprint = verdict["fingerprint_id"]
            row = _normalize_row(
                raw, fingerprint=fingerprint, evidence=verdict["cofactor_evidence"], index=index
            )
            if not str(
                row.get("duplicate_current_registry_conflict_status") or ""
            ).startswith("no_exact"):
                decision_counts["skip"] += 1
                per_pool[pool]["skip_screen"] += 1
                skips.append(
                    {
                        "accession": _clean_accession(raw.get("accession")),
                        "pool": pool,
                        "reason": "current702_duplicate_screen_not_confirmed",
                    }
                )
                continue

            accession = _clean_accession(row.get("accession"))
            entry_id = f"uniprot:{accession}"
            if entry_id in existing_entry_ids or accession in seen_accessions:
                decision_counts["skip"] += 1
                per_pool[pool]["skip_duplicate"] += 1
                skips.append(
                    {
                        "accession": accession,
                        "pool": pool,
                        "reason": "duplicate_entry_id_in_registry_or_batch",
                    }
                )
                continue
            seen_accessions.add(accession)

            decision = _build_decision(row, fingerprint)
            label = _build_label(row, decision)
            evidence = label["evidence"]
            evidence["sources"] = ["external_cofactor_ec_disambiguation"]
            evidence.setdefault("source_provenance", {})["disambiguation_pool"] = pool
            evidence["source_provenance"]["disambiguation_source_artifact"] = source_artifact
            evidence.setdefault("import_gate_evidence", []).append(
                "mechanism_corroborator_ec_disambiguation_unique_fingerprint_match"
            )
            # Record the broadened mechanism corroboration as SCOPE/admission evidence only --
            # the counted axes (cofactor/cosubstrate, Rhea participant, active-site, domain) and
            # the non-counted EC scope hint. This is excluded_context, never a predictive feature.
            present_axes = verdict.get("present_axes") or []
            corroboration = verdict.get("corroboration") or {}
            evidence["source_trust_tier"] = {
                "source_tier": "source_tier_0",
                "mechanism_corroborator_axes_present": corroboration.get(
                    "distinct_corroborator_axes", []
                ),
                "ec_scope_hint_axes_not_counted": corroboration.get(
                    "scope_hint_axes_present_not_counted", []
                ),
                "meets_n_of_m": corroboration.get("meets_n_of_m"),
                "present_axes": present_axes,
            }
            for axis in corroboration.get("distinct_corroborator_axes", []):
                evidence["import_gate_evidence"].append(f"mechanism_axis:{axis}")
            evidence.setdefault("notes", []).append(
                "mechanism-corroborator/EC disambiguation of a previously-held or freshly "
                f"sourced row: {pool}; membership confirmed by mechanism evidence "
                f"({', '.join(corroboration.get('distinct_corroborator_axes', [])) or 'n/a'}); "
                "EC class used for scope assignment only (review-only; never a predictive feature)"
            )
            new_labels.append(label)
            decision_counts["import"] += 1
            per_pool[pool]["import"] += 1
            fingerprint_counts[fingerprint] += 1
            confidence_counts[label["confidence"]] += 1
            lane = str(raw.get("target_family_lane"))
            lane_scope.setdefault(lane, Counter())[fingerprint] += 1

    current_total = len(registry)
    imported = len(new_labels)
    return {
        "artifact_id": (
            "v3_external_cofactor_ec_disambiguation_preview_current702_20260609"
        ),
        "schema_version": "external_annotation_anchored_import.v1",
        "created_utc": _utc_now_iso(),
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
        "disambiguation_basis": (
            "previously-held cofactor-confounded redox and secondary-probe "
            "radical-SAM/cobalamin rows made countable by corroborating the "
            "annotated cofactor identity against the reviewed reaction/EC class; "
            "only unique single-fingerprint matches are imported, multi-signal "
            "rows stay held; EC is used for scope assignment only and remains a "
            "review-only, non-predictive feature"
        ),
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_or_prose": False,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "ec_name_prose_excluded_context_on_every_label": True,
            "all_new_labels_tier": "bronze",
            "all_new_labels_review_status": "automation_curated",
            "external_entry_id_namespace": "uniprot",
            "heldout_benchmark_unchanged": True,
            "current702_accession_sequence_duplicate_screen_required": True,
            "multi_fingerprint_signal_rows_held": True,
            "structure_geometry_confirmation_is_deferred_promotion_signal": True,
        },
        "counts": {
            "examined_rows": total_rows,
            "decision_counts": dict(decision_counts),
            "per_pool_decision_counts": {
                pool: dict(counter) for pool, counter in sorted(per_pool.items())
            },
            "importable_new_labels": imported,
            "fingerprint_counts": dict(sorted(fingerprint_counts.items())),
            "confidence_counts": dict(confidence_counts),
            "hold_count": len(holds),
            "hold_reason_counts": dict(hold_reasons),
            "skip_count": len(skips),
            "current_registry_labels": current_total,
            "projected_registry_labels_if_merged": current_total + imported,
        },
        "diversity_by_lane": {
            lane: dict(counter) for lane, counter in sorted(lane_scope.items())
        },
        "next_action": (
            "On explicit authorization, append `applied_labels` to the SEPARATE "
            "expansion registry `data/registries/external_bronze_labels.json` via "
            "`apply-external-annotation-anchored-import`. Rows still held "
            "(no/ambiguous cofactor-EC corroboration) remain a review queue."
        ),
        "applied_labels": new_labels,
        "holds_sample": holds[:50],
        "skips_sample": skips[:50],
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Cofactor/EC Disambiguation Of Held Redox + Radical-SAM/Cobalamin Lanes",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Makes a high-precision subset of the previously-HELD cofactor-confounded",
        "redox and secondary-probe radical-SAM/cobalamin rows countable, by",
        "corroborating the annotated cofactor against the reviewed reaction/EC",
        "class. Only unique single-fingerprint matches are imported; multi-signal",
        "rows stay held. EC is used for scope assignment only and is never a",
        "predictive feature. The frozen current702 benchmark is NOT written.",
        "",
        "## Result",
        "",
        f"- Held rows examined: {c['examined_rows']}.",
        f"- **Disambiguated bronze labels: {c['importable_new_labels']}** "
        f"-> expansion registry {c['current_registry_labels']} -> "
        f"**{c['projected_registry_labels_if_merged']}** if merged.",
        f"- Fingerprints recovered: {c['fingerprint_counts']}.",
        f"- Confidence: {c['confidence_counts']}.",
        f"- Still held: {c['hold_count']} ({c['hold_reason_counts']}).",
        f"- Skipped: {c['skip_count']}.",
        "",
        "## Per-pool decisions",
        "",
        "| Pool | decisions |",
        "| --- | --- |",
    ]
    for pool, counter in c["per_pool_decision_counts"].items():
        lines.append(f"| {pool} | {counter} |")
    lines.extend(
        [
            "",
            "## Diversity by lane (recovered fingerprint)",
            "",
            "| Lane | recovered |",
            "| --- | --- |",
        ]
    )
    for lane, counter in audit["diversity_by_lane"].items():
        lines.append(f"| {lane} | {counter} |")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Curated registry written: "
            f"{audit['guardrails']['curated_registry_written']}.",
            "- EC used for scope assignment only, never predictive: "
            f"{audit['guardrails']['ec_used_for_scope_assignment_only_never_predictive']}.",
            "- Multi-fingerprint-signal rows held: "
            f"{audit['guardrails']['multi_fingerprint_signal_rows_held']}.",
            "- All new labels bronze / automation_curated; uniprot namespace; "
            "heldout benchmark unchanged.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def load_disambiguation_pools(
    specs: tuple[dict[str, Any], ...] = DISAMBIGUATION_POOLS,
) -> list[dict[str, Any]]:
    loaded: list[dict[str, Any]] = []
    for spec in specs:
        rows = _preview_rows(_load_json(Path(spec["path"])))
        if spec.get("only_unscreened"):
            rows = [
                row
                for row in rows
                if not str(
                    row.get("duplicate_current_registry_conflict_status") or ""
                ).startswith("no_exact")
            ]
        lanes = spec.get("lanes")
        if lanes:
            allowed = set(lanes)
            rows = [row for row in rows if row.get("target_family_lane") in allowed]
        loaded.append({**spec, "rows": rows})
    return loaded


def write_cofactor_ec_disambiguation(
    *,
    out_path: Path,
    report_path: Path | None = None,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    specs: tuple[dict[str, Any], ...] = DISAMBIGUATION_POOLS,
) -> dict[str, Any]:
    frozen = _load_json(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    index = build_current702_reference_index(
        current_manifest_payload=_load_json(current_manifest_path),
        frozen_benchmark_payload=frozen,
        expansion_payload=expansion,
    )
    audit = build_cofactor_ec_disambiguation(
        pools=load_disambiguation_pools(specs),
        registry=expansion,
        index=index,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
