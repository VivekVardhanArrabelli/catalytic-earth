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
  byte-identical to the GitHub baseline. The architecture file-count field and
  report-archive membership index are refreshed for the new engineering files
  and this board. The archive index uses staged Git blobs, so its update must
  follow staging the board; a post-commit check caught and corrected that order.
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

## Follow-on: scientific review acceleration

The owner requested Rosalind setup and substantive review work while external
review is slow. The prior engineering checkpoint is pushed as PR #31 at
`a459ec78`; all four Linux/Windows Python 3.10/3.12 CI jobs passed.

- Root: identify/setup the requested Rosalind tool, reconcile current guidance,
  integrate source-supported corrections, and keep private correspondence out
  of the public repository.
- phase_b_audit: computational assessment of all 40 panel candidates, with
  primary-source checks concentrated on inclusion errors and representation
  blockers. Owns the new panel review JSON and report only.
- forward_path: computational assessment of the 57 fingerprint crosswalk rows,
  including granularity and candidate-handle mismatches. Owns the new crosswalk
  review JSON and report only.
- All new review results explicitly identify agent assessment and distinguish
  local inspection from refreshed source verification. Existing human review
  counts, frozen Phase A/B bytes, evidence tiers, and protected registries are
  not silently upgraded.
- Progress is measured by corrected claims, ruled-out mappings, usable source
  evidence, and fewer specific questions for humans—not additional blank forms.

### Scientific correction round

- Root completed the A0A177THN5 public-source reassessment. UniProt entry 32
  remains unreviewed/homology-inferred. InterPro IPR044831 explicitly contains
  both Ccp1 and APX; its short name cannot resolve donor specificity. CE-017
  and ER-011 withdraw the APX transfer and record retirement of the larger
  comparison. The current interpretation stays provisional. Historical
  handoff/shortlist documents carry the specific correction.
- The panel agent refreshed all 40 official M-CSA records and found exact
  agreement for the checked identifier/detail fields. That transcription
  result does not establish the source/applicability or representation gates.
  Focused concerns include M0106 carrier state, M0064 topology, M0107 component
  state, and M0753 exact source scope.
- The crosswalk agent found a direct cofactor mismatch at M0049 (pyruvoyl,
  placed under PLP), a missing named target for relation labels, and concrete
  locator omissions. A second agent pass used historical curated702 labels
  only as discovery leads; root specifically requested reconciliation against
  direct source evidence where the second pass overaccepted M0049.
- Root bounded the deeper follow-up to decision-changing rows. The full-row
  reports must say when a row received only local/identifier checks rather
  than imply 97 complete mechanistic adjudications.
- Rosalind Workbench was installed/enabled at 0.2.5-research-preview via the
  official app CLI; its launcher/settings are app-only. No GPT-Rosalind model
  inference or account Research entitlement is claimed. Current agents perform
  the assessment using public sources. No private correspondence is archived.

### Integration and second-pass checks

- The completed crosswalk artifact covers exactly the 57 frozen fingerprint
  IDs with 15 provisional, 26 targetless-unresolved, and 16 correction flags.
  Root verified every frozen input hash and byte count and directly checked
  M0049, M0112 and M0239. A summary-count error was caught: 33 rows lack M-CSA
  handles, but only 32 have all source slots empty because row 49 has EC-based
  lookups. The agent was asked to correct the JSON summary before publication.
- The panel artifact covers exactly 40 candidate IDs: 34 transcription-only
  and six targeted checks. It recommends priority holds for three proposed
  inclusions (M0064/M0106/M0107) and retains three existing exclusions
  (M0212/M0753/M0970). It does not assert that all 40 mechanisms were deeply
  reviewed or that any new mechanism was admitted.
- The consolidated report groups remaining human decisions around named
  relation targets, generic state representation, and exact source scope.
  This keeps computational correction work moving while preserving the
  missing independent annotation boundary.
- The APX correction raised the canonical claim count from 16 to 17. Root
  updated the required-claim gate and its existing regression expectation;
  all 117 core/unit tests pass on Python 3.12 after that change. CI now checks
  the diagnostic evidence namespace and the new review document/JSON paths.

### Scientific review publication checkpoint

Final crosswalk triage is 15 provisional, 26 unresolved and 16 correction
flags; the cobalamin relation remains unresolved rather than asserting an
unsupported classification change. Root checked count parity and source-slot
counts after the final refinement. Both agents have completed their files.

All repository contracts pass with 17 canonical claims. The 117 core/unit
tests pass. Root verified all frozen Atlas-3/10 and Atlas-50 Phase A/B data,
protected registries, and exposure-ledger bytes unchanged from `a459ec78`.
The review overlay's receipt accounting and exact row coverage pass, and
`git diff --check` is clean. The report archive index is regenerated from the
staged board and historical correction banners. Root will push this tested
checkpoint to the existing PR #31 and check CI at its new commit separately.
