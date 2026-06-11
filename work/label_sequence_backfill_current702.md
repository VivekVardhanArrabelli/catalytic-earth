# Label Sequence Backfill — deploy-input sequence for expansion bronze (non-destructive preview)

Run: 2026-06-11T15:37:09Z

Backfills `evidence.sequence_provenance` (the raw protein SEQUENCE the model
predicts FROM) onto every expansion bronze label by fetching the reviewed UniProt
sequence by accession. The sequence is stored DATA, never a predictive feature:
the leakage wall (EC / protein name / UniProt prose) is unchanged and
`predictive_evidence` stays []. The frozen current702 benchmark is NOT written.

## Result

- Expansion labels: 2940 (row count unchanged).
- Needed fetch: 2940; distinct accessions fetched: 2940.
- **Backfilled this run: 2940** (already backfilled 0; fetch-missing 0).
- Rows with sequence after: 2940 (100.0% coverage).
- Length conflicts (stored vs fetched): 0.

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- Sequence is the deploy INPUT, not a predictive feature; stored source_provenance never overwritten; sequence never fabricated.

## Next action

- Review counts/conflicts, then on explicit authorization re-run with --apply to write data/registries/external_bronze_labels.json (frozen current702 never written; row count unchanged; only evidence.sequence_provenance added).
