# Fold-NN Mechanism Recovery Readout

Run: 2026-06-28T16:22:52Z
Surface: `mcsa_calibration_inscope_baseline`
Status: `fold_nn_mechanism_recovery_readout_complete`

## Coverage

- Positives with a fold hit: 35/35 (1.0).

## Recovery (no abstention)

- Fold-NN recovered true fingerprint: 28/35 (0.8).
- Fold-NN score median: 0.743.

## Recovery / Abstention Curve

- fold >= 0.0: retained 35 (abstained 0); recovered 28; precision-on-retained 0.8; recovery-of-all 0.8.
- fold >= 0.5: retained 30 (abstained 5); recovered 26; precision-on-retained 0.8667; recovery-of-all 0.7429.
- fold >= 0.566: retained 27 (abstained 8); recovered 25; precision-on-retained 0.9259; recovery-of-all 0.7143.
- fold >= 0.6: retained 27 (abstained 8); recovered 25; precision-on-retained 0.9259; recovery-of-all 0.7143.
- fold >= 0.65: retained 25 (abstained 10); recovered 24; precision-on-retained 0.96; recovery-of-all 0.6857.
- fold >= 0.7: retained 20 (abstained 15); recovered 19; precision-on-retained 0.95; recovery-of-all 0.5429.
- fold >= 0.74: retained 18 (abstained 17); recovered 17; precision-on-retained 0.9444; recovery-of-all 0.4857.

## Notes

- Raising the fold gate trades recovered coverage for precision on the retained set; compare against the off-M-CSA abstention frontier when a non-M-CSA positive surface becomes available.

## Guardrails

- Labels are evaluation targets only, never model features.
- No heldout row scored; no model trained; no threshold selected on heldout; no registry/ontology/label/threshold/fingerprint change.
