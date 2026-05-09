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

Each automation run is a 55-minute focused work block. The remaining time in
the hour is break/overhead.

At the start of each block, record the real wall-clock start timestamp. At
50 minutes elapsed from that timestamp, stop starting new implementation work
and begin wrap-up: tests, artifacts, handoff, progress log, commit, and push.

After each hourly work block:

1. Log measured elapsed time and evidence. Use `--time-mode measured` with
   `--started-at` and `--ended-at`, or `--measured-minutes`, whenever possible.
2. Update `status.md`.
3. Update `handoff.md` with exact next-agent instructions.
4. Run relevant checks.
5. Commit and push to `origin/main`.
6. Recalibrate the scope or timeline if observed speed contradicts estimates.

## Context Rule

If the active chat context becomes heavy or performance drops, use this folder as
the recovery surface. Update `handoff.md`, then continue from a fresh context
using the repository state as the source of truth.
