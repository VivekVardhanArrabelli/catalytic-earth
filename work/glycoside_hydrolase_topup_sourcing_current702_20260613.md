# Glycoside Hydrolase Sourcing - broadened evidence handles

Run: 2026-06-13T17:09:15Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.2.1 glycoside hydrolases via
glycosidase family text, reviewed glycosidic-bond hydrolysis reaction context,
and active-/binding-site acid/base or nucleophile annotations. EC / keyword /
reaction text are scope-admission only, never predictive; transferase,
transglycosylase, phosphorylase, lyase, side-EC, EC-only, and multi-signal rows
are guarded out.

## Result

- Families sourced: glycoside_hydrolase.
- Lanes queried: 1 (<= 420 rows each).
- Fetched candidate rows: 420.
- Target mechanism-corroborated bronze labels: 27 (off-target held 0; disambiguation holds 290; skipped 103).
- **Novelty-admitted labels: 27** (throttled/rejected 0; held@cap 0).
- Combined registry 7151 -> **7178** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| glycoside_hydrolase | glycosidic_substrate_ordered_water_hydrolysis_context | 45 | 27 | 72 | 150 | False | 0 |

## Novelty gate

- Decisions: {'admit': 27}.
- Reasons: {'closes_under_floor_fingerprint': 27}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 290}.
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
