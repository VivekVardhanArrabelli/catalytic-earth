# Cysteine-Protease Sourcing - broadened evidence handles

Run: 2026-06-27T03:39:50Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.4.22 cysteine (thiol)
proteases (papain / caspase / legumain / calpain / deubiquitinase clans)
through an annotated catalytic active site (the catalytic Cys nucleophile /
Cys-His dyad) plus a cysteine/thiol-peptidase or protease family/name.
EC / keyword / name text are scope-admission only, never predictive;
serine proteases, aspartic proteases, metallopeptidases, protease inhibitors,
side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: cysteine_protease.
- Lanes queried: 3 (<= 200 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 280.
- Target mechanism-corroborated bronze labels: 219 (off-target held 4; disambiguation holds 56; skipped 1).
- **Novelty-admitted labels: 150** (throttled/rejected 24; held@cap 45).
- Combined registry 9627 -> **9777** if merged.

## Floor projection

- `cysteine_protease`: 0 -> 150 (added 150; cap 150; floor reached: True; held@cap 45).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'cysteine_protease': 150}.

## Novelty gate

- Decisions: {'admit': 195, 'throttle': 24}.
- Reasons: {'adds_diversity': 95, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 4, 'redundant_no_novelty_signal': 20}.

## Hold reasons

- {'no_mechanism_corroboration': 50, 'multi_fingerprint_signal_conflict': 6}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
