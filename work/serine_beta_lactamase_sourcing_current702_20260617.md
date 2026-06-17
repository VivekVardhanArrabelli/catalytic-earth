# Serine Beta-lactamase Sourcing - guarded beta-lactam hydrolysis handles

Run: 2026-06-17T20:08:44Z

Sources bronze labels for exact EC 3.5.2.6 serine beta-lactamases through
beta-lactamase family/name context, beta-lactam hydrolysis reaction evidence,
and active-site Ser/Lys/Glu residue-role context. EC, names, keywords,
reaction text, and source handles are scope/admission context only, never
predictive. Metallo/zinc beta-lactamases, PBPs/DD-peptidases, generic
amidohydrolases, synthases, resistance-only, side-EC, EC-only, and
multi-fingerprint rows are guarded.

## Result

- Families sourced: serine_beta_lactamase.
- Lanes queried: 1 (<= 250 rows each).
- Per-lane record window: offset 0, limit None.
- Source trust tier: source_tier_0.
- Fetched candidate rows: 128.
- Target mechanism-corroborated bronze labels: 121 (off-target held 0; disambiguation holds 3; skipped 4).
- **Novelty-admitted labels: 44** (throttled/rejected 63; held@cap 14).
- Combined registry 8772 -> **8816** if merged.

## Floor projection

- `serine_beta_lactamase`: 106 -> 150 (added 44; cap 150; floor reached: True; held@cap 14).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'serine_beta_lactamase': 150}.

## Novelty gate

- Decisions: {'admit': 58, 'throttle': 63}.
- Reasons: {'adds_diversity': 58, 'redundant_no_novelty_signal': 63}.

## Hold reasons

- {'no_mechanism_corroboration': 3}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
