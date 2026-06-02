# Fold-Augmented Non-Residue Interaction Sidecar Policy Preflight - current702

Run: 2026-06-02T22:10:40Z

Policy preflight for the Lever 3 P10746/m_csa:204 non-residue interaction blocker. It records why no residue sidecar can be created mechanically and defines the minimum accepted shape for a future interaction sidecar without using mechanism text, labels, source IDs, EC/Rhea IDs, target names, or heldout labels as predictive inputs.

## Status

- fold_augmented_non_residue_interaction_sidecar_policy_preflight_blocked_no_approved_policy
- Policy rows: 1
- Coordinate-available rows: 1
- Source-feature rows: 0
- Graph residue nodes: 0
- Mechanism-text nodes eligible for predictive features: 0
- Approved policy rows: 0
- Sidecars created now: 0
- Copy authorized now: 0
- Deployment blockers cleared now: 0

## Policy Row

| row | accession | coordinate | source features | graph residues | policy defined | ready now | next action |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| m_csa:204 | P10746 | True | 0 | 0 | False | False | Define and approve a non-residue interaction sidecar policy with source-backed interaction evidence, or keep P10746 fold-only. |

## Future Policy Contract

- Required fields: entry_id, accession, interaction_partner_type, interaction_partner_identifier, interaction_type, source_database, source_record_id, source_url, source_record_version_or_date, evidence_code_or_citation, coordinate_anchor_strategy, feature_to_coordinate_mapping, reviewer_decision
- Accepted evidence types: source-backed ligand/substrate/intermediate binding feature, source-backed active-site interaction annotation, approved external structure-derived interaction packet with coordinate mapping
- Forbidden predictive inputs: mechanism_text, EC_ID, Rhea_ID, benchmark_label, source_id, target_name, heldout_label

## Interpretation

- P10746 remains blocked for deployment-valid combined-channel scoring: coordinates exist, but there are 0 source-feature rows and 0 curated residue nodes, and mechanism text is not eligible as a predictive sidecar source.
- Either approve a concrete non-residue interaction sidecar policy matching this contract, source new primary residue or interaction evidence, or keep m_csa:204 fold-only.
