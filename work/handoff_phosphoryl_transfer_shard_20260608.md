# Phosphoryl-Transfer Boundary Shard Handoff

## Wall-clock Ledger

- STARTED_AT_UTC: `2026-06-08T15:11:23Z`
- STARTED_AT_LOCAL: `2026-06-08T10:11:23-0500`
- ENDED_AT_UTC: `2026-06-08T15:20:24Z`
- ENDED_AT_LOCAL: `2026-06-08T10:20:24-0500`
- ELAPSED_MINUTES: `9.017`
- Lock: `/tmp/ce_scaleout_phosphoryl_transfer.lock`

## Scope

Produced a family-sharded source-free candidate/evidence artifact for the phosphoryl-transfer boundary lane from current main. The shard combines current targeted-expansion factory and conversion rows with ATP-family boundary/control artifacts, ePK structure scout/review artifacts, AMP/product-state discriminator panels, and phosphatase/nucleotide rows from the current metal-hydrolase scale-out shard.

No label import or promotion was performed. No curated registry, ontology, imports, production threshold, train/test split, model weight, global doc, or heldout training/tuning surface was changed.

## Outputs

- JSON artifact: `artifacts/v3_scaleout_phosphoryl_transfer_shard_current702_20260608.json`
- Markdown report: `work/scaleout_phosphoryl_transfer_shard_current702_20260608.md`
- Lane handoff: `work/handoff_phosphoryl_transfer_shard_20260608.md`

## Result

- Candidate rows: `1281`
- `blocked_coordinate`: `16`
- `blocked_family_decision`: `142`
- `blocked_locator`: `33`
- `countable_candidate_preflight_only`: `1`
- `reject/OOS_preserve_signal`: `885`
- `review_only_evidence`: `204`

## Validation

- `python -m json.tool artifacts/v3_scaleout_phosphoryl_transfer_shard_current702_20260608.json`: passed.
- `git diff --check`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: passed with 702 curated mechanism labels.
- Custom shard guardrails: passed for 1,281 rows with required row fields, allowed terminal states, source hashes, source-free guardrail, and machine-actionable next steps.

## Exact Next Action

Review blocked-family ePK and UniProt kinase rows first, then the AMP/product-state discriminator rejects. Do not import from this shard directly; route candidate promotions through the merger/admission lane only after locator, duplicate, and source-free family gates pass.
