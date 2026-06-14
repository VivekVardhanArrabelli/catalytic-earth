# Alpha/Beta Hydrolase Esterase/Lipase Sourcing - broadened evidence handles

Run: 2026-06-14T21:32:59Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.1 esterases/lipases
through alpha/beta hydrolase or esterase/lipase family context,
Ser-His-Asp/Glu catalytic-site evidence, and Rhea/reviewed ester hydrolysis.
EC / keyword / reaction text are scope-admission only, never predictive;
protease/amidase, glycoside/transglycosylase, metal-hydrolase, side-EC,
EC-only, and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: alpha_beta_hydrolase_esterase_lipase.
- Lanes queried: 3 (<= 380 rows each).
- Per-lane record window: offset 340, limit 20.
- Fetched candidate rows: 40.
- Target mechanism-corroborated bronze labels: 1 (off-target held 1; disambiguation holds 38; skipped 0).
- **Novelty-admitted labels: 1** (throttled/rejected 0; held@cap 0).
- Combined registry 7860 -> **7861** if merged.

## Floor projection

- `alpha_beta_hydrolase_esterase_lipase`: 0 -> 1 (added 1; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'alpha_beta_hydrolase_esterase_lipase': 150}.

## Novelty gate

- Decisions: {'admit': 1}.
- Reasons: {'closes_hole_fingerprint': 1}.

## Hold reasons

- {'no_mechanism_corroboration': 38}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
