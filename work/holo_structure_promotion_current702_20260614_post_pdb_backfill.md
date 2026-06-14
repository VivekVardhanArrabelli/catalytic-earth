# Holo Structure Promotion — experimental-PDB cofactor confirmation (non-destructive preview)

Run: 2026-06-14T15:31:18Z

Supplies the missing HOLO signal the bronze->silver gate needs. AlphaFold predictions are apo (no cofactor), so silver_ready was stuck at 0; this confirms the annotated cofactor IS present in an EXPERIMENTAL PDB for chemistry-corroborated labels, recording a sha-pinned holo_pdb_confirmation. The mmCIFs are regeneratable from the PDB id and are NOT committed. Structure is review-only mechanism context.

- Seed labels: 5638.
- **Holo confirmed this run: 0** (already confirmed 260; total after 260).
- No holo PDB found: 50; not corroborated: 507; no pdb/cofactor: 4760.
- Deferred (limit/cap): 61/0; rows fetched this run: 50.

## Holo confirmed by fingerprint

| fingerprint | confirmed |
| --- | --- |

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- Large mmCIFs never committed; coordinate regeneratable from PDB id; existing structure_provenance preserved (additive); structure review-only, not predictive.

## Next action

- Review counts, then re-run with --apply to write data/registries/external_bronze_labels.json (frozen current702 never written, sha printed before/after; row count unchanged; only evidence.structure_provenance.holo_pdb_confirmation added). The confirmed rows become silver_ready_pending_geometry_run in the promotion preview -- still pending the SEPARATE authorized geometry-confirmation run. Use --limit / --per-fingerprint-cap for chunked runs; the cache makes re-runs resumable.
