# Zinc Lyase/Hydratase Sourcing - broadened evidence handles

Run: 2026-06-13T06:06:19Z

Sources fresh reviewed Swiss-Prot bronze for EC 4.2.1 zinc hydro-lyases
via Zn cofactor/site context, Rhea hydration/dehydration/carbonic reaction
evidence, Lyase/hydratase family text, and active-/binding-/metal-site annotations.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
PLP, ThDP, hydrolase/transferase/aldolase/isomerase side rows, non-4.2.1 side ECs,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: zinc_lyase_hydratase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 116 (off-target held 57; disambiguation holds 10; skipped 57).
- **Novelty-admitted labels: 113** (throttled/rejected 3; held@cap 0).
- Combined registry 5788 -> **5901** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| zinc_lyase_hydratase | zinc_water_elimination_addition_context | 0 | 113 | 113 | 150 | True | 0 |

## Novelty gate

- Decisions: {'admit': 113, 'throttle': 3}.
- Reasons: {'adds_diversity': 13, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 3}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 10}.
- Off-target held counts: {'metallo_amidohydrolase_deaminase': 4, 'metallophosphomonoesterase': 6, 'nad_p_dehydrogenase': 47}.

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
