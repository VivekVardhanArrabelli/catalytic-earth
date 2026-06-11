# Stage-2 Hydrolase Sub-Family Sourcing — metal_dependent_hydrolase v2 split (non-destructive preview)

Run: 2026-06-11T10:50:47Z

Sources fresh reviewed Swiss-Prot bronze for the four metal_dependent_hydrolase
v2 sub-families via the existing fetch -> metal/EC disambiguation -> novelty-gate
-> cap-guard pipeline. EC/name/prose are scope-only (never predictive); tier=bronze;
the frozen current702 benchmark is NOT written. No new labels go to the coarse
metal_dependent_hydrolase umbrella.

## Result

- Sub-families sourced: metallopeptidase, metallophosphoesterase_nuclease, metallophosphomonoesterase, metallo_amidohydrolase_deaminase.
- Lanes queried: 15 (<= 120 rows each).
- Fetched candidate rows: 1530.
- Disambiguated bronze labels: 1167 (held 69, skipped 294).
- **Novelty-admitted labels: 600** (throttled/rejected 206; held@cap 361).
- Combined registry 3042 -> **3642** if merged.

## Floor projection (100-label floor)

| Sub-family | combined before | admitted | projected | floor reached | held@cap |
| --- | --- | --- | --- | --- | --- |
| metallopeptidase | 0 | 150 | 150 | True | 101 |
| metallophosphoesterase_nuclease | 0 | 150 | 150 | True | 104 |
| metallophosphomonoesterase | 0 | 150 | 150 | True | 54 |
| metallo_amidohydrolase_deaminase | 0 | 150 | 150 | True | 102 |

## Novelty gate

- Decisions: {'admit': 961, 'reject': 102, 'throttle': 104}.
- Reasons: {'adds_diversity': 557, 'closes_hole_fingerprint': 104, 'closes_under_floor_fingerprint': 296, 'fingerprint_over_cap_no_new_chemistry': 102, 'needed_fingerprint_but_redundant_ortholog': 13, 'over_cap_but_new_reaction_chemistry': 4, 'redundant_no_novelty_signal': 91}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- No new labels added to the coarse umbrella: True.
- Deploy-missing active-site context per sub-family: metal.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on explicit authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written). Held/throttled rows are the next batch.
