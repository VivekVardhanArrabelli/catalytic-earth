# Atlas Broadening Feasibility

Run: 2026-06-28T19:47:08Z
Status: `blocked_atlas_broadening_no_fine_multifamily_mcsa_label_source`

## Question

- Can the M-CSA fold atlas be broadened beyond the cofactor families using a locally available fine (57-family) labelled, structure-backed M-CSA source?

## Current Atlas

- 5 families, 133 structures: flavin_dehydrogenase_reductase, heme_peroxidase_oxidase, metal_dependent_hydrolase, plp_dependent_enzyme, ser_his_acid_hydrolase.

## Fine-Label Sources Checked

- current-57 cofactor operating point: fine labels present but scoped to 5 cofactor families only.
- label manifest fine-fingerprint rows: 0.
- curated registry families: 8 (coarse (8-family) frozen taxonomy, incompatible with the fine 57-family atlas/bronze labels).
- external bronze labels: non-M-CSA (cannot serve as the M-CSA atlas).

## Blocker

- Fine (57-family) M-CSA truth labels exist only on the current-57 cofactor operating-point surface (5 families). The label manifest carries 0 fine-fingerprint rows, the curated registry is coarse (8 families), and bronze labels are non-M-CSA. So no local source provides a fine multi-family structure-backed M-CSA atlas beyond the cofactor families.
- Families unreachable for now: 52 of 57.

## Unblock Plan

1. Derive fine (57-family) truth fingerprints for M-CSA train in-scope rows across all families (run the router/operating-point machinery on the full M-CSA in-distribution set, not just the cofactor surface), with explicit leakage controls.
2. Stage AlphaFold/PDB structures for those M-CSA rows (most are likely already local; backfill the rest via an authorized bounded download).
3. Rebuild the atlas accession->fine-fingerprint map across families and re-run the off-M-CSA recovery harness against the broadened atlas.
- Caveat: Router-derived fine M-CSA labels are not gold truth; broadening trades coverage for label confidence and should be reported as such.

## Bottom Line

- Broadening the fold atlas beyond the cofactor families is not runnable on current local data: no fine multi-family structure-backed M-CSA label source exists. Off-M-CSA recovery remains validated for the cofactor families; broadening is a separate fine-labelling effort.

## Guardrails

- Read-only inventory; no download, no registry/label/threshold/model change, no held-out read.
