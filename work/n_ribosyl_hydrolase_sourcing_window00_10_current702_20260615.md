# N-ribosyl Hydrolase Sourcing - broadened evidence handles

Run: 2026-06-15T15:50:58Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.2.2 N-ribosyl hydrolases
through nucleoside hydrolase family/name context, N-glycosidic bond
hydrolysis reaction evidence, and active-/binding-site context where available.
EC / keyword / reaction text are scope-admission only, never predictive;
O-glycosidase, phosphorylase, kinase, transferase, DNA glycosylase lyase,
side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: n_ribosyl_hydrolase.
- Lanes queried: 3 (<= 40 rows each).
- Per-lane record window: offset 0, limit 10.
- Fetched candidate rows: 12.
- Target mechanism-corroborated bronze labels: 1 (off-target held 0; disambiguation holds 7; skipped 4).
- **Novelty-admitted labels: 1** (throttled/rejected 0; held@cap 0).
- Combined registry 8122 -> **8123** if merged.

## Floor projection

- `n_ribosyl_hydrolase`: 0 -> 1 (added 1; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'n_ribosyl_hydrolase': 150}.

## Novelty gate

- Decisions: {'admit': 1}.
- Reasons: {'closes_hole_fingerprint': 1}.

## Hold reasons

- {'no_mechanism_corroboration': 7}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
