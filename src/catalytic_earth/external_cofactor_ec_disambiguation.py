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


def _ec_has_exact(row: dict[str, Any], exact: tuple[str, ...]) -> bool:
    return any(ec in exact for ec in _ec_numbers(row))


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
        "biotin": any_name("biotin", "biocytin", "biotinyl")
        or bool(flags.get("biotin_or_biocytin_evidence_present")),
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
# Glycoside hydrolase handles. EC 3.2.1 selects scope only; counted mechanism
# corroboration comes from reviewed glycosidic hydrolysis reaction text,
# glycosidase family/domain text, and active-site acid/base or nucleophile
# residue annotations. Glycosyltransferase, transglycosylase, phosphorylase,
# lyase/isomerase, and side-EC boundary rows stay held.
_GLYCOSIDE_HYDROLASE_FAMILY_TOKENS = (
    "glycosidase",
    "glycoside hydrolase",
    "glycosyl hydrolase",
    "glucosidase",
    "galactosidase",
    "mannosidase",
    "xylanase",
    "cellulase",
    "amylase",
    "chitinase",
    "beta-glucanase",
)
_GLYCOSIDE_HYDROLYSIS_REACTION_TOKENS = (
    "h2o",
    "h(2)o",
    "water",
    "hydrolysis",
    "glycoside",
    "glycosidic",
    "oligosaccharide",
    "polysaccharide",
)
_GLYCOSIDE_HYDROLASE_ACTIVE_SITE_TOKENS = (
    "proton donor",
    "nucleophile",
    "acid/base",
    "general acid",
    "general base",
    "glutamate",
    "aspartate",
)
_GLYCOSIDE_HYDROLASE_BOUNDARY_TOKENS = (
    "glycosyltransferase",
    "transferase",
    "transglycosylase",
    "phosphorylase",
    "lyase",
    "isomerase",
    "mutase",
    "esterase",
    "peptidase",
    "nuclease",
)
# N-ribosyl / nucleoside hydrolase handles. EC 3.2.2 scopes N-glycosylase
# candidates only; counted corroboration comes from nucleoside hydrolase family
# text, N-glycosidic bond hydrolysis reaction text, and optional active-/binding-
# site evidence. O-glycosidases, phosphorylases, kinases, transferases, lyases,
# and EC-only rows stay held.
_N_RIBOSYL_HYDROLASE_FAMILY_TOKENS = (
    "nucleoside hydrolase",
    "n-ribosylhydrolase",
    "n-ribosidase",
    "nucleosidase",
    "uridine nucleosidase",
    "purine nucleosidase",
    "n-ribohydrolase",
    "nucleoside n-ribohydrolase",
    "ribosyl hydrolase",
    "ribohydrolase",
)
_N_RIBOSYL_HYDROLYSIS_REACTION_TOKENS = (
    "h2o",
    "h(2)o",
    "water",
    "hydrolysis",
    "d-ribose",
    "ribose",
    "deoxyribose",
)
_N_RIBOSYL_BASE_PRODUCT_TOKENS = (
    "adenine",
    "guanine",
    "hypoxanthine",
    "xanthine",
    "uracil",
    "thymine",
    "cytosine",
    "purine",
    "pyrimidine",
)
_N_RIBOSYL_ACTIVE_SITE_TOKENS = (
    "acid/base",
    "general acid",
    "general base",
    "aspartate",
    "aspartic",
    "glutamate",
    "glutamic",
    "ribose binding",
    "base binding",
)
_N_RIBOSYL_BOUNDARY_TOKENS = (
    "glycosidase",
    "glycoside hydrolase",
    "glycosyl hydrolase",
    "glycosyltransferase",
    "transferase",
    "phosphorylase",
    "phosphorolysis",
    "kinase",
    "nucleotidyltransferase",
    "dna glycosylase",
    "lyase",
)
# Metal-independent phosphodiesterase handles. EC 3.1.4 / 4.6.1 scopes
# phosphodiester/cyclic-nucleotide candidates only; counted corroboration comes
# from phosphodiesterase family text, hydrolytic phosphodiester/cyclic-nucleotide
# reaction text, and optional active-/binding-site evidence. Catalytic metal rows
# are owned by the existing metallophosphoesterase/nuclease wall; phosphatases,
# cyclases/lyases without hydrolysis, kinases, transferases, and EC-only rows stay
# held.
_METAL_INDEPENDENT_PDE_FAMILY_TOKENS = (
    "phosphodiesterase",
    "cyclic nucleotide phosphodiesterase",
    "cyclic-nucleotide phosphodiesterase",
    "phospholipase d",
)
_METAL_INDEPENDENT_PDE_REACTION_TOKENS = (
    "phosphodiester",
    "cyclic nucleotide",
    "cyclic-nucleotide",
    "cyclic amp",
    "cyclic gmp",
    "camp",
    "cgmp",
    "phosphatidylcholine",
    "phosphatidate",
    "phosphocholine",
    "phosphoethanolamide",
    "glycosylinositol",
    "glycero-3-phosphate",
)
_METAL_INDEPENDENT_PDE_HYDROLYSIS_TOKENS = (
    "h2o",
    "h(2)o",
    "water",
    "hydrolysis",
)
_METAL_INDEPENDENT_PDE_ACTIVE_SITE_TOKENS = (
    "acid/base",
    "general acid",
    "general base",
    "histidine",
    "lysine",
    "tyrosine",
    "arginine",
    "substrate binding",
)
_METAL_INDEPENDENT_PDE_BOUNDARY_TOKENS = (
    "phosphatase",
    "phosphomonoesterase",
    "protein phosphatase",
    "nuclease",
    "ribonuclease",
    "deoxyribonuclease",
    "phospholipase c",
    "adenylate cyclase",
    "guanylate cyclase",
    "lyase",
    "kinase",
    "transferase",
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
# Mn/Fe superoxide dismutase handles. EC 1.15.1.1 scopes the reviewed supply only;
# counted mechanism corroboration comes from superoxide dismutation Rhea text,
# Mn/Fe metal or metal-site evidence, SOD keyword/domain text, and
# active-/binding-/metal-site evidence. Protein-name tokens are used only as
# scope/admission context and are not counted as a domain/family axis.
_SOD_FAMILY_TEXT_TOKENS = (
    "superoxide dismutase",
    "manganese superoxide dismutase",
    "iron superoxide dismutase",
    "mnsod",
    "fesod",
)
_SOD_REACTION_TOKENS = ("superoxide",)
_SOD_PRODUCT_TOKENS = (
    "h2o2",
    "hydrogen peroxide",
    "o2",
    "o(2)",
    "dioxygen",
)
_MN_FE_SOD_METAL_TOKENS = (
    "manganese",
    "mn(",
    "mn2",
    "mn(2",
    "iron",
    "fe(",
    "fe2",
    "fe3",
)
_MN_FE_SOD_BOUNDARY_TOKENS = (
    "cu-zn",
    "cu/zinc",
    "cu/zn",
    "cuzn",
    "copper-zinc",
    "copper/zinc",
    "copper",
    "zinc",
    "superoxide reductase",
    "hemoglobin",
    "haemoglobin",
    "cytoglobin",
    "myoglobin",
    "peroxidase",
    "nitrite",
    "nitric oxide",
    "nitric-oxide",
    "dioxygenase",
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
# Ser/Thr/Tyr protein kinase handles. EC 2.7.10/2.7.11 scopes candidates only;
# counted corroboration comes from protein-kinase family text, ATP/ADP/Mg
# participant or binding-site context, protein-substrate phosphorylation reaction
# text, and active-/binding-site evidence. Histidine kinases, small-molecule
# kinases, ATP ligases, hydrolases, and side-EC rows stay held.
_PROTEIN_KINASE_FAMILY_TEXT_TOKENS = (
    "protein kinase",
    "serine/threonine-protein kinase",
    "serine/threonine kinase",
    "tyrosine-protein kinase",
    "tyrosine kinase",
    "dual specificity protein kinase",
    "dual-specificity protein kinase",
)
_PROTEIN_KINASE_ATP_MG_TOKENS = (
    "atp",
    "adenosine 5'-triphosphate",
    "adenosine triphosphate",
    "adp",
    "adenosine 5'-diphosphate",
    "magnesium",
    "mg(2",
    "mg2",
)
_PROTEIN_KINASE_REACTION_TOKENS = (
    "protein",
    "phosphoprotein",
    "l-serine",
    "l-threonine",
    "l-tyrosine",
    "o-phospho-l-serine",
    "o-phospho-l-threonine",
    "o4-phospho-l-tyrosine",
    "phosphorylated protein",
)
_PROTEIN_KINASE_BOUNDARY_TOKENS = (
    "histidine kinase",
    "two-component",
    "ribokinase",
    "deoxynucleoside kinase",
    "nucleoside diphosphate kinase",
    "phosphofructokinase",
    "fructokinase",
    "hexokinase",
    "glucokinase",
    "acetate kinase",
    "galactokinase",
    "homoserine kinase",
    "mevalonate kinase",
    "atp-grasp",
    "atp grasp",
    "ligase",
)
# Aminoglycoside phosphotransferase handles. Exact APH EC scopes candidates
# only; counted corroboration comes from APH family/name/domain text,
# ATP/Mg or ADP/phosphate context, aminoglycoside phosphorylation reaction text,
# and active-/binding-site evidence. Protein kinases, histidine kinases,
# generic small-molecule kinases, acetyltransferases, nucleotidyltransferases,
# and EC-only rows stay held.
_AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_FAMILY_TEXT_TOKENS = (
    "aminoglycoside phosphotransferase",
    "aminoglycoside-phosphotransferase",
    "aminoglycoside kinase",
    "aminoglycoside 3'-phosphotransferase",
    "aminoglycoside 6-phosphotransferase",
    "neomycin-kanamycin phosphotransferase",
    "streptomycin kinase",
    "aph(",
    "aph ",
)
_AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_ATP_MG_TOKENS = (
    "atp",
    "adenosine 5'-triphosphate",
    "adenosine triphosphate",
    "adp",
    "adenosine 5'-diphosphate",
    "magnesium",
    "mg(2",
    "mg2",
)
_AMINOGLYCOSIDE_SUBSTRATE_TOKENS = (
    "aminoglycoside",
    "kanamycin",
    "neomycin",
    "streptomycin",
    "gentamicin",
    "amikacin",
    "tobramycin",
    "hygromycin",
    "paromomycin",
    "spectinomycin",
    "ribostamycin",
    "butirosin",
)
_AMINOGLYCOSIDE_PHOSPHORYL_TOKENS = (
    "phospho",
    "phosphate",
    "phosphoryl",
    "o-phospho",
    "-phosphate",
)
_AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_BOUNDARY_TOKENS = (
    "protein kinase",
    "serine/threonine",
    "tyrosine kinase",
    "histidine kinase",
    "two-component",
    "aminoglycoside acetyltransferase",
    "acetyltransferase",
    "aminoglycoside nucleotidyltransferase",
    "nucleotidyltransferase",
    "adenylyltransferase",
    "glycosyltransferase",
    "ribokinase",
    "phosphofructokinase",
    "nucleoside kinase",
    "deoxynucleoside kinase",
)
# Aminoglycoside acetyltransferase (AAC) handles. EC 2.3.1 scopes the acetyltransferase
# candidate supply only; counted corroboration comes from aminoglycoside-acetyltransferase
# family/name text, acetyl-CoA/CoA cosubstrate context, and Rhea/reviewed acetyl-transfer text.
# Generic CoA acyltransferases (no aminoglycoside name) route to coa_acyltransferase; the
# phospho/nucleotidyl aminoglycoside-resistance enzymes are boundary-guarded, and bifunctional
# acetyltransferase-phosphotransferase rows are held by both family boundaries.
_AMINOGLYCOSIDE_ACETYLTRANSFERASE_FAMILY_TEXT_TOKENS = (
    "aminoglycoside acetyltransferase",
    "aminoglycoside n-acetyltransferase",
    "aminoglycoside 3-n-acetyltransferase",
    "aminoglycoside 3-acetyltransferase",
    "aminoglycoside 6'-n-acetyltransferase",
    "aminoglycoside 2'-n-acetyltransferase",
    "gentamicin acetyltransferase",
    "kanamycin acetyltransferase",
    "aac(",
    "aac6",
    "aac3",
)
_AMINOGLYCOSIDE_DRUG_CLASS_TOKENS = (
    "aminoglycoside",
    "gentamicin",
    "kanamycin",
    "tobramycin",
    "amikacin",
    "neomycin",
    "streptomycin",
    "apramycin",
    "netilmicin",
    "sisomicin",
    "ribostamycin",
    "paromomycin",
    "spectinomycin",
)
_AMINOGLYCOSIDE_ACETYLTRANSFERASE_COA_TOKENS = (
    "coenzyme a",
    "acetyl-coa",
    "acetyl coenzyme a",
    "acetyl-coenzyme a",
    "coa(",
    " coa ",
    "coa)",
)
_AMINOGLYCOSIDE_ACETYLTRANSFERASE_BOUNDARY_TOKENS = (
    "aminoglycoside phosphotransferase",
    "aminoglycoside kinase",
    "aminoglycoside 3'-phosphotransferase",
    "aminoglycoside 6-phosphotransferase",
    "aminoglycoside nucleotidyltransferase",
    "aminoglycoside adenylyltransferase",
    "phosphotransferase",
    "nucleotidyltransferase",
    "adenylyltransferase",
)
# HAD-like phosphatase handles. EC 3.1.3 scopes phosphomonoesterase candidates only;
# counted corroboration comes from HAD/haloacid-dehalogenase family text, catalytic
# Asp or Mg binding-site context, and Rhea/reviewed phosphomonoester hydrolysis text.
# Protein phosphatases without HAD/Asp evidence, metal phosphomonoesterases without
# HAD signal, phosphodiesterases/nucleases, kinases, transferases, and EC-only rows stay held.
_HAD_LIKE_PHOSPHATASE_FAMILY_TEXT_TOKENS = (
    "had-like",
    "had family",
    "had superfamily",
    "haloacid dehalogenase",
    "haloacid-dehalogenase",
    "haloacid dehalogenase-like",
    "phosphoserine phosphatase",
    "phosphoglycolate phosphatase",
    "beta-phosphoglucomutase",
)
_HAD_LIKE_PHOSPHATASE_ASP_MG_TOKENS = (
    "aspartate",
    "asp",
    "phosphoaspartate",
    "phospho-aspartate",
    "magnesium",
    "mg(2",
    "mg2",
    "mg cation",
    "dxd",
    "dxt",
    "dxdt",
)
_HAD_LIKE_PHOSPHATASE_REACTION_TOKENS = (
    "phosphomonoester",
    "phosphatase",
    "phosphoserine",
    "phosphoglycolate",
    "phosphate",
    "orthophosphate",
)
_HAD_LIKE_PHOSPHATASE_HYDROLYSIS_TOKENS = ("h2o", "h(2)o", "water")
_HAD_LIKE_PHOSPHATASE_BOUNDARY_TOKENS = (
    "protein phosphatase",
    "serine/threonine-protein phosphatase",
    "tyrosine-protein phosphatase",
    "protein-tyrosine phosphatase",
    "alkaline phosphatase",
    "purple acid phosphatase",
    "phosphodiesterase",
    "nuclease",
    "exonuclease",
    "endonuclease",
    "ribonuclease",
    "deoxyribonuclease",
    "kinase",
    "transferase",
)
# Ser/Thr protein phosphatase handles. EC 3.1.3.16/48 scopes protein-substrate
# dephosphorylation candidates only; counted corroboration comes from protein
# phosphatase family text, catalytic metal/cofactor or metal-binding context, and
# Rhea/reviewed phosphoprotein dephosphorylation text. Cys-based PTP/DSP/PTEN rows,
# HAD-like Asp-phosphatases, small-molecule phosphatases, kinases, transferases,
# phosphodiesterases/nucleases, side-EC rows, and EC-only rows stay held.
_SER_THR_PROTEIN_PHOSPHATASE_FAMILY_TEXT_TOKENS = (
    "protein phosphatase",
    "serine/threonine-protein phosphatase",
    "serine/threonine protein phosphatase",
    "ser/thr protein phosphatase",
    "pp1",
    "pp2a",
    "pp2b",
    "calcineurin",
    "protein phosphatase 1",
    "protein phosphatase 2a",
    "protein phosphatase 2b",
    "protein phosphatase 5",
)
_SER_THR_PROTEIN_PHOSPHATASE_METAL_TOKENS = (
    "manganese",
    "mn(2",
    "mn2",
    "iron",
    "fe(2",
    "fe2",
    "fe(3",
    "fe3",
    "magnesium",
    "mg(2",
    "mg2",
    "metal",
    "dinuclear",
    "bimetal",
    "binuclear",
)
_SER_THR_PROTEIN_PHOSPHATASE_REACTION_TOKENS = (
    "phosphoprotein",
    "protein phosphate",
    "phosphorylated protein",
    "o-phospho-l-serine",
    "o-phospho-l-seryl",
    "o-phospho-l-threonine",
    "o-phospho-l-threonyl",
    "o4-phospho-l-tyrosine",
    "l-serine",
    "l-seryl",
    "l-threonine",
    "l-threonyl",
    "l-tyrosine",
)
_SER_THR_PROTEIN_PHOSPHATASE_PRODUCT_TOKENS = (
    "protein",
    "phosphate",
    "orthophosphate",
)
_SER_THR_PROTEIN_PHOSPHATASE_HYDROLYSIS_TOKENS = (
    "h2o",
    "h(2)o",
    "water",
    "hydrolysis",
)
_SER_THR_PROTEIN_PHOSPHATASE_BOUNDARY_TOKENS = (
    "had-like",
    "haloacid dehalogenase",
    "phosphoserine phosphatase",
    "phosphoglycolate phosphatase",
    "alkaline phosphatase",
    "purple acid phosphatase",
    "acid phosphatase",
    "phytase",
    "phosphodiesterase",
    "nuclease",
    "exonuclease",
    "endonuclease",
    "ribonuclease",
    "kinase",
    "phosphotransferase",
    "transferase",
    "pten",
    "dual specificity phosphatase",
    "dual-specificity phosphatase",
    "protein-tyrosine phosphatase",
    "tyrosine-protein phosphatase",
    "low molecular weight phosphotyrosine protein phosphatase",
    "cysteine",
    "cys",
    "phosphocysteine",
)
# Aldehyde dehydrogenase handles. EC 1.2.1 scopes reviewed aldehyde-oxidation
# candidates only; counted corroboration comes from ALDH family/domain text, NAD(P)
# participant/binding context, catalytic Cys/Glu active-site evidence, and Rhea/reviewed
# aldehyde-to-acid oxidation text. Molybdopterin aldehyde oxidoreductases, flavin aldehyde
# oxidases, generic NAD(P) dehydrogenases, SDR/AKR/MDR rows, side-EC rows, and EC-only rows stay held.
_ALDEHYDE_DEHYDROGENASE_FAMILY_TEXT_TOKENS = (
    "aldehyde dehydrogenase",
    "aldehyde-dehydrogenase",
    "aldh",
    "aldehyde dehydrogenase family",
    "aldehyde dehydrogenase superfamily",
    "aldedh",
    "aldehyde oxidoreductase dehydrogenase",
)
_ALDEHYDE_DEHYDROGENASE_ACTIVE_SITE_TOKENS = (
    "cysteine",
    "cys",
    "glutamate",
    "glu",
    "catalytic cysteine",
    "catalytic glutamate",
    "active site cysteine",
    "active site glutamate",
)
_ALDEHYDE_DEHYDROGENASE_REACTION_TOKENS = (
    "aldehyde",
    "carboxylate",
    "carboxylic acid",
    "acid",
    "nad(+)",
    "nadp(+)",
    "nadh",
    "nadph",
)
_ALDEHYDE_DEHYDROGENASE_BOUNDARY_TOKENS = (
    "aldehyde oxidase",
    "xanthine dehydrogenase",
    "molybdopterin",
    "molybdenum",
    "flavin",
    "fad",
    "fmn",
    "short-chain dehydrogenase",
    "short chain dehydrogenase",
    "sdr",
    "aldo-keto reductase",
    "aldo keto reductase",
    "akr",
    "medium-chain dehydrogenase",
    "medium chain dehydrogenase",
    "alcohol dehydrogenase",
    "oxidase",
    "monooxygenase",
)
# Short-chain dehydrogenase/reductase handles. EC 1.1.1 scopes the reviewed
# candidate supply only; counted corroboration comes from SDR family/name text,
# NAD(P) cosubstrate/binding context, and Rhea/reviewed NAD(P) hydride-transfer
# reaction text. AKR, MDR/zinc alcohol dehydrogenase, ALDH, flavin/metal redox,
# oxygenase, side-EC, EC-only, and generic NAD(P) rows stay held or routed away.
_SDR_FAMILY_TEXT_TOKENS = (
    "short-chain dehydrogenase",
    "short chain dehydrogenase",
    "short-chain dehydrogenase/reductase",
    "short chain dehydrogenase/reductase",
    "short-chain alcohol dehydrogenase",
    "sdr family",
    "sdr superfamily",
    "sdr ",
)
_SDR_ACTIVE_SITE_TOKENS = (
    "ser-tyr-lys",
    "ser tyr lys",
    "tyr-lys",
    "tyrosine",
    "lysine",
    "serine",
    "asn",
    "asparagine",
    "catalytic tetrad",
)
_SDR_REACTION_TOKENS = (
    "nad(+)",
    "nadp(+)",
    "nadh",
    "nadph",
    "alcohol",
    "hydroxy",
    "hydroxyl",
    "ketone",
    "oxo",
    "dehydrogenase",
    "reductase",
)
_SDR_BOUNDARY_TOKENS = (
    "aldo-keto reductase",
    "aldo keto reductase",
    "aldose reductase",
    "akr",
    "medium-chain dehydrogenase",
    "medium chain dehydrogenase",
    "mdr",
    "zinc-containing alcohol dehydrogenase",
    "zinc alcohol dehydrogenase",
    "alcohol dehydrogenase class",
    "aldehyde dehydrogenase",
    "aldh",
    "aldehyde oxidase",
    "flavin",
    "fad",
    "fmn",
    "molybdopterin",
    "molybdenum",
    "pqq",
    "oxygenase",
    "monooxygenase",
    "oxidase",
)
# Aldo-keto reductase (AKR) handles. EC 1.1.1 scopes the reviewed candidate
# supply only; counted corroboration comes from AKR family/name text, NADP(H)
# cosubstrate/binding context, and Rhea/reviewed NADP carbonyl-reduction text.
# SDR/Rossmann, MDR/zinc alcohol dehydrogenase, ALDH, flavin/metal redox,
# oxygenase, side-EC, EC-only, and generic NAD(P) rows stay held or routed away.
_AKR_FAMILY_TEXT_TOKENS = (
    "aldo-keto reductase",
    "aldo keto reductase",
    "aldose reductase",
    "aldehyde reductase",
    "akr family",
    "akr superfamily",
    "akr1",
    "akr7",
)
_AKR_ACTIVE_SITE_TOKENS = (
    "tyr-lys-his",
    "tyr lys his",
    "catalytic tetrad",
    "tetrad",
    "tyrosine",
    "lysine",
    "histidine",
    "aspartate",
)
_AKR_REACTION_TOKENS = (
    "nadp(+)",
    "nadph",
    "aldehyde",
    "ketone",
    "oxo",
    "carbonyl",
    "alcohol",
    "hydroxy",
    "reductase",
    "reduction",
)
_AKR_BOUNDARY_TOKENS = (
    "short-chain dehydrogenase",
    "short chain dehydrogenase",
    "sdr family",
    "sdr superfamily",
    "rossmann",
    "medium-chain dehydrogenase",
    "medium chain dehydrogenase",
    "mdr",
    "zinc-containing alcohol dehydrogenase",
    "zinc alcohol dehydrogenase",
    "alcohol dehydrogenase class",
    "aldehyde dehydrogenase",
    "aldh",
    "aldehyde oxidase",
    "flavin",
    "fad",
    "fmn",
    "molybdopterin",
    "molybdenum",
    "pqq",
    "oxygenase",
    "monooxygenase",
    "oxidase",
)
# Alpha/beta hydrolase esterase/lipase handles. EC 3.1.1 scopes the candidate
# supply only; counted corroboration comes from esterase/lipase family text,
# Ser-His-Asp/Glu catalytic-site context, and Rhea/reviewed ester hydrolysis.
# Proteases/amidases, glycoside hydrolases/transglycosylases, metal hydrolase
# rows, side-EC rows, EC-only rows, and multi-fingerprint rows stay held.
_ALPHA_BETA_HYDROLASE_FAMILY_TEXT_TOKENS = (
    "alpha/beta hydrolase",
    "alpha beta hydrolase",
    "alpha-beta hydrolase",
    "esterase",
    "lipase",
    "carboxylesterase",
    "cutinase",
    "polyesterase",
    "triacylglycerol lipase",
)
_ALPHA_BETA_HYDROLASE_SERINE_TOKENS = (
    "serine",
    "catalytic ser",
    "ser-his",
    "ser his",
    "serine hydrolase",
    "nucleophile ser",
)
_ALPHA_BETA_HYDROLASE_HISTIDINE_TOKENS = (
    "histidine",
    "catalytic his",
    "ser-his",
    "ser his",
    "his-asp",
    "his-glu",
)
_ALPHA_BETA_HYDROLASE_ACID_TOKENS = (
    "aspartate",
    "aspartic",
    "glutamate",
    "glutamic",
    "catalytic asp",
    "catalytic glu",
    "ser-his-asp",
    "ser-his-glu",
    "his-asp",
    "his-glu",
)
_ALPHA_BETA_HYDROLASE_TRIAD_TOKENS = (
    "catalytic triad",
    "ser-his-asp",
    "ser-his-glu",
    "ser his asp",
    "ser his glu",
    "charge relay",
)
_ALPHA_BETA_HYDROLASE_ESTER_TOKENS = (
    "ester",
    "carboxylic ester",
    "carboxylate ester",
    "acylglycerol",
    "triacylglycerol",
    "triglyceride",
    "lipid",
    "fatty acid",
    "alcohol",
)
_ALPHA_BETA_HYDROLASE_HYDROLYSIS_TOKENS = (
    "h2o",
    "h(2)o",
    "water",
    "hydrolysis",
    "hydrolyzes",
)
_ALPHA_BETA_HYDROLASE_BOUNDARY_TOKENS = (
    "protease",
    "peptidase",
    "proteinase",
    "amidase",
    "amidohydrolase",
    "beta-lactamase",
    "metallo-beta-lactamase",
    "glycosidase",
    "glycoside hydrolase",
    "transglycosylase",
    "glycosyltransferase",
    "nuclease",
    "phosphatase",
    "phosphodiesterase",
    "metallohydrolase",
    "metal-dependent hydrolase",
    "zinc hydrolase",
)
# Serine beta-lactamase handles. EC 3.5.2.6 scopes the candidate supply only;
# counted corroboration comes from serine/class A/C/D beta-lactamase family text,
# beta-lactam hydrolysis reaction text, and active-site Ser/Lys/Glu residue-role
# context. Metallo/zinc beta-lactamases, PBPs/DD-peptidases/transpeptidases,
# beta-lactam synthases, generic amidohydrolases, side-EC rows, EC-only rows, and
# multi-fingerprint rows stay held.
_SERINE_BETA_LACTAMASE_FAMILY_TEXT_TOKENS = (
    "serine beta-lactamase",
    "serine-type beta-lactamase",
    "class a beta-lactamase",
    "class c beta-lactamase",
    "class d beta-lactamase",
    "beta-lactamase class a",
    "beta-lactamase class c",
    "beta-lactamase class d",
    "beta-lactamase",
    "penicillinase",
    "cephalosporinase",
    "oxacillinase",
)
_SERINE_BETA_LACTAMASE_REACTION_TOKENS = (
    "beta-lactam",
    "beta lactam",
    "penicillin",
    "cephalosporin",
    "cephalothin",
    "carbapenem",
    "nitrocefin",
    "imipenem",
    "ampicillin",
    "benzylpenicillin",
)
_SERINE_BETA_LACTAMASE_HYDROLYSIS_TOKENS = (
    "h2o",
    "h(2)o",
    "water",
    "hydrolysis",
    "hydrolyzes",
    "penicilloate",
    "cephalosporoate",
)
_SERINE_BETA_LACTAMASE_ACTIVE_SITE_TOKENS = (
    "active site",
    "serine",
    "catalytic ser",
    "ser-lys",
    "ser lys",
    "lysine",
    "glutamate",
    "glu",
    "carbamylated lys",
    "acyl-enzyme",
    "acyl enzyme",
    "nucleophile",
)
_SERINE_BETA_LACTAMASE_BOUNDARY_TOKENS = (
    "metallo-beta-lactamase",
    "metallo beta-lactamase",
    "metallo-lactamase",
    "zinc beta-lactamase",
    "zinc-dependent beta-lactamase",
    "metal-binding",
    "zinc",
    "zn(2",
    "zn2",
    "penicillin-binding protein",
    "pbp",
    "d-alanyl-d-alanine carboxypeptidase",
    "d-alanyl-d-alanine peptidase",
    "d-alanyl-d-alanine-endopeptidase",
    "dd-peptidase",
    "d,d-peptidase",
    "transpeptidase",
    "carboxypeptidase",
    "endopeptidase",
    "beta-lactam synthase",
    "clavaminate synthase",
    "amidohydrolase",
    "amidase",
    "lactamase-like",
    "resistance protein",
)
# Metallo-beta-lactamase (MBL) handles. EC 3.5.2.6 scopes the candidate supply only
# (shared with serine beta-lactamase); counted corroboration comes from a metallo/zinc
# beta-lactamase family/name OR a catalytic-zinc context, plus a Rhea/reviewed beta-lactam
# hydrolysis reaction. The mechanism is a Zn2+-activated-hydroxide ring hydrolysis (NO Ser
# acyl-enzyme), so serine beta-lactamases (already zinc-excluded) and penicillin-binding
# proteins / DD-peptidases are boundary-guarded.
_METALLO_BETA_LACTAMASE_FAMILY_TEXT_TOKENS = (
    "metallo-beta-lactamase",
    "metallo beta-lactamase",
    "metallo-lactamase",
    "zinc beta-lactamase",
    "zinc-dependent beta-lactamase",
    "zinc metallo-beta-lactamase",
    "class b beta-lactamase",
    "subclass b1",
    "subclass b2",
    "subclass b3",
)
_METALLO_BETA_LACTAMASE_BOUNDARY_TOKENS = (
    "penicillin-binding protein",
    "pbp",
    "d-alanyl-d-alanine carboxypeptidase",
    "d-alanyl-d-alanine peptidase",
    "dd-peptidase",
    "transpeptidase",
    "carboxypeptidase",
    "endopeptidase",
    "beta-lactam synthase",
    "clavaminate synthase",
)
# Peroxiredoxin / thiol(selenol)-based peroxidase handles. EC 1.11.1 scopes the candidate
# supply only (shared with heme peroxidases/catalases); counted corroboration comes from a
# peroxiredoxin / glutathione-peroxidase / thiol-peroxidase family/name OR a peroxidatic
# cysteine/selenocysteine thiol-redox context, plus a Rhea/reviewed peroxide (H2O2 /
# hydroperoxide) reduction reaction. The mechanism is a peroxidatic-thiol/selenol O-O
# reduction (NO heme), so heme peroxidases/catalases, vanadium/non-heme haloperoxidases,
# FAD-dependent NADH peroxidases, manganese catalases, and superoxide dismutases are
# boundary-guarded.
_PEROXIREDOXIN_FAMILY_TEXT_TOKENS = (
    "peroxiredoxin",
    "glutathione peroxidase",
    "thiol peroxidase",
    "thiol-specific antioxidant",
    "thioredoxin peroxidase",
    "thioredoxin-dependent peroxide reductase",
    "thioredoxin-dependent peroxiredoxin",
    "alkyl hydroperoxide reductase",
    "peroxidase ahpc",
    "ahpc",
    "bacterioferritin comigratory protein",
    "prxq",
    "tryparedoxin peroxidase",
)
_PEROXIREDOXIN_THIOL_TOKENS = (
    "peroxidatic cysteine",
    "peroxidatic cys",
    "resolving cysteine",
    "redox-active",
    "redox active",
    "selenocysteine",
    "selenenic",
    "sulfenic",
    "cysteine sulfenic",
)
_PEROXIREDOXIN_REACTION_TOKENS = (
    "peroxide",
    "hydroperoxide",
    "h2o2",
    "hydrogen peroxide",
)
_PEROXIREDOXIN_BOUNDARY_TOKENS = (
    "catalase",
    "heme peroxidase",
    "haem peroxidase",
    "catalase-peroxidase",
    "ascorbate peroxidase",
    "cytochrome c peroxidase",
    "lignin peroxidase",
    "manganese peroxidase",
    "myeloperoxidase",
    "lactoperoxidase",
    "haloperoxidase",
    "chloroperoxidase",
    "bromoperoxidase",
    "vanadium",
    "nadh peroxidase",
    "nadh oxidase",
    "superoxide dismutase",
)
# PAPS-dependent sulfotransferase handles. EC 2.8.2 scopes the candidate supply only
# (and is NOT shared with any existing fingerprint); counted corroboration comes from a
# sulfotransferase family/name plus a Rhea/reviewed sulfuryl-transfer reaction that names
# the PAPS donor / PAP product (3'-phosphoadenylyl sulfate -> adenosine 3',5'-bisphosphate).
# Sulfur-relay sulfurtransferases (rhodanese, cysteine desulfurase, EC 2.8.1), ATP
# sulfurylase / adenylyl-sulfate enzymes, and PAPS reductase are boundary-guarded.
_PAPS_SULFOTRANSFERASE_FAMILY_TEXT_TOKENS = (
    "sulfotransferase",
    "sulphotransferase",
    "sulfokinase",
)
_PAPS_SULFOTRANSFERASE_REACTION_TOKENS = (
    "phosphoadenylyl sulfate",
    "phosphoadenosine 5'-phosphosulfate",
    "3'-phosphoadenosine-5'-phosphosulfate",
    "adenosine 3',5'-bisphosphate",
    "3',5'-bisphosphate",
)
_PAPS_SULFOTRANSFERASE_BOUNDARY_TOKENS = (
    "rhodanese",
    "thiosulfate sulfurtransferase",
    "3-mercaptopyruvate sulfurtransferase",
    "cysteine desulfurase",
    "sulfurtransferase",
    "sulfur carrier",
    "atp sulfurylase",
    "sulfate adenylyltransferase",
    "adenylyl-sulfate",
    "adenylylsulfate",
    "phosphoadenosine phosphosulfate reductase",
    "paps reductase",
)
# Glutathione S-transferase (GST) handles. EC 2.5.1.18 scopes the candidate supply only
# (and is NOT shared with any existing fingerprint); counted corroboration comes from a
# glutathione-transferase family/name plus a Rhea/reviewed reaction that conjugates glutathione
# to an electrophile (-> an S-substituted glutathione). Glutathione peroxidase (EC 1.11.1),
# glutathione reductase (EC 1.8.1.7), glutathione synthetase (EC 6.3.2.3), glutaredoxin, and
# gamma-glutamyltransferase are boundary-guarded.
_GLUTATHIONE_S_TRANSFERASE_FAMILY_TEXT_TOKENS = (
    "glutathione s-transferase",
    "glutathione s transferase",
    "glutathione transferase",
    "s-glutathione transferase",
)
_GLUTATHIONE_S_TRANSFERASE_REACTION_TOKENS = (
    "glutathione",
    "s-substituted glutathione",
    "glutathionyl",
)
_GLUTATHIONE_S_TRANSFERASE_BOUNDARY_TOKENS = (
    "glutathione peroxidase",
    "glutathione reductase",
    "glutathione synthase",
    "glutathione synthetase",
    "glutaredoxin",
    "gamma-glutamyl",
    "thioredoxin",
    "disulfide reductase",
)
# Aminoacyl-tRNA synthetase (aaRS) handles. EC 6.1.1 scopes the candidate supply only (NOT shared
# with any existing fingerprint); counted corroboration comes from an "X--tRNA ligase" / aminoacyl-
# tRNA-synthetase family name plus a Rhea/reviewed aminoacylation reaction that consumes ATP and a
# tRNA and releases AMP + diphosphate. tRNA-modifying enzymes (methyltransferases, pseudouridine
# synthases, CCA-adding / nucleotidyltransferases, amidotransferases) are boundary-guarded; they are
# also off-scope (not EC 6.1.1). NOTE: the ATP-adenylation mechanism is shared with the EC 6.3
# atp_amide_ligase, so aaRS is representation-confusable with it (capped at 150).
_AMINOACYL_TRNA_SYNTHETASE_FAMILY_TEXT_TOKENS = (
    "--trna ligase",
    "trna ligase",
    "trna synthetase",
    "aminoacyl-trna synthetase",
    "aminoacyl trna synthetase",
)
_AMINOACYL_TRNA_SYNTHETASE_REACTION_TOKENS = (
    "trna",
)
_AMINOACYL_TRNA_SYNTHETASE_BOUNDARY_TOKENS = (
    "methyltransferase",
    "pseudouridine",
    "dihydrouridine",
    "amidotransferase",
    "transamidase",
    "deaminase",
    "nucleotidyltransferase",
    "cca-adding",
    "cca trna",
    "trna-modifying",
)
# Biotin-dependent carboxylase handles. EC 6.4.1 / 6.3.4 scopes the reviewed
# candidate supply only; counted corroboration comes from biotin/biotinyl-Lys
# cofactor or modified-residue evidence plus ATP/hydrogencarbonate/carboxybiotin
# carboxylation participant text, carboxylase/biotin-carboxylase family text, or
# active-/binding-site annotations. Kinases, biotin-protein ligases, hydrolases,
# transferase side rows, and non-scope side ECs stay held.
_BIOTIN_FEATURE_TOKENS = (
    "biotin",
    "biocytin",
    "biotinyl",
    "n6-biotinyl-l-lysine",
    "n6-biotinyllysine",
)
_BIOTIN_CARBOXYLASE_TEXT_TOKENS = (
    "biotin carboxylase",
    "biotin-dependent carboxylase",
    "carboxylase",
    "carboxyltransferase",
    "carboxybiotin",
)
_BIOTIN_CARBOXYLATION_CARBON_TOKENS = (
    "hydrogencarbonate",
    "bicarbonate",
    "carbon dioxide",
    "co2",
    "co(2)",
    "carboxybiotin",
    "carboxylated biotin",
)
_BIOTIN_CARBOXYLATION_ATP_TOKENS = (
    "atp",
    "adp",
    "orthophosphate",
    "phosphate",
)
# Nucleoside diphosphate kinase handles. EC 2.7.4.6 scopes the candidate
# supply only; counted corroboration comes from NTP/NDP phosphoryl-transfer Rhea
# text, NDK family text, and active-site/phosphohistidine/binding-site context.
_NDK_FAMILY_TEXT_TOKENS = (
    "nucleoside diphosphate kinase",
    "nucleoside-diphosphate kinase",
    "nucleoside diphosphate phosphotransferase",
    "ndpk",
    "ndp kinase",
)
_NDK_NTP_NDP_REACTION_TOKENS = (
    "atp",
    "adp",
    "gtp",
    "gdp",
    "phosphate",
    "phospho",
    "diphosphate",
    "triphosphate",
)
_NDK_NUCLEOTIDE_CLASS_REACTION_TOKENS = (
    "nucleoside triphosphate",
    "nucleoside diphosphate",
    "nucleoside 5'-triphosphate",
    "nucleoside 5'-diphosphate",
    "ntp",
    "ndp",
    "gtp",
    "gdp",
    "ctp",
    "cdp",
    "utp",
    "udp",
    "itp",
    "idp",
)
_NDK_ACTIVE_HISTIDINE_TOKENS = (
    "phosphohistidine",
    "phospho-l-histidine",
    "pros-phosphohistidine",
    "tele-phosphohistidine",
    "histidine",
)
# ASKHA sugar/acetate kinase handles. EC 2.7.1 scopes reviewed candidates only;
# counted corroboration comes from ATP/ADP/Mg phosphoryl-transfer participant text,
# acetate/glucose/hexose/glycerol kinase family text, and active-/binding-site evidence.
# Neighboring kinase subclasses stay held rather than being merged by generic ATP wording.
_ASKHA_FAMILY_TEXT_TOKENS = (
    "acetate kinase",
    "glucokinase",
    "hexokinase",
    "hexose kinase",
    "glycerol kinase",
)
_ASKHA_PHOSPHORYL_REACTION_TOKENS = (
    "atp",
    "adp",
    "phosphate",
    "phospho",
    "-phosphate",
    "acetyl phosphate",
)
_ASKHA_ATP_MG_TOKENS = (
    "atp",
    "adp",
    "magnesium",
    "mg(2",
    "mg2",
)
_ASKHA_DNK_BOUNDARY_TOKENS = (
    "deoxynucleoside kinase",
    "thymidine kinase",
    "deoxycytidine kinase",
    "deoxyguanosine kinase",
)
_ASKHA_GHMP_BOUNDARY_TOKENS = (
    "homoserine kinase",
    "mevalonate kinase",
    "phosphomevalonate kinase",
    "galactokinase",
)
_ASKHA_PFK_BOUNDARY_TOKENS = (
    "phosphofructokinase",
    "ribokinase",
    "pfka",
    "pfkb",
)
# GHMP superfamily kinase handles. EC 2.7.1 scopes candidates only; counted
# corroboration comes from ATP/ADP phosphoryl-transfer participant text, GHMP-family
# homoserine/mevalonate/phosphomevalonate/galactokinase text, and active-/binding-site evidence.
_GHMP_FAMILY_TEXT_TOKENS = (
    "homoserine kinase",
    "mevalonate kinase",
    "phosphomevalonate kinase",
    "galactokinase",
)
_GHMP_PHOSPHORYL_REACTION_TOKENS = _ASKHA_PHOSPHORYL_REACTION_TOKENS
_GHMP_ATP_MG_TOKENS = _ASKHA_ATP_MG_TOKENS
# Deoxynucleoside kinase handles. EC 2.7.1 scopes candidates only; counted
# corroboration comes from ATP/ADP phosphoryl-transfer participant text,
# deoxynucleoside/thymidine/deoxyguanosine/deoxycytidine family text, and active-/
# binding-site evidence. Neighboring kinase subclasses stay held rather than
# being merged by generic ATP wording.
_DNK_FAMILY_TEXT_TOKENS = (
    "deoxynucleoside kinase",
    "deoxyribonucleoside kinase",
    "thymidine kinase",
    "deoxycytidine kinase",
    "deoxyguanosine kinase",
    "deoxyadenosine kinase",
)
_DNK_PHOSPHORYL_REACTION_TOKENS = (
    "atp",
    "adp",
    "phosphate",
    "phospho",
    "5'-phosphate",
)
_DNK_SUBSTRATE_REACTION_TOKENS = (
    "2'-deoxy",
    "deoxynucleoside",
    "deoxyribonucleoside",
    "thymidine",
    "deoxycytidine",
    "deoxyguanosine",
    "deoxyadenosine",
    "deoxyuridine",
    "dtmp",
    "dcmp",
    "dgmp",
    "damp",
    "dump",
)
_DNK_ATP_MG_TOKENS = _ASKHA_ATP_MG_TOKENS
# PfkA-fold phosphofructokinase handles. EC 2.7.1 scopes candidates only;
# counted corroboration comes from ATP/ADP phosphoryl-transfer participant text
# with fructose-6-phosphate acceptor/product context, PfkA/6-phosphofructokinase
# family text, and active-/binding-site evidence. PfkB/ribokinase and neighboring
# kinase subclasses stay held rather than being merged by generic sugar kinase wording.
_PFKA_FAMILY_TEXT_TOKENS = (
    "6-phosphofructokinase",
    "atp-dependent 6-phosphofructokinase",
    "phosphofructokinase 1",
    "phosphofructokinase i",
    "phosphofructokinase-1",
    "atp-pfk",
    "pfka",
    "pfk-a",
    "phosphohexokinase",
)
_PFKA_PHOSPHORYL_REACTION_TOKENS = _ASKHA_PHOSPHORYL_REACTION_TOKENS
_PFKA_SUBSTRATE_REACTION_TOKENS = (
    "fructose 6-phosphate",
    "fructose-6-phosphate",
    "beta-d-fructose 6-phosphate",
    "d-fructose 6-phosphate",
    "fructose 1,6-bisphosphate",
    "fructose-1,6-bisphosphate",
    "fructose 1,6-diphosphate",
    "fructose-1,6-diphosphate",
)
_PFKA_ATP_MG_TOKENS = _ASKHA_ATP_MG_TOKENS
_PFKB_BOUNDARY_TOKENS = (
    "ribokinase",
    "1-phosphofructokinase",
    "adenosine kinase",
    "inosine kinase",
    "hydroxymethylpyrimidine kinase",
    "pfkb",
    "pfk-b",
)
# PfkB/ribokinase-family handles. EC 2.7.1 scopes candidates only; counted
# corroboration comes from ATP/ADP phosphoryl-transfer participant text with
# ribose/adenosine/inosine/fructose-1-phosphate/PfkB acceptor context,
# PfkB/ribokinase-family text, and active-/binding-site evidence.
_PFKB_FAMILY_TEXT_TOKENS = _PFKB_BOUNDARY_TOKENS
_PFKB_PHOSPHORYL_REACTION_TOKENS = _ASKHA_PHOSPHORYL_REACTION_TOKENS
_PFKB_SUBSTRATE_REACTION_TOKENS = (
    "d-ribose",
    "ribose",
    "ribose 5-phosphate",
    "ribose-5-phosphate",
    "adenosine",
    "adenosine 5'-phosphate",
    "amp",
    "inosine",
    "inosine 5'-phosphate",
    "imp",
    "fructose 1-phosphate",
    "fructose-1-phosphate",
    "d-fructose 1-phosphate",
    "fructose 1,6-bisphosphate",
    "fructose-1,6-bisphosphate",
    "hydroxymethylpyrimidine",
    "4-amino-5-hydroxymethyl-2-methylpyrimidine",
)
_PFKB_ATP_MG_TOKENS = _ASKHA_ATP_MG_TOKENS
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
# Terpene cyclase/synthase handles. EC 4.2.3 scopes terpene cyclase candidates only;
# counted mechanism corroboration comes from terpene/cyclase family text, Mg/Mn or
# diphosphate binding context, and Rhea/reviewed diphosphate-release or terpene product
# participant text. Prenyltransferase chain-extension rows, generic hydratases/lyases,
# and side-EC rows stay held.
_TERPENE_FAMILY_TEXT_TOKENS = (
    "terpene",
    "terpenoid",
    "terpene synthase",
    "terpene cyclase",
    "monoterpene",
    "sesquiterpene",
    "diterpene",
    "triterpene",
    "squalene-hopene cyclase",
    "copalyl diphosphate synthase",
    "cyclase",
)
_TERPENE_DIPHOSPHATE_TOKENS = (
    "diphosphate",
    "pyrophosphate",
    "geranyl diphosphate",
    "farnesyl diphosphate",
    "geranylgeranyl diphosphate",
    "copalyl diphosphate",
    "dimethylallyl diphosphate",
    "isopentenyl diphosphate",
)
_TERPENE_PRODUCT_TOKENS = (
    "terpene",
    "monoterpene",
    "sesquiterpene",
    "diterpene",
    "triterpene",
    "cyclo",
    "ene",
)
_TERPENE_MG_MN_TOKENS = ("magnesium", "mg(2", "mg2", "manganese", "mn(", "mn2", "mn(2")
_TERPENE_BOUNDARY_TOKENS = (
    "prenyltransferase",
    "prenyl transferase",
    "dimethylallyltransferase",
    "geranyltransferase",
    "farnesyltransferase",
    "transferase",
    "hydratase",
    "dehydratase",
    "hydro-lyase",
    "carbonic anhydrase",
    "aldolase",
    "isomerase",
    "hydrolase",
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
        for key in ("description", "ligand_name", "feature_type"):
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
    active_or_binding_site_present = bool(
        _feature_codes(row) & _ACTIVE_OR_BINDING_FEATURE_CODES
    )

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
    glycoside_hydrolase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_GLYCOSIDE_HYDROLASE_FAMILY_TOKENS,
    )
    glycoside_hydrolysis_reaction = in_any(
        reactions, *_GLYCOSIDE_HYDROLYSIS_REACTION_TOKENS
    )
    glycoside_hydrolase_active_site_context = in_any(
        feature_texts, *_GLYCOSIDE_HYDROLASE_ACTIVE_SITE_TOKENS
    )
    glycoside_hydrolase_boundary_signal = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_GLYCOSIDE_HYDROLASE_BOUNDARY_TOKENS,
    )
    non_glycoside_hydrolase_scope_side_ec = any(
        ec and not ec.startswith("3.2.1") for ec in _ec_numbers(row)
    )
    n_ribosyl_hydrolase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_N_RIBOSYL_HYDROLASE_FAMILY_TOKENS,
    )
    n_ribosyl_hydrolysis_reaction = in_any(
        reactions, *_N_RIBOSYL_HYDROLYSIS_REACTION_TOKENS
    ) and in_any(reactions, *_N_RIBOSYL_BASE_PRODUCT_TOKENS)
    n_ribosyl_active_site_context = in_any(
        feature_texts, *_N_RIBOSYL_ACTIVE_SITE_TOKENS
    )
    n_ribosyl_hydrolase_boundary_signal = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_N_RIBOSYL_BOUNDARY_TOKENS,
    )
    non_n_ribosyl_hydrolase_scope_side_ec = any(
        ec and not ec.startswith("3.2.2") for ec in _ec_numbers(row)
    )
    metal_independent_pde_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_METAL_INDEPENDENT_PDE_FAMILY_TOKENS,
    )
    metal_independent_pde_reaction = in_any(
        reactions, *_METAL_INDEPENDENT_PDE_REACTION_TOKENS
    ) and in_any(reactions, *_METAL_INDEPENDENT_PDE_HYDROLYSIS_TOKENS)
    metal_independent_pde_active_site_context = in_any(
        feature_texts, *_METAL_INDEPENDENT_PDE_ACTIVE_SITE_TOKENS
    )
    metal_independent_pde_metal_boundary = bool(evidence.get("metal")) or in_any(
        cofactor_names + feature_texts,
        "magnesium",
        "mg(2",
        "mg2",
        "manganese",
        "mn(2",
        "mn2",
        "zinc",
        "zn(2",
        "zn2",
        "metal",
    )
    metal_independent_pde_boundary_signal = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_METAL_INDEPENDENT_PDE_BOUNDARY_TOKENS,
    )
    non_metal_independent_pde_scope_side_ec = any(
        ec and not (ec.startswith("3.1.4") or ec.startswith("4.6.1"))
        for ec in _ec_numbers(row)
    )
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
    mn_fe_sod_family_text = in_any(keywords + feature_texts, *_SOD_FAMILY_TEXT_TOKENS)
    mn_fe_sod_family_or_name_context = mn_fe_sod_family_text or in_any(
        [protein_name], *_SOD_FAMILY_TEXT_TOKENS
    )
    mn_fe_sod_superoxide_dismutation_reaction = in_any(
        reactions, *_SOD_REACTION_TOKENS
    ) and in_any(reactions, *_SOD_PRODUCT_TOKENS)
    mn_fe_sod_metal_context = in_any(
        cofactor_names + feature_texts, *_MN_FE_SOD_METAL_TOKENS
    )
    mn_fe_sod_boundary_signal = (
        evidence.get("copper", False)
        or evidence.get("zinc", False)
        or evidence.get("heme", False)
        or evidence.get("flavin", False)
        or molybdopterin_moco
        or in_any(
            cofactor_names + feature_texts + keywords + [protein_name],
            *_MN_FE_SOD_BOUNDARY_TOKENS,
        )
    )
    non_mn_fe_sod_scope_side_ec = any(
        ec and ec != "1.15.1.1" for ec in _ec_numbers(row)
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
    biotin_feature_or_ligand = bool(evidence.get("biotin")) or in_any(
        cofactor_names + feature_texts, *_BIOTIN_FEATURE_TOKENS
    )
    biotin_keyword_or_name = in_any(
        keywords + [protein_name], "biotin", "biocytin", "biotinyl"
    )
    biotin_carboxylase_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_BIOTIN_CARBOXYLASE_TEXT_TOKENS,
    )
    biotin_carboxylation_reaction = in_any(
        reactions, *_BIOTIN_CARBOXYLATION_CARBON_TOKENS
    ) and in_any(
        reactions, *_BIOTIN_CARBOXYLATION_ATP_TOKENS
    )
    ndk_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts, *_NDK_FAMILY_TEXT_TOKENS
    )
    ndk_ntp_ndp_reaction = in_any(
        reactions, *_NDK_NTP_NDP_REACTION_TOKENS
    ) and in_any(reactions, *_NDK_NUCLEOTIDE_CLASS_REACTION_TOKENS)
    ndk_active_his_context = in_any(feature_texts, *_NDK_ACTIVE_HISTIDINE_TOKENS)
    ndk_protein_kinase_boundary = _ec_has_prefix(row, ("2.7.11",)) or in_any(
        keywords + [protein_name], "protein kinase"
    )
    ndk_two_component_histidine_kinase_boundary = _ec_has_prefix(
        row, ("2.7.13",)
    ) or in_any(keywords + [protein_name], "histidine kinase")
    ndk_hydrolase_nuclease_side_ec_boundary = _ec_has_prefix(row, ("3.",))
    ndk_other_nmp_kinase_side_ec_boundary = any(
        ec in {"2.7.4.3", "2.7.4.4", "2.7.4.14", "2.7.4.18"}
        for ec in _ec_numbers(row)
    )
    askha_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_ASKHA_FAMILY_TEXT_TOKENS,
    )
    askha_phosphoryl_reaction = in_any(reactions, *_ASKHA_PHOSPHORYL_REACTION_TOKENS)
    askha_atp_mg_context = in_any(
        reactions + cofactor_names + feature_texts, *_ASKHA_ATP_MG_TOKENS
    )
    askha_protein_kinase_boundary = _ec_has_prefix(row, ("2.7.11",)) or in_any(
        keywords + [protein_name], "protein kinase"
    )
    askha_histidine_kinase_boundary = _ec_has_prefix(row, ("2.7.13",)) or in_any(
        keywords + [protein_name], "histidine kinase"
    )
    askha_hydrolase_side_ec_boundary = _ec_has_prefix(row, ("3.",))
    askha_ndk_boundary = _ec_has_prefix(row, ("2.7.4.6",)) or in_any(
        keywords + [protein_name], *_NDK_FAMILY_TEXT_TOKENS
    )
    askha_dnk_boundary = in_any(keywords + [protein_name], *_ASKHA_DNK_BOUNDARY_TOKENS)
    askha_ghmp_boundary = in_any(keywords + [protein_name], *_ASKHA_GHMP_BOUNDARY_TOKENS)
    askha_pfk_boundary = in_any(keywords + [protein_name], *_ASKHA_PFK_BOUNDARY_TOKENS)
    non_askha_scope_side_ec = any(
        ec and not ec.startswith("2.7.1") for ec in _ec_numbers(row)
    )
    ghmp_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_GHMP_FAMILY_TEXT_TOKENS,
    )
    ghmp_phosphoryl_reaction = in_any(reactions, *_GHMP_PHOSPHORYL_REACTION_TOKENS)
    ghmp_atp_mg_context = in_any(
        reactions + cofactor_names + feature_texts, *_GHMP_ATP_MG_TOKENS
    )
    ghmp_protein_kinase_boundary = askha_protein_kinase_boundary
    ghmp_histidine_kinase_boundary = askha_histidine_kinase_boundary
    ghmp_hydrolase_side_ec_boundary = askha_hydrolase_side_ec_boundary
    ghmp_ndk_boundary = askha_ndk_boundary
    ghmp_dnk_boundary = askha_dnk_boundary
    ghmp_askha_boundary = in_any(keywords + [protein_name], *_ASKHA_FAMILY_TEXT_TOKENS)
    ghmp_pfk_boundary = askha_pfk_boundary
    non_ghmp_scope_side_ec = any(
        ec and not ec.startswith("2.7.1") for ec in _ec_numbers(row)
    )
    dnk_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_DNK_FAMILY_TEXT_TOKENS,
    )
    dnk_phosphoryl_reaction = in_any(
        reactions, *_DNK_PHOSPHORYL_REACTION_TOKENS
    ) and in_any(reactions, *_DNK_SUBSTRATE_REACTION_TOKENS)
    dnk_atp_mg_context = in_any(
        reactions + cofactor_names + feature_texts, *_DNK_ATP_MG_TOKENS
    )
    dnk_protein_kinase_boundary = askha_protein_kinase_boundary
    dnk_histidine_kinase_boundary = askha_histidine_kinase_boundary
    dnk_hydrolase_side_ec_boundary = askha_hydrolase_side_ec_boundary
    dnk_ndk_boundary = _ec_has_prefix(row, ("2.7.4",)) or in_any(
        keywords + [protein_name], *_NDK_FAMILY_TEXT_TOKENS
    )
    dnk_askha_boundary = in_any(keywords + [protein_name], *_ASKHA_FAMILY_TEXT_TOKENS)
    dnk_ghmp_boundary = in_any(keywords + [protein_name], *_GHMP_FAMILY_TEXT_TOKENS)
    dnk_pfk_boundary = askha_pfk_boundary
    non_dnk_scope_side_ec = any(
        ec and not ec.startswith("2.7.1") for ec in _ec_numbers(row)
    )
    pfka_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_PFKA_FAMILY_TEXT_TOKENS,
    )
    pfka_phosphoryl_reaction = in_any(
        reactions, *_PFKA_PHOSPHORYL_REACTION_TOKENS
    ) and in_any(reactions, *_PFKA_SUBSTRATE_REACTION_TOKENS)
    pfka_atp_mg_context = in_any(
        reactions + cofactor_names + feature_texts, *_PFKA_ATP_MG_TOKENS
    )
    pfka_protein_kinase_boundary = askha_protein_kinase_boundary
    pfka_histidine_kinase_boundary = askha_histidine_kinase_boundary
    pfka_hydrolase_side_ec_boundary = askha_hydrolase_side_ec_boundary
    pfka_ndk_boundary = _ec_has_prefix(row, ("2.7.4",)) or in_any(
        keywords + [protein_name], *_NDK_FAMILY_TEXT_TOKENS
    )
    pfka_dnk_boundary = in_any(keywords + [protein_name], *_DNK_FAMILY_TEXT_TOKENS)
    pfka_askha_boundary = in_any(
        keywords + [protein_name],
        "acetate kinase",
        "glucokinase",
        "hexokinase",
        "hexose kinase",
        "glycerol kinase",
        "askha",
    ) and "phosphohexokinase" not in protein_name
    pfka_ghmp_boundary = in_any(keywords + [protein_name], *_GHMP_FAMILY_TEXT_TOKENS)
    pfka_pfkb_boundary = in_any(keywords + [protein_name], *_PFKB_BOUNDARY_TOKENS)
    non_pfka_scope_side_ec = any(
        ec and not ec.startswith("2.7.1") for ec in _ec_numbers(row)
    )
    pfkb_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_PFKB_FAMILY_TEXT_TOKENS,
    )
    pfkb_phosphoryl_reaction = in_any(
        reactions, *_PFKB_PHOSPHORYL_REACTION_TOKENS
    ) and in_any(reactions, *_PFKB_SUBSTRATE_REACTION_TOKENS)
    pfkb_atp_mg_context = in_any(
        reactions + cofactor_names + feature_texts, *_PFKB_ATP_MG_TOKENS
    )
    pfkb_protein_kinase_boundary = askha_protein_kinase_boundary
    pfkb_histidine_kinase_boundary = askha_histidine_kinase_boundary
    pfkb_hydrolase_side_ec_boundary = askha_hydrolase_side_ec_boundary
    pfkb_ndk_boundary = _ec_has_prefix(row, ("2.7.4",)) or in_any(
        keywords + [protein_name], *_NDK_FAMILY_TEXT_TOKENS
    )
    pfkb_dnk_boundary = in_any(keywords + [protein_name], *_DNK_FAMILY_TEXT_TOKENS)
    pfkb_askha_boundary = in_any(keywords + [protein_name], *_ASKHA_FAMILY_TEXT_TOKENS)
    pfkb_ghmp_boundary = in_any(keywords + [protein_name], *_GHMP_FAMILY_TEXT_TOKENS)
    pfkb_pfka_boundary = in_any(keywords + [protein_name], *_PFKA_FAMILY_TEXT_TOKENS)
    non_pfkb_scope_side_ec = any(
        ec and not ec.startswith("2.7.1") for ec in _ec_numbers(row)
    )
    kinase_boundary = in_any(keywords + [protein_name], *_KINASE_BOUNDARY_TOKENS) or _ec_has_prefix(
        row, ("2.7.",)
    )
    protein_kinase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_PROTEIN_KINASE_FAMILY_TEXT_TOKENS,
    )
    protein_kinase_atp_mg_context = in_any(
        reactions + cofactor_names + feature_texts,
        *_PROTEIN_KINASE_ATP_MG_TOKENS,
    )
    protein_kinase_phosphoryl_reaction = in_any(
        reactions, *_PROTEIN_KINASE_REACTION_TOKENS
    ) and in_any(reactions, "atp", "adp", "phosphate", "phospho")
    protein_kinase_boundary_signal = _ec_has_prefix(
        row, ("2.7.1.", "2.7.4", "2.7.13", "6.")
    ) or in_any(
        keywords + [protein_name] + feature_texts,
        *_PROTEIN_KINASE_BOUNDARY_TOKENS,
    )
    non_protein_kinase_scope_side_ec = any(
        ec and not (ec.startswith("2.7.10") or ec.startswith("2.7.11"))
        for ec in _ec_numbers(row)
    )
    aminoglycoside_phosphotransferase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_FAMILY_TEXT_TOKENS,
    ) or (
        in_any(reactions + keywords + [protein_name] + feature_texts, "phosphotransferase")
        and in_any(
            reactions + keywords + [protein_name] + feature_texts,
            *_AMINOGLYCOSIDE_SUBSTRATE_TOKENS,
        )
    )
    aminoglycoside_phosphotransferase_atp_mg_context = in_any(
        reactions + cofactor_names + feature_texts,
        *_AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_ATP_MG_TOKENS,
    )
    aminoglycoside_phosphotransferase_phosphoryl_reaction = (
        in_any(reactions, *_AMINOGLYCOSIDE_SUBSTRATE_TOKENS)
        and in_any(reactions, *_AMINOGLYCOSIDE_PHOSPHORYL_TOKENS)
        and in_any(reactions, "atp", "adp")
    )
    aminoglycoside_phosphotransferase_boundary_signal = (
        in_any(
            keywords + [protein_name] + feature_texts + reactions,
            *_AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_BOUNDARY_TOKENS,
        )
        and not aminoglycoside_phosphotransferase_family_text
    )
    non_aminoglycoside_phosphotransferase_scope_side_ec = any(
        ec and ec not in _AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_EC
        for ec in _ec_numbers(row)
    )
    _aac_name_fields = reactions + keywords + [protein_name] + feature_texts
    aminoglycoside_acetyltransferase_family_text = (
        # aminoglycoside-resistance acetyltransferase names vary widely
        # (N(6')-, 6'-N-, 3-N-, gentamicin/kanamycin ...), so the robust handle is an
        # aminoglycoside-class drug term co-occurring with "acetyltransferase", plus
        # explicit AAC tokens.
        in_any(_aac_name_fields, *_AMINOGLYCOSIDE_DRUG_CLASS_TOKENS)
        and in_any(_aac_name_fields, "acetyltransferase")
    ) or in_any(_aac_name_fields, *_AMINOGLYCOSIDE_ACETYLTRANSFERASE_FAMILY_TEXT_TOKENS)
    aminoglycoside_acetyltransferase_acetyl_coa_context = in_any(
        reactions + feature_texts + cofactor_names,
        *_AMINOGLYCOSIDE_ACETYLTRANSFERASE_COA_TOKENS,
    )
    aminoglycoside_acetyltransferase_boundary_signal = (
        evidence.get("metal", False)
        or evidence.get("flavin", False)
        or in_any(
            keywords + [protein_name] + feature_texts + cofactor_names,
            *_AMINOGLYCOSIDE_ACETYLTRANSFERASE_BOUNDARY_TOKENS,
        )
    )
    non_aminoglycoside_acetyltransferase_scope_side_ec = any(
        ec and not ec.startswith("2.3.1") for ec in _ec_numbers(row)
    )
    had_like_phosphatase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_HAD_LIKE_PHOSPHATASE_FAMILY_TEXT_TOKENS,
    )
    had_like_phosphatase_asp_mg_context = in_any(
        cofactor_names + feature_texts,
        *_HAD_LIKE_PHOSPHATASE_ASP_MG_TOKENS,
    )
    had_like_phosphatase_phosphomonoester_reaction = in_any(
        reactions, *_HAD_LIKE_PHOSPHATASE_REACTION_TOKENS
    ) and in_any(reactions, *_HAD_LIKE_PHOSPHATASE_HYDROLYSIS_TOKENS)
    had_like_phosphatase_boundary_signal = (
        in_any(
            keywords + [protein_name] + feature_texts,
            *_HAD_LIKE_PHOSPHATASE_BOUNDARY_TOKENS,
        )
        and not had_like_phosphatase_family_text
    ) or _ec_has_prefix(row, ("3.1.4", "3.1.11", "3.1.12", "3.1.13", "3.1.21", "3.1.31"))
    non_had_like_phosphatase_scope_side_ec = any(
        ec and not ec.startswith("3.1.3") for ec in _ec_numbers(row)
    )
    ser_thr_protein_phosphatase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_SER_THR_PROTEIN_PHOSPHATASE_FAMILY_TEXT_TOKENS,
    )
    ser_thr_protein_phosphatase_metal_context = evidence.get("metal", False) or in_any(
        cofactor_names + feature_texts,
        *_SER_THR_PROTEIN_PHOSPHATASE_METAL_TOKENS,
    )
    ser_thr_protein_phosphatase_dephosphorylation_reaction = (
        in_any(reactions, *_SER_THR_PROTEIN_PHOSPHATASE_REACTION_TOKENS)
        and in_any(reactions, *_SER_THR_PROTEIN_PHOSPHATASE_PRODUCT_TOKENS)
        and in_any(reactions, *_SER_THR_PROTEIN_PHOSPHATASE_HYDROLYSIS_TOKENS)
    )
    ser_thr_protein_phosphatase_boundary_signal = (
        in_any(
            keywords + [protein_name] + feature_texts,
            *_SER_THR_PROTEIN_PHOSPHATASE_BOUNDARY_TOKENS,
        )
        and not ser_thr_protein_phosphatase_family_text
    ) or _ec_has_prefix(row, ("3.1.4", "3.1.11", "3.1.12", "3.1.13", "3.1.21", "3.1.31"))
    ser_thr_protein_phosphatase_cys_ptp_boundary = (
        _ec_has_prefix(row, ("3.1.3.48",))
        or in_any(
            keywords + [protein_name] + feature_texts,
            "protein-tyrosine phosphatase",
            "tyrosine-protein phosphatase",
            "dual specificity phosphatase",
            "dual-specificity phosphatase",
            "pten",
            "low molecular weight phosphotyrosine protein phosphatase",
            "phosphocysteine",
        )
    ) and not ser_thr_protein_phosphatase_metal_context
    non_ser_thr_protein_phosphatase_scope_side_ec = any(
        ec and not (ec.startswith("3.1.3.16") or ec.startswith("3.1.3.48"))
        for ec in _ec_numbers(row)
    )
    aldehyde_dehydrogenase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_ALDEHYDE_DEHYDROGENASE_FAMILY_TEXT_TOKENS,
    )
    aldehyde_dehydrogenase_active_site_context = in_any(
        feature_texts, *_ALDEHYDE_DEHYDROGENASE_ACTIVE_SITE_TOKENS
    )
    aldehyde_dehydrogenase_nad_p_context = cosubstrate_nad_p or in_any(
        feature_texts + cofactor_names, _NAD_P_COSUBSTRATE_TOKEN
    )
    aldehyde_dehydrogenase_reaction = in_any(
        reactions, *_ALDEHYDE_DEHYDROGENASE_REACTION_TOKENS
    )
    aldehyde_dehydrogenase_boundary_signal = (
        evidence.get("flavin", False)
        or molybdopterin_moco
        or peroxide_reaction
        or _ec_has_prefix(row, ("1.2.3", "1.2.5", "1.2.7", "1.2.99"))
        or in_any(
            keywords + [protein_name] + feature_texts + cofactor_names,
            *_ALDEHYDE_DEHYDROGENASE_BOUNDARY_TOKENS,
        )
    ) and not aldehyde_dehydrogenase_family_text
    generic_nad_p_dehydrogenase_boundary = (
        cosubstrate_nad_p
        and not aldehyde_dehydrogenase_family_text
        and not aldehyde_dehydrogenase_active_site_context
    )
    non_aldehyde_dehydrogenase_scope_side_ec = any(
        ec and not ec.startswith("1.2.1") for ec in _ec_numbers(row)
    )
    short_chain_dehydrogenase_reductase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_SDR_FAMILY_TEXT_TOKENS,
    )
    short_chain_dehydrogenase_reductase_nad_p_context = cosubstrate_nad_p or in_any(
        feature_texts + cofactor_names, _NAD_P_COSUBSTRATE_TOKEN
    )
    short_chain_dehydrogenase_reductase_active_site_context = in_any(
        feature_texts, *_SDR_ACTIVE_SITE_TOKENS
    )
    short_chain_dehydrogenase_reductase_reaction = in_any(
        reactions, *_SDR_REACTION_TOKENS
    ) and short_chain_dehydrogenase_reductase_nad_p_context
    short_chain_dehydrogenase_reductase_boundary_signal = (
        evidence.get("flavin", False)
        or evidence.get("metal", False)
        or molybdopterin_moco
        or evidence.get("copper", False)
        or peroxide_reaction
        or in_any(
            keywords + [protein_name] + feature_texts + cofactor_names,
            *_SDR_BOUNDARY_TOKENS,
        )
    )
    non_short_chain_dehydrogenase_reductase_scope_side_ec = any(
        ec and not ec.startswith("1.1.1") for ec in _ec_numbers(row)
    )
    aldo_keto_reductase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_AKR_FAMILY_TEXT_TOKENS,
    )
    aldo_keto_reductase_nad_p_context = cosubstrate_nad_p or in_any(
        feature_texts + cofactor_names, _NAD_P_COSUBSTRATE_TOKEN
    )
    aldo_keto_reductase_active_site_context = in_any(
        feature_texts, *_AKR_ACTIVE_SITE_TOKENS
    )
    aldo_keto_reductase_reaction = in_any(
        reactions, *_AKR_REACTION_TOKENS
    ) and aldo_keto_reductase_nad_p_context
    aldo_keto_reductase_boundary_signal = (
        evidence.get("flavin", False)
        or evidence.get("metal", False)
        or molybdopterin_moco
        or evidence.get("copper", False)
        or peroxide_reaction
        or in_any(
            keywords + [protein_name] + feature_texts + cofactor_names,
            *_AKR_BOUNDARY_TOKENS,
        )
    )
    non_aldo_keto_reductase_scope_side_ec = any(
        ec and not ec.startswith("1.1.1") for ec in _ec_numbers(row)
    )
    alpha_beta_hydrolase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_ALPHA_BETA_HYDROLASE_FAMILY_TEXT_TOKENS,
    )
    alpha_beta_hydrolase_ser_his_acid_context = in_any(
        feature_texts, *_ALPHA_BETA_HYDROLASE_TRIAD_TOKENS
    ) or (
        in_any(feature_texts, *_ALPHA_BETA_HYDROLASE_SERINE_TOKENS)
        and in_any(feature_texts, *_ALPHA_BETA_HYDROLASE_HISTIDINE_TOKENS)
        and in_any(feature_texts, *_ALPHA_BETA_HYDROLASE_ACID_TOKENS)
    )
    alpha_beta_hydrolase_ester_hydrolysis_reaction = in_any(
        reactions, *_ALPHA_BETA_HYDROLASE_ESTER_TOKENS
    ) and in_any(reactions, *_ALPHA_BETA_HYDROLASE_HYDROLYSIS_TOKENS)
    alpha_beta_hydrolase_boundary_signal = in_any(
        keywords + [protein_name] + feature_texts + reactions,
        *_ALPHA_BETA_HYDROLASE_BOUNDARY_TOKENS,
    )
    non_alpha_beta_hydrolase_scope_side_ec = any(
        ec and not ec.startswith("3.1.1") for ec in _ec_numbers(row)
    )
    serine_beta_lactamase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_SERINE_BETA_LACTAMASE_FAMILY_TEXT_TOKENS,
    )
    serine_beta_lactamase_hydrolysis_reaction = in_any(
        reactions, *_SERINE_BETA_LACTAMASE_REACTION_TOKENS
    ) and in_any(reactions, *_SERINE_BETA_LACTAMASE_HYDROLYSIS_TOKENS)
    serine_beta_lactamase_active_site_context = in_any(
        feature_texts, *_SERINE_BETA_LACTAMASE_ACTIVE_SITE_TOKENS
    ) or (
        active_or_binding_site_present
        and serine_beta_lactamase_family_text
    )
    serine_beta_lactamase_boundary_signal = (
        evidence.get("zinc", False)
        or evidence.get("metal", False)
        or _ec_has_prefix(row, ("3.5.2.7",))
        or in_any(
            keywords + [protein_name] + feature_texts + reactions + cofactor_names,
            *_SERINE_BETA_LACTAMASE_BOUNDARY_TOKENS,
        )
    )
    non_serine_beta_lactamase_scope_side_ec = any(
        ec and ec != "3.5.2.6" for ec in _ec_numbers(row)
    )
    metallo_beta_lactamase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_METALLO_BETA_LACTAMASE_FAMILY_TEXT_TOKENS,
    )
    metallo_beta_lactamase_zinc_context = bool(evidence.get("zinc")) or in_any(
        keywords + [protein_name] + feature_texts + cofactor_names, "metallo", "zinc"
    )
    metallo_beta_lactamase_betalactam_reaction = in_any(
        reactions, *_SERINE_BETA_LACTAMASE_REACTION_TOKENS
    ) and in_any(reactions, *_SERINE_BETA_LACTAMASE_HYDROLYSIS_TOKENS)
    metallo_beta_lactamase_boundary_signal = in_any(
        keywords + [protein_name] + feature_texts + reactions,
        *_METALLO_BETA_LACTAMASE_BOUNDARY_TOKENS,
    )
    non_metallo_beta_lactamase_scope_side_ec = any(
        ec and ec != "3.5.2.6" for ec in _ec_numbers(row)
    )
    peroxiredoxin_thiol_peroxidase_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_PEROXIREDOXIN_FAMILY_TEXT_TOKENS,
    )
    peroxiredoxin_thiol_peroxidase_thiol_context = in_any(
        keywords + [protein_name] + feature_texts + reactions + cofactor_names,
        *_PEROXIREDOXIN_THIOL_TOKENS,
    )
    peroxiredoxin_thiol_peroxidase_reaction = in_any(
        reactions, *_PEROXIREDOXIN_REACTION_TOKENS
    )
    peroxiredoxin_thiol_peroxidase_boundary_signal = in_any(
        keywords + [protein_name] + feature_texts + reactions,
        *_PEROXIREDOXIN_BOUNDARY_TOKENS,
    )
    non_peroxiredoxin_thiol_peroxidase_scope_side_ec = any(
        ec and not ec.startswith("1.11.1") for ec in _ec_numbers(row)
    )
    paps_sulfotransferase_family_text = in_any(
        keywords + [protein_name] + feature_texts,
        *_PAPS_SULFOTRANSFERASE_FAMILY_TEXT_TOKENS,
    )
    paps_sulfotransferase_reaction = in_any(
        reactions, *_PAPS_SULFOTRANSFERASE_REACTION_TOKENS
    )
    paps_sulfotransferase_boundary_signal = in_any(
        keywords + [protein_name] + feature_texts + reactions,
        *_PAPS_SULFOTRANSFERASE_BOUNDARY_TOKENS,
    )
    non_paps_sulfotransferase_scope_side_ec = any(
        ec and not ec.startswith("2.8.2") for ec in _ec_numbers(row)
    )
    glutathione_s_transferase_family_text = in_any(
        keywords + [protein_name] + feature_texts,
        *_GLUTATHIONE_S_TRANSFERASE_FAMILY_TEXT_TOKENS,
    )
    glutathione_s_transferase_reaction = in_any(
        reactions, *_GLUTATHIONE_S_TRANSFERASE_REACTION_TOKENS
    )
    glutathione_s_transferase_boundary_signal = in_any(
        keywords + [protein_name] + feature_texts + reactions,
        *_GLUTATHIONE_S_TRANSFERASE_BOUNDARY_TOKENS,
    )
    non_glutathione_s_transferase_scope_side_ec = any(
        ec and not ec.startswith("2.5.1.18") for ec in _ec_numbers(row)
    )
    aminoacyl_trna_synthetase_family_text = in_any(
        keywords + [protein_name] + feature_texts,
        *_AMINOACYL_TRNA_SYNTHETASE_FAMILY_TEXT_TOKENS,
    )
    aminoacyl_trna_synthetase_reaction = in_any(
        reactions, *_AMINOACYL_TRNA_SYNTHETASE_REACTION_TOKENS
    )
    aminoacyl_trna_synthetase_boundary_signal = in_any(
        keywords + [protein_name] + feature_texts,
        *_AMINOACYL_TRNA_SYNTHETASE_BOUNDARY_TOKENS,
    )
    non_aminoacyl_trna_synthetase_scope_side_ec = any(
        ec and not ec.startswith("6.1.1") for ec in _ec_numbers(row)
    )
    non_6_3_side_ec = any(ec and not ec.startswith("6.3") for ec in _ec_numbers(row))
    non_biotin_carboxylase_scope_side_ec = any(
        ec and not (ec.startswith("6.4.1") or ec.startswith("6.3.4"))
        for ec in _ec_numbers(row)
    )
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
    terpene_family_text = in_any(
        reactions + keywords + [protein_name] + feature_texts,
        *_TERPENE_FAMILY_TEXT_TOKENS,
    )
    terpene_mg_mn_context = in_any(
        cofactor_names + feature_texts, *_TERPENE_MG_MN_TOKENS
    )
    terpene_diphosphate_context = in_any(
        reactions + cofactor_names + feature_texts, *_TERPENE_DIPHOSPHATE_TOKENS
    )
    terpene_cyclization_reaction = in_any(
        reactions, *_TERPENE_PRODUCT_TOKENS
    ) and terpene_diphosphate_context
    terpene_boundary_signal = (
        _ec_has_prefix(row, ("2.5.1",))
        or in_any(keywords + [protein_name], *_TERPENE_BOUNDARY_TOKENS)
    ) and not terpene_family_text
    non_4_2_3_side_ec = any(ec and not ec.startswith("4.2.3") for ec in _ec_numbers(row))
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
            "glycoside_hydrolase_family_text": glycoside_hydrolase_family_text,
            "glycoside_hydrolysis_reaction": glycoside_hydrolysis_reaction,
            "glycoside_hydrolase_active_site_context": glycoside_hydrolase_active_site_context,
            "glycoside_hydrolase_boundary_signal": glycoside_hydrolase_boundary_signal,
            "non_glycoside_hydrolase_scope_side_ec": non_glycoside_hydrolase_scope_side_ec,
            "n_ribosyl_hydrolase_family_text": n_ribosyl_hydrolase_family_text,
            "n_ribosyl_hydrolysis_reaction": n_ribosyl_hydrolysis_reaction,
            "n_ribosyl_active_site_context": n_ribosyl_active_site_context,
            "n_ribosyl_hydrolase_boundary_signal": n_ribosyl_hydrolase_boundary_signal,
            "non_n_ribosyl_hydrolase_scope_side_ec": non_n_ribosyl_hydrolase_scope_side_ec,
            "metal_independent_pde_family_text": metal_independent_pde_family_text,
            "metal_independent_pde_reaction": metal_independent_pde_reaction,
            "metal_independent_pde_active_site_context": metal_independent_pde_active_site_context,
            "metal_independent_pde_metal_boundary": metal_independent_pde_metal_boundary,
            "metal_independent_pde_boundary_signal": metal_independent_pde_boundary_signal,
            "non_metal_independent_pde_scope_side_ec": non_metal_independent_pde_scope_side_ec,
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
            "mn_fe_sod_family_text": mn_fe_sod_family_text,
            "mn_fe_sod_family_or_name_context": mn_fe_sod_family_or_name_context,
            "mn_fe_sod_superoxide_dismutation_reaction": mn_fe_sod_superoxide_dismutation_reaction,
            "mn_fe_sod_metal_context": mn_fe_sod_metal_context,
            "mn_fe_sod_boundary_signal": mn_fe_sod_boundary_signal,
            "non_mn_fe_sod_scope_side_ec": non_mn_fe_sod_scope_side_ec,
            "atp_ligase_atp_or_adp_phosphate": atp_ligase_atp_or_adp_phosphate,
            "atp_ligase_mg_context": atp_ligase_mg_context,
            "keyword_ligase": keyword_ligase,
            "atp_grasp_family_text": atp_grasp_family_text,
            "atp_amide_ligation_text": atp_amide_ligation_text,
            "atp_acyl_phosphate_intermediate": atp_acyl_phosphate_intermediate,
            "biotin_carboxylase_boundary": biotin_carboxylase_boundary,
            "biotin_feature_or_ligand": biotin_feature_or_ligand,
            "biotin_keyword_or_name": biotin_keyword_or_name,
            "biotin_carboxylase_text": biotin_carboxylase_text,
            "biotin_carboxylation_reaction": biotin_carboxylation_reaction,
            "ndk_family_text": ndk_family_text,
            "ndk_ntp_ndp_reaction": ndk_ntp_ndp_reaction,
            "ndk_active_his_context": ndk_active_his_context,
            "ndk_protein_kinase_boundary": ndk_protein_kinase_boundary,
            "ndk_two_component_histidine_kinase_boundary": ndk_two_component_histidine_kinase_boundary,
            "ndk_hydrolase_nuclease_side_ec_boundary": ndk_hydrolase_nuclease_side_ec_boundary,
            "ndk_other_nmp_kinase_side_ec_boundary": ndk_other_nmp_kinase_side_ec_boundary,
            "askha_family_text": askha_family_text,
            "askha_phosphoryl_reaction": askha_phosphoryl_reaction,
            "askha_atp_mg_context": askha_atp_mg_context,
            "askha_protein_kinase_boundary": askha_protein_kinase_boundary,
            "askha_histidine_kinase_boundary": askha_histidine_kinase_boundary,
            "askha_hydrolase_side_ec_boundary": askha_hydrolase_side_ec_boundary,
            "askha_ndk_boundary": askha_ndk_boundary,
            "askha_dnk_boundary": askha_dnk_boundary,
            "askha_ghmp_boundary": askha_ghmp_boundary,
            "askha_pfk_boundary": askha_pfk_boundary,
            "non_askha_scope_side_ec": non_askha_scope_side_ec,
            "ghmp_family_text": ghmp_family_text,
            "ghmp_phosphoryl_reaction": ghmp_phosphoryl_reaction,
            "ghmp_atp_mg_context": ghmp_atp_mg_context,
            "ghmp_protein_kinase_boundary": ghmp_protein_kinase_boundary,
            "ghmp_histidine_kinase_boundary": ghmp_histidine_kinase_boundary,
            "ghmp_hydrolase_side_ec_boundary": ghmp_hydrolase_side_ec_boundary,
            "ghmp_ndk_boundary": ghmp_ndk_boundary,
            "ghmp_dnk_boundary": ghmp_dnk_boundary,
            "ghmp_askha_boundary": ghmp_askha_boundary,
            "ghmp_pfk_boundary": ghmp_pfk_boundary,
            "non_ghmp_scope_side_ec": non_ghmp_scope_side_ec,
            "dnk_family_text": dnk_family_text,
            "dnk_phosphoryl_reaction": dnk_phosphoryl_reaction,
            "dnk_atp_mg_context": dnk_atp_mg_context,
            "dnk_protein_kinase_boundary": dnk_protein_kinase_boundary,
            "dnk_histidine_kinase_boundary": dnk_histidine_kinase_boundary,
            "dnk_hydrolase_side_ec_boundary": dnk_hydrolase_side_ec_boundary,
            "dnk_ndk_boundary": dnk_ndk_boundary,
            "dnk_askha_boundary": dnk_askha_boundary,
            "dnk_ghmp_boundary": dnk_ghmp_boundary,
            "dnk_pfk_boundary": dnk_pfk_boundary,
            "non_dnk_scope_side_ec": non_dnk_scope_side_ec,
            "pfka_family_text": pfka_family_text,
            "pfka_phosphoryl_reaction": pfka_phosphoryl_reaction,
            "pfka_atp_mg_context": pfka_atp_mg_context,
            "pfka_protein_kinase_boundary": pfka_protein_kinase_boundary,
            "pfka_histidine_kinase_boundary": pfka_histidine_kinase_boundary,
            "pfka_hydrolase_side_ec_boundary": pfka_hydrolase_side_ec_boundary,
            "pfka_ndk_boundary": pfka_ndk_boundary,
            "pfka_dnk_boundary": pfka_dnk_boundary,
            "pfka_askha_boundary": pfka_askha_boundary,
            "pfka_ghmp_boundary": pfka_ghmp_boundary,
            "pfka_pfkb_boundary": pfka_pfkb_boundary,
            "non_pfka_scope_side_ec": non_pfka_scope_side_ec,
            "pfkb_family_text": pfkb_family_text,
            "pfkb_phosphoryl_reaction": pfkb_phosphoryl_reaction,
            "pfkb_atp_mg_context": pfkb_atp_mg_context,
            "pfkb_protein_kinase_boundary": pfkb_protein_kinase_boundary,
            "pfkb_histidine_kinase_boundary": pfkb_histidine_kinase_boundary,
            "pfkb_hydrolase_side_ec_boundary": pfkb_hydrolase_side_ec_boundary,
            "pfkb_ndk_boundary": pfkb_ndk_boundary,
            "pfkb_dnk_boundary": pfkb_dnk_boundary,
            "pfkb_askha_boundary": pfkb_askha_boundary,
            "pfkb_ghmp_boundary": pfkb_ghmp_boundary,
            "pfkb_pfka_boundary": pfkb_pfka_boundary,
            "non_pfkb_scope_side_ec": non_pfkb_scope_side_ec,
            "kinase_boundary": kinase_boundary,
            "non_6_3_side_ec": non_6_3_side_ec,
            "non_biotin_carboxylase_scope_side_ec": non_biotin_carboxylase_scope_side_ec,
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
            "terpene_family_text": terpene_family_text,
            "terpene_mg_mn_context": terpene_mg_mn_context,
            "terpene_diphosphate_context": terpene_diphosphate_context,
            "terpene_cyclization_reaction": terpene_cyclization_reaction,
            "terpene_boundary_signal": terpene_boundary_signal,
            "non_4_2_3_side_ec": non_4_2_3_side_ec,
            "protein_kinase_family_text": protein_kinase_family_text,
            "protein_kinase_atp_mg_context": protein_kinase_atp_mg_context,
            "protein_kinase_phosphoryl_reaction": protein_kinase_phosphoryl_reaction,
            "protein_kinase_boundary_signal": protein_kinase_boundary_signal,
            "non_protein_kinase_scope_side_ec": non_protein_kinase_scope_side_ec,
            "aminoglycoside_phosphotransferase_family_text": aminoglycoside_phosphotransferase_family_text,
            "aminoglycoside_phosphotransferase_atp_mg_context": aminoglycoside_phosphotransferase_atp_mg_context,
            "aminoglycoside_phosphotransferase_phosphoryl_reaction": aminoglycoside_phosphotransferase_phosphoryl_reaction,
            "aminoglycoside_phosphotransferase_boundary_signal": aminoglycoside_phosphotransferase_boundary_signal,
            "non_aminoglycoside_phosphotransferase_scope_side_ec": non_aminoglycoside_phosphotransferase_scope_side_ec,
            "aminoglycoside_acetyltransferase_family_text": aminoglycoside_acetyltransferase_family_text,
            "aminoglycoside_acetyltransferase_acetyl_coa_context": aminoglycoside_acetyltransferase_acetyl_coa_context,
            "aminoglycoside_acetyltransferase_boundary_signal": aminoglycoside_acetyltransferase_boundary_signal,
            "non_aminoglycoside_acetyltransferase_scope_side_ec": non_aminoglycoside_acetyltransferase_scope_side_ec,
            "had_like_phosphatase_family_text": had_like_phosphatase_family_text,
            "had_like_phosphatase_asp_mg_context": had_like_phosphatase_asp_mg_context,
            "had_like_phosphatase_phosphomonoester_reaction": had_like_phosphatase_phosphomonoester_reaction,
            "had_like_phosphatase_boundary_signal": had_like_phosphatase_boundary_signal,
            "non_had_like_phosphatase_scope_side_ec": non_had_like_phosphatase_scope_side_ec,
            "ser_thr_protein_phosphatase_family_text": ser_thr_protein_phosphatase_family_text,
            "ser_thr_protein_phosphatase_metal_context": ser_thr_protein_phosphatase_metal_context,
            "ser_thr_protein_phosphatase_dephosphorylation_reaction": ser_thr_protein_phosphatase_dephosphorylation_reaction,
            "ser_thr_protein_phosphatase_boundary_signal": ser_thr_protein_phosphatase_boundary_signal,
            "ser_thr_protein_phosphatase_cys_ptp_boundary": ser_thr_protein_phosphatase_cys_ptp_boundary,
            "non_ser_thr_protein_phosphatase_scope_side_ec": non_ser_thr_protein_phosphatase_scope_side_ec,
            "aldehyde_dehydrogenase_family_text": aldehyde_dehydrogenase_family_text,
            "aldehyde_dehydrogenase_active_site_context": aldehyde_dehydrogenase_active_site_context,
            "aldehyde_dehydrogenase_nad_p_context": aldehyde_dehydrogenase_nad_p_context,
            "aldehyde_dehydrogenase_reaction": aldehyde_dehydrogenase_reaction,
            "aldehyde_dehydrogenase_boundary_signal": aldehyde_dehydrogenase_boundary_signal,
            "generic_nad_p_dehydrogenase_boundary": generic_nad_p_dehydrogenase_boundary,
            "non_aldehyde_dehydrogenase_scope_side_ec": non_aldehyde_dehydrogenase_scope_side_ec,
            "short_chain_dehydrogenase_reductase_family_text": short_chain_dehydrogenase_reductase_family_text,
            "short_chain_dehydrogenase_reductase_nad_p_context": short_chain_dehydrogenase_reductase_nad_p_context,
            "short_chain_dehydrogenase_reductase_active_site_context": short_chain_dehydrogenase_reductase_active_site_context,
            "short_chain_dehydrogenase_reductase_reaction": short_chain_dehydrogenase_reductase_reaction,
            "short_chain_dehydrogenase_reductase_boundary_signal": short_chain_dehydrogenase_reductase_boundary_signal,
            "non_short_chain_dehydrogenase_reductase_scope_side_ec": non_short_chain_dehydrogenase_reductase_scope_side_ec,
            "aldo_keto_reductase_family_text": aldo_keto_reductase_family_text,
            "aldo_keto_reductase_nad_p_context": aldo_keto_reductase_nad_p_context,
            "aldo_keto_reductase_active_site_context": aldo_keto_reductase_active_site_context,
            "aldo_keto_reductase_reaction": aldo_keto_reductase_reaction,
            "aldo_keto_reductase_boundary_signal": aldo_keto_reductase_boundary_signal,
            "non_aldo_keto_reductase_scope_side_ec": non_aldo_keto_reductase_scope_side_ec,
            "alpha_beta_hydrolase_family_text": alpha_beta_hydrolase_family_text,
            "alpha_beta_hydrolase_ser_his_acid_context": alpha_beta_hydrolase_ser_his_acid_context,
            "alpha_beta_hydrolase_ester_hydrolysis_reaction": alpha_beta_hydrolase_ester_hydrolysis_reaction,
            "alpha_beta_hydrolase_boundary_signal": alpha_beta_hydrolase_boundary_signal,
            "non_alpha_beta_hydrolase_scope_side_ec": non_alpha_beta_hydrolase_scope_side_ec,
            "serine_beta_lactamase_family_text": serine_beta_lactamase_family_text,
            "serine_beta_lactamase_hydrolysis_reaction": serine_beta_lactamase_hydrolysis_reaction,
            "serine_beta_lactamase_active_site_context": serine_beta_lactamase_active_site_context,
            "serine_beta_lactamase_boundary_signal": serine_beta_lactamase_boundary_signal,
            "metallo_beta_lactamase_family_text": metallo_beta_lactamase_family_text,
            "metallo_beta_lactamase_zinc_context": metallo_beta_lactamase_zinc_context,
            "metallo_beta_lactamase_betalactam_reaction": metallo_beta_lactamase_betalactam_reaction,
            "metallo_beta_lactamase_boundary_signal": metallo_beta_lactamase_boundary_signal,
            "non_metallo_beta_lactamase_scope_side_ec": non_metallo_beta_lactamase_scope_side_ec,
            "peroxiredoxin_thiol_peroxidase_family_text": peroxiredoxin_thiol_peroxidase_family_text,
            "peroxiredoxin_thiol_peroxidase_thiol_context": peroxiredoxin_thiol_peroxidase_thiol_context,
            "peroxiredoxin_thiol_peroxidase_reaction": peroxiredoxin_thiol_peroxidase_reaction,
            "peroxiredoxin_thiol_peroxidase_boundary_signal": peroxiredoxin_thiol_peroxidase_boundary_signal,
            "non_peroxiredoxin_thiol_peroxidase_scope_side_ec": non_peroxiredoxin_thiol_peroxidase_scope_side_ec,
            "paps_sulfotransferase_family_text": paps_sulfotransferase_family_text,
            "paps_sulfotransferase_reaction": paps_sulfotransferase_reaction,
            "paps_sulfotransferase_boundary_signal": paps_sulfotransferase_boundary_signal,
            "non_paps_sulfotransferase_scope_side_ec": non_paps_sulfotransferase_scope_side_ec,
            "glutathione_s_transferase_family_text": glutathione_s_transferase_family_text,
            "glutathione_s_transferase_reaction": glutathione_s_transferase_reaction,
            "glutathione_s_transferase_boundary_signal": glutathione_s_transferase_boundary_signal,
            "non_glutathione_s_transferase_scope_side_ec": non_glutathione_s_transferase_scope_side_ec,
            "aminoacyl_trna_synthetase_family_text": aminoacyl_trna_synthetase_family_text,
            "aminoacyl_trna_synthetase_reaction": aminoacyl_trna_synthetase_reaction,
            "aminoacyl_trna_synthetase_boundary_signal": aminoacyl_trna_synthetase_boundary_signal,
            "non_aminoacyl_trna_synthetase_scope_side_ec": non_aminoacyl_trna_synthetase_scope_side_ec,
            "non_serine_beta_lactamase_scope_side_ec": non_serine_beta_lactamase_scope_side_ec,
            "non_thdp_scope_side_ec": non_thdp_scope_side_ec,
            "schiff_class_i_boundary_signal": schiff_class_i_boundary_signal,
            "non_4_1_2_or_4_1_3_side_ec": non_4_1_2_or_4_1_3_side_ec,
            "plp_boundary_signal": evidence.get("plp", False),
            "cofactorless_context": cofactorless_context,
            "active_or_binding_site_present": active_or_binding_site_present,
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
        or evidence.get("mn_fe_sod_metal_context")
        or evidence.get("atp_ligase_atp_or_adp_phosphate")
        or evidence.get("atp_ligase_mg_context")
        or evidence.get("thdp")
        or evidence.get("thdp_mg_context")
        or evidence.get("zinc_feature_or_ligand")
        or evidence.get("biotin_feature_or_ligand")
        or (
            evidence.get("biotin_keyword_or_name")
            and evidence.get("biotin_carboxylation_reaction")
        )
        or (
            evidence.get("biotin_carboxylation_reaction")
            and evidence.get("biotin_carboxylase_text")
        )
        or evidence.get("ndk_ntp_ndp_reaction")
        or evidence.get("askha_atp_mg_context")
        or evidence.get("askha_phosphoryl_reaction")
        or evidence.get("ghmp_atp_mg_context")
        or evidence.get("ghmp_phosphoryl_reaction")
        or evidence.get("dnk_atp_mg_context")
        or evidence.get("dnk_phosphoryl_reaction")
        or evidence.get("pfka_atp_mg_context")
        or evidence.get("pfka_phosphoryl_reaction")
        or evidence.get("pfkb_atp_mg_context")
        or evidence.get("pfkb_phosphoryl_reaction")
        or evidence.get("terpene_mg_mn_context")
        or evidence.get("terpene_diphosphate_context")
        or evidence.get("protein_kinase_atp_mg_context")
        or evidence.get("aminoglycoside_phosphotransferase_atp_mg_context")
        or evidence.get("aminoglycoside_phosphotransferase_phosphoryl_reaction")
        or evidence.get("had_like_phosphatase_asp_mg_context")
        or evidence.get("ser_thr_protein_phosphatase_metal_context")
        or evidence.get("aldehyde_dehydrogenase_nad_p_context")
        or evidence.get("short_chain_dehydrogenase_reductase_nad_p_context")
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
        or evidence.get("glycoside_hydrolysis_reaction")
        or evidence.get("n_ribosyl_hydrolysis_reaction")
        or evidence.get("metal_independent_pde_reaction")
        or evidence.get("isomerization_reaction")
        or evidence.get("molybdopterin_redox_reaction")
        or evidence.get("molybdopterin_oxo_transfer_reaction")
        or evidence.get("copper_redox_reaction")
        or evidence.get("copper_oxidase_reaction")
        or evidence.get("mn_fe_sod_superoxide_dismutation_reaction")
        or evidence.get("racemase_epimerase_text")
        or evidence.get("atp_ligase_atp_or_adp_phosphate")
        or evidence.get("atp_amide_ligation_text")
        or evidence.get("atp_acyl_phosphate_intermediate")
        or evidence.get("class_ii_aldolase_cc_reaction")
        or evidence.get("class_ii_metal_aldolase_text")
        or evidence.get("thdp_reaction_context")
        or evidence.get("zinc_hydration_elimination_reaction")
        or evidence.get("biotin_carboxylation_reaction")
        or evidence.get("ndk_ntp_ndp_reaction")
        or evidence.get("askha_phosphoryl_reaction")
        or evidence.get("ghmp_phosphoryl_reaction")
        or evidence.get("dnk_phosphoryl_reaction")
        or evidence.get("pfka_phosphoryl_reaction")
        or evidence.get("pfkb_phosphoryl_reaction")
        or evidence.get("terpene_cyclization_reaction")
        or evidence.get("protein_kinase_phosphoryl_reaction")
        or evidence.get("aminoglycoside_phosphotransferase_phosphoryl_reaction")
        or evidence.get("had_like_phosphatase_phosphomonoester_reaction")
        or evidence.get("ser_thr_protein_phosphatase_dephosphorylation_reaction")
        or evidence.get("aldehyde_dehydrogenase_reaction")
        or evidence.get("short_chain_dehydrogenase_reductase_reaction")
        or evidence.get("alpha_beta_hydrolase_ester_hydrolysis_reaction")
        or evidence.get("serine_beta_lactamase_hydrolysis_reaction")
    ):
        axes.add("rhea_reaction_or_participant_pattern")
    if (
        evidence.get("active_or_binding_site_present")
        or evidence.get("glycoside_hydrolase_active_site_context")
        or evidence.get("n_ribosyl_active_site_context")
        or evidence.get("metal_independent_pde_active_site_context")
        or evidence.get("cx3cx2c_motif")
        or evidence.get("heme_thiolate_binding")
        or evidence.get("molybdopterin_feature_or_ligand")
        or evidence.get("copper_feature_or_ligand")
        or evidence.get("zinc_feature_or_ligand")
        or evidence.get("biotin_feature_or_ligand")
        or evidence.get("ndk_active_his_context")
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("askha_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("ghmp_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("dnk_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("pfka_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("pfkb_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("mn_fe_sod_family_or_name_context")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("terpene_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("protein_kinase_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("aminoglycoside_phosphotransferase_family_text")
        )
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("had_like_phosphatase_family_text")
        )
        or evidence.get("had_like_phosphatase_asp_mg_context")
        or (
            evidence.get("active_or_binding_site_present")
            and evidence.get("ser_thr_protein_phosphatase_family_text")
        )
        or evidence.get("ser_thr_protein_phosphatase_metal_context")
        or evidence.get("aldehyde_dehydrogenase_active_site_context")
        or evidence.get("short_chain_dehydrogenase_reductase_active_site_context")
        or evidence.get("alpha_beta_hydrolase_ser_his_acid_context")
        or evidence.get("serine_beta_lactamase_active_site_context")
    ):
        axes.add("active_site_motif_or_residue_role")
    if (
        evidence.get("keyword_glycosyltransferase")
        or evidence.get("glycoside_hydrolase_family_text")
        or evidence.get("n_ribosyl_hydrolase_family_text")
        or evidence.get("metal_independent_pde_family_text")
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
        or evidence.get("biotin_keyword_or_name")
        or evidence.get("biotin_carboxylase_text")
        or evidence.get("ndk_family_text")
        or evidence.get("askha_family_text")
        or evidence.get("ghmp_family_text")
        or evidence.get("dnk_family_text")
        or evidence.get("pfka_family_text")
        or evidence.get("pfkb_family_text")
        or evidence.get("mn_fe_sod_family_text")
        or evidence.get("terpene_family_text")
        or evidence.get("protein_kinase_family_text")
        or evidence.get("aminoglycoside_phosphotransferase_family_text")
        or evidence.get("had_like_phosphatase_family_text")
        or evidence.get("ser_thr_protein_phosphatase_family_text")
        or evidence.get("aldehyde_dehydrogenase_family_text")
        or evidence.get("short_chain_dehydrogenase_reductase_family_text")
        or evidence.get("aldo_keto_reductase_family_text")
        or evidence.get("aminoglycoside_acetyltransferase_family_text")
        or evidence.get("alpha_beta_hydrolase_family_text")
        or evidence.get("serine_beta_lactamase_family_text")
        or evidence.get("metallo_beta_lactamase_family_text")
        or evidence.get("peroxiredoxin_thiol_peroxidase_family_text")
        or evidence.get("paps_sulfotransferase_family_text")
        or evidence.get("glutathione_s_transferase_family_text")
        or evidence.get("aminoacyl_trna_synthetase_family_text")
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
_SHORT_CHAIN_DEHYDROGENASE_REDUCTASE_EC = ("1.1.1",)  # SDR subtype; EC scope only
_ALDO_KETO_REDUCTASE_EC = ("1.1.1",)  # AKR subtype; EC scope only
_GLYCOSYLTRANSFERASE_EC = ("2.4",)    # glycosyl/hexosyl/pentosyl/sialyl transferases
_GLYCOSIDE_HYDROLASE_EC = ("3.2.1",)  # glycosidic bond hydrolysis; EC scope only
_SAM_METHYLTRANSFERASE_EC = ("2.1.1",)  # methyl group transfer, mostly SAM/SAH donor/product
_P450_MONOOXYGENASE_EC = ("1.14.",)  # paired-donor oxidoreductases incorporating one O atom
_NON_HEME_IRON_2OG_EC = ("1.14.11",)  # 2-oxoglutarate-dependent dioxygenases
_COA_ACYLTRANSFERASE_EC = ("2.3.1",)  # acyltransferases using CoA/acyl-CoA donors
_AMINOGLYCOSIDE_ACETYLTRANSFERASE_EC = ("2.3.1",)  # AAC acetyltransferases; EC scope only
_COFACTOR_INDEPENDENT_ISOMERASE_EC = ("5.3.",)  # intramolecular isomerases
_MOLYBDOPTERIN_OXIDOREDUCTASE_EC = ("1.",)  # oxidoreductases; Mo-cofactor handles confirm
_COPPER_OXIDOREDUCTASE_EC = (
    "1.10.3",
    "1.4.3",
)  # copper oxidases; copper/Rhea handles confirm
_MN_FE_SUPEROXIDE_DISMUTASE_EC = ("1.15.1.1",)  # Mn/Fe SOD; EC scope only
_METAL_RACEMASE_EPIMERASE_NON_PLP_EC = ("5.1.",)  # racemase/epimerase scope only
_ATP_AMIDE_LIGASE_EC = ("6.3.",)  # C-N ligases; ATP/Mg/Rhea handles confirm
_BIOTIN_DEPENDENT_CARBOXYLASE_EC = (
    "6.4.1",
    "6.3.4",
)  # biotin carboxylases; EC is scope only
_CLASS_II_METAL_ALDOLASE_EC = ("4.1.2", "4.1.3")  # metal aldol lyases; EC is scope only
_THIAMINE_DIPHOSPHATE_ENZYME_EC = (
    "2.2.1",
    "4.1.1",
    "1.2.4",
)  # ThDP ylide/carbonyl chemistry; EC is scope only
_ZINC_LYASE_HYDRATASE_EC = ("4.2.1",)  # zinc hydro-lyases; EC is scope only
_TERPENE_CYCLASE_SYNTHASE_EC = ("4.2.3",)  # terpene cyclases/synthases; EC is scope only
_PROTEIN_KINASE_SER_THR_TYR_EC = ("2.7.10", "2.7.11")  # protein kinases; EC scope only
_AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_EC = (
    "2.7.1.95",
    "2.7.1.72",
    "2.7.1.87",
    "2.7.1.119",
    "2.7.1.163",
)  # APH aminoglycoside kinases; EC scope only
_HAD_LIKE_PHOSPHATASE_EC = ("3.1.3",)  # HAD-like phosphatases; EC scope only
_SER_THR_PROTEIN_PHOSPHATASE_EC = ("3.1.3.16", "3.1.3.48")  # protein phosphatases; EC scope only
_ALDEHYDE_DEHYDROGENASE_EC = ("1.2.1",)  # ALDH; EC scope only
_ALPHA_BETA_HYDROLASE_ESTERASE_LIPASE_EC = ("3.1.1",)  # esterase/lipase; EC scope only
_SERINE_BETA_LACTAMASE_EC = ("3.5.2.6",)  # serine beta-lactamase; EC scope only
_METALLO_BETA_LACTAMASE_EC = ("3.5.2.6",)  # metallo beta-lactamase; EC scope only (shared)
_PEROXIREDOXIN_THIOL_PEROXIDASE_EC = ("1.11.1",)  # peroxiredoxin/thiol peroxidase; EC scope only (shared with heme peroxidases)
_PAPS_SULFOTRANSFERASE_EC = ("2.8.2",)  # PAPS-dependent sulfotransferase; EC scope only (not shared)
_GLUTATHIONE_S_TRANSFERASE_EC = ("2.5.1.18",)  # glutathione S-transferase; EC scope only (not shared)
_AMINOACYL_TRNA_SYNTHETASE_EC = ("6.1.1",)  # aminoacyl-tRNA synthetase; EC scope only (not shared)
_METAL_INDEPENDENT_PHOSPHODIESTERASE_EC = (
    "3.1.4",
    "4.6.1",
)  # metal-independent phosphodiester/cyclic-nucleotide hydrolysis; EC scope only
_N_RIBOSYL_HYDROLASE_EC = ("3.2.2",)  # N-glycosylase/nucleoside hydrolase; EC scope only
_NUCLEOSIDE_DIPHOSPHATE_KINASE_EC = ("2.7.4.6",)  # NDK; EC is scope only
_ASKHA_SUGAR_ACETATE_KINASE_EC = ("2.7.1",)  # ASKHA sugar/acetate kinase; EC scope only
_GHMP_SMALL_MOLECULE_KINASE_EC = ("2.7.1",)  # GHMP small-molecule kinase; EC scope only
_DEOXYNUCLEOSIDE_KINASE_EC = ("2.7.1",)  # dNK; EC scope only
_PFKA_PHOSPHOFRUCTOKINASE_EC = ("2.7.1",)  # PfkA; EC scope only
_PFKB_RIBOKINASE_FAMILY_EC = ("2.7.1",)  # PfkB/ribokinase family; EC scope only


# Each rule: fingerprint id -> predicate over (cofactor_evidence, row).
DISAMBIGUATION_RULES: tuple[tuple[str, Callable[[dict[str, bool], dict[str, Any]], bool]], ...] = (
    (
        "heme_peroxidase_oxidase",
        lambda c, row: c["heme"]
        and _ec_has_prefix(row, ("1.11.1",))
        and not c["peroxiredoxin_thiol_peroxidase_family_text"],
    ),
    (
        "peroxiredoxin_thiol_peroxidase",
        lambda c, row: _ec_has_prefix(row, _PEROXIREDOXIN_THIOL_PEROXIDASE_EC)
        and (
            c["peroxiredoxin_thiol_peroxidase_family_text"]
            or c["peroxiredoxin_thiol_peroxidase_thiol_context"]
        )
        and c["peroxiredoxin_thiol_peroxidase_reaction"]
        and not c["heme"]
        and not c["flavin"]
        and not c["peroxiredoxin_thiol_peroxidase_boundary_signal"]
        and not c["non_peroxiredoxin_thiol_peroxidase_scope_side_ec"],
    ),
    (
        "paps_sulfotransferase",
        lambda c, row: _ec_has_prefix(row, _PAPS_SULFOTRANSFERASE_EC)
        and c["paps_sulfotransferase_family_text"]
        and c["paps_sulfotransferase_reaction"]
        and not c["paps_sulfotransferase_boundary_signal"]
        and not c["non_paps_sulfotransferase_scope_side_ec"],
    ),
    (
        "glutathione_s_transferase",
        lambda c, row: _ec_has_prefix(row, _GLUTATHIONE_S_TRANSFERASE_EC)
        and c["glutathione_s_transferase_family_text"]
        and c["glutathione_s_transferase_reaction"]
        and not c["glutathione_s_transferase_boundary_signal"]
        and not c["non_glutathione_s_transferase_scope_side_ec"],
    ),
    (
        "aminoacyl_trna_synthetase",
        lambda c, row: _ec_has_prefix(row, _AMINOACYL_TRNA_SYNTHETASE_EC)
        and c["aminoacyl_trna_synthetase_family_text"]
        and c["aminoacyl_trna_synthetase_reaction"]
        and not c["aminoacyl_trna_synthetase_boundary_signal"]
        and not c["non_aminoacyl_trna_synthetase_scope_side_ec"],
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
        lambda c, row: c["metal"]
        and _ec_has_prefix(row, _METALLOPHOSPHOMONOESTERASE_EC)
        and not c["had_like_phosphatase_family_text"]
        and not c["ser_thr_protein_phosphatase_family_text"],
    ),
    (
        "metallo_beta_lactamase",
        lambda c, row: _ec_has_prefix(row, _METALLO_BETA_LACTAMASE_EC)
        and (
            c["metallo_beta_lactamase_family_text"]
            or c["metallo_beta_lactamase_zinc_context"]
        )
        and c["metallo_beta_lactamase_betalactam_reaction"]
        and not c["metallo_beta_lactamase_boundary_signal"]
        and not c["non_metallo_beta_lactamase_scope_side_ec"],
    ),
    (
        "metallo_amidohydrolase_deaminase",
        lambda c, row: c["metal"]
        and _ec_has_prefix(row, _METALLO_AMIDOHYDROLASE_DEAMINASE_EC)
        and not c["metallo_beta_lactamase_betalactam_reaction"],
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
        and _ec_has_prefix(row, _NAD_P_DEHYDROGENASE_EC)
        and not c["short_chain_dehydrogenase_reductase_family_text"]
        and not c["aldo_keto_reductase_family_text"],
    ),
    (
        "aldo_keto_reductase",
        lambda c, row: _ec_has_prefix(row, _ALDO_KETO_REDUCTASE_EC)
        and c["aldo_keto_reductase_family_text"]
        and c["aldo_keto_reductase_nad_p_context"]
        and c["aldo_keto_reductase_reaction"]
        and not c["aldo_keto_reductase_boundary_signal"]
        and not c["non_aldo_keto_reductase_scope_side_ec"],
    ),
    (
        "short_chain_dehydrogenase_reductase",
        lambda c, row: _ec_has_prefix(row, _SHORT_CHAIN_DEHYDROGENASE_REDUCTASE_EC)
        and c["short_chain_dehydrogenase_reductase_family_text"]
        and c["short_chain_dehydrogenase_reductase_nad_p_context"]
        and c["short_chain_dehydrogenase_reductase_reaction"]
        and not c["short_chain_dehydrogenase_reductase_boundary_signal"]
        and not c["aldehyde_dehydrogenase_family_text"]
        and not c["non_short_chain_dehydrogenase_reductase_scope_side_ec"],
    ),
    (
        "glycosyltransferase",
        lambda c, row: (c["sugar_nucleotide_donor"] or c["keyword_glycosyltransferase"])
        and _ec_has_prefix(row, _GLYCOSYLTRANSFERASE_EC),
    ),
    (
        "metal_independent_phosphodiesterase",
        lambda c, row: _ec_has_prefix(row, _METAL_INDEPENDENT_PHOSPHODIESTERASE_EC)
        and c["metal_independent_pde_family_text"]
        and c["metal_independent_pde_reaction"]
        and not c["metal_independent_pde_metal_boundary"]
        and not c["metal_independent_pde_boundary_signal"]
        and not c["kinase_boundary"]
        and not c["transferase_side_ec"]
        and not c["non_metal_independent_pde_scope_side_ec"],
    ),
    (
        "glycoside_hydrolase",
        lambda c, row: _ec_has_prefix(row, _GLYCOSIDE_HYDROLASE_EC)
        and c["glycoside_hydrolase_family_text"]
        and c["glycoside_hydrolysis_reaction"]
        and (
            c["active_or_binding_site_present"]
            or c["glycoside_hydrolase_active_site_context"]
        )
        and not c["glycoside_hydrolase_boundary_signal"]
        and not c["transferase_side_ec"]
        and not c["oxidoreductase_side_ec"]
        and not c["kinase_boundary"]
        and not c["non_glycoside_hydrolase_scope_side_ec"],
    ),
    (
        "n_ribosyl_hydrolase",
        lambda c, row: _ec_has_prefix(row, _N_RIBOSYL_HYDROLASE_EC)
        and c["n_ribosyl_hydrolase_family_text"]
        and c["n_ribosyl_hydrolysis_reaction"]
        and not c["n_ribosyl_hydrolase_boundary_signal"]
        and not c["glycoside_hydrolase_family_text"]
        and not c["transferase_side_ec"]
        and not c["kinase_boundary"]
        and not c["non_n_ribosyl_hydrolase_scope_side_ec"],
    ),
    (
        "sam_methyltransferase",
        lambda c, row: (c["sam_sah_methyl_donor"] or c["keyword_methyltransferase"])
        and not c["fe_s"]
        and not c["cx3cx2c_motif"]
        and _ec_has_prefix(row, _SAM_METHYLTRANSFERASE_EC),
    ),
    (
        "aminoglycoside_acetyltransferase",
        lambda c, row: _ec_has_prefix(row, _AMINOGLYCOSIDE_ACETYLTRANSFERASE_EC)
        and c["aminoglycoside_acetyltransferase_family_text"]
        and not c["hydrolase_side_ec"]
        and (
            c["coa_acyl_coa_reaction"]
            or c["coa_acyl_coa_feature"]
            or c["aminoglycoside_acetyltransferase_acetyl_coa_context"]
        )
        and not c["aminoglycoside_acetyltransferase_boundary_signal"]
        and not c["non_aminoglycoside_acetyltransferase_scope_side_ec"],
    ),
    (
        "coa_acyltransferase",
        lambda c, row: _ec_has_prefix(row, _COA_ACYLTRANSFERASE_EC)
        and not c["hydrolase_side_ec"]
        and c["keyword_acyltransferase"]
        and not c["aminoglycoside_acetyltransferase_family_text"]
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
        "manganese_iron_superoxide_dismutase",
        lambda c, row: _ec_has_prefix(row, _MN_FE_SUPEROXIDE_DISMUTASE_EC)
        and c["mn_fe_sod_family_or_name_context"]
        and c["mn_fe_sod_superoxide_dismutation_reaction"]
        and c["mn_fe_sod_metal_context"]
        and c["active_or_binding_site_present"]
        and not c["mn_fe_sod_boundary_signal"]
        and not c["non_mn_fe_sod_scope_side_ec"],
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
        "biotin_dependent_carboxylase",
        lambda c, row: _ec_has_prefix(row, _BIOTIN_DEPENDENT_CARBOXYLASE_EC)
        and c["biotin_carboxylation_reaction"]
        and c["biotin_carboxylase_text"]
        and (
            c["biotin_feature_or_ligand"]
            or c["biotin_keyword_or_name"]
            or c["active_or_binding_site_present"]
        )
        and not c["kinase_boundary"]
        and not c["hydrolase_side_ec"]
        and not c["transferase_side_ec"]
        and not c["non_biotin_carboxylase_scope_side_ec"]
        and not c["plp_boundary_signal"]
        and not c["thdp_boundary_signal"]
        and not c["molybdopterin_moco"]
        and not c["heme"]
        and not c["flavin"],
    ),
    (
        "nucleoside_diphosphate_kinase",
        lambda c, row: _ec_has_prefix(row, _NUCLEOSIDE_DIPHOSPHATE_KINASE_EC)
        and c["ndk_family_text"]
        and c["ndk_ntp_ndp_reaction"]
        and (c["ndk_active_his_context"] or c["active_or_binding_site_present"])
        and not c["ndk_protein_kinase_boundary"]
        and not c["ndk_two_component_histidine_kinase_boundary"]
        and not c["ndk_hydrolase_nuclease_side_ec_boundary"]
        and not c["ndk_other_nmp_kinase_side_ec_boundary"],
    ),
    (
        "askha_sugar_acetate_kinase",
        lambda c, row: _ec_has_prefix(row, _ASKHA_SUGAR_ACETATE_KINASE_EC)
        and c["askha_family_text"]
        and c["askha_phosphoryl_reaction"]
        and c["askha_atp_mg_context"]
        and c["active_or_binding_site_present"]
        and not c["askha_protein_kinase_boundary"]
        and not c["askha_histidine_kinase_boundary"]
        and not c["askha_hydrolase_side_ec_boundary"]
        and not c["askha_ndk_boundary"]
        and not c["askha_dnk_boundary"]
        and not c["askha_ghmp_boundary"]
        and not c["askha_pfk_boundary"]
        and not c["non_askha_scope_side_ec"],
    ),
    (
        "ghmp_small_molecule_kinase",
        lambda c, row: _ec_has_prefix(row, _GHMP_SMALL_MOLECULE_KINASE_EC)
        and c["ghmp_family_text"]
        and c["ghmp_phosphoryl_reaction"]
        and c["ghmp_atp_mg_context"]
        and c["active_or_binding_site_present"]
        and not c["ghmp_protein_kinase_boundary"]
        and not c["ghmp_histidine_kinase_boundary"]
        and not c["ghmp_hydrolase_side_ec_boundary"]
        and not c["ghmp_ndk_boundary"]
        and not c["ghmp_dnk_boundary"]
        and not c["ghmp_askha_boundary"]
        and not c["ghmp_pfk_boundary"]
        and not c["non_ghmp_scope_side_ec"],
    ),
    (
        "deoxynucleoside_kinase",
        lambda c, row: _ec_has_prefix(row, _DEOXYNUCLEOSIDE_KINASE_EC)
        and c["dnk_family_text"]
        and c["dnk_phosphoryl_reaction"]
        and c["dnk_atp_mg_context"]
        and c["active_or_binding_site_present"]
        and not c["dnk_protein_kinase_boundary"]
        and not c["dnk_histidine_kinase_boundary"]
        and not c["dnk_hydrolase_side_ec_boundary"]
        and not c["dnk_ndk_boundary"]
        and not c["dnk_askha_boundary"]
        and not c["dnk_ghmp_boundary"]
        and not c["dnk_pfk_boundary"]
        and not c["non_dnk_scope_side_ec"],
    ),
    (
        "pfka_phosphofructokinase",
        lambda c, row: _ec_has_prefix(row, _PFKA_PHOSPHOFRUCTOKINASE_EC)
        and c["pfka_family_text"]
        and c["pfka_phosphoryl_reaction"]
        and c["pfka_atp_mg_context"]
        and c["active_or_binding_site_present"]
        and not c["pfka_protein_kinase_boundary"]
        and not c["pfka_histidine_kinase_boundary"]
        and not c["pfka_hydrolase_side_ec_boundary"]
        and not c["pfka_ndk_boundary"]
        and not c["pfka_dnk_boundary"]
        and not c["pfka_askha_boundary"]
        and not c["pfka_ghmp_boundary"]
        and not c["pfka_pfkb_boundary"]
        and not c["non_pfka_scope_side_ec"],
    ),
    (
        "pfkb_ribokinase_family",
        lambda c, row: _ec_has_prefix(row, _PFKB_RIBOKINASE_FAMILY_EC)
        and c["pfkb_family_text"]
        and c["pfkb_phosphoryl_reaction"]
        and c["pfkb_atp_mg_context"]
        and c["active_or_binding_site_present"]
        and not c["pfkb_protein_kinase_boundary"]
        and not c["pfkb_histidine_kinase_boundary"]
        and not c["pfkb_hydrolase_side_ec_boundary"]
        and not c["pfkb_ndk_boundary"]
        and not c["pfkb_dnk_boundary"]
        and not c["pfkb_askha_boundary"]
        and not c["pfkb_ghmp_boundary"]
        and not c["pfkb_pfka_boundary"]
        and not c["non_pfkb_scope_side_ec"],
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
    (
        "terpene_cyclase_synthase",
        lambda c, row: _ec_has_prefix(row, _TERPENE_CYCLASE_SYNTHASE_EC)
        and c["terpene_family_text"]
        and (c["terpene_mg_mn_context"] or c["terpene_diphosphate_context"])
        and not c["plp_boundary_signal"]
        and not c["thdp_boundary_signal"]
        and not c["zinc_feature_or_ligand"]
        and not c["hydrolase_side_ec"]
        and not c["transferase_side_ec"]
        and not c["oxidoreductase_side_ec"]
        and not c["keyword_isomerase"]
        and not c["terpene_boundary_signal"]
        and not c["non_4_2_3_side_ec"]
        and (c["terpene_cyclization_reaction"] or c["active_or_binding_site_present"]),
    ),
    (
        "protein_kinase_ser_thr_tyr",
        lambda c, row: _ec_has_prefix(row, _PROTEIN_KINASE_SER_THR_TYR_EC)
        and c["protein_kinase_family_text"]
        and c["protein_kinase_atp_mg_context"]
        and not c["protein_kinase_boundary_signal"]
        and not c["hydrolase_side_ec"]
        and not c["non_protein_kinase_scope_side_ec"]
        and (
            c["protein_kinase_phosphoryl_reaction"]
            or c["active_or_binding_site_present"]
        ),
    ),
    (
        "aminoglycoside_phosphotransferase",
        lambda c, row: _ec_has_exact(row, _AMINOGLYCOSIDE_PHOSPHOTRANSFERASE_EC)
        and c["aminoglycoside_phosphotransferase_family_text"]
        and (
            c["aminoglycoside_phosphotransferase_atp_mg_context"]
            or c["active_or_binding_site_present"]
            or c["aminoglycoside_phosphotransferase_phosphoryl_reaction"]
        )
        and (
            c["aminoglycoside_phosphotransferase_phosphoryl_reaction"]
            or c["active_or_binding_site_present"]
        )
        and not c["aminoglycoside_phosphotransferase_boundary_signal"]
        and not c["protein_kinase_family_text"]
        and not c["askha_family_text"]
        and not c["ghmp_family_text"]
        and not c["dnk_family_text"]
        and not c["pfka_family_text"]
        and not c["pfkb_family_text"]
        and not c["non_aminoglycoside_phosphotransferase_scope_side_ec"],
    ),
    (
        "had_like_phosphatase",
        lambda c, row: _ec_has_prefix(row, _HAD_LIKE_PHOSPHATASE_EC)
        and c["had_like_phosphatase_family_text"]
        and not c["had_like_phosphatase_boundary_signal"]
        and not c["non_had_like_phosphatase_scope_side_ec"]
        and not c["kinase_boundary"]
        and not c["transferase_side_ec"]
        and (
            c["had_like_phosphatase_asp_mg_context"]
            or c["active_or_binding_site_present"]
        )
        and (
            c["had_like_phosphatase_phosphomonoester_reaction"]
            or c["active_or_binding_site_present"]
        ),
    ),
    (
        "ser_thr_protein_phosphatase",
        lambda c, row: _ec_has_prefix(row, _SER_THR_PROTEIN_PHOSPHATASE_EC)
        and c["ser_thr_protein_phosphatase_family_text"]
        and c["ser_thr_protein_phosphatase_metal_context"]
        and c["ser_thr_protein_phosphatase_dephosphorylation_reaction"]
        and not c["ser_thr_protein_phosphatase_boundary_signal"]
        and not c["ser_thr_protein_phosphatase_cys_ptp_boundary"]
        and not c["had_like_phosphatase_family_text"]
        and not c["kinase_boundary"]
        and not c["transferase_side_ec"]
        and not c["non_ser_thr_protein_phosphatase_scope_side_ec"],
    ),
    (
        "aldehyde_dehydrogenase",
        lambda c, row: _ec_has_prefix(row, _ALDEHYDE_DEHYDROGENASE_EC)
        and c["aldehyde_dehydrogenase_family_text"]
        and c["aldehyde_dehydrogenase_nad_p_context"]
        and c["aldehyde_dehydrogenase_reaction"]
        and not c["aldehyde_dehydrogenase_boundary_signal"]
        and not c["generic_nad_p_dehydrogenase_boundary"]
        and not c["non_aldehyde_dehydrogenase_scope_side_ec"],
    ),
    (
        "alpha_beta_hydrolase_esterase_lipase",
        lambda c, row: _ec_has_prefix(row, _ALPHA_BETA_HYDROLASE_ESTERASE_LIPASE_EC)
        and c["alpha_beta_hydrolase_family_text"]
        and c["alpha_beta_hydrolase_ser_his_acid_context"]
        and c["alpha_beta_hydrolase_ester_hydrolysis_reaction"]
        and not c["alpha_beta_hydrolase_boundary_signal"]
        and not c["glycoside_hydrolase_family_text"]
        and not c["non_alpha_beta_hydrolase_scope_side_ec"],
    ),
    (
        "serine_beta_lactamase",
        lambda c, row: _ec_has_exact(row, _SERINE_BETA_LACTAMASE_EC)
        and c["serine_beta_lactamase_family_text"]
        and c["serine_beta_lactamase_hydrolysis_reaction"]
        and c["serine_beta_lactamase_active_site_context"]
        and not c["serine_beta_lactamase_boundary_signal"]
        and not c["alpha_beta_hydrolase_family_text"]
        and not c["non_serine_beta_lactamase_scope_side_ec"],
    ),
)


def disambiguate_row(row: dict[str, Any], *, source_tier: str = "source_tier_0") -> dict[str, Any]:
    """Assign a fingerprint only when exactly one rule fires (else stay held).

    Scope is selected by the EC-prefix predicate; membership is CONFIRMED by a mechanism
    corroborator (cofactor OR cosubstrate/Rhea participant OR functional keyword OR
    active-site/binding residue). The trust-tier N-of-M rule
    (`source_trust_tiers.evaluate_corroboration`) must ADMIT before the row can be built into
    a label. Tier 0 requires at least one counted MECHANISM axis; tier 2 requires three
    independent mechanism axes. EC is a scope hint and never counts toward N-of-M.
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
    corroboration = evaluate_corroboration(source_tier=source_tier, present_axes=present_axes)
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
    elif fingerprint == "biotin_dependent_carboxylase" and evidence.get("biotin_feature_or_ligand"):
        records = [{"name": "biotin", "cross_reference": {"id": None}}]
    elif fingerprint == "nucleoside_diphosphate_kinase" and evidence.get("ndk_ntp_ndp_reaction"):
        records = [{"name": "nucleoside triphosphate/diphosphate", "cross_reference": {"id": None}}]
    elif fingerprint == "askha_sugar_acetate_kinase" and evidence.get("askha_atp_mg_context"):
        records = [{"name": "ATP/Mg2+ phosphoryl-transfer cosubstrate", "cross_reference": {"id": None}}]
    elif fingerprint == "ghmp_small_molecule_kinase" and evidence.get("ghmp_atp_mg_context"):
        records = [{"name": "ATP/Mg2+ GHMP phosphoryl-transfer cosubstrate", "cross_reference": {"id": None}}]
    elif fingerprint == "deoxynucleoside_kinase" and evidence.get("dnk_atp_mg_context"):
        records = [{"name": "ATP/Mg2+ deoxynucleoside phosphoryl-transfer cosubstrate", "cross_reference": {"id": None}}]
    elif fingerprint == "pfka_phosphofructokinase" and evidence.get("pfka_atp_mg_context"):
        records = [{"name": "ATP/Mg2+ fructose-6-phosphate phosphoryl-transfer cosubstrate", "cross_reference": {"id": None}}]
    elif fingerprint == "pfkb_ribokinase_family" and evidence.get("pfkb_atp_mg_context"):
        records = [{"name": "ATP/Mg2+ PfkB/ribokinase-family phosphoryl-transfer cosubstrate", "cross_reference": {"id": None}}]
    elif fingerprint == "manganese_iron_superoxide_dismutase" and evidence.get("mn_fe_sod_metal_context"):
        records = [{"name": "manganese/iron catalytic redox metal", "cross_reference": {"id": None}}]
    elif fingerprint == "terpene_cyclase_synthase" and (
        evidence.get("terpene_mg_mn_context") or evidence.get("terpene_diphosphate_context")
    ):
        records = [{"name": "Mg2+/Mn2+ prenyl-diphosphate cyclization context", "cross_reference": {"id": None}}]
    elif fingerprint == "protein_kinase_ser_thr_tyr" and evidence.get("protein_kinase_atp_mg_context"):
        records = [{"name": "ATP/Mg2+ protein-substrate phosphoryl-transfer cosubstrate", "cross_reference": {"id": None}}]
    elif fingerprint == "aminoglycoside_acetyltransferase" and (
        evidence.get("coa_acyl_coa_reaction")
        or evidence.get("coa_acyl_coa_feature")
        or evidence.get("aminoglycoside_acetyltransferase_acetyl_coa_context")
    ):
        records = [
            {
                "name": "acetyl-CoA aminoglycoside N-acetyltransferase context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "aminoglycoside_phosphotransferase" and (
        evidence.get("aminoglycoside_phosphotransferase_atp_mg_context")
        or evidence.get("aminoglycoside_phosphotransferase_phosphoryl_reaction")
    ):
        records = [
            {
                "name": "ATP/Mg2+ aminoglycoside phosphoryl-transfer context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "had_like_phosphatase" and (
        evidence.get("had_like_phosphatase_asp_mg_context")
        or evidence.get("had_like_phosphatase_phosphomonoester_reaction")
    ):
        records = [{"name": "Mg2+/Asp phosphoenzyme phosphomonoesterase context", "cross_reference": {"id": None}}]
    elif fingerprint == "ser_thr_protein_phosphatase" and (
        evidence.get("ser_thr_protein_phosphatase_metal_context")
        or evidence.get("ser_thr_protein_phosphatase_dephosphorylation_reaction")
    ):
        records = [
            {
                "name": "dinuclear metal protein-substrate dephosphorylation context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "aldehyde_dehydrogenase" and evidence.get("aldehyde_dehydrogenase_nad_p_context"):
        records = [{"name": "NAD(P)+ aldehyde dehydrogenase cosubstrate", "cross_reference": {"id": None}}]
    elif fingerprint == "short_chain_dehydrogenase_reductase" and (
        evidence.get("short_chain_dehydrogenase_reductase_nad_p_context")
        or evidence.get("short_chain_dehydrogenase_reductase_reaction")
    ):
        records = [
            {
                "name": "NAD(P)+ short-chain dehydrogenase/reductase context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "aldo_keto_reductase" and (
        evidence.get("aldo_keto_reductase_nad_p_context")
        or evidence.get("aldo_keto_reductase_reaction")
    ):
        records = [
            {
                "name": "NADP(H) aldo-keto reductase carbonyl-reduction context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "alpha_beta_hydrolase_esterase_lipase" and (
        evidence.get("alpha_beta_hydrolase_ser_his_acid_context")
        or evidence.get("alpha_beta_hydrolase_ester_hydrolysis_reaction")
    ):
        records = [{"name": "Ser-His-Asp/Glu ester-hydrolysis context", "cross_reference": {"id": None}}]
    elif fingerprint == "serine_beta_lactamase" and (
        evidence.get("serine_beta_lactamase_hydrolysis_reaction")
        or evidence.get("serine_beta_lactamase_active_site_context")
    ):
        records = [
            {
                "name": "Ser/Lys/Glu beta-lactam acyl-enzyme hydrolysis context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "metallo_beta_lactamase" and (
        evidence.get("metallo_beta_lactamase_zinc_context")
        or evidence.get("metallo_beta_lactamase_betalactam_reaction")
    ):
        records = [
            {
                "name": "Zn2+ metallo-beta-lactamase ring-hydrolysis context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "peroxiredoxin_thiol_peroxidase" and (
        evidence.get("peroxiredoxin_thiol_peroxidase_thiol_context")
        or evidence.get("peroxiredoxin_thiol_peroxidase_reaction")
    ):
        records = [
            {
                "name": "peroxidatic cysteine/selenocysteine thiol-redox peroxide-reduction context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "paps_sulfotransferase" and evidence.get(
        "paps_sulfotransferase_reaction"
    ):
        records = [
            {
                "name": "3'-phosphoadenylyl sulfate (PAPS) sulfuryl-transfer cosubstrate context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "glutathione_s_transferase" and evidence.get(
        "glutathione_s_transferase_reaction"
    ):
        records = [
            {
                "name": "glutathione conjugation (GSH thiolate -> S-substituted glutathione) cosubstrate context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "aminoacyl_trna_synthetase" and evidence.get(
        "aminoacyl_trna_synthetase_reaction"
    ):
        records = [
            {
                "name": "ATP-dependent aminoacyl-tRNA synthetase (aminoacyl-adenylate -> aminoacyl-tRNA) cosubstrate context",
                "cross_reference": {"id": None},
            }
        ]
    elif fingerprint == "n_ribosyl_hydrolase" and (
        evidence.get("n_ribosyl_hydrolysis_reaction")
        or evidence.get("n_ribosyl_active_site_context")
    ):
        records = [{"name": "N-glycosidic bond hydrolysis context", "cross_reference": {"id": None}}]
    elif fingerprint == "metal_independent_phosphodiesterase" and (
        evidence.get("metal_independent_pde_reaction")
        or evidence.get("metal_independent_pde_active_site_context")
    ):
        records = [{"name": "metal-independent phosphodiester hydrolysis context", "cross_reference": {"id": None}}]
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
    source_tier: str = "source_tier_0",
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
            verdict = disambiguate_row(raw, source_tier=source_tier)
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
                "source_tier": source_tier,
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
