# Ser/Thr Protein Phosphatase Live Sourcing Blocker

Run: 2026-06-14T22:03:34Z automation (`ce-nad-glyco-floor-expansion`)

## What Was Attempted

- Full non-destructive preview:
  `PYTHONPATH=src python scripts/source_ser_thr_protein_phosphatase_family.py --max-records-per-lane 260 --out artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_current702_20260614.json --report work/ser_thr_protein_phosphatase_sourcing_current702_20260614.md`
- Bounded 20-row preview:
  `PYTHONPATH=src python scripts/source_ser_thr_protein_phosphatase_family.py --max-records-per-lane 260 --record-limit-per-lane 20 --out artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window00_current702_20260614.json --report work/ser_thr_protein_phosphatase_sourcing_window00_current702_20260614.md`
- Bounded 5-row preview with the same output/report path as the 20-row window.
- Bounded 1-row preview with the same output/report path as the 20-row window.

## Result

No preview artifact was written, and no labels were applied. Each live preview was interrupted
after UniProt REST responses stalled inside `urllib` reads. The full and 20/5-row attempts reached
entry JSON fetches; the 1-row attempt later stalled during the search TSV read. Search-only probes
did return first-page accessions quickly, so the lane design appears viable, but the full ingestion
path was not reliable enough to support a preview, row guardrail audit, or registry apply in this
run.

After adding per-fetch timeouts, eleven adjacent bounded windows completed non-destructively:
`artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_timeout_window00_current702_20260614.json`
through
`artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_timeout_window08_current702_20260614.json`,
plus
`artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_timeout_window09_11_current702_20260614.json`
and
`artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_timeout_window12_14_current702_20260614.json`.
Across offsets 0-14, the bounded probes fetched **13** candidate rows, admitted **0** target rows,
held **13** rows for `no_mechanism_corroboration`, and recorded **26** fetch failures. This is not
enough material for aggregation, row guardrail audit, or apply.

## Safety Decision

- Do not apply any `ser_thr_protein_phosphatase` bronze rows until a complete preview and row-level
  guardrail audit exist.
- The new fingerprint, ontology node, disambiguation rule, source runner, OOS preregistration, and
  tests are local-infrastructure changes only. They do not mutate the external bronze registry.
- The high-yield factory now recognizes the lane as an existing runner with cap room; the next
  action is to rerun larger bounded windows when UniProt entry/search responses are stable, or add
  a repo-supported batch entry fetch/cache path before previewing.
