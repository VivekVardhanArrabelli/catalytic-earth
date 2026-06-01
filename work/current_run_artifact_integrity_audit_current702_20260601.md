# Current Run Artifact Integrity Audit

## Summary

This audit indexes the 10 new JSON artifacts and 10 matching work reports from
the current run. All JSON artifacts parse, all reports are present, and the run
kept review-only guardrails: no label/registry/ontology changes, no production
threshold changes, no coordinate fetches, no model fitting, and no predicted
geometry scoring.

## Validation

- Focused locator regression slice: 6 passed.
- Mechanism-feature guardrail slice: 3 passed.
- Full pytest: 1086 passed, 26 subtests passed, one sklearn deprecation warning.
- `unittest discover`: 1064 passed.
- `validate`: 702 curated labels validated.
- Artifact migration dry run: 113 rows, 0 blockers, removal_allowed=0.
- Current-docs reference check: 430 concrete references, zero missing.
- Repo artifact parse sweep: 3108 JSON files and 25 JSONL files parsed with
  zero errors.
- `compileall` and `git diff --check`: passed.

## Next Action

Use `artifacts/v3_family_panel_source_free_locator_blocker_resolution_status_current702_20260601.json`
as the next locator entry point. Do not rerun source-free locator discovery.
