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

All Codex automations for this project must run on `gpt-5.5` with `xhigh`
reasoning. Do not downgrade the model or reasoning level when editing the
automation.

Each automation run is a measured hour with a strict 50-minute productive work
requirement followed by about 5 minutes of wrap-up. The productive portion must
advance completion of the whole project.

At the start of each block, record the real wall-clock start timestamp. At
50 minutes elapsed from that timestamp, stop starting new implementation work
and begin wrap-up: tests, artifacts, documentation review, handoff, progress
log, commit, and push.

Before 50 elapsed minutes, the agent must not hand off early, idle, or spend the
remaining time only reporting. If the handoff-assigned task is completed or
blocked, it must:

1. Write a short plan for the remaining measured time before the 50-minute
   wrap-up boundary.
2. Execute the highest-value bounded unblocked item from that plan immediately.
3. Continue advancing the project until the 50-minute wrap-up boundary, then
   complete normal wrap-up.

After each hourly work block:

1. Log measured elapsed time and evidence. Use `--time-mode measured` with
   `--started-at` and `--ended-at`, or `--measured-minutes`, whenever possible.
2. Review `README.md`, `docs/*.md`, `work/scope.md`, `work/handoff.md`, and
   `work/status.md`; update anything stale so docs reflect the actual end state.
3. If no documentation changes are needed, record `documentation checked; no
   changes needed` in handoff or progress evidence.
4. Update `status.md`.
5. Update `handoff.md` with exact next-agent instructions.
6. Run relevant checks.
7. Commit and push to `origin/main`.
8. Verify remote sync before handoff:
   `git fetch origin` then confirm `git rev-parse HEAD` equals
   `git rev-parse origin/main` and confirm no merge is pending.
9. Recalibrate the scope or timeline if observed speed contradicts estimates.

## Context Rule

If the active chat context becomes heavy or performance drops, use this folder as
the recovery surface. Update `handoff.md`, then continue from a fresh context
using the repository state as the source of truth.
