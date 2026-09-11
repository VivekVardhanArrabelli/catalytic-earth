# Scientific direction and review

This is the current direction review and compact coordination record for the
hourly research loop. Claims, errata and the atlas truth policy control evidence
scope. The North Star remains the full computable catalytic-mechanism atlas,
ultimately enabling de novo enzyme design directly or through a useful dataset.
Oversight changes priorities and corrects consequential defects; it is not a
second hourly research writer.

## Current review — 2026-09-11 13:05 UTC

**Published evidence reviewed:** the previous oversight merge
`dbcff2541baf00d378d13c6e676c34419a9cfb35` through
`36018246c49dafe3256800041f5395b899f416d5` (PRs #91–#99).
The first pass reviewed immutable `edef3d5c` while PR #99 was in progress and
left its writer's files, Git refs and lock alone. This follow-up includes the
merged PR #99 after its task completed and released ownership. Local main and
live remote agreed, required PR CI passed, and no PR was open before this
review acquired the shared lock for the correction below. Uncommitted worker
output was not used as published evidence.

**Decision:** retain the scientific direction and the newer M0187 handoff.
The recent work connects source-model transitions and control evidence to
measured endpoints through shared consumers. It remains incomplete as a
mechanistic dataset for design. Close the older DERA acquisition priority:
the bounded attempt finished, but the requested residue–state–function relation
remains unassessed because primary text and its flagged erratum were unavailable.
The pivot to KSI was appropriate. Do not restart access-only work or replace the
current question with a benchmark, showcase or new task queue.
The [previous review](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/dbcff2541baf00d378d13c6e676c34419a9cfb35/docs/SCIENTIFIC_DIRECTION.md)
preserves its original question and stopping condition.

### Coordination and evidence

| Review role | Evidence checked | Finding |
| --- | --- | --- |
| Direction | Published PRs #91–#99, claims, North Star and handoffs | DERA acquisition and the bounded M0186 continuity inquiry are complete at their stated limits. M0187 offers a distinct source-site-to-function relation. |
| Representation/reuse | Shared runtime and isolated public queries for TKT, POX, RA61, calmodulin and the micellar system | Existing facts serve shared model/control consumers without enzyme-ID branches. Two assessed contexts incorrectly receive the generic unassessed-control reason and prose. |
| Source challenge | Retained Fried2014 Table S2, Kim1995 Table 1 and Schmidt2013 primary text; KSI2010/calmodulin/KE59 assessment declarations | The bounded primary sample supports the retained denominators, probe/turnover distinction and uncertainty scope. The status correction does not require changing source facts or scientific conclusions. |

The reviewers were `direction_review_12h`, `reuse_review_12h` and
`evidence_review_12h`. They reuse earlier context and are correlated computational
reviews, not independent human review. The primary sample did not re-review all
calmodulin experiments, raw fits or the disputed electrostatic contribution.
No new source acquisition was needed. Source objections take precedence over
agreement among agents.

### What the published work establishes

- [KSI field/function](ATLAS_KSI_FIELD_FUNCTION.md) preserves the distinction
  between inhibitor-carbonyl spectroscopy and steroid turnover, primary and
  compiled kinetic values, and the authors' exclusion of D40N from their
  field/rate model. [Tyr16 controls](ATLAS_KSI_FIELD_FUNCTION.md#donor-controls-distinguish-mutation-effects-from-a-single-hydrogen-bond-energy) show that
  hydroxyl-bearing and hydroxyl-absent replacements can retain moderate source
  turnover relative to the severe Phe loss. This does not yield a universal
  removable hydrogen-bond energy or prove an identical microscopic pathway.
- [TKT and POX model relations](ATLAS_STUDY_CONTEXT.md) and the
  [RA61 reporter path](ATLAS_PERTURBATION_RELATION.md) use one consumer to
  distinguish reversible adduct formation, a reporter spanning multiple
  transitions and initial product formation. A fitted or apparent endpoint
  does not become an individual-arrow rate or a full-cycle rate.
- [Calmodulin controls](ATLAS_CALMODULIN_CONTROLS.md) retain reported activity
  after named nucleophile-removal/acetylation interventions. They constrain a
  unique lysine-route interpretation without proving hydrophobic-only catalysis
  or a particular alternative. The [micellar control](ATLAS_MICELLAR_CONTROLS.md)
  adds a supported butylamine system contrast while retaining missing long-chain
  controls, distinct denominators and nominal bulk normalization. It cannot
  isolate catalytic component energies.
- [M0186 continuity](ATLAS_PLP_STEP_BOUNDARY.md#within-m0186-the-next-state-stops-at-explicit-hydrogen-continuity)
  accounts for the selected heavy-atom changes but cannot replay the full
  explicit-H depiction. Hydrogen-neighbor elements differ across the boundary;
  panel-local H identifiers do not establish physical identity. The next panel
  retains a substrate–PLP adduct, so “free PLP” cannot mean unbound cofactor here.
  This closes one consequential source-state question without declaring the
  underlying chemistry false. A repeated panel-refusal campaign is unwarranted.

These are useful evidence relations and inference limits. They add protein
study contexts without establishing broad protein coverage, new project-run
experiments or demonstrated design performance. Source-specific interpretation, chemical-state completeness and
construct/preparation joins remain substantial work.

### Correction made by this review

The KSI2010 donor and calmodulin nucleophile contexts explicitly declare
`source_discriminant_assessed: true` and `arithmetic_requested: false`.
Their legacy `operation: unassessed` requests nevertheless returned
`matched_perturbation_control_unassessed` and prose saying no matched comparison
was evaluated. That conflates source assessment with absent scalar arithmetic
and could make a consumer discard already assessed evidence.

The shared response now emits `arithmetic_not_requested` and states that
source-scoped discrimination was assessed without a requested or computed scalar
comparison. Both contexts retain `eligible: false` and null value, unit and
uncertainty, together with every source block and evidence limitation. Genuine
unassessed requests, including KE59's E230 question, retain their prior behavior.
Explicit assessment flags must be a consistent Boolean pair; context alone does
not promote assessment. A focused regression addresses this demonstrated
failure. The whole-query comparison checks that only these two reason lists and
interpretation strings change, apart from the review binding. No measurement,
source conclusion, evidence tier, scientific claim or numerical comparison is
changed. Original provider review manifests remain historical.

### The three reconsideration conditions

1. **Repeated bespoke chemistry code:** not observed in this window. Source-
   model measurement boundaries and non-genetic controls justify shared concepts
   used across multiple contexts. Facts and mappings remain in data. This
   reuse does not establish coverage of all chemistry.
2. **Curation becoming reusable:** previously curated measurements and provider
   objects serve additional model and control relations without transcription.
   Source interpretation still needs manual work. No measured curation-time
   saving is established; repeating settled joins would erase the benefit.
3. **Integrated value beyond repackaging:** endpoint-to-model relations and
   conditional controls prevent specific unsupported transfers. They still do
   not supply a complete construct–reacted-state–mechanism–outcome chain or a
   demonstrated design consumer. Prefer the next missing consequential relation
   over another field inventory, access receipt or repeated refusal.

## Current priority: connect a source catalytic fragment to functional evidence

**Question:** can the retained M0187 step-1 arrow endpoint `a58` be associated
with the source's His297 fragment and named reference site, then connected to
the already curated H297N functional evidence at its actual scope?

Use `data/atlas/atlas10/sources/mcsa/M0187.json` (the fragment contains `a52`,
alias His297A), `data/atlas/transformations/m0187/transformations.json` and
`data/atlas/mechanism_evidence/m0187/evidence.json`. This is a zero-acquisition
inquiry. Verify the fragment, source role and reference numbering before
representing the relation. Evaluate any needed representation change before
implementation; do not create enzyme-specific runtime logic.

**Expected gain:** source atom-to-named-site resolution alongside enantiomer-
specific function, beyond another panel refusal. Preserve the distinction
between S-substrate exchange, R-exchange nondetection and separate racemization
nondetection. The source depiction is a mechanistic proposal; these assays do
not experimentally validate that exact arrow.

**Stopping condition:** one supported scoped relation or the first ambiguous
fragment, role/numbering join or unsupported transfer. Missing exact assayed
sequence remains a limitation, not a new blanket gate for a supported reference-
site relation. Do not infer PDB atom identity, mutant geometry, zero from
nondetection or equivalence of exchange and racemization. Do not reopen the
closed M0186 hydrogen or M0213 stereo inquiries without new evidence.
Reassess the bottleneck after this bounded outcome.

## Recurring direction review

The active `targeted-expansion-oversight-check` schedule is **Catalytic Earth
scientific direction review**, attached to this oversight task at 07:55 and
19:55 America/Chicago. The hourly worker is configured for five minutes past
each hour on GPT-6 Astra/max but is **paused**, as verified in the actual app
configuration at this review. Preserve that pause pending the user's response;
an older receipt's “active” description is not current scheduling authority.
The queued one-off status correction can be retired from the hourly prompt
after this correction is merged, without changing the pause or standing brief.

Review substantive changes since the last reviewed commit, sample consequential
source claims and apply the three conditions across the whole window. Recognize
completed stopping conditions and useful newer handoffs. Publish necessary
changes under the [shared ownership protocol](HOURLY_RESEARCH.md), without
reclaiming an active or uncertain writer's lock. While a writer is active, use
immutable committed snapshots and defer edits to a safely owned run.

Record meaningful changed findings here; keep unchanged checks in the local
receipt or task. Notify only for meaningful findings, direction changes,
completed corrections, failures or required action. No new claim, report, test
or commit is required merely because twelve hours elapsed.
