# Glycoside Hydrolase Sourcing - broadened evidence handles

Run: 2026-06-13T23:17:37Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.2.1 glycoside hydrolases via
glycosidase family text, reviewed glycosidic-bond hydrolysis reaction context,
and active-/binding-site acid/base or nucleophile annotations. EC / keyword /
reaction text are scope-admission only, never predictive; transferase,
transglycosylase, phosphorylase, lyase, side-EC, EC-only, and multi-signal rows
are guarded out.

## Result

- Families sourced: glycoside_hydrolase.
- Lanes queried: 1 (<= 120 rows each).
- Query pages per lane: 1.
- Per-lane record window: offset 40, limit 40.
- Source trust tier: source_tier_2.
- Unreviewed tier-2 lanes enabled: False (only: True).
- Fetched candidate rows: 40.
- Target mechanism-corroborated bronze labels: 40 (off-target held 0; disambiguation holds 0; skipped 0).
- **Novelty-admitted labels: 34** (throttled/rejected 6; held@cap 0).
- Combined registry 7488 -> **7522** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| glycoside_hydrolase | glycosidic_substrate_ordered_water_hydrolysis_context | 107 | 34 | 141 | 150 | True | 0 |

## Novelty gate

- Decisions: {'admit': 34, 'throttle': 6}.
- Reasons: {'adds_diversity': 34, 'redundant_no_novelty_signal': 6}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Glycoside hydrolase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Source trust tier: source_tier_2; tier-2 three-axis gate: True.
- Transferase/phosphorylase/lyase/side-EC guard: True.
- Per-family cap ceiling: {'glycoside_hydrolase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` with frozen current702 sha checks.
