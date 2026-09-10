# Scientific direction and review

This is the current direction review and compact coordination record for the
hourly research loop. Claims, errata and the atlas truth policy control evidence
scope. A direction decision changes the next work; it does not rewrite accepted
source facts, frozen kernels or the full-atlas North Star.

## Current review — 2026-09-10

**Review boundary:** hourly restart `b9aa9a5f` through scientific main
`db28b67fc41a552b9152bada94c8903e066729cd` (PRs #56–#71; its tree was reviewed
at PR head `0c0199a9`). PR #71 was in CI when this review began.
The first pass was read-only while that hourly writer owned the lock.
This review's containing Git commit identifies the resulting direction change.

**Verdict:** the work advances the atlas, but accumulated source annotations
now need a common scientific use. Continue the program with the priority below.
Neither abandoning the atlas nor accelerating the same annotation queue is
justified by this review.

The material gains include the [polymer donor/acceptor correction](ATLAS_POLYMER_CONTEXT.md),
[study/assembly-aware transketolase context](ATLAS_STUDY_CONTEXT.md),
[RA61 component counterevidence](ATLAS_RA61_COMPONENT_EVIDENCE.md), and
[RA95 construct- and endpoint-specific effects](ATLAS_DESIGNED_ENZYME_OUTCOMES.md).
The RA95 [substrate-preference conflict](ATLAS_DESIGN_STEREOSELECTIVITY.md) and
[conditional tyrosine comparison](ATLAS_RA95_TETRAD_CONTROLS.md) can prevent
incorrect design or training labels. These are published source outcomes and
applicability restrictions, not project experiments or design-success estimates.

### Coordination and sampled evidence

| Review role | Evidence checked | Finding |
| --- | --- | --- |
| Direction | North Star, claim/errata scope, recent increments and current handoff | Scientific relevance is real; another isolated endpoint is lower priority than making the accumulated relations usable. |
| Reuse | Recent packet shapes, existing consumers, two sequence providers and three cross-case pointers | All five sampled references resolve; the two sequence hashes match. Shared schema names nevertheless cover incompatible observation layouts, and no common consumer spans the recent designed-enzyme packets. |
| Source challenge | Hash-verified retained 2017 and 2013 supplements, 2013 article, table/Methods images and recomputed arithmetic | No material defect found in the two sampled claims. The RA95.5-8F double/reference factors are 0.021 for kcat, about 0.423 for KM and about 0.050 for printed efficiency. The inconsistent 2013 RA95.5 kinetic row is correctly quarantined. |

The reviewers were `direction_review_12h`, `reuse_review_12h` and
`evidence_review_12h`, using GPT-6 Astra/max with separate questions. Related
model reviews are not independent human review. This was not an exhaustive
literature, sequence, structural or raw-fit audit. Primary-source bytes were
available in retained host-local temporary caches; hash and locator records do
not by themselves guarantee those bytes will remain available after cleanup.

### The three reconsideration conditions

1. **Repeated bespoke chemistry code: controlled in recent curation.** Keeping
   source facts in data is useful. It is not sufficient evidence of shared
   computational behavior.
2. **Curation becoming reusable: partly demonstrated, still a bottleneck.**
   Exact sequence and provenance reuse works. But `functional-comparison.v1`
   stores RA95 kinetic values under both `steady_state` and `parameters`;
   `source-qualification.v1` spans `observations`, `kinetic_observations`,
   `pH_profile` and parameter arrays. These labels are not a common executable
   contract. The existing study validator does not cover the newer packet set.
3. **Integrated value beyond convenient repackaging: promising but unproven
   across the new studies.** Source corrections and prevented transfers matter.
   The [study documentation](ATLAS_STUDY_CONTEXT.md) explicitly limits the new
   functional tables to repository annotations. A reader still reconstructs
   study-specific joins; no measured curation saving or design utility is shown.

Numeric measurements, qualitative traces, endpoint-specific nondetection and
unassessed controls must remain different record kinds. In particular,
[beta-barrel control context](ATLAS_BETA_BARREL_CONTROLS.md) cannot become a
matched observation merely because a nearby deposited construct has a sequence.

## Current priority: one usable perturbation relation

**Question:** which proposed catalytic-group perturbations retain a measured
catalytic endpoint, in which construct/background, substrate and assay, and
which apparent comparisons cannot be transferred?

Use the already acquired RA95 2013/2017 and RA61 packets to produce one
source-bound, executable cross-study perturbation dataset view. Include KE59
as an unassessed-matched-control countercase. Preserve the beta-barrel
construct/control mismatch if that packet is included; do not invent missing
construct or assay joins to make it fit. Prefer completing this relation before
adding the inherited standalone forward-synthesis annotation.

The minimum common relation carries source-defined construct and background,
exact sequence/provider or explicit missing identity, perturbation, substrate
and stereochemistry, reaction direction at its supported scope, assay,
parameter/units, observed value or scoped result kind, uncertainty, matched
control, admissible comparison, source pointers and unresolved applicability.
Keep the relevant control and counterexample rows; this is not a success-only
selection. Do not pool rates across assays or studies, convert nondetection
to zero, normalize inconsistent source triplets silently, or claim causal
chemical roles from mutation effects.

Use a shared data projection and eligibility rules rather than enzyme-ID
branches in a consumer. This is a bounded use of existing evidence, not a new
application, model, universal ontology or mandatory benchmark before all future
science. Preserve study-specific chemical meaning and source records during
any representation migration. Preserve hash-verified source witnesses in a
durable permitted local cache when needed, without new acquisition or
redistributing publisher bodies contrary to the source policy.

**Expected gain:** a researcher or model can recover supported perturbation
comparisons and their exclusions without reconstructing each study's file
shape. It also tests whether today's curation can supply a design-relevant
dataset relation at all.

**Stopping condition:** the same consumer and eligibility rules recover the
RA95 parameter/background distinction and paired-tyrosine effect, the retained
substrate-preference limitation, RA61's scoped initial-rate contrast, and the
KE59 abstention with exact provenance. If this requires another case-specific
runtime branch, identify and fix the smallest shared missing concept instead
of collecting more cases. No design-success or independent-validation claim
follows. Reassess the bottleneck after this bounded result; the priority is not
a permanent gate against useful coverage growth.

## Recurring direction review

The existing oversight schedule `targeted-expansion-oversight-check` is
repurposed as **Catalytic Earth scientific direction review**, attached to the
current oversight task. It runs at 07:55 and 19:55 America/Chicago, using this
task's GPT-6 Astra/max settings. The hourly worker remains at five minutes past
each hour on GPT-6 Astra/max. Other historical research schedules stay paused.

Review substantive changes since the last reviewed commit, sample consequential
source claims, and apply the three conditions across the whole window. When a
correction is justified, update the current priority and the hourly prompt;
publish necessary repository changes under the
[shared ownership protocol](HOURLY_RESEARCH.md). Read-only oversight can run
during research. An active or uncertain writer's lock must not be reclaimed.
If repository editing must wait, put a concrete correction into the next
hourly prompt and leave its implementation to a safely owned run.

Record meaningful changed findings here; use a local receipt or the oversight
task for unchanged checks. Notify the user for meaningful scientific findings,
direction changes, completed corrections, failures or required action. No new
claim, report, test or commit is required merely because twelve hours elapsed.
