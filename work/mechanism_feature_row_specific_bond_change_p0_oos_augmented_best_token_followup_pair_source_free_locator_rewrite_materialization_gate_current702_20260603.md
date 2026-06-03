# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Locator Rewrite Materialization Gate - current702

Run: 2026-06-03T11:11:09Z

Fail-closed materialization gate for priority-1 current702 heldout coordinate-anchor locator rewrites. It consumes the rewrite preflight and an explicit approval-decision artifact, verifies candidate and planned-payload hashes, and writes approved source-free locator sidecars only when the write flag is explicitly enabled. It does not score heldout rows or apply the frozen row-specific residual threshold.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_ready_blocked
- Preflight rows: 55
- Approval records: 0
- Approved decisions: 0
- Invalid approval records: 0
- Approved ready for materialization: 0
- Approved locator sidecars written: 0
- Invalid approval/preflight rows: 0
- Rows without explicit approval: 55
- Blockers: explicit_locator_rewrite_approval_decisions_missing, approved_locator_rewrite_rows_missing, approved_locator_sidecar_write_flag_not_enabled, approved_locator_sidecars_not_materialized

## Decision

- Approved locator rewrites available: False
- Write approved locator sidecars: False
- Approved source-free locator surface ready: False
- Heldout-safe pair application surface ready: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Provide explicit approval decisions with matching candidate and planned-payload hashes, rerun this gate with locator writes enabled, then rerun locator input, application-surface, event-linker, and heldout-safe surface-plan audits before any heldout threshold read.

## Row Decisions

| row | accession | approval | decision | violations |
| --- | --- | ---: | --- | --- |
| m_csa:3 | P15559 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:9 | P31153 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:32 | Q04760 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:43 | P80366 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:44 | P00634 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:45 | P43379 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:46 | P14385 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:56 | Q9WZW0 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:97 | P0ABF6 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:109 | Q02127 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:115 | Q9T0N8 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:121 | P07850 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:131 | P20586 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:159 | P0A434 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:163 | P0A7Y4 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:171 | P00730 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:180 | P35505 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:188 | P09147 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:199 | P04425 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:211 | P38489 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:220 | P20906 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:239 | P00433 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:242 | Q8I914 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:250 | P04963 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:311 | P00924 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:321 | P09155 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:323 | P05314 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:333 | Q9RUB5 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:352 | P00949 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:356 | P14769 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:370 | O75164 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:384 | P23395 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:392 | P07801 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:397 | P04063 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:403 | P07584 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:418 | P37821 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:419 | O52552 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:480 | P26214 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:497 | Q9FDN7 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:517 | P61517 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:526 | P11708 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:541 | P75430 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:545 | Q7M523 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:551 | P15245 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:599 | P36936 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:709 | P00431 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:710 | P25524 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:714 | P0ABI8 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:723 | P00782 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:750 | P55792 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:853 | P31570 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:854 | P80147 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:916 | P9WI55 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:990 | Q8GS60 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:994 | Q9Y3Z3 | 0 | not_materialized_no_explicit_approval | none |

## Interpretation

- 0 explicit approval decisions were found; 0 locator sidecars were written to the audited directory.
- Do not copy priority-1 locator sidecars from preflight alone. Consume explicit approvals only, keep the event-axis blocker separate, and leave the frozen residual threshold unapplied until the source-free heldout surface is complete.
