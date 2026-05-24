# M-CSA AI-Visual Review Surface, 2026-05-24

This is a review-only orientation note for the fixed 298-row M-CSA
AI-assisted visual review universe. It does not make accept/reject decisions
and does not authorize label imports, import previews, registry edits,
fingerprint edits, scoring changes, artifact migration, uploads, or removals.

## Count Invariants

- Source universe: 298 rows.
- Review signal split: 22 accepted review signals, 210 current-target-only
  hard negatives, 66 unresolved `needs_more_evidence` holds.
- Human review packet: 40 rows, all with blank decisions.
- Fast path: 10 clean-likely-positive rows with local PyMOL scripts.
- Non-clean exact40 rows: 30 rows pre-sorted by review workflow.
- Deferred backlog: 26 rows outside exact40; review only after exact40 is
  complete or a new bounded plan promotes them.
- Canonical count invariants: 695 curated labels and 8 production
  fingerprints.

## Review Order

1. Open `artifacts/v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json`
   for the canonical exact40 queue.
2. Use
   `artifacts/v3_mcsa_ai_visual_exact40_review_workqueue_worksheet_20260524.tsv`
   when a spreadsheet/table view is easier.
3. Start with
   `artifacts/v3_mcsa_ai_visual_clean10_fast_review_cards_20260524.json` and
   the local PyMOL scripts under
   `artifacts/review_pymol/mcsa_ai_visual_exact40_20260524/`.
4. Use
   `artifacts/v3_mcsa_ai_visual_nonclean30_exact40_strategy_20260524.json` for
   the 30 harder exact40 rows.
5. Record human decisions only in
   `artifacts/v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json`
   or a later explicit derivative created for that purpose.
6. Leave
   `artifacts/v3_mcsa_ai_visual_deferred26_after_exact40_backlog_20260524.json`
   and
   `artifacts/v3_mcsa_ai_visual_deferred26_after_exact40_worksheet_20260524.tsv`
   untouched until exact40 review is complete.

## Machine-Readable Entry Point

Use `artifacts/v3_mcsa_ai_visual_review_support_index_20260524.json` as the
machine-readable index. It links the triage matrix, exact40 packet, clean10
cards, PyMOL index, workqueue, worksheets, deferred backlog, learning manifest,
and rejected-signal taxonomy.

## Learning Signal Guardrail

For representation-learning work, start from
`artifacts/v3_mcsa_ai_visual_learning_signal_manifest_20260524.json` and drop
fields listed in its prediction-leakage contract before training. The 210
rejected rows are current-target hard negatives only, not global negatives, and
the 22 accepted review signals are not countable labels.
