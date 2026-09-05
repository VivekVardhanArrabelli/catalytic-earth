# Catalytic Earth maintenance and forward progress — 2026-09-05

Shared internal message board requested by the project owner. This records
engineering coordination; it is not scientific review or evidence of biological
validation.

## Objective and baseline

- Inspect the actual project, correct actionable defects, and complete a useful
  next engineering step with verification.
- Clean local checkout fast-forwarded from `8e1feea1` to GitHub main
  `3a4d786ff0275fe6dcfd6fabaa737b809d881bdf`.
- Working branch: `codex/atlas50-forward`.
- Current reality: Atlas-10 runs; Atlas-50 Phase B has 97 unreviewed packets,
  a 47-case unfrozen candidate, and unmet human review/freeze conditions.
- Preserve source evidence, inherited Atlas objects, protected registries,
  exposure history, and honest review state. No external messages are authorized.

## Ownership and coordination

| Agent | Scope | Status |
| --- | --- | --- |
| root | Review intake module/CLI, contract/CI integration, board, final verification | Integration complete; publishing for review |
| phase_b_audit | Phase B submission validator and its existing test file | Fixes and independent intake review complete |
| forward_path | README and current state/decision/Phase B documents | Documentation and independent peer review complete |
| validation | Baseline checks, wheel reproduction, new review-intake test file | 117 core tests pass, including 13 intake tests |

Root owns this file to avoid write collisions. Agents send findings and updates
through the collaboration mailbox; root records decisions here and assigns
non-overlapping file ownership before edits. Agents may read this board anytime.

## Decisions and evidence

1. GitHub's latest main CI passed; there are no open pull requests or issues in
   the initial read. Local validation remains to be run.
2. Do not mistake prepared packets for actual review. Automation can improve
   intake, validation, and reproducibility without inventing reviewer decisions.
3. Iterate on reproduced defects and peer review. Stop additional iteration when
   relevant checks pass and no material unresolved issue remains in the change.

## Updates

- Baseline core/unit tier: 98 tests passed on Python 3.12. The working-tree
  repository contract check reached architecture path-manifest validation and
  flagged the newly added board; isolated baseline verification is in progress.
- Selected forward step: a usable local CLI to list/export packets, create
  deliberately blank review drafts, validate supplied submissions, record them
  without replacement, and report intake separately from the frozen checkpoint.
- Peer audit identified missing type/date checks, revision-evidence loopholes,
  and acceptance/disposition inconsistencies. The validator owner is correcting
  those without changing frozen scientific data or pretending review occurred.
- Intake rejects ambiguous JSON and duplicate IDs, binds exact packet content,
  preserves submitted bytes, and checks committed evidence against a Git base.
  CI will compare against the PR base or previous push, not only current HEAD.
- No real review submissions have been supplied or recorded. No external
  messages, source reacquisition, model runs, or scientific evaluations occurred.
- Isolated baseline verification confirmed all repository contracts pass on a
  clean sparse checkout. The locked baseline wheel reproduces Atlas-3 (3 cases,
  9 objects) and Atlas-10 (10 cases, 30 objects) from empty directories. The
  earlier working-tree architecture failure was solely the added file count.
- The validator now rejects malformed identity/date fields, contradictory
  classification/disposition decisions, source confirmations that contradict
  explicit gaps, and empty revision-evidence objects. A second pass caught
  Python accepting an invalid timezone offset by normalization; bounds and a
  regression test were added.
- Intake tests verify ambiguous JSON rejection, intentionally invalid drafts,
  exact byte preservation, duplicate IDs, invalid existing evidence, namespace
  indirection, unresolved/conflicting decisions, and deletion or rewriting of
  evidence both before and after committing a change.
- The command is deliberately a submission intake. It cannot authenticate a
  human reviewer or apply scientific revisions. A later candidate update must
  retain the actual proposed corrections and adjudications; no revision is
  inferred from an accept/revise/unresolved verb.
- Current scientific data and all frozen Atlas/registry/exposure assets remain
  byte-identical to the GitHub baseline. Only the architecture file-count field
  is refreshed for the new engineering files.
- Final local checks: 117 core/unit tests pass on Python 3.12; full repository
  contracts pass, including both deterministic Atlas-50 packages, all inherited
  Atlas objects, manifests, exposure controls, and the new intake scan.
  `git diff --check` passes. CLI status remains zero submissions across 97 packets.

## Completion boundary

The implemented next step is review intake and submission-integrity repair.
Actual reviewer submissions, conflict adjudication, an approved source budget,
and an explicit reviewed selection freeze remain scientific follow-on work.
No external outreach is performed by this change. Root will publish the tested
branch as a pull request and report its CI and merge state separately.
