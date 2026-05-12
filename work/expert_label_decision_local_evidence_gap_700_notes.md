# 700 Expert-Decision Local Evidence Gap Notes

This note summarizes the non-countable local-evidence gap audit for the
accepted 700 state. It is a repair guide only; it does not make any label
countable.

## Operational Confidence Call

Label-quality gates remain good enough for repair and discovery-path work, but
not for count growth. Evidence: `artifacts/v3_label_factory_gate_check_700.json`
passes 20/20 gates after adding the local-evidence gap audit/export, repair
resolution, alternate residue-position sourcing requests, and review-only
import-safety audit;
hard negatives, near misses, out-of-scope false non-abstentions, actionable
in-scope failures, accepted labels with review debt, expert-decision countable
candidates, repair guardrail countable candidates, local-evidence gap countable
candidates, local-evidence review export countable candidates, and review-only
import new countable labels are all 0.
The blocker remains the 81 review-state decisions and 21 priority
expert-decision repair lanes.

## New Local-Evidence Gap Audit

Artifact:

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-expert-label-decision-local-evidence-gaps \
  --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json \
  --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json \
  --out artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json
```

Current summary:

- 21 priority lanes audited; 0 missing priority rows; 0 countable candidates.
- 14 lanes have selected-structure residue support shortfall.
- 17 lanes have alternate structures lacking explicit residue positions.
- 12 lanes were scanned without local expected-family hits.
- 4 lanes have structure-wide or nonlocal expected-family evidence only.
- 4 lanes have a single selected structure and no alternate-PDB context.
- 3 conservative-remap local evidence leads remain review-only.

## Review Export And Repair Plan

Artifacts:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-expert-label-decision-local-evidence-review-export \
  --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json \
  --labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_expert_label_decision_local_evidence_review_export_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch \
  --review artifacts/v3_expert_label_decision_local_evidence_review_export_700.json \
  --batch-id 700_expert_label_decision_local_evidence_review \
  --reviewer automation_label_factory \
  --out artifacts/v3_expert_label_decision_local_evidence_decision_batch_700.json

PYTHONPATH=src python -m catalytic_earth.cli summarize-expert-label-decision-local-evidence-repair-plan \
  --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json \
  --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json \
  --out artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json
```

The export carries all 21 priority lanes as review-only `no_decision` items,
and countable import refuses accepted decisions from this export type. The
repair plan is ready and sorts the lanes into:

- 4 reaction/substrate expert-review lanes.
- 3 explicit alternate-structure residue-position sourcing lanes.
- 3 active-site mapping or structure-selection inspection lanes.
- 11 family-boundary expert-review lanes.

## Repair-Lane Resolution And Sourcing Requests

Artifacts:

```bash
PYTHONPATH=src python -m catalytic_earth.cli resolve-expert-label-decision-local-evidence-repair-lanes \
  --expert-label-decision-local-evidence-repair-plan artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json \
  --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json \
  --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json \
  --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json \
  --reaction-substrate-mismatch-decision-batch artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json \
  --out artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json

PYTHONPATH=src python -m catalytic_earth.cli build-explicit-alternate-residue-position-requests \
  --expert-label-decision-local-evidence-repair-plan artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json \
  --review-debt-remediation artifacts/v3_review_debt_remediation_700_all.json \
  --graph artifacts/v1_graph_700.json \
  --out artifacts/v3_explicit_alternate_residue_position_requests_700.json

PYTHONPATH=src python -m catalytic_earth.cli audit-review-only-import-safety \
  --labels data/registries/curated_mechanism_labels.json \
  --review artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json \
  --review artifacts/v3_expert_label_decision_decision_batch_700.json \
  --review artifacts/v3_expert_label_decision_local_evidence_decision_batch_700.json \
  --out artifacts/v3_review_only_import_safety_audit_700.json
```

Current summary:

- 4 reaction/substrate local-evidence repair lanes are closed as reviewed
  out-of-scope repair-only rows: `m_csa:592`, `m_csa:643`, `m_csa:654`, and
  `m_csa:662`.
- 17 local-evidence repair lanes remain open, including the 3 explicit
  alternate-residue-position sourcing lanes and 11 family-boundary lanes.
- 3 explicit alternate residue-position requests are ready for `m_csa:567`,
  `m_csa:578`, and `m_csa:667`, covering 34 alternate PDB structures.
- The review-only import-safety audit covers 3 decision artifacts and confirms
  0 new countable labels.

The top prioritized repair rows are:

| Entry | Repair lane | Selected PDB | Selected residues | Alternate PDBs | Explicit alternate positions |
| --- | --- | --- | ---: | ---: | ---: |
| `m_csa:592` | reaction/substrate expert review | `3IDH` | 2 | 34 | 0 |
| `m_csa:643` | reaction/substrate expert review | `1G99` | 5 | 2 | 0 |
| `m_csa:654` | reaction/substrate expert review | `1OJ4` | 2 | 0 | 0 |
| `m_csa:662` | reaction/substrate expert review | `1BO1` | 2 | 25 | 0 |
| `m_csa:567` | explicit alternate residue positions | `1GAL` | 1 | 5 | 0 |
| `m_csa:578` | explicit alternate residue positions | `1HRK` | 9 | 24 | 0 |
| `m_csa:667` | explicit alternate residue positions | `1PZ3` | 2 | 5 | 0 |

## Highest-Value Repair Subset

The immediate bounded subset is the four single-structure/no-alternate-context
lanes. These cannot be fixed by another bounded alternate-PDB scan because the
current graph exposes only one candidate PDB structure for each row.

| Entry | Selected PDB | Current blocker profile | Next repair path |
| --- | --- | --- | --- |
| `m_csa:654` | `1OJ4` | kinase/reaction-substrate mismatch; 2 residues; no expected metal evidence | keep in reaction/substrate expert review before any local-evidence repair |
| `m_csa:659` | `1K82` | heme counterevidence; 2 residues; metal context only | route to family-boundary review or source external cofactor evidence |
| `m_csa:692` | `1DL5` | flavin/NAD counterevidence; 1 residue; local SAM context | treat as ontology/family mismatch pressure, not a flavin countable candidate |
| `m_csa:701` | `1EU1` | heme counterevidence; 2 residues; molybdopterin/metal context | route to family-boundary review or external cofactor-source review |

None of these rows should enter the countable registry without explicit local
mechanistic evidence plus external review resolution and a passing factory gate.
