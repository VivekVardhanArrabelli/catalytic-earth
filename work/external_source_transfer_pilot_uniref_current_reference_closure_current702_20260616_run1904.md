# External Source-Transfer Pilot UniRef/Current-Reference Closure - Run1904

Date: 2026-06-16

## Scope

This run continued the approved source-transfer duplicate-screen follow-up for
the 5 normalized `needs_review` rows from run1804. No label registry apply was
performed, and frozen current702 stayed byte-unchanged at sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

## What Changed

- Added `build-external-source-pilot-uniref-current-reference-screen`, a
  review-only source-transfer pilot command that fetches candidate UniRef90/50
  cluster context and intersects it against current countable reference
  accessions.
- Let source-transfer confidence and success-criteria replay consume the
  optional UniRef/current-reference screen so rows with no current-reference
  cluster overlap can clear the `broader_duplicate_screening_required` process
  blocker.
- Preserved non-countable semantics: the new screen cannot create import-ready
  rows, countable labels, predictive evidence, or registry writes.

## Artifacts

- `artifacts/v3_external_source_pilot_uniref_current_reference_screen_t12_allvsall_current702_20260616_run1904.json`
  screened 5 rows, fetched 13 UniRef clusters, found 5 no-overlap rows, and had
  0 fetch failures or overlap holdouts.
- `artifacts/v3_external_source_pilot_success_criteria_t12_allvsall_uniref_current702_20260616_run1904.json`
  remains `needs_more_work`: 5 rows now have
  `current_reference_external_all_vs_all_uniref_no_signal`, 7 rows still require
  broader duplicate screening, and all 12 rows still need full label-factory and
  terminal review decisions before any import.
- `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_allvsall_uniref_current702_20260616_run1904.json`
  routes 5 rows to `needs_review`, 6 to
  `rejected_active_site_evidence_missing`, and 1 to
  `rejected_duplicate_or_near_duplicate`.
- `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run1904.json`
  queues 5 rows and no longer carries the broader duplicate-screening blocker.
- The refreshed repair lane and import-safety artifacts remain review-only with
  0 import-ready and 0 countable candidate rows. AKR, SDR, and DNA Pol X
  representation conflicts are repaired review-only; the glycoside boundary
  remains unrepaired.

## Validation

- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed.
- Baseline critical suite passed `587 passed, 174 subtests`.
- Focused new regression suite passed `6 passed, 126 deselected`.
- Full CLI/transfer-scope module suite passed `349 passed, 160 subtests`.
- Post-change critical suite passed `592 passed, 174 subtests`.
- Full `PYTHONPATH=src pytest -q` passed `2374 passed, 1 warning, 244 subtests`.
- `PYTHONPATH=src python -m compileall -q src tests`, run1904 JSON parsing,
  `jq empty work/progress_log.jsonl`, and `git diff --check` passed.

## Remaining Blockers

- 7 pilot rows still require broader duplicate-screening resolution.
- 12 pilot rows still require full label-factory gate execution.
- 12 pilot rows still lack terminal accepted review decisions.
- 2 pilot rows still carry representation-control blockers.
- 6 pilot rows still lack explicit active-site source resolution.
- The glycoside hydrolase/metal hydrolase boundary control remains unrepaired.

## Next Exact Action

Run the external source pilot review/factory path for the 5 queued
`needs_review` rows in
`artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run1904.json`,
then rerun mechanism repair controls, import-safety adjudication, success
criteria, and label-factory/novelty/governor gates. Do not import or apply from
the run1904 source-transfer artifacts.
