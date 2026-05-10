# 550-Entry Label Queue Notes

These notes cover the 550-entry label-factory batch after the accepted 525
countable batch.

## Queue State

- Countable curated labels advanced from 523 to 546 after the accepted
  550-entry batch.
- Review-state labels advanced to 550, including pending `needs_expert_review`
  placeholders from `m_csa:494`, `m_csa:510`, `m_csa:529`, `m_csa:534`, and
  five boundary-control rows.
- 550 geometry artifacts contain 549 entries and 539 entries with pairwise
  geometry.
- The pre-batch 550 label-expansion queue had 25 candidate rows in 9 groups,
  with 23 ready for label review.
- The accepted 550 decision batch added 23 countable labels and left 9
  review-state decisions pending.
- The post-batch 550 label-expansion queue has 0 ready candidates because all
  550-slice rows are either countable or explicitly in review state.

## Likely In-Scope Seed Candidates

- `m_csa:528` phospholipase A2 and `m_csa:546` fructose-bisphosphatase:
  ligand-supported metal-dependent hydrolysis candidates with strong retrieval
  support.
- `m_csa:545` 1-aminocyclopropane-1-carboxylate deaminase: ligand-supported
  PLP candidate.
- `m_csa:551` phenol 2-monooxygenase: ligand-supported flavin candidate.
- `m_csa:549` exodeoxyribonuclease: role-inferred metal-dependent nuclease
  candidate close to the abstention floor; route through review before
  counting.

## Likely Boundary Or Out-Of-Scope Controls

- `m_csa:534`, `m_csa:535`, `m_csa:537`, `m_csa:540`, and `m_csa:541`:
  ATP/GTP/ligase or synthetase phosphate-transfer contexts that may mimic
  metal hydrolase evidence.
- `m_csa:529`: phospholipase A2 text has ester hydrolysis evidence but current
  retrieval lacks local cofactor support; review carefully.
- `m_csa:530`, `m_csa:532`, `m_csa:533`, and `m_csa:542`: lower-scoring
  metal-like controls below the abstention floor.
- `m_csa:543`: prenyl/diphosphate synthase chemistry outside current seed
  fingerprints.
- `m_csa:544`: UDP-sugar epimerase/elimination chemistry outside current seed
  fingerprints.
- `m_csa:547`: dioxygenase chemistry with role-inferred metal support, not a
  hydrolase label without stronger evidence.
- `m_csa:548`: glycosyl hydrolase chemistry should remain outside the current
  Ser-His-Asp/Glu hydrolase seed unless a new glycosidase seed is introduced.
- `m_csa:552`: aconitase/dehydratase chemistry should not be counted as a
  Ser-His hydrolase merely because of serine/general-base text.
- `m_csa:531` and `m_csa:536`: not ready for automatic label review because
  geometry is not OK and fewer than three residues are resolved.

## Guardrails

- The 550 evaluation against the 546 countable labels keeps 0 out-of-scope
  false non-abstentions, 0 hard negatives, and 0 near misses at threshold
  `0.4115`.
- The 550 batch acceptance check passed with 23 accepted new labels and 9
  pending review-state decisions. Do not reprocess the 550 batch.
- Keep the accepted 550 batch and the pending review-state labels separate:
  `artifacts/v3_countable_labels_batch_550.json` is the countable registry,
  while `artifacts/v3_imported_labels_batch_550.json` is the review-state
  registry for suppressing already-deferred rows in future queue generation.
