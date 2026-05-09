# Work Folder

This folder is the durable operating record for Catalytic Earth.

It exists because the project should not depend on chat memory. Every serious
work session should leave enough state here for a fresh context to continue.

## Files

- `scope.md` defines the current v0/v1/v2 targets and completion criteria.
- `progress_log.jsonl` records timed work entries.
- `status.md` is generated from the progress log.
- `handoff.md` stores the current continuation instructions.

## Operating Rule

After each material work chunk:

1. Log elapsed time and evidence.
2. Update `status.md`.
3. Run relevant checks.
4. Commit and push if the chunk materially advances the project.
5. Recalibrate the scope or timeline if observed speed contradicts estimates.

## Context Rule

If the active chat context becomes heavy or performance drops, use this folder as
the recovery surface. Update `handoff.md`, then continue from a fresh context
using the repository state as the source of truth.
