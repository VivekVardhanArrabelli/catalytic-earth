# Agent Runbook

Use this runbook for bounded maintenance, audits, and artifact/report work in
the main repo.

## Source Of Truth Order

Quick compass first: `docs/MAP.md` — one page with the current headline
(**cofactor reconstruction**: predicted-apo 23/45 → 37/45, confirmed) and where each
thing lives. Then in order:

1. `docs/project_state.md` for current north star, benchmark state, blockers,
   and next gates. (The "Current Benchmark State" section opens with the current
   headline result — cofactor reconstruction — so it is not buried.)
2. `docs/decision_log.md` for dated decisions that override older wording.
2. `docs/decision_log.md` for dated decisions that override older wording.
3. `docs/artifact_index.md` for which artifacts answer which questions.
4. Machine artifacts under `artifacts/`, especially JSON contracts and audit
   outputs named in the project state.
5. Registries under `data/registries/` as canonical data sources. Read them for
   context; do not edit them unless the task explicitly authorizes it.
6. Human reports under `work/` and older docs for historical context.

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

For code changes:

```bash
python -m unittest discover -s tests
```

For docs-only changes, `PYTHONPATH=src python -m catalytic_earth.cli validate`
and `git diff --check` are usually enough unless the docs describe a command
whose output should be verified.

## Bounded Task Pattern

1. Read the automation memory, if an automation ID is provided.
2. Check disk headroom and branch status.
3. Read `docs/project_state.md`, `docs/decision_log.md`, and
   `docs/artifact_index.md`.
4. Identify the exact input artifacts and whether newer readthrough addenda
   supersede them.
5. Write new outputs with explicit guardrails, source artifacts, split policy,
   and verification fields.
6. Validate JSON, run the CLI validator when feasible, and run
   `git diff --check`.
7. Commit and push only if the task requests it and verification passes.

If the worktree is already dirty, identify which files are unrelated before
editing. Do not revert or stage unrelated user changes. If a tracked file is
already modified and affects the requested command, work with it and call out
the residual risk in the final status.

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
