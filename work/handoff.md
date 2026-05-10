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
600-, 625-, 650-, 675-, and 700-entry curated slices. The 500-entry and larger
slices are countable only through the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
624 countable labels. Review-state registries preserve pending
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

## Current Metrics

- Curated label registry: 624 bronze automation-curated labels, with 157
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
- Label factory at 700: 79 bronze-to-silver promotions proposed, 188 active
  learning review rows queued, 100 adversarial negatives mined, 161
  expert-review export items generated, and 11/11 gate checks passing.
- Label batch summary: 9/9 accepted batches, 0 blockers, 0 hard negatives,
  0 near misses, 0 false non-abstentions, 0 actionable in-scope failures, and
  all active queues retained their unlabeled candidates.
- Latest accepted batch acceptance: 5 additional labels accepted for counting,
  81 review-state decisions pending, 624 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- 700 post-batch active-learning queue: all 64 unlabeled candidates are
  retained; no unlabeled rows are omitted by the queue limit.
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
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_700.json --applied-label-factory artifacts/v3_label_factory_applied_labels_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_700.json --expert-review-export artifacts/v3_expert_review_export_700_post_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json --out artifacts/v3_label_factory_gate_check_700.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --baseline-review-debt artifacts/v3_review_debt_summary_675.json --max-rows 45 --out artifacts/v3_review_debt_summary_700.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-review-debt-remediation --review-debt artifacts/v3_review_debt_summary_700.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --graph artifacts/v1_graph_700.json --geometry artifacts/v3_geometry_features_700.json --debt-status new --out artifacts/v3_review_debt_remediation_700.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-review-debt-remediation --review-debt artifacts/v3_review_debt_summary_700.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --graph artifacts/v1_graph_700.json --geometry artifacts/v3_geometry_features_700.json --debt-status all --out artifacts/v3_review_debt_remediation_700_all.json
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures --remediation artifacts/v3_review_debt_remediation_700.json --max-entries 13 --max-structures-per-entry 60 --out artifacts/v3_review_debt_alternate_structure_scan_700.json
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures --remediation artifacts/v3_review_debt_remediation_700_all.json --max-entries 46 --max-structures-per-entry 80 --out artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt-remap-leads --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json --remediation artifacts/v3_review_debt_remediation_700_all.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --out artifacts/v3_review_debt_remap_leads_700_all_bounded.json
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-cluster-proxy --graph artifacts/v1_graph_700.json --out artifacts/v3_sequence_cluster_proxy_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-label-scaling-quality --batch-id 700_preview --acceptance artifacts/v3_label_batch_acceptance_check_700_preview.json --readiness artifacts/v3_label_preview_promotion_readiness_700.json --review-debt artifacts/v3_review_debt_summary_700_preview.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700_preview.json --active-learning-queue artifacts/v3_active_learning_review_queue_700_preview_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700_preview_batch.json --hard-negatives artifacts/v3_hard_negative_controls_700_preview_batch.json --decision-batch artifacts/v3_expert_review_decision_batch_700_preview.json --structure-mapping artifacts/v3_structure_mapping_issues_700.json --expert-review-export artifacts/v3_expert_review_export_700_preview_post_batch.json --sequence-clusters artifacts/v3_sequence_cluster_proxy_700.json --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700.json --out artifacts/v3_label_scaling_quality_audit_700_preview.json
```

## Next Agent Start Here

Start from the accepted 700 state. Do not reopen the accepted 675/700 clean
label decisions unless a regression appears. The canonical registry has 624
countable labels; the latest accepted labels are `m_csa:686`, `m_csa:688`,
`m_csa:694`, `m_csa:697`, and `m_csa:699`.

The next bounded task is still quality repair, not another tranche. Start with
`artifacts/v3_review_debt_remap_leads_700_all_bounded.json` and
`artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json`: the
all-debt scan now covers all 739 candidate PDB structures and found review-only
local expected-family hits from remapped positions for `m_csa:577`,
`m_csa:592`, and `m_csa:641`. Do not count any of these rows unless a later
review import clears their gap reasons in
`artifacts/v3_review_evidence_gaps_700.json` and the label-factory gates pass.
The highest-value next repair is to audit those three remap-local leads against
their counterevidence and selected-structure gaps, then decide whether they
need expert review, a local structure-selection rule, or a stricter remap
guardrail.

Keep `m_csa:650` in review unless explicit metal-catalysis evidence is added;
it is the regression case for Ser-His text with a metal-dependent top retrieval
hit.

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

- STARTED_AT: 2026-05-10T17:53:25Z
- ENDED_AT: 2026-05-10T18:46:07Z
- Measured elapsed time: 52.700 minutes
- Documentation checked and updated across README, docs, scope, handoff,
  label-factory notes, 700 preview notes, and status inputs before final
  status regeneration.
- Normal locked run from the accepted 700 state did not grow the countable
  registry. It added conservative alternate-PDB residue-position remapping,
  regenerated the focused 700 scan, added a complete all-debt 739-structure
  bounded scan, and summarized 44 review-only remap leads while keeping
  countable label candidates at 0.
- Final verification passed: `git diff --check`, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m unittest
  discover -s tests` passed with 162 tests.
- Local perf-suite checks on the 700 artifacts completed in `/tmp` during the
  productive window; they were used as bounded verification and did not replace
  the committed 5-iteration performance artifact.
