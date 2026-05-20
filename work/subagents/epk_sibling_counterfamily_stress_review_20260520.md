# ePK sibling counterfamily stress review

Date: 2026-05-20  
Subagent: C  
Scope: review-only sibling counterfamily stress test for `epk_atp_gamma_phosphoryl_transfer`

## Recommendation

No-go for ePK sibling-control sufficiency as a frozen production policy.

The current artifacts are strong enough to block distance-only ePK thresholding
and to stress the review-only decision surface. They are not strong enough to
activate production scoring because sibling coverage is uneven, the only
passing decision surfaces are still review-only, and substrate identity is not
source-free/frozen enough for a production scorer.

## What is represented today

NDK, PfkB, PfkA, and ATP-grasp are the meaningful current sibling stress
families.

- NDK has four gamma/Mg homolog controls (`1WKL`, `3Q86`, `9OAN`, `9PFY`) with
  mapped catalytic histidine distances of 2.899-3.339 Angstrom. These block
  ePK by phosphohistidine counteraxis, not by hydroxyl-acceptor support.
- PfkB has nine measured family-specific controls. PG-to-family-acid/base
  distances span 3.872-5.596 Angstrom, so all nine collide with the 6 Angstrom
  candidate cutoff.
- PfkA has five measured family-specific controls. PG-to-family-acid/base
  distances span 3.611-5.534 Angstrom, so all five collide with the 6 Angstrom
  candidate cutoff.
- ATP-grasp has two measured family-specific controls. Both collide with the
  6 Angstrom candidate cutoff, but this is thin coverage: useful as a blocker,
  not enough for production sufficiency.

ASKHA, dNK, GHKL, and GHMP are present in the ATP/phosphoryl-transfer ontology
and in review controls, but they are under-covered. dNK has one close selected
control (`2OCP`, 3.232 Angstrom), ASKHA has alternate controls including
`3FGU` at 4.175 Angstrom, GHKL has one alternate measured row, and GHMP has one
selected measured row. That is not a credible family-specific control panel.

## Rule stress

Robust against current review rows:

- The substrate-acceptor counteraxis blocks the 20 measured NDK/PfkA/PfkB/
  ATP-grasp rows, but records its own weak axis: source-supported acceptor
  identity is review context, not a frozen predictive feature.
- The chain/ligand acceptor feature is the best current source-free candidate:
  it hits the three current positives, blocks or non-hits 25 sibling controls,
  and has 0 sibling false hits. It is still not production-admissible because
  chain/ligand generalization, ligand-analog policy, external hard-negative
  re-audit, threshold calibration, and registry/factory extension are all open.
- The unified review-only scorer blocks current controls across all eight
  represented sibling family IDs with 0 current-control false non-abstentions,
  but it remains fail-closed and uncalibrated.

Not robust:

- Distance-only thresholding is falsified. Sibling-family gamma geometry
  overlaps the candidate positive geometry.
- The nearest-gamma-to-oxygen source-free rule false-hits 11 of 20 measured
  NDK/PfkA/PfkB/ATP-grasp sibling controls.
- Relaxed polymer/protein-role rules remain overfit: `7B56` false-hits, and
  same-accession/topology controls (`3Q4Z`, `4I94`, `5XD6`) remain risky.

## Direct answers

1. Sufficiently represented today: NDK, PfkB, PfkA, and thinly ATP-grasp, but
   only for review-only stress and distance-threshold blocking.

2. Under-covered or review-context-only: ASKHA, dNK, GHKL, GHMP, and ATP-grasp
   for production breadth.

3. Current rules block the requested families without source text only for the
   rows present in the review artifacts. The unified and chain/ligand surfaces
   mark sibling rows as text-free and report 0 current sibling false hits. That
   does not yet prove a production-safe source-free policy because the simplest
   text-free oxygen feature fails, and several passing axes are explicitly
   review-only or context-dependent.

4. Minimal controls for a credible frozen policy:
   add 3-5 active-state gamma/Mg controls each for ASKHA, dNK, GHKL, and GHMP;
   expand ATP-grasp beyond two measured rows; repair or replace unresolved
   PfkA/PfkB/ATP-grasp candidates; rerun the frozen rule with source text
   masked; include product/partial nucleotide, split-state, same-chain
   hydroxyl, phosphohistidine, acyl-phosphate, and small-molecule acceptor
   controls; then run a real external hard-negative scored re-audit.

5. Production activation is blocked by both sibling controls and substrate
   identity. It is not only a substrate-identity problem. The current sibling
   surface is enough to reject bad thresholds, but not enough to certify a
   frozen policy across all sibling families.

## Files inspected

- `artifacts/v3_epk_unified_review_only_scoring_prototype_1025.json`
- `artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json`
- `artifacts/v3_epk_precount_gate_status_1025.json`
- `artifacts/v3_epk_negative_control_*_1025.json`
- `artifacts/v3_epk_sibling_*_1025.json`
- `artifacts/v3_epk_family_specific_*_1025.json`
- `artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json`
- `docs/label_factory.md`
- `work/handoff.md`
- `work/atp_phosphoryl_transfer_family_expansion_700_notes.md`
- `tests/test_leakage_closure.py`
- `tests/test_geometry_artifact_regression.py`

No production registries, migration files, or git history were touched.
