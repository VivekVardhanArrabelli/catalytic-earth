# Glycoside Hydrolase Sourcing - broadened evidence handles

Run: 2026-06-13T18:12:25Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.2.1 glycoside hydrolases via
glycosidase family text, reviewed glycosidic-bond hydrolysis reaction context,
and active-/binding-site acid/base or nucleophile annotations. EC / keyword /
reaction text are scope-admission only, never predictive; transferase,
transglycosylase, phosphorylase, lyase, side-EC, EC-only, and multi-signal rows
are guarded out.

## Result

- Families sourced: glycoside_hydrolase.
- Lanes queried: 1 (<= 500 rows each).
- Query pages per lane: 2.
- Per-lane record window: offset 500, limit 80.
- Fetched candidate rows: 80.
- Target mechanism-corroborated bronze labels: 0 (off-target held 0; disambiguation holds 36; skipped 44).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 7190 -> **7190** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| glycoside_hydrolase | glycosidic_substrate_ordered_water_hydrolysis_context | 84 | 0 | 84 | 150 | False | 0 |

## Novelty gate

- Decisions: {}.
- Reasons: {}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 36}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Glycoside hydrolase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Transferase/phosphorylase/lyase/side-EC guard: True.
- Per-family cap ceiling: {'glycoside_hydrolase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` with frozen current702 sha checks.
