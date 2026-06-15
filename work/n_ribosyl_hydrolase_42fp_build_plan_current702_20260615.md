# N-ribosyl Hydrolase 42fp Build Plan

Created: 2026-06-15T15:11:00Z

Purpose: turn the top discovery-compass candidate into the next guarded bronze lane without
repeating source-wall design work or applying labels prematurely.

## Current State

- Factory artifact:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_discovery_compass.json`.
- Preregistration artifact:
  `artifacts/v3_n_ribosyl_hydrolase_lane_preregistration_current702_20260615_discovery_compass.json`.
- Source-wall status: implemented preview-only in
  `src/catalytic_earth/external_cofactor_ec_disambiguation.py`.
- Tests:
  `tests/test_external_cofactor_ec_disambiguation.py::test_n_ribosyl_hydrolase_requires_non_ec_mechanism_handles`
  and
  `tests/test_external_cofactor_ec_disambiguation.py::test_n_ribosyl_hydrolase_boundary_controls_hold`.
- Live planning supply: **1991** reviewed non-EC-corroborated rows, projected **150** clean admits
  under the chemistry-confusable cap.

## Required Mechanism Contract

- EC 3.2.2 is scope/fetch context only; it must stay in `excluded_context` and must never count.
- Counted non-EC mechanism evidence:
  - nucleoside hydrolase / N-ribosylhydrolase / N-ribosidase family or name handle;
  - Rhea N-glycosidic bond hydrolysis with ribose/deoxyribose product;
  - active-site acid/base or ribose/base-binding residue evidence where available.
- Holds:
  - O-glycosidase/glycoside hydrolase rows;
  - nucleoside phosphorylase/phosphorolysis rows;
  - nucleoside kinase or nucleotidyltransferase side rows;
  - DNA glycosylase lyase rows unless the rule explicitly proves hydrolytic N-ribosyl cleavage;
  - EC-only rows and multi-fingerprint conflicts.

## Build Steps

1. Add fingerprint `n_ribosyl_hydrolase` in
   `data/registries/mechanism_fingerprints.json` and an ontology node for N-glycosidic bond
   hydrolysis in `data/registries/mechanism_ontology.json`.
2. Bump the current positive universe from `label_factory_v1_41fp` to `label_factory_v1_42fp` in
   `src/catalytic_earth/labels.py`, then add the matching 42fp preregistration constant/path in
   `src/catalytic_earth/transfer_scope.py`.
3. Re-freeze hard-negative OOS preregistration as
   `artifacts/v3_external_hard_negative_next_tranche_preregistration_42fp_1025.json` before any
   candidate selection or apply, and extend the preregistration supersession assertions in
   `tests/test_leakage_closure.py`.
4. Add a reviewed-UniProt source runner using bounded windows and fetch timeouts. Initial lane
   queries should match the factory:
   - `(reviewed:true) AND ((ec:3.2.2.*) OR (protein_name:"nucleoside hydrolase") OR (protein_name:"N-ribosylhydrolase") OR (protein_name:"N-ribosidase"))`
   - the same scope plus non-EC handles:
     `(protein_name:"nucleoside hydrolase") OR (protein_name:"N-ribosylhydrolase") OR (protein_name:"N-ribosidase") OR (keyword:Hydrolase) OR (ft_act_site:*) OR (ft_binding:*)`
5. Run non-destructive preview only; then row guardrail audit, novelty/governor/dedup/cap replay,
   source-contract validation, leakage validation, and full tests.
6. Apply only after the preview gates pass and only through a command that prints frozen current702
   sha256 before and after.

## Minimum Validation Before Any Apply

- `PYTHONPATH=src python -m catalytic_earth.cli validate`
- `PYTHONPATH=src pytest tests/test_external_cofactor_ec_disambiguation.py tests/test_high_yield_family_lane_factory.py tests/test_leakage_closure.py -q`
- source-contract / novelty / coverage / import-apply focused tests after the runner exists
- full `PYTHONPATH=src pytest -q`

## Do Not Do

- Do not apply from the preview-only source wall before the fingerprint/OOS/runner gates exist.
- Do not count EC, keyword, protein name, or source prose as predictive evidence.
- Do not turn annotation-only rows into silver.
- Do not write `data/registries/curated_mechanism_labels.json`.
