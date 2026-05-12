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
600-, 625-, 650-, 675-, 700-, 725-, and 750-entry curated slices. The 500-entry and larger
slices are countable only through the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
637 countable labels. Review-state registries preserve pending
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

## Current Metrics

- Curated label registry: 637 bronze automation-curated labels, with 170
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
- Label factory at 750: 88 bronze-to-silver promotions proposed, 225 active
  learning review rows queued, 100 adversarial negatives mined, 142
  expert-review export items generated, 113 active expert-label decision rows
  routed through a review-only export, complete repair-candidate summary,
  priority repair guardrail audit, complete 28-row local-evidence gap
  audit/export, repair plan, review-only import-safety audit,
  ATP/phosphoryl-transfer family expansion, and 20/20 gate checks passing.
- Label batch summary: 11/11 accepted batches, 0 blockers, 0 hard negatives,
  0 near misses, 0 false non-abstentions, 0 actionable in-scope failures, and
  all active queues retained their unlabeled candidates.
- Latest accepted batch acceptance: 7 additional labels accepted for counting,
  118 review-state decisions pending, 637 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- Accepted-750 deferral audit: all 118 review-state rows explicitly remain
  non-countable, with 58 metadata-only rows carried from the capped review-debt
  table, 28 priority local-evidence rows audited/exported, 18 new
  750-preview review-debt rows classified and deferred, and 0 accepted-label
  overlap.
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

Start from the accepted 750 state. The canonical registry has 637 countable
labels; the latest accepted labels are `m_csa:728`, `m_csa:733`, `m_csa:735`,
`m_csa:739`, `m_csa:740`, `m_csa:742`, and `m_csa:750`.

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

This run accepted 750 after explicitly deferring all 118 review-state rows.
`artifacts/v3_accepted_review_debt_deferral_audit_750.json` covers the 18 new
750-preview review-debt rows and keeps every deferred row non-countable.
`artifacts/v3_label_factory_batch_summary.json` now reports 11/11 accepted
batches, latest batch `750`, 637 countable labels, 118 pending review-state
rows, and 0 blockers.

Start with:
`artifacts/v3_label_batch_acceptance_check_750.json`,
`artifacts/v3_label_factory_gate_check_750.json`,
`artifacts/v3_accepted_review_debt_deferral_audit_750.json`,
`artifacts/v3_label_scaling_quality_audit_750_preview.json`,
`artifacts/v3_review_debt_summary_750_preview.json`,
`artifacts/v3_active_learning_review_queue_750.json`,
`artifacts/v3_expert_label_decision_review_export_750.json`,
`artifacts/v3_expert_label_decision_repair_candidates_750.json`,
`artifacts/v3_expert_label_decision_local_evidence_gap_audit_750.json`,
`artifacts/v3_expert_label_decision_local_evidence_repair_plan_750.json`,
`artifacts/v3_mechanism_ontology_gap_audit_750.json`,
`artifacts/v3_learned_retrieval_manifest_750.json`,
`artifacts/v3_sequence_similarity_failure_sets_750.json`,
`artifacts/v3_label_factory_batch_summary.json`, and
`work/label_preview_750_notes.md`.

Highest-value options:

1. Open a bounded 775 preview toward the 1,000-label milestone only if the 750
   post-batch gate remains clean.
2. Run the full label-factory gate before any 775 promotion: review/confidence
   evidence validation, promotion/demotion checks, ontology/family guardrails,
   active-learning queue, adversarial negatives, expert-review artifacts,
   abstention calibration, hard-negative checks, in-scope failure analysis,
   tests, validate, and docs/status updates.
3. If the 775 preview adds review debt or exposes ontology/family-propagation
   drift, stop count growth and repair or explicitly defer that surface before
   promotion.
4. Preserve the nine-family ATP/phosphoryl-transfer layer as boundary evidence;
   do not collapse these families into generic hydrolase or metal-hydrolase
   labels.

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
