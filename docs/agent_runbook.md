# Agent Runbook

Use this runbook for bounded scientific work and necessary maintenance in the
main repo. Hourly research follows [the current standing brief](HOURLY_RESEARCH.md)
and the marked current block in `work/handoff.md`. The hourly task uses the
atlas North Star and its eventual de novo design purpose, not historical
predictor/deployment queues.

## Source Of Truth Order

Current order:

1. `CLAIMS.md` for canonical current claim status and permitted wording.
2. `ERRATA.md` for explicit corrections to historical wording.
3. `docs/ATLAS_TRUTH_POLICY.md` for counted objects, evidence tiers, exposure,
   and admission rules.
4. `data/governance/exposure_ledger.jsonl` before evaluation or tuning work.
5. `docs/MAP.md` and `docs/RAPID_ATLAS_PLAN.md` for mission and execution order.
6. `docs/CURRENT_STATE.md` and `docs/CURRENT_DECISIONS.md` for the compact
   current reset.
7. `docs/project_state.md`, `docs/decision_log.md`, `docs/artifact_index.md`,
   machine artifacts, registries, and human reports
   for progressively older or more detailed evidence.

If history conflicts with the claim ledger or errata, preserve the historical
record and use the corrected wording. Never reset exposure by renaming a split,
branch, artifact, endpoint, or agent session.

Older predictor/cofactor instructions remain recoverable in Git history. They
do not override this order or become the next task merely because an old
handoff contains an imperative.

## Safe Edits

- `docs/*.md` when creating durable orientation, design notes, or cleanup.
- `work/*.md` for human-readable reports from a bounded run.
- New `artifacts/v3_*.json` or `artifacts/v3_*.jsonl` when a task explicitly
  asks for machine-readable audit outputs.
- New worksheet-style `artifacts/v3_*.tsv` only when it is explicitly
  manual-fill or review-only, has a matching `work/*.md` report, and is not
  consumed by training, threshold selection, or a feature contract until a
  strict evidence audit passes.
- Code and tests only when the task requires implementation.

## Forbidden Or Approval-Gated Edits

Do not edit these surfaces during ordinary cleanup/audit runs:

- `data/registries/curated_mechanism_labels.json`
- `data/registries/mechanism_fingerprints.json`
- `data/registries/mechanism_ontology.json`
- label imports, registry summaries, ontology entries, production scoring,
  global thresholds, or import gates

Do not tune thresholds on heldout/test rows. Do not use names, EC numbers,
Rhea IDs, source prose, mechanism text, expert notes, review-hold reasons, or
candidate-specific repair rationale as predictive model features. Do not run
large downloads by default. Stop or redesign the run if disk would fall below
10 GiB free.

Real supervised model runs on CE labels require explicit task authorization and
a leakage preflight. Diagnostic probes must state whether they trained anything,
which split selected thresholds, and whether heldout rows were final-only.

## Validation Commands

Before heavy work:

```bash
df -h .
git status --short --branch
```

For JSON outputs:

```bash
python -m json.tool artifacts/path.json >/dev/null
```

For routine repository validation:

```bash
PYTHONPATH=src python -m catalytic_earth.cli validate
git diff --check
```

For shared code changes, run the relevant focused checks and existing core tier:

```bash
python scripts/run_test_tier.py core/unit
```

For docs-only changes, `PYTHONPATH=src python -m catalytic_earth.cli validate`
and `git diff --check` are usually enough unless the docs describe a command
whose output should be verified.

## Bounded Task Pattern

1. For scheduled writers, acquire the owner-checked shared Git lock first.
2. Check disk headroom, branch, remote and unfinished work; preserve unrelated edits.
3. Read the current handoff and the source-of-truth order above. Automation
   memory and older reports are context, not authority over current decisions.
4. Choose the highest-impact scientific question and its expected information gain.
5. Produce new content, evidence or a supported decision where justified.
   A new report, schema, test or artifact is not required merely to fill a run.
6. Verify the changed content proportionately and run `git diff --check`.
7. Publish verified changes within task authorization and preserve an exact
   continuation when incomplete. Stop all workers before releasing ownership.

If the worktree is already dirty, identify which files are unrelated before
editing. Do not revert or stage unrelated user changes. If a tracked file is
already modified and affects the requested command, work with it and call out
the residual risk in the final status.

For timed automation, continue after a checkpoint only when another bounded
action has justified scientific information gain and fits the remaining time.
Reserve approximately 5-10 minutes for verification, publication and handoff;
aim to finish by minute 55. No minimum runtime or hourly commit is required.
If a run overruns, its lock makes the next scheduled writer skip. Follow
`docs/HOURLY_RESEARCH.md` for recovery and the three reconsideration rules.

## Leakage Rules

- Train or calibrate only on in-distribution train/cal rows.
- Evaluate heldout rows once, after threshold/model choices are fixed.
- Do not join labels into feature generation except as final evaluation targets.
- Keep active-site pooling and whole-sequence evidence budgets separate.
- For old Wave 1 artifacts, read `m_csa:497` and `m_csa:750` through the OOS
  revision artifacts before interpreting primary flavin metrics.
- Treat review packets as provenance and triage context, never as direct model
  inputs.

## Common Interpretation Traps

The following predictor-specific notes are historical context for those tracks;
they do not authorize new evaluation or select the hourly atlas research task.

- Wave 1.2 clean experimental-coordinate geometry is the current router gate,
  but it is not a deployment claim. Read
  `artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json`
  before making sequence-to-predicted-structure claims.
- A row in a review packet, scout, or PyMOL queue is not countable label
  support until it passes explicit import and label-factory gates.
- A manual extraction worksheet is not source evidence. Treat blank worksheet
  cells as a to-do list, not as a sidecar, and require a strict source-evidence
  audit before using any filled values in feature generation.
- A draft source-evidence sidecar is still not model input. Rows must remain
  non-consumable until `review_status: approved` carries reviewer provenance
  and the strict source-evidence audit passes after that approval.
- Existing ProtT5 and SaProt exports are not fair logistic-head peers for
  ESM-2/ESM-C until row-aligned local sidecars or local weights exist.

## Output Locations

- Machine-readable audit: `artifacts/v3_<topic>_<scope>_<date>.json`
- Human-readable report: `work/<topic>_<date>.md`
- Durable project memory: `docs/project_state.md`, `docs/decision_log.md`,
  `docs/artifact_index.md`, and `docs/agent_runbook.md`
- Code tests: `tests/test_<topic>.py`

## Commit Checklist

- Required artifacts/reports are present.
- JSON parses.
- No forbidden registry, ontology, threshold, import, production scoring, or
  label changes are present unless explicitly authorized.
- Disk is above 10 GiB free.
- Validation commands were run or the reason they were skipped is documented.
- Commit message names the bounded outcome, not the whole research history.
