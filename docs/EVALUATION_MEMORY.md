# Mechanical evaluation memory

Evaluation independence is computed from versioned evidence; it is never
accepted from a hand-written `one_shot=true` field.

## Canonical files

- `data/governance/exposure_ledger.jsonl` is the append-only surface event log.
- `data/governance/exposure_rows.jsonl` contains one row per data item and
  evaluation surface, including the source release/hash, label version, split
  role, first exposure commit/time, exposed information, later decisions, and
  development/independent-test eligibility.
- `data/governance/exposure_rows_manifest.json` binds the ledger bytes and each
  surface's exact row identity set.
- `data/governance/preregistration-v1.schema.json` freezes the code commit,
  data hashes, row-set hash, threshold, metric, seed, endpoint, role, and
  namespace of every new evaluation.

The historical row ledger is rebuilt from first-exposure Git commits with:

```bash
python scripts/build_exposure_row_ledger.py --check
```

This requires a full-history clone. The four audited current files match their
first-exposure Git bytes under the repository's canonical LF text-hash rule.
Earlier Windows checks falsely reported all four as drifted because the
worktree used CRLF line endings. The historical commit remains authoritative;
today's copy is never allowed to redefine row identity even when its bytes
match.

## Evaluator gate

Call `catalytic_earth.truth_guard.assert_evaluation_request_allowed` before
loading scores or labels. The gate rejects unknown rows, development use of a
protected test surface, independent-test claims on a spent surface, and
independent-test subsets that trim the frozen population. Post-hoc work must
use a namespace beginning with `posthoc/`.

`compute_one_shot_status` returns `available_once` only when every row remains
`frozen_unscored`, is independently eligible, and has no score or outcome
exposure. Every other surface returns `spent`.

## Interpretation boundary

The 22-row Option-B surface is currently `available_once`, but only as a
bronze-proxy test. Known proxy labels and its small selected population limit
the resulting claim even if the score is clean. The 140-row M-CSA surface, the
702-row chemistry surface, and the 136-row EC-proxy surface are spent.
