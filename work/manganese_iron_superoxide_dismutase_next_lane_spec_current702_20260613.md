# Mn/Fe Superoxide Dismutase Next-Lane Spec

Generated: `2026-06-13T15:05:52Z`

Status: **non-importing fingerprint/ontology/source-lane spec; no labels generated and no registry writes.**

Source scout: `artifacts/v3_manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.json`.
Frozen current702 sha256: `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

## Decision

Select `manganese_iron_superoxide_dismutase` as the next clean 10k-path lane, superseding the earlier source-poor Mn/Fe SOD assessment. The earlier scout used a narrow cofactor-comment count; the corrected guarded query finds 252 reviewed rows. In an 80-row sample, 80 were registry-new, 77 had Rhea/reaction + Mn/Fe + family + site evidence, and 0 showed the explicit Cu/Zn/heme/side-EC boundary flags.

## Proposed Fingerprint

- Fingerprint: `manganese_iron_superoxide_dismutase`
- Ontology node: `metal_superoxide_dismutation`
- Universe after wiring: `label_factory_v1_34fp`
- Cap: 250 (not chemistry-confusable under current lane definitions)
- Deploy-missing context: `mn_fe_superoxide_redox_dismutation_context`

## Source Lane

- Lane id: `mn_fe_sod_reviewed_ec_1_15_1_1_guarded`
- Query: `(reviewed:true) AND (ec:1.15.1.1) AND ((cc_cofactor:manganese) OR (cc_cofactor:iron) OR (protein_name:manganese) OR (protein_name:iron) OR (protein_name:Mn) OR (protein_name:Fe)) NOT ((cc_cofactor:copper) OR (cc_cofactor:zinc) OR (protein_name:"Cu-Zn") OR (protein_name:"Cu/Zn") OR (protein_name:copper) OR (protein_name:zinc))`
- Reviewed total: **252**
- Sample registry-new likely-wireable rows: **77 / 80**

## Counted Mechanism Axes

- rhea_reaction_or_participant_pattern: RHEA:20696 / superoxide + H+ -> H2O2 + O2 dismutation text
- cofactor_or_cosubstrate: Mn/Fe metal feature, ligand, cofactor, or reviewed family metal context
- active_site_motif_or_residue_role: active-site, binding-site, or metal-binding feature annotation
- domain_or_family_profile: superoxide dismutase family/name/keyword text

## Required Guards

- hold Cu/Zn SOD and copper/zinc name/cofactor rows
- hold heme/cytoglobin/hemoglobin/peroxidase/nitric oxygen dioxygenase/nitrite reductase rows
- hold superoxide reductase rows; dismutation only
- hold side-EC rows unless future subclass rule explicitly owns them
- hold multi-fingerprint signal rows instead of forcing SOD labels
- EC-only rows are never admitted

## Implementation Checklist

- add mechanism_fingerprints.json fingerprint and mechanism_ontology.json node
- bump CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION to label_factory_v1_34fp
- add DEPLOY_MISSING_CONTEXT and coverage_redundancy signature
- add external_cofactor_ec_disambiguation evidence tokens/rule/synthesized cofactor/trust axes
- add source module + script with non-destructive preview and explicit --apply sha checks
- add offline tests for admission, boundary holds, leakage, trust-tier axes, cap, and no EC-only admission
- re-freeze OOS preregistration for 34fp before live preview/apply
- run non-destructive preview; apply only if novelty/dedup/governor/trust-tier gates pass

Do not admit scout rows directly. EC/name/Rhea/text handles remain excluded-context admission evidence only; EC alone is never a counted corroborator, and future labels must keep `predictive_evidence []`.
