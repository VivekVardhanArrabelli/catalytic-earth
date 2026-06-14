# Ser/Thr Protein Phosphatase Aggregate Sourcing Preview

Run: 2026-06-14T23:26:33Z

Contiguous bounded-window aggregate after the Ser/Thr Rhea seryl/threonyl protein reaction-token fix.

## Result

- Source windows: 8.
- Fetched candidate rows: 743.
- Unique mechanism-corroborated Ser/Thr candidates before novelty replay: 170.
- Novelty-admitted labels after aggregate replay and cap: 112.
- Held at cap: 0; novelty throttled/rejected before cap: 58.
- Registry projection: 8010 -> 8122 if merged.
- Fetch failures: 0.

## Guardrails

- Frozen current702 is not written by this artifact.
- EC, protein names, keywords, source prose, and broadened handles remain excluded context.
- `predictive_evidence` remains empty on admitted labels.
- Apply is blocked until the row guardrail audit is clean.

## Source Windows

- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window00_10_post_rhea_token_fix_current702_20260614.json`: admitted 4 / fetched 30.
- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window10_30_post_rhea_token_fix_current702_20260614.json`: admitted 9 / fetched 58.
- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window30_60_post_rhea_token_fix_current702_20260614.json`: admitted 22 / fetched 90.
- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window60_100_post_rhea_token_fix_current702_20260614.json`: admitted 26 / fetched 106.
- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window100_140_post_rhea_token_fix_current702_20260614.json`: admitted 25 / fetched 108.
- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window140_180_post_rhea_token_fix_current702_20260614.json`: admitted 34 / fetched 114.
- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window180_220_post_rhea_token_fix_current702_20260614.json`: admitted 47 / fetched 120.
- `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window220_260_post_rhea_token_fix_current702_20260614.json`: admitted 39 / fetched 117.
