# ASKHA Sugar Acetate Kinase Sourcing - broadened evidence handles

Run: 2026-06-13T08:42:58Z

Sources fresh reviewed Swiss-Prot bronze for strict EC 2.7.1 ASKHA sugar/
acetate kinase rows via Rhea ATP/ADP phosphoryl-transfer text, ASKHA family
text, and active-site/binding-site annotations. EC, keywords, names, UniProt
prose, and Rhea text are scope-admission only and never predictive.

## Result

- Families sourced: askha_sugar_acetate_kinase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 227 (off-target held 0; disambiguation holds 9; skipped 4).
- **Novelty-admitted labels: 150** (throttled/rejected 7; held@cap 70).
- Combined registry 6135 -> **6285** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| askha_sugar_acetate_kinase | atp_mg_sugar_or_acetate_phosphoryl_transfer_context | 0 | 150 | 150 | 150 | True | 70 |

## Novelty gate

- Decisions: {'admit': 220, 'throttle': 7}.
- Reasons: {'adds_diversity': 120, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 7}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 9}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- ASKHA handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Protein-kinase/histidine-kinase/hydrolase/NDK/dNK/GHMP/Pfk boundary guards: True.
- Per-family cap ceiling: {'askha_sugar_acetate_kinase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
