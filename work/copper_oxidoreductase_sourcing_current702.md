# Copper Oxidoreductase Sourcing - broadened evidence handles

Run: 2026-06-13T03:10:52Z

Sources fresh reviewed Swiss-Prot bronze for copper-center oxidoreductases
via copper cofactor/site annotation, Copper keyword/domain, Rhea oxygen/redox
participants, or active-/binding-/metal-site context with oxidoreductase EC
scope. EC / keyword / reaction text are scope-admission only, never predictive;
heme, flavin, molybdopterin, hydrolase, glycosyltransferase, non-oxidoreductase,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: copper_oxidoreductase.
- Lanes queried: 2 (<= 80 rows each).
- Fetched candidate rows: 149.
- Target mechanism-corroborated bronze labels: 140 (off-target held 0; disambiguation holds 7; skipped 2).
- **Novelty-admitted labels: 119** (throttled/rejected 21; held@cap 0).
- Combined registry 5111 -> **5230** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| copper_oxidoreductase | copper_redox_metal_center_context | 0 | 119 | 119 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 119, 'throttle': 21}.
- Reasons: {'adds_diversity': 19, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 12, 'redundant_no_novelty_signal': 9}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 7}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Copper handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Boundary guards: True.
- Per-family cap ceiling: {'copper_oxidoreductase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
