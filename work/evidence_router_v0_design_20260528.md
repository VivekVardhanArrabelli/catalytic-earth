# Evidence Router V0 Design - 2026-05-28

This report defines the evidence-router v0 contract for Catalytic Earth. It is an implementation design only. It does not edit labels, registries, ontologies, thresholds, production scoring, imports, or model outputs.

Artifacts produced:

- `artifacts/v3_evidence_router_v0_design_20260528.json`
- `work/evidence_router_v0_design_20260528.md`

## Context Inspected

The design is grounded in the existing Wave 1.1 diagnostic readout, the Foldseek plus geometry diagnostic router pilot, Foldseek readiness notes, geometry retrieval and cofactor policy artifacts, external-source transfer gates, FMO/hard-negative panel work, and learned-representation manifests.

Key findings carried into the contract:

- Wave 1.1 cells are explicitly review-only unless they already belong to frozen countable metrics.
- Foldseek remains useful for dense same-mechanism structural transfer, but it is unsafe in close-structure different-mechanism conflicts.
- Geometry is the strongest existing rescue channel for near-orphan and wrong-Foldseek-transfer slices.
- Cofactor and ligand evidence must distinguish local active-site support from structure-wide or absent support.
- Learned representation tracks are useful as auxiliary row-aligned comparisons, not as a reason to tune thresholds or rerun larger models now.
- External panels remain validation contracts and acquisition worklists until evidence tier, duplicate, sequence, Foldseek, active-site, and review gates are frozen.

## Router Contract

The router consumes frozen channel outputs and emits a result-card-compatible state. It does not compute a new production mechanism score. Each row gets one primary `router_state_id` and zero or more secondary flags.

Primary states:

- `close_same_mechanism_structural_transfer`: close structural neighbor agrees with geometry and cofactor/ligand evidence.
- `close_structure_different_mechanism_conflict`: close structural neighbor crosses a mechanism, OOS, or cofactor-locus boundary; abstain or review.
- `true_near_orphan_active_site_supported`: no reliable close same-mechanism structure, but active-site geometry supports the parent family.
- `no_reliable_structure`: structure/Foldseek/geometry evidence is missing or unsupported; acquisition route.
- `cofactor_ligand_mismatch`: expected local cofactor, ligand, substrate analog, or ligand state is absent, structure-wide only, or incompatible.
- `broad_family_child_unresolved`: parent fingerprint may be supported, but the child mechanism is proposal-only, blocked, underpowered, or not in production.
- `oos_or_hard_negative`: OOS or pre-registered hard-negative/control row; positive routing is a regression.
- `acquisition_needed`: missing evidence can be resolved by structure, sequence, active-site, ligand-state, representation, duplicate-screen, or source acquisition.
- `expert_review_needed`: evidence is decision-relevant but human review or admissibility is required before countable use.

State assignment is deterministic and precedence-based. Prediction-time logic must not use true labels, future expert answers, metric outcomes, or handpicked success/failure membership except as pre-frozen review-only evaluation context.

## Channel Interface

Predictive channels:

- `foldseek_structure`: frozen Foldseek/TM or structural-neighborhood outputs, nearest-neighbor scope, coverage, and conflict status.
- `sequence_similarity`: sequence coverage, identity/similarity, duplicate flags, current-reference overlap, and frozen sequence-NN outputs.
- `geometry_active_site`: residue identities, roles, distances, compactness, pocket descriptors, and predictive counterevidence hits.
- `cofactor_ligand`: expected versus local and structure-wide cofactors, ligand state, evidence level, and mismatch reason.
- `learned_representation`: precomputed row-aligned model outputs and embedding availability only.
- `abstention`: frozen abstain decisions, policy refs, and route-level abstention reason.

Gate-only channel:

- `evidence_tier`: gold/silver/bronze/review-only and external tier A/B/C/D metadata. This gates metrics and review actions; it is not positive mechanism evidence.

Review/source context is physically separate. Names, EC/Rhea identifiers, M-CSA/UniProt source IDs, mechanism prose, citations, expert notes, rationale, proposal-only child labels, and panel row names can explain a card or queue review, but must not add route support, tune thresholds, or create countable labels.

## Evidence And Metrics

Gold and silver labels can be countable evaluation anchors only when they were present before the frozen split and pass duplicate/leakage rules. Bronze labels can remain in existing frozen countable metrics, but they are weak supervision for future work and cannot define new child-label metrics. Review-only rows are excluded from accuracy, threshold calibration, training, and production claims.

External provenance tiers map as follows:

- `tier_A_mcsa_curated`: countable only if already canonical and not marked review-only/control-only.
- `tier_B_external_curated`: future validation-only after active-site, sequence, Foldseek, duplicate, and terminal review gates.
- `tier_C_external_incomplete`: sourcing backlog only.
- `tier_D_control_only`: hard-negative/OOS/duplicate/mismatch control, counted only in pre-registered rejection or abstention metrics.

## Result Card Outputs

Each router card should include:

- `entry_id`
- `router_schema_version`
- `router_state_id`
- `secondary_flags`
- `route_decision`
- `abstained`
- `abstention_reason`
- `candidate_mechanism`
- `input_channels`
- `metric_policy`
- `review_source_context`
- `source_artifacts`

Aggregate result-card sections should include state counts, abstention reasons, unsafe nonabstentions by state, near-orphan rescue counts, close-structure conflict counts, OOS/hard-negative regression counts, cofactor/ligand mismatch counts, acquisition counts, expert-review counts, channel availability, metric inclusion summary, non-claims, and guardrails.

## Evaluation Plan

Wave 1.1 should be evaluated by review-only replay. The router should map the existing diagnostic cells into states and report route/abstention behavior, not new production accuracy:

- Primary v1 after m_csa:497/m_csa:750 read-through: existing summary only.
- Packet 2 near-orphan rescue: expect `true_near_orphan_active_site_supported` where geometry supports the parent family.
- Packet 2 wrong-Foldseek transfer: expect `close_structure_different_mechanism_conflict` and no unsafe positive transfer.
- Packet 3 pilot child strata: expect `broad_family_child_unresolved` or `expert_review_needed`.
- Unresolved and underpowered buckets: abstention-probe only.
- Canary and mixed-chemistry cells: control or review-only behavior only.

External panels should run only after row IDs, sequence controls, duplicate screens, structure selection, Foldseek-neighbor checks, active-site/cofactor extraction, and evidence tiers are frozen. Success is correct routing, safe abstention, or acquisition/expert-review routing. Hard negatives sharing fold, cofactor, metal, O2, PLP, heme, glycan, or names must not become target positives.

## Implementation Plan

1. Define typed interfaces for `RouterInputRow`, channel payloads, state cards, and aggregate cards.
2. Build read-only adapters for Wave 1.1 artifacts, Foldseek readiness, geometry retrieval, cofactor coverage/policy, learned tracks, and external panel manifests.
3. Implement deterministic precedence-based state assignment over normalized channel statuses.
4. Emit per-row review-only router cards and aggregate result-card sections.
5. Add leakage tests proving review/source context cannot enter predictive payloads.
6. Add metric-scope tests proving review-only, proposal-only, external tier C, and blocked child rows cannot become countable through the router.
7. Replay Wave 1.1 and compare state counts and unsafe nonabstentions against the existing model-by-cell report.
8. Prepare external panel replay after missing panel inputs and terminal review decisions are complete.

Explicit non-steps: no label import, no registry edit, no ontology or fingerprint edit, no threshold change, no model training or inference, no production scoring change, and no child-label metric creation.
