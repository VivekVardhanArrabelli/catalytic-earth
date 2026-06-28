# Fold-NN Mechanism Recovery Readout

Run: 2026-06-28T19:28:12Z
Surface: `offmcsa_bronze_high_confidence`
Status: `fold_nn_mechanism_recovery_readout_complete`

## Coverage

- Positives with a fold hit: 156/156 (1.0).

## Recovery (no abstention)

- Fold-NN recovered true fingerprint: 132/156 (0.8462).
- Fold-NN score median: 0.8052.

## Recovery / Abstention Curve

- fold >= 0.0: retained 156 (abstained 0); recovered 132; precision-on-retained 0.8462; recovery-of-all 0.8462.
- fold >= 0.5: retained 138 (abstained 18); recovered 122; precision-on-retained 0.8841; recovery-of-all 0.7821.
- fold >= 0.566: retained 133 (abstained 23); recovered 120; precision-on-retained 0.9023; recovery-of-all 0.7692.
- fold >= 0.6: retained 126 (abstained 30); recovered 113; precision-on-retained 0.8968; recovery-of-all 0.7244.
- fold >= 0.65: retained 124 (abstained 32); recovered 111; precision-on-retained 0.8952; recovery-of-all 0.7115.
- fold >= 0.7: retained 112 (abstained 44); recovered 101; precision-on-retained 0.9018; recovery-of-all 0.6474.
- fold >= 0.74: retained 95 (abstained 61); recovered 93; precision-on-retained 0.9789; recovery-of-all 0.5962.

## Notes

- Raising the fold gate trades recovered coverage for precision on the retained set; compare against the off-M-CSA abstention frontier when a non-M-CSA positive surface becomes available.

## Guardrails

- Labels are evaluation targets only, never model features.
- No heldout row scored; no model trained; no threshold selected on heldout; no registry/ontology/label/threshold/fingerprint change.
