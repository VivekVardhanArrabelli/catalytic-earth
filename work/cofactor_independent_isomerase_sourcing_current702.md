# Cofactor-Independent Isomerase Sourcing - broadened evidence handles

Run: 2026-06-13T01:38:56Z

Sources fresh reviewed Swiss-Prot bronze for cofactor-independent isomerases via
Rhea isomerization equation text or Isomerase keyword plus active-/binding-site
context with EC 5.3 scope. EC / keyword / reaction text are scope-admission
only, never predictive; non-5.3 side-EC rows are guarded out.

## Result

- Families sourced: cofactor_independent_isomerase.
- Lanes queried: 4 (<= 80 rows each).
- Fetched candidate rows: 266.
- Target mechanism-corroborated bronze labels: 147 (off-target held 28; disambiguation holds 70; skipped 21).
- **Novelty-admitted labels: 142** (throttled/rejected 5; held@cap 0).
- Combined registry 4762 -> **4904** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cofactor_independent_isomerase | active_site_base_isomerization_context | 0 | 142 | 142 | 150 | True | 0 |

## Novelty gate

- Decisions: {'admit': 142, 'throttle': 5}.
- Reasons: {'adds_diversity': 42, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 5}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 70}.
- Off-target held counts: {'nad_p_dehydrogenase': 28}.

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
