# Metal-independent Phosphodiesterase 43fp Source Strategy

Run: 2026-06-15 automation `ce-nad-glyco-floor-expansion`

## Summary

The `metal_independent_phosphodiesterase` fingerprint and ontology infrastructure is now wired for
the live positive universe, but the tested UniProt source handles do not justify a registry apply.
No bronze rows were written. Frozen current702 remained untouched, and the sharded external bronze
registry stayed at 7570 rows.

## What changed

- Added the 43rd positive fingerprint, `metal_independent_phosphodiesterase`.
- Added ontology family `metal_independent_phosphodiester_hydrolysis`.
- Refreshed the hard-negative OOS preregistration for `label_factory_v1_43fp`:
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_43fp_1025.json`.
- Added a reusable reviewed-UniProt source runner:
  `src/catalytic_earth/metal_independent_phosphodiesterase_sourcing.py` and
  `scripts/source_metal_independent_phosphodiesterase_family.py`.
- Wired coverage/governor, deploy context, high-yield factory status, leakage preregistration tests,
  and focused source-wall tests.

## Source handle results

Reviewed Swiss-Prot runner preview:

- Artifact:
  `artifacts/v3_metal_independent_phosphodiesterase_sourcing_preview_cursor_pages4_size80_current702_20260615.json`
- Report:
  `work/metal_independent_phosphodiesterase_sourcing_preview_cursor_pages4_size80_current702_20260615.md`
- Fetched candidates: 265.
- Target mechanism-corroborated labels: 18.
- Novelty-admitted labels: 14.
- Off-target holds: 52, mainly metallophosphoesterase/nuclease and SAM methyltransferase boundary
  rows.
- Main non-admission reason: 183 rows without mechanism corroboration.

Alternate reviewed source handles:

- Count scout:
  `artifacts/v3_metal_independent_phosphodiesterase_additional_source_handle_count_scout_current702_20260615.json`
- Preview:
  `artifacts/v3_metal_independent_phosphodiesterase_alternate_handle_preview_current702_20260615.json`
- Report:
  `work/metal_independent_phosphodiesterase_alternate_handle_preview_current702_20260615.md`
- Fetched candidates: 130.
- Target labels: 0.
- Novelty-admitted labels: 0.

Unreviewed tier-2 PDE handles:

- Count scout:
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_source_count_scout_current702_20260615.json`
- Preview:
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_sourcing_preview_cursor_pages2_size100_current702_20260615.json`
- Report:
  `work/metal_independent_phosphodiesterase_tier2_sourcing_preview_cursor_pages2_size100_current702_20260615.md`
- Fetched candidates: 400.
- Target labels: 0.
- Novelty-admitted labels: 0.
- Off-target holds: 186, all routed away from PDE.
- Tier-2 trust holds: 197 `trust_tier_corroboration_insufficient`.

## Guardrail interpretation

- EC 3.1.4 / 4.6.1 and protein-name/query handles are scope/admission context only.
- Metal absence is a filter and never counted as evidence.
- `predictive_evidence` remains empty for generated rows.
- Tier-2 rows require `source_tier_2` plus at least three independent mechanism-bearing axes before
  admission; the tested tier-2 PDE windows did not meet that standard.
- The reviewed 14-row preview is clean enough as source-wall evidence, but it is far below the
  150-row batch gate and should not be padded.

## Current queue implication

The refreshed factory after this infrastructure reports:

- Combined label surface: 8272.
- Combined seed surface: 6576.
- Current positive universe: `label_factory_v1_43fp`.
- Holes/under-floor fingerprints: `metal_independent_phosphodiesterase`.
- Ready existing lanes with at least 150 projected clean admits: 0.
- Best projected new-family lane under current handles: `short_chain_dehydrogenase_reductase` at
  84 projected clean admits.

Next action: stop retrying the same PDE UniProt handles for mass growth. Either design a materially
sharper PDE mechanism-bearing source split, or move to a higher-yield source-handle/source-tier
strategy such as SDR/AKR with a family-specific source wall, fresh OOS preregistration if the
fingerprint universe changes, non-destructive preview, row guardrail audit, and novelty/governor
apply gate.
