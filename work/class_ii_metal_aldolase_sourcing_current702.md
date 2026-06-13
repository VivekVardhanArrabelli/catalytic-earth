# Class-II Metal Aldolase Sourcing - broadened evidence handles

Run: 2026-06-13T04:29:40Z

Sources fresh reviewed Swiss-Prot bronze for EC 4.1.2/4.1.3 class-II metal
aldolases via metal cofactor/site context, Lyase/aldolase text, Rhea C-C/oxoacid
reaction evidence, and active-/binding-/metal-site annotations.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
PLP, ThDP, class-I Schiff-base, transferase/hydrolase/oxidoreductase side rows,
non-4.1.2/4.1.3 side-EC rows, and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: class_ii_metal_aldolase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 182 (off-target held 7; disambiguation holds 36; skipped 15).
- **Novelty-admitted labels: 150** (throttled/rejected 7; held@cap 25).
- Combined registry 5488 -> **5638** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| class_ii_metal_aldolase | metal_stabilized_aldol_c_c_bond_context | 0 | 150 | 150 | 150 | True | 25 |

## Novelty gate

- Decisions: {'admit': 175, 'throttle': 7}.
- Reasons: {'adds_diversity': 75, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 7}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 36}.
- Off-target held counts: {'metallophosphomonoesterase': 7}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- class-II aldolase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- PLP/ThDP/Schiff-base/transferase/hydrolase/side-EC boundary guards: True.
- Per-family cap ceiling: {'class_ii_metal_aldolase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
