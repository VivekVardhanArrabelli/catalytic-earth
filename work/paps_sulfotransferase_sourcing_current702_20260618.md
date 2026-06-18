# PAPS-Sulfotransferase Sourcing - broadened evidence handles

Run: 2026-06-18T18:32:28Z

Sources fresh reviewed Swiss-Prot bronze for EC 2.8.2 PAPS-dependent
sulfotransferases through a sulfotransferase family/name plus a Rhea/reviewed
sulfuryl-transfer reaction naming the PAPS donor (3'-phosphoadenylyl sulfate) or
the PAP product (adenosine 3',5'-bisphosphate).
EC / keyword / reaction text are scope-admission only, never predictive;
sulfur-relay sulfurtransferases (rhodanese / cysteine desulfurase, EC 2.8.1),
ATP sulfurylase / adenylyl-sulfate enzymes, PAPS reductase,
side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: paps_sulfotransferase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 237.
- Target mechanism-corroborated bronze labels: 140 (off-target held 0; disambiguation holds 96; skipped 1).
- **Novelty-admitted labels: 130** (throttled/rejected 10; held@cap 0).
- Combined registry 9056 -> **9186** if merged.

## Floor projection

- `paps_sulfotransferase`: 0 -> 130 (added 130; cap 250; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'paps_sulfotransferase': 250}.

## Novelty gate

- Decisions: {'admit': 130, 'throttle': 10}.
- Reasons: {'adds_diversity': 30, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 3, 'redundant_no_novelty_signal': 7}.

## Hold reasons

- {'no_mechanism_corroboration': 96}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
