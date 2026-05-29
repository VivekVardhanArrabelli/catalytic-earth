# Agent Runbook

Use this runbook for bounded maintenance, audits, and artifact/report work in
the main repo.

## Source Of Truth Order

1. `docs/project_state.md` for current north star, benchmark state, blockers,
   and next gates.
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

## Leakage Rules

- Train or calibrate only on in-distribution train/cal rows.
- Evaluate heldout rows once, after threshold/model choices are fixed.
- Do not join labels into feature generation except as final evaluation targets.
- Keep active-site pooling and whole-sequence evidence budgets separate.
- For old Wave 1 artifacts, read `m_csa:497` and `m_csa:750` through the OOS
  revision artifacts before interpreting primary flavin metrics.
- Treat review packets as provenance and triage context, never as direct model
  inputs.

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
