# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Locator Rewrite Materialization Gate - current702

Run: 2026-06-03T20:12:39Z

Fail-closed materialization gate for priority-1 current702 heldout coordinate-anchor locator rewrites. It consumes the rewrite preflight and an explicit approval-decision artifact, verifies candidate and planned-payload hashes, and writes approved source-free locator sidecars only when the write flag is explicitly enabled. It does not score heldout rows or apply the frozen row-specific residual threshold.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_materialized
- Preflight rows: 55
- Approval records: 55
- Approved decisions: 53
- Invalid approval records: 0
- Approved ready for materialization: 0
- Approved locator sidecars written: 53
- Invalid approval/preflight rows: 0
- Rows without explicit approval: 2
- Blockers: none

## Decision

- Approved locator rewrites available: True
- Write approved locator sidecars: True
- Approved source-free locator surface ready: True
- Heldout-safe pair application surface ready: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Provide explicit approval decisions with matching candidate and planned-payload hashes, rerun this gate with locator writes enabled, then rerun locator input, application-surface, event-linker, and heldout-safe surface-plan audits before any heldout threshold read.

## Row Decisions

| row | accession | approval | decision | violations |
| --- | --- | ---: | --- | --- |
| m_csa:3 | P15559 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:9 | P31153 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:32 | Q04760 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:43 | P80366 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:44 | P00634 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:45 | P43379 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:46 | P14385 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:56 | Q9WZW0 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:97 | P0ABF6 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:109 | Q02127 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:115 | Q9T0N8 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:121 | P07850 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:131 | P20586 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:159 | P0A434 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:163 | P0A7Y4 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:171 | P00730 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:180 | P35505 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:188 | P09147 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:199 | P04425 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:211 | P38489 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:220 | P20906 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:239 | P00433 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:242 | Q8I914 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:250 | P04963 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:311 | P00924 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:321 | P09155 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:323 | P05314 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:333 | Q9RUB5 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:352 | P00949 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:356 | P14769 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:370 | O75164 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:384 | P23395 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:392 | P07801 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:397 | P04063 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:403 | P07584 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:418 | P37821 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:419 | O52552 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:480 | P26214 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:497 | Q9FDN7 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:517 | P61517 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:526 | P11708 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:541 | P75430 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:545 | Q7M523 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:551 | P15245 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:599 | P36936 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:709 | P00431 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:710 | P25524 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:714 | P0ABI8 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:723 | P00782 | 0 | not_materialized_no_explicit_approval | none |
| m_csa:750 | P55792 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:853 | P31570 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:854 | P80147 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:916 | P9WI55 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:990 | Q8GS60 | 1 | materialized_to_audited_locator_dir | none |
| m_csa:994 | Q9Y3Z3 | 1 | materialized_to_audited_locator_dir | none |

## Interpretation

- 53 explicit approval decisions were found; 53 locator sidecars were written to the audited directory.
- Do not copy priority-1 locator sidecars from preflight alone. Consume explicit approvals only, keep the event-axis blocker separate, and leave the frozen residual threshold unapplied until the source-free heldout surface is complete.
