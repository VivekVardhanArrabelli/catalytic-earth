# Stage-1 Hole Sourcing — Cofactor-Defined Holes (non-destructive preview)

Run: 2026-06-14T00:31:56Z

Sources fresh reviewed Swiss-Prot bronze for the cofactor-defined holes via
the existing fetch -> cofactor/EC disambiguation -> novelty-gate pipeline.
EC/name/prose are scope-only (never predictive); tier=bronze; the frozen
current702 benchmark is NOT written. ser_his uses the triad-locator tool.

## Result

- Holes sourced: radical_sam_enzyme, cobalamin_radical_rearrangement.
- Lanes queried: 10 (<= 180 rows each).
- Per-lane record window: offset 100, limit 40.
- Fetched candidate rows: 160.
- Disambiguated bronze labels: 82 (held 78, skipped 0).
- **Novelty-admitted labels: 81** (throttled/rejected 0).
- Combined registry 7661 -> **7742** if merged.

## Floor projection (100-label floor)

| Fingerprint | combined before | admitted | projected | floor reached | held@cap | over cap |
| --- | --- | --- | --- | --- | --- | --- |
| radical_sam_enzyme | 133 | 81 | 214 | True | 0 | False |
| cobalamin_radical_rearrangement | 144 | 0 | 144 | True | 0 | False |

## Novelty gate

- Decisions: {'admit': 82}.
- Reasons: {'adds_diversity': 82}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on explicit authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written). Held/throttled rows are the next batch.
