# Dihydrofolate-Reductase Sourcing - broadened evidence handles

Run: 2026-06-27T19:30:01Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.5.1.3 dihydrofolate reductases
(DHFR) through a Rhea/reviewed NADPH-dependent 7,8-dihydrofolate -> tetrahydrofolate
reduction reaction plus a dihydrofolate-reductase family/name or active-site handle.
EC / keyword / reaction text are scope-admission only, never predictive; dihydrofolate
synthase / folylpolyglutamate synthetase, methylenetetrahydrofolate reductase, the
bifunctional thymidylate-synthase side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: dihydrofolate_reductase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 118.
- Target mechanism-corroborated bronze labels: 79 (off-target held 19; disambiguation holds 18; skipped 2).
- **Novelty-admitted labels: 74** (throttled/rejected 5; held@cap 0).
- Combined registry 9927 -> **10001** if merged.

## Floor projection

- `dihydrofolate_reductase`: 0 -> 74 (added 74; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'dihydrofolate_reductase': 150}.

## Novelty gate

- Decisions: {'admit': 74, 'throttle': 5}.
- Reasons: {'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 48, 'needed_fingerprint_but_redundant_ortholog': 5}.

## Hold reasons

- {'no_mechanism_corroboration': 18}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
