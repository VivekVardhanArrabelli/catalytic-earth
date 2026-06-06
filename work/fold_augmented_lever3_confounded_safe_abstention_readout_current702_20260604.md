# Fold-Augmented Lever 3 Confounded-Safe Abstention Readout - current702

Run: 2026-06-05T02:10:53Z

Lever 3 measured confounded-safe abstention readout. It composes the accepted fixed-threshold operating-point readout, the P07658 sequence-compatibility all-or-abstain gate, and the deployment input gap audit. It reports the safe deployment action when P07658 lacks accepted predicted-coordinate provenance without scoring rows, staging coordinates, changing threshold 0.44155, or using heldout rows for threshold selection.

## Status

- fold_augmented_lever3_confounded_safe_abstention_readout_ready_fail_closed_p07658
- Safe abstention routing available: True
- Fixed-threshold scoring closure available: False
- Unsafe forced transfer allowed: False

## Operating Point

- Route: fixed_baseline_plus_cofactor_context_counteraxis_plus_same_family_numeric_bandpass_counteraxis_contract
- Baseline threshold: 0.44155
- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204
- Hard-confounded residuals closed: True

## P07658 Fail-Closed Gate

- Sequence contract valid: True
- All-or-abstain action: abstain_or_route_novel_oos_until_coordinate_provenance_exists
- Required acceptance gates failed: 4
- Failed gate IDs: ['credentialed_or_local_exact_prediction_route_available', 'preferred_full_length_coordinate_present', 'filled_prediction_provenance_present', 'local_inventory_ready_for_acceptance_preflight']
- Forced abstention required now: True

## Deployment Policy

| policy | action | available now | allowed now | reason |
| --- | --- | ---: | ---: | --- |
| accepted_complete_coordinate_provenance_rows | score_with_fixed_threshold_and_counteraxis_contracts | False | False | Only rows with accepted predicted-coordinate provenance may be scored by the fixed 0.44155 operating point. |
| missing_p07658_coordinate_or_provenance | abstain_or_route_novel_oos | True | True | The exact P07658 sequence contract is valid, but no accepted full-length coordinate/provenance exists; the safe action is not to force a mechanism transfer. |
| mutated_truncated_or_experimental_pdb_shortcut | reject_as_deployment_closure_input | False | False | Mutation, truncation, split prediction, and experimental-PDB shortcuts are rejected by the sequence compatibility readout. |

## Counts

- Strict high-cofactor proxy abstained: 1/4
- Strict same-family proxy abstained: 26/59
- P07658 forced abstention rows: 1
- P07658 unsafe shortcut policy rows rejected: 3
- Deployment input gates satisfied: 2/6
- Critical violations: 0

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for scoring closure: False
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Run exactly one credentialed or local full-length P07658 prediction route, fill provenance, and rerun acceptance preflight before any fixed-threshold scoring rerun.

## Guardrails

- Measured readout only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 is deployment-safe as an abstention router for the remaining P07658 gap, but not ready for fixed-threshold scoring closure.
- Retains 31/34 calibration in-scope rows, abstains 105/204 train/cal OOS rows, and forces 1 incomplete P07658 row to abstain instead of forcing a mechanism transfer.
- Use the fail-closed route for incomplete P07658 inputs now; for scoring closure, provision one exact full-length predictor route and rerun acceptance preflight with provenance.
