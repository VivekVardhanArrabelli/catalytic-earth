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
  --retrieval artifacts/v3_geometry_retrieval_650.json \
  --hard-negatives artifacts/v3_hard_negative_controls_650.json \
  --adversarial-negatives artifacts/v3_adversarial_negative_controls_650.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_label_factory_audit_650.json
```

`apply-label-factory-actions` materializes those recommendations into a registry
artifact for review without overwriting the curated registry:

```bash
PYTHONPATH=src python -m catalytic_earth.cli apply-label-factory-actions \
  --label-factory-audit artifacts/v3_label_factory_audit_650.json \
  --out artifacts/v3_label_factory_applied_labels_650.json
```

## Mechanism Ontology

`data/registries/mechanism_ontology.json` maps seed fingerprints into mechanism
families:

- hydrolysis
- PLP chemistry
- radical rearrangement
- flavin redox
- heme redox

`build-family-propagation-guardrails` audits where family propagation is blocked
across UniRef/CATH/InterPro-style evidence or the current local proxies
available in this repo: M-CSA mechanism text, ligand/cofactor context, and
pocket geometry. Local proxies can prioritize review but cannot promote labels
above bronze without direct evidence.

## Active Learning Queue

`build-active-learning-queue` ranks entries by:

- uncertainty
- impact
- novelty
- hard-negative value
- evidence conflict
- family-boundary value

The queue includes unlabeled tranche candidates plus labeled entries whose
current evidence needs review. After the accepted 650 batch, the current queue
artifact is `artifacts/v3_active_learning_review_queue_650.json`: it retains
all 32 unlabeled post-batch candidate rows in addition to labeled review rows.
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
review. The accepted-650 artifact is
`artifacts/v3_review_debt_summary_650.json`; the generated but unpromoted
675 preview has its own triage artifact at
`artifacts/v3_review_debt_summary_675_preview.json`. When a baseline debt
artifact is provided, the summary records carried versus new review-debt rows
and full carried/new entry-id lists so preview growth is auditable even when
the prioritized row table is capped.

```bash
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_675_preview.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_675_preview_batch.json \
  --baseline-review-debt artifacts/v3_review_debt_summary_650.json \
  --max-rows 35 \
  --out artifacts/v3_review_debt_summary_675_preview.json
```

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
  --gate artifacts/v3_label_factory_gate_check_500.json \
  --gate artifacts/v3_label_factory_gate_check_525.json \
  --gate artifacts/v3_label_factory_gate_check_550.json \
  --gate artifacts/v3_label_factory_gate_check_575.json \
  --gate artifacts/v3_label_factory_gate_check_600.json \
  --gate artifacts/v3_label_factory_gate_check_625.json \
  --gate artifacts/v3_label_factory_gate_check_650.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_500.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_525.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_550.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_575.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_600.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_625.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_650.json \
  --out artifacts/v3_label_factory_batch_summary.json
```

The summary records accepted-batch counts, review debt, hard-negative status,
factory gate status, and unlabeled queue retention across all accepted batches.
For preview batches, also pass `--scaling-quality-audit`; the summary records
audit readiness, accepted-label review-debt blockers, unclassified new
review-debt rows, omitted underrepresented queue rows, and non-blocking audit
warnings before the batch can be treated as promotion-ready.

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
  --batch-id 675_preview \
  --acceptance artifacts/v3_label_batch_acceptance_check_675_preview.json \
  --readiness artifacts/v3_label_preview_promotion_readiness_675.json \
  --review-debt artifacts/v3_review_debt_summary_675_preview.json \
  --review-evidence-gaps artifacts/v3_review_evidence_gaps_675_preview.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_675_preview_batch.json \
  --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_675_preview_batch.json \
  --hard-negatives artifacts/v3_hard_negative_controls_675_preview_batch.json \
  --decision-batch artifacts/v3_expert_review_decision_batch_675_preview.json \
  --structure-mapping artifacts/v3_structure_mapping_issues_675.json \
  --expert-review-export artifacts/v3_expert_review_export_675_preview_post_batch.json \
  --out artifacts/v3_label_scaling_quality_audit_675_preview.json
```

When sequence-family or near-duplicate cluster evidence is available, add
`--sequence-clusters`. Without it, the audit emits a specific
`sequence_cluster_artifact_missing_for_near_duplicate_audit` warning so the
paralog/near-duplicate check is not silently skipped before larger propagation
batches.

Bulk label expansion should proceed only in batches, and each batch must
regenerate the factory audit, adversarial negatives, active-learning queue,
expert export/import artifacts, family-propagation guardrails, validation, and
tests before its labels are counted.

Current 650-queue gate state:

- 10/10 gate checks pass.
- Passing gates: explicit label schema, ontology loaded, promotion
  demonstrated, demotion/abstention demonstrated, applied label actions ready,
  adversarial negatives mined, active queue ranked, expert-review export ready,
  family-propagation guardrails ready, and unlabeled queue retention ready.
- 75 bronze-to-silver promotions are proposed in the applied-label artifact
  after the accepted 650 batch.
- 144 rows are queued for active-learning review after the accepted 650 batch,
  including all 32 unlabeled post-batch candidates.
- 100 adversarial negative controls are mined.
- 56 expert-review items are exported from the post-650 review queue.
- The 500, 525, 550, 575, 600, 625, and 650 decision batches accepted 143 new
  countable labels beyond the 475-entry source slice. The canonical registry
  now contains 618 bronze automation-curated labels, while the review-state
  registry keeps pending `needs_expert_review` placeholders separate from the
  countable benchmark.
- A 675 preview batch is generated and preview-accepted, but it is not promoted
  to the canonical registry until its decisions are reviewed. The preview was
  quality-repaired so below-threshold evidence-limited negatives remain
  review-state only. Its review-debt summary ranks 61 evidence-gap rows,
  including 61 `needs_more_evidence` decisions, 37 carried rows, 24 new rows,
  and full carried/new entry-id lists plus next-action counts by debt status in
  metadata. `artifacts/v3_label_factory_preview_summary_675.json` records 1
  clean countable addition (`m_csa:666`), 61 pending review-state rows, 11/11
  passing gates, 1 attached scaling-quality audit with recommendation
  `review_before_promoting`, and 0 blocker metrics.
- `artifacts/v3_label_preview_promotion_readiness_675.json` separates
  mechanical acceptance from promotion. It is mechanically ready, but its
  recommendation is `review_before_promoting` because preview review debt rises
  from 53 to 61 rows and pending review rows remain. The readiness metadata
  also copies the new debt entry ids and next-action counts from the preview
  debt summary.
- `artifacts/v3_label_scaling_quality_audit_675_preview.json` records the
  failure-mode audit. It has 0 accepted labels with review debt and 0 hard
  negatives. It observes hydrolysis-dominated queue composition, but the
  diversity-aware review export retains all underrepresented ontology-family
  rows, so the scaling-quality audit has 0 blockers. It still flags ontology
  scope pressure, cofactor ambiguity, reaction/substrate mismatches, active-site
  mapping gaps, and the missing sequence-cluster artifact needed for a stronger
  paralog/near-duplicate audit as promotion-review issues.

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
