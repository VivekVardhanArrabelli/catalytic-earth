# Scale-out Merged Acceptance Surface - current702 - 20260608

- Automation ID: `ce-expansion-merger-qa`
- Created UTC: `2026-06-08T15:34:16Z`
- Source branch/head: `main` / `e9cac07a95e76e9ac33245af5d45813bf2428fa9`
- Origin main head consumed: `15094774bbf00c05be58083c787d2747fb310ebd`
- JSON artifact: `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`
- Repair overlay consumed: `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`

## Result

Seven shard artifacts were available, so this run refreshed the consolidated non-importing acceptance surface. The merge consumed 4820 shard rows and deduplicated them to 2463 canonical candidate keys. The merge preserves every source-row terminal state as a source member, applies the locator/coordinate repair overlay, and keeps exact/current-screen registry overlap as a hard import-preview blocker.

No production registry edit, locator sidecar copy, model/threshold/split edit, heldout training, or label import was performed.

## Shard Readiness

- `glycoside_nucleoside`: 835 rows; terminal counts {'blocked_coordinate': 44, 'blocked_family_decision': 50, 'blocked_locator': 97, 'countable_candidate_preflight_only': 1, 'reject/OOS_preserve_signal': 233, 'review_only_evidence': 410}; validation_passed=True
- `metal_hydrolase`: 411 rows; terminal counts {'blocked_coordinate': 10, 'blocked_family_decision': 2, 'blocked_locator': 34, 'reject/OOS_preserve_signal': 117, 'review_only_evidence': 248}; validation_passed=True
- `near_orphan_tail`: 746 rows; terminal counts {'blocked_family_decision': 44, 'blocked_locator': 74, 'reject/OOS_preserve_signal': 438, 'review_only_evidence': 190}; validation_passed=True
- `phosphoryl_transfer`: 1281 rows; terminal counts {'blocked_coordinate': 16, 'blocked_family_decision': 142, 'blocked_locator': 33, 'countable_candidate_preflight_only': 1, 'reject/OOS_preserve_signal': 885, 'review_only_evidence': 204}; validation_passed=True
- `plp_children`: 442 rows; terminal counts {'blocked_coordinate': 2, 'blocked_family_decision': 2, 'blocked_locator': 90, 'reject/OOS_preserve_signal': 314, 'review_only_evidence': 34}; validation_passed=True
- `radical_sam_cobalamin`: 735 rows; terminal counts {'blocked_coordinate': 23, 'blocked_family_decision': 21, 'reject/OOS_preserve_signal': 681, 'review_only_evidence': 10}; validation_passed=True
- `redox_oxygen_sulfur`: 370 rows; terminal counts {'blocked_coordinate': 79, 'blocked_family_decision': 6, 'blocked_locator': 47, 'countable_candidate_preflight_only': 2, 'reject/OOS_preserve_signal': 120, 'review_only_evidence': 116}; validation_passed=True

## Source Terminal Counts

{"blocked_coordinate": 174, "blocked_family_decision": 267, "blocked_locator": 375, "countable_candidate_preflight_only": 4, "reject/OOS_preserve_signal": 2788, "review_only_evidence": 1212}

## Canonical Terminal Counts

- `blocked_coordinate`: 24 canonical candidates
- `blocked_family_decision`: 134 canonical candidates
- `blocked_locator`: 85 canonical candidates
- `countable_candidate_preflight_only`: 0 canonical candidates
- `reject/OOS_preserve_signal`: 1940 canonical candidates
- `review_only_evidence`: 280 canonical candidates

## Import Preview Decision

No import-preview artifact was built. The 4 source `countable_candidate_preflight_only` rows collapse to 3 blocked canonical groups after dedupe/current-registry overlap:

- `m_csa:127` -> `reject/OOS_preserve_signal`; blockers: canonical_terminal_state=reject/OOS_preserve_signal, current_registry_overlap, reject_or_oos_signal_present; current matches: m_csa:127/out_of_scope; source states: {'countable_candidate_preflight_only': 1, 'reject/OOS_preserve_signal': 4}
- `m_csa:281` -> `reject/OOS_preserve_signal`; blockers: canonical_terminal_state=reject/OOS_preserve_signal, current_registry_overlap, reject_or_oos_signal_present; current matches: m_csa:281/seed_fingerprint; source states: {'countable_candidate_preflight_only': 1, 'reject/OOS_preserve_signal': 1}
- `uniprot:p78549` -> `reject/OOS_preserve_signal`; blockers: canonical_terminal_state=reject/OOS_preserve_signal, current_registry_overlap, reject_or_oos_signal_present; current matches: uniprot:P78549/out_of_scope; source states: {'blocked_coordinate': 1, 'countable_candidate_preflight_only': 2, 'reject/OOS_preserve_signal': 2}

This means there are 0 new non-overlapping countable candidates ready for a gated import preview in this pass.

## Repair Overlay

The repair artifact remains durable and was applied as a merger overlay. It confirms all seven prior acquisition-conversion `blocked_locator` rows have hash-matched local coordinates, carries the source-backed preflight locator mapping for `uniprot:P60174`, and converts `uniprot:Q9BXS1` to a conservative future-surface `reject/OOS_preserve_signal` recommendation through transitive structural duplicate evidence. No locator sidecar was copied.

## Family Diversity

Top canonical family-lane coverage:

- `phosphoryl_transfer_boundary`: 1281 canonical candidates
- `radical_cobalamin_sam_like_probes`: 735 canonical candidates
- `plp_child_subclasses`: 442 canonical candidates
- `metal_hydrolase_subclasses`: 411 canonical candidates
- `background_family_control_lane`: 384 canonical candidates
- `redox_oxygen_transfer_sulfur_lipoamide_shard`: 370 canonical candidates
- `near_orphan_or_unrepresented_mechanism_tail`: 283 canonical candidates
- `external_hard_negative_structural_tail`: 246 canonical candidates
- `mechanistically_distinct_oos_abstention_lane`: 178 canonical candidates
- `no_reliable_structure_or_locator_gap`: 113 canonical candidates
- `locator_coordinate_repair_lane`: 111 canonical candidates
- `glycoside_nucleoside_hydrolase_control_lane`: 102 canonical candidates

Full family/subfamily terminal counts are in the JSON artifact under `family_diversity`.

## Conflict Handling

Terminal conflicts were resolved conservatively: reject/OOS dominates, then coordinate/locator/family blockers, then preflight-only, then review-only. Current registry overlaps block import-preview eligibility; current seed/curated overlaps downgrade source preflight rows to review-only, and current out-of-scope overlaps are preserved as reject/OOS signal.

First terminal-conflict examples:

- `m_csa:1` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 4, 'review_only_evidence': 1}
- `m_csa:10` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 3, 'review_only_evidence': 1}
- `m_csa:1000` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:1002` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:1003` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:1004` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 3}
- `m_csa:101` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 4, 'review_only_evidence': 1}
- `m_csa:102` -> `reject/OOS_preserve_signal` from {'blocked_coordinate': 1, 'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:103` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:104` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 4, 'review_only_evidence': 1}
- `m_csa:105` -> `reject/OOS_preserve_signal` from {'blocked_coordinate': 4, 'reject/OOS_preserve_signal': 1}
- `m_csa:106` -> `reject/OOS_preserve_signal` from {'blocked_coordinate': 1, 'reject/OOS_preserve_signal': 1}
- `m_csa:11` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:111` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 2, 'review_only_evidence': 1}
- `m_csa:115` -> `reject/OOS_preserve_signal` from {'blocked_family_decision': 1, 'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:116` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 2, 'review_only_evidence': 2}
- `m_csa:117` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 2, 'review_only_evidence': 1}
- `m_csa:12` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:120` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 2, 'review_only_evidence': 1}
- `m_csa:121` -> `reject/OOS_preserve_signal` from {'blocked_family_decision': 1, 'reject/OOS_preserve_signal': 3}

## Validation Contract

- Shard artifact count >= 3: `True`
- Source shard validations passed: `True`
- All source rows represented: `True`
- Reject/OOS source rows preserved: `True`
- Review-only source rows preserved: `True`
- Import preview rows: `0`

## Next Action

Review the consolidated JSON `import_preview_decision` and `terminal_conflict_records` before any future import-gate run. If the main thread wants new labels, it should first resolve the current-registry overlaps for `uniprot:P78549`, `m_csa:127`, and `m_csa:281`, then review the remaining locator queue with `uniprot:P60174` first because it has the mapped source-backed locator payload. The new phosphoryl-transfer, near-orphan-tail, and radical-SAM/cobalamin shards did not open an import preview; the extra source preflight row is another `uniprot:P78549` member and remains blocked by exact current702 overlap and reject/OOS conflict.
