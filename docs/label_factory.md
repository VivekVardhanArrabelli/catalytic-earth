# Label Factory Automation

Catalytic Earth labels are now tiered, review-aware records rather than flat
curation notes. This keeps benchmark growth separate from evidence quality.

## Label Schema

Each label in `data/registries/curated_mechanism_labels.json` has:

- `tier`: `bronze`, `silver`, or `gold`.
- `review_status`: `automation_curated`, `needs_expert_review`,
  `expert_reviewed`, or `rejected`.
- `confidence`: curator confidence, still `high`, `medium`, or `low`.
- `evidence_score`: a bounded numeric score in `[0, 1]`.
- `evidence`: provenance-bearing evidence fields with sources, retrieval score,
  cofactor evidence, conflicts, and review notes.

Current migrated labels start as bronze automation-curated labels. Gold labels
require `expert_reviewed` status and cannot be created by retrieval evidence
alone.

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
risk.

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
- 115 bronze-to-silver promotions are proposed in the applied-label artifact
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
  countable labels beyond the 475-entry source slice. The canonical registry now contains
  679 bronze
  automation-curated labels, while the review-state registry keeps pending
  `needs_expert_review` placeholders separate from the countable benchmark.
- The 1,000 batch is now accepted for its 4 clean countable labels:
  `m_csa:978`, `m_csa:988`, `m_csa:990`, and `m_csa:994`.
  `artifacts/v3_accepted_review_debt_deferral_audit_1000.json` explicitly
  defers all 326 review-state rows, including the 21 new 1,000-preview
  review-debt rows, with 0 countable candidates. The canonical registry now
  has 679 labels and the 1,000 gate passes 21/21.

Current 1,025-preview state:

- `artifacts/v3_label_factory_gate_check_1025_preview.json` passes 21/21
  checks, preserving the label-quality gates.
- `artifacts/v3_label_batch_acceptance_check_1025_preview.json` is not
  accepted for counting because it adds 0 clean labels; the canonical registry
  remains at 679 countable labels.
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
  `artifacts/v3_external_source_review_only_import_safety_audit_1025.json`, and
  `artifacts/v3_external_source_transfer_gate_check_1025.json` scope a
  review-only UniProtKB/Swiss-Prot transfer path. They create 0 countable label
  candidates, route two exact-reference overlaps to holdout controls, pass the
  22/22 external transfer gate for evidence collection, pass the lane-balance
  audit across six query lanes, queue 25 review-only active-site evidence rows,
  defer five rows, sample all 25 ready rows for UniProtKB active-site evidence,
  map 4/4 sampled controls onto AlphaFold structures, and must not be imported
  as labels. The heuristic-control audit records a metal-hydrolase top1
  collapse and scope/top1 mismatch as review-only failure modes rather than
  countable evidence.
  `artifacts/v3_external_source_reaction_evidence_sample_1025.json`
  adds bounded Rhea reaction context for six candidates while keeping every row
  non-countable and outside any reviewed decision artifact; its companion
  guardrail audit is clean and flags three broad/incomplete EC queries as
  review-only context.

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
