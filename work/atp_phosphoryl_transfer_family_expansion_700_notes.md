# ATP/Phosphoryl-Transfer Family Expansion 700 Notes

This run implemented the expert-reviewed ATP/phosphoryl-transfer family
expansion surfaced by the 700 reaction/substrate mismatch lane.

## Family Coverage

`data/registries/mechanism_ontology.json` now includes an
`atp_phosphoryl_transfer` parent family plus these nine child families:

- ePK (`epk`)
- ASKHA (`askha`)
- ATP-grasp (`atp_grasp`)
- GHKL (`ghkl`)
- dNK (`dnk`)
- NDK (`ndk`)
- PfkA (`pfka`)
- PfkB (`pfkb`)
- GHMP (`ghmp`)

Each child record has a parent relationship, sibling list, scope note, and
family-boundary guardrails. The records are ontology/family-boundary evidence;
they are not new countable seed fingerprints.

## Artifacts

`artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json` maps
20 expert-supported reaction/substrate mismatch lanes to the nine families:

- ePK: 5 rows
- ASKHA: 4 rows
- ATP-grasp: 2 rows
- GHKL: 2 rows
- dNK: 2 rows
- NDK: 1 row
- PfkA: 1 row
- PfkB: 2 rows
- GHMP: 1 row

The same artifact records 4 non-target expert hints for future ontology work
and keeps every row non-countable. Metadata: `boundary_guardrail_ready=true`,
`unmapped_required_family_ids=[]`, `unsupported_mapping_count=0`, and
`countable_label_candidate_count=0`.

The regenerated 700 queue/guardrail artifacts now carry family-boundary fields:

- `artifacts/v3_active_learning_review_queue_700.json`: 15 ATP-family boundary
  rows and an `atp_phosphoryl_family_boundary_value` ranking term.
- `artifacts/v3_family_propagation_guardrails_700.json`: 20 ATP-family boundary
  rows and a dedicated `atp_phosphoryl_transfer_family_boundary` blocker.
- `artifacts/v3_adversarial_negative_controls_700.json`: 8 ATP-family
  boundary controls.
- `artifacts/v3_reaction_substrate_mismatch_review_export_700.json`: 20
  mapped family-boundary lanes while preserving 0 countable label candidates.

`artifacts/v3_label_factory_gate_check_700.json` now passes 21/21 gates with
the ATP-family expansion attached. The scaling-quality audit includes the
family expansion as a failure-mode surface and remains `review_before_promoting`
because review-only debt is still present even though the expansion gate is
clean.

## Remaining-Time Plan

After the expansion artifact and gate passed before the 50-minute boundary, the
remaining productive time was used to add command/test coverage, refresh the
700 artifacts, update docs, and prepare the next run to resume bounded
factory-gated scaling instead of opening blind count growth.
