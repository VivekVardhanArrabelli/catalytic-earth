# Mechanism Feature Row-Specific Bond-Change Schema - current702

Run: 2026-06-01T16:56:13Z

No-fit schema and materialization queue for a future row-specific bond-change sidecar. This closes the schema ambiguity left by the fingerprint-template reaction-center sidecar without materializing source evidence or training a model.

## Status

- row_specific_bond_change_schema_staged_no_fit
- Manifest rows: 702
- Reaction-template rows: 702
- Rows requiring row-specific bond-change evidence: 232
- Row status counts: {'not_applicable_no_mechanism_fingerprint_oos_or_unlabeled': 470, 'row_specific_bond_change_evidence_required': 232}

## Schema Contract

- Required top-level fields: entry_id, accession, split_assignment, status, source_evidence, reaction_participant_mapping, bond_change_events, active_site_residue_role_support, guardrails
- Allowed event types: bond_formed, bond_broken, bond_order_changed, proton_transfer, electron_transfer, redox_state_changed, coordination_changed, leaving_group_departure, isomerization_or_rearrangement

## Interpretation

- The expected row-specific bond-change sidecar shape, allowed event vocabulary, forbidden feature keys, and materialization queue are now explicit.
- No source-backed row-specific bond-change events have been materialized; the existing reaction-center template remains fingerprint-level evidence only.
- Materialize this sidecar from frozen source graphs/databases, then audit it before adding it to the no-fit train/cal feature contract.
