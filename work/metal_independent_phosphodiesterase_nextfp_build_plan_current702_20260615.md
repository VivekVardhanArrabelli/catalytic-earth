# Metal-independent Phosphodiesterase Next-fingerprint Build Plan

Created: 2026-06-15T15:13:00Z

Purpose: preserve the second discovery-compass lane as a ready follow-on after
`n_ribosyl_hydrolase`, without confusing the preview-only source wall for registry authority.

## Current State

- Factory artifact:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_discovery_compass.json`.
- Preregistration artifact:
  `artifacts/v3_metal_independent_phosphodiesterase_lane_preregistration_current702_20260615_discovery_compass.json`.
- Source-wall status: implemented preview-only in
  `src/catalytic_earth/external_cofactor_ec_disambiguation.py`.
- Tests:
  `tests/test_external_cofactor_ec_disambiguation.py::test_metal_independent_phosphodiesterase_requires_non_ec_mechanism_handles`
  and
  `tests/test_external_cofactor_ec_disambiguation.py::test_metal_independent_phosphodiesterase_boundary_controls_hold`.
- Live planning supply: **1129** reviewed non-EC-corroborated rows, projected **150** clean admits
  under the chemistry-confusable cap.

## Required Mechanism Contract

- EC 3.1.4 / 4.6.1 are scope/fetch context only; they must stay in `excluded_context` and must
  never count.
- Counted non-EC mechanism evidence:
  - phosphodiesterase or cyclic-nucleotide phosphodiesterase family/name handle;
  - Rhea hydrolytic phosphodiester or cyclic-nucleotide P-O cleavage reaction;
  - active-site acid/base or substrate-binding residue evidence where available.
- Holds:
  - catalytic-metal phosphodiesterase/nuclease rows;
  - phosphomonoesterase and protein phosphatase rows;
  - phospholipase C or cyclase/lyase rows without hydrolytic phosphodiester cleavage;
  - kinase or transferase side rows;
  - EC-only rows and multi-fingerprint conflicts.
- Metal presence is a boundary/filter, not evidence. Do not count metal absence as a
  corroborator.

## Build Steps

1. Add fingerprint `metal_independent_phosphodiesterase` in
   `data/registries/mechanism_fingerprints.json` and an ontology node for metal-independent
   hydrolytic phosphodiester/cyclic-nucleotide P-O cleavage in
   `data/registries/mechanism_ontology.json`.
2. If this is still the next new family after N-ribosyl, bump the positive universe from the
   then-current value to the next `label_factory_v1_<N>fp` in
   `src/catalytic_earth/labels.py`, add the matching preregistration constant/path in
   `src/catalytic_earth/transfer_scope.py`, refresh OOS preregistration before candidate
   selection, and extend the supersession assertions in `tests/test_leakage_closure.py`.
3. Add a reviewed-UniProt source runner using bounded windows and fetch timeouts. Initial lane
   queries should match the factory:
   - `(reviewed:true) AND ((ec:3.1.4.*) OR (ec:4.6.1.*))`
   - the same scope plus non-EC handles and metal filters:
     `(protein_name:phosphodiesterase) OR (protein_name:phospholipase) OR (keyword:Hydrolase) OR (ft_act_site:*) OR (ft_binding:*)`
     and not magnesium/manganese/zinc/metal/Metal-binding source handles.
4. Run non-destructive preview only; then row guardrail audit, novelty/governor/dedup/cap replay,
   source-contract validation, leakage validation, and full tests.
5. Apply only after the preview gates pass and only through a command that prints frozen current702
   sha256 before and after.

## Minimum Validation Before Any Apply

- `PYTHONPATH=src python -m catalytic_earth.cli validate`
- `PYTHONPATH=src pytest tests/test_external_cofactor_ec_disambiguation.py tests/test_high_yield_family_lane_factory.py tests/test_leakage_closure.py -q`
- source-contract / novelty / coverage / import-apply focused tests after the runner exists
- full `PYTHONPATH=src pytest -q`

## Do Not Do

- Do not apply from the preview-only source wall before fingerprint/OOS/runner gates exist.
- Do not count EC, keyword, protein name, source prose, or metal absence as predictive evidence.
- Do not merge metal-dependent phosphodiesterases into this lane.
- Do not write `data/registries/curated_mechanism_labels.json`.
