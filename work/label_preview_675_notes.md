# 675 Label-Factory Preview Notes

## Status

The 675 batch is a preview only. It is not promoted to
`data/registries/curated_mechanism_labels.json`.

Mechanical checks pass:

- `artifacts/v3_label_batch_acceptance_check_675_preview.json`: accepted for
  counting if promoted, with 1 clean new countable label and 61 pending
  review-state rows. The acceptance check now verifies that newly countable
  labels do not appear in the review-evidence-gap artifact.
- `artifacts/v3_label_factory_gate_check_675_preview_batch.json`: 11/11 gates
  pass.
- `artifacts/v3_label_factory_preview_summary_675.json`: 0 blockers, 0 hard
  negatives, 0 near misses, 0 false non-abstentions, and all unlabeled preview
  rows retained. It now attaches the scaling-quality audit and records
  `review_before_promoting` as the latest audit recommendation.
- `artifacts/v3_label_scaling_quality_audit_675_preview.json`: 0 accepted
  labels with review debt after the evidence-limited negative deferral rule was
  tightened. The audit has 0 blockers because the diversity-aware review export
  retains all underrepresented ontology-family rows. It records
  `not_assessed_no_sequence_cluster_artifact` for the paralog/near-duplicate
  audit until a sequence-cluster artifact is attached.

Promotion should still wait for review:

- `artifacts/v3_label_preview_promotion_readiness_675.json` is mechanically
  ready but recommends `review_before_promoting`.
- The readiness artifact also copies the new debt entry ids and next-action
  counts so the promotion decision can be audited without separately diffing
  debt summaries.
- Preview review debt increases from 53 to 61 rows.
- `needs_more_evidence` decisions increase from 37 to 61 rows because the
  preview now keeps below-threshold evidence-limited negatives in review rather
  than counting them as safe out-of-scope labels.
- Of the 61 preview debt rows, 37 are carried from the accepted 650 state and
  24 are new in the 675 preview.
- The preview debt artifact records full `carried_review_debt_entry_ids` and
  `new_review_debt_entry_ids` metadata so the new rows are not hidden by the
  capped prioritized row table.
- New preview debt entry ids: `m_csa:653`, `m_csa:654`, `m_csa:655`,
  `m_csa:656`, `m_csa:657`, `m_csa:658`, `m_csa:659`, `m_csa:660`,
  `m_csa:661`, `m_csa:662`, `m_csa:663`, `m_csa:664`, `m_csa:665`,
  `m_csa:667`, `m_csa:668`, `m_csa:669`, `m_csa:670`, `m_csa:671`,
  `m_csa:672`, `m_csa:673`, `m_csa:674`, `m_csa:675`, `m_csa:676`, and
  `m_csa:677`.
- New debt next actions: 14 alternate structure/cofactor-source inspections,
  5 local cofactor or active-site mapping checks, 3 expert-review decisions,
  and 2 expert family-boundary reviews.
- Among the prioritized new preview rows, the dominant next action is alternate
  structure/cofactor-source inspection for expected-absent cofactors; the next
  largest group needs local cofactor or active-site mapping checks.

## Accepted Preview Label

The preview would add 1 seed-fingerprint label:

- `m_csa:666` as bronze automation-curated `ser_his_acid_hydrolase`.
  Supporting preview evidence: selected structure `1MPX` is geometry `ok`,
  retrieval score is 0.8521 at threshold 0.4115, the Ser-His-Asp/Glu residue
  signature is complete, and mechanism text explicitly describes a serine
  hydrolase-like mechanism.

The 17 previously accepted out-of-scope rows are now deferred because their
below-threshold negative calls depended on missing/structure-only cofactor
evidence, structural blockers, counterevidence, or reaction/substrate mismatch.
They remain in the review-state registry and are not countable benchmark
labels.

## Scaling-Quality Audit

The 675 preview audit documents the required failure-mode checks before any
promotion:

- 24 new review-debt rows were classified; none are unclassified.
- 0 accepted labels have review debt; `m_csa:666` is the only clean accepted
  label.
- Observed issue classes among the new debt rows: ontology scope pressure
  (24), cofactor-family ambiguity (19), reaction/substrate-class mismatch (14),
  active-site mapping gaps (6), family-propagation boundary pressure (1), and
  mixed evidence (1).
- Hard-negative family concentration is not observed because the preview has
  0 hard negatives and 0 near misses.
- Active-learning queue concentration is observed, but the expert-review export
  now retains all 26 underrepresented ontology-family rows, so it is not a
  scaling-quality blocker for this preview.

## Review Debt

Top debt remains `m_csa:494` (`propanediol dehydratase`). The selected `1DIO`
structure has structure-wide `B12` but no local cobalamin within the 6 A
active-site ligand cutoff; nearest B12 is 8.349 A. Keep it review-state only
unless local cobalamin evidence, a better structure, or expert review resolves
that gap.

The 675 preview adds review pressure around metal-hydrolase boundary rows such
as:

- `m_csa:656`: adenosinetriphosphatase, metal-hydrolase target below the
  abstention floor with structure-only expected cofactor evidence.
- `m_csa:657`: mitochondrial processing peptidase, high-scoring metal boundary
  with structure-only expected cofactor evidence and insufficient explicit
  hydrolysis context.
- `m_csa:660`: superoxide reductase, high-scoring metal boundary but mechanism
  text points to redox/peroxide chemistry rather than hydrolysis.
- `m_csa:668`: leishmanolysin, high-scoring metal boundary needing expert
  review before counting.
- `m_csa:671` and `m_csa:674`: N-carbamoyl-D-amino-acid hydrolase entries
  below the abstention floor with expected cofactor absent from the selected
  structures.

Inspect these before promotion if the next run chooses quality review over
immediate scaling.
