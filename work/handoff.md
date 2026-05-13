# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval and label-factory quality
automation. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, 450-, 475-, 500-, 525-, 550-, 575-,
600-, 625-, 650-, 675-, 700-, 725-, 750-, 775-, 800-, 825-, 850-, 875-,
900-, 925-, 950-, 975-, and 1000-entry
curated slices. The 500-entry and larger
slices are countable only through the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
679 countable labels. Review-state registries preserve pending
`needs_expert_review` rows separately so unresolved evidence gaps do not count
as benchmark labels.

## Repository

Local path:

```text
/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth
```

GitHub:

```text
https://github.com/VivekVardhanArrabelli/catalytic-earth
```

## Operating Rules

1. Acquire `.git/catalytic-earth-automation.lock` before work; the tested
   `automation-lock` CLI command can enforce the same atomic lock rules.
2. Sync with `git fetch origin` and `git pull --ff-only origin main`.
3. Read `README.md`, `work/scope.md`, `work/status.md`, and this file.
4. Run `PYTHONPATH=src python -m unittest discover -s tests`.
5. Work productively until 50 elapsed wall-clock minutes, then wrap.
6. During wrap, update stale docs, log measured time, regenerate status,
   commit, push, verify `HEAD == origin/main`, and release the lock only when
   the worktree is clean.

## Recent Project Progress

- Recovered a stale automation lock with a dirty worktree and finalized the
  coherent in-progress label-factory scaling work rather than starting a
  conflicting tranche.
- Accepted gated 625-, 650-, 675-, and 700-entry label-factory batches. The
  675 batch added only `m_csa:666`; the 700 batch added `m_csa:686`,
  `m_csa:688`, `m_csa:694`, `m_csa:697`, and `m_csa:699`.
- Tightened provisional review rules so Ser-His mechanism text paired with a
  metal-dependent top hit stays `needs_expert_review` unless explicit metal
  catalysis evidence is present.
- Added an active-learning gate requiring all unlabeled candidate rows to be
  retained even when the ranked queue is capped.
- Added `artifacts/v3_label_factory_batch_summary.json` to aggregate accepted
  batches, review debt, gate status, and active-queue retention.
- Added `artifacts/v3_review_debt_summary_650.json` to rank 53 evidence-gap
  rows for the next review pass.
- Added preview triage artifacts
  `artifacts/v3_review_evidence_gaps_675_preview.json` and
  `artifacts/v3_review_debt_summary_675_preview.json` so the 675 promotion
  decision can inspect evidence gaps first.
- Added `artifacts/v3_label_factory_preview_summary_675.json` to summarize the
  unpromoted preview's acceptance, pending-review, gate, and queue-retention
  metrics.
- Added `artifacts/v3_label_preview_promotion_readiness_675.json`; it is
  mechanically ready but recommends review before promotion because preview
  review debt increased, and it carries new-debt entry ids and next-action
  counts for audit. The gate requires preview summary counts to match
  acceptance and explicit unlabeled-candidate retention.
- After the preview-readiness gate was in place, used the remaining productive
  work window to expose carried/new debt entry ids and next-action counts in
  durable artifacts and regression tests.
- Added `work/label_preview_675_notes.md` with the accepted-label profile and
  top evidence gaps to inspect before promotion.
- Added `artifacts/v3_label_scaling_quality_audit_675_preview.json` and a
  batch-acceptance review-gap gate. The 675 preview now defers
  below-threshold evidence-limited negatives instead of counting them.
- Added graph-derived exact-UniProt sequence-cluster proxy artifacts for 675
  and 700 and attached them to scaling-quality audits; both report 0 missing
  assignments and 0 near-duplicate hits among audited rows.
- Extended geometry slice summaries, regression tests, and performance timing
  through the 700-entry countable slice.
- Added `work/label_preview_700_notes.md` with the accepted-label profile and
  highest-priority 700 review-debt rows.
- Remaining-time plan executed before wrap-up: after the 700 gate accepted five
  clean labels but review debt rose to 81 rows, stopped tranche growth and
  focused on sequence-cluster audit coverage, review-debt notes, regression
  tests, and documentation.
- Added `analyze-review-debt-remediation` and
  `scan-review-debt-alternate-structures` so accepted-700 review debt is
  repairable without counting new labels. The focused 20-row remediation
  artifact, full 81-row remediation artifact, and 152-PDB alternate-structure
  scan now keep structure-wide cofactor hits separate from local active-site
  support.
- Remaining-time plan for the 700 review-debt repair run: after the remediation
  commands and target regression tests passed before the productive-work
  boundary, rerun the deterministic remediation, scaling-quality audit, batch
  summary, validation, and full test suite; use any remaining time to check
  docs for stale current-state claims rather than opening another tranche.
- Remaining-time plan executed for the remap run: after conservative
  alternate-PDB residue remapping worked on the focused 700 scan, used the
  remaining productive window to run a complete all-debt bounded scan, add a
  review-only remap lead summary command, regenerate artifacts, and verify
  targeted tests instead of reopening label count growth.
- Remaining-time plan for the expert-decision run: after the dedicated
  expert-label decision export passed, use the remaining productive window to
  harden countable-import refusal, add repair-candidate ranking, make the gate
  and scaling audit require the repair-candidate summary, refresh artifact
  regression coverage, and document the next non-countable repair subset
  instead of reopening 725+ label growth.
- Remaining-time plan executed for this recovery run: after the local-evidence
  gap audit was coherent and tests passed, added a dedicated local-evidence
  review export, no-decision batch, repair plan, factory/scaling-quality gates,
  and countable-import refusal before updating docs. Count growth stayed
  stopped at 624 labels.
- This run reduced review-only local-evidence debt without count growth:
  the 4 reaction/substrate repair lanes (`m_csa:592`, `m_csa:643`,
  `m_csa:654`, `m_csa:662`) are closed as reviewed out-of-scope repair-only
  rows, the 3 explicit alternate-residue lanes (`m_csa:567`, `m_csa:578`,
  `m_csa:667`) now have concrete sourcing requests across 34 alternate PDB
  structures, and the review-only import-safety audit confirms the mismatch,
  expert-decision, and local-evidence decision batches add 0 countable labels.
- Implemented the expert-reviewed ATP/phosphoryl-transfer fingerprint-family
  expansion for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP.
  The expansion is wired through ontology records, reaction/substrate mismatch
  review export mapping, family-propagation blockers, active-learning priority,
  adversarial negatives, gate checks, scaling-quality audit, regression tests,
  and documentation while keeping every mapped row non-countable.
- Accepted the gated 725-entry label-factory batch. The batch added
  `m_csa:705`, `m_csa:709`, `m_csa:714`, `m_csa:716`, `m_csa:723`, and
  `m_csa:727` as clean countable labels, raising the canonical registry to 630
  labels while leaving 100 review-state rows non-countable.
- Added accepted-725 review-only repair artifacts: expert-label decision export
  for 95 rows, 25-row local-evidence gap audit/export/repair plan, 8 explicit
  alternate residue-position requests, review-only import-safety audit, focused
  alternate-structure scan, remap-local audit for `m_csa:712`, ontology-gap
  audit, learned-retrieval manifest, sequence-similarity failure-set audit, and
  scaling-quality audit.
- Added `artifacts/v3_accepted_review_debt_deferral_audit_725.json`, which
  explicitly defers all 100 accepted-725 review-state rows with 0 countable
  candidates and upgrades the 725 gate to 21/21 checks.
- Accepted the gated 750-entry label-factory batch. The batch added
  `m_csa:728`, `m_csa:733`, `m_csa:735`, `m_csa:739`, `m_csa:740`,
  `m_csa:742`, and `m_csa:750` as clean countable labels, raising the
  canonical registry to 637 labels while leaving 118 review-state rows
  non-countable.
- Added `artifacts/v3_accepted_review_debt_deferral_audit_750.json`, which
  explicitly defers all 118 accepted-750 review-state rows with 0 countable
  candidates and upgrades the post-batch 750 gate to 20/20 checks.
- Accepted the gated 775-entry label-factory batch. The batch added
  `m_csa:754`, `m_csa:758`, `m_csa:759`, `m_csa:762`, and `m_csa:776` as
  clean countable labels, raising the canonical registry to 642 labels while
  leaving 138 review-state rows non-countable.
- Tightened the provisional Ser-His hydrolase path so `m_csa:771`-style
  Ser-His text with counterevidence remains `needs_more_evidence` and is
  classified as a text-leakage risk rather than counted.
- Accepted the gated 800-, 825-, and 850-entry label-factory batches. The
  batches added ten clean countable labels total, raising the canonical
  registry to 652 labels while leaving 203 review-state rows non-countable.
- Added geometry-feature row reuse through `build-geometry-features
  --reuse-existing` so bounded tranches can reuse unchanged geometry rows
  instead of rebuilding every prior entry.
- Tightened provisional metal-hydrolase promotion so `m_csa:836`-style
  role-inferred metal-hydrolase candidates without local ligand support remain
  `needs_more_evidence` rather than counted.
- Accepted the gated 875-, 900-, 925-, and 950-entry label-factory batches.
  The batches added 21 clean countable labels total, raising the canonical
  registry to 673 labels while leaving 282 review-state rows non-countable.
- Added `expert_review_decision_needed` as an explicit scaling-quality issue
  class so PLP-supported rows such as `m_csa:865` are classified as
  non-countable external-review debt rather than blocking promotion as
  unclassified review debt.
- Accepted the gated 975- and 1,000-entry label-factory batches, raising the
  canonical registry to 679 countable labels while leaving 326 review-state
  rows non-countable.
- Opened the bounded 1,025 preview. The preview gate passes 21/21 checks, but
  acceptance is false because it adds 0 clean countable labels and review debt
  rises to 329 rows. The source-scale audit records 1,003 observed M-CSA source
  records and shifts next work toward external-source transfer.
- Added external-source transfer scaffolding for the post-M-CSA path:
  source-limit audit, transfer manifest, query manifest, OOD calibration plan,
  30-row UniProtKB/Swiss-Prot read-only candidate sample, guardrail audit,
  artifact regression tests, and unit tests. All external candidates are
  non-countable.
- Hardened the external-source transfer path with a review-only candidate
  manifest, candidate-manifest audit, lane-balance audit, evidence plan,
  evidence request export, external review-only import-safety audit, 11/11
  transfer gate, bounded Rhea reaction-context sample, and reaction-context
  guardrail audit. The canonical registry remains at 679 labels; 0 external
  labels are countable.
- Added broad/incomplete EC routing and a review-only active-site evidence
  queue for the external path: seven candidates require broad-EC attention,
  three broad-only rows are deferred before active-site mapping, 25 candidates
  are queued for active-site evidence, and 0 external labels are countable.
- Advanced the external path from evidence queue to bounded review-only
  controls: sampled UniProtKB active-site features for all 25 ready external
  rows, found 15 active-site-feature-supported candidates and 10 feature gaps,
  queued 12 candidates for heuristic-control prototyping, mapped all 12
  heuristic-ready controls onto current AlphaFold CIF structures, ran the
  current geometry heuristic, and recorded a metal-hydrolase top1 collapse plus
  9 scope/top1 mismatches in
  `artifacts/v3_external_source_failure_mode_audit_1025.json`. The external
  transfer gate now passes 33/33 review-only checks and still adds 0 countable
  labels.
- Expanded external-source controls from the 4-control heuristic sample to all
  12 heuristic-ready AlphaFold controls, added review-only control-repair,
  representation-control, binding-context, full reaction-context, and
  sequence-holdout artifacts, and raised the external transfer gate to 33/33.
  External candidates still add 0 countable labels and are not import-ready.
- Added external-source repair controls for the prior repair pass: feature-proxy
  representation comparison, broad-EC disambiguation, active-site gap source
  requests, and a sequence-neighborhood plan. The external transfer gate now
  passes 38/38 review-only checks while keeping every external row non-countable.
- Added bounded sequence-neighborhood screening and candidate-level import
  readiness auditing. That intermediate external transfer gate passed 41/41
  review-only checks while keeping every external row non-countable and
  import-blocked.
- Added bounded sequence-alignment verification for the sequence-neighborhood
  top hits plus an active-site sourcing queue for the 10 external active-site
  gaps. That checkpoint raised the external transfer gate to 45/45 review-only
  checks while keeping every external row non-countable and import-blocked.
- Added source-review exports for active-site sourcing and complete sequence
  search, a representation-backend plan, and an integrated external blocker
  matrix. The external transfer gate now passes 53/53 review-only checks while
  keeping every external row non-countable and import-blocked.
- Added active-site sourcing resolution and representation backend samples for
  the external 1,025 transfer path. The active-site resolution re-checks all 10
  gap rows against UniProt feature evidence, finds 0 explicit active-site
  residue sources, and keeps 7 binding-plus-reaction rows and 3 reaction-only
  rows non-countable. The deterministic sequence k-mer baseline covers all 12
  planned representation controls and flags `P60174` as a representation
  near-duplicate holdout; the canonical ESM-2 sample covers all 12 controls,
  flags 3 representation near-duplicate holdouts, and keeps the external
  transfer gate at 59/59 review-only checks with 0 import-ready labels.
- Added sequence/fold-distance holdout evaluation for the accepted countable
  registry in both the 1,000 and 1,025 slice contexts. No Foldseek, MMseqs2,
  BLAST, or DIAMOND executable was available locally, so
  `artifacts/v3_sequence_distance_holdout_eval_1000.json` and
  `artifacts/v3_sequence_distance_holdout_eval_1025.json` explicitly label the
  split as a deterministic proxy using exact UniProt reference clusters,
  selected-structure identifiers, and active-site geometry buckets. The
  held-out partition has 136 rows, 135/136 rows passing the strict
  low-neighborhood proxy, 0 out-of-scope false non-abstentions, held-out
  evaluable in-scope top1 accuracy and retention of `0.9767`, and
  top1/top3 accuracy among retained held-out evaluable rows of `1.0000`.
- Added the first bounded learned representation backend sample for external
  pilot readiness. `artifacts/v3_external_source_representation_backend_sample_1025.json`
  computes 12 ESM-2 (`facebook/esm2_t6_8M_UR50D`) candidate-control rows with
  320-dimensional embeddings, keeps all rows review-only and non-countable,
  flags 3 representation-near-duplicate holdouts, and emits 12
  learned-vs-heuristic disagreement rows. The existing 12-row deterministic
  k-mer sample remains the baseline/proxy control, and heuristic geometry
  retrieval remains attached as the required baseline.

## Current Metrics

- Curated label registry: 679 bronze automation-curated labels, with 212
  seed-fingerprint positives and 467 out-of-scope labels.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 500-entry countable slice: threshold `0.4115`, 490/498 evaluated labeled
  rows evaluable, 127/131 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and `m_csa:494` preserved as non-countable.
- 525-entry countable slice: threshold `0.4115`, 514/522 evaluated labeled
  rows evaluable, 135/139 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 550-entry countable slice: threshold `0.4115`, 535/545 evaluated labeled
  rows evaluable, 140/144 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 575-entry countable slice: threshold `0.4115`, 552/562 evaluated labeled
  rows evaluable, 142/146 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 600-entry countable slice: threshold `0.4115`, 568/578 evaluated labeled
  rows evaluable, 143/147 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 625-entry countable slice: threshold `0.4115`, 584/598 evaluated labeled
  rows evaluable, 144/148 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 25 ready label candidates before the accepted
  batch decisions.
- 650-entry countable slice: threshold `0.4115`, 601/617 evaluated labeled
  rows evaluable, 147/151 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 31 ready label candidates before the accepted
  batch decisions.
- 675-entry countable slice: threshold `0.4115`, 601/618 evaluated labeled
  rows evaluable, 148/152 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 49 ready label candidates after accepting
  `m_csa:666`.
- 700-entry countable slice: threshold `0.4115`, 607/623 evaluated labeled
  rows evaluable, 153/157 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 64 ready label candidates after accepting the five
  clean 700 labels.
- 725-entry countable slice: threshold `0.4115`, 613/629 evaluated labeled
  rows evaluable, 159/163 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 85 ready label candidates before accepting six
  clean 725 labels.
- 750-entry countable slice: threshold `0.4115`, 620/636 evaluated labeled
  rows evaluable, 166/170 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 95 ready label candidates after accepting seven
  clean 750 labels.
- 775-entry countable slice: threshold `0.4115`, 625/641 evaluated labeled
  rows evaluable, 171/175 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 113 ready label candidates after accepting five
  clean 775 labels.
- 800-entry countable slice: threshold `0.4115`, 629/645 evaluated labeled
  rows evaluable, 175/179 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, and 4 evidence-limited
  in-scope abstentions after accepting four clean 800 labels.
- 825-entry countable slice: threshold `0.4115`, 632/648 evaluated labeled
  rows evaluable, 178/182 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, and 4 evidence-limited
  in-scope abstentions after accepting three clean 825 labels.
- 850-entry countable slice: threshold `0.4115`, 635/651 evaluated labeled
  rows evaluable, 181/185 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 97 bronze-to-silver promotion candidates after
  accepting three clean 850 labels.
- 950-entry countable slice: threshold `0.4115`, 656/672 evaluated labeled
  rows evaluable, 202/206 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 111 bronze-to-silver promotion candidates after
  accepting six clean 950 labels.
- Evidence-limited abstentions remain `m_csa:132`, `m_csa:353`, `m_csa:372`,
  and `m_csa:430`.
- Retained evidence-limited positives remain `m_csa:41`, `m_csa:108`,
  `m_csa:160`, `m_csa:446`, and `m_csa:486`; the smallest retained
  evidence-limited margin is `0.013`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is still `m_csa:65`, a
  metal-dependent hydrolase hit `0.0131` below the correct-positive floor.
- Label factory at 950: 111 bronze-to-silver promotions proposed, 389 active
  learning review rows queued, 100 adversarial negatives mined, 277 active
  expert-label decision rows routed through a review-only export, complete
  repair-candidate summary, priority repair guardrail audit, complete 84-row
  local-evidence gap audit/export, repair plan, review-only import-safety
  audit, ATP/phosphoryl-transfer family expansion, and 21/21 gate checks
  passing.
- Label batch summary: 19/19 accepted batches, 0 blockers, 0 hard negatives,
  0 near misses, 0 false non-abstentions, 0 actionable in-scope failures, and
  all active queues retained their unlabeled candidates.
- Latest accepted batch acceptance: 6 additional labels accepted for counting,
  282 review-state decisions pending, 673 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- Accepted-950 deferral audit: all 282 review-state rows explicitly remain
  non-countable, with 84 priority local-evidence rows audited/exported, 32
  explicit alternate residue-position requests, 19 new 950-preview review-debt
  rows classified and deferred, and 0 accepted-label overlap.
- Accepted-1000 current state: 679 countable labels, 326 review-state rows
  explicitly deferred, 21/21 gate checks passing, 0 hard negatives, 0 near
  misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures,
  and `m_csa:986` kept non-countable as a low-score local-heme boundary row.
- 1,025 preview state: 21/21 preview gate checks passing but 0 accepted new
  labels, so the preview is not promoted. Review debt rises to 329 rows with
  new rows `m_csa:1003`, `m_csa:1004`, and `m_csa:1005`; all remain
  non-countable. Source scaling is now the bottleneck: the graph exposes 1,003
  M-CSA records, and external-source transfer artifacts now provide a
  review-only UniProtKB/Swiss-Prot path with 30 non-countable sample candidates.
- Sequence/fold-distance holdout state: `artifacts/v3_sequence_distance_holdout_eval_1000.json`
  and `artifacts/v3_sequence_distance_holdout_eval_1025.json` evaluate the
  accepted countable registry under a proxy low-neighborhood partition. Both
  contexts evaluate 678 labeled retrieval rows and hold out 136 rows. Held-out
  metrics are 44 in-scope rows, 43 evaluable in-scope rows, 92 out-of-scope
  rows, 0 held-out out-of-scope false non-abstentions, `0.9767` held-out
  evaluable top1 accuracy, `1.0000` held-out evaluable top3 accuracy among
  retained rows, and `0.9767` held-out evaluable retention. In-distribution
  evaluable top1 accuracy is `0.9881`, and top3 accuracy among retained
  in-distribution rows is `1.0000`. These are proxy metrics only: real
  <=30% sequence-identity or <0.7 TM-score clustering was not computed because
  no local clustering executable was available.
- Learned representation state: `artifacts/v3_external_source_representation_backend_sample_1025.json`
  computes a 12-row ESM-2 sample for external mapped controls with
  `embedding_backend_available=true`, vector dimension `320`, 0 embedding
  failures, 3 representation-near-duplicate holdouts, 12 learned-vs-heuristic
  disagreement rows, and 0 countable/import-ready rows. The audit
  `artifacts/v3_external_source_representation_backend_sample_audit_1025.json`
  is guardrail-clean. This is pilot-priority evidence only; sequence search,
  active-site sourcing, review decisions, and full factory gates remain
  required before any import.
- 725 post-batch review surface: all 95 unlabeled candidates are retained in a
  207-row active-learning queue; 95 expert-label decision rows are exported as
  review-only no-decision items; 25 priority local-evidence lanes are audited
  and exported with 0 countable candidates; 8 alternate residue-position
  requests are explicit; 24 reaction/substrate mismatch lanes remain
  non-countable; the scaling-quality audit classifies all 24 new review-debt
  rows and leaves 0 unclassified.
- 725 discovery controls: the mechanism ontology gap audit records 121
  review-only scope-pressure rows, the learned-retrieval manifest stages 568
  eligible rows with the heuristic baseline as control, and the
  sequence-similarity failure-set audit keeps 2 duplicate clusters as
  non-countable controls.
- Historical accepted-700 repair context remains below because the 725 repair
  artifacts build on those same review-only lanes.
- 700 post-batch active-learning queue: all 76 unlabeled candidates are
  retained; no unlabeled rows are omitted by the queue limit. The queue now
  includes `reaction_substrate_mismatch_value` and ranks 18 kinase or ATP
  phosphoryl-transfer rows with hydrolase top hits for expert review.
- 700 expert-label decision review export: all 76 active-queue
  `expert_label_decision_needed` rows are exported as `no_decision`, 0 are
  countable candidates, 56 carried review-debt rows and 20 new review-debt rows
  are linked, and the 7 reaction/substrate mismatch lanes are already covered by
  the dedicated mismatch export. Risk flags include 50 cofactor-family
  ambiguity rows, 29 counterevidence-boundary rows, 14 active-site
  mapping/structure-gap rows, 9 text-leakage/nonlocal-evidence risks, 7
  reaction/substrate mismatches, 7 substrate-class boundaries, 6 sibling
  mechanism confusions, and 2 Ser-His/metal-boundary rows.
- 700 expert-label repair candidates:
  `artifacts/v3_expert_label_decision_repair_candidates_700.json` ranks 30
  review-only repair candidates and buckets all 76 rows as 14 active-site
  mapping/structure-gap repairs, 7 text-leakage/nonlocal-evidence guardrails,
  30 cofactor-evidence repairs, 1 Ser-His/metal-boundary review, 1 sibling
  mechanism-boundary review, and 23 external expert-label decisions.
- 700 expert-label repair guardrail audit: 21 priority repair rows remain
  non-countable, including 14 active-site mapping/structure-gap rows and 9
  text-leakage/nonlocal-evidence rows. Three conservative-remap local expected
  family evidence leads (`m_csa:577`, `m_csa:592`, and `m_csa:641`) remain
  review-only, with 0 countable label candidates.
- 700 mechanism ontology gap audit: 115 non-countable scope-pressure rows
  expose transferase phosphoryl, lyase, isomerase, oxidoreductase long-tail,
  methyl-transfer, and glycan chemistry pressure without creating a new
  ontology family from keyword evidence alone.
- 700 learned retrieval manifest: 562 eligible labeled entries are staged for a
  future learned-representation path, with 160 emitted rows and the current
  heuristic geometry retrieval preserved as the required control.
- 700 sequence-similarity failure-set audit: 2 exact-reference duplicate
  clusters are kept as non-countable controls before any family propagation or
  learned-retrieval split.
- Review debt summary: 81 evidence-gap rows, all `needs_more_evidence`, with
  61 carried rows and 20 new rows. New-debt next actions are 16 alternate
  structure/cofactor-source inspections, 2 expert-review decisions, 1 family
  boundary review, and 1 local cofactor/active-site mapping check.
- 700 scaling-quality audit: 20 new review-debt rows classified, 0 accepted
  labels with review debt, 0 hard negatives, 0 near misses, 0 near-duplicate
  hits, observed ontology scope pressure, family-propagation boundary,
  cofactor ambiguity, reaction/substrate mismatch, active-site mapping gaps,
  active-learning queue concentration, and alternate-structure hits lacking
  local support.
- 700 remediation plan: all 20 new debt rows have gap detail, graph context,
  selected geometry context, and a repair bucket. Buckets are 12
  alternate-PDB ligand scans, 3 external cofactor-source reviews, 1 active-site
  mapping repair, 1 local mapping/structure-selection review, 1 family-boundary
  review, and 2 expert label decisions.
- 700 full debt remediation plan: all 81 review-debt rows are mapped. Buckets
  are 37 alternate-PDB ligand scans, 9 local mapping/structure-selection
  reviews, 9 external cofactor-source reviews, 7 family-boundary reviews,
  16 expert label decisions, and 3 active-site mapping repairs. Sixty-nine
  rows have alternate PDBs but 0 alternate-PDB M-CSA residue-position support.
- 700 focused alternate-structure scan: 13 structure-scan rows, 152 candidate
  PDB structures, 0 fetch failures, 63 alternate-PDB structures with
  conservative remapped active-site positions, 3 structure-wide
  expected-family hit rows (`m_csa:679`, `m_csa:696`, `m_csa:698`), and 0
  local active-site expected-family hit rows. These hits remain review-only
  evidence.
- 700 all-debt bounded alternate-structure scan: 46 scan-candidate review-debt
  rows, all 739 candidate PDB structures scanned, 0 fetch failures, 362
  alternate-PDB structures with conservative remapped active-site positions,
  19 expected-family hit rows, and 3 review-only local expected-family hit
  rows from remaps (`m_csa:577`, `m_csa:592`, `m_csa:641`). The remap lead
  summary records 44 review-only leads and 0 countable label candidates.
- 700 remap-local audit: `m_csa:577` and `m_csa:641` require expert
  family-boundary review, `m_csa:592` requires expert reaction/substrate review,
  all three require strict remap guardrails, and there are 0 structure-selection
  candidates after reaction mismatch triage.
- 700 reaction/substrate mismatch audit: 18 active-queue hydrolase-top1 rows
  with kinase or ATP phosphoryl-transfer text are routed to expert
  reaction/substrate review; 0 are countable.
- 700 family-propagation guardrails now block 24 reported rows with
  `reaction_substrate_mismatch` before propagation or countable promotion;
  14 of those rows are retained by a priority override beyond `max_rows`.
- 700 reaction/substrate mismatch review export: all 24 family-guardrail lanes
  are exported together, split into 17 current out-of-scope labels and 7
  unlabeled pending-review rows. The export records 0 labeled seed mismatches,
  and now supplies the expert-reviewed pressure surface for the ePK, ASKHA,
  ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP ontology expansion. The
  expansion artifact maps 20 supported lanes across all nine families, records
  4 non-target hints and 0 unsupported family mappings, and keeps
  `countable_label_candidate_count=0`. Its current review-only decision batch
  routes the 7 unlabeled rows to reviewed out-of-scope repair decisions,
  rejects 17 current controls, and adds 0 countable labels.
- Structure mapping: 19 total mapping issues at 700.
- Local performance was regenerated on 700 artifacts in `artifacts/perf_report.json`.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m catalytic_earth.cli automation-lock --lock-dir .git/catalytic-earth-automation.lock status
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --out artifacts/v3_label_expansion_candidates_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --labels data/registries/curated_mechanism_labels.json --out artifacts/v3_family_propagation_guardrails_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --labels artifacts/v3_countable_labels_batch_675.json --out artifacts/v3_family_propagation_guardrails_700_preview_batch.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --baseline-review-debt artifacts/v3_review_debt_summary_675.json --max-rows 45 --out artifacts/v3_review_debt_summary_700.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-review-debt-remediation --review-debt artifacts/v3_review_debt_summary_700.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --graph artifacts/v1_graph_700.json --geometry artifacts/v3_geometry_features_700.json --debt-status new --out artifacts/v3_review_debt_remediation_700.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-review-debt-remediation --review-debt artifacts/v3_review_debt_summary_700.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --graph artifacts/v1_graph_700.json --geometry artifacts/v3_geometry_features_700.json --debt-status all --out artifacts/v3_review_debt_remediation_700_all.json
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures --remediation artifacts/v3_review_debt_remediation_700.json --max-entries 13 --max-structures-per-entry 60 --out artifacts/v3_review_debt_alternate_structure_scan_700.json
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures --remediation artifacts/v3_review_debt_remediation_700_all.json --max-entries 46 --max-structures-per-entry 80 --out artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt-remap-leads --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json --remediation artifacts/v3_review_debt_remediation_700_all.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --out artifacts/v3_review_debt_remap_leads_700_all_bounded.json
PYTHONPATH=src python -m catalytic_earth.cli audit-review-debt-remap-local-leads --remap-leads artifacts/v3_review_debt_remap_leads_700_all_bounded.json --remediation artifacts/v3_review_debt_remediation_700_all.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --out artifacts/v3_review_debt_remap_local_lead_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-reaction-substrate-mismatches --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --out artifacts/v3_reaction_substrate_mismatch_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-reaction-substrate-mismatch-review-export --reaction-substrate-mismatch-audit artifacts/v3_reaction_substrate_mismatch_audit_700.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json --labels data/registries/curated_mechanism_labels.json --out artifacts/v3_reaction_substrate_mismatch_review_export_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch --review artifacts/v3_reaction_substrate_mismatch_review_export_700.json --batch-id 700_reaction_substrate_mismatch_review --reviewer automation_label_factory --out artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-expert-label-decision-repair-guardrails --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json --remap-local-lead-audit artifacts/v3_review_debt_remap_local_lead_audit_700.json --out artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-expert-label-decision-local-evidence-gaps --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json --out artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-expert-label-decision-local-evidence-review-export --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --labels data/registries/curated_mechanism_labels.json --out artifacts/v3_expert_label_decision_local_evidence_review_export_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch --review artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --batch-id 700_expert_label_decision_local_evidence_review --reviewer automation_label_factory --out artifacts/v3_expert_label_decision_local_evidence_decision_batch_700.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-expert-label-decision-local-evidence-repair-plan --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --out artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json
PYTHONPATH=src python -m catalytic_earth.cli resolve-expert-label-decision-local-evidence-repair-lanes --expert-label-decision-local-evidence-repair-plan artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json --reaction-substrate-mismatch-decision-batch artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json --out artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-explicit-alternate-residue-position-requests --expert-label-decision-local-evidence-repair-plan artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json --review-debt-remediation artifacts/v3_review_debt_remediation_700_all.json --graph artifacts/v1_graph_700.json --out artifacts/v3_explicit_alternate_residue_position_requests_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-review-only-import-safety --labels data/registries/curated_mechanism_labels.json --review artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json --review artifacts/v3_expert_label_decision_decision_batch_700.json --review artifacts/v3_expert_label_decision_local_evidence_decision_batch_700.json --out artifacts/v3_review_only_import_safety_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_700.json --applied-label-factory artifacts/v3_label_factory_applied_labels_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_700.json --expert-review-export artifacts/v3_expert_review_export_700_post_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json --expert-label-decision-review-export artifacts/v3_expert_label_decision_review_export_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700.json --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --expert-label-decision-local-evidence-repair-resolution artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json --explicit-alternate-residue-position-requests artifacts/v3_explicit_alternate_residue_position_requests_700.json --review-only-import-safety-audit artifacts/v3_review_only_import_safety_audit_700.json --atp-phosphoryl-transfer-family-expansion artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json --out artifacts/v3_label_factory_gate_check_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-mechanism-ontology-gaps --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --max-rows 80 --out artifacts/v3_mechanism_ontology_gap_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-learned-retrieval-manifest --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --labels data/registries/curated_mechanism_labels.json --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_700.json --max-rows 160 --out artifacts/v3_learned_retrieval_manifest_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-sequence-similarity-failure-sets --sequence-clusters artifacts/v3_sequence_cluster_proxy_700.json --labels data/registries/curated_mechanism_labels.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --out artifacts/v3_sequence_similarity_failure_sets_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-cluster-proxy --graph artifacts/v1_graph_700.json --out artifacts/v3_sequence_cluster_proxy_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-label-scaling-quality --batch-id 700_preview --acceptance artifacts/v3_label_batch_acceptance_check_700_preview.json --readiness artifacts/v3_label_preview_promotion_readiness_700.json --review-debt artifacts/v3_review_debt_summary_700_preview.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700_preview.json --active-learning-queue artifacts/v3_active_learning_review_queue_700_preview_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700_preview_batch.json --hard-negatives artifacts/v3_hard_negative_controls_700_preview_batch.json --decision-batch artifacts/v3_expert_review_decision_batch_700_preview.json --structure-mapping artifacts/v3_structure_mapping_issues_700.json --expert-review-export artifacts/v3_expert_review_export_700_preview_post_batch.json --sequence-clusters artifacts/v3_sequence_cluster_proxy_700.json --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700.json --remap-local-lead-audit artifacts/v3_review_debt_remap_local_lead_audit_700.json --reaction-substrate-mismatch-audit artifacts/v3_reaction_substrate_mismatch_audit_700.json --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json --expert-label-decision-review-export artifacts/v3_expert_label_decision_review_export_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700.json --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --expert-label-decision-local-evidence-repair-resolution artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json --explicit-alternate-residue-position-requests artifacts/v3_explicit_alternate_residue_position_requests_700.json --review-only-import-safety-audit artifacts/v3_review_only_import_safety_audit_700.json --atp-phosphoryl-transfer-family-expansion artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json --out artifacts/v3_label_scaling_quality_audit_700_preview.json
```

## Next Agent Start Here

User-approved priority override: do not keep adding gates upon gates. The next
runs should follow this ordered worklist unless a concrete repo blocker appears.
Every new artifact, audit, or gate must directly remove one generalization or
external-pilot blocker; otherwise do not build it.

1. Sequence/fold-distance holdout evaluation is now implemented and pinned by
   regression tests. Treat the current artifacts as a proxy-only generalization
   signal, not as proof of <=30% sequence identity or <0.7 TM-score behavior.
   Re-run with Foldseek/MMseqs2 or an equivalent local clustering backend if it
   becomes available.
2. Use the learned representation backend path. A 12-row ESM-2 sample is now
   computed and review-only; next use its learned-vs-heuristic disagreement
   rows to rank external pilot candidates and decide which representation
   repairs are needed. Preserve heuristic geometry retrieval as the baseline.
3. Implement a general selected-PDB override path with provenance and apply the
   holo-preference audit action path for `m_csa:577` and `m_csa:641`. Seed it
   from `v3_structure_selection_holo_preference_audit_700.json` rows where
   `recommendation == "swap_selected_structure"`. Skip `m_csa:592` unless new
   evidence changes the current kinase/reaction-mismatch demotion. Only count
   labels if regenerated gates pass. The 2026-05-13T13:16:40Z run inspected
   this path and did not start it because the selected-PDB override needs a
   general provenance-carrying implementation plus regenerated geometry,
   retrieval, label-eval, factory gate, and acceptance artifacts for affected
   entries.
4. Add the ePK fingerprint conservatively after the holdout signal exists:
   fingerprint JSON, ontology link, minimal abstention/counterevidence rules,
   and tests first. Let gates reveal which stronger sibling-family rules are
   needed before overfitting ePK against ASKHA, ATP-grasp, GHKL, dNK, NDK,
   PfkA, PfkB, and GHMP.
5. Add `transition_state_signature` only after the higher-priority
   generalization and external-pilot blockers are addressed, or if the run is
   otherwise blocked. Keep it validation-only at first.

Concrete user direction for the next runs: stop adding abstract gates unless
they directly unblock the first external-source import pilot. The 1,025
checkpoint already proved the key strategic point: M-CSA-only count growth is
source-limited, while external-source import is not yet ready. The next
valuable work is not a larger gate count; it is a small, evidence-backed
external pilot.

Immediate target: build toward a 5-10 candidate external-source pilot from the
existing 30-row UniProtKB/Swiss-Prot sample. Keep every external row
review-only until active-site, reaction, sequence, representation, review, and
full label-factory gates pass. Do not open another M-CSA-only tranche such as
1,050 as normal progress.

Priority blockers to remove:

1. Source explicit catalytic or active-site residue evidence for the 10
   active-site-feature gap rows using
   `artifacts/v3_external_source_active_site_sourcing_export_1025.json`.
   Binding context and Rhea context are useful, but they do not replace
   catalytic active-site evidence.
2. Complete real near-duplicate or UniRef-style sequence searches for the 28
   rows in `artifacts/v3_external_source_sequence_search_export_1025.json`.
   Exact-reference overlaps and high-similarity rows stay holdout controls, not
   labels.
3. Replace deterministic k-mer proxy controls with a real learned or
   structure-language representation backend, or a clearly executable backend
   interface with a small computed sample. Preserve heuristic geometry
   retrieval as the required control baseline.
4. Rank the 30 external candidates for pilot readiness and choose 5-10 with
   explicit active-site evidence, specific reaction evidence, clean sequence
   holdout status, clean structure mapping, non-collapsed
   heuristic/representation behavior, and no broad-EC ambiguity.
5. Produce a review decision export for the pilot candidates. Keep decisions
   review-only first. Attempt countable import only for candidates that pass
   active-site, reaction, sequence, representation, review, and full factory
   gates.

Definition of done for this pivot: 5-10 named external candidates have
per-row evidence dossiers covering active-site residues, reaction/mechanism
evidence, structure mapping, sequence holdout/near-duplicate status, heuristic
retrieval control, representation control, and remaining blockers. If no
candidate is import-ready, the output should be a ranked blocker list for the
pilot, not more generic audit machinery.

Start from the accepted 1,000 state plus the non-promoted 1,025 preview. The
canonical registry remains at 679 countable labels; the latest accepted labels
are still `m_csa:978`, `m_csa:988`, `m_csa:990`, and `m_csa:994`.

The bounded 1,025 preview remains open but not promotable. The preview gate
passes 21/21 checks, but
`artifacts/v3_label_batch_acceptance_check_1025_preview.json` is not accepted
for counting because it adds 0 clean countable labels. Review debt rises from
326 to 329 rows, with new rows `m_csa:1003`, `m_csa:1004`, and `m_csa:1005`,
all explicitly deferred by
`artifacts/v3_accepted_review_debt_deferral_audit_1025_preview.json`.

The 1,025 run exposed a source-scale bottleneck rather than a label-quality
failure. `artifacts/v3_source_scale_limit_audit_1025.json` records 1,003
observed M-CSA source records for the requested 1,025 tranche and recommends
stopping M-CSA-only count growth. The external-source transfer path is now
gated for review-only evidence collection rather than count growth:
`artifacts/v3_external_source_transfer_manifest_1025.json`,
`artifacts/v3_external_source_query_manifest_1025.json`,
`artifacts/v3_external_ood_calibration_plan_1025.json`,
`artifacts/v3_external_source_candidate_sample_1025.json`,
`artifacts/v3_external_source_candidate_sample_audit_1025.json`,
`artifacts/v3_external_source_candidate_manifest_1025.json`,
`artifacts/v3_external_source_candidate_manifest_audit_1025.json`,
`artifacts/v3_external_source_lane_balance_audit_1025.json`,
`artifacts/v3_external_source_evidence_plan_1025.json`,
`artifacts/v3_external_source_evidence_request_export_1025.json`,
`artifacts/v3_external_source_active_site_evidence_queue_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_audit_1025.json`,
`artifacts/v3_external_source_failure_mode_audit_1025.json`,
`artifacts/v3_external_source_control_repair_plan_1025.json`,
`artifacts/v3_external_source_control_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_audit_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_audit_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_active_site_gap_source_requests_1025.json`,
`artifacts/v3_external_source_sequence_holdout_audit_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_plan_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json`,
`artifacts/v3_external_source_sequence_search_export_1025.json`,
`artifacts/v3_external_source_sequence_search_export_audit_1025.json`,
`artifacts/v3_external_source_import_readiness_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_audit_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json`,
`artifacts/v3_external_source_review_only_import_safety_audit_1025.json`, and
`artifacts/v3_external_source_transfer_gate_check_1025.json` keep
`countable_label_candidate_count=0` and pass a 59/59 review-only transfer gate.
The candidate manifest has 30 UniProtKB/Swiss-Prot rows across six balanced
query lanes; `O15527` and `P42126` are exact-reference overlaps and are routed
to sequence-holdout controls. The evidence plan flags seven broad/incomplete EC
contexts; the active-site queue exports 25 ready evidence rows and defers five
rows, including two exact-reference holdouts and three broad-EC disambiguation
cases.

External active-site and control work is broader now. The UniProtKB feature
sample covers all 25 active-site-ready rows: 15 have active-site features, 10
remain active-site-feature gaps, and all sampled rows remain non-countable. The
heuristic-control queue marks 12 candidates ready for control prototyping and
defers 13 rows. The expanded structure-mapping sample maps all 12
heuristic-ready controls onto current AlphaFold model CIFs, resolves all
requested active-site positions, and then runs the existing geometry retrieval
heuristic as a control. The heuristic is not label-ready: top1 predictions are
9 `metal_dependent_hydrolase`, 2 `heme_peroxidase_oxidase`, and 1
`flavin_dehydrogenase_reductase`, with 9 scope/top1 mismatches. The
failure-mode audit records active-site feature gaps, broad-EC disambiguation
needs, top1 fingerprint collapse, metal-hydrolase collapse, and scope/top1
mismatch as review-only failures to repair before any external label decision.
The active-site feature-gap rows are `O60568`, `P29372`, `P27144`, `A2RUC4`,
`P51580`, `O95050`, `Q9HBK9`, `A5PLL7`, `P32189`, and `Q32P41`.

The new control-repair artifacts turn the current weaknesses into concrete
non-countable repair work. `artifacts/v3_external_source_control_repair_plan_1025.json`
has 25 repair rows: 10 active-site feature gaps, 3 broad-EC disambiguation
rows, and 12 heuristic-control repair rows. The representation control manifest
exposes all 12 mapped controls as future representation rows with embeddings
explicitly not computed and no training labels. The representation comparison
adds feature-proxy controls for all 12 mapped rows, flags 7 metal-hydrolase
collapse rows, preserves 2 glycan-boundary rows, and keeps every row
non-countable. The binding-context repair plan splits the 10 active-site
feature gaps into 7 rows ready for binding-context mapping and 3 rows still
missing binding context; the mapping sample maps 7/7 ready rows with 0 fetch
failures. Binding positions remain repair context only, not catalytic
active-site evidence. The active-site gap source-request artifact now covers
all 10 gaps as review-only sourcing tasks, and the active-site sourcing queue
prioritizes those gaps into 7 mapped-binding-context rows and 3 primary-source
rows.

`artifacts/v3_external_source_reaction_evidence_sample_1025.json` now queries
Rhea for all 30 external candidates. It records 64 reaction-context rows with 0
fetch failures and remains non-countable. Its companion audit
`artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json` is
guardrail-clean but flags 16 broad-EC context rows across `1.1.1.-`,
`1.11.1.-`, `1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and `4.2.99.-`;
those rows are not specific mechanism evidence. The sequence-holdout audit
keeps `O15527` and `P42126` as exact-reference holdouts and marks the remaining
28 candidates as near-duplicate-search cases before any future import decision.
The broad-EC disambiguation audit finds specific reaction context for all 3
broad-only repair rows, and the sequence-neighborhood plan converts the
sequence surface into 2 exact-holdout rows and 28 near-duplicate search
requests. The sequence-neighborhood sample fetches all 30 external sequences
and 733 current countable M-CSA reference sequences, finds 0 high-similarity
alerts in the bounded unaligned screen, and keeps complete near-duplicate or
UniRef-style search mandatory before import. The bounded alignment verification
checks 90 top-hit pairs, confirms `O15527` and `P42126` as exact holdouts, and
records 88 no-signal pairs. The import-readiness audit keeps 0 rows ready for
label import and records 10 active-site gaps, 2 exact sequence holdouts, 28
complete near-duplicate search requirements, 9 heuristic scope/top1 mismatches,
29 representation-control issues, and 2 alignment-confirmed sequence holdouts.
The sequence-search export converts all 30 rows into no-decision sequence
controls, with 28 complete near-duplicate searches and 2 sequence-holdout tasks.
The active-site sourcing export carries 72 source targets for the 10 active-site
gaps with 0 completed decisions. The active-site sourcing resolution re-checks
those 10 gaps against UniProt feature evidence, records 0 explicit active-site
residue sources, and keeps the 7 binding-plus-reaction rows plus 3 reaction-only
rows non-countable. The representation-backend plan covers 12 mapped controls,
keeps embeddings absent, and requires heuristic-baseline contrast for 9 rows.
The deterministic k-mer representation backend sample computes review-only
sequence controls for all 12 planned rows, flags one representation
near-duplicate holdout (`P60174` against `m_csa:324`/`P00940`), and does not
replace the future learned or structure-language backend requirement. The
transfer blocker matrix joins all 30 candidates into
prioritized review-only next actions: 7 primary literature/PDB active-site
source reviews for rows where the UniProt re-check found no explicit active-site
positions, 3 primary active-site source tasks, 18 near-duplicate sequence
searches, and 2 sequence holdouts. Its audit now records 10 active-site
resolution rows, 12 representation sample rows, and one representation
near-duplicate alert. Its dominant next-action fraction is 0.6000 and dominant
lane fraction is 0.1667, so the queue has not collapsed to one action or one
chemistry lane.

Label-quality confidence call for the 2026-05-13T10:12:41Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
work. Evidence at run start: `validate` and 259 unit tests passed, the 1,025
preview gate remains clean but non-promotable with 0 accepted new labels, the
external transfer gate passes 45/45 review-only checks, hard negatives remain
0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
the import-readiness audit keeps 0 external rows import-ready, and active-site,
sequence-neighborhood, heuristic, and representation blockers remain
unresolved. The operational decision is to reduce external-source readiness
uncertainty while keeping every external candidate non-countable.

Remaining-time plan for the 2026-05-13T10:12:41Z run: after adding
active-site sourcing export, complete sequence-search export,
representation-backend planning, the external transfer blocker matrix, and the
53/53 transfer gate, use the remaining productive window for guardrail
hardening, artifact regression tests, full validation, JSON/countable-label
scans, CLI help checks, and documentation freshness. Do not open an external
label decision or import path until source evidence, complete sequence search,
real representation controls, review decisions, and the full label-factory gate
pass.

Wrap-up note for the 2026-05-13T10:12:41Z run: productive work continued to the
50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T11:03:46Z`;
documentation was checked and updated across README, docs, and work notes. The
run added active-site sourcing export, sequence-search export,
representation-backend planning, an integrated transfer blocker matrix,
review-only status hardening for the new export audits, and a 53/53
external-source transfer gate. Final verification passed:
`PYTHONPATH=src python -m unittest discover -s tests` with 265 tests,
`PYTHONPATH=src python -m catalytic_earth.cli validate`, `compileall`,
`git diff --check`, JSON/countable-label guardrail scans, and CLI help checks.
External rows remain 0 countable and not import-ready.

Label-quality confidence call for the 2026-05-13T11:14:12Z run: yes for
external-source repair and scientific-expansion controls, no for external label
import or M-CSA-only count growth. Evidence at run start: `validate` and 265
unit tests passed, the 1,025 preview remained non-promotable with 0 accepted
new labels, the external transfer gate passed 53/53 review-only checks, hard
negatives remained 0, near misses remained 0, out-of-scope false
non-abstentions remained 0, actionable in-scope failures remained 0,
review-only import growth remained 0, and the import-readiness audit kept 0
external rows import-ready. The operational decision was to reduce external
active-site and representation uncertainty while keeping every external
candidate non-countable.

Label-quality confidence call for the 2026-05-13T13:16:40Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
work, no for external-source import, and yes for scientific generalization
work. Evidence at run start: `validate` and 268 unit tests passed, the 1,025
preview still added 0 clean countable labels, source-scale audit remained
limited to 1,003 observed M-CSA records, hard negatives remained 0, near misses
remained 0, out-of-scope false non-abstentions remained 0, actionable in-scope
failures remained 0, review-only import growth remained 0, the external
transfer gate remained review-only at 59/59 checks with 0 import-ready rows,
active-site source evidence remained unresolved for 10 external rows, complete
near-duplicate search remained unresolved for 28 rows, and real representation
controls remained absent. The run therefore implemented the user-requested
sequence/fold-distance holdout first. The new holdout artifacts preserve 0
held-out out-of-scope false non-abstentions and surface a small held-out versus
in-distribution accuracy gap (`0.9767` vs `0.9881` evaluable in-scope top1),
but explicitly do not claim real <=30% sequence-identity or <0.7 TM-score
separation because no local Foldseek/MMseqs2/BLAST/DIAMOND executable was
available.

Wrap-up for the 2026-05-13T13:16:40Z run: implemented the proxy
sequence/fold-distance holdout artifacts for the 1,000 and 1,025 contexts,
promoted the canonical 12-row external representation sample to ESM-2
(`facebook/esm2_t6_8M_UR50D`), preserved the k-mer sample as an explicit
baseline artifact, and kept all external rows review-only/non-countable. The
transfer gate remains 59/59 and `ready_for_label_import=false`; the learned
sample has 0 embedding failures, 3 representation near-duplicate holdouts, and
12 learned-vs-heuristic disagreements. The holo-PDB swap action path was
inspected but not started because it requires a general selected-PDB override
implementation plus regenerated geometry/retrieval/factory artifacts. Final
verification before logging: 273 unit tests passed, `validate` passed,
`compileall` passed, `git diff --check` passed, JSON artifact parse passed, and
CLI help checks passed.

Remaining-time plan for the 2026-05-13T11:14:12Z run: after the active-site
sourcing resolution and deterministic representation sample were in place, use
the remaining productive window to make the blocker matrix consume those packets
directly, add gate/audit checks that reject stale blocker matrices, refresh
artifacts and docs to the 59/59 gate state, and rerun the full validation stack
before wrap-up. Do not open external label decisions or import rows during this
run.

New failure modes checked in the 2026-05-13T11:14:12Z run: the deterministic
representation sample surfaced one representation-level near-duplicate holdout
(`P60174` nearest `P00940`/`m_csa:324`) that was not promoted, and the blocker
matrix path had a stale-integration risk where resolution/sample artifacts could
exist without row-level blocker evidence. The transfer gate now has explicit
matrix-integration checks for active-site resolution and representation sample
rows, and the matrix audit rejects advertised integration counts that are absent
from rows.

Wrap-up note for the 2026-05-13T11:14:12Z run:
`ENDED_AT=2026-05-13T12:04:24Z`; measured productive-plus-wrap elapsed time was
about 50.2 minutes. Documentation was checked and updated across README, docs,
and work notes; no stale current-state claims are intentionally left outside
historical progress entries/status that will be regenerated from the log. Final
verification before wrap-up passed: full unit tests with 268 tests, validate,
compileall, `git diff --check`, JSON artifact parse checks,
countable/import-ready guardrail scans for the new artifacts, and CLI help
checks for the new commands. External rows remain 0 countable and not
import-ready; the gate is 59/59 review-only checks.

Label-quality confidence call for the 2026-05-13T09:10:54Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
work. Evidence at run start: `validate` and 256 unit tests passed, the 1,025
preview gate remains clean but non-promotable with 0 accepted new labels, the
external transfer gate passed 41/41 review-only checks before this run's new
sequence-alignment and active-site-sourcing gates, hard negatives remain
0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
the import-readiness audit keeps 0 external rows import-ready, and active-site,
sequence-neighborhood, heuristic, and representation blockers remain unresolved.
The operational decision is to reduce external-source readiness uncertainty
while keeping every external candidate non-countable.

Remaining-time plan for the 2026-05-13T09:10:54Z run: after adding bounded
sequence-alignment verification, active-site sourcing queue artifacts, and the
45/45 external transfer gate, use the remaining productive window for artifact
regression tests, full validation, JSON/countable-label guardrail scans, and
documentation freshness. Do not open an external label decision or import path
until active-site sourcing, complete sequence-neighborhood controls, real
representation controls, review decisions, and full label-factory gates pass.

Wrap-up note for the 2026-05-13T09:10:54Z run: productive work continued to the
50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T10:03:45Z`;
documentation was checked and updated across README, docs, and work notes. Final
verification passed with 259 unit tests, `validate`, `compileall`,
`git diff --check`, JSON artifact parsing, CLI help checks for the new commands,
external countable/import-ready guardrail scans, and a 45/45 external transfer
gate.

Label-quality confidence call for the 2026-05-13T03:08:55-05:00 run: no for
additional M-CSA-only count growth, yes for bounded external-source control
repair. Evidence at run start: `validate` and 252 unit tests passed, the 1,025
preview gate remains clean but non-promotable with 0 accepted new labels, the
prior external transfer gate passed 38/38 review-only checks, hard negatives
remain 0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
and the source-scale audit records only 1,003 observed M-CSA records for the
requested 1,025 tranche. The operational decision was to reduce external
sequence/readiness uncertainty while keeping every external candidate
non-countable.

Remaining-time plan for the 2026-05-13T03:08:55-05:00 run: after the bounded
sequence-neighborhood screen and import-readiness audit passed targeted tests,
keep work scoped to artifact regression coverage, docs, validation, and final
gate verification. Do not import external labels until explicit active-site
sourcing, complete sequence-neighborhood controls, real representation
controls, review decisions, and full label-factory gates pass.

Wrap-up note for the 2026-05-13T03:08:55-05:00 run: productive work continued
to the 50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T03:59:49-05:00`;
documentation was checked and updated across README, docs, and work notes.
Final verification passed with 256 unit tests, `validate`, `compileall`,
`git diff --check`, JSON artifact parse checks, CLI help checks, and external
artifact import/countable guardrail checks.

Label-quality confidence call for the 2026-05-13T07:08:09Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
controls. Evidence at run start: `validate` and 247 unit tests passed, the
1,025 preview gate remains clean but non-promotable with 0 accepted new labels,
the prior external transfer gate passed 33/33 review-only checks, hard
negatives remain 0, near misses remain 0, out-of-scope false non-abstentions
remain 0, actionable in-scope failures remain 0, review-only import growth
remains 0, the ATP/phosphoryl-transfer family expansion remains guardrail-clean,
and the source-scale audit records only 1,003 observed M-CSA records for the
requested 1,025 tranche. The operational decision is to repair external-source
control readiness while keeping every external candidate non-countable.

Remaining-time plan for the 2026-05-13T07:08:09Z run: after adding
representation-control comparison, broad-EC disambiguation, active-site gap
source requests, sequence-neighborhood controls, and updated external transfer
gates, use the remaining productive window for focused regression tests, full
validation, JSON artifact checks, and documentation/status updates. Do not
import external labels until explicit sequence, active-site, representation,
decision, and label-factory gates pass.

Wrap-up note for the 2026-05-13T07:08:09Z run: productive work continued past
the 50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T08:00:14Z`;
documentation was checked and updated across README, docs, and work notes.
Final verification passed with 252 unit tests, `validate`, `compileall`,
`git diff --check`, CLI help checks for the new commands, and JSON artifact
countable-label checks.

Label-quality confidence call for the 2026-05-13T06:06:38Z run: no for
additional M-CSA-only count growth, yes for bounded external-source control
repair. Evidence at run start: `validate` and 239 unit tests passed, the 1,025
preview gate passes 21/21 checks, the prior external transfer gate passes 22/22
review-only checks, hard negatives remain 0, near misses remain 0,
out-of-scope false non-abstentions remain 0, actionable in-scope failures
remain 0, review-only import growth remains 0, the 1,025 acceptance artifact
adds 0 clean countable labels, and the source-scale audit records only 1,003
observed M-CSA records for the requested 1,025 tranche. The existing external
control artifacts exposed active-site feature gaps, broad-EC rows, and a
metal-hydrolase/top1 collapse, so this run repaired guardrails instead of
opening label growth. This is an operational workflow decision, not a claim of
biological truth.

Remaining-time plan for the 2026-05-13T06:06:38Z run: after expanding
structure mapping to all 12 heuristic-ready controls, adding repair,
representation, binding-context, reaction, and sequence-holdout artifacts, use
the remaining productive window for regression tests, docs, and final gate
validation. Do not import external labels until a separate reviewed decision
artifact passes full label-factory gates.

Label-quality confidence call for the 2026-05-13T03:03:14Z run: yes, current
quality gates are good enough to spend this run on a bounded 1,025 preview.
Evidence at run start: `validate` and 206 unit tests passed, the accepted-1,000
gate passes 21/21 checks with 0 blockers, the accepted-1,000 review-debt
deferral audit keeps all 326 review-state rows non-countable with 0 accepted
overlap and 0 countable candidates, hard negatives remain 0, near misses remain
0, out-of-scope false non-abstentions remain 0, actionable in-scope failures
remain 0, review-only import growth remains 0, 321 expert-label decision rows
remain review-only, the 92 priority local-evidence gap rows remain
non-countable, and the ATP/phosphoryl-transfer family expansion remains
guardrail-clean with 0 countable label candidates. This is an operational
workflow decision, not a claim of biological truth.

Label-quality confidence call at handoff after the 2026-05-13T03:03:14Z run:
no for additional M-CSA-only count growth, yes for bounded external-source
transfer scaffolding.
Evidence: the 1,025 factory gate passes 21/21 checks, hard negatives remain 0,
near misses remain 0, out-of-scope false non-abstentions remain 0, actionable
in-scope failures remain 0, accepted review-gap labels remain 0, and
review-only import growth remains 0. However, the 1,025 acceptance artifact has
0 accepted new labels and the source-scale audit shows the M-CSA-only path does
not have enough source records for the next tranche. This is an operational
workflow decision, not a claim of biological truth.

Label-quality confidence call for the 2026-05-13T04:04:36Z run: no for
additional M-CSA-only count growth, yes for bounded external-source transfer
scaffolding. Evidence at run start: `validate` and 217 unit tests passed, the
1,025 preview gate passes 21/21 checks, hard negatives remain 0, near misses
remain 0, out-of-scope false non-abstentions remain 0, actionable in-scope
failures remain 0, accepted review-gap labels remain 0, review-only import
growth remains 0, the 1,025 acceptance artifact adds 0 clean countable labels,
and the source-scale audit records only 1,003 observed M-CSA records for the
requested 1,025 tranche. This run should advance external-source transfer
guardrails while keeping all external candidates non-countable.

Label-quality confidence call for the 2026-05-13T05:05:40Z run: no for
additional M-CSA-only count growth, yes for bounded external-source evidence
and control work. Evidence at run start: `validate` and 230 unit tests passed,
the 1,025 preview gate passes 21/21 checks, hard negatives remain 0, near
misses remain 0, out-of-scope false non-abstentions remain 0, actionable
in-scope failures remain 0, review-only import growth remains 0, the 1,025
acceptance artifact adds 0 clean countable labels, and the source-scale audit
records only 1,003 observed M-CSA records for the requested 1,025 tranche. This
run should keep external rows review-only while converting evidence gaps into
explicit control artifacts.

Remaining-time plan for the 2026-05-13T05:05:40Z run: after all 25 ready
external rows had active-site evidence sampled and the first 4 mapped controls
showed a metal-hydrolase top1 collapse, use remaining productive time to attach
failure-mode tests, update durable docs, and avoid any external label decision
until ontology/representation controls can separate those lanes.

Remaining-time plan for the 2026-05-13T04:04:36Z run: after the external
candidate manifest, evidence plan, evidence request export, import-safety
audit, and 11/11 external-transfer gate are implemented, use the remaining
productive window to harden documentation, artifact regression coverage, and
review-only external-source guardrails rather than opening another M-CSA-only
tranche.

Remaining-time plan for the 2026-05-13T03:03:14Z run: after the 1,025 preview
proved clean but non-promotable, use the remaining productive window to harden
the external-source transfer path. Completed: source-scale audit, transfer
manifest, query manifest, OOD calibration plan, bounded read-only UniProtKB/
Swiss-Prot sample, sample guardrail audit, regression tests, and documentation.

Label-quality confidence call for the 2026-05-13T01:00:39Z run: yes, current
quality gates are good enough to spend this run on a bounded 975 preview.
Evidence at run start: `validate` and 205 unit tests passed, the accepted-950
gate passes 21/21 checks with 0 blockers, the accepted-950 review-debt
deferral audit keeps all 282 review-state rows non-countable with 0 accepted
overlap, hard negatives remain 0, near misses remain 0, out-of-scope false
non-abstentions remain 0, actionable in-scope failures remain 0, review-only
import growth remains 0, 277 expert-label decision rows remain review-only,
the 84 priority local-evidence gap rows remain non-countable, and the
ATP/phosphoryl-transfer family expansion remains guardrail-clean with 0
countable label candidates. This is an operational workflow decision, not a
claim of biological truth.

Remaining-time plan for the 2026-05-13T01:00:39Z run: after the 975 gate
accepted two clean labels and the post-975 gate stayed clean, the run opened,
repaired, and accepted the bounded 1,000-entry preview. The review-debt
deferral, queue-retention, hard-negative, false-non-abstention,
actionable-failure, and family-boundary gates are clean.

Label-quality confidence call for the 2026-05-12T23:58:38Z run: yes, current
quality gates are good enough to spend this run on bounded 875 scaling.
Evidence at run start: `validate` and 205 unit tests passed, the accepted-850
gate passes 20/20 checks, the accepted-850 review-debt deferral audit keeps
all 203 review-state rows non-countable with 0 accepted-label overlap, hard
negatives remain 0, near misses remain 0, out-of-scope false non-abstentions
remain 0, actionable in-scope failures remain 0, review-only import growth
remains 0, and the ATP/phosphoryl-transfer family expansion remains
guardrail-clean with 0 countable label candidates. This is an operational
workflow decision, not a claim of biological truth.

Label-quality confidence call for the 2026-05-12T20:55:05Z run: yes, current
quality gates are good enough to spend this run on bounded 775 scaling.
Evidence at run start: `validate` and 200 unit tests passed, the accepted-750
gate passes 20/20 checks, the accepted-750 review-debt deferral audit keeps 118
review-state rows non-countable, hard negatives remain 0, near misses remain 0,
out-of-scope false non-abstentions remain 0, actionable in-scope failures
remain 0, review-only import growth remains 0, and the ATP/phosphoryl-transfer
family expansion remains guardrail-clean with 0 countable label candidates.
This is an operational workflow decision, not a claim of biological truth.

Label-quality confidence call for the 2026-05-12T19:54:22Z run: yes, current
quality gates were good enough to explicitly defer the 750 review-debt surface
and promote the seven clean 750 labels. Evidence: baseline `validate` and 200
unit tests passed at run start, the post-batch 750 gate passes 20/20 checks,
hard negatives remain 0, near misses remain 0, out-of-scope false
non-abstentions remain 0, actionable in-scope failures remain 0, accepted
labels with review debt remain 0, review-only import growth remains 0, and the
ATP/phosphoryl-transfer family expansion remains guardrail-clean with 0
countable label candidates. This is an operational workflow decision, not a
claim of biological truth.

Start with:
`artifacts/v3_label_batch_acceptance_check_1025_preview.json`,
`artifacts/v3_label_factory_gate_check_1025_preview.json`,
`artifacts/v3_label_scaling_quality_audit_1025_preview.json`,
`artifacts/v3_review_debt_summary_1025_preview.json`,
`artifacts/v3_accepted_review_debt_deferral_audit_1025_preview.json`,
`artifacts/v3_source_scale_limit_audit_1025.json`,
`artifacts/v3_external_source_transfer_manifest_1025.json`,
`artifacts/v3_external_source_query_manifest_1025.json`,
`artifacts/v3_external_ood_calibration_plan_1025.json`,
`artifacts/v3_external_source_candidate_sample_1025.json`,
`artifacts/v3_external_source_candidate_sample_audit_1025.json`,
`artifacts/v3_external_source_candidate_manifest_1025.json`,
`artifacts/v3_external_source_candidate_manifest_audit_1025.json`,
`artifacts/v3_external_source_lane_balance_audit_1025.json`,
`artifacts/v3_external_source_evidence_plan_1025.json`,
`artifacts/v3_external_source_evidence_request_export_1025.json`,
`artifacts/v3_external_source_active_site_evidence_queue_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_audit_1025.json`,
`artifacts/v3_external_source_failure_mode_audit_1025.json`,
`artifacts/v3_external_source_control_repair_plan_1025.json`,
`artifacts/v3_external_source_control_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_audit_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_audit_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_active_site_gap_source_requests_1025.json`,
`artifacts/v3_external_source_sequence_holdout_audit_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_plan_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json`,
`artifacts/v3_external_source_sequence_search_export_1025.json`,
`artifacts/v3_external_source_sequence_search_export_audit_1025.json`,
`artifacts/v3_external_source_import_readiness_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_audit_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json`,
`artifacts/v3_external_source_review_only_import_safety_audit_1025.json`,
`artifacts/v3_external_source_transfer_gate_check_1025.json`,
`artifacts/v3_external_source_reaction_evidence_sample_1025.json`,
`artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json`,
`artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json`, and
`work/label_preview_1025_notes.md`. For the compact external-transfer profile,
also read `work/external_source_transfer_1025_notes.md`.

Highest-value options:

1. Do not promote the 1,025 preview; it has 0 accepted labels and exists as a
   source-limit audit point.
2. Continue review-only external-source evidence collection from
   `artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`:
   the first UniProt feature re-check found 0 explicit active-site residue
   sources, so the next active-site step is primary literature/PDB source
   review for the 7 binding-plus-reaction context rows and primary active-site
   source discovery for the 3 reaction-only rows without counting any row.
3. Treat the Rhea reaction-context sample as context only, especially the 16
   broad-EC context rows; do not treat Rhea rows as active-site evidence.
4. Run real near-duplicate sequence searches for the 28 rows in
   `artifacts/v3_external_source_sequence_search_export_1025.json`; the
   bounded screen in
   `artifacts/v3_external_source_sequence_neighborhood_sample_1025.json` and
   bounded top-hit alignment check in
   `artifacts/v3_external_source_sequence_alignment_verification_1025.json` are
   not enough for import readiness.
5. Use the 12-row ESM-2 representation sample in
   `artifacts/v3_external_source_representation_backend_sample_1025.json` and
   its learned-vs-heuristic disagreements to prioritize pilot review, while
   keeping heuristic retrieval, sequence-search controls, and
   `artifacts/v3_external_source_kmer_representation_backend_sample_1025.json`
   as required baselines.
6. Use `artifacts/v3_external_source_transfer_blocker_matrix_1025.json` as the
   candidate-level blocker map: 10 active-site source rows with resolution
   statuses carried forward, 28 complete near-duplicate searches, 2 sequence
   holdouts, 12 representation-backend plans, 12 representation sample rows, 3
   representation near-duplicate holdouts in the ESM-2 sample, 1 representation
   near-duplicate holdout in the k-mer baseline, and 0 completed import
   decisions. The 59/59 transfer gate now fails stale matrices that omit
   active-site resolution or representation sample integration.
7. Keep every external UniProtKB/Swiss-Prot candidate non-countable until a
   separate decision artifact passes the full label-factory gate.
8. Preserve the nine-family ATP/phosphoryl-transfer layer as boundary evidence;
   do not collapse these families into generic hydrolase or metal-hydrolase
   labels.

Label-quality confidence call for the 2026-05-12T16:56:09-05:00 run: yes,
current quality gates are good enough to open a bounded 800 preview. Evidence
at run start: `validate` and 202 unit tests passed, the accepted-775 gate
passes 20/20 checks, the accepted-775 review-debt deferral audit keeps all 138
review-state rows non-countable with 0 accepted-label overlap, hard negatives
remain 0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
and the ATP/phosphoryl-transfer family expansion remains guardrail-clean with
0 countable label candidates. This is an operational workflow decision, not a
claim of biological truth.

Remaining-time plan for the 2026-05-12T16:56:09-05:00 run: after accepting
the clean 800 batch, use the remaining productive window to remove a scaling
bottleneck exposed by the run by adding geometry-artifact row reuse, verify it
against the real 800 graph, then open the next bounded tranche only if the
post-800 gate remains clean and the wrap-up window is still protected.

Keep `m_csa:650` and `m_csa:771` in review unless explicit local mechanism
evidence resolves their counterevidence; they are regression cases for
mechanism text that should not override family-boundary or triad-coherence
conflicts.

Remaining-time plan executed for the 2026-05-12T20:55:05Z run: after the 775
gate was clean and the registry had 642 labels, do not open 800 in the final
productive minutes. Instead, preserve the 775 evidence by adding
`work/label_preview_775_notes.md`, refreshing current-state docs, generating
`artifacts/perf_report_775.json`, and checking stale status/handoff claims
before measured wrap-up.

Known blockers:

- Labels are provisional and not expert-reviewed; do not claim validated enzyme
  function.
- Bronze/silver/gold tiers are evidence-management tiers, not wet-lab
  validation status.
- Geometry retrieval is heuristic, not learned.
- Ligand/cofactor evidence uses nearby and structure-wide mmCIF ligand atoms
  plus inferred roles; it does not model occupancy, alternate conformers,
  biological assembly, or substrate state.
- `m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430` are currently best
  treated as evidence-limited abstentions because selected structures lack
  expected local or structure-wide cofactor evidence.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.

## Run Timing

- STARTED_AT: 2026-05-13T06:06:38Z
- ENDED_AT: 2026-05-13T06:57:46Z
- Measured elapsed time: 51.133 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/external_source_transfer.md, docs/v2_strengthening_report.md,
  work/scope.md, work/handoff.md, work/label_factory_notes.md,
  work/label_preview_1025_notes.md, work/external_source_transfer_1025_notes.md,
  and work/external_source_control_repair_1025_notes.md before status
  regeneration.
- Normal locked run kept external UniProtKB/Swiss-Prot candidates review-only
  and repaired the post-M-CSA transfer controls without importing labels.
- Expanded structure mapping and heuristic scoring from 4 to all 12
  heuristic-ready external controls, added control-repair, representation,
  binding-context, full reaction-context, and sequence-holdout artifacts, and
  kept every external row non-countable.
- The external transfer gate now passes 33/33 checks for review-only evidence
  collection; the repair plan records 25 non-countable repair rows, the
  representation manifest exposes 12 mapped controls, the binding-context
  sample maps 7/7 rows as context only, and the sequence audit keeps two exact
  reference overlaps as holdouts.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 247 tests,
  targeted external-transfer/scaling tests, JSON artifact parsing, external
  import/countable violation scan, and `python -m compileall -q src tests`.

- STARTED_AT: 2026-05-13T04:04:36Z
- ENDED_AT: 2026-05-13T04:55:29Z
- Measured elapsed time: 50.883 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/external_source_transfer.md, docs/ingestion_plan.md,
  docs/research_program.md, docs/safety_scope.md, docs/v2_report.md,
  docs/v2_strengthening_report.md, work/scope.md, work/handoff.md,
  work/label_factory_notes.md, work/label_preview_1025_notes.md, and
  work/external_source_transfer_1025_notes.md before status regeneration.
- Normal locked run from the non-promoted 1,025 preview kept M-CSA-only growth
  stopped and hardened external-source transfer without importing labels.
- Added review-only external candidate manifest, manifest audit, lane-balance
  audit, evidence plan/export, active-site evidence queue, import-safety audit,
  11/11 transfer gate, Rhea reaction-context sample, and reaction-context audit.
  All external artifacts keep `countable_label_candidate_count=0`.
- The evidence plan flags seven broad/incomplete EC candidates; the active-site
  evidence queue exports 25 ready review-only candidates and defers five rows
  (two exact-reference holdouts and three broad-EC disambiguation cases).
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 230 tests,
  targeted external-transfer tests, and `python -m compileall -q src tests`.

- STARTED_AT: 2026-05-13T03:03:14Z
- ENDED_AT: 2026-05-13T03:54:50Z
- Measured elapsed time: 51.600 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md,
  docs/research_program.md, docs/ingestion_plan.md, docs/safety_scope.md,
  docs/external_source_transfer.md, work/scope.md, work/handoff.md,
  work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_1025_notes.md before status regeneration.
- Normal locked run from the accepted 1000 state first made an evidence-based
  confidence call, opened the bounded 1025 preview, and stopped promotion when
  the acceptance artifact added 0 clean countable labels.
- The 1025 preview gate passes 21/21 checks and records 0 hard negatives, 0
  near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope
  failures, 0 accepted review-gap labels, and 0 review-only import count
  growth. All 329 preview review-state rows remain non-countable.
- Source-scale audit now records 1,003 observed M-CSA source records for the
  requested 1,025 tranche, so M-CSA-only scaling is the active bottleneck. The
  run added review-only external-source transfer, query, OOD calibration,
  30-row UniProtKB/Swiss-Prot candidate sample, and sample guardrail artifacts
  with 0 countable external candidates.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 217 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and JSON parsing across
  1627 artifact/registry files.

- STARTED_AT: 2026-05-13T01:00:39Z
- ENDED_AT: 2026-05-13T02:01:02Z
- Measured elapsed time: 60.383 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md,
  work/label_preview_975_notes.md, and work/label_preview_1000_notes.md before
  status regeneration.
- Normal locked run from the accepted 950 state first made an evidence-based
  confidence call, accepted the bounded 975 batch, then opened, repaired, and
  accepted the bounded 1000 batch.
- The 1000 gate passes 21/21 checks and records 0 hard negatives, 0 near
  misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope
  failures, 0 accepted review-gap labels, 0 accepted reaction/substrate
  mismatch labels, and 0 review-only import count growth.
- The canonical registry now has 679 labels. All 326 accepted-1000 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_1000.json`, including the
  21 new 1000-preview review-debt rows. `m_csa:986` is explicitly deferred as
  local-heme low-score boundary evidence rather than counted out-of-scope.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 206 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and JSON parsing across
  artifact/registry files.

- STARTED_AT: 2026-05-12T23:58:38Z
- ENDED_AT: 2026-05-13T00:50:24Z
- Measured elapsed time: 51.767 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_950_notes.md before status regeneration.
- Normal locked run from the accepted 850 state first made an evidence-based
  confidence call, then accepted the bounded 875, 900, 925, and 950 batches.
- The 950 gate passes 21/21 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 673 labels. All 282 accepted-950 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_950.json`, including the
  19 new 950-preview review-debt rows. `m_csa:865` is explicitly classified as
  `expert_review_decision_needed` rather than unclassified review debt.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 205 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and JSON parsing across
  1432 artifact/registry files.

- STARTED_AT: 2026-05-12T16:56:09-05:00
- ENDED_AT: 2026-05-12T17:58:13-05:00
- Measured elapsed time: 62.067 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_850_notes.md before status regeneration.
- Normal locked run from the accepted 775 state first made an evidence-based
  confidence call, then accepted the bounded 800, 825, and 850 batches.
- The 850 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 652 labels. All 203 accepted-850 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_850.json`, including the
  22 new 850-preview review-debt rows. `m_csa:836` is explicitly deferred as
  role-inferred metal-hydrolase evidence without local ligand support rather
  than counted.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 205 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and `jq empty` across
  JSON artifacts.

- STARTED_AT: 2026-05-12T20:55:05Z
- ENDED_AT: 2026-05-12T21:45:56Z
- Measured elapsed time: 50.850 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_775_notes.md before status regeneration.
- Normal locked run from the accepted 750 state first made an evidence-based
  confidence call, then opened, repaired, and accepted the bounded 775 batch.
- The 775 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 642 labels. All 138 accepted-775 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_775.json`, including the
  20 new 775-preview review-debt rows. `m_csa:771` is explicitly deferred as
  counterevidence/text-leakage risk rather than counted.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 202 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and `jq empty` across
  JSON artifacts.

- STARTED_AT: 2026-05-12T19:54:22Z
- ENDED_AT: 2026-05-12T20:14:16Z
- Measured elapsed time: 79.900 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/v2_strengthening_report.md, work/scope.md,
  work/handoff.md, work/label_factory_notes.md, and
  work/label_preview_750_notes.md before status regeneration.
- Normal locked run from the accepted 725 state first made an evidence-based
  confidence call, then explicitly deferred the 750 preview review-debt surface
  and promoted the seven clean 750 candidates into the canonical registry.
- The 750 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 637 labels. All 118 accepted-750 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_750.json`, including the
  18 new 750-preview review-debt rows.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 200 tests, and
  `PYTHONPATH=src python -m compileall -q src tests`.

- STARTED_AT: 2026-05-12T17:51:49Z
- ENDED_AT: 2026-05-12T18:51:39Z
- Measured elapsed time: 59.833 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  work/scope.md, work/handoff.md, work/status.md inputs, and
  work/label_preview_750_notes.md before status regeneration.
- Normal locked run from the accepted 725 state first made an evidence-based
  confidence call, then added an accepted-725 review-debt deferral audit with
  100 non-countable rows and upgraded the 725 gate to 21/21 checks.
- Remaining-time plan executed before wrap-up: after the 725 deferral audit was
  clean, opened a bounded 750 preview. The 750 preview generated graph,
  geometry, retrieval, label-factory, review export, acceptance, scaling-quality,
  ontology-gap, learned-retrieval, and sequence-similarity artifacts. It found
  7 mechanically clean candidates and a 19/19 preview gate, but promotion is
  deferred because 18 new review-debt rows require repair or explicit deferral.
- Final verification passed: `git diff --check`, `jq empty` over regenerated
  JSON artifacts, `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 200 tests, and
  `PYTHONPATH=src python -m compileall -q src tests`.

- STARTED_AT: 2026-05-12T11:51:27-05:00
- ENDED_AT: 2026-05-12T12:47:20-05:00
- Measured elapsed time: 55.883 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  work/scope.md, work/handoff.md, work/status.md inputs, and
  work/label_preview_725_notes.md before status regeneration.
- Normal locked run from the accepted 700 state first made an evidence-based
  confidence call, then accepted the bounded 725 label-factory batch with 6
  clean countable labels and 100 review-state rows kept outside the benchmark.
- The 725 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- Remaining-time plan executed before wrap-up: after accepting 725, added
  review-only repair controls for 95 expert-label decision rows, 25
  local-evidence lanes, 8 alternate residue-position requests, a focused
  alternate-structure scan, strict remap-local audit for `m_csa:712`,
  ontology-gap audit, learned-retrieval manifest, sequence-similarity failure
  controls, regression tests, and documentation. Next run should repair or
  explicitly defer the accepted-725 review-debt surface before blind 750
  scaling.

- STARTED_AT: 2026-05-12T15:50:29Z
- ENDED_AT: 2026-05-12T16:41:18Z
- Measured elapsed time: 50.817 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  work/scope.md, work/handoff.md, work/label_preview_700_notes.md,
  work/expert_label_decision_local_evidence_gap_700_notes.md,
  work/atp_phosphoryl_transfer_family_expansion_700_notes.md, and status
  inputs before status regeneration.
- Normal locked run from the accepted 700 state did not grow the countable
  registry. It implemented the expert-reviewed ATP/phosphoryl-transfer family
  expansion for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP as
  ontology/family-boundary evidence.
- The expansion artifact maps 20 supported reaction/substrate mismatch lanes
  across all nine target families, records 4 non-target expert hints and 0
  unsupported mappings, and keeps `countable_label_candidate_count=0`.
- The 700 gate now passes 21/21 checks and requires complete mismatch-lane
  export, complete expert-label decision export, complete expert-label
  repair-candidate coverage, complete repair-guardrail coverage, complete
  local-evidence gap audit/export, local-evidence repair resolution, explicit
  alternate residue-position requests, review-only import-safety evidence, and
  ATP/phosphoryl-transfer family expansion evidence with 0 countable candidates.
  The scaling-quality audit and batch summary also carry those gates.
- Final verification passed: `git diff --check`, `jq empty` over regenerated
  JSON artifacts, `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 198 tests, and
  `PYTHONPATH=src python -m compileall -q src tests`.
