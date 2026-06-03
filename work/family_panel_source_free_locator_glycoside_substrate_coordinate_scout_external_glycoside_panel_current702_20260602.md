# Source-Free Locator Glycoside Substrate-Coordinate Scout - current702

Run: 2026-06-02T23:17:15Z

Local-cache-only scout for external_glycoside_panel after the NAG validator rejected glycan-context retargeting. It looks for already cached same-accession coordinates with non-glycan, non-buffer ligands that could be manually reviewed as substrate-complex locator candidates.

## Status

- source_free_locator_glycoside_substrate_coordinate_scout_blocked_no_substrate_like_local_coordinate_review_only
- Local coordinate files scanned: 60
- Same-accession coordinate records: 4
- Same-accession AFDB records: 3
- Records with rejected glycan/buffer ligands: 1
- Substrate-like coordinate candidates: 0
- Ready for predicted-geometry scoring: 0

## Coordinate Records

| coordinate | kind | struct_ref | rejected ligands | substrate-like ligands | clears gate |
| --- | --- | --- | --- | --- | --- |
| artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-Q6NSJ0-F1-model_v6.cif | alphafolddb_predicted_cif | MYORG_HUMAN, Q6NSJ0 | {} | {} | False |
| artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_7QQF.cif | pdb_mmcif | MYORG_HUMAN, Q6NSJ0 | {'ACT': 16, 'BMA': 22, 'FUC': 20, 'MAN': 11, 'MLI': 28, 'NAG': 434} | {} | False |
| artifacts/v3_external_structural_coordinates_1025/afdb_Q6NSJ0.cif | alphafolddb_predicted_cif | MYORG_HUMAN, Q6NSJ0 | {} | {} | False |
| artifacts/v3_external_structural_coordinates_1025_all30/afdb_Q6NSJ0.cif | alphafolddb_predicted_cif | MYORG_HUMAN, Q6NSJ0 | {} | {} | False |

## Guardrails

- Local-cache-only scout; no coordinates or source data were fetched.
- No locator sidecars were copied, created, or marked scoring-ready.
- No labels, registries, ontologies, imports, thresholds, training data, or model weights changed.

## Interpretation

- No cached same-accession substrate-like coordinate clears the external_glycoside_panel gate unless substrate-like candidates are listed. Provide an explicit substrate-complex coordinate or expert-approved non-glycan locator before any audited locator copy or scoring.
