# Fold-Augmented Lever 3 Finalization Stop Readiness - current702

Run: 2026-06-05T15:03:53Z

Final Lever 3 stop/readiness report. This turns Lever 3 into a reusable
deployment-safety gate and records the final P07658 fixed-threshold scoring
closure status. It does not add counteraxes, stage coordinates, score rows, or
change threshold `0.44155`.

## Status

- `fold_augmented_lever3_finalization_stop_condition_reached_p07658_fail_closed`
- Safe abstain/route operator contract is reproducible and current: true
- Current hard-confounded rows are safely routed, not force-labeled: true
- P07658 fully accepted/scored: false
- P07658 fail-closed with exact missing evidence: true
- Reusable family-expansion gate documented: true
- Stop current-family Lever 3 optimization now: true

## Current Operator Contract

Use
`artifacts/v3_fold_augmented_lever3_deployment_operator_transfer_safety_application_reproducibility_audit_current702_20260605.json`
as the current operator-facing Lever 3 safety artifact.

- 21/21 hard residual operator rows are safe to `abstain_or_route_novel_oos`.
- 0 rows allow mechanism transfer.
- 0 rows allow scoring or forced mechanism labeling.
- 0 unsafe actions, forced labels, threshold changes, or rule-selection rows.
- 31/34 calibration in-scope rows are retained.
- 167/204 train/cal OOS rows abstain or route.
- Retained residual rows after all current counteraxes: 0.

The current route classes are current-family evidence only:
cofactor/same-family confound, fold-similarity confound, pocket-geometry
confound, protein-descriptor counteraxis, and pocket-chemistry confound. They
are not universal family rules.

## Reusable Gate

Reusable parts:

- Use predicted-structure/source-free evidence only.
- Select counteraxes on train/calibration evidence only.
- Do not tune on heldout or application rows.
- Do not use mechanism text, labels, EC/Rhea IDs, source IDs, target names, or
  experimental-PDB metadata as predictive features.
- Fail closed for unsafe lookalikes by abstaining or routing novel/OOS.
- Require source hashes, coordinate/provenance records, and normalized rebuild
  audits before operator use.
- Permit mechanism transfer only after family-specific evidence passes the
  provenance, reproducibility, calibration, confounder, and leakage gates.

Family-specific parts:

- The current current702 counteraxes and route-class counts are not reusable as
  universal rules.
- Current hard-confounded row behavior supports safe routing, not forced
  mechanism labels.
- P07658 is a current fixed-threshold scoring closure blocker, not a general
  family-expansion blocker.

New-family gate:

1. Freeze the family panel, split, source boundaries, and allowed source-free
   feature set.
2. Materialize exact predicted-coordinate and provenance sidecars with sequence
   hashes and nonstandard residue handling.
3. Select family counteraxes on train/cal only.
4. Verify calibration retention and OOS abstain/route behavior without heldout
   tuning.
5. Apply to application rows only as retain versus
   `abstain_or_route_novel_oos`.
6. Run provenance, source-hash, and reproducibility audits.
7. Allow mechanism transfer only if all family-specific gates pass.

## P07658 Closure Status

P07658 remains fail-closed as `abstain_or_route_novel_oos`.

Frozen input:

- Entry: `m_csa:562`
- Accession: `P07658`
- Frozen FASTA:
  `work/fold_augmented_p07658_full_length_prediction_input_current702_20260604.fasta`
- Sequence length: 715
- Sequence SHA-256:
  `3090cc03d7d9a4015e6607c7008d258d99b15b4dfec5db660eadfea94b8fe9fa`
- Selenocysteine: U140 preserved

Current closure check:

- No exact P07658 coordinate file is present at the preferred staging path.
- No repo P07658 `.cif`, `.mmcif`, `.bcif`, `.pdb`, or `.pdbx` coordinate
  candidate is present.
- No filled coordinate provenance file is present.
- No HF, NVIDIA, BioLM, or equivalent provider credential is present in the
  current environment.
- No local `esm`, `openfold`, `colabfold`, `alphafold`, ESMFold, ColabFold, or
  AlphaFold runtime is available.
- No provider calls or equivalent no-credential retries were performed in this
  finalization run.

The fixed-threshold scoring closure is blocked only by the exact
coordinate/provenance requirement:

- Exact full-length P07658 predicted coordinate for the frozen 715-aa sequence.
- Filled provider/model/version/path/checksum provenance.
- Input sequence hash match and explicit U140 handling.
- Passing P07658 acceptance preflight before any scoring rerun.

## Stop Condition

Lever 3 stop condition is reached.

Do not continue current-family Lever 3 optimization or open-ended counteraxis
hunting. Resume Lever 3 only if one of these arrives:

- A new frozen family panel that must pass through this reusable gate.
- An exact full-length P07658 coordinate plus filled provenance that passes the
  acceptance preflight.

Until then, keep fixed-threshold scoring closure fail-closed and use the
current reproducible operator contract only for safe abstain/route decisions.

## Guardrails

- Lever 3 only.
- No blocker packet created.
- No labels, registries, ontologies, imports, heldout splits, production
  thresholds, threshold values, row scores, coordinates, provider calls, or
  source decisions changed.
- No heldout rows used for training, threshold tuning, or rule selection.
- No mechanism text, labels, EC/Rhea IDs, source IDs, target names, or
  experimental-PDB metadata used as predictive features.
