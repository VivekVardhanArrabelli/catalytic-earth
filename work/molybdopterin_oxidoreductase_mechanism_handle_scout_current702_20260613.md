# Molybdopterin oxidoreductase mechanism-handle scout

Run: 2026-06-13T02:02:09Z

Non-destructive 80-entry UniProt entry sample for the post-isomerase 20fp candidate lane. No registry write, no labels emitted.

- Search rows fetched: 80
- Entry records examined: 80
- Fetch failures: 0

## Mechanism handles in sample

- `active_site_context`: 23 (0.287)
- `binding_site_context`: 78 (0.975)
- `catalytic_activity_context`: 78 (0.975)
- `cofactor_molybdopterin_or_moco`: 80 (1.0)
- `flavin_boundary_signal`: 33 (0.412)
- `heme_boundary_signal`: 13 (0.163)
- `keyword_molybdenum`: 80 (1.0)
- `mo_feature_or_ligand_context`: 65 (0.812)
- `oxo_transfer_reaction_text`: 71 (0.887)
- `peroxidase_boundary_signal`: 26 (0.325)
- `redox_reaction_text`: 49 (0.613)
- `rhea_cross_reference_present`: 78 (0.975)

## Top EC numbers in search rows

- `1.2.3.1`: 11
- `1.17.3.-`: 10
- `1.17.1.4`: 9
- `1.7.-.-`: 6
- `1.17.3.2`: 6
- `1.7.1.1`: 6
- `1.8.5.3`: 5
- `1.8.3.1`: 5
- `1.2.3.7`: 5
- `1.7.2.3`: 4
- `1.9.6.1`: 4
- `1.7.5.1`: 4

## Recommendation

- Wire 20fp lane: True.
- Use EC 1.* only as scope; counted corroboration should require molybdopterin/Mo-cofactor, Mo-pterin feature/keyword/domain, Rhea redox/oxo-transfer participant/equation, or active-/binding-/metal-site evidence.
- Guard heme, flavin, copper, peroxidase, hydrolase, and non-oxidoreductase side-EC boundary rows before any apply.
