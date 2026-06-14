# Rhea/Metal Annotation Backfill Blocker - post silver apply

Run: 2026-06-14T18:43:15Z

Status: blocked for mutation in this repo state. No registry was written.

## Finding

The current repo has family sourcing modules and the non-destructive
`scout_evidence_handle_expansion.py` recon path, but it does not have a bounded
Rhea/metal annotation backfill writer that can safely add missing Rhea reactions
or metal annotations to already-admitted registry rows.

The refreshed evidence-handle scout for this run is
`artifacts/v3_evidence_handle_expansion_current702_20260614_post_silver_apply.json`.
It is useful for source planning, but it is not a row-level registry backfill.

## Required Before Any Apply

- A row-level target selector for data-ceiling families such as metallopeptidase,
  metallophosphoesterase/nuclease, metal racemase/epimerase, and molybdopterin.
- A curated source fetcher/parser for Rhea reactions and metal/cofactor annotations.
- A merge policy that writes only `excluded_context` / source provenance and never
  `predictive_evidence`.
- Tests proving EC is scope-only, EC-only rows are not admitted, and the frozen
  current702 registry is never written.
- Preview/apply commands that print frozen current702 SHA before and after any
  external registry write.

## Next Action

Implement this as a non-destructive preview first. Until then, use the evidence
handle scout for planning only and do not mutate labels based on annotation gaps.
