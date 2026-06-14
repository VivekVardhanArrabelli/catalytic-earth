# Novelty / Saturation Admission Gate

Run: 2026-06-14T03:00:18Z

An online, non-destructive filter that sits AFTER the exact accession/sequence-SHA screen and admits incoming candidates only when they add diversity -- closing the near-duplicate / lane-saturation gap the governor measured. Writes no registry; emits no labels.

## Policy

- Cluster key: (fingerprint_or_scope, full_ec, organism, sequence_length_bin).
- Per-cluster cap 3; floor 100; cap ceiling 250; hole threshold 25.
- post exact-dedup gate: hole/under-floor admit unless redundant ortholog; over-cap reject unless new reaction; balanced/OOS admit only on novelty, throttle saturated clusters.

## Retrospective self-audit (existing expansion replayed through the gate)

- Expansion rows: 7363.
- Decisions: {'admit': 6907, 'reject': 47, 'throttle': 409}.
- Would NOT re-admit (redundant under policy): 456 (0.0619).
- Reasons: {'adds_diversity': 3437, 'closes_hole_fingerprint': 832, 'closes_under_floor_fingerprint': 2628, 'fingerprint_over_cap_no_new_chemistry': 47, 'needed_fingerprint_but_redundant_ortholog': 10, 'over_cap_but_new_reaction_chemistry': 10, 'redundant_no_novelty_signal': 399}.
- Non-admit concentration by scope: {'out_of_scope': 373, 'metal_dependent_hydrolase': 71, 'heme_peroxidase_oxidase': 10, 'plp_dependent_enzyme': 2}.

## Usage

- feed an engine preview's applied_labels through evaluate_batch against build_diversity_state(frozen, expansion); apply only the ADMIT set via apply-external-annotation-anchored-import.

## Guardrails

- Frozen benchmark written: False.
- Labels emitted: 0.
- The gate is advisory; the authorized apply step is what writes.
