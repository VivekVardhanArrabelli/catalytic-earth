# ePK false-positive hunter handoff

- Last updated: 2026-05-21T12:52:45Z
- Started: 2026-05-21T05:34:01Z
- Ended: 2026-05-21T12:52:45Z
- Measured minutes: 438.73
- Primary outcome: regression_rows_emitted
- Pushed commit: f61f579b6898f11104ed6c642c0ecc0c35478a7e via alternate-index commit/push.
- Commit/push status: primary and follow-up status alternate-index commits pushed; local checked-out HEAD update remains blocked by linked-worktree metadata.
- Rule under attack: materializer equivalence on local geometry prefilters plus later-offset source-valid ePK entity v4 seed coverage.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran a new lane-only helper that audited the prior local-geometry/materializer gap IDs and expanded later-offset source-valid ePK entity seed queries. CIFs were fetched in memory only and reduced to compact entity/topology/materializer rows.

- Helper: `tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py`
- Primary artifact: `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_20260521_053401Z.json`
- Extended gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_125234Z.json`
- Entries reviewed: 307
- Coordinate contexts reviewed: 657
- Gap audit materializer contexts: 8
- Later-offset source-valid ePK v4 seed entries: 0
- Fetch errors: 0
- Materializer context errors: 0

## Result

The 8OOZ/9OFD/9OFE/9W1G geometry-vs-materializer gap is now explicit: all eight deposited/biological-assembly contexts had local Tyr-to-ATP gamma geometry, but every local hit mapped to the same author chain and the same polymer entity as the gamma-associated chain. The actual heteromeric materializer abstained in all eight contexts with `no_heteromeric_candidate_hit_review_only`.

The later-offset CDK/cyclin, JNK, receptor tyrosine kinase, insulin receptor kinase, EGFR dimer, mTORC1, and mTORC2 full-text/component search pages returned 307 unique entries after de-duplication with the four gap controls. None became a source-valid polymer/entity-family ePK v4 seed under this helper's compact entity bucket criteria.

The regression gate now emits 313 `epk_candidate_evidence_v1` rows from 12 lane sources. Expected-policy unsafe non-abstentions remain 0. The known context-v4-only residual remains `5UJ7:biological_assembly_1`.

## Evidence For / Against

Evidence for the added regression controls:

- The gap artifact records acceptor entity, gamma-associated polymer entity, same-chain status, same-entity reuse, local distance, materializer decision, and reject reasons for every 8OOZ/9OFD/9OFE/9W1G deposited/assembly context.
- The extended gate includes eight new `geometry_prefiltered_non_epk_v4_contaminant_control` rows; gate status remains `passes_expected_policy_gate_review_only`.
- The explicit negative-control rule now distinguishes local geometry prefilter hits from materializer-equivalent heteromeric entity hits.

Evidence against counterexamples on this run's surface:

- No gap-audit context had a heteromeric-entity-eligible local hit after entity mapping.
- No later-offset source-valid ePK v4 seed beyond the prior 9LGO surface was found across the bounded 307-entry / 657-context search.
- No source-valid ePK entry-level overblock risk and no unsafe non-abstention were observed.

## Verification

- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py`
- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_20260521_053401Z.json >/dev/null`
- `python tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py --started-at 2026-05-21T05:34:01Z --output artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_125234Z.json --repo-root .`
- JSONL validation passed for `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl` (16 lines).
- `git diff --check -- tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl work/research_lanes/epk_false_positive_hunter/handoff.md`

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal `git add --dry-run` failed creating linked-worktree `index.lock`: Operation not permitted.
- Alternate-index primary commit/push succeeded.
- Local checked-out HEAD remains behind `origin/research/epk-false-positive-hunter`; normal status still reflects linked-worktree metadata/index issues from prior runs.

## Next Query

Generalize deposited-v4 / assembly-below-floor split traps outside the fixed ORC/OCCM/MCM set: search non-ORC AAA+/ATPase/transporter/motor entries where deposited atom_site is v4-positive, a declared biological assembly falls below the current chain floor, and compact local Tyr or N-terminal Ser/Thr/Tyr geometry is heteromeric-entity eligible before materialization. In parallel, replace full-text later-offset source-valid ePK search with polymer-entity classification or curated accession/domain seeds for CDK/cyclin, JNK, receptor tyrosine kinases, and mTOR complexes.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py`
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_20260521_053401Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_125234Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
