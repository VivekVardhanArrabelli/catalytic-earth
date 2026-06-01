# D11 Northstar Bundle Import Handoff - 2026-05-31

## Scope

Manual repo-sync handoff for the D11/northstar commits imported from local
bundles and pushed to `origin/main`. This was not a full automation work block,
but this file records the state so the next automation run can start from the
right context instead of rediscovering it.

## Wall Clock

- Start: 2026-05-31 local evening session
- End: 2026-05-31 local evening session
- Run type: manual bundle verification, fast-forward import, focused validation,
  push, and automation retarget

## Git State

- Repository:
  `/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth`
- Starting visible `main`: `e46753a`
- Imported first bundle:
  `/Users/vivekvardhanarrabelli/Downloads/d11work.bundle`
- First bundle result: `main` fast-forwarded to `5af7848`
- Imported second bundle:
  `/Users/vivekvardhanarrabelli/Downloads/d11northstarincremental.bundle`
- Second bundle result: `main` fast-forwarded to `98d803c`
- Final pushed functional commit before this handoff:
  `98d803c Add northstar next-works doc (feature overlap is the binding constraint)`

The second bundle contained exactly these four expected commits:

```text
6a2451f Operating-point reality: de novo AUC 0.852 is not a usable abstention threshold
383fc69 Per-channel rule gate: operational architecture settled; constraint is feature overlap
605e763 Rule out in-repo lever: richer geometry sub-features don't beat top1_score
98d803c Add northstar next-works doc (feature overlap is the binding constraint)
```

## Validation

Focused validation after each bundle import used:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_mechanism_abstention_gate_eval.py \
  tests/test_mechanism_novelty_abstention_eval.py \
  tests/test_mechanism_relationship_surface_eval.py
```

Result after `5af7848`: `23 passed`.

Result after `98d803c`: `23 passed`.

Push result:

```text
origin/main = 98d803c
local main = 98d803c
```

## Functional State

D11 now says:

- De novo abstention is rank-achievable: deployment-valid predicted/apo geometry
  two-channel gate reaches AUC 0.852.
- That is not yet operational: no threshold gives enough OOS capture at 90%
  in-scope retention.
- The per-channel rule-gate architecture is settled, but lift is bounded because
  in-scope and OOS geometry score distributions overlap.
- Richer in-repo geometry subfeatures do not beat `top1_score`; the binding
  constraint is missing/new mechanism-discriminative feature signal, not another
  threshold.

Primary next-work document:

```text
work/NEXT_WORKS_northstar_20260531.md
```

## Automation Retarget

The `catalytic-earth-work-loop` automation was retargeted and set `ACTIVE`.
Its stale t6/t12 blocker prompt was replaced. It now preserves:

- 55-minute wall-clock cap
- mandatory startup continuity
- mandatory wall-clock handoff
- no label/ontology/threshold/split mutation without explicit artifact contract
- no heldout leakage

Current priority order:

1. Predicted-geometry retrieval over the `in_distribution` atlas.
2. Fold-level novelty signal for the cofactor-confounded OOS rows.
3. Learned mechanism-feature embedding scaffold/pilot.
4. Family-set expansion proposal to de-risk the 8-fingerprint bound.

## Exact Next Action

Start with Priority 1 only. Find the current702 split/manifests and existing
predicted-geometry retrieval code/artifacts. Produce or unblock a nonzero,
row-aligned predicted-geometry atlas retrieval artifact for the
`in_distribution` atlas rows using the same deployment/predicted-geometry fields
as the heldout/query retrieval.

Desired first output:

```text
artifacts/v3_predicted_geometry_in_distribution_atlas_retrieval_current702_20260601.json
work/predicted_geometry_in_distribution_atlas_retrieval_current702_20260601.md
```

If the predicted geometry structures or AF outputs are missing, do not fabricate
scores. Search existing caches/artifacts/worktrees first, then produce an exact
acquisition/job manifest and runnable command.

Stop broadening once Priority 1 produces a valid nonzero atlas artifact; the next
run should then rerun deployment abstention and atlas novelty against that
artifact.
