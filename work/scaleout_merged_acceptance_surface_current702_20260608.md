# Scale-out Merged Acceptance Surface - current702 - 20260608

- Automation ID: `ce-expansion-merger-qa`
- Created UTC: `2026-06-08T14:40:53Z`
- Source branch/head: `ce-expansion-merger-qa-20260608` / `a9a0c4af208151e346c0f42eb4842f681c982751`
- Origin main head consumed: `5a915007d68d4df05f7d0b1f4eef6761357b7b63`
- JSON artifact: `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`
- Repair overlay consumed: `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`

## Result

Four shard artifacts were available, so this run built the consolidated non-importing acceptance surface. The merge consumed 2058 shard rows and deduplicated them to 1116 canonical candidate keys. The merge preserves every source-row terminal state as a source member, applies the locator/coordinate repair overlay, and keeps current-registry overlap as a hard import-preview blocker.

No production registry edit, locator sidecar copy, model/threshold/split edit, heldout training, or label import was performed.

## Shard Readiness

- `glycoside_nucleoside`: 835 rows; terminal counts {'blocked_coordinate': 44, 'blocked_family_decision': 50, 'blocked_locator': 97, 'countable_candidate_preflight_only': 1, 'reject/OOS_preserve_signal': 233, 'review_only_evidence': 410}; validation_passed=True
- `metal_hydrolase`: 411 rows; terminal counts {'blocked_coordinate': 10, 'blocked_family_decision': 2, 'blocked_locator': 34, 'reject/OOS_preserve_signal': 117, 'review_only_evidence': 248}; validation_passed=True
- `plp_children`: 442 rows; terminal counts {'blocked_coordinate': 2, 'blocked_family_decision': 2, 'blocked_locator': 90, 'reject/OOS_preserve_signal': 314, 'review_only_evidence': 34}; validation_passed=True
- `redox_oxygen_sulfur`: 370 rows; terminal counts {'blocked_coordinate': 79, 'blocked_family_decision': 6, 'blocked_locator': 47, 'countable_candidate_preflight_only': 2, 'reject/OOS_preserve_signal': 120, 'review_only_evidence': 116}; validation_passed=True

## Source Terminal Counts

{"blocked_coordinate": 135, "blocked_family_decision": 60, "blocked_locator": 268, "countable_candidate_preflight_only": 3, "reject/OOS_preserve_signal": 784, "review_only_evidence": 808}

## Canonical Terminal Counts

- `blocked_coordinate`: 68 canonical candidates
- `blocked_family_decision`: 59 canonical candidates
- `blocked_locator`: 122 canonical candidates
- `countable_candidate_preflight_only`: 0 canonical candidates
- `reject/OOS_preserve_signal`: 583 canonical candidates
- `review_only_evidence`: 284 canonical candidates

## Import Preview Decision

No import-preview artifact was built. The three source `countable_candidate_preflight_only` rows are blocked after dedupe/current-registry overlap:

- `m_csa:127` -> `reject/OOS_preserve_signal`; blockers: canonical_terminal_state=reject/OOS_preserve_signal, current_registry_overlap, reject_or_oos_signal_present; current matches: m_csa:127/out_of_scope
- `m_csa:281` -> `review_only_evidence`; blockers: canonical_terminal_state=review_only_evidence, current_registry_overlap; current matches: m_csa:281/seed_fingerprint
- `uniprot:p78549` -> `reject/OOS_preserve_signal`; blockers: canonical_terminal_state=reject/OOS_preserve_signal, current_registry_overlap, reject_or_oos_signal_present; current matches: m_csa:798/seed_fingerprint, uniprot:p78549/out_of_scope

This means there are 0 new non-overlapping countable candidates ready for a gated import preview in this pass.

## Repair Overlay

The repair artifact remains durable and was applied as a merger overlay. It confirms all seven prior acquisition-conversion `blocked_locator` rows have hash-matched local coordinates, carries the source-backed preflight locator mapping for `uniprot:P60174`, and converts `uniprot:Q9BXS1` to a conservative future-surface `reject/OOS_preserve_signal` recommendation through transitive structural duplicate evidence. No locator sidecar was copied.

## Family Diversity

Top canonical family-lane coverage:

- `plp_child_subclasses`: 442 canonical candidates
- `metal_hydrolase_subclasses`: 411 canonical candidates
- `background_family_control_lane`: 384 canonical candidates
- `redox_oxygen_transfer_sulfur_lipoamide_shard`: 370 canonical candidates
- `mechanistically_distinct_oos_abstention_lane`: 178 canonical candidates
- `locator_coordinate_repair_lane`: 111 canonical candidates
- `glycoside_nucleoside_hydrolase_control_lane`: 102 canonical candidates
- `family_decision_repair_lane`: 48 canonical candidates
- `tim_barrel_fold_confounder_lane`: 7 canonical candidates
- `glycosidase_boundary_control_lane`: 5 canonical candidates

Full family/subfamily terminal counts are in the JSON artifact under `family_diversity`.

## Conflict Handling

Terminal conflicts were resolved conservatively: reject/OOS dominates, then coordinate/locator/family blockers, then preflight-only, then review-only. Current registry overlaps block import-preview eligibility and current out-of-scope overlaps are preserved as reject/OOS signal.

First terminal-conflict examples:

- `m_csa:1000` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:1002` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:1003` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:1004` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:102` -> `blocked_coordinate` from {'blocked_coordinate': 1, 'review_only_evidence': 1}
- `m_csa:104` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 2, 'review_only_evidence': 1}
- `m_csa:105` -> `reject/OOS_preserve_signal` from {'blocked_coordinate': 2, 'reject/OOS_preserve_signal': 1}
- `m_csa:111` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:116` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:117` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:120` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:124` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 2}
- `m_csa:127` -> `reject/OOS_preserve_signal` from {'countable_candidate_preflight_only': 1, 'reject/OOS_preserve_signal': 3}
- `m_csa:136` -> `reject/OOS_preserve_signal` from {'blocked_coordinate': 1, 'reject/OOS_preserve_signal': 2}
- `m_csa:160` -> `blocked_coordinate` from {'blocked_coordinate': 1, 'review_only_evidence': 2}
- `m_csa:173` -> `blocked_coordinate` from {'blocked_coordinate': 1, 'review_only_evidence': 1}
- `m_csa:184` -> `reject/OOS_preserve_signal` from {'blocked_locator': 1, 'reject/OOS_preserve_signal': 1}
- `m_csa:211` -> `reject/OOS_preserve_signal` from {'reject/OOS_preserve_signal': 1, 'review_only_evidence': 1}
- `m_csa:230` -> `reject/OOS_preserve_signal` from {'blocked_locator': 2, 'reject/OOS_preserve_signal': 1}
- `m_csa:233` -> `reject/OOS_preserve_signal` from {'blocked_coordinate': 1, 'reject/OOS_preserve_signal': 1}

## Validation Contract

- Shard artifact count >= 3: `True`
- Source shard validations passed: `True`
- All source rows represented: `True`
- Reject/OOS source rows preserved: `True`
- Review-only source rows preserved: `True`
- Import preview rows: `0`

## Next Action

Review the consolidated JSON `import_preview_decision` and `terminal_conflict_records` before any future import-gate run. If the main thread wants new labels, it should first resolve the current-registry overlaps for `uniprot:P78549`, `m_csa:127`, and `m_csa:281`, then review the remaining locator queue with `uniprot:P60174` first because it has the mapped source-backed locator payload.
