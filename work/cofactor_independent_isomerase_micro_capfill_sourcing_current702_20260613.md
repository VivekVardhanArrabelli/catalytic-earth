# Cofactor-Independent Isomerase Sourcing - broadened evidence handles

Run: 2026-06-13T14:33:42Z

Sources fresh reviewed Swiss-Prot bronze for cofactor-independent isomerases via
Rhea isomerization equation text or Isomerase keyword plus active-/binding-site
context with EC 5.3 scope. EC / keyword / reaction text are scope-admission
only, never predictive; non-5.3 side-EC rows are guarded out.

## Result

- Families sourced: cofactor_independent_isomerase.
- Lanes queried: 4 (<= 5 rows each).
- Fetched candidate rows: 14.
- Target mechanism-corroborated bronze labels: 0 (off-target held 2; disambiguation holds 5; skipped 7).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 6940 -> **6940** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cofactor_independent_isomerase | active_site_base_isomerization_context | 142 | 0 | 142 | 150 | True | 0 |

## Novelty gate

- Decisions: {}.
- Reasons: {}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 5}.
- Off-target held counts: {'nad_p_dehydrogenase': 2}.

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
