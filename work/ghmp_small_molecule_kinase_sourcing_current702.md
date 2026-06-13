# GHMP Small Molecule Kinase Sourcing - broadened evidence handles

Run: 2026-06-13T08:55:51Z

Sources fresh reviewed Swiss-Prot bronze for strict EC 2.7.1 GHMP
small-molecule kinase rows via Rhea ATP/ADP phosphoryl-transfer text, GHMP family
text, and active-site/binding-site annotations. EC, keywords, names, UniProt
prose, and Rhea text are scope-admission only and never predictive.

## Result

- Families sourced: ghmp_small_molecule_kinase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 228 (off-target held 0; disambiguation holds 10; skipped 2).
- **Novelty-admitted labels: 150** (throttled/rejected 0; held@cap 78).
- Combined registry 6285 -> **6435** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ghmp_small_molecule_kinase | atp_mg_ghmp_small_molecule_phosphoryl_transfer_context | 0 | 150 | 150 | 150 | True | 78 |

## Novelty gate

- Decisions: {'admit': 228}.
- Reasons: {'adds_diversity': 128, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 10}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- GHMP handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Protein-kinase/histidine-kinase/hydrolase/ASKHA/NDK/dNK/Pfk boundary guards: True.
- Per-family cap ceiling: {'ghmp_small_molecule_kinase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
