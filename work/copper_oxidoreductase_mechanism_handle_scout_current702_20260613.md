# Copper oxidoreductase mechanism-handle scout

Run: 2026-06-13T02:27:58Z

Non-destructive 80-entry UniProt entry sample for the post-molybdopterin 21fp candidate lane. No registry write, no labels emitted.

- Search rows fetched: 80
- Entry records examined: 80
- Fetch failures: 0

## Mechanism handles in sample

- `active_site_context`: 28 (0.35)
- `amine_oxidase_text`: 29 (0.362)
- `binding_site_context`: 77 (0.963)
- `catalytic_activity_context`: 78 (0.975)
- `cofactor_copper`: 20 (0.25)
- `copper_feature_or_ligand_context`: 31 (0.388)
- `glycosyltransferase_side_ec_signal`: 1 (0.013)
- `heme_boundary_signal`: 2 (0.025)
- `hydrolase_side_ec_signal`: 2 (0.025)
- `keyword_copper`: 80 (1.0)
- `non_oxidoreductase_side_ec_signal`: 2 (0.025)
- `oxygen_reduction_or_oxidase_text`: 78 (0.975)
- `redox_reaction_text`: 77 (0.963)
- `rhea_cross_reference_present`: 78 (0.975)

## Top EC numbers in search rows

- `1.4.3.13`: 24
- `1.4.3.21`: 22
- `1.10.3.2`: 16
- `1.4.3.-`: 6
- `1.10.3.-`: 6
- `1.4.3.22`: 5
- `1.10.3.3`: 3
- `1.10.3.4`: 2
- `1.10.3.1`: 2
- `3.5.-.-`: 2
- `1.3.3.5`: 1
- `1.10.3.15`: 1

## Recommendation

- Wire 21fp lane: True.
- Use EC only as scope; counted corroboration should require copper cofactor/keyword/domain, Rhea redox participant/equation, active-/binding-/metal-site evidence, or structure.
- Guard heme, flavin, molybdopterin, hydrolase, glycosyltransferase, and non-oxidoreductase side rows before any apply.
