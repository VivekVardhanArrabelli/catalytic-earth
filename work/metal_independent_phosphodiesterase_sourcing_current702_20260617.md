# Metal-independent Phosphodiesterase Sourcing - broadened evidence handles

Run: 2026-06-17T20:12:01Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.4/4.6.1 metal-independent phosphodiesterases through phosphodiesterase family/name context, hydrolytic phosphodiester/cyclic-nucleotide reaction evidence, and active-/binding-site context where available.
EC / keyword / reaction text are scope-admission only, never predictive; metal-dependent phosphoesterase/nuclease, phosphatase, cyclase/lyase, kinase, transferase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: metal_independent_phosphodiesterase.
- Lanes queried: 8 (<= 250 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 381.
- Target mechanism-corroborated bronze labels: 35 (off-target held 132; disambiguation holds 202; skipped 12).
- **Novelty-admitted labels: 25** (throttled/rejected 10; held@cap 0).
- Combined registry 8817 -> **8842** if merged.

## Floor projection

- `metal_independent_phosphodiesterase`: 100 -> 125 (added 25; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Metal absence counted as evidence: False.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'metal_independent_phosphodiesterase': 150}.

## Novelty gate

- Decisions: {'admit': 25, 'throttle': 10}.
- Reasons: {'adds_diversity': 25, 'redundant_no_novelty_signal': 10}.

## Hold reasons

- {'no_mechanism_corroboration': 202}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
