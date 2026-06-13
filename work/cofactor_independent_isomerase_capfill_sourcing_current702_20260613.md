# Cofactor-Independent Isomerase Sourcing - broadened evidence handles

Run: 2026-06-13T21:14:28Z

Sources fresh reviewed Swiss-Prot bronze for cofactor-independent isomerases via
Rhea isomerization equation text or Isomerase keyword plus active-/binding-site
context with EC 5.3 scope. EC / keyword / reaction text are scope-admission
only, never predictive; non-5.3 side-EC rows are guarded out.

## Result

- Families sourced: cofactor_independent_isomerase.
- Lanes queried: 4 (<= 120 rows each).
- Fetched candidate rows: 405.
- Target mechanism-corroborated bronze labels: 91 (off-target held 61; disambiguation holds 90; skipped 163).
- **Novelty-admitted labels: 8** (throttled/rejected 11; held@cap 72).
- Combined registry 7232 -> **7240** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cofactor_independent_isomerase | active_site_base_isomerization_context | 142 | 8 | 150 | 150 | True | 72 |

## Novelty gate

- Decisions: {'admit': 80, 'throttle': 11}.
- Reasons: {'adds_diversity': 80, 'redundant_no_novelty_signal': 11}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 90}.
- Off-target held counts: {'nad_p_dehydrogenase': 61}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Isomerase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Non-5.3 side-EC guard: True.
- Per-family cap ceiling: {'cofactor_independent_isomerase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` with frozen current702 sha checks.
