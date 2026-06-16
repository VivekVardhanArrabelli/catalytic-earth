# PDE Reaction-Cap-Trimmed Tier-2 Preview

Source preview: `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_combined_local_slice_preview_current702_20260616_run1302.json`.

## Result

- Untrimmed combined novelty-admitted rows: 116.
- Kept rows: 100.
- Reaction-aware trimmed rows: 16.
- Floor projection: 0 -> 100; floor reached: True.
- Distinct reactions after trim: 1.
- Reaction-aware cap after trim: 100.
- Reaction saturated after trim: False.

## Guardrails

- Registry written: false.
- Frozen current702 written: false.
- EC/name/source handles remain excluded context and never predictive evidence.
- Trimmed rows stay held, not imported.
