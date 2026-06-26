# Acid--CoA-Ligase Sourcing - broadened evidence handles

Run: 2026-06-26T20:33:02Z

Sources fresh reviewed Swiss-Prot bronze for EC 6.2.1 acid--CoA ligases /
acyl-CoA synthetases (the ANL superfamily) through a CoA-ligase /
acyl-CoA-synthetase family/name plus a Rhea/reviewed reaction forming an
acyl-CoA thioester with ATP (acid + ATP + CoA -> acyl-CoA + AMP + diphosphate).
EC / keyword / reaction text are scope-admission only, never predictive;
CoA transferases, biotin carboxylases, thiolases, acyl-CoA dehydrogenases,
side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: acid_coa_ligase.
- Lanes queried: 3 (<= 200 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 261.
- Target mechanism-corroborated bronze labels: 169 (off-target held 1; disambiguation holds 90; skipped 1).
- **Novelty-admitted labels: 150** (throttled/rejected 19; held@cap 0).
- Combined registry 9477 -> **9627** if merged.

## Floor projection

- `acid_coa_ligase`: 0 -> 150 (added 150; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'acid_coa_ligase': 150}.

## Novelty gate

- Decisions: {'admit': 150, 'throttle': 19}.
- Reasons: {'adds_diversity': 50, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 3, 'redundant_no_novelty_signal': 16}.

## Hold reasons

- {'no_mechanism_corroboration': 90}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
