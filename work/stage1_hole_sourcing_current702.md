# Stage-1 Hole Sourcing — Cofactor-Defined Holes (non-destructive preview)

Run: 2026-06-10T19:35:42Z

Sources fresh reviewed Swiss-Prot bronze for the cofactor-defined holes via
the existing fetch -> cofactor/EC disambiguation -> novelty-gate pipeline.
EC/name/prose are scope-only (never predictive); tier=bronze; the frozen
current702 benchmark is NOT written. ser_his uses the triad-locator tool.

## Result

- Holes sourced: radical_sam_enzyme, cobalamin_radical_rearrangement.
- Lanes queried: 10 (<= 100 rows each).
- Fetched candidate rows: 548.
- Disambiguated bronze labels: 259 (held 277, skipped 12).
- **Novelty-admitted labels: 257** (throttled/rejected 2).
- Combined registry 2412 -> **2669** if merged.

## Floor projection (100-label floor)

| Hole | combined before | admitted | projected | floor reached |
| --- | --- | --- | --- | --- |
| radical_sam_enzyme | 10 | 123 | 133 | True |
| cobalamin_radical_rearrangement | 10 | 134 | 144 | True |

## Novelty gate

- Decisions: {'admit': 257, 'throttle': 2}.
- Reasons: {'adds_diversity': 77, 'closes_hole_fingerprint': 32, 'closes_under_floor_fingerprint': 148, 'redundant_no_novelty_signal': 2}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on explicit authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written). Held/throttled rows are the next batch.
