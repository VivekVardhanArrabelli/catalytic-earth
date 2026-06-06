# Fold-Augmented Q43088 Source-Free Locator Approval Contract - current702

Run: 2026-06-04T08:48:47Z

Review-only Lever 3 contract for clearing m_csa:604/Q43088's source-free geometry locator blocker. Q43088 already has a local predicted coordinate and fold channel, but only one active-site residue; this contract approves no locator, sidecar, score, import, or threshold change.

## Status

- fold_augmented_q43088_source_free_locator_approval_contract_ready_for_review
- Affected row: m_csa:604 / Q43088
- Local predicted coordinate available: True
- Active-site residues: 1
- Additional locator positions needed: 2
- Remaining coordinate-source blockers: 4
- Blockers: ['q43088_two_additional_source_free_locator_positions_not_approved', 'q43088_geometry_sidecar_not_approved', 'fixed_threshold_audit_not_ready_to_rerun']

## Locator Contract

- Each new locator position must come from source-free predicted-structure or residue-level evidence, not mechanism text, EC/Rhea IDs, labels, source IDs, or target names.
- Approved positions must map unambiguously onto the local Q43088 predicted coordinate frame before any geometry rescore.
- An approved geometry sidecar may satisfy the contract only if it records source-free provenance and the exact residue/coordinate locus used by the fold/geometry channel.
- The contract cannot change labels, registries, ontologies, imports, production thresholds, heldout splits, or threshold 0.44155.
- Q43088 cannot trigger a full fixed-threshold audit rerun alone; the four alternate predicted-structure source rows must also clear.

## Pass/Fail

- Pass condition: Q43088 has at least 3 approved source-free locator positions or an equivalent approved geometry sidecar, and is ready for row-level fold/geometry rescore at unchanged threshold 0.44155.
- Fail conditions: Fewer than two additional source-free locator positions are approved and no equivalent geometry sidecar is approved; Any locator uses mechanism text, EC/Rhea IDs, labels, source IDs, or target names as predictive evidence; Any locator cannot be mapped onto the local Q43088 predicted coordinate frame; Any threshold, split, label, registry, ontology, import, or production artifact is changed under this contract.

## Decision

- Q43088 ready for rescore now: False
- Surface completeness ready after contract alone: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Next gate: Approve two additional source-free Q43088 locator positions or an equivalent geometry sidecar. Then rescore only Q43088 after the four coordinate-source blockers have approved predicted structures; do not retune threshold 0.44155.

## Interpretation

- Q43088 is not blocked on coordinates; it is blocked on the minimum source-free geometry locus needed for the combined fold/geometry channel.
- Review or create a Q43088 locator approval packet for two additional source-free positions, or an equivalent approved geometry sidecar, before any rescore.
