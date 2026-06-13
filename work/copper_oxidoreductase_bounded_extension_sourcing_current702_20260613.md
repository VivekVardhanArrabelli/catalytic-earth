# Copper Oxidoreductase Sourcing - broadened evidence handles

Run: 2026-06-13T14:38:26Z

Sources fresh reviewed Swiss-Prot bronze for copper-center oxidoreductases
via copper cofactor/site annotation, Copper keyword/domain, Rhea oxygen/redox
participants, or active-/binding-/metal-site context with oxidoreductase EC
scope. EC / keyword / reaction text are scope-admission only, never predictive;
heme, flavin, molybdopterin, hydrolase, glycosyltransferase, non-oxidoreductase,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: copper_oxidoreductase.
- Lanes queried: 2 (<= 20 rows each).
- Fetched candidate rows: 40.
- Target mechanism-corroborated bronze labels: 1 (off-target held 0; disambiguation holds 2; skipped 37).
- **Novelty-admitted labels: 0** (throttled/rejected 1; held@cap 0).
- Combined registry 6940 -> **6940** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| copper_oxidoreductase | copper_redox_metal_center_context | 140 | 0 | 140 | 250 | True | 0 |

## Novelty gate

- Decisions: {'throttle': 1}.
- Reasons: {'redundant_no_novelty_signal': 1}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 2}.
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
