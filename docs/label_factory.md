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
  --retrieval artifacts/v3_geometry_retrieval_475.json \
  --hard-negatives artifacts/v3_hard_negative_controls_475.json \
  --adversarial-negatives artifacts/v3_adversarial_negative_controls_475.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_label_factory_audit_475.json
```

`apply-label-factory-actions` materializes those recommendations into a registry
artifact for review without overwriting the curated registry:

```bash
PYTHONPATH=src python -m catalytic_earth.cli apply-label-factory-actions \
  --label-factory-audit artifacts/v3_label_factory_audit_475.json \
  --out artifacts/v3_label_factory_applied_labels_475.json
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

The queue includes all 25 unlabeled 500-slice candidates plus labeled entries
whose current evidence needs review. The 500-entry queue artifact is
`artifacts/v3_active_learning_review_queue_500.json`.

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
accepted decisions to a label registry copy while preserving existing evidence
sources and appending `expert_review_import` provenance.

No-decision imports are safe previews. Accepted gold decisions require expert
review status and a rationale.

## Scaling Gate

Before any new label batch is counted as benchmark labels, run:

```bash
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates \
  --label-factory-audit artifacts/v3_label_factory_audit_475.json \
  --applied-label-factory artifacts/v3_label_factory_applied_labels_475.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_500.json \
  --adversarial-negatives artifacts/v3_adversarial_negative_controls_475.json \
  --expert-review-export artifacts/v3_expert_review_export_500.json \
  --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_500.json \
  --out artifacts/v3_label_factory_gate_check_500.json
```

Bulk label expansion should proceed only in batches, and each batch must
regenerate the factory audit, adversarial negatives, active-learning queue,
expert export/import artifacts, family-propagation guardrails, validation, and
tests before its labels are counted.

Current 500-queue gate state:

- 9/9 gate checks pass.
- Passing gates: explicit label schema, ontology loaded, promotion
  demonstrated, demotion/abstention demonstrated, applied label actions ready,
  adversarial negatives mined, active queue ranked, expert-review export ready,
  and family-propagation guardrails ready.
- 61 bronze-to-silver promotions are proposed in the applied-label artifact.
- 98 labels are marked for review/abstention in the applied-label artifact.
- 100 adversarial negative controls are mined.
- 123 active-learning rows are queued, including all 25 unlabeled candidates.
- 50 expert-review items are exported: the top 25 ranked rows plus all 25
  unlabeled candidates.

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
