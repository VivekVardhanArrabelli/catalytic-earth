# Metal-independent Phosphodiesterase Sourcing - broadened evidence handles

Run: 2026-06-17T01:51:09Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.4/4.6.1 metal-independent phosphodiesterases through phosphodiesterase family/name context, hydrolytic phosphodiester/cyclic-nucleotide reaction evidence, and active-/binding-site context where available.
EC / keyword / reaction text are scope-admission only, never predictive; metal-dependent phosphoesterase/nuclease, phosphatase, cyclase/lyase, kinase, transferase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: metal_independent_phosphodiesterase.
- Lanes queried: 4 (<= 260 rows each).
- Per-lane record window: offset 0, limit 80.
- Fetched candidate rows: 315.
- Target mechanism-corroborated bronze labels: 0 (off-target held 66; disambiguation holds 171; skipped 78).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 8728 -> **8728** if merged.

## Floor projection

- `metal_independent_phosphodiesterase`: 100 -> 100 (added 0; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Metal absence counted as evidence: False.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'metal_independent_phosphodiesterase': 150}.

## Novelty gate

- Decisions: {}.
- Reasons: {}.

## Hold reasons

- {'no_mechanism_corroboration': 94, 'trust_tier_corroboration_insufficient': 77}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
