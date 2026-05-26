# North-Star Wave 1 to Engine Handoff - 2026-05-26

## What changed

This handoff converts Wave 1 diagnosis into a practical diagnostic router and evidence queue. It is not a production scorer, not a threshold selection, and not a label or ontology change.

New artifacts:

```text
artifacts/v3_foldseek_geometry_diagnostic_router_pilot_702_20260526.json
artifacts/v3_targeted_mechanism_evidence_acquisition_queue_702_20260526.json
```

The router covers 140 heldout rows from `artifacts/v3_wave1_structure_neighborhood_audit_20260526.json`. Route counts are: evidence_conflict_no_claim=1, fold_conflict_abstain_or_review=15, missing_structure_or_embedding_blocker=6, near_orphan_geometry_supported=18, oos_boundary_abstain=83, structure_neighbor_transfer_supported=9, v2_sublabel_needed=8.

## First practical engine decision

Do not scale models next. Scale the diagnostic evidence router and evidence-acquisition loop. Use Foldseek as a structural-neighborhood router, not a standalone mechanism scorer. Let active-site geometry nominate near-orphan primary candidates when same-fingerprint structural support is weak, and force abstain/review when Foldseek crosses an OOS, secondary, or different-primary boundary.

Composite diagnostic counts: 27 primary rows retained as diagnostic candidates, 113 rows abstained/reviewed/blocked, and 0 composite OOS false positives. Raw component OOS/secondary false positives are still important canaries: Foldseek structural NN has 8, sequence-NN has 25, ESM-2 has 16, and geometry has 0 under its abstention policy.

## Evidence to acquire next

1. Curate fold-conflict hard negatives first: `m_csa:217`, `m_csa:428`, `m_csa:440`, `m_csa:477`, plus primary geometry-rescue rows `m_csa:250`, `m_csa:497`, `m_csa:517`, `m_csa:916`, and `m_csa:990`.
2. Repair or confirm near-orphan primary support for metal, flavin, and serine-hydrolase rows where geometry is carrying the signal under weak Foldseek support.
3. Send proposal-only v2 sublabels for expert review before using child mechanism strata in evals, especially unresolved metal-water hydrolase, unresolved acyl-enzyme hydrolase, flavin monooxygenase boundary, and underpowered child families.
4. Add representation and geometry canaries: `m_csa:43` and `m_csa:750` are learned-representation failure canaries; no true Foldseek-correct/geometry-wrong primary canary exists yet, so one should be mined or acquired.

## Guardrails

No labels, ontology, fingerprint registry, imports, thresholds, model scaling, production scoring, representation branch outputs, or predictive use of EC/name/prose/expert-note/source IDs were changed. V2 sublabels remain proposal-only and review-only.

## Verification target

Validate both JSON artifacts with `python -m json.tool`, then run `PYTHONPATH=src python -m catalytic_earth.cli validate`. Focused tests are unnecessary unless code changes are made.
