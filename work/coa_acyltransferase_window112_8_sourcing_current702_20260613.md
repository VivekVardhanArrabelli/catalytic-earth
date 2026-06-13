# CoA Acyltransferase Sourcing - broadened evidence handles

Run: 2026-06-13T22:26:21Z

Sources fresh reviewed Swiss-Prot bronze for CoA/acyl-CoA acyltransferases via
CoA/acyl-CoA Rhea participant or binding-site evidence, or Acyltransferase keyword
plus active-/binding-site context with EC 2.3.1 scope. EC / keyword / CoA text are
scope-admission only, never predictive; hydrolase side-EC rows are guarded out.

## Result

- Families sourced: coa_acyltransferase.
- Lanes queried: 4 (<= 500 rows each).
- Fetched candidate rows: 24.
- Target mechanism-corroborated bronze labels: 23 (off-target held 0; disambiguation holds 0; skipped 1).
- **Novelty-admitted labels: 7** (throttled/rejected 11; held@cap 5).
- Combined registry 7340 -> **7347** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| coa_acyltransferase | coa_acyl_coa_donor | 243 | 7 | 250 | 250 | True | 5 |

## Novelty gate

- Decisions: {'admit': 12, 'reject': 11}.
- Reasons: {'adds_diversity': 8, 'fingerprint_over_cap_no_new_chemistry': 11, 'over_cap_but_new_reaction_chemistry': 4}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- CoA/acyltransferase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Hydrolase side-EC guard: True.
- Per-family cap ceiling: {'coa_acyltransferase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` with frozen current702 sha checks.
