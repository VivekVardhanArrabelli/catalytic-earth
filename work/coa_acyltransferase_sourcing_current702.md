# CoA Acyltransferase Sourcing - broadened evidence handles

Run: 2026-06-13T01:13:10Z

Sources fresh reviewed Swiss-Prot bronze for CoA/acyl-CoA acyltransferases via
CoA/acyl-CoA Rhea participant or binding-site evidence, or Acyltransferase keyword
plus active-/binding-site context with EC 2.3.1 scope. EC / keyword / CoA text are
scope-admission only, never predictive; hydrolase side-EC rows are guarded out.

## Result

- Families sourced: coa_acyltransferase.
- Lanes queried: 4 (<= 80 rows each).
- Fetched candidate rows: 218.
- Target mechanism-corroborated bronze labels: 204 (off-target held 1; disambiguation holds 11; skipped 2).
- **Novelty-admitted labels: 188** (throttled/rejected 16; held@cap 0).
- Combined registry 4574 -> **4762** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| coa_acyltransferase | coa_acyl_coa_donor | 0 | 188 | 188 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 188, 'throttle': 16}.
- Reasons: {'adds_diversity': 88, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 4, 'redundant_no_novelty_signal': 12}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 11}.
- Off-target held counts: {'metallo_amidohydrolase_deaminase': 1}.

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
