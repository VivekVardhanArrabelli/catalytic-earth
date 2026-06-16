# Metal-independent Phosphodiesterase Sourcing - broadened evidence handles

Run: 2026-06-16T01:23:45Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.4/4.6.1 metal-independent phosphodiesterases through phosphodiesterase family/name context, hydrolytic phosphodiester/cyclic-nucleotide reaction evidence, and active-/binding-site context where available.
EC / keyword / reaction text are scope-admission only, never predictive; metal-dependent phosphoesterase/nuclease, phosphatase, cyclase/lyase, kinase, transferase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: metal_independent_phosphodiesterase.
- Lanes queried: 1 (<= 120 rows each).
- Per-lane record window: offset 0, limit 120.
- Fetched candidate rows: 120.
- Target mechanism-corroborated bronze labels: 17 (off-target held 22; disambiguation holds 69; skipped 12).
- **Novelty-admitted labels: 17** (throttled/rejected 0; held@cap 0).
- Combined registry 8628 -> **8645** if merged.

## Floor projection

- `metal_independent_phosphodiesterase`: 0 -> 17 (added 17; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Metal absence counted as evidence: False.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'metal_independent_phosphodiesterase': 150}.

## Novelty gate

- Decisions: {'admit': 17}.
- Reasons: {'closes_hole_fingerprint': 17}.

## Hold reasons

- {'no_mechanism_corroboration': 69}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
