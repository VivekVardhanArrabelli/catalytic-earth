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

## Owner-authorized computational development track

The owner explicitly authorized proceeding and urgently replacing the human
review dependency for development. PR #31 was merged at `5e917f3b`; the next
work runs on `codex/atlas50-computational-gate`. The July human-review contract
stays intact as a historical validation commitment. A new versioned policy
will permit source-scoped draft work through evidence and challenge checks;
it will not fabricate people, independent validation, gold labels, or assays.

| Agent | Current ownership | Required result |
| --- | --- | --- |
| root | computational development gate, current policy, integration, this board | executable bounded permissions and adjudications, tests, release checks |
| crosswalk_v2 | successor generator, crosswalk_v2 data/report/tests | 57 corrected rows with named relation targets and old/new change map |
| state_contracts | shared state probe, six-case data/report/tests | concrete PASS/SCOPED_PASS/ABSTAIN at exact source scope |
| forward_path | source challenge JSON/report | challenge prior holds and corrections using primary evidence |

A fresh challenge-agent spawn hit the tool's thread limit, so the existing
forward_path agent is reused and explicitly reports prior exposure. No blind
or statistically independent panel is claimed. Distinct roles and contexts
help find objections; source evidence, not vote count, decides their resolution.

Early challenge results already narrow blanket holds: M0049 is invalid PLP
evidence but remains a pyruvoyl panel candidate; HisF with free ammonium is a
legitimate scoped alternative to a full coupled synthase claim; a permanent
CODH heterotrimer may be distinguishable from ATP-coupled transient nitrogenase
association. E2 accession presence must not be mistaken for lipoyl-carrier
structure coverage. These points are sent directly to the implementation agents.

### Review resolutions and integration

- Crosswalk v2 is final: 57 rows, 23 computational-provisional and 34
  unresolved, with named targets, source applicability, and an old/new map.
  Source challenge corrected our first DHFR review: the actual EC 1.5.1.3
  reaction-core admission contract supports the one M0112 exact relation.
  The earlier broad/bifunctional aggregation rationale is superseded. Water
  remains the proton donor; Asp26/Asp27 has a network role.
- The shared six-case state probe is final. M0106/M0107/M0212/M0753 permit
  source-scoped mechanism drafts; M0064/M0970 permit source annotation only.
  The typed sidecar does not compile a new v3 kernel mechanism. M0106 retains
  the E2 binding-domain versus lipoyl-domain distinction. M0753 is HisF only.
- Source challenge reviewed final crosswalk/state bytes and preserved the
  M0970 polymer-state objection. Root created six evidence-linked
  adjudications, kept all probe abstentions and blocked exact reaction
  instances in every case. Topoisomerase and polymer work remain annotation
  only; useful work on the other four cases can advance.
- Root updated current policy and CE-012 wording to replace the human-only
  draft-development dependency under the owner's explicit instruction.
  Frozen July packet completion, independent annotation, and protected
  registry admission retain their distinct meanings. Source checks are
  bounded to public primary sources, 100 requests and 30 MiB per batch.
- The crosswalk agent is hardening the executable development gate against
  real structured abstentions and attempted permission promotion. Its nested
  read-only shape audit found the initial root implementation's list-of-dicts
  bug before publication. The state agent integrated all three deterministic
  builders into the existing repository/CI contract runner.
- Updated documentation points to the successor review and labels old
  computational judgments as history. Rosalind Workbench is installed, but
  no GPT-Rosalind scientific model run or account entitlement is claimed.
  No private correspondence or reviewer endorsement is included.

Publication checkpoint: targeted crosswalk/state checks pass (18 tests).
Root is completing gate tests, full repository contracts, frozen-byte checks,
and cross-platform CI before landing this development checkpoint.

### Local release checks

Root's direct M0753 source check found reversed Asp11/Asp130 role assignments
between the overall residue-role table and summary/Step 5. The adjudication
adds `resolved_aspartate_roles` as a mandatory abstention. The probe makes no
resolved residue-role assignment, so its scoped state permissions remain valid.

The final gate binds adjudications and transitive reviewed inputs, preserves
structured abstentions, checks source evidence/scope and material objections,
and rejects scientific or independence promotion. All 147 core/unit tests pass
on Python 3.12, including 12 gate adversarial tests. The three deterministic
builders and repository-wide contracts pass. Root's comparison against merged
PR #31 (`5e917f3b79b0237eafc1523aa6ab6d35b40cd2ef`) confirms unchanged Atlas-3/10,
July Phase A/B, protected registries, expansion freeze and exposure ledgers.

The new checkpoint is ready to publish. Cross-platform CI and merge status
will be reported separately from these local results.
