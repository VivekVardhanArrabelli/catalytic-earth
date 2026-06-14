# Holo Structure Promotion — experimental-PDB cofactor confirmation (non-destructive preview)

Run: 2026-06-14T12:20:21Z

Supplies the missing HOLO signal the bronze->silver gate needs. AlphaFold predictions are apo (no cofactor), so silver_ready was stuck at 0; this confirms the annotated cofactor IS present in an EXPERIMENTAL PDB for chemistry-corroborated labels, recording a sha-pinned holo_pdb_confirmation. The mmCIFs are regeneratable from the PDB id and are NOT committed. Structure is review-only mechanism context.

- Seed labels: 5638.
- **Holo confirmed this run: 109** (already confirmed 0; total after 109).
- No holo PDB found: 44; not corroborated: 507; no pdb/cofactor: 4760.
- Deferred (limit/cap): 0/218; rows fetched this run: 113.

## Holo confirmed by fingerprint

| fingerprint | confirmed |
| --- | --- |
| askha_sugar_acetate_kinase | 1 |
| atp_amide_ligase | 6 |
| biotin_dependent_carboxylase | 3 |
| class_ii_metal_aldolase | 2 |
| cytochrome_p450_monooxygenase | 7 |
| deoxynucleoside_kinase | 1 |
| flavin_dehydrogenase_reductase | 6 |
| flavin_monooxygenase | 6 |
| glycoside_hydrolase | 3 |
| glycosyltransferase | 7 |
| heme_peroxidase_oxidase | 2 |
| manganese_iron_superoxide_dismutase | 8 |
| metallo_amidohydrolase_deaminase | 8 |
| metallophosphomonoesterase | 7 |
| nad_p_dehydrogenase | 8 |
| non_heme_iron_2og_dioxygenase | 3 |
| nucleoside_diphosphate_kinase | 1 |
| pfka_phosphofructokinase | 4 |
| plp_dependent_enzyme | 1 |
| protein_kinase_ser_thr_tyr | 3 |
| radical_sam_enzyme | 3 |
| terpene_cyclase_synthase | 7 |
| thiamine_diphosphate_enzyme | 6 |
| zinc_lyase_hydratase | 6 |

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- Large mmCIFs never committed; coordinate regeneratable from PDB id; existing structure_provenance preserved (additive); structure review-only, not predictive.

## Next action

- Review counts, then re-run with --apply to write data/registries/external_bronze_labels.json (frozen current702 never written, sha printed before/after; row count unchanged; only evidence.structure_provenance.holo_pdb_confirmation added). The confirmed rows become silver_ready_pending_geometry_run in the promotion preview -- still pending the SEPARATE authorized geometry-confirmation run. Use --limit / --per-fingerprint-cap for chunked runs; the cache makes re-runs resumable.
