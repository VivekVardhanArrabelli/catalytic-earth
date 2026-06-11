# Label Structure Backfill — AlphaFoldDB v6 coordinate provenance (non-destructive preview)

Run: 2026-06-11T16:10:04Z

Stages the AlphaFoldDB v6 predicted coordinate for each expansion label by
accession (`AF-{acc}-F1-model_v6.cif`), hashes it, and records
`evidence.structure_provenance.afdb_v6_coordinate` (handle + sha256 + provenance).
The CIFs are regeneratable from the handle and are NOT committed. Structure is
review-only mechanism context (a bronze->silver signal), never a predictive feature.
The frozen current702 benchmark is NOT written.

## Result

- Expansion labels: 2940 (row count unchanged).
- **Staged this run: 2890** (already staged 0; unavailable 50; deferred over --limit 0).
- Rows with a staged coordinate after: 2890 (98.3% coverage).
- AFDB fetches this run: 0.

Status breakdown: {'afdb_v6_predicted_coordinate_staged': 2890, 'afdb_v6_unavailable': 50}.

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- Large CIFs never committed; coordinate regeneratable from handle; existing structure_provenance preserved (additive); structure is review-only, not predictive.

## Next action

- Review counts, then re-run with --apply to write data/registries/external_bronze_labels.json (frozen current702 never written; row count unchanged; only evidence.structure_provenance.afdb_v6_coordinate added). Use --limit for chunked runs; the cache makes re-runs resumable.

## AFDB v6 unavailable (50 accessions, first 200)

A0A024B7W1, A0A1L4BKS3, A1YES6, C5IY43, D0EZM8, O39521, O39522, O39828, O43451, O89049, O91254, P03133, P03134, P03567, P03694, P03708, P07300, P07636, P0C647, P0CK60, P0DY11, P10310, P17312, P24030, P26745, P27260, P36311, P82679, Q03164, Q16881, Q17745, Q5NVA2, Q65202, Q66862, Q805H4, Q811C4, Q86BA1, Q86VQ6, Q8BB16, Q8YD09, Q99MD6, Q9JLT4, Q9JMH6, Q9MCT1, Q9N2I8, Q9NNW7, Q9PZT1, Q9WIJ5, Q9WIK0, Q9Z0J5
