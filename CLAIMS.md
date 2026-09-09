# Catalytic Earth claim ledger

**Effective:** 2026-07-13
**Machine-readable source:** `data/governance/claim_ledger.json`
**Policy:** `docs/ATLAS_TRUTH_POLICY.md`

This is the canonical current claim surface. Older documents and artifacts are
historical records; where they conflict with this ledger, this ledger controls
current wording. Status meanings:

- **Supported:** directly supported at the stated scope.
- **Diagnostic:** useful evidence that does not justify a broad conclusion.
- **Superseded:** a real result or decision whose earlier interpretation is no
  longer current.
- **Retracted:** wording that must not be used as a current claim.

## CE-001 — current702 composition

**Status:** Supported

`current702` contains 702 project benchmark labels: 685 bronze and 17 silver,
with zero project-gold labels. Of these, 683 were automation-curated and 19
author-reviewed. Do not call this surface expert-curated gold.

## CE-002 — the 10,001-row surface

**Status:** Supported

The combined surface is 8,305 positive fingerprint assignments plus 1,696 OOS
protein-label records. These are not 10,001 mechanisms. Positive assignments,
controls/OOS records, reactions, and mechanism hypotheses are reported
separately.

## CE-003 — chemistry result

**Status:** Diagnostic

The chemistry evaluation produced 160/210 coarse cofactor-bucket matches
(76.19%) and 65/210 exact fingerprint matches (30.95%) on the featurizable,
centroid-covered positive subset. The 76.19% number is not called exact
mechanism recovery. The ID/OOS similarity distributions did not establish a
useful abstention or novelty boundary by themselves.

## CE-004 — percentage of mechanism space

**Status:** Retracted

The claim that the project covers about 2% of mechanism space is withdrawn.
No percentage is reported until the project defines a mechanism object and a
defensible denominator. Rhea reactions, M-CSA exemplars, EC classes, ontology
families, fingerprints, and protein records are not interchangeable units.

## CE-005 — June 28 M-CSA holdout

**Status:** Retracted

The June 28 result is not a never-touched independent holdout. The 126
later-frozen rows had already appeared in scored project surfaces. It is
retained as retrospective analysis of an exhausted surface. Its numerical
result is not deleted, but its independence claim is retracted.

## CE-006 — June 29 Swiss-Prot/PDB-holo evaluation

**Status:** Superseded

This is a spent EC-proxy validation surface, not independent stepwise-mechanism
gold. It recovered 45/64 in-scope rows, including only 2/16 metal rows, with
2/72 OOS false positives. The 40% preregistered OOS ceiling was too permissive
for a deployment claim, and the successful three-family reading is post-hoc.

## CE-007 — structure versus sequence

**Status:** Diagnostic

Structure retrieval beat pairwise Smith-Waterman on a selected surface. This
does not show that structure generally beats mature profile, family, reaction,
template, or learned baselines. Those matched baselines remain required on a
disjoint evaluation.

## CE-008 — active-site verification wording

**Status:** Superseded

Automated residue and geometry checks are computational consistency checks.
They are not expert or experimental verification. Current records must use the
atlas evidence tier and identify the checking process.

## CE-009 — full test-suite state

**Status:** Supported

The preserved Python 3.13 audit ran 2,559 tests with 74 failures, 20 errors,
and one skip. Its later root-cause attribution is corrected: 54 failed tests
contained 179 hash comparisons that differed only because a Windows checkout
converted Git's LF blobs to CRLF; those were not content drift. One genuine
historical lineage mismatch remains quarantined without rewriting its embedded
hash. After dependency, path, compatibility, and fixture repairs, the pinned
Python 3.13 environment ran the complete expanded 2,586-test suite with zero
failures, zero errors, and one skip. This is software validation, not
scientific validation.

## CE-010 — fabrication audit boundary

**Status:** Diagnostic

The bounded public-repository audit found no evidence of fabricated raw
results, invented structures, or falsified Foldseek output. This statement
does not infer private intent and is not an omniscient guarantee.

## CE-011 — present project maturity

**Status:** Supported

Catalytic Earth is a real research scaffold for an open computable
catalytic-mechanism atlas. It is not yet a validated global atlas, a validated
sequence-to-mechanism predictor, or a production biological design system.
The full atlas remains the mission.

## CE-012 — expansion freeze

September development amendment: the owner-authorized
[computational policy](data/governance/computational_review_policy.json)
permits source-scoped draft operations after source challenge and adjudication,
without waiting for human submissions. It does not establish independent
validation, expand protected registries, or authorize performance claims.

**Status:** Supported

The truth-reset gates are implemented, but protected registry writes and new
performance headlines remain frozen as a deliberate safety latch until an
explicit reviewed post-reset admission decision changes `frozen` to `false`.
P0 completion does not silently authorize registry mutation. Corrective work,
schema/crosswalk work, bounded preregistered experiments, audits, and packaging
remain allowed.

## CE-013 — Option-B bronze22 state

**Status:** Supported

The 22-row off-M-CSA Option-B bronze surface is recorded as frozen and unscored.
It may be spent once under its frozen contract. Because its labels are bronze
proxies, even a clean result cannot be described as expert or mechanism-gold
validation.

## CE-014 — post-hoc family views

**Status:** Diagnostic

Family-selected and three-family views produced after inspecting a result are
exploratory analyses. They remain visible because they can generate useful
hypotheses, but they are not preregistered endpoints and require a fresh,
disjoint test before supporting a confirmatory claim.

## CE-015 — original predictor hypothesis and negative result

**Status:** Supported

The original hypothesis that the current structural atlas would reveal
mechanism-family orphans missed by ordinary sequence annotation failed on the
tested families: every proposed structural orphan carried a Pfam annotation
that revealed its family. The atlas north star does not erase this negative
predictor result or convert it into a success.

## CE-016 — GFAT2 proxy mapping

**Status:** Retracted

The June 29 EC-proxy set mapped human GFAT2/O94808 (EC 2.6.1.16) to
`plp_dependent_enzyme` by a blanket `2.6.1.*` rule. That assignment is
withdrawn: the cited EC chemistry is lysine-ketimine/transamidination chemistry,
not evidence of PLP dependence. The historical row remains unchanged for
provenance and must be excluded or independently adjudicated in any reuse.

## CE-017 — A0A177THN5 donor-specific transfer

**Status:** Retracted

The APX-specific assignment inferred from neighbour P48534 is withdrawn. The
larger APX-versus-CcP study based on that premise is retired. Retain the
class-I-like heme-peroxidase family hypothesis; CcP-like is a provisional
working interpretation, not experimentally established donor specificity.
Neither conserved catalytic residues nor the broad InterPro `Ccp1-like`
family distinguishes APX from CcP. See the
[computational reassessment](docs/COMPUTATIONAL_REVIEW_20260905.md).

## CE-018 — structural identity does not establish a productive chemical state

**Status:** Supported

The retained 1SUP structure is sequence-unmutated but explicitly deposits a
PMS covalent modification on catalytic Ser221. Its His64 A/B alternatives
remain distinct, with no inferred relation to PMS occupancy or catalytic
activity. 1PQ5 is a pH-5 model with partially occupied ARG atoms and a
primary-source-described autoproteolytic fragment context. The shared
[structural-context query](docs/ATLAS_STRUCTURAL_CONTEXT.md) preserves these
states and atom-specific coordinates. It adds two annotations of existing
cases, not new biological coverage or validated catalytic arrangements.

## CE-019 — partner-subunit omission and distinct functional endpoints

**Status:** Supported

In deposited 6HA3 assembly 1, operator 2 supplies Glu366 beside the
operator-1 cofactor/Gln160 neighborhood. A crop containing only the original
protein copy omits that study-implicated group. The same study reports E366Q
F6P-intermediate nondetection, residual X5P/R5P turnover, and unavailable
F6P stopped-flow kinetics because the reporter band is absent. These are
different endpoints, not three demonstrations of abolished catalysis.
The [assembly context](docs/ATLAS_STUDY_CONTEXT.md#partner-subunit-context)
preserves exact atom/copy identity and this omission warning. It establishes
neither a complete catalytic site, a causal geometric tolerance, nor independent
experimental support for the deposited assembly.

## CE-020 — peptidoglycan donor role and nonproductive analogue

**Status:** Supported

The prior M0970 state-probe label calling the growing glycan an acceptor is
corrected. In the primary SaMGT elongation model the growing chain occupies
donor site S2 and incoming lipid II occupies acceptor site S1. The same paper
describes the 3VMT GalNAc-containing analogue as binding but unable to serve
as an E100 substrate. The [current source view](docs/ATLAS_POLYMER_CONTEXT.md)
exposes these limits beside the corrected role while preserving historical
reports and source-only permissions. A separate published direction assay on
four PGTs is not a direct Q99T05/SaMGT experiment. Exact product X00676,
numeric chain length, processivity and the complete M0970 mechanism remain
unresolved.

## CE-021 — K166R deposited context and inferred product origin

**Status:** Supported

The [1MDL source followup](docs/ATLAS_MECHANISM_EVIDENCE.md#new-source-followup-the-k166r-deposit)
binds the exact K166R paper citation to a deposited P11444-referenced
Arg166/Lys166 difference. The model contains distinct R- and S-mandelate
instances despite its R-mandelate title. The depositor's proposed slow
racemization origin for SMN is interpretation, not a measured turnover event.
Conflicting organism metadata remains unresolved. No H297N structure, exact
assay-preparation identity, assay condition, source-atom map or new functional
measurement is established. This is a supplemental annotation; the existing
six-observation query and its endpoint-specific conclusion remain unchanged.

## CE-022 — an intermediate label does not identify a mobile-catalyst pose

**Status:** Supported

In retained 2QUT, author Tyr363 OH is over 24 Å from both same-chain deposited
13P C1/C3 in chains A/B/C; chain D Tyr363 is unmodeled. All four chains retain
their Lys229–13P covalent connections, and declared assembly 1 uses only the
identity operator. The [M0222 evidence limitation](docs/ATLAS_SOURCE_DRAFTS.md#m0222-an-enamine-model-does-not-supply-the-mobile-catalyst-pose)
therefore separates covalent-enamine identity from the proposed Tyr
proton-transfer arrangement. It establishes no absent catalysis, solution
population, conformational trajectory, reacting-atom map, kinetic rate or
design-distance threshold. Existing annotations and source drafts retain their
counts and evidence tiers.

## Change rule

Do not edit a status silently. Update the JSON ledger, this readable ledger,
`ERRATA.md` when public wording changes, and the exposure ledger when an
evaluation surface is viewed, scored, tuned against, or adjudicated. Negative
and superseded results remain in history.
