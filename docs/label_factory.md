# Label Factory Automation

Catalytic Earth labels are now tiered, review-aware records rather than flat
curation notes. This keeps benchmark growth separate from evidence quality.

## Label Schema

Each label in `data/registries/curated_mechanism_labels.json` has:

- `tier`: `bronze`, `silver`, or `gold`.
- `review_status`: `automation_curated`, `needs_expert_review`,
  `expert_reviewed`, or `rejected`.
- `confidence`: curator confidence, still `high`, `medium`, or `low`.
- `ontology_version_at_decision`: the ontology/fingerprint universe used when
  the label decision was made. Missing historical records migrate to
  `label_factory_v1_8fp`.
- `evidence_score`: a bounded numeric score in `[0, 1]`.
- `evidence`: provenance-bearing evidence fields with sources, retrieval score,
  cofactor evidence, conflicts, and review notes.

Current migrated labels start as bronze automation-curated labels. Gold labels
require `expert_reviewed` status and cannot be created by retrieval evidence
alone. External `out_of_scope` terminal decisions must carry
`ontology_version_at_decision` so future fingerprint expansion cannot
retroactively redefine what the hard-negative decision meant.
External hard-negative labels also separate evidence into
`predictive_evidence`, `import_gate_evidence`, `review_only_context`, and
`excluded_context`. Predictive evidence is limited to the scored local
structure/inverse-gate surface. Import-gate evidence covers duplicate screens,
UniRef/current-reference checks, terminal review, label-factory gates, and
external-transfer gates. Protein names, EC labels, UniProt prose, source
annotations, curated mechanism text, and candidate-specific repair rationale
are review-only or excluded context unless a future rule explicitly permits
them for a non-predictive gate.

The original 10 selected external pilot candidates and their repaired lanes
(`O14756`, `Q6NSJ0`, `P34949`, `Q9BXD5`, `C9JRZ8`, `P06746`, `P55263`,
`O60568`, `O95050`, and `P51580`) are development/review evidence, not clean
held-out performance evidence. A future candidate from a repaired lane can be
used for evaluation only if the rule set, threshold policy, ontology version,
duplicate controls, and structural-neighborhood rules were frozen before
candidate selection.

The next external hard-negative tranche is pre-registered in
`artifacts/v3_external_hard_negative_next_tranche_preregistration_1025.json`.
It freezes the 8-fingerprint universe, `label_factory_v1_8fp`,
threshold-policy version `external_hard_negative_threshold_policy_v1_2026_05_17`,
floor `0.4115`, inverse-gate rule, duplicate rules, structural-neighborhood
rules, admissible source evidence, excluded context, and success/failure
criteria before candidate selection.

## Promotion And Demotion

`build-label-factory-audit` applies deterministic rules against geometry
retrieval evidence, cofactor coverage, pocket context, abstention thresholds,
hard-negative artifacts, and adversarial negative controls.

Bronze labels promote to silver when retrieval agrees with the label, the score
clears the abstention threshold, and no evidence-limiting cofactor or
counterevidence conflict is present.

Silver or gold labels demote to bronze when retrieval counterevidence,
abstention, top-family mismatch, or out-of-scope false non-abstention appears.
Bronze labels with the same conflicts stay bronze and enter review/abstention
handling.

Counterevidence policy is now table-driven rather than a growing branch cascade
inside the geometry scorer. `geometry_retrieval.py` evaluates typed
`CounterevidenceInputs` against a versioned `COUNTEREVIDENCE_POLICY`; retrieval
artifacts keep the existing `counterevidence_reasons` and
`counterevidence_penalty_details` fields, and newer outputs also attach
`counterevidence_policy_version` and `counterevidence_policy_hits`. Policy hits
record rule id, evidence fields, leakage flags, and explicit counterevidence
categories. Structure/local-evidence counterevidence remains predictive safety
evidence, while mechanism-text-derived counterevidence is marked
`review_context_only_not_predictive` and
`review_context_only_not_valid_for_orphan_discovery_claims`. Text can route
curated rows to review or abstention, but it is not positive discovery evidence
and is not a valid orphan/external safety requirement.

Geometry retrieval now carries an explicit text-free scoring policy in artifact
metadata. Mechanism text, entry names, labels, EC/Rhea identifiers, source ids,
and target labels are excluded from positive scoring and kept only as review or
counterevidence context. The prior PLP text-context score boost has been
replaced by a local PLP ligand-anchor feature from proximal PLP/LLP/PMP/P5P
ligand context, and regression tests verify that PLP mechanism text does not
change the score. This removes the text-leakage SPOF without lowering the
accepted 1,000 guardrails: hard negatives, near misses, out-of-scope false
non-abstentions, and actionable in-scope failures remain 0.
`artifacts/v3_mechanism_text_counterevidence_ablation_1000.json` strips
mechanism-text fields from the accepted 1,000 retrieval artifact and reports
the rows whose route or counterevidence changes. The current ablation finds
157 changed rows, 156 review-debt rows, 20 top1 route changes, and 0
structure/local guardrail losses. Rows losing only text-derived guardrails are
review debt and are not valid support for orphan discovery safety claims.

The label-factory gate also has a typed input contract:
`LabelFactoryGateInputs.v1`. The CLI loads required and optional gate artifacts
through a table-driven artifact map before calling `check_label_factory_gates`,
which keeps future gate inputs from becoming another one-off argument cascade.
The same path validates high-fan-in artifact lineage from path and payload
metadata: all non-exempt gate inputs must share a compatible slice id, payload
slice/batch declarations must not contradict the path lineage, and
`artifacts/v3_label_factory_gate_check_1000.json` now records the validated
lineage plus payload methods and short digests under `metadata.artifact_lineage`.
The only current exemption is the historical ATP-family boundary-control
artifact, which remains review/scope context rather than a count-growth input.
The countable batch-acceptance CLI also validates countable/review-state label,
evaluation, hard-negative, in-scope failure, factory-gate, and review-gap
lineage before deciding whether any labels can count.
The scaling-quality audit now uses the same path/payload slice-lineage check
before it classifies promotion risks, so a preview audit cannot silently combine
acceptance, review debt, active-learning, hard-negative, or repair artifacts
from different slices.

Current slice artifact:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-label-factory-audit \
  --retrieval artifacts/v3_geometry_retrieval_725.json \
  --hard-negatives artifacts/v3_hard_negative_controls_725.json \
  --adversarial-negatives artifacts/v3_adversarial_negative_controls_725.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_label_factory_audit_725.json
```

`apply-label-factory-actions` materializes those recommendations into a registry
artifact for review without overwriting the curated registry:

```bash
PYTHONPATH=src python -m catalytic_earth.cli apply-label-factory-actions \
  --label-factory-audit artifacts/v3_label_factory_audit_725.json \
  --out artifacts/v3_label_factory_applied_labels_725.json
```

## Mechanism Ontology

`data/registries/mechanism_ontology.json` maps seed fingerprints and
review-backed family boundaries into mechanism families:

- hydrolysis
- PLP chemistry
- radical rearrangement
- flavin redox
- heme redox
- ATP-dependent phosphoryl transfer, with child family records for ePK, ASKHA,
  ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP

`build-family-propagation-guardrails` audits where family propagation is blocked
across UniRef/CATH/InterPro-style evidence or the current local proxies
available in this repo: M-CSA mechanism text, ligand/cofactor context, and
pocket geometry. Local proxies can prioritize review but cannot promote labels
above bronze without direct evidence. Current guardrails treat
hydrolase-top1 rows with kinase or ATP phosphoryl-transfer text as
`reaction_substrate_mismatch` propagation blockers before any label can count,
retain those blocker rows even when they rank below the normal `max_rows`
cutoff, and record
`atp_phosphoryl_transfer_family_boundary` when a conservative family mapping is
available.

The expert-reviewed ATP/phosphoryl-transfer lane has been expanded into durable
family records for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP.
`artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json` maps 20
expert-supported mismatch lanes across all nine families, retains 4 non-target
expert hints for future ontology work, and keeps every mapped row
non-countable. The family expansion is boundary evidence for routing,
active-learning priority, adversarial negatives, and factory gates; it is not a
new countable seed-fingerprint label source. With this expansion tested,
documented, and gate-clean, the project resumed scaling through the accepted
1000 batch. The accepted-1000 review-debt surface is now explicitly deferred by
`artifacts/v3_accepted_review_debt_deferral_audit_1000.json`.

The first post-infra positive-fingerprint preparation step is review-only:
`artifacts/v3_epk_positive_fingerprint_readiness_packet_1025.json` packages the
five expert-supported ePK/ePK-like boundary rows into a draft fingerprint
evidence packet. It records active-site base, ATP/Mg2+ cofactor,
ATP gamma-phosphoryl-transfer reaction-center, hydroxyl-acceptor, hydrolase
counterevidence, and neighboring ATP-family control requirements. The packet is
`evidence_ready_for_draft_fingerprint_spec=true`, but
`ready_to_expand_positive_fingerprint_universe=false`: it edits neither
`mechanism_fingerprints.json` nor `curated_mechanism_labels.json`, keeps all
rows non-countable, preserves the 8-fingerprint universe, and requires
external-hard-negative re-audit plus future scorer/factory gates before any ePK
counting work.
`artifacts/v3_epk_external_hard_negative_reaudit_plan_1025.json` expands that
blocker into three explicit review-only rows for `uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`. The plan is ready as a checklist, but
`ready_to_run_scored_reaudit=false` because no ePK positive scoring rule,
inverse-gate threshold, or terminal-review rerun has been implemented.
`artifacts/v3_epk_draft_fingerprint_spec_1025.json` is the next review-only
step: it turns the packet into a draft scorer specification without adding the
fingerprint. The spec names the local predictive evidence requirements
(ATP/Mg2+ positioning, ATP gamma-phosphoryl-transfer reaction center,
hydroxyl-acceptor scope, acid/base activation, and sibling ATP-family
counterevidence), excludes text/name/EC/Rhea/UniProt context from predictive
use, and lists the blocked pre-count gates. It remains
`ready_to_expand_positive_fingerprint_universe=false` and edits no registries.
`artifacts/v3_epk_local_evidence_audit_1025.json` profiles those five rows
against current local geometry evidence. It finds three rows ready for a
text-free ATP/metal/acid-base axis prototype, one row with structure-level ATP/Mg
signal that is not local to the active-site axis, and one row with no local
ligand axis. The audit is deliberately not an ePK scorer and keeps
`ready_to_run_epk_scorer=false`.
`artifacts/v3_epk_text_free_local_axis_prototype_1025.json` is the first
review-only axis materialization from that audit. It uses only the three ready
rows, emits binary local adenine-nucleotide, metal-ligand, and catalytic
acid/base axes from geometry evidence, excludes text/name/identifier/prose and
expert-rationale inputs from predictive use, and leaves ePK scoring, threshold
calibration, external hard-negative re-audit, registry edits, and label import
closed.
`artifacts/v3_epk_acceptor_geometry_axis_gap_plan_1025.json` extends the same
review-only scorer-development surface to the acceptor axis. It records
candidate hydroxyl-residue context for the three prototype rows and the
nearby `KAN` acceptor-like ligand context for `m_csa:640`, but keeps acceptor
identity verification, gamma-phosphate-to-acceptor geometry, thresholding, ePK
scoring, external hard-negative re-audit, and countable label gates blocked.
`artifacts/v3_epk_nonready_ligand_repair_plan_1025.json` keeps
`m_csa:282` and `m_csa:662` outside that prototype. It identifies
`m_csa:282` as a structure-level ATP/Mg signal that is not local to the
active-site axis, and `m_csa:662` as selected-structure ligand-axis missing;
both require repair and a rerun of the local-evidence audit before scorer
development can include them.
`artifacts/v3_epk_nonready_ligand_alternate_structure_plan_1025.json` starts
that repair review without changing the prototype: it finds one gamma-capable
alternate for `m_csa:282` and two for `m_csa:662`, but none combine
gamma-capable nucleotide, metal context, and complete catalytic-residue
mapping. The non-ready rows therefore remain excluded.
`artifacts/v3_epk_nonready_ligand_exclusion_decision_1025.json` now records
that exclusion as a terminal review-only calibration decision for the current
ePK lane. `m_csa:282` and `m_csa:662` are kept out of threshold calibration
unless future evidence provides local gamma-capable nucleotide, metal context,
and catalytic-residue mapping. This passes only the non-ready-row
repaired-or-excluded pre-count gate; it does not score ePK, rerun local
evidence, edit registries, or import labels.
`artifacts/v3_epk_acceptor_axis_threshold_design_1025.json` records candidate
acceptor-axis cutoffs of 4, 6, and 8 Angstrom for later validation. The
6-Angstrom candidate covers the current three prototype rows by local
hydroxyl-residue context, but it remains a hypothesis rather than a calibrated
or selected ePK threshold.
`artifacts/v3_epk_gamma_geometry_feasibility_plan_1025.json` then classifies
whether the prototype rows are ready for a future atom-level gamma-phosphate
geometry pass. `m_csa:35` and `m_csa:246` have local ATP/ANP plus acceptor
context, while `m_csa:640` is product-state ADP context and needs ATP-state
evidence before a gamma-phosphate geometry measurement can support scoring.
`artifacts/v3_epk_gamma_geometry_measurement_sample_1025.json` runs the first
review-only atom-level sample for those gamma-capable rows. It measures nearest
PG-to-candidate-hydroxyl distances of 3.610 Angstrom for `m_csa:35` and
5.082 Angstrom for `m_csa:246`, skips `m_csa:640` because only ADP is local,
and still leaves threshold calibration, external re-audit, and score
construction unresolved.
`artifacts/v3_epk_acceptor_identity_review_1025.json` closes the measured-row
acceptor identity review gap without converting it into a score. The two
gamma-measured rows are source-supported review-only acceptor candidates:
`m_csa:35` maps nearest PG to a non-catalytic-chain Ser hydroxyl consistent
with protein substrate hydroxyl context, and `m_csa:246` maps nearest PG to a
non-catalytic-chain Tyr hydroxyl consistent with tyrosine substrate context.
`m_csa:640` remains source-supported but unmeasured because the current
structure is ADP/product-state. Mechanism text remains review context only and
is not a predictive ePK feature.
`artifacts/v3_epk_atp_state_evidence_plan_1025.json` then screens graph-linked
PDB structures for the `m_csa:640` product-state gap. It finds two
gamma-capable ANP/Mg alternate structures (`1J7U` and `3TM0`) that map all
four catalytic sequence-position residues; `3TM0` also has the acceptor-like
aminoglycoside ligand code `B31`, with nearest ANP PG-to-B31 oxygen distance
3.558 Angstrom. It remains review-only because no threshold, score, or external
re-audit is run.
`artifacts/v3_epk_m_csa640_alternate_gamma_geometry_review_1025.json` closes
the review-only geometry review gap for that row. It marks `3TM0` as
alternate-structure review evidence with all catalytic residues mapped,
review-only B31 substrate-OH analog admissibility, and 3.558 Angstrom ANP
PG-to-B31 O14 geometry; it also records that the evidence is not production
scoring-admissible.
`artifacts/v3_epk_gamma_threshold_control_plan_1025.json` then turns the
observed review geometry into threshold/control requirements. It records that
4 Angstrom covers `m_csa:35` plus the alternate `m_csa:640` geometry but misses
`m_csa:246`, while 6 and 8 Angstrom cover all three positive-like review rows.
Those are still only candidate scenarios: no threshold is selected until
negative-control distance distributions, sibling ATP-phosphoryl-transfer
controls, external hard-negative re-audit, non-ready row handling, and
alternate-structure policy are resolved.
`artifacts/v3_epk_negative_control_gamma_distance_distribution_1025.json`
starts the sibling-family negative-control distribution and immediately keeps
threshold selection blocked: dNK `m_csa:615` is a selected-structure non-ePK
control with DTP PG-to-Ser hydroxyl distance 3.232 Angstrom, while GHMP
`m_csa:654` contributes ANP PG-to-Ser hydroxyl distance 6.184 Angstrom. This
is review-only counterevidence against using gamma-distance geometry alone as
an ePK threshold; the distribution is explicitly not ready for calibration.
`artifacts/v3_epk_sibling_negative_control_alternate_structure_plan_1025.json`
opens the next bounded control-coverage step. It screens 38 graph-linked
alternate PDB structures for the 13 unmeasured sibling-family controls, under
an 8-structure-per-entry cap. Three rows (`m_csa:592`, `m_csa:603`, and
`m_csa:696`) now have review-only gamma-plus-metal mapped alternate candidates
for distance measurement.
`artifacts/v3_epk_sibling_negative_control_alternate_gamma_distance_sample_1025.json`
measures those candidates without turning them into calibration evidence:
ASKHA `m_csa:592`/`3FGU` has nearest ANP PG-to-Thr hydroxyl distance
4.175 Angstrom, GHKL `m_csa:603`/`3CRL` has nearest ANP PG-to-Ser hydroxyl
distance 7.910 Angstrom, and ASKHA `m_csa:696`/`1QHA` has nearest ANP
PG-to-Thr hydroxyl distance 9.920 Angstrom. The 6-Angstrom candidate scenario
already hits one sibling control, so the distribution still remains not
calibration-ready.
`artifacts/v3_epk_negative_control_calibration_sufficiency_decision_1025.json`
records the calibration decision explicitly. The combined selected and
alternate control surface has 5 measured entries across 4 sibling families,
leaves ATP-grasp, NDK, PfkA, and PfkB unmeasured, and keeps threshold
selection at `do_not_select_threshold`.
`artifacts/v3_epk_missing_sibling_control_source_request_1025.json` converts
those four missing family lanes into concrete review-only source requests:
ATP-grasp and PfkA need additional gamma-capable source evidence, NDK needs an
ATP-state/gamma-capable alternate, and PfkB needs metal/context or catalytic-
residue mapping repair for an existing gamma-capable alternate. The request
packet is a blocker inventory only; it does not measure distances, calibrate a
threshold, score ePK, edit registries, re-audit external hard negatives, or
import labels.
`artifacts/v3_epk_sibling_control_repair_review_1025.json` begins that repair
work for one missing family, PfkB. It reviews the two PfkB rows from the source
request and confirms that `m_csa:663` has complete catalytic-residue mapping
in gamma-capable `1GQT`/`ACP` but no metal ligand context, while `m_csa:670`
still has no gamma-capable graph-linked alternate. The artifact records 0
measurement-ready repaired structures, keeps the PfkB lane
`blocked_review_only`, and remains outside threshold calibration, ePK scoring,
external re-audit, registry edits, and label import.
The follow-on one-family reviews
`artifacts/v3_epk_sibling_control_repair_review_atp_grasp_1025.json`,
`artifacts/v3_epk_sibling_control_repair_review_ndk_1025.json`, and
`artifacts/v3_epk_sibling_control_repair_review_pfka_1025.json` apply the same
review to ATP-grasp, NDK, and PfkA. The direct graph-linked repair surface has
0 gamma-capable and 0 measurement-ready repaired structures across those three
families: `m_csa:310` has no candidate structures, `m_csa:498` has only
no-target-ligand `8FBZ` context, `m_csa:637` has product/partial `1DEL`
`AMP`/`DGP`/`MG` context, and `m_csa:365` has no-target-ligand `2PFK` context.
Those families still need gamma-capable source evidence before distance
measurement.
`artifacts/v3_epk_missing_sibling_control_post_repair_source_decision_1025.json`
records the resulting source decision: all six missing sibling-control rows
now require external or homolog gamma-capable source evidence because direct
graph-linked repair produced 0 measurement-ready structures. This is only
blocker routing; it does not fetch candidates, measure distances, calibrate a
threshold, score ePK, edit registries, re-audit external hard negatives, or
import labels.
`artifacts/v3_epk_sibling_control_homolog_source_plan_ndk_1025.json` then
starts the first one-family homolog-source pass for NDK. The bounded RCSB
shortlist has four gamma-capable, Mg-supported NDK structures (`1WKL`, `3Q86`,
`9OAN`, and `9PFY`), but catalytic-residue mapping is still pending and
`measurement_ready_homolog_structure_count=0`. The artifact is review-only:
it does not measure distances, select thresholds, score ePK, edit registries,
re-audit external hard negatives, or import labels.
`artifacts/v3_epk_sibling_control_homolog_mapping_review_ndk_1025.json`
removes that mapping blocker for NDK without converting it into calibration
evidence. It maps all four sourced structures to catalytic histidine and local
nucleotide-site residue context, setting
`measurement_ready_homolog_structure_count=4` for a future bounded measurement
pass. It still does not measure calibration distances, select thresholds,
score ePK, edit registries, re-audit external hard negatives, or import
labels.
`artifacts/v3_epk_sibling_control_homolog_gamma_distance_sample_ndk_1025.json`
then measures the mapped NDK homolog controls as a review-only
phosphohistidine counter-axis. All four structures are measured, with nearest
PG-to-mapped-His distances from 2.899 to 3.339 Angstrom, and the artifact
keeps threshold selection blocked because this is not a hydroxyl-acceptor
axis.
`artifacts/v3_epk_sibling_control_homolog_source_plan_pfkb_1025.json`,
`artifacts/v3_epk_sibling_control_homolog_source_plan_pfka_1025.json`, and
`artifacts/v3_epk_sibling_control_homolog_source_plan_atp_grasp_1025.json`
open bounded source-only queues for the remaining missing sibling families.
They find 9 PfkB, 5 PfkA, and 2 ATP-grasp gamma-plus-metal candidates,
respectively.
`artifacts/v3_epk_sibling_control_homolog_mapping_review_pfkb_1025.json`,
`artifacts/v3_epk_sibling_control_homolog_mapping_review_pfka_1025.json`, and
`artifacts/v3_epk_sibling_control_homolog_mapping_review_atp_grasp_1025.json`
then record the first family-specific mapping result for those queues. All
three families fail closed under the current histidine-centric mapper:
PfkB has 4 nucleotide-site mapped candidates but 0 catalytic-histidine mapped
candidates, PfkA has 5 and 0, and ATP-grasp has 0 and 0. The result is useful
counterevidence for the next experiment, but no row is measurement-ready.
`artifacts/v3_epk_family_specific_mapping_template_review_pfkb_1025.json`,
`artifacts/v3_epk_family_specific_mapping_template_review_pfka_1025.json`, and
`artifacts/v3_epk_family_specific_mapping_template_review_atp_grasp_1025.json`
then seed source-family mapping templates for those blockers. They record
35 non-countable residue-role seeds across five M-CSA source entries while
keeping `family_specific_mapping_ready=false` and forbidding exact
residue-position transfer to homolog candidates.
`artifacts/v3_epk_family_specific_homolog_mapping_review_pfkb_1025.json`,
`artifacts/v3_epk_family_specific_homolog_mapping_review_pfka_1025.json`, and
`artifacts/v3_epk_family_specific_homolog_mapping_review_atp_grasp_1025.json`
turn those templates into a first review-only mapper. They map 16/32 homolog
candidates with role-compatible acid/base, phosphate-context, and local-metal
evidence while keeping exact residue-position transfer disabled: 9 PfkB, 5
PfkA, and 2 ATP-grasp candidates are measurement-ready; the rest remain blocked
by unresolved acid/base mapping.
`artifacts/v3_epk_family_specific_homolog_gamma_distance_sample_pfkb_1025.json`,
`artifacts/v3_epk_family_specific_homolog_gamma_distance_sample_pfka_1025.json`,
and
`artifacts/v3_epk_family_specific_homolog_gamma_distance_sample_atp_grasp_1025.json`
then measure those 16 mapped candidates. The nearest PG-to-family-acid/base
distances span 3.611-5.596 Angstrom, so every measured PfkB, PfkA, and
ATP-grasp homolog collides with the 6-Angstrom candidate scenario. This is
review-only sibling-family counterevidence, not a calibrated threshold or
countable ePK score.
`artifacts/v3_epk_review_only_scoring_prototype_1025.json` evaluates a
fail-closed prototype decision surface against current ePK rows, the NDK
homolog counter-axis, the family-specific sibling counter-axis, and the three
imported external hard negatives. After the `m_csa:640` alternate review, it
records three uncalibrated positive-like rows, four NDK phosphohistidine
counter-axis blocks, 16 family-specific sibling-control blocks, and three
imported external hard-negative abstentions. It deliberately keeps
`epk_score_computed=false`,
`threshold_calibrated=false`, and `ready_to_expand_positive_fingerprint_universe=false`.
`artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` makes the
negative result explicit: the current counteraxis evidence is enough to block
distance-only threshold selection because all 16 family-specific sibling
controls hit the 6-Angstrom candidate cutoff and the four NDK homolog controls
remain phosphohistidine-axis blockers. It does not select a threshold, compute
an ePK score, re-audit external hard negatives, edit registries, or import
labels.
`artifacts/v3_epk_substrate_acceptor_counteraxis_prototype_1025.json` adds one
concrete fail-closed rule surface on top of that prototype. The rule marks the
three current ePK rows as positive-like review-only acceptor-axis hits, blocks
all 20 NDK/family-specific ATP-family controls, abstains on the three imported
external hard negatives, and records the weak axis as source-supported
acceptor identity remaining review context rather than text-free production
evidence.
`artifacts/v3_epk_external_hard_negative_counteraxis_review_1025.json` then
pulls those three imported external hard-negative rows into a separate
review-only check: all three abstain under the counteraxis, 0 are
non-abstentions, and clean held-out performance claims remain explicitly
closed until a real calibrated ePK scorer exists.
`artifacts/v3_epk_text_free_acceptor_feature_gap_audit_1025.json` tests the
obvious text-free replacement for the review-context acceptor axis: nearest
gamma-to-oxygen distance within the 6-Angstrom candidate cutoff. It hits all
three current ePK positives but also false-hits 11 of 20 NDK, PfkB, PfkA, and
ATP-grasp sibling controls, so the feature is `blocked_review_only` and cannot
be used for scoring without an additional text-free disambiguation signal.
`artifacts/v3_epk_chain_ligand_acceptor_disambiguation_audit_1025.json` adds
that next review-only disambiguation surface. The chain/ligand feature keeps
3/3 current positives, produces 0 false hits across the 20 current sibling
controls by requiring non-catalytic-chain acceptor context or an acceptor-like
ligand analog, and leaves the three imported external hard negatives as
abstentions. The paired
`artifacts/v3_epk_chain_ligand_external_hard_negative_feature_screen_1025.json`
keeps external hard-negative non-abstentions at 0 while explicitly remaining
not a scored re-audit or held-out performance claim.
`artifacts/v3_epk_protein_substrate_acceptor_candidate_audit_1025.json`
tightens the same feature to protein-substrate non-catalytic-chain acceptor
context only. It keeps `m_csa:35` and `m_csa:246`, blocks all 25 current
negative-control rows with 0 false hits, and abstains on the three imported
external hard negatives, but misses `m_csa:640` because the only current
support for that row is the review-only ligand-analog acceptor context. The
artifact therefore fails closed with
`primary_blocker=protein_substrate_feature_misses_ligand_analog_positive`.
`artifacts/v3_epk_ligand_analog_policy_blocker_decision_1025.json` makes the
policy outcome explicit for that dependency: current ligand-analog acceptor
evidence is not production-admissible, `m_csa:640` cannot rescue the
protein-substrate positive coverage gap, and the next scorer step needs either
another protein-substrate ePK positive or a pre-registered ligand-analog policy
plus scored external re-audit.
`artifacts/v3_epk_protein_substrate_positive_source_triage_1025.json` scopes
the next bounded source experiment from existing active-learning rows. It
excludes the five current readiness-packet entries, emits three non-countable
ePK-family source candidates (`m_csa:756`, `m_csa:757`, and `m_csa:760`), and
recommends `m_csa:760` first because its selected structure has local ADP/Mg
product-state context. None of the three is measurement-ready; all need
active-state gamma geometry and acceptor identity review before scorer work.
`artifacts/v3_epk_m_csa760_atp_state_repair_scan_1025.json` then scans the
known `m_csa:760` alternate structures. It finds ATP/Mg catalytic-residue
contexts in `1TID` and `1TIL`, and protein-substrate/product-state contexts in
`1TH8` and `1THN`, but no single structure with both ATP/Mg and the
protein-substrate acceptor. The row is split-state blocked, has 0
measurement-ready candidates, and stays non-countable.
`artifacts/v3_epk_m_csa757_active_state_repair_scan_1025.json` follows the
source-repair ladder. It scans the first 25 `m_csa:757` alternates and finds
two active-state leads: `1CDK` has ANP/Mn but requires an ambiguous homomeric
chain choice, and `1Q24` has conservative ATP/Mg plus structure-level SEP/TPO
context. Neither maps a protein-substrate acceptor chain, so the artifact has
0 measurement-ready candidates and remains non-countable.
`artifacts/v3_epk_m_csa756_active_state_repair_scan_1025.json` then scans all
15 `m_csa:756` alternates. `5LI1` has structure-level ANP/Mg/SEP/TPO context,
but active-site residue remapping is not conservative; ADP/Mg product-state
leads (`5LIH`, `9EJM`) also lack active-state gamma geometry. The artifact
therefore fails closed with 0 active-state ATP/Mg candidates and 0
measurement-ready candidates.
`artifacts/v3_epk_m_csa756_5li1_residue_evidence_audit_1025.json` then narrows
that clue to `5LI1` only. Chain-A Lys380, Asp382, and Asn383 resolve near
ANP/Mg, and the structure contains phosphoacceptor-like SEP/TPO/PTR context,
but no canonical terminal `PG` atom is available for measurement; a
noncanonical `PB` atom is recorded and explicitly policy-inadmissible. The 5LI1
residue positions are not source-authoritative, and no protein-substrate
acceptor is mapped. The artifact remains review-only and contributes 0
countable label candidates.
`artifacts/v3_epk_protein_substrate_source_repair_terminal_decision_1025.json`
then closes the current bounded source-repair loop. The three current source
candidates (`m_csa:760`, `m_csa:757`, and `m_csa:756`) have 0
measurement-ready candidates in aggregate, so the next useful experiment is
new source acquisition or a pre-registered ligand-analog/product-state policy,
not another repeat scan of the same rows.
`artifacts/v3_epk_protein_substrate_positive_source_triage_expanded_1025.json`
tests the new-source path with a larger review-only triage cap. It still finds
only those same three exhausted source candidates and 0 measurement-ready rows.
The matching expanded terminal decision keeps the branch at
`current_source_candidates_exhausted_review_only`.
`artifacts/v3_epk_analog_product_state_policy_preregistration_1025.json`
creates that policy surface without activating it. The draft blocks
mechanism-text predictive use, homomeric chain-choice substrate mapping, and
product-state ADP-without-gamma evidence, and requires a frozen policy,
sibling-family re-audit, and scored external hard-negative re-audit before any
future scorer use.
`artifacts/v3_epk_analog_product_state_policy_activation_audit_1025.json`
then checks whether that inactive policy can activate against the current
evidence. It remains `blocked_review_only`: the review-only chain/ligand
feature still blocks sibling controls and the imported external hard negatives
have 0 feature non-abstentions, but seven activation requirements fail,
including the ligand-analog dependency on `m_csa:640`, 0 production-admissible
analog rows, 0 measurement-ready source-repair candidates, no calibrated ePK
score, no scored external hard-negative re-audit, and no registry or
label-factory extension.
`artifacts/v3_epk_analog_product_state_policy_control_reaudit_1025.json`
separates the control question from activation. Under an inactive
active-gamma ligand-analog policy variant, 3/3 current positives are feature
hits, 25 sibling controls have 0 false hits, and the three imported external
hard negatives have 0 feature non-abstentions. The artifact remains
`review_only_reaudit_not_activated` because the policy was not frozen before
candidate selection and the external hard negatives were not scored by a real
ePK scorer.
`artifacts/v3_epk_review_only_external_hard_negative_score_probe_1025.json`
records that explicit prototype probe. The three imported external hard
negatives score 0.0 and have no policy-feature hits in review-only mode, but
`external_hard_negative_reaudit_scored` remains false because thresholds are
uncalibrated and the probe is not a real scored re-audit or clean held-out
performance claim.
`artifacts/v3_epk_external_protein_substrate_source_scout_1025.json` starts the
new-source branch after current M-CSA source repair failed closed. The scout
uses reviewed PDB-backed UniProt protein-kinase lanes only as source-triage
context and finds eight non-countable rows with active-site, ATP-binding, and
protein-phosphotransfer evidence. They remain blocked on structure mapping,
protein-substrate acceptor mapping, thresholds, external hard-negative re-audit,
and label-factory extension.
`artifacts/v3_epk_external_source_structure_mapping_review_1025.json` maps the
top sourced rows by direct UniProt residue positions plus struct-ref-seq
alignment. It now resolves nine structures, including five active-state ANP/Mg
mapped structures for `Q8IVT5` (`7JUW`, `7JUX`, `7JUY`, `7JV0`, and `7JV1`),
but no row has source-mapped protein-substrate acceptor evidence. The result
is therefore a review-only lead rather than measurement-ready or countable
evidence.
`artifacts/v3_epk_external_source_acceptor_gap_audit_1025.json` follows that
lead and keeps it fail-closed: three structures have a non-catalytic-chain Ser
hydroxyl within 6 Angstrom of ANP PG and two do not, but none has a
source-mapped protein-substrate acceptor. Measurement readiness remains 0.
`artifacts/v3_epk_external_source_next_experiment_queue_1025.json` converts the
mapping/audit result into a review-only queue: first source-map the three
within-threshold Ser acceptor-like residues, then look for alternate
active-state substrate co-complex evidence for the two outside-threshold rows,
while the remaining mapped or unmapped rows stay blocked and non-countable.
`artifacts/v3_epk_external_source_acceptor_source_mapping_review_1025.json`
executes that first source-mapping item and fails closed. All five active-state
`Q8IVT5` candidates map to MEK1 `P29678` Ser194, while source phosphoserine
evidence is at Ser218/Ser222; therefore the nearby geometry hits are not
source-mapped protein-substrate acceptors.
`artifacts/v3_epk_external_source_q8ivt5_alternate_cocomplex_review_1025.json`
checks the exact P29678/Q02750 phospho-acceptor residues in the same
co-complex surface and still finds 0 within-threshold source acceptors. Two
additional broad UniProt/PDB-backed source passes are captured by
`artifacts/v3_epk_external_source_three_pass_terminal_decision_1025.json`:
24 sourced candidates and 63 reviewed structure rows produce 0
measurement-ready positives, so repeat broad scouting is closed for this lane.
`artifacts/v3_epk_ligand_specific_active_state_source_scout_1025.json` opens
the next route with an RCSB ANP/Mg EC 2.7.11.1 query. It finds 11 review-only
source rows and one active-state mapped lead (`P53355`/`1JKK`), but
`artifacts/v3_epk_ligand_specific_p53355_substrate_cocomplex_review_1025.json`
keeps that lead blocked because active-state kinase structures and mapped
source phospho-acceptor structures are split. The broader
`artifacts/v3_epk_ligand_specific_substrate_cocomplex_query_probe_1025.json`
finds one cross-accession review lead (`5HVK`: source-ready `P53667` with
`P23528` Ser3 near gamma). The follow-on
`artifacts/v3_epk_ligand_specific_5hvk_source_validity_review_1025.json`
accepts the LIMK1/cofilin co-complex as source-valid review evidence and maps
P23528 Ser3 OG 4.236 Angstrom from ANP PG. This makes one review lead
measurement-ready for control reruns only; scoring, import, threshold
selection, registry edits, and held-out claims remain closed.
`artifacts/v3_epk_ligand_specific_5hvk_control_rerun_queue_1025.json`
materializes the exact next review-only queue: add 5HVK to the prototype
surface, rerun the 20 sibling-control rows, and rerun the three imported
external hard negatives as diagnostics, while keeping the real scored re-audit
closed.
`artifacts/v3_epk_ligand_specific_5hvk_prototype_control_rerun_1025.json`
executes that queued diagnostic. It adds source-valid 5HVK to the review-only
prototype surface, keeps all 20 current sibling controls blocked, leaves the
three imported external hard negatives abstained, and still keeps
`epk_score_computed=false`. The follow-on
`artifacts/v3_epk_5hvk_protein_substrate_axis_generalization_audit_1025.json`
records that the protein-substrate-only axis now has three review-only
positive-like rows without relying on ligand-analog-only `m_csa:640`; this
reduces the ligand-analog dependency for scorer development but does not make
the feature production-admissible.
`artifacts/v3_epk_protein_substrate_scorer_design_freeze_1025.json` freezes a
review-only diagnostic design from that axis and explicitly marks
source-authority axes as invalid for orphan-discovery claims. The matching
`artifacts/v3_epk_protein_substrate_calibration_diagnostic_1025.json` computes
only review-only diagnostic scores: three protein-substrate positives score as
full-axis diagnostics, ligand-analog `m_csa:640` is excluded from calibration
positives, and all sibling/imported-external controls remain at zero. Because
that still leaves source authority in the acceptor and catalytic-context axes,
`artifacts/v3_epk_source_authority_axis_replacement_gap_audit_1025.json` keeps
production scoring blocked. The first local replacement attempt,
`artifacts/v3_epk_local_chain_topology_acceptor_replacement_rule_1025.json`,
passes current review controls but still requires source-assigned 5HVK chain
roles, so it remains review-only.
`artifacts/v3_epk_5hvk_local_polymer_entity_role_audit_1025.json` tests that
specific dependency. It confirms local polymer/entity evidence is consistent
with a 5HVK co-complex and disjoint kinase/acceptor chains in ANP/Mg context,
but it cannot assign kinase versus substrate roles without source authority.
`artifacts/v3_epk_source_free_chain_topology_role_audit_1025.json` then makes
the negative control explicit. The source-free masked topology rule sees four
local gamma-to-hydroxyl hits in the ligand-specific co-complex probe, but only
one is the cross-accession 5HVK positive-like lead; the other three are
same-accession phosphosite/control-risk structures (`3Q4Z`, `4I94`, and
`5XD6`). The audit is therefore `blocked_review_only`, keeps source authority
as review context, adds the failing pre-count gate
`source_free_chain_topology_role_audit`, and opens no score, registry edit, or
label import.
`artifacts/v3_epk_heteromeric_chain_topology_signal_audit_1025.json` adds the
first source-free counter-axis on top of that failure. It compares the
candidate acceptor polymer entity to the nearest adenylate gamma atom's
associated author-chain polymer entity. On the current hit controls it keeps
5HVK as the only positive-like heteromeric signal and abstains on `3Q4Z`,
`4I94`, and `5XD6`, with zero same-accession false hits. The gate can pass as
review-only counterevidence, but production remains closed because the signal
has only one positive-like case and still lacks threshold calibration, a real
external hard-negative scored re-audit, and registry/label-factory extensions.
The same artifact also runs a full source-free scan across the 60-structure
probe and finds only 5HVK as a heteromeric candidate, making the positive
coverage gap explicit.
`artifacts/v3_epk_heteromeric_positive_coverage_candidate_scout_1025.json`
then scans the next 50 RCSB ANP/Mg EC 2.7.11.1 entries after that first-60
probe. The source-free topology rule finds six heteromeric candidates:
`6Z3R`, `7M0T`, `7M0W`, `8OXM`, `8OXO`, and `8ZN6`. This removes only the
"no broader candidates checked" gap.
`artifacts/v3_epk_heteromeric_candidate_source_validation_review_1025.json`
then source-reviews those leads and accepts `6Z3R`, `8OXM`, and `8OXO` as
review-only positive-like structures across two unique pairs (`smg1_upf1` and
`atm_p53`). It blocks `7M0T`/`7M0W` as BRAF/MEK role-direction ambiguous and
rejects `8ZN6` as a non-ePK/designed clock-protein context. These accepted
rows are not countable controls because protein-substrate acceptor mapping,
threshold calibration, scored external re-audit, and registry/label-factory
gates remain closed.
`artifacts/v3_epk_heteromeric_source_valid_candidate_gamma_distance_sample_1025.json`
then carries forward the local topology hits for the three source-valid review
leads and records nearest ANP gamma distances from 3.482 to 5.607 Angstrom.
This gives measured review controls for the accepted leads without turning the
axis into a calibrated scorer.
`artifacts/v3_epk_heteromeric_source_valid_control_rerun_1025.json` reruns the
fail-closed review surface with those measured leads. It now carries seven
positive-like review rows (the three current ePK rows, source-valid 5HVK, and
`6Z3R`/`8OXM`/`8OXO`), preserves 20 sibling controls with 0 false hits, keeps
the three imported external hard negatives at 0 non-abstentions, and separates
ambiguous `7M0T`/`7M0W` plus rejected `8ZN6` from the positive-like set.
`artifacts/v3_epk_heteromeric_text_free_axis_gap_audit_1025.json` then
classifies why this is still blocked: all four source-authority-dependent
positive-like rows have local geometry evidence, but none has source-free role
assignment or source-free acceptor identity, so 0 are production-admissible.
`artifacts/v3_epk_heteromeric_source_free_role_rule_probe_1025.json` tests the
obvious local replacement rule, heteromeric topology plus gamma distance, and
fails closed because it hits all six reviewed candidates, including nonaccepted
`7M0T`, `7M0W`, and `8ZN6`.
`artifacts/v3_epk_heteromeric_acceptor_chain_counteraxis_audit_1025.json` adds
a first local counter-axis: block a topology/gamma hit when the candidate
acceptor chain itself carries nucleotide or metal ligand context. On the
current six-row review surface it retains all three source-valid positives,
blocks the three nonaccepted hits, and leaves 0 residual nonaccepted hits, but
remains review-only until broader heteromeric/sibling controls, thresholds, and
external scored re-audits exist.
`artifacts/v3_epk_heteromeric_broader_counteraxis_control_audit_1025.json`
then runs that counter-axis against the full bounded 50-structure heteromeric
scout plus measured NDK, ATP-grasp, PfkA, and PfkB sibling controls. It
retains `6Z3R`, `8OXM`, and `8OXO`, blocks `7M0T`, `7M0W`, and `8ZN6`, and
blocks 11/11 measured sibling same-chain hydroxyl hits with 0 residual sibling
false hits. `artifacts/v3_epk_heteromeric_ligand_asymmetry_role_audit_1025.json`
turns the same evidence into an explicit source-free role-direction probe with
3 retained role hits, 0 nonaccepted role hits, and 0 sibling role false hits.
`artifacts/v3_epk_heteromeric_acceptor_identity_gap_audit_1025.json` records
the remaining blocker: those retained role hits still have only source-context
Ser acceptor identity and 0 source-free acceptor-identity features.
`artifacts/v3_epk_heteromeric_acceptor_identity_rule_probe_1025.json` probes
generic Ser/Thr/Tyr hydroxyl residue class as the weakest source-free identity
axis. It currently hits all three retained role candidates with 0 nonaccepted
or sibling false hits only after the three nonaccepted heteromeric hits and
11 sibling same-chain hydroxyl hits are blocked upstream. It is deliberately
weak and review-only: source-free acceptor-identity ready count remains 0
because residue class is not substrate identity.
`artifacts/v3_epk_heteromeric_peptide_acceptor_identity_probe_1025.json` adds
a narrower non-generic local identity axis: candidate hydroxyls must be on
short peptide-like acceptor polymer chains without local nucleotide/metal
ligand context, while the gamma-associated polymer chain is larger. It hits
all three retained heteromeric role candidates, blocks the three nonaccepted
heteromeric controls, and blocks 11/11 measured sibling same-chain hydroxyl
controls with 0 false hits. The paired
`artifacts/v3_epk_heteromeric_peptide_external_hard_negative_probe_1025.json`
screens the three imported external hard negatives against this feature; all
three abstain with 0 non-abstentions, 0 missing rows, and 0 coordinate gaps.
These artifacts are review-only diagnostics and do not satisfy the scored
external re-audit or label-factory extension gates.
`artifacts/v3_epk_heteromeric_peptide_broader_stress_audit_1025.json` closes
the same-query stress test by confirming that the exact RCSB ANP/Mg EC
2.7.11.1 snapshot has 110 entries and 0 unreviewed rows after the first-60 and
follow-on-50 reviews. It does not unblock scoring: all retained positives are
short peptide-chain contexts and there are 0 non-peptide substrate-chain
positives. Outside that exhausted snapshot, the first 25 novel ATP/Mg, ADP/Mg,
and AGS/Mg hits yield 0 heteromeric topology leads. The 11 novel AMP-PNP/Mg
hits yield `1O6K`/`1O6L`; source validation accepts `1O6K` as
explicit PKB/GSK3 peptide source evidence, accepts `1O6L` through raw CIF
PKB/GSK3 peptide context, measures both at 3.542-3.566 Angstrom, and the rerun
remains fail-closed because the new positive-like pair is source-authority
dependent. A broader "kinase substrate peptide ATP/Mg" first-25 scout finds
`9L3M`/`9L3U`, but source validation blocks both as outer mitochondrial
transmembrane helix translocase contexts rather than ePK substrate evidence.
The 1025 preview/expanded source-triage artifacts repeat the same exhausted
source candidates (`m_csa:760`, `m_csa:757`, and `m_csa:756`) and do not open
a new protein-substrate ePK source lane; the expanded terminal decision stays
closed.
`artifacts/v3_epk_family_specific_mapping_template_validation_review_1025.json`
validates the PfkB, PfkA, and ATP-grasp family templates by downstream mapping
and distance evidence only. It closes the template-review gap for pre-count
bookkeeping but does not make those templates countable label evidence.
`artifacts/v3_epk_precount_gate_status_1025.json` consolidates these artifacts
into a blocked pre-count status. Local-axis prototyping, measured-row acceptor
identity review, gamma-threshold control planning, explicit non-ready-row
exclusion, sibling alternate-control screening, sibling alternate-control
distance measurement, calibration-sufficiency review, NDK homolog sourcing,
NDK homolog mapping, NDK homolog histidine-axis measurement, and
family-specific homolog measurement are now explicit review-only preparation.
The `m_csa:640` alternate geometry review lets the prototype gamma-geometry
gate pass, the family-template gate passes by downstream validation, and the
chain/ligand feature screen, policy activation audit, inactive policy control
re-audit, review-only external hard-negative score probe, 5LI1 clue audit,
5HVK source-validity/control-rerun queue, 5HVK prototype rerun, and 5HVK
protein-substrate generalization reviews pass as diagnostic guard gates. The
heteromeric chain-topology signal gate also passes current hit controls, but
only as one-positive review-only evidence. The broadened heteromeric candidate
scout passes as a source-validation queue, and the source-validation review
passes with three accepted review-only structures across two unique pairs. The
source-valid distance sample also passes with all three accepted leads
measured, the heteromeric control rerun passes as a fail-closed diagnostic
surface, and the text-free gap/probe artifacts make the next blocker explicit:
topology plus gamma distance is not enough without source-free role-direction
and acceptor-identity evidence. The acceptor-chain counter-axis passes only the
current review controls. The broader counter-axis and ligand-asymmetry role
audit now pass broader heteromeric/sibling review controls, and the peptide
acceptor identity plus peptide external hard-negative probes pass as diagnostic
feature gates. The outside-query source-expansion peptide-role audit also
passes for `1O6K`/`1O6L` while blocking the `9L3M`/`9L3U` nonpositive controls.
The substrate-mode gap audit combines those two outside-query peptide hits
with `6Z3R`/`8OXM`/`8OXO` and the three protein-substrate positive-like
controls; both modes pass current controls, and
`artifacts/v3_epk_unified_substrate_identity_rule_probe_1025.json` now tests
one unified review-only rule across those modes. The rule hits eight
positive-like rows (`1O6K`, `1O6L`, `6Z3R`, `8OXM`, `8OXO`, `2PHK`, `1IR3`,
and `5HVK`), blocks current peptide/protein/sibling controls, and keeps the
three imported external hard negatives at 0 feature non-abstentions. It still
excludes ligand-analog-only `m_csa:640` and is not a calibrated scorer. The
new `artifacts/v3_epk_unified_review_only_scoring_prototype_1025.json` scores
that surface only as a diagnostic: eight positive-like rows receive full
review-only signal, `3TM0` remains excluded as ligand-analog-only, 44 current
controls plus 20 legacy sibling counter-axis rows abstain, and all three
imported external hard negatives score as abstentions. The bounded
`artifacts/v3_epk_unified_prototype_broad_stress_audit_1025.json` then records
that exact-query stress is exhausted but outside-query broad sourcing still has
source-validation counterexamples (`9L3M` and `9L3U`). The next broad-stress
tranche is preregistered in
`artifacts/v3_epk_unified_prototype_next_broad_stress_preregistration_1025.json`.
The downstream counteraxis sufficiency decision carries the unified rule,
unified prototype, and broad-stress audit as review-only decision rows but
keeps `do_not_select_threshold` because threshold calibration, a real scored
external re-audit, and registry/factory extension are still closed.
Negative-control distribution readiness,
acceptor-threshold calibration, text-free acceptor
feature production admissibility, real scorer design, `m_csa:760` split-state
repair, `m_csa:757`/`m_csa:756` active-state source
repair, external hard-negative scored re-audit, and registry/label-factory
extension all remain failed gates.

## Active Learning Queue

`build-active-learning-queue` ranks entries by:

- uncertainty
- impact
- novelty
- hard-negative value
- evidence conflict
- family-boundary value
- ATP/phosphoryl-transfer family-boundary value

The queue includes unlabeled tranche candidates plus labeled entries whose
current evidence needs review. After the accepted 1000 batch, the current queue
artifact is `artifacts/v3_active_learning_review_queue_1000.json`: it retains
all 321 expert-label decision rows in addition to labeled review rows and
includes `reaction_substrate_mismatch_value` plus
`atp_phosphoryl_family_boundary_value` ranking terms for kinase or ATP
phosphoryl-transfer text with hydrolase top hits.
The gate fails if a queue limit truncates unlabeled candidates, so label
expansion cannot silently skip lower-ranked unlabeled rows.

## Adversarial Negatives

`build-adversarial-negatives` mines out-of-scope controls beyond simple
threshold misses. It ranks cofactor mimics, close ontology-family boundaries,
counterevidence-heavy rows, mechanistic-coherence mimics, and entries near the
abstention threshold. These controls feed the label-factory audit before new
labels are counted.

## Expert Review

`export-label-review` writes queue rows with a decision scaffold for expert
review. It exports the highest-ranked rows plus all unlabeled queue rows even
when some unlabeled rows rank below the cutoff. `import-label-review` applies
all accepted, rejected, and needs-more-evidence decisions to a review-state
registry copy while preserving existing evidence sources and appending review
provenance. `import-countable-label-review` applies only accepted countable
decisions, preserving the existing baseline labels and leaving pending-review
items out of the benchmark registry.
For reaction/substrate mismatch exports, countable import is stricter:
accepted rows must be explicitly `expert_reviewed` and have a
non-`needs_more_evidence` reaction/substrate resolution before they can enter a
countable registry.
Dedicated expert-label decision exports are stricter still: they are
review-only context artifacts. Countable import refuses accepted decisions from
`expert_label_decision_review_export` artifacts, so those rows cannot become
benchmark labels through automation.

Do not build a countable batch by simply filtering a review-state registry:
that would remove baseline labels temporarily marked `needs_expert_review` for
boundary-control tracking. Use `import-countable-label-review` against the
baseline registry and the decision batch instead. The `filter-countable-labels`
CLI now refuses registries with pending/rejected review records unless
`--allow-pending-review` is passed for an intentional lossy filter.

No-decision imports are safe previews. Accepted gold decisions require expert
review status and a rationale. Automation-curated decisions can be imported as
bronze labels without claiming expert review.

The provisional batch builder intentionally keeps cobalamin-radical candidates
in `needs_expert_review` unless the review context has local ligand-supported
cobalamin evidence. Structure-wide B12 context alone is not enough for a
countable automation-curated label.

`analyze-review-evidence-gaps` audits accepted and deferred review decisions
against retrieval evidence, expected cofactor families, local versus
structure-wide ligand support, score-floor gaps, and counterevidence. This is
used to keep deferrals such as `m_csa:494` auditable without counting
text-only or structure-wide evidence as a benchmark label.

`summarize-review-debt` turns those gap rows into a triage artifact for the
next expert-review pass. It ranks review debt by cofactor evidence gaps,
counterevidence, below-threshold retrieval, family mismatches, and active-queue
rank, then recommends whether to inspect alternate structures, verify local
cofactor/active-site mapping, or route a family-boundary question to expert
review. The accepted-700 artifact is
`artifacts/v3_review_debt_summary_700.json`; preview passes keep their own
triage artifacts such as `artifacts/v3_review_debt_summary_700_preview.json`
until clean labels are promoted. When a baseline debt
artifact is provided, the summary records carried versus new review-debt rows
and full carried/new entry-id lists so preview growth is auditable even when
the prioritized row table is capped.

`analyze-review-debt-remediation` expands review-debt triage into a
structure-aware repair plan without making any label countable. It preserves
every requested debt row, links it to the selected geometry structure, graph
reference proteins, candidate PDB structures, alternate PDB availability,
M-CSA residue-position coverage, cofactor gap reasons, and a concrete repair
bucket. For the accepted 700 state this closes the previous visibility gap
where the summary metadata listed 20 new review-debt ids but the capped row
table only exposed detailed triage for a subset. The focused accepted-700
artifact covers the 20 new rows; `artifacts/v3_review_debt_remediation_700_all.json`
covers all 81 current review-debt rows. The full plan currently records 69
rows where alternate PDBs exist but none of those alternates have M-CSA
residue-position support, so explicit M-CSA alternate-PDB position evidence is
absent for those rows. Downstream scan artifacts now keep explicit positions
separate from conservative selected-structure residue-position remaps.

```bash
PYTHONPATH=src python -m catalytic_earth.cli analyze-review-debt-remediation \
  --review-debt artifacts/v3_review_debt_summary_700.json \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json \
  --graph artifacts/v1_graph_700.json \
  --geometry artifacts/v3_geometry_features_700.json \
  --debt-status new \
  --out artifacts/v3_review_debt_remediation_700.json
```

`scan-review-debt-alternate-structures` performs a bounded structure-wide ligand
scan for remediation rows that need alternate-PDB or local-structure selection
review. When M-CSA residue positions are available for a scanned PDB, it
computes local ligand context around those catalytic residues. If an alternate
PDB lacks explicit M-CSA positions, it can conservatively remap the selected
structure's residue ids and residue codes into the alternate structure, while
recording the remap basis and warnings. The scan is explicitly review evidence
only: expected cofactor-family hits remain non-countable unless later evidence
clears the review gap and the factory gates. The focused accepted-700 scan
covers all 13 structure-scan candidates, scans 152 candidate PDB structures
with 0 fetch failures, remaps 63 alternate-PDB structures, finds
structure-wide expected-family hits for `m_csa:679`, `m_csa:696`, and
`m_csa:698`, and records that all three still lack local active-site support.

The all-debt bounded scan
`artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json`
covers all 46 scan-candidate review-debt rows and all 739 candidate PDB
structures. It remaps 362 alternate-PDB structures, finds review-only local
expected-family hits for `m_csa:577`, `m_csa:592`, and `m_csa:641`, and leaves
7 rows without usable alternate-PDB active-site positions. The companion
`summarize-review-debt-remap-leads` artifact
`artifacts/v3_review_debt_remap_leads_700_all_bounded.json` summarizes 44
review-only leads and keeps `countable_label_candidate_count` at 0.
The follow-up
`artifacts/v3_review_debt_remap_local_lead_audit_700.json` keeps the three
remap-local hits non-countable: `m_csa:577` and `m_csa:641` require expert
family-boundary review, and `m_csa:592` requires expert reaction/substrate
review because glucokinase/ATP phosphoryl-transfer text conflicts with a
hydrolase top hit. `artifacts/v3_review_debt_structure_selection_candidates_700.json`
therefore has 0 current structure-selection candidates after reaction mismatch
triage.

The selected-PDB repair path is now executable rather than only advisory.
`build-selected-pdb-overrides` turns holo-preference swap recommendations into
a provenance-bearing override plan with explicit residue positions. The first
plan, `artifacts/v3_selected_pdb_override_plan_700.json`, marks `m_csa:577`
and `m_csa:641` ready to apply, skips `m_csa:592` because its glucokinase
reaction/substrate mismatch still requires review, and keeps
`countable_label_candidate_count` at 0. The downstream selected-PDB override
geometry/retrieval/evaluation artifacts for the 1,000 context confirm the two
ready rows now use holo alternates `1AWB` and `1J7N` while preserving 0 hard
negatives, 0 near misses, 0 out-of-scope false non-abstentions, and 0
actionable in-scope failures. These artifacts repair selected-structure
evidence only; they are not a label-import path. `build-geometry-features`
now fails fast if a selected-PDB override plan contains ready rows outside the
selected graph slice, residue node ids not present in that graph slice, or a
`current_selected_pdb_id` that no longer matches the selected graph evidence.
That closes the silent selected-PDB artifact mismatch surface before any
override geometry is written.

```bash
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures \
  --remediation artifacts/v3_review_debt_remediation_700.json \
  --max-entries 13 \
  --max-structures-per-entry 60 \
  --out artifacts/v3_review_debt_alternate_structure_scan_700.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures \
  --remediation artifacts/v3_review_debt_remediation_700_all.json \
  --max-entries 46 \
  --max-structures-per-entry 80 \
  --out artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json

PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt-remap-leads \
  --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json \
  --remediation artifacts/v3_review_debt_remediation_700_all.json \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json \
  --out artifacts/v3_review_debt_remap_leads_700_all_bounded.json

PYTHONPATH=src python -m catalytic_earth.cli audit-review-debt-remap-local-leads \
  --remap-leads artifacts/v3_review_debt_remap_leads_700_all_bounded.json \
  --remediation artifacts/v3_review_debt_remediation_700_all.json \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json \
  --out artifacts/v3_review_debt_remap_local_lead_audit_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-selected-pdb-overrides \
  --holo-preference-audit artifacts/v3_structure_selection_holo_preference_audit_700.json \
  --remediation artifacts/v3_review_debt_remediation_700_all.json \
  --entry-ids m_csa:577,m_csa:592,m_csa:641 \
  --skip-entry-ids m_csa:592 \
  --out artifacts/v3_selected_pdb_override_plan_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph_1000.json \
  --max-entries 1000 \
  --reuse-existing artifacts/v3_geometry_features_1000.json \
  --selected-pdb-overrides artifacts/v3_selected_pdb_override_plan_700.json \
  --out artifacts/v3_geometry_features_1000_selected_pdb_override.json

PYTHONPATH=src python -m catalytic_earth.cli audit-reaction-substrate-mismatches \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700.json \
  --out artifacts/v3_reaction_substrate_mismatch_audit_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-reaction-substrate-mismatch-review-export \
  --reaction-substrate-mismatch-audit artifacts/v3_reaction_substrate_mismatch_audit_700.json \
  --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json \
  --labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_reaction_substrate_mismatch_review_export_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch \
  --review artifacts/v3_reaction_substrate_mismatch_review_export_700.json \
  --batch-id 700_reaction_substrate_mismatch_review \
  --reviewer automation_label_factory \
  --out artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700.json \
  --baseline-review-debt artifacts/v3_review_debt_summary_675.json \
  --max-rows 45 \
  --out artifacts/v3_review_debt_summary_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-expert-label-decision-review-export \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700.json \
  --review-debt artifacts/v3_review_debt_summary_700.json \
  --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json \
  --labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_expert_label_decision_review_export_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch \
  --review artifacts/v3_expert_label_decision_review_export_700.json \
  --batch-id 700_expert_label_decision_review \
  --reviewer automation_label_factory \
  --out artifacts/v3_expert_label_decision_decision_batch_700.json

PYTHONPATH=src python -m catalytic_earth.cli summarize-expert-label-decision-repair-candidates \
  --expert-label-decision-review-export artifacts/v3_expert_label_decision_review_export_700.json \
  --review-debt-remediation artifacts/v3_review_debt_remediation_700_all.json \
  --structure-mapping artifacts/v3_structure_mapping_issues_700.json \
  --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json \
  --max-rows 30 \
  --out artifacts/v3_expert_label_decision_repair_candidates_700.json
```

Use `--max-rows 0` with the same inputs to regenerate
`artifacts/v3_expert_label_decision_repair_candidates_700_all.json`, the full
76-row companion table.

Priority expert-decision repair lanes also have a non-countable guardrail audit:

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-expert-label-decision-repair-guardrails \
  --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json \
  --remap-local-lead-audit artifacts/v3_review_debt_remap_local_lead_audit_700.json \
  --out artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json
```

The accepted-700 guardrail audit covers 21 priority repair rows: 14 active-site
mapping/structure-gap rows and 9 text-leakage/nonlocal-evidence risk rows,
with overlap between the two classes. It records 3 local expected-family hits
from conservative remaps (`m_csa:577`, `m_csa:592`, and `m_csa:641`) and keeps
all 3 review-only under strict remap, family-boundary, or reaction/substrate
blockers. It records 0 countable label candidates.

Mechanism-scope pressure and learned-retrieval pathing are tracked separately:

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-mechanism-ontology-gaps \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700.json \
  --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json \
  --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json \
  --max-rows 80 \
  --out artifacts/v3_mechanism_ontology_gap_audit_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-learned-retrieval-manifest \
  --geometry artifacts/v3_geometry_features_700.json \
  --retrieval artifacts/v3_geometry_retrieval_700.json \
  --labels data/registries/curated_mechanism_labels.json \
  --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_700.json \
  --max-rows 160 \
  --out artifacts/v3_learned_retrieval_manifest_700.json

PYTHONPATH=src python -m catalytic_earth.cli audit-sequence-similarity-failure-sets \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_700.json \
  --labels data/registries/curated_mechanism_labels.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700.json \
  --out artifacts/v3_sequence_similarity_failure_sets_700.json
```

These artifacts are review-only. The 700 ontology-gap audit finds 115
non-countable scope-pressure rows, led by transferase/phosphoryl-transfer,
lyase, isomerase, long-tail redox, methyltransferase, and glycan-chemistry
signals. The learned-retrieval manifest defines a future representation-learning
interface with the current geometry retrieval as a required control; it has 562
eligible countable/control rows and computes no embeddings. The sequence
failure-set audit keeps the 2 exact-UniProt duplicate clusters as propagation
controls.

Completed 650 batch workflow:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch \
  --review artifacts/v3_expert_review_export_650.json \
  --batch-id 650_batch \
  --reviewer automation_label_factory \
  --out artifacts/v3_expert_review_decision_batch_650.json

PYTHONPATH=src python -m catalytic_earth.cli import-label-review \
  --review artifacts/v3_expert_review_decision_batch_650.json \
  --labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_imported_labels_batch_650.json

PYTHONPATH=src python -m catalytic_earth.cli import-countable-label-review \
  --review artifacts/v3_expert_review_decision_batch_650.json \
  --labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_countable_labels_batch_650.json
```

## Scaling Gate

Before any new label batch is counted as benchmark labels, run:

```bash
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates \
  --label-factory-audit artifacts/v3_label_factory_audit_650.json \
  --applied-label-factory artifacts/v3_label_factory_applied_labels_650.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_650.json \
  --adversarial-negatives artifacts/v3_adversarial_negative_controls_650.json \
  --expert-review-export artifacts/v3_expert_review_export_650_post_batch.json \
  --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_650.json \
  --out artifacts/v3_label_factory_gate_check_650.json
```

When family guardrails report reaction/substrate mismatch lanes, pass the
dedicated mismatch export as well. The accepted 700 gate uses:

```bash
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates \
  --label-factory-audit artifacts/v3_label_factory_audit_700.json \
  --applied-label-factory artifacts/v3_label_factory_applied_labels_700.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700.json \
  --adversarial-negatives artifacts/v3_adversarial_negative_controls_700.json \
  --expert-review-export artifacts/v3_expert_review_export_700_post_batch.json \
  --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json \
  --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json \
  --expert-label-decision-review-export artifacts/v3_expert_label_decision_review_export_700.json \
  --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700.json \
  --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json \
  --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json \
  --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json \
  --expert-label-decision-local-evidence-repair-resolution artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json \
  --explicit-alternate-residue-position-requests artifacts/v3_explicit_alternate_residue_position_requests_700.json \
  --review-only-import-safety-audit artifacts/v3_review_only_import_safety_audit_700.json \
  --atp-phosphoryl-transfer-family-expansion artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json \
  --out artifacts/v3_label_factory_gate_check_700.json
```

For a decision batch, also verify the countable subset:

```bash
PYTHONPATH=src python -m catalytic_earth.cli check-label-batch-acceptance \
  --baseline-label-count 599 \
  --review-state-labels artifacts/v3_imported_labels_batch_650.json \
  --countable-labels artifacts/v3_countable_labels_batch_650.json \
  --evaluation artifacts/v3_geometry_label_eval_650.json \
  --hard-negatives artifacts/v3_hard_negative_controls_650.json \
  --in-scope-failures artifacts/v3_in_scope_failure_analysis_650.json \
  --label-factory-gate artifacts/v3_label_factory_gate_check_650.json \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_650.json \
  --out artifacts/v3_label_batch_acceptance_check_650.json
```

The baseline count should be the countable registry size before the batch. For
the accepted 650 batch this was `599 -> 618`, recorded in
`artifacts/v3_label_batch_acceptance_check_650.json`. The prior accepted 625
batch was `579 -> 599`. Supplying `--review-evidence-gaps` adds the
counting-boundary guardrail that rejects any newly countable label still
appearing in the review-gap artifact.

For the accepted 700 clean-label pass this was `619 -> 624`, recorded in
`artifacts/v3_label_batch_acceptance_check_700.json`. The 81 review-state rows
remain outside the countable benchmark.

Accepted batches are also aggregated by
`artifacts/v3_label_factory_batch_summary.json`:

```bash
PYTHONPATH=src python -m catalytic_earth.cli summarize-label-factory-batches \
  --acceptance artifacts/v3_label_batch_acceptance_check_500.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_525.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_550.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_575.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_600.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_625.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_650.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_675.json \
  --acceptance artifacts/v3_label_batch_acceptance_check_700.json \
  --gate artifacts/v3_label_factory_gate_check_500.json \
  --gate artifacts/v3_label_factory_gate_check_525.json \
  --gate artifacts/v3_label_factory_gate_check_550.json \
  --gate artifacts/v3_label_factory_gate_check_575.json \
  --gate artifacts/v3_label_factory_gate_check_600.json \
  --gate artifacts/v3_label_factory_gate_check_625.json \
  --gate artifacts/v3_label_factory_gate_check_650.json \
  --gate artifacts/v3_label_factory_gate_check_675.json \
  --gate artifacts/v3_label_factory_gate_check_700.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_500.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_525.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_550.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_575.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_600.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_625.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_650.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_675.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700.json \
  --scaling-quality-audit artifacts/v3_label_scaling_quality_audit_675_preview.json \
  --scaling-quality-audit artifacts/v3_label_scaling_quality_audit_700_preview.json \
  --out artifacts/v3_label_factory_batch_summary.json
```

The summary records accepted-batch counts, review debt, hard-negative status,
factory gate status, and unlabeled queue retention across all accepted batches.
For preview batches, also pass `--scaling-quality-audit`; the summary records
audit readiness, accepted-label review-debt blockers, unclassified new
review-debt rows, omitted underrepresented queue rows, and non-blocking audit
warnings before the batch can be treated as promotion-ready. The current 950
summary also carries whether every family-guardrail reaction/substrate mismatch
lane is present in the dedicated mismatch export.

After the scaling-quality audit below exists, rerun the preview summary with
the audit attached:

```bash
PYTHONPATH=src python -m catalytic_earth.cli summarize-label-factory-batches \
  --acceptance artifacts/v3_label_batch_acceptance_check_675_preview.json \
  --gate artifacts/v3_label_factory_gate_check_675_preview_batch.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_675_preview_batch.json \
  --scaling-quality-audit artifacts/v3_label_scaling_quality_audit_675_preview.json \
  --out artifacts/v3_label_factory_preview_summary_675.json
```

For unpromoted previews, run a promotion-readiness check before copying the
preview countable labels into the canonical registry:

```bash
PYTHONPATH=src python -m catalytic_earth.cli check-label-preview-promotion \
  --preview-acceptance artifacts/v3_label_batch_acceptance_check_675_preview.json \
  --preview-summary artifacts/v3_label_factory_preview_summary_675.json \
  --preview-review-debt artifacts/v3_review_debt_summary_675_preview.json \
  --current-review-debt artifacts/v3_review_debt_summary_650.json \
  --out artifacts/v3_label_preview_promotion_readiness_675.json
```

The readiness check requires the preview summary counts to match the acceptance
artifact and requires explicit unlabeled-candidate queue retention before it can
report `mechanically_ready`.

The scaling-quality audit checks the failure modes required before promotion:
ontology scope pressure, sibling mechanism confusion, family propagation across
boundaries, sequence-family leakage guards, cofactor ambiguity, mixed evidence,
reaction/substrate mismatches, active-site mapping gaps, hard-negative family
concentration, active-learning queue chemistry concentration, and text-leakage
risk. The CLI records `metadata.artifact_lineage` with
`blocker_removed=artifact_graph_consistency_for_label_scaling_quality`, and it
fails fast on non-exempt slice or payload-lineage mismatches before writing an
audit artifact.

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-label-scaling-quality \
  --batch-id 700_preview \
  --acceptance artifacts/v3_label_batch_acceptance_check_700_preview.json \
  --readiness artifacts/v3_label_preview_promotion_readiness_700.json \
  --review-debt artifacts/v3_review_debt_summary_700_preview.json \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_700_preview.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_700_preview_batch.json \
  --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700_preview_batch.json \
  --hard-negatives artifacts/v3_hard_negative_controls_700_preview_batch.json \
  --decision-batch artifacts/v3_expert_review_decision_batch_700_preview.json \
  --structure-mapping artifacts/v3_structure_mapping_issues_700.json \
  --expert-review-export artifacts/v3_expert_review_export_700_preview_post_batch.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_700.json \
  --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700.json \
  --remap-local-lead-audit artifacts/v3_review_debt_remap_local_lead_audit_700.json \
  --reaction-substrate-mismatch-audit artifacts/v3_reaction_substrate_mismatch_audit_700.json \
  --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json \
  --expert-label-decision-review-export artifacts/v3_expert_label_decision_review_export_700.json \
  --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700.json \
  --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json \
  --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json \
  --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json \
  --expert-label-decision-local-evidence-repair-resolution artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json \
  --explicit-alternate-residue-position-requests artifacts/v3_explicit_alternate_residue_position_requests_700.json \
  --review-only-import-safety-audit artifacts/v3_review_only_import_safety_audit_700.json \
  --atp-phosphoryl-transfer-family-expansion artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json \
  --out artifacts/v3_label_scaling_quality_audit_700_preview.json
```

The local sequence-cluster proxy is generated from exact reference UniProt
accession sets:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-cluster-proxy \
  --graph artifacts/v1_graph_700.json \
  --out artifacts/v3_sequence_cluster_proxy_700.json
```

If `--sequence-clusters` is omitted or empty, the audit emits a specific
`sequence_cluster_artifact_missing_for_near_duplicate_audit` warning so the
paralog/near-duplicate check is not silently skipped before larger propagation
batches.

Bulk label expansion should proceed only in batches, and each batch must
regenerate the factory audit, adversarial negatives, active-learning queue,
expert export/import artifacts, family-propagation guardrails, validation, and
tests before its labels are counted.

Current 1,000-queue gate state:

- 21/21 gate checks pass.
- Passing gates: explicit label schema, ontology loaded, promotion
  demonstrated, demotion/abstention demonstrated, applied label actions ready,
  adversarial negatives mined, active queue ranked, expert-review export ready,
  family-propagation guardrails ready, mismatch review export ready,
  expert-label decision review export ready, expert-label decision repair
  candidates ready, expert-label decision repair guardrails ready,
  expert-label local-evidence gap audit ready, expert-label local-evidence
  review export ready, review-only import safety ready, ATP/phosphoryl-transfer
  family expansion ready, accepted-review-debt deferral ready, scaling-quality
  audit attached, and unlabeled queue retention ready.
- 125 bronze-to-silver promotions are proposed in the applied-label artifact
  after the accepted 1,000 batch.
- 433 rows are queued for active-learning review after the accepted 1,000 batch,
  including all 321 expert-label decision rows; 24 queued rows carry the
  reaction/substrate mismatch review signal.
- The 1,000 family-propagation guardrail reports 30
  `reaction_substrate_mismatch` blockers and keeps ATP/phosphoryl-transfer
  boundary rows separate from generic hydrolase or metal-hydrolase labels.
- The dedicated reaction/substrate mismatch export carries all 30 lanes and
  remains review-only. The attached nine-family ontology expansion maps
  expert-supported lanes across ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK, PfkA,
  PfkB, and GHMP with 0 countable label candidates.
- The dedicated expert-label decision export carries all 321 active-queue
  `expert_label_decision_needed` rows as `no_decision`, records 0 countable
  label candidates, and feeds the scaling-quality audit as an
  `expert_label_decision_review_only_debt` failure-mode surface.
- The expert-label repair-candidate and repair-guardrail artifacts cover the
  321 expert-label decision rows and 92 priority repair rows while keeping every
  row non-countable.
- The local-evidence gap audit/export covers those 92 priority lanes, emits 92
  review-only/no-decision items, and records 0 countable candidates.
- `artifacts/v3_accepted_review_debt_deferral_audit_1000.json` explicitly
  defers all 326 accepted-1,000 review-state rows, keeps 0 countable candidates,
  and covers all 21 new 1,000-preview review-debt rows. The accepted-1,000 gate is
  now 21/21 with this deferral artifact attached.
- `artifacts/v3_review_only_import_safety_audit_1000.json` audits the
  reaction/substrate mismatch, expert-label decision, and local-evidence
  decision batches and confirms countable import adds 0 labels from those
  review-only artifacts.
- `artifacts/v3_mechanism_ontology_gap_audit_1000.json` records 223
  non-countable ontology-scope pressure rows. It recommends expert-reviewed
  ontology expansion rather than keyword-only labels.
- `artifacts/v3_learned_retrieval_manifest_1000.json` defines a future learned
  representation interface with 617 eligible rows while preserving the
  heuristic retrieval baseline as the control.
- `artifacts/v3_sequence_similarity_failure_sets_1000.json` keeps the 6
  exact-reference duplicate clusters as sequence-similarity failure controls
  before any propagation or learned split.
- 80 adversarial negative controls are mined, including ATP/phosphoryl-transfer
  family-boundary controls.
- 430 expert-review items are exported from the 1,000 post-batch review queue.
- The 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, and
  850, 875, 900, 925, 950, 975, and 1,000 decision batches accepted 204 new
  countable M-CSA labels beyond the 475-entry source slice. The canonical
  registry now contains 682 bronze automation-curated labels: 679 accepted
  M-CSA labels plus three external out-of-scope hard negatives. The
  review-state registry keeps pending `needs_expert_review` placeholders
  separate from the countable benchmark.
- The 1,000 batch is now accepted for its 4 clean countable labels:
  `m_csa:978`, `m_csa:988`, `m_csa:990`, and `m_csa:994`.
  `artifacts/v3_accepted_review_debt_deferral_audit_1000.json` explicitly
  defers all 326 review-state rows, including the 21 new 1,000-preview
  review-debt rows, with 0 countable candidates. The accepted M-CSA surface has
  679 labels and the 1,000 gate passes 21/21; the canonical registry now has
  682 labels after three external out-of-scope hard-negative imports.

Current 1,025-preview state:

- `artifacts/v3_label_factory_gate_check_1025_preview.json` passes 21/21
  checks, preserving the label-quality gates.
- `artifacts/v3_label_batch_acceptance_check_1025_preview.json` is not
  accepted for M-CSA counting because it adds 0 clean labels; the canonical
  registry remains at 682 countable labels after the three separate external
  hard-negative imports.
- `artifacts/v3_review_debt_summary_1025_preview.json` records 329 review-debt
  rows with 3 new rows: `m_csa:1003`, `m_csa:1004`, and `m_csa:1005`.
  `artifacts/v3_accepted_review_debt_deferral_audit_1025_preview.json` keeps
  all 329 non-countable.
- `artifacts/v3_source_scale_limit_audit_1025.json` records 1,003 observed
  M-CSA source records against a 1,025 requested tranche and recommends stopping
  M-CSA-only count growth.
- `artifacts/v3_external_source_transfer_manifest_1025.json`,
  `artifacts/v3_external_source_query_manifest_1025.json`,
  `artifacts/v3_external_ood_calibration_plan_1025.json`,
  `artifacts/v3_external_source_candidate_sample_1025.json`,
  `artifacts/v3_external_source_candidate_sample_audit_1025.json`,
  `artifacts/v3_external_source_candidate_manifest_1025.json`,
  `artifacts/v3_external_source_candidate_manifest_audit_1025.json`,
  `artifacts/v3_external_source_lane_balance_audit_1025.json`,
  `artifacts/v3_external_source_evidence_plan_1025.json`,
  `artifacts/v3_external_source_evidence_request_export_1025.json`,
  `artifacts/v3_external_source_active_site_evidence_queue_1025.json`,
  `artifacts/v3_external_source_active_site_evidence_sample_1025.json`,
  `artifacts/v3_external_source_heuristic_control_queue_1025.json`,
  `artifacts/v3_external_source_structure_mapping_plan_1025.json`,
  `artifacts/v3_external_source_structure_mapping_sample_1025.json`,
  `artifacts/v3_external_source_heuristic_control_scores_1025.json`,
  `artifacts/v3_external_source_failure_mode_audit_1025.json`,
  `artifacts/v3_external_source_control_repair_plan_1025.json`,
  `artifacts/v3_external_source_representation_control_manifest_1025.json`,
  `artifacts/v3_external_source_representation_control_comparison_1025.json`,
  `artifacts/v3_external_source_binding_context_repair_plan_1025.json`,
  `artifacts/v3_external_source_binding_context_mapping_sample_1025.json`,
  `artifacts/v3_external_source_active_site_gap_source_requests_1025.json`,
  `artifacts/v3_external_source_sequence_holdout_audit_1025.json`,
  `artifacts/v3_external_source_sequence_neighborhood_plan_1025.json`,
  `artifacts/v3_external_source_sequence_neighborhood_sample_1025.json`,
  `artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json`,
  `artifacts/v3_external_source_sequence_alignment_verification_1025.json`,
  `artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json`,
  `artifacts/v3_external_source_sequence_search_export_1025.json`,
  `artifacts/v3_external_source_sequence_search_export_audit_1025.json`,
  `artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json`,
  `artifacts/v3_external_source_import_readiness_audit_1025.json`,
  `artifacts/v3_external_source_active_site_sourcing_queue_1025.json`,
  `artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json`,
  `artifacts/v3_external_source_active_site_sourcing_export_1025.json`,
  `artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json`,
  `artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`,
  `artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json`,
  `artifacts/v3_external_source_representation_backend_plan_1025.json`,
  `artifacts/v3_external_source_representation_backend_plan_audit_1025.json`,
  `artifacts/v3_external_source_representation_backend_sample_1025.json`,
  `artifacts/v3_external_source_representation_backend_sample_audit_1025.json`,
  `artifacts/v3_external_source_transfer_blocker_matrix_1025.json`,
  `artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json`,
  `artifacts/v3_external_source_pilot_candidate_priority_1025.json`,
  `artifacts/v3_external_source_pilot_review_decision_export_1025.json`,
  `artifacts/v3_external_source_pilot_terminal_decisions_1025.json`,
  `artifacts/v3_external_source_pilot_human_expert_review_queue_1025.json`,
  `artifacts/v3_external_structural_cluster_index_1025.json`,
  `artifacts/v3_external_structural_tm_holdout_path_1025_all30.json`,
  `artifacts/v3_external_structural_cluster_index_1025_all30.json`,
  `artifacts/v3_external_structural_tm_diverse_split_plan_1025_all30.json`,
  `artifacts/v3_external_source_review_only_import_safety_audit_1025.json`, and
  `artifacts/v3_external_source_transfer_gate_check_1025.json` scope a
  review-only UniProtKB/Swiss-Prot transfer path. They create 0 countable label
  candidates, route two exact-reference overlaps to holdout controls, pass the
  68/68 external transfer gate for evidence collection under the typed
  `ExternalSourceTransferGateInputs.v1` contract, pass the lane-balance
  audit across six query lanes, queue 25 review-only active-site evidence rows,
  defer five rows, sample all 25 ready rows for UniProtKB active-site evidence,
  resolve 0 explicit active-site residue sources across the 10 gap rows, map
  all 12 heuristic-ready controls onto AlphaFold structures, preserve a
  deterministic k-mer representation baseline, compute a canonical 12-row ESM-2
  representation sample with three representation near-duplicate holdouts and
  12 learned-vs-heuristic disagreements, stage all 10 selected pilot AlphaFold
  coordinate sidecars for review-only Foldseek nearest-neighbor clustering,
  expand that structure cache to all 30 current external candidates with 6
  high-TM pre-split pairs across 26 clusters, complete the all-30 Foldseek
  all-vs-all cache at 435/435 unordered nonself pairs, assign a review-only
  cluster-preserving split with 6 test and 24 train rows at max cross-split
  TM-score `0.6963`, and
  must not be imported as labels.
  The heuristic-control audit records a 9/12
  metal-hydrolase top1 collapse and 9 scope/top1 mismatches as review-only
  failure modes rather than countable evidence. The repair plan creates 25
  non-countable repair rows, the representation manifest exposes 12 mapped
  controls for future learned or structure-language scoring, the feature-proxy
  representation comparison flags 7 metal-hydrolase collapse rows and 2
  glycan-boundary rows, and the binding-context path maps 7/7 active-site-gap
  rows as repair context only. The active-site gap source requests cover all 10
  feature-gap rows, and the sequence-neighborhood plan scopes sequence review
  for the 28 non-holdout external rows. The bounded sequence-neighborhood
  sample fetches all 30 external sequences plus 735 current countable M-CSA
  reference accessions after resolving inactive references. The backend search
  artifact `artifacts/v3_external_source_backend_sequence_search_1025.json`
  uses MMseqs2 18-8cc5c over those 30 external rows against 735 current
  reference accessions / 737 sequence records, preserves exact holdouts
  `O15527` and `P42126`, records 28 no-signal rows, 0 near-duplicate rows, and
  0 failures, and keeps every row review-only, non-countable, and not
  import-ready. This removes the bounded current-reference backend search debt
  for the 28 no-signal rows. The external all-vs-all sequence screen
  `artifacts/v3_external_source_all_vs_all_sequence_search_1025.json` covers
  all 30 current external rows, finds 0 near-duplicate pairs at 90% identity /
  80% coverage, records max reported external-external identity `0.647`, and
  keeps every row review-only. UniRef-wide duplicate screening still blocks
  import. The bounded sequence-alignment verification
  checks 90 top-hit pairs, confirms the two exact-reference holdouts, and keeps
  all rows non-countable. The
  import-readiness audit keeps 0 rows import-ready while summarizing 10
  active-site gaps, 2 exact sequence holdouts, 9 heuristic scope/top1
  mismatches, 29 representation-control issues, and UniRef-wide duplicate-screening
  limitations; the active-site sourcing queue prioritizes the 10 active-site
  gaps into 7 mapped-binding-context rows and 3 primary-source rows. The
  active-site sourcing export carries 72 source targets with 0 completed
  decisions, the active-site sourcing resolution records 0 explicit active-site
  residue sources, the sequence-search export plus backend search keeps all 30
  candidates in no-decision sequence controls, the representation-backend plan
  covers 12 mapped controls without embeddings, the deterministic k-mer
  representation baseline flags one representation near-duplicate holdout, the
  canonical ESM-2 sample flags three representation near-duplicate holdouts and
  12 learned-vs-heuristic disagreements, and the transfer blocker matrix joins
  all 30 external candidates into a review-only next-action worklist:
  7 literature/PDB active-site reviews, 3 primary active-site source tasks,
  9 select/run real representation-backend actions, 6 compute/attach
  representation-control actions, 3 representation-near-duplicate holdouts,
  and 2 sequence holdouts, with no single-action or single-lane collapse. The
  pilot-priority artifact selects 10 non-countable candidates
  across lanes and defers exact-holdout or near-duplicate rows before any
  import attempt. The pilot review-decision export creates no-decision packets
  for those 10 rows with 0 completed decisions and 0 countable candidates, and
  the refreshed pilot packet/dossiers carry backend no-signal status for all
  selected rows without retaining stale complete-near-duplicate sequence
  blockers.
  The pilot terminal-decision artifact now converts the 10 selected rows into
  explicit non-countable terminal statuses: 4 duplicate/near-duplicate
  rejections, 3 active-site-evidence-missing rejections, and 3 human-expert
  deferrals, with 0 import-ready candidates.
  The human/expert queue routes exactly those 3 deferred rows into review-only
  packets with unresolved evidence and expert questions while keeping broader
  duplicate screening and full gates as explicit non-human blockers.
  `artifacts/v3_external_source_reaction_evidence_sample_1025.json`
  adds bounded Rhea reaction context for all 30 candidates while keeping every
  row non-countable and outside any reviewed decision artifact; its companion
  guardrail audit is clean and flags 16 broad-EC context rows as review-only
  context. `artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json`
  finds specific reaction context for all 3 broad-only repair rows while keeping
  them non-countable.

## Automation Lock

The local run lock is also available as code, so future schedulers do not have
to rely only on prompt text:

```bash
PYTHONPATH=src python -m catalytic_earth.cli automation-lock \
  --lock-dir .git/catalytic-earth-automation.lock \
  acquire --started-at "$STARTED_AT"

PYTHONPATH=src python -m catalytic_earth.cli automation-lock \
  --lock-dir .git/catalytic-earth-automation.lock \
  release --require-clean --require-no-merge --require-synced
```

Fresh locks block concurrent runs. Stale locks are replaced only when the git
worktree is clean; a stale lock plus a dirty worktree enters recovery mode
instead of starting unrelated work.
