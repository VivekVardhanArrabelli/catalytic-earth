# Redox Oxygen Sulfur Shard Handoff

- Automation ID: `ce-expansion-shard-redox-oxygen-sulfur`
- STARTED_AT_UTC: `2026-06-08T14:11:51Z`
- STARTED_AT_LOCAL: `Mon Jun  8 09:11:51 CDT 2026`
- Artifact created UTC: `2026-06-08T14:23:12Z`
- Wrap validation UTC: `2026-06-08T14:27:14Z`
- Elapsed minutes at validation: `15.383`
- Status: lane artifact/report materialized and validation passed; commit, push,
  sync check, memory update, and lock release are remaining wrap steps.
- Lock: lane-specific linked-worktree gitdir lock `catalytic-earth-redox-oxygen-sulfur-shard.lock`.

## Outputs

- JSON artifact: `artifacts/v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608.json`
- Markdown report: `work/scaleout_redox_oxygen_sulfur_shard_current702_20260608.md`
- Lane handoff: `work/handoff_redox_oxygen_sulfur_shard_20260608.md`

## Result Summary

- Candidate rows: `370`.
- Selected source-row contributions: `989`.
- Terminal state counts: `{'blocked_coordinate': 79, 'blocked_family_decision': 6, 'blocked_locator': 47, 'countable_candidate_preflight_only': 2, 'reject/OOS_preserve_signal': 120, 'review_only_evidence': 116}`.
- Subfamily lane counts: `{'flavin_dehydrogenase_reductase_boundary': 48, 'flavin_fe_s_cofactor_confounded_boundary': 18, 'flavin_monooxygenase_oxygen_transfer_boundary': 20, 'heme_oxygen_peroxide_transfer_boundary': 64, 'iron_sulfur_or_fe_s_electron_transfer_boundary': 100, 'nad_p_dehydrogenase_reductase_specificity_boundary': 4, 'redox_oxygen_sulfur_lipoamide_unresolved_boundary': 111, 'sulfur_lipoamide_transfer_redox_boundary': 2, 'thiol_disulfide_oxidoreductase_isomerase_boundary': 3}`.
- Removed non-candidate control-group rows: `['flavin.dehydrogenase_oxidase_hydride_transfer']`.
- No registry, ontology, import, split, model weight, production threshold, heldout training/tuning, or global doc edit was performed.

## Validation

- `python -m json.tool artifacts/v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608.json`: passed.
- Artifact contract audit: 370 rows, 0 required-field/state/source-hash violations.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records, 8 mechanism fingerprints, 15 ontology families, 702 curated labels.
- `PYTHONPATH=src python -m pytest tests/test_targeted_expansion_factory.py tests/test_targeted_expansion_acquisition_conversion.py -q`: 7 passed.
- `git diff --check`: passed.
- Disk free at validation: 10,956,772 KiB, above the 10 GiB guardrail.

## Next Merger-Lane Action

Review the preflight-only rows, source-free locator blockers, Fe-S/flavin cofactor-confounded rows, and heme/flavin hard-negative controls before integrating any candidate into a registry-edit lane.
