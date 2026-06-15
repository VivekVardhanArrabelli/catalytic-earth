# Metal-independent Phosphodiesterase Sourcing - broadened evidence handles

Run: 2026-06-15T19:05:00Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.4/4.6.1 metal-independent phosphodiesterases through phosphodiesterase family/name context, hydrolytic phosphodiester/cyclic-nucleotide reaction evidence, and active-/binding-site context where available.
EC / keyword / reaction text are scope-admission only, never predictive; metal-dependent phosphoesterase/nuclease, phosphatase, cyclase/lyase, kinase, transferase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: metal_independent_phosphodiesterase.
- Lanes queried: 4 (<= 80 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 130.
- Target mechanism-corroborated bronze labels: 0 (off-target held 5; disambiguation holds 121; skipped 4).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 8272 -> **8272** if merged.

## Floor projection

- `metal_independent_phosphodiesterase`: 0 -> 0 (added 0; cap 150; floor reached: False; held@cap 0).

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

- {'no_mechanism_corroboration': 116, 'multi_fingerprint_signal_conflict': 5}.

## Next action

- Do not apply unless a later aggregate reaches >=150 clean admits; add only handles with mechanism-corroborated yield to the reusable runner.
