# ESMFold2 Predicted Active-Site Geometry Robustness — Experiment Contract

Status: `blocked_on_staged_coordinates`

## Open problem

Make the mechanism router robust to predicted (vs experimental) active-site geometry degradation: recover the clean 45/45 -> AlphaFoldDB-v6 23/45 primary drop and cut the 12.3% OOS false positive rate, as a learned-model job rather than a clean-M-CSA accuracy contest.

## Apo caveat (front and center)

ESMFold2, like every sequence folder, predicts apo structures. It will not place FAD/PLP/heme/Zn or substrate. The active-site signal leans heavily on cofactor/metal coordination, so ESMFold2 can only improve the protein side-chain part, not supply cofactor geometry. Expect partial help; measure it, do not assume it.

## AlphaFoldDB-v6 baseline to beat

- Predicted hand-router primary correct: 23/45 (clean experimental reference is 45/45)
- Predicted OOS/secondary false-positive rate: 0.123457

## Prediction work list

- Atlas (in-distribution + fingerprint) rows: 184
- Heldout rows (final-only): 140
- Unique accessions to predict: 323

## Staging status

- Staged dir: `None`
- Accessions with staged mmCIF: 0/323
- Blocker: `esmfold2_runtime_or_staged_coordinates_unavailable`

## Discipline

- Thresholds/models selected on in-distribution train/cal; heldout read once.
- ESMFold2 swaps only the coordinate source; geometry router and fold channel stay frozen.
- No labels/fingerprints/EC/Rhea/source text as predictive inputs.

This contract runs no ESMFold2 inference, downloads no weights, selects no threshold, and reads no heldout label.
