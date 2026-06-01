# Fold-Only Train/Cal OOS Negative Surface - current702

Run: 2026-06-01T05:14:00Z

Fold-only salvage surface for train/cal OOS negatives with real Foldseek/TM hits but missing predicted-geometry channel scores.

## Status

- fold_only_negative_surface_ready
- Fold-only rows: 10
- Mean nearest-train TM: 0.53259
- Nearest train fingerprint counts: {'flavin_dehydrogenase_reductase': 3, 'metal_dependent_hydrolase': 3, 'plp_dependent_enzyme': 1, 'ser_his_acid_hydrolase': 3}

## Rows

| Entry | geometry status | nearest train atlas | nearest train fingerprint | TM |
| --- | --- | --- | --- | ---: |
| m_csa:57 | missing | m_csa:472 | metal_dependent_hydrolase | 0.4255 |
| m_csa:106 | missing | m_csa:275 | flavin_dehydrogenase_reductase | 0.6479 |
| m_csa:178 | missing | m_csa:94 | ser_his_acid_hydrolase | 0.4969 |
| m_csa:204 | missing | m_csa:337 | ser_his_acid_hydrolase | 0.5651 |
| m_csa:284 | missing | m_csa:430 | plp_dependent_enzyme | 0.4309 |
| m_csa:314 | missing | m_csa:353 | flavin_dehydrogenase_reductase | 0.419 |
| m_csa:503 | missing | m_csa:11 | metal_dependent_hydrolase | 0.6857 |
| m_csa:531 | missing | m_csa:862 | flavin_dehydrogenase_reductase | 0.611 |
| uniprot:P78549 | missing | m_csa:83 | metal_dependent_hydrolase | 0.4411 |
| uniprot:Q3LXA3 | missing | m_csa:518 | ser_his_acid_hydrolase | 0.6028 |

## Interpretation

- Calibration OOS candidates with fold evidence but missing geometry are available for fold-only sensitivity checks.
- Use these only for fold-only diagnostics or repair active-site geometry eligibility before combined threshold calibration.
