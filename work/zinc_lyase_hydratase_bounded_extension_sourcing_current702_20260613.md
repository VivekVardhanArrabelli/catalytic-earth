# Zinc Lyase/Hydratase Sourcing - broadened evidence handles

Run: 2026-06-13T14:38:04Z

Sources fresh reviewed Swiss-Prot bronze for EC 4.2.1 zinc hydro-lyases
via Zn cofactor/site context, Rhea hydration/dehydration/carbonic reaction
evidence, Lyase/hydratase family text, and active-/binding-/metal-site annotations.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
PLP, ThDP, hydrolase/transferase/aldolase/isomerase side rows, non-4.2.1 side ECs,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: zinc_lyase_hydratase.
- Lanes queried: 1 (<= 20 rows each).
- Fetched candidate rows: 20.
- Target mechanism-corroborated bronze labels: 0 (off-target held 0; disambiguation holds 0; skipped 20).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 6940 -> **6940** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| zinc_lyase_hydratase | zinc_water_elimination_addition_context | 113 | 0 | 113 | 150 | True | 0 |

## Novelty gate

- Decisions: {}.
- Reasons: {}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Zinc/hydratase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- PLP/ThDP/hydrolase/transferase/aldolase/isomerase/side-EC boundary guards: True.
- Per-family cap ceiling: {'zinc_lyase_hydratase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
