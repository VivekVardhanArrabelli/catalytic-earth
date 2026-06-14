# Holo Structure Promotion — experimental-PDB cofactor confirmation (non-destructive preview)

Run: 2026-06-14T12:44:43Z

Supplies the missing HOLO signal the bronze->silver gate needs. AlphaFold predictions are apo (no cofactor), so silver_ready was stuck at 0; this confirms the annotated cofactor IS present in an EXPERIMENTAL PDB for chemistry-corroborated labels, recording a sha-pinned holo_pdb_confirmation. The mmCIFs are regeneratable from the PDB id and are NOT committed. Structure is review-only mechanism context.

- Seed labels: 5638.
- **Holo confirmed this run: 151** (already confirmed 109; total after 260).
- No holo PDB found: 111; not corroborated: 507; no pdb/cofactor: 4760.
- Deferred (limit/cap): 0/0; rows fetched this run: 218.

## Holo confirmed by fingerprint

| fingerprint | confirmed |
| --- | --- |
| atp_amide_ligase | 6 |
| cytochrome_p450_monooxygenase | 23 |
| flavin_dehydrogenase_reductase | 27 |
| flavin_monooxygenase | 6 |
| glycosyltransferase | 1 |
| manganese_iron_superoxide_dismutase | 6 |
| metallo_amidohydrolase_deaminase | 19 |
| metallophosphomonoesterase | 29 |
| nad_p_dehydrogenase | 5 |
| non_heme_iron_2og_dioxygenase | 5 |
| protein_kinase_ser_thr_tyr | 16 |
| terpene_cyclase_synthase | 1 |
| zinc_lyase_hydratase | 7 |

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- Large mmCIFs never committed; coordinate regeneratable from PDB id; existing structure_provenance preserved (additive); structure review-only, not predictive.

## Next action

- Review counts, then re-run with --apply to write data/registries/external_bronze_labels.json (frozen current702 never written, sha printed before/after; row count unchanged; only evidence.structure_provenance.holo_pdb_confirmation added). The confirmed rows become silver_ready_pending_geometry_run in the promotion preview -- still pending the SEPARATE authorized geometry-confirmation run. Use --limit / --per-fingerprint-cap for chunked runs; the cache makes re-runs resumable.
