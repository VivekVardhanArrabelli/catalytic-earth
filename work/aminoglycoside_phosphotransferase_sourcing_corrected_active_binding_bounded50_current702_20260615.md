# Aminoglycoside Phosphotransferase Sourcing - exact EC mechanism handles

Run: 2026-06-15T20:53:48Z

Sources fresh reviewed Swiss-Prot bronze for exact APH EC scopes through APH
family/name context, ATP/Mg or ADP/phosphate context, aminoglycoside
phosphorylation reaction evidence, and active-/binding-site context.
EC / keyword / reaction text are scope-admission only, never predictive;
protein kinase, small-molecule kinase, aminoglycoside acetyltransferase,
nucleotidyltransferase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: aminoglycoside_phosphotransferase.
- Lanes queried: 1 (<= 50 rows each).
- Per-lane record window: offset 0, limit 50.
- Fetched candidate rows: 18.
- Target mechanism-corroborated bronze labels: 17 (off-target held 0; disambiguation holds 0; skipped 1).
- **Novelty-admitted labels: 17** (throttled/rejected 0; held@cap 0).
- Combined registry 8272 -> **8289** if merged.

## Floor projection

- `aminoglycoside_phosphotransferase`: 0 -> 17 (added 17; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'aminoglycoside_phosphotransferase': 150}.

## Novelty gate

- Decisions: {'admit': 17}.
- Reasons: {'closes_hole_fingerprint': 17}.

## Hold reasons

- {}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
