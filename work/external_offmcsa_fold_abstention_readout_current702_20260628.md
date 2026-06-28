# Off-M-CSA Fold-NN Abstention Generalization Readout

Run: 2026-06-28T14:15:08Z
Status: `fold_nn_abstention_signal_generalizes_off_mcsa`

## Fold-NN Distributions (best alntmscore to the M-CSA train atlas)

- External off-M-CSA negatives: median 0.5737 (mean 0.5622, n 52).
- M-CSA calibration in-scope: median 0.743 (n 35).
- M-CSA calibration OOS: median 0.5661 (n 26).

## Generalization Test

- External median 0.5737 vs M-CSA OOS median 0.5661 (tracks OOS within 0.05: True).
- External median below M-CSA in-scope median 0.743: True.
- External negatives at/above the in-scope median: 2.
- Abstention signal generalizes off M-CSA: True.

## Abstention / Recovery Frontier

- fold >= 0.5: external false-accept 38/52 (0.7308); M-CSA in-scope retained 30/35 (0.8571); M-CSA OOS false-accept 18/26.
- fold >= 0.566: external false-accept 27/52 (0.5192); M-CSA in-scope retained 27/35 (0.7714); M-CSA OOS false-accept 13/26.
- fold >= 0.6: external false-accept 18/52 (0.3462); M-CSA in-scope retained 27/35 (0.7714); M-CSA OOS false-accept 12/26.
- fold >= 0.65: external false-accept 10/52 (0.1923); M-CSA in-scope retained 25/35 (0.7143); M-CSA OOS false-accept 5/26.
- fold >= 0.7: external false-accept 3/52 (0.0577); M-CSA in-scope retained 20/35 (0.5714); M-CSA OOS false-accept 4/26.
- fold >= 0.74: external false-accept 2/52 (0.0385); M-CSA in-scope retained 18/35 (0.5143); M-CSA OOS false-accept 3/26.

## Caveats

- This probes off-M-CSA OOS rejection only, not off-M-CSA in-scope recovery (which would need non-M-CSA positives with known mechanism and structure). The external set is a curated negative panel, not a random deployment sample, and a strict abstention threshold also lowers in-scope recovery (see the frontier). No threshold is selected here.

## Guardrails

- External negatives are non-M-CSA, scored only against the M-CSA train atlas.
- No heldout row was scored or read; no model was trained; no threshold was selected on heldout.
- No production threshold, model weight, registry, ontology, label, or fingerprint-family change was made.
