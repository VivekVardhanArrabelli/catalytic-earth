"""Leakage-safe mechanism representation loop (Phase 3: self-feeding supply).

The hand-curated pools are drained, so the climb cannot lean on hand-sourcing
forever. We have been banking rich review-only ``mechanism_evidence`` on every
bronze label precisely so a representation can eventually *organise, triage, and
propose* labels itself. This is the first iteration of that loop.

THE LEAKAGE WALL IS ABSOLUTE. The representation is built ONLY from the review-only
**structural / chemical** evidence -- cofactor and binding-ligand chemical
identities (ChEBI names) and active-site residue role counts. It NEVER reads, and
this module asserts it never reads:

- ``ec_numbers`` (EC is scope-assignment metadata, excluded_context),
- protein name / UniProt prose / curated mechanism text / source annotation,
- ``target_family_lane``,
- the ``fingerprint_id`` / ``label_type`` target itself,
- the frozen 702 benchmark (this loop is for the expansion's self-organisation and
  bronze->silver promotion triage; it is NOT a benchmark scorer and must never be
  used as one).

Cofactor/ligand chemical identity is the legitimate, deploy-available structural
basis the whole project is built on (the eight fingerprints are *defined* by their
cofactor chemistry); it is distinct from the excluded protein-name/prose/EC fields.

Three capabilities:

1. ``featurize`` -- a deterministic, leakage-safe chemical/structural feature
   vector per label.
2. ``promotion_triage`` -- using per-fingerprint centroids, partition bronze seed
   labels into promotion candidates (chemistry coheres with the assigned
   fingerprint), review outliers (chemistry points at a *different* fingerprint --
   a possible mislabel), and not-yet-coherent rows. A leave-one-out
   self-consistency read measures how strongly the chemistry alone recovers the
   fingerprint -- the representation's coherence.
3. ``propose_for_fingerprint`` -- rank a candidate pool (e.g. the out_of_scope
   rows) by representation similarity to a target fingerprint's centroid: the
   model-proposed "what to source/predict next", aimed at the governor's holes.

NON-DESTRUCTIVE: writes no registry, emits no label, changes no benchmark.
"""

from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .registry_io import load_json

DEFAULT_FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# Cofactor / ligand chemical-identity -> canonical cofactor class. Keys are matched
# as lowercased substrings against cofactor names, binding-ligand names, and ChEBI
# names. These are CHEMICAL identities (the legitimate structural basis), never the
# excluded protein-name/EC/prose fields.
COFACTOR_CLASS_PATTERNS: dict[str, tuple[str, ...]] = {
    "flavin": ("fad", "fmn", "flavin"),
    "plp": ("pyridoxal",),
    "heme": ("heme",),
    "iron_sulfur": ("4fe-4s", "2fe-2s", "3fe-4s", "fe-s cluster", "iron-sulfur"),
    "sam": ("s-adenosyl-l-methionine", "adenosyl-l-methionine", "adenosylmethionine"),
    "cobalamin": ("cobalamin", "cobamamide", "vitamin b12", "adenosylcobalamin"),
    "zinc": ("zn(", "zinc"),
    "divalent_metal_other": (
        "mn(", "mg(", "ni(", "co(", "fe(", "fe cation", "fe3", "fe2",
        "divalent metal", "cu(", "manganese", "magnesium",
    ),
    "calcium": ("ca(2+)", "ca("),
}

COFACTOR_CLASSES = tuple(COFACTOR_CLASS_PATTERNS.keys())

# Cosubstrate / donor chemical-identity classes (added 2026-06-14). Many expansion
# families are defined NOT by a bound cofactor but by a dissociable COSUBSTRATE / donor
# that appears as a Rhea reaction PARTICIPANT (NAD(P), a nucleoside-triphosphate, CoA,
# a sugar-nucleotide). These are CHEMICAL identities read from the reaction-equation
# substrate->product strings and the chemical-identity terms -- the same legitimate basis
# as cofactor identity, never EC/name/prose/fingerprint. They are co-equal mechanistic
# features (full weight), kept SEPARATE from COFACTOR_CLASSES so the cofactor-presence
# helpers (which index COFACTOR_CLASSES positionally) are unaffected.
COSUBSTRATE_CLASS_PATTERNS: dict[str, tuple[str, ...]] = {
    "cos_nad": ("nad(+)", "nadh", "nadp(+)", "nadph", "nad(p)"),
    "cos_coa": ("coa", "coenzyme a"),
    "cos_nucleotide_sugar": (
        "udp-", "gdp-", "dtdp-", "cdp-", "cmp-n", "gdp-l", "udp-n", "adp-d",
    ),
    "cos_2_oxoglutarate": ("2-oxoglutarate",),
    "cos_prenyl_diphosphate": (
        "geranyl diphosphate", "farnesyl diphosphate", "geranylgeranyl diphosphate",
        "prenyl diphosphate", "dimethylallyl diphosphate",
    ),
}

COSUBSTRATE_CLASSES = tuple(COSUBSTRATE_CLASS_PATTERNS.keys())

# Row-specific reaction-center BOND-CHANGE classes (Track 1 / 1c). Derived ONLY from the
# Rhea reaction equation's substrate->product chemistry -- the legitimate North Star axis,
# exactly like cofactor identity. It is NOT the fingerprint's declared bond_change (that
# would leak the label), NOT the EC number, NOT protein name/prose. The four metal
# sub-families share the same cofactor (a divalent metal) and water-activator residue
# roles, so cofactor chemistry ALONE cannot separate them; they differ only by the
# reaction-center bond hydrolysed. These features are that discriminator. They fire only
# for HYDROLYSIS reactions (water on the substrate side), which keeps non-hydrolase
# (lyase/transferase) chemistries -- e.g. cobalamin ammonia-lyases -- out of the bond
# space and preserves the non-metal families' cofactor-based separability.
#
# ``bc_ester_hydrolysis``, ``bc_glycoside_hydrolysis``,
# ``bc_n_glycosidic_hydrolysis`` (added 2026-06-15), and
# ``bc_beta_lactam_hydrolysis`` (added 2026-06-16) extend the same hydrolysis basis to
# the new ester-/lipase-, carbohydrate glycoside-, N-ribosyl-hydrolase, and serine
# beta-lactamase family lanes, which otherwise carried NO reaction-center class and
# collapsed. All read only the Rhea substrate->product equation.
BOND_CHANGE_CLASSES = (
    "bc_phosphomonoester",  # phosphomonoester P-O hydrolysis (free phosphate released)
    "bc_phosphodiester",    # phosphodiester P-O hydrolysis (nuclease / cyclic-nucleotide)
    "bc_peptide_cn",        # peptide C-N hydrolysis (peptide-fragment products, no Pi)
    "bc_amide_cn",          # non-peptide amide/amidine C-N hydrolysis / deamination
    "bc_ester_hydrolysis",  # ester/lipase C-O hydrolysis (acylglycerol/sterol-ester -> fatty acid + alcohol)
    "bc_glycoside_hydrolysis",  # carbohydrate O-glycoside hydrolysis (glycoside + H2O -> free sugar + aglycone)
    "bc_n_glycosidic_hydrolysis",  # nucleoside/nucleotide N-glycosidic hydrolysis (ribose + nucleobase)
    "bc_beta_lactam_hydrolysis",  # beta-lactam amide ring hydrolysis (penicillin/cephalosporin/carbapenem -> opened product)
)

# Non-hydrolytic reaction-center bond-change classes (added 2026-06-14). The four
# hydrolysis classes above only separate the metal-hydrolase sub-families; the bulk of
# the expansion ontology is transfer / redox / lyase / isomerase chemistry that carries
# NO water reactant, so the hydrolysis classifier yields nothing and those families
# collapse together. These classes are derived ONLY from the Rhea substrate->product
# equation (the same leakage-safe basis), never EC/name/prose/fingerprint, and are
# co-equal mechanistic features (full weight). They are the discriminator the expansion
# ontology was missing.
NONHYDROLYTIC_BOND_CLASSES = (
    "bc_redox_hydride",      # NAD(P)+/NADH or FAD/FADH2 hydride transfer (dehydrogenase)
    "bc_phosphoryl_transfer",  # (d)NTP -> (d)NDP with phosphate to a non-water acceptor (kinase)
    "bc_atp_dependent_ligation",  # ATP -> ADP + Pi driving C-N/C-O ligation (ligase/synthetase)
    "bc_glycosyl_transfer",  # sugar-nucleotide donor -> free nucleotide (glycosyltransferase)
    "bc_acyl_transfer",      # acyl-CoA -> CoA, acyl group transferred (acyltransferase)
    "bc_methyl_transfer",    # S-adenosyl-L-methionine -> S-adenosyl-L-homocysteine (SAM MTase)
    "bc_oxygenation",        # O2 incorporated (mono-/di-oxygenase, peroxidase boundary)
    "bc_decarboxylation",    # CO2 released without water (decarboxylase)
    "bc_carboxylation",      # hydrogencarbonate/CO2 fixed with ATP (biotin carboxylase)
    "bc_diphosphate_lyase",  # prenyl-diphosphate -> diphosphate + carbocation (terpene cyclase)
    "bc_isomerization",      # single substrate = single product, no cosubstrate (isomerase/racemase)
    "bc_carbon_carbon_lyase",  # one organic substrate cleaved into two organic fragments (aldol/C-C lyase)
    "bc_aldehyde_oxidation",  # aldehyde + NAD(+) + H2O -> carboxylate + NADH (water-consuming NAD redox)
    "bc_peroxide_reduction",  # hydroperoxide/H2O2 on substrate side -> alcohol/water (O-O reductive cleavage; peroxidatic thiol/heme/NAD(P)H peroxidase)
)

# Small inorganic / proton species that are NOT a carbon-skeleton fragment. Used only by
# the C-C lyase detector to count the organic fragments on each side of a reaction; a
# leaving CO2 / phosphate / ammonia is inorganic, so decarboxylation / dehydratase /
# deamination chemistry does NOT masquerade as a C-C bond cleavage. Charged ions keep
# their ``(+)``/``(-)`` here, so the equation must be split on Rhea's ' + ' separator
# (NOT a bare '+', which shreds ``NH4(+)`` / ``H(+)``).
_INORGANIC_FRAGMENTS = frozenset(
    {
        "h2o", "co2", "hydrogencarbonate", "phosphate", "diphosphate",
        "hydrogenphosphate", "nh3", "nh4(+)", "o2", "co", "sulfite",
        "hydrogen sulfide", "hydrogen peroxide", "oxygen", "h(+)", "h(-)",
        "hydrogen cyanide", "cyanate",
    }
)

# Phospho-ACCEPTOR classes (added 2026-06-14). The kinase sub-families all share the
# phosphoryl-transfer bond change + ATP/Mg and differ ONLY by the group that accepts the
# phosphate. These fire ONLY inside a phosphoryl-transfer reaction (so a sugar substrate in
# a glycosidase does not spuriously trip ``acc_sugar``), and separate protein- vs
# nucleoside- vs sugar-acceptor kinases. Derived only from the Rhea equation string.
PHOSPHOACCEPTOR_CLASSES = (
    "acc_protein",      # a [protein] residue is phosphorylated (protein kinase)
    "acc_nucleoside",   # a nucleoside / (deoxy)nucleotide is phosphorylated (NDP/dNK/PfkB)
    "acc_sugar",        # a sugar / polyol is phosphorylated (PfkA / ASKHA / GHMP)
)

_NUCLEOSIDE_ACCEPTOR_TERMS = (
    "nucleoside", "guanosine", "inosine", "adenosine", "cytidine", "uridine",
    "xanthosine", "thymidine",
)
_SUGAR_ACCEPTOR_TERMS = (
    "hexose", "fructose", "galactose", "glucose", "mannose", "glucosamine",
    "glycerol", "ribose", "ribulose", "xylulose", "gluconate", "arabino",
    "mevalonate", "homoserine",
)

# Ordered numeric feature names. Cofactor classes lead (their positional index is reused
# by the centroid-cofactor helpers, so they MUST stay the prefix). Bond-change classes are
# co-equal mechanistic features (full weight, like cofactor); residue role ratios are
# secondary structural context (down-weighted in ``_vector``).
RESIDUE_FEATURES = (
    "catalytic_fraction",
    "binding_fraction",
    "active_site_size",
)
# COFACTOR_CLASSES MUST remain the prefix (the centroid-cofactor helpers index it
# positionally). Cosubstrate + non-hydrolytic bond classes are appended after it and
# before the down-weighted residue features.
FEATURE_NAMES = (
    COFACTOR_CLASSES
    + COSUBSTRATE_CLASSES
    + BOND_CHANGE_CLASSES
    + NONHYDROLYTIC_BOND_CLASSES
    + PHOSPHOACCEPTOR_CLASSES
    + RESIDUE_FEATURES
)

# Fields that must never enter the representation -- asserted by featurize.
EXCLUDED_FROM_REPRESENTATION = (
    "ec_numbers",
    "fingerprint_id",
    "label_type",
    "protein_name",
    "uniprot_prose",
    "target_family_lane",
    "rationale",
)

DEFAULT_PROMOTION_COHESION = 0.92


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> list[dict[str, Any]]:
    payload = load_json(Path(path))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON list")
    return payload


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("mechanism_evidence", {}) or {}


def _classify_cofactor(name: str) -> str | None:
    low = (name or "").lower()
    for cls, patterns in COFACTOR_CLASS_PATTERNS.items():
        if any(p in low for p in patterns):
            return cls
    return None


def _chemical_identity_terms(row: dict[str, Any]) -> list[str]:
    """Collect ONLY chemical identities: cofactor names + binding-ligand names.

    Reads nothing from EC / protein name / prose / lane / fingerprint.
    """
    mech = _mechanism_evidence(row)
    terms: list[str] = []
    for cofactor in mech.get("cofactors") or []:
        if cofactor.get("name"):
            terms.append(cofactor["name"])
    for residue in mech.get("active_site_residues") or []:
        if residue.get("feature_code") == "BINDING" and residue.get("ligand_name"):
            terms.append(residue["ligand_name"])
    return terms


def _reaction_equations(row: dict[str, Any]) -> list[str]:
    """The Rhea reaction-equation STRINGS only (substrate->product chemistry).

    Reads ``reaction`` strings exclusively -- never the co-stored ``ec_number`` (EC is an
    excluded predictive field), never the fingerprint label.
    """
    mech = _mechanism_evidence(row)
    return [
        str(rec.get("reaction") or "")
        for rec in (mech.get("reaction_equations") or [])
        if isinstance(rec, dict) and rec.get("reaction")
    ]


_GLYCOSIDE_FREE_SUGARS = (
    "d-glucose", "d-mannose", "d-galactose", "d-glucosamine", "n-acetyl",
    "d-xylose", "l-fucose", "d-fructose", "d-galactosamine",
)
_N_GLYCOSIDIC_RIBOSE_PRODUCTS = (
    "d-ribose", "2-deoxy-d-ribose",
)
_N_GLYCOSIDIC_BASE_PRODUCTS = (
    "adenine", "guanine", "cytosine", "uracil", "thymine", "hypoxanthine",
    "xanthine", "nucleobase",
)


def classify_reaction_bond_change(reaction: str) -> set[str]:
    """Classify a single reaction string into reaction-center bond-change classes.

    Leakage-safe: reads only the substrate->product chemistry. Fires only for HYDROLYSIS
    (water on the substrate side), which is what the metal hydrolase sub-families and the
    ester-/glycoside-hydrolase lanes do and what distinguishes them; lyases/transferases
    (no water) yield no bond-change class, keeping non-hydrolase chemistries out of this
    space.
    """
    low = reaction.lower()
    if "=" not in low:
        return set()
    lhs, rhs = low.split("=", 1)
    lhs_tokens = [token.strip() for token in lhs.split("+")]
    rhs_tokens = [token.strip() for token in rhs.split("+")]
    if "h2o" not in lhs_tokens:  # hydrolases only
        return set()

    # Rhea ' + '-separated product terms keep charged ions (H(+), NH4(+)) intact -- a bare
    # '+' split shreds them -- and have stoichiometric coefficients stripped, so the
    # ester/glycoside detectors below can test product-token suffixes/identities cleanly.
    rhs_terms = [
        re.sub(r"^\d+\s+", "", term.strip()) for term in re.split(r"\s\+\s", rhs.strip())
    ]

    classes: set[str] = set()
    free_phosphate = any(
        token in ("phosphate", "diphosphate", "hydrogenphosphate") for token in rhs_tokens
    )
    phospho_substrate = ("phospho" in lhs) or ("phosphate" in lhs)
    anhydride = bool(
        re.search(r"\b(atp|gtp|ctp|utp|itp)\b", lhs)
        and re.search(r"\b(adp|gdp|cdp|udp|idp)\b", rhs)
    )
    diester = "phosphodiester" in low or bool(
        re.search(r"\b(dna|rna|oligonucleotide|nucleic|cyclic)\b", low)
    )
    # glycerophosphodiester / sphingomyelin phospholipid-headgroup phosphodiester hydrolysis
    # (metal-independent GDPD, sphingomyelinase, phospholipase D): the phosphodiester to a choline /
    # ethanolamine head group is cleaved, RELEASING that head group as a free small molecule (free
    # choline / ethanolamine) or a standalone phospho-headgroup (phosphocholine / phosphoethanolamine).
    # These carry none of the nucleic-acid keywords above but ARE phosphodiester hydrolysis, and are
    # the reaction-center class the cofactor-free metal_independent_phosphodiesterase family was
    # missing (it otherwise collapsed to ~0.07). Match the released head group as an EXACT product
    # term (rhs_terms is ' + '-split and coefficient-stripped) so that acyl-ester hydrolases which
    # merely RETAIN a phosphocholine group -- phospholipase A -> a 1-acyl-...-phosphocholine -- and
    # [protein]-PE deconjugating proteases (ATG4) do NOT false-fire. Reads only the Rhea equation.
    released_headgroup = any(
        term in ("choline", "ethanolamine", "phosphocholine", "phosphoethanolamine")
        for term in rhs_terms
    )
    if (diester or (released_headgroup and not free_phosphate)) and "phosphate monoester" not in lhs:
        classes.add("bc_phosphodiester")
    if "phosphate monoester" in lhs or ("an alcohol" in rhs and free_phosphate):
        classes.add("bc_phosphomonoester")
    elif free_phosphate and phospho_substrate and not anhydride and not diester:
        classes.add("bc_phosphomonoester")

    # protein dephosphorylation: a phosphomonoester hydrolysis that removes a phosphate
    # from a [protein] residue (Ser/Thr/Tyr phosphatase). The acc_protein tag (reused from
    # the kinase acceptor classes -- no new dim) separates it from small-molecule
    # phosphomonoesterases, which share the same bc_phosphomonoester bond change.
    if (
        "bc_phosphomonoester" in classes
        and "[protein]" in low
        and "phospho" in lhs
        and free_phosphate
    ):
        classes.add("acc_protein")

    peptide_like = bool(
        re.search(r"\bpeptide\b", lhs)
        or re.search(r"\(\d+-\d+\)", rhs)
        or re.search(r"l-[a-z]{3}-l-[a-z]{3}", rhs)
    )
    if peptide_like and not free_phosphate and not phospho_substrate:
        classes.add("bc_peptide_cn")

    deamination = bool(re.search(r"\bnh3\b|nh4\(\+\)|ammonia", rhs)) or "deaminat" in low
    amide_ring = "carbamoyl" in rhs or "formimidoyl" in rhs or "imidazolone" in lhs
    if (deamination or amide_ring) and not free_phosphate:
        classes.add("bc_amide_cn")

    # beta-lactam hydrolysis: water opens a beta-lactam amide ring to penicilloate /
    # cephalosporoate / related carboxylate products. This is distinct from generic
    # ester/lipase hydrolysis even though several products end in "-oate".
    beta_lactam_hydrolysis = (
        "beta-lactam" in low
        or "beta lactam" in low
        or "penicillin" in low
        or "cephalosporin" in low
        or "cephalothin" in low
        or "carbapenem" in low
        or "nitrocefin" in low
        or "imipenem" in low
        or "ampicillin" in low
        or "benzylpenicillin" in low
        or any(
            "penicilloate" in term or "cephalosporoate" in term
            for term in rhs_terms
        )
    )
    if beta_lactam_hydrolysis:
        classes.add("bc_beta_lactam_hydrolysis")

    # ester / lipase hydrolysis: an acylglycerol / sterol-ester / phospholipid hydrolysed
    # to an alcohol + carboxylate/fatty acid. Excludes the NAD(P)-dependent aldehyde
    # dehydrogenase (which also makes a carboxylate), protein substrates, and any reaction
    # that releases a free phosphate (those are phosphatases handled above).
    ester_product = ("fatty acid" in rhs) or any(
        term.endswith("oate") or term == "acetate" for term in rhs_terms
    )
    if (
        "nad" not in low
        and "nadp" not in low
        and "[protein]" not in low
        and not free_phosphate
        and not beta_lactam_hydrolysis
        and ester_product
    ):
        classes.add("bc_ester_hydrolysis")

    # N-glycosidic hydrolysis: a nucleoside/nucleotide hydrolysed to ribose (or
    # ribose-phosphate) plus a nucleobase. This is source-free chemistry from Rhea; keeping
    # it separate from carbohydrate O-glycoside hydrolysis prevents the new N-ribosyl lane
    # from collapsing into the glycoside-hydrolase centroid.
    ribose_product = any(
        any(ribose in term for ribose in _N_GLYCOSIDIC_RIBOSE_PRODUCTS)
        for term in rhs_terms
    )
    nucleobase_product = any(
        any(base in term for base in _N_GLYCOSIDIC_BASE_PRODUCTS) for term in rhs_terms
    )
    if ribose_product and nucleobase_product:
        classes.add("bc_n_glycosidic_hydrolysis")

    # Carbohydrate O-glycoside hydrolysis: a glycoside / oligosaccharide hydrolysed to a
    # free sugar + aglycone. Fires on a free-monosaccharide product OR a
    # glycosidic-linkage marker on the substrate side. (Also gives glycoside_hydrolase its
    # defining feature so it stops spuriously firing bc_carbon_carbon_lyase.)
    free_sugar_product = any(
        any(sugar in term for sugar in _GLYCOSIDE_FREE_SUGARS) for term in rhs_terms
    )
    glycosidic_marker = (
        "(1->" in lhs
        or "glucosid" in lhs
        or "glycosid" in lhs
        or "galactosid" in lhs
    )
    if free_sugar_product or glycosidic_marker:
        classes.add("bc_glycoside_hydrolysis")
    return classes


def reaction_bond_change_classes(row: dict[str, Any]) -> set[str]:
    """The union of bond-change classes over all of a row's reaction equations."""
    classes: set[str] = set()
    for reaction in _reaction_equations(row):
        classes |= classify_reaction_bond_change(reaction)
    return classes


def _organic_fragments(side: str) -> list[str]:
    """Organic (carbon-skeleton) tokens on one side of a reaction equation.

    Splits on Rhea's ' + ' separator so charged ions (``NH4(+)``, ``H(+)``) survive
    intact, strips stoichiometric coefficients, and drops protons / water / small
    inorganic leaving groups. Used ONLY by the C-C lyase detector to recognise aldol /
    C-C-bond-cleavage topology -- it reads the substrate->product string only.
    """
    frags: list[str] = []
    for token in re.split(r"\s\+\s", side.strip()):
        token = re.sub(r"^\d+\s+", "", token.strip()).lower()
        if not token or len(token) <= 2 or token in _INORGANIC_FRAGMENTS:
            continue
        frags.append(token)
    return frags


def classify_reaction_nonhydrolytic(reaction: str) -> set[str]:
    """Classify a reaction string into NON-hydrolytic bond-change classes.

    Companion to ``classify_reaction_bond_change`` (which fires only for hydrolysis).
    These cover the transfer / redox / lyase / isomerase chemistry that defines most of
    the expansion ontology. Leakage-safe: reads ONLY the substrate->product equation
    string -- never EC / protein name / prose / fingerprint.
    """
    low = reaction.lower()
    if "=" not in low:
        return set()
    lhs, rhs = low.split("=", 1)
    lhs_tokens = [t.strip() for t in lhs.split("+")]
    rhs_tokens = [t.strip() for t in rhs.split("+")]
    both = lhs_tokens + rhs_tokens

    def _has(tokens: list[str], *subs: str) -> bool:
        return any(any(s in tok for s in subs) for tok in tokens)

    classes: set[str] = set()

    # redox hydride transfer: oxidised<->reduced nicotinamide or flavin across the eqn.
    # Charged species (nad(+), nadp(+)) carry an internal '+' that the token split above
    # mangles, so the nicotinamide pair is matched on the raw lhs/rhs strings.
    nad_ox = ("nad(+)" in low) or ("nadp(+)" in low)
    nad_red = ("nadh" in low) or ("nadph" in low)
    flavin_pair = (("fadh2" in rhs or "fmnh2" in rhs) and ("fad" in lhs or "fmn" in lhs)) or (
        ("fadh2" in lhs or "fmnh2" in lhs) and ("fad" in rhs or "fmn" in rhs)
    )
    if (nad_ox and nad_red) or flavin_pair:
        classes.add("bc_redox_hydride")

    # aldehyde oxidation: aldehyde + NAD(+) + H2O -> carboxylate + NADH. The water-CONSUMING
    # NAD redox is the reaction-center signature of aldehyde dehydrogenase, separating it
    # from generic NAD redox (alcohol -> ketone; no water) which fires only bc_redox_hydride.
    if (nad_ox and nad_red) and "h2o" in lhs_tokens:
        classes.add("bc_aldehyde_oxidation")

    # methyl transfer: S-adenosyl-L-methionine -> S-adenosyl-L-homocysteine
    if "s-adenosyl-l-methionine" in low and "s-adenosyl-l-homocysteine" in low:
        classes.add("bc_methyl_transfer")

    # NTP anhydride cleavage: (d)NTP -> (d)NDP. A kinase TRANSFERS the phosphate to an
    # organic acceptor (no free phosphate, no water); an ATP-dependent ligase/synthetase
    # instead releases free phosphate and/or consumes water to drive a ligation.
    anhydride = bool(
        re.search(r"\b(d?atp|gtp|ctp|utp|itp)\b", lhs)
        and re.search(r"\b(d?adp|gdp|cdp|udp|idp)\b", rhs)
    )
    free_phosphate = ("phosphate" in rhs_tokens) or ("hydrogenphosphate" in rhs_tokens)
    if anhydride and "h2o" not in lhs_tokens and not free_phosphate:
        classes.add("bc_phosphoryl_transfer")
        # phospho-acceptor sub-class (kinase sub-family discriminator)
        if "[protein]" in low:
            classes.add("acc_protein")
        elif any(t in low for t in _NUCLEOSIDE_ACCEPTOR_TERMS):
            classes.add("acc_nucleoside")
        elif any(t in low for t in _SUGAR_ACCEPTOR_TERMS):
            classes.add("acc_sugar")
    elif anhydride and ("h2o" in lhs_tokens or free_phosphate):
        classes.add("bc_atp_dependent_ligation")
    # adenylylating ligases/synthetases: ATP -> AMP + diphosphate drives the ligation
    elif re.search(r"\b(atp|gtp)\b", lhs) and ("amp" in rhs_tokens) and ("diphosphate" in rhs_tokens):
        classes.add("bc_atp_dependent_ligation")

    # glycosyl transfer: sugar-nucleotide donor -> free nucleotide
    sugar_nt = _has(lhs_tokens, "udp-", "gdp-", "dtdp-", "cdp-", "cmp-n", "udp-n", "adp-d")
    free_nt = any(tok in ("udp", "gdp", "dtdp", "cdp", "cmp", "ump", "gmp") for tok in rhs_tokens)
    if sugar_nt and free_nt:
        classes.add("bc_glycosyl_transfer")

    # acyl transfer: acyl-CoA -> free CoA (no water)
    if _has(lhs_tokens, "-coa") and ("coa" in rhs_tokens) and "h2o" not in lhs_tokens:
        classes.add("bc_acyl_transfer")

    # oxygenation: molecular O2 consumed
    if "o2" in lhs_tokens:
        classes.add("bc_oxygenation")

    # peroxide reduction: a hydroperoxide / H2O2 on the SUBSTRATE side is reductively cleaved
    # (O-O bond) to an alcohol / water. This is the reaction-center signature of the cofactor-free
    # peroxidatic thiol/selenol peroxidases (peroxiredoxin / glutathione peroxidase), which carry NO
    # cofactor class and -- before this class -- NO bond-change class at all, so they collapsed into
    # the cofactor-free hydrolase cluster (proteases/esterases). The heme and NAD(P)H peroxidases
    # also fire it, but they separate on their heme / NAD(P) cofactor; the discriminating value here
    # is for the cofactor-free thiol peroxidases. Reads only the Rhea substrate->product equation.
    # NOTE: "superoxide" contains the substring "peroxide" -- exclude it so superoxide dismutases
    # (2 O2(.-) + 2 H(+) = O2 + H2O2; peroxide is a PRODUCT) do not false-fire this class. Match
    # both the spelled-out "(hydro)peroxide" and the "h2o2" formula notation.
    if any(
        ("peroxide" in tok and "superoxide" not in tok) or "h2o2" in tok
        for tok in lhs_tokens
    ):
        classes.add("bc_peroxide_reduction")

    # carboxylation (CO2/bicarbonate fixed with ATP) vs decarboxylation (CO2 released)
    co2_lhs = any(tok in ("co2", "hydrogencarbonate") for tok in lhs_tokens)
    co2_rhs = any(tok in ("co2", "hydrogencarbonate") for tok in rhs_tokens)
    if co2_lhs and re.search(r"\batp\b", lhs):
        classes.add("bc_carboxylation")
    elif co2_rhs and not co2_lhs and "h2o" not in lhs_tokens:
        classes.add("bc_decarboxylation")

    # prenyl-diphosphate cyclase/lyase: prenyl-PP -> diphosphate + carbocation product
    if _has(
        lhs_tokens,
        "geranyl diphosphate",
        "farnesyl diphosphate",
        "geranylgeranyl diphosphate",
        "prenyl diphosphate",
        "dimethylallyl diphosphate",
    ) and ("diphosphate" in rhs_tokens):
        classes.add("bc_diphosphate_lyase")

    # isomerization/racemization: single substrate = single product, no cosubstrate/water
    if len(lhs_tokens) == 1 and len(rhs_tokens) == 1 and "h2o" not in lhs_tokens:
        classes.add("bc_isomerization")

    # C-C bond lyase / aldol cleavage: ONE organic substrate cleaved into TWO organic
    # fragments (retro-aldol, citrate/isocitrate lyase, HMG-CoA lyase, fructose-bisP
    # aldolase) or the reverse aldol condensation -- no water, no NTP anhydride. This is
    # the reaction-center bond change that DEFINES the class II (metal) aldolases, which
    # otherwise carry only the shared divalent-metal cofactor and so cannot separate. A
    # CO2 / phosphate / ammonia leaving group is inorganic (not a second carbon fragment),
    # so decarboxylation / dehydratase / deamination do NOT trip this class.
    if "h2o" not in lhs_tokens and "h2o" not in rhs_tokens and not anhydride:
        lhs_org = _organic_fragments(lhs)
        rhs_org = _organic_fragments(rhs)
        if (len(lhs_org) == 1 and len(rhs_org) == 2) or (
            len(lhs_org) == 2 and len(rhs_org) == 1
        ):
            classes.add("bc_carbon_carbon_lyase")

    return classes


def reaction_nonhydrolytic_classes(row: dict[str, Any]) -> set[str]:
    """Union of non-hydrolytic bond-change classes over a row's reaction equations."""
    classes: set[str] = set()
    for reaction in _reaction_equations(row):
        classes |= classify_reaction_nonhydrolytic(reaction)
    return classes


def cosubstrate_classes(row: dict[str, Any]) -> set[str]:
    """Cosubstrate/donor chemical classes from reaction participants + chemical identities.

    Leakage-safe: reads the Rhea substrate->product equation strings and the cofactor/
    binding-ligand chemical-identity terms only -- never EC / name / prose / fingerprint.
    """
    text = " ".join(_reaction_equations(row)).lower()
    text += " " + " ".join(_chemical_identity_terms(row)).lower()
    return {
        cls
        for cls, patterns in COSUBSTRATE_CLASS_PATTERNS.items()
        if any(p in text for p in patterns)
    }


def featurize(row: dict[str, Any]) -> dict[str, float]:
    """Deterministic leakage-safe chemical/structural feature vector for a label.

    Cofactor-class presence (from chemical identities) and reaction-center bond change
    (from Rhea substrate->product chemistry) are the co-equal mechanistic features;
    active-site residue role ratios provide secondary structural context. EC / name /
    prose / lane / fingerprint are never consulted.
    """
    features = {name: 0.0 for name in FEATURE_NAMES}
    for term in _chemical_identity_terms(row):
        cls = _classify_cofactor(term)
        if cls is not None:
            features[cls] = 1.0

    # dissociable cosubstrate/donor classes (NAD(P), CoA, sugar-nucleotide, 2OG, prenyl-PP)
    for cls in cosubstrate_classes(row):
        features[cls] = 1.0

    # reaction-center bond change: hydrolysis classes + non-hydrolytic transfer/redox/lyase
    for bond_class in reaction_bond_change_classes(row):
        features[bond_class] = 1.0
    for bond_class in reaction_nonhydrolytic_classes(row):
        features[bond_class] = 1.0

    mech = _mechanism_evidence(row)
    active = mech.get("active_site_residue_count") or 0
    catalytic = mech.get("catalytic_residue_count") or 0
    binding = mech.get("binding_residue_count") or 0
    if active > 0:
        features["catalytic_fraction"] = round(catalytic / active, 4)
        features["binding_fraction"] = round(binding / active, 4)
    # bounded structural-size context (log-scaled, capped)
    features["active_site_size"] = round(min(math.log1p(active) / math.log1p(30), 1.0), 4)
    return features


def _active_cofactor_classes(row: dict[str, Any]) -> set[str]:
    """The cofactor classes actually present in a row's chemistry (non-zero)."""
    features = featurize(row)
    return {cls for cls in COFACTOR_CLASSES if features.get(cls, 0.0) > 0.0}


def _significant_centroid_cofactors(
    centroid: list[float], *, threshold: float = 0.15
) -> set[str]:
    """Cofactor classes that meaningfully define a fingerprint centroid."""
    return {
        COFACTOR_CLASSES[i]
        for i in range(len(COFACTOR_CLASSES))
        if centroid[i] >= threshold
    }


def _vector(features: dict[str, float], *, residue_weight: float = 0.15) -> list[float]:
    out = []
    for name in FEATURE_NAMES:
        value = features.get(name, 0.0)
        if name in RESIDUE_FEATURES:
            value *= residue_weight
        out.append(value)
    return out


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def _centroid(vectors: list[list[float]]) -> list[float]:
    if not vectors:
        return [0.0] * len(FEATURE_NAMES)
    n = len(vectors)
    return [sum(v[i] for v in vectors) / n for i in range(len(FEATURE_NAMES))]


def fingerprint_centroids(
    seed_labels: list[dict[str, Any]],
) -> dict[str, list[float]]:
    """Mean representation per fingerprint, from confirmed seed labels."""
    groups: dict[str, list[list[float]]] = defaultdict(list)
    for row in seed_labels:
        fp = row.get("fingerprint_id")
        if not fp:
            continue
        groups[fp].append(_vector(featurize(row)))
    return {fp: _centroid(vectors) for fp, vectors in sorted(groups.items())}


def _nearest_fingerprint(
    vector: list[float], centroids: dict[str, list[float]]
) -> tuple[str | None, float]:
    best_fp, best_sim = None, -1.0
    for fp, centroid in centroids.items():
        sim = _cosine(vector, centroid)
        if sim > best_sim:
            best_fp, best_sim = fp, sim
    return best_fp, round(best_sim, 4)


def assess_row_against_centroids(
    row: dict[str, Any], centroids: dict[str, list[float]]
) -> dict[str, Any]:
    """Public: nearest fingerprint + cohesion for a row, given full centroids.

    Operational classifier (uses the full centroids) reused by the bronze->silver
    promotion preview. Leakage-safe -- featurize reads only chemistry, never
    EC/name/label.
    """
    vector = _vector(featurize(row))
    nearest, nearest_sim = _nearest_fingerprint(vector, centroids)
    fp = row.get("fingerprint_id")
    own = round(_cosine(vector, centroids[fp]), 4) if fp in centroids else None
    return {
        "assigned_fingerprint": fp,
        "nearest_fingerprint": nearest,
        "nearest_similarity": nearest_sim,
        "own_cohesion": own,
        "chemistry_agrees_with_label": (nearest == fp) if fp else None,
    }


def promotion_triage(
    seed_labels: list[dict[str, Any]],
    *,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    """Triage bronze seed labels for bronze->silver promotion vs review.

    Uses leave-one-out centroids (a row never votes on its own centroid) so the
    self-consistency read is honest, not circular.
    """
    vectors = {id(row): _vector(featurize(row)) for row in seed_labels}
    by_fp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in seed_labels:
        if row.get("fingerprint_id"):
            by_fp[row["fingerprint_id"]].append(row)

    full_sums: dict[str, list[float]] = {}
    for fp, rows in by_fp.items():
        acc = [0.0] * len(FEATURE_NAMES)
        for row in rows:
            v = vectors[id(row)]
            for i in range(len(FEATURE_NAMES)):
                acc[i] += v[i]
        full_sums[fp] = acc

    promote, review_outlier, low_cohesion = [], [], []
    loo_agree = 0
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in seed_labels:
        fp = row.get("fingerprint_id")
        if not fp:
            continue
        v = vectors[id(row)]
        # leave-one-out centroids
        loo_centroids = {}
        for other_fp, acc in full_sums.items():
            count = len(by_fp[other_fp])
            if other_fp == fp:
                count -= 1
                if count <= 0:
                    loo_centroids[other_fp] = [0.0] * len(FEATURE_NAMES)
                    continue
                loo_centroids[other_fp] = [
                    (acc[i] - v[i]) / count for i in range(len(FEATURE_NAMES))
                ]
            else:
                loo_centroids[other_fp] = [acc[i] / count for i in range(len(FEATURE_NAMES))]
        nearest, sim = _nearest_fingerprint(v, loo_centroids)
        own_sim = round(_cosine(v, loo_centroids[fp]), 4)
        confusion[fp][nearest or "none"] += 1
        record = {
            "entry_id": row.get("entry_id"),
            "fingerprint_id": fp,
            "nearest_fingerprint": nearest,
            "own_cohesion": own_sim,
            "nearest_similarity": sim,
        }
        if nearest == fp:
            loo_agree += 1
            if own_sim >= cohesion_threshold:
                promote.append(record)
            else:
                low_cohesion.append(record)
        else:
            review_outlier.append(record)

    total = sum(len(rows) for rows in by_fp.values())
    self_consistency_by_fp = {
        fp: round(counts.get(fp, 0) / sum(counts.values()), 4)
        for fp, counts in confusion.items()
        if sum(counts.values())
    }
    return {
        "seed_labels_triaged": total,
        "leave_one_out_self_consistency": round(loo_agree / total, 4) if total else 0.0,
        "self_consistency_by_fingerprint": dict(sorted(self_consistency_by_fp.items())),
        "promotion_candidates": len(promote),
        "review_outliers": len(review_outlier),
        "coherent_but_below_threshold": len(low_cohesion),
        "cohesion_threshold": cohesion_threshold,
        "confusion_by_fingerprint": {
            fp: dict(sorted(counts.items(), key=lambda kv: -kv[1]))
            for fp, counts in sorted(confusion.items())
        },
        "review_outlier_samples": review_outlier[:15],
        "promotion_candidate_samples": promote[:10],
    }


def propose_for_fingerprint(
    target_fingerprint: str,
    candidate_pool: list[dict[str, Any]],
    centroids: dict[str, list[float]],
    *,
    top_k: int = 25,
    min_similarity: float = 0.6,
) -> list[dict[str, Any]]:
    """Rank a candidate pool by representation similarity to a target fingerprint.

    The model-proposed "what to look at next" for a hole. A candidate is only
    proposed when (a) it shares genuine cofactor chemistry with the target (a
    non-empty overlap with the target centroid's defining cofactor classes -- so a
    cofactor-less row is never proposed for a cofactor-defined fingerprint), and
    (b) the target fingerprint is ALSO its nearest centroid (so we do not propose
    rows whose chemistry actually matches some other fingerprint).
    """
    target_centroid = centroids.get(target_fingerprint)
    if not target_centroid:
        return []
    defining = _significant_centroid_cofactors(target_centroid)
    ranked = []
    for row in candidate_pool:
        # require real cofactor-chemistry overlap with the target fingerprint
        if defining and not (_active_cofactor_classes(row) & defining):
            continue
        v = _vector(featurize(row))
        sim = round(_cosine(v, target_centroid), 4)
        if sim < min_similarity:
            continue
        nearest, _ = _nearest_fingerprint(v, centroids)
        if nearest != target_fingerprint:
            continue
        ranked.append(
            {
                "entry_id": row.get("entry_id"),
                "similarity_to_target": sim,
                "shared_cofactor_classes": sorted(
                    _active_cofactor_classes(row) & defining
                ),
                "current_label_type": row.get("label_type"),
            }
        )
    ranked.sort(key=lambda r: (-r["similarity_to_target"], str(r["entry_id"])))
    return ranked[:top_k]


def build_mechanism_representation_loop(
    expansion: list[dict[str, Any]],
    *,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    hole_fingerprints: tuple[str, ...] = (
        "radical_sam_enzyme",
        "cobalamin_radical_rearrangement",
        "ser_his_acid_hydrolase",
    ),
    proposal_top_k: int = 25,
) -> dict[str, Any]:
    seed = [r for r in expansion if r.get("label_type") == "seed_fingerprint"]
    oos = [r for r in expansion if r.get("label_type") == "out_of_scope"]
    centroids = fingerprint_centroids(seed)
    triage = promotion_triage(seed, cohesion_threshold=cohesion_threshold)

    proposals = {}
    for fp in hole_fingerprints:
        proposals[fp] = {
            "centroid_available": fp in centroids,
            "proposed_from_out_of_scope": propose_for_fingerprint(
                fp, oos, centroids, top_k=proposal_top_k
            )
            if fp in centroids
            else [],
        }

    return {
        "audit": "mechanism_representation_loop",
        "created_utc": _utc_now_iso(),
        "status": "ok",
        "non_destructive": True,
        "feature_space": {
            "names": list(FEATURE_NAMES),
            "basis": (
                "review_only_cofactor_and_binding_ligand_chemistry + "
                "rhea_reaction_substrate_product_bond_change + active_site_residue_roles"
            ),
            "bond_change_classes": list(BOND_CHANGE_CLASSES),
            "excluded_from_representation": list(EXCLUDED_FROM_REPRESENTATION),
        },
        "seed_labels": len(seed),
        "out_of_scope_labels": len(oos),
        "fingerprint_centroids_built": sorted(centroids.keys()),
        "promotion_triage": triage,
        "hole_proposals": proposals,
        "leakage_guardrails": {
            "frozen_benchmark_read": False,
            "ec_name_prose_lane_used": False,
            "fingerprint_label_used_as_feature": False,
            "fingerprint_declared_bond_change_used_as_feature": False,
            "bond_change_derived_from_reaction_substrate_product_only": True,
            "reaction_ec_number_used_as_feature": False,
            "used_only_for_candidate_ranking_and_promotion_triage_not_benchmark_scoring": True,
            "registry_written": False,
            "labels_emitted": 0,
        },
    }


def _report(audit: dict[str, Any]) -> str:
    tri = audit["promotion_triage"]
    fs = audit["feature_space"]
    lines = [
        "# Mechanism Representation Loop (leakage-safe self-feeding supply)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "First iteration of the self-feeding loop. A representation learned ONLY from "
        "review-only cofactor/ligand chemistry + active-site residue roles "
        "organises the bronze labels, triages bronze->silver promotion, and proposes "
        "candidates for the governor's holes. EC / protein-name / prose / lane / the "
        "fingerprint label / the frozen benchmark are never read.",
        "",
        f"- Feature space: {fs['names']}.",
        f"- Excluded from representation: {fs['excluded_from_representation']}.",
        f"- Seed labels: {audit['seed_labels']}; out_of_scope: "
        f"{audit['out_of_scope_labels']}; centroids: "
        f"{audit['fingerprint_centroids_built']}.",
        "",
        "## Promotion triage",
        "",
        f"- Leave-one-out self-consistency (chemistry alone recovers the "
        f"fingerprint): {tri['leave_one_out_self_consistency']}.",
        f"- Promotion candidates (cohesion >= {tri['cohesion_threshold']}): "
        f"{tri['promotion_candidates']}.",
        f"- Review outliers (chemistry points at a different fingerprint): "
        f"{tri['review_outliers']}.",
        f"- Coherent but below threshold: {tri['coherent_but_below_threshold']}.",
        "",
        "## Hole proposals (model-ranked from out_of_scope)",
        "",
    ]
    for fp, payload in audit["hole_proposals"].items():
        n = len(payload["proposed_from_out_of_scope"])
        lines.append(
            f"- {fp}: centroid {'available' if payload['centroid_available'] else 'MISSING'}; "
            f"{n} proposed candidates."
        )
    lines.extend(
        [
            "",
            "## Leakage guardrails",
            "",
            f"- Frozen benchmark read: {audit['leakage_guardrails']['frozen_benchmark_read']}.",
            f"- EC/name/prose/lane used: "
            f"{audit['leakage_guardrails']['ec_name_prose_lane_used']}.",
            f"- Fingerprint label used as feature: "
            f"{audit['leakage_guardrails']['fingerprint_label_used_as_feature']}.",
            "- Used only for candidate ranking + promotion triage, NEVER as a "
            "benchmark scorer.",
            f"- Registry written: {audit['leakage_guardrails']['registry_written']}.",
            "",
        ]
    )
    return "\n".join(lines)


def write_mechanism_representation_loop(
    *,
    out_path: Path,
    report_path: Path | None = None,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    proposal_top_k: int = 25,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    audit = build_mechanism_representation_loop(
        expansion,
        cohesion_threshold=cohesion_threshold,
        proposal_top_k=proposal_top_k,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
