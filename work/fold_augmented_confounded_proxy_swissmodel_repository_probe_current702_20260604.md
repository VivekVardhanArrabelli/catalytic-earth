# Fold-Augmented Confounded Proxy SWISS-MODEL Repository Probe - current702

Run: 2026-06-04T10:12:21Z

Live SWISS-MODEL Repository probe for the four AFDB-unavailable Lever 3 coordinate-source blockers. It records provider/type availability and stages only provider=SWISSMODEL homology-model coordinates; provider=PDB mappings are recorded as disallowed experimental shortcuts.

## Status

- fold_augmented_confounded_proxy_swissmodel_repository_probe_partial_3_of_4
- Rows with SWISS-MODEL predicted models: 3
- Rows with only PDB-provider mappings: 1
- Coordinates staged for review only: 3

## Rows

| row | accession | SWISS-MODEL models | PDB mappings | selected template | staged path |
| --- | --- | ---: | ---: | --- | --- |
| m_csa:416 | P07071 | 3 | 5 | 9d3x.1.A | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P07071_9d3x_1_A_range_6_605.pdb |
| m_csa:562 | P07658 | 0 | 5 | none | none |
| m_csa:586 | P00806 | 1 | 2 | 1lba.1.A | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P00806_1lba_1_A_range_7_151.pdb |
| m_csa:637 | P04531 | 1 | 2 | 1del.1.A | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P04531_1del_1_A_range_1_241.pdb |

## Decision

- All four clearable now: False
- Partial rows clearable now: 3
- Remaining coordinate-source blocker: m_csa:562/P07658
- Next gate: Use the staged SWISS-MODEL predicted coordinates for P07071/P00806/P04531 as review-only rescore inputs after P07658 and Q43088 clear; do not use P07658 provider=PDB mappings.
