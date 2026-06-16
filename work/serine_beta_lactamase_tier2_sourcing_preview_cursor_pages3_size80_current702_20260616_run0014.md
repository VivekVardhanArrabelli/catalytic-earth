# Serine Beta-lactamase Sourcing - guarded beta-lactam hydrolysis handles

Run: 2026-06-16T00:28:50Z

Sources bronze labels for exact EC 3.5.2.6 serine beta-lactamases through
beta-lactamase family/name context, beta-lactam hydrolysis reaction evidence,
and active-site Ser/Lys/Glu residue-role context. EC, names, keywords,
reaction text, and source handles are scope/admission context only, never
predictive. Metallo/zinc beta-lactamases, PBPs/DD-peptidases, generic
amidohydrolases, synthases, resistance-only, side-EC, EC-only, and
multi-fingerprint rows are guarded.

## Result

- Families sourced: serine_beta_lactamase.
- Lanes queried: 1 (<= 80 rows each).
- Per-lane record window: offset 0, limit None.
- Source trust tier: source_tier_2.
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 115 (off-target held 0; disambiguation holds 122; skipped 3).
- **Novelty-admitted labels: 106** (throttled/rejected 9; held@cap 0).
- Combined registry 8522 -> **8628** if merged.

## Floor projection

- `serine_beta_lactamase`: 0 -> 106 (added 106; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'serine_beta_lactamase': 150}.

## Novelty gate

- Decisions: {'admit': 106, 'throttle': 9}.
- Reasons: {'adds_diversity': 6, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 8, 'redundant_no_novelty_signal': 1}.

## Hold reasons

- {'no_mechanism_corroboration': 122}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
