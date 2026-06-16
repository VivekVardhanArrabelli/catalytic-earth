# Q6NSJ0 Replacement Source-Transfer Closure - run2205

Date: 2026-06-16

Registry mutation: none. Frozen current702 stayed sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

## What Changed

- Q6NSJ0 was selected as the review-only glycoside replacement for the failed P33025
  glycoside-boundary row:
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_replacement_scout_current702_20260616_run2205.json`.
- Pinned pilot priority now includes Q6NSJ0 in the 13-row source-transfer worklist:
  `artifacts/v3_external_source_pilot_candidate_priority_q6nsj0_replacement_current702_20260616_run2205.json`.
- Pinned selected rows now flow through review export, evidence packet, representation plan,
  terminal decision, confidence normalization, and gap-audit builders without becoming
  import-ready or countable.

## Q6NSJ0 Evidence

- Explicit active-site evidence: positions 463 (`Nucleophile`) and 520 (`Proton donor/acceptor`),
  PubMed 36129849.
- Reaction/mechanism context: Rhea `RHEA:21112`, EC `3.2.1.22`.
- Sequence/duplicate context: bounded current-reference search no-signal and UniRef90/50 no
  current countable-reference overlap:
  `artifacts/v3_external_source_pilot_uniref_current_reference_screen_q6nsj0_replacement_current702_20260616_run2205.json`.
- Representation context: deterministic representation sample/adjudication remains review-only and
  flags `heuristic_fingerprint_context_changed`, not a cleared representation gate:
  `artifacts/v3_external_source_pilot_representation_adjudication_q6nsj0_replacement_current702_20260616_run2205.json`.

## Current Gate State

- Success criteria: `needs_more_work` in
  `artifacts/v3_external_source_pilot_success_criteria_q6nsj0_replacement_current702_20260616_run2205.json`.
- Terminal decisions:
  `artifacts/v3_external_source_pilot_terminal_decisions_q6nsj0_replacement_current702_20260616_run2205.json`
  has 7 `deferred_requires_human_expert`, 6 `rejected_active_site_evidence_missing`, 0 import-ready,
  and 0 countable rows.
- Expert queue:
  `artifacts/v3_external_source_pilot_human_expert_review_queue_q6nsj0_replacement_current702_20260616_run2205.json`
  has 7 queued rows. After UniRef replay, the only non-human queue blocker is
  `full_label_factory_gate_not_run`.
- Gap audit:
  `artifacts/v3_external_source_pilot_review_resolution_gap_audit_q6nsj0_replacement_current702_20260616_run2205.json`
  holds all 7 queued rows for missing family import-safety adjudication / review / factory gates.

## Validation

- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed.
- Focused registry/source/leakage/novelty/import/transfer/CLI suite passed: 607 tests, 174 subtests.
- Full `PYTHONPATH=src pytest -q` passed: 2389 tests, 244 subtests, one SciPy deprecation warning.
- `python -m compileall -q src tests`, JSON parsing, hard-limit scan, docs reference check, and
  `git diff --check` passed.

## Next Exact Action

Build a current-slice `needs_review_resolution` and repair-lane mapping for Q6NSJ0, then run
`build-external-source-pilot-glycoside-hydrolase-import-safety-adjudication` against the Q6NSJ0
replacement packet. Only after that, rerun success criteria, terminal/confidence normalization,
label-factory, novelty, governor, and row-guardrail gates before any import.
