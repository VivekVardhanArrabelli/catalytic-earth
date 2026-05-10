# 525-Entry Label Queue Notes

These notes cover the 525-entry label-factory batch after the `m_csa:494`
review deferral. The initial queue was built with
`artifacts/v3_imported_labels_batch_494.json` as the review-state registry, so
`m_csa:494` was intentionally treated as a documented non-countable evidence
gap rather than as an unreviewed candidate.

## Queue State

- Countable curated labels advanced from 499 to 523 after the accepted
  525-entry batch.
- Review-state labels advanced to 525 because `m_csa:494`, `m_csa:510`, and
  five boundary-control rows are present as `needs_expert_review` placeholders.
- 525 geometry artifacts contain 524 entries and 516 entries with pairwise
  geometry.
- The pre-batch 525 label-expansion queue had 25 candidate rows in 8 groups,
  with 20 ready for label review. It is preserved as
  `artifacts/v3_label_expansion_candidates_525_pre_batch.json`.
- The accepted 525 decision batch added 24 countable labels and left 7
  review-state decisions pending.
- The post-batch 525 label-expansion queue has 0 ready candidates because all
  525-slice rows are either countable or explicitly in review state.

## Candidate Groups

Likely in-scope seed candidates to review first:

- `m_csa:518`, `m_csa:519`, `m_csa:520`, `m_csa:522`, and `m_csa:523`:
  high-scoring Ser-His-Asp/Glu lipase or palmitoyl hydrolase candidates.
- `m_csa:516` and `m_csa:517`: ligand-supported metal-dependent carbonate
  dehydratase candidates.
- `m_csa:506`: ligand-supported flavin dehydrogenase/reductase candidate.

Likely out-of-scope or boundary controls:

- `m_csa:503`: dehydratase chemistry with only role-inferred metal-hydrolase
  retrieval support.
- `m_csa:504`, `m_csa:513`, and `m_csa:514`: phosphoryl-transfer chemistry
  below the abstention floor.
- `m_csa:505` and `m_csa:512`: sulfur/disulfide transfer or redox chemistry
  outside the current seed set.
- `m_csa:507` and `m_csa:508`: ATPase/protein-splicing contexts below the
  abstention floor.
- `m_csa:524` and `m_csa:525`: acetyltransferase chemistry below the
  abstention floor.
- `m_csa:511`: prolyl isomerase chemistry outside current seed fingerprints.
- `m_csa:509`, `m_csa:521`, `m_csa:526`, and `m_csa:527`: not ready for
  automatic label review because fewer than three residues are resolved or
  retrieval support is below the review threshold.

## Guardrails

- The 525 evaluation against the 523 countable labels keeps 0 out-of-scope
  false non-abstentions, 0 hard negatives, and 0 near misses at threshold
  `0.4115`.
- The same four evidence-limited in-scope abstentions remain:
  `m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430`.
- The 525 score-margin artifact has `correct_positive_score_separation_gap`
  `0.0131`; the all-in-scope score gap remains negative because the four
  evidence-limited positives are intentionally abstained.
- Do not reprocess the 525 batch. Continue from the 550 accepted state and
  use the review-state registry when generating future queues so deferred rows
  are not rediscovered as unlabeled candidates.
