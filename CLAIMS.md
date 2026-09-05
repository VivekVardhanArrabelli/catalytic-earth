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

## Change rule

Do not edit a status silently. Update the JSON ledger, this readable ledger,
`ERRATA.md` when public wording changes, and the exposure ledger when an
evaluation surface is viewed, scored, tuned against, or adjudicated. Negative
and superseded results remain in history.
