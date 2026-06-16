# External Source-Transfer Pilot Repair Closure - Run1804

Scope: non-destructive source-transfer pilot follow-up. No label registry was
written, no row is countable, and no row is import-ready.

## Current Packet

- Success criteria:
  `artifacts/v3_external_source_pilot_success_criteria_t12_allvsall_current702_20260616_run1804.json`
  remains `needs_more_work`: 12 candidates, 0 import-ready rows, 0 terminal
  review decisions in the review-decision export.
- Terminal decisions:
  `artifacts/v3_external_source_pilot_terminal_decisions_t12_allvsall_current702_20260616_run1804.json`
  records 6 `rejected_active_site_evidence_missing`, 2
  `rejected_duplicate_or_near_duplicate`, and 4
  `deferred_requires_human_expert`.
- Confidence replay with all-vs-all sequence context:
  `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_allvsall_current702_20260616_run1804.json`
  feeds normalized decisions at
  `artifacts/v3_external_source_pilot_decisions_review_normalized_t12_allvsall_current702_20260616_run1804.json`
  and normalized queue
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_current702_20260616_run1804.json`.
  The normalized queue has 5 `needs_review` rows.
- Mechanism repair lanes:
  `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_current702_20260616_run1804_enriched.json`
  assigns named lanes for 4 rows and leaves 1 manual mechanism review row.
- All-vs-all duplicate screen:
  `artifacts/v3_external_source_all_vs_all_sequence_search_current702_20260616_run1804.json`
  and audit
  `artifacts/v3_external_source_all_vs_all_sequence_search_audit_current702_20260616_run1804.json`
  used real MMseqs2, covered 47/47 external candidates, found 0 exact/near
  duplicate pairs, and remains review-only. It does not remove the
  `uniref_wide_duplicate_screen_not_run` blocker.

## Repair-Lane Rows

| Accession | Repair lane | Source context |
| --- | --- | --- |
| C9JRZ8 | `add_akr_nadp_redox_representation_axis` | Rhea reaction context present |
| O14756 | `add_sdr_nad_p_redox_representation_axis` | Rhea reaction context present |
| P06746 | `add_dna_pol_x_lyase_representation_axis` | Rhea reaction context present |
| Q8N0X4 | `manual_source_mechanism_review_required` | Rhea reaction context present |
| P33025 | `split_glycoside_hydrolase_from_metal_hydrolase_control` | Rhea reaction context present |

## Adjudication State

- AKR/NADP, SDR/NAD(P), and DNA Pol X/5'-dRP lyase each have one
  review-only representation conflict repaired:
  `artifacts/v3_external_source_pilot_akr_nadp_import_safety_adjudication_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_sdr_redox_import_safety_adjudication_t12_allvsall_current702_20260616_run1804.json`,
  and
  `artifacts/v3_external_source_pilot_dna_pol_x_lyase_import_safety_adjudication_t12_allvsall_current702_20260616_run1804.json`.
- Glycoside hydrolase boundary remains unrepaired:
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_t12_allvsall_current702_20260616_run1804.json`
  records `glycoside_boundary_representation_conflict_not_repaired`.
- Every adjudication keeps `ready_for_label_import: false`,
  `import_ready_candidate_count: 0`, and `countable_label_candidate_count: 0`.

## Remaining Blockers

- All 12 success-criteria rows still require broader duplicate screening beyond
  the bounded current-reference/all-vs-all packet.
- All 12 still need a terminal human/expert review decision and a full
  label-factory gate after duplicate/review blockers are cleared.
- Six rows lack explicit active-site source evidence and stay rejected for this
  pilot packet.
- Two rows are duplicate/near-duplicate rejected in the current terminal packet.
- The glycoside boundary row needs a stronger non-text boundary control before
  any further import-safety consideration.

## Next Exact Action

Do not import from run1804 artifacts. Continue by either:

1. Run the approved broader duplicate screen/UniRef current-reference control
   for the 5 normalized `needs_review` rows, then rerun confidence,
   normalization, repair lanes, and import-safety adjudication.
2. If broader duplicate screening cannot be run locally, resolve the Q8N0X4
   manual mechanism review and P33025 glycoside boundary controls as
   review-only artifacts, keeping every row blocked from label import until
   duplicate screening, terminal review decisions, and label-factory gates pass.
