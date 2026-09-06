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

## Impact-driven atlas development

The owner explicitly directed optimizing each next action for progress toward
an open, computable mechanism atlas. A demonstration or benchmark is not a
prerequisite unless it resolves a decision that affects that goal. Do not
spend a sprint proving progress for its own sake. Review priorities whenever
the binding bottleneck changes. This supersedes the conversational suggestion
to make an enzyme-decision showcase the immediate next milestone.

Current branch: `codex/atlas-source-drafts`, based on PR #32 merged at
`3c3ef59775b5e347b90415b0f4aa953c94a9437c` after all four CI jobs passed.
The selected bottleneck is the gap between reviewed chemistry and usable records.

| Agent | Ownership in this batch | Work |
| --- | --- | --- |
| root | architecture choice, compiler integration, query/package, current docs, board | turn allowed source chemistry into usable atlas drafts |
| state_contracts | generic v4 schema/compiler and focused tests | preserve source proposals and positive typed state fields |
| source_ingestion | bounded official-source importer, snapshots, manifest, tests | preserve receipt evidence and source uncertainty; check scientific fidelity |
| draft_integration_review | read-only query and release integration review | check material omissions and package isolation |

No new evidence claim follows from the priority change. Existing source scope,
HisF role conflict, carrier-identity gaps and nitrogenase uncertainty remain
part of the chemistry we must represent. The intended output is a reusable
source-to-draft path, not another review-administration layer.

### Implementation and challenge results

- Official-source acquisition retrieved four entries and 48 linked MRV schemes
  using 49 requests and 1,109,896 bytes. All responses were HTTP 200; inputs
  are snapshotted with attribution, response receipts, and content hashes.
- One generic compiler produces four Tier-1 v4 records, with five source
  proposals, 43 reaction steps, five terminal states and 148 source arrow
  annotations. The fixed and cycling assemblies, unknown carrier owner/site,
  incomplete nitrogenase pathway and HisF role conflict remain explicit.
- The compiler selects from manifest and gate data rather than branching by
  enzyme family. Offline rebuilds check source completeness and preserve
  inferred steps and alternatives. It makes no balanced-reaction, exact-instance
  or Tier-2 claim.
- Root added package assets and an offline CLI. Review caught omitted residue
  evidence in compact results and missing batch scope in empty results. Both
  were corrected and the reviewer confirmed closure; five query tests pass.
- The inherited Atlas-3/10, July Phase A/B, state probe, adjudications and
  crosswalk v2 remain unchanged. No independent review or biological result is
  inferred from these engineering checks.
- Full-suite integration initially caught the new assets inside the frozen
  Atlas-10 package directory. Root relocated them to `draft_data` and added
  that directory to the wheel package list; the inherited directory stays
  byte-identical. The subsequent core run and repository contracts passed.
- Source-fidelity review confirmed exact scopes, alternatives and step text,
  then identified that absence of the word "inferred" was encoded as false.
  The successor record now uses null (unspecified) when the source provides no
  explicit tag. Its validator rejects guessed false values, and a regression
  test checks nitrogenase uncertainty and explicitly inferred return steps.
- The built wheel queries the four drafts from an empty directory with network
  connections blocked. Its existing Atlas-10 query still returns 10 cases,
  30 objects and runtime hash
  `57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.

### Final local checkpoint

After the inference correction, the full core tier runs 166 tests: 165 pass,
with one optional JSON Schema test skipped in the Python 3.12 build environment.
The compiler agent's schema-enabled run passes all nine focused tests. The
rebuilt wheel again passes the network-blocked draft query and unchanged
Atlas-10 result check. Sixteen frozen/registry/exposure scopes are unchanged
from merged PR #32. Root will publish this checkpoint and report exact-head CI
and merge status separately.

## Structured chemical queries

PR #33 merged at `fdfd2cd65291b5934bff6ad9f062893f847f28e0` after all
four Linux/Windows Python 3.10/3.12 jobs passed. The owner asked to continue
without waiting. Current branch: `codex/atlas-chemical-queries`.

The next bottleneck is retrieval: v4 already holds 26 source participant rows
with ChEBI identifiers, but its query supports only record ID, assembly and
free text. Implement exact participant-ID and source-side queries using those
fields, preserving scope and evidence in every result. Source left/right is
the drawn reaction direction, not physiological direction or proven turnover.

| Agent | Ownership | Deliverable |
| --- | --- | --- |
| root | query/CLI integration, release verification, docs, board | useful chemical filtering in the installed offline command |
| state_contracts | generic participant index module and its focused tests | deterministic relational materialization and exact multi-participant matching |
| source_ingestion | read-only chemical-query semantic review | source-backed expectations and specific overclaim risks |
| draft_integration_review | query/CLI regression tests; subsequent read-only integration review | compositional filters and evidence-preserving results |

All work uses the existing compiled package. No new source acquisition, schema
migration, source-record rewrite or registry change is required for retrieval.

The implementation indexes the existing 26 participant rows in two in-memory
SQLite tables and adds repeatable CLI filters with same-record AND semantics.
Source review verified every participant projection against its raw source and
checked CO2, ammonium side/count differences and water/ammonium conjunctions.
Both CODH alternatives and all uncertainty remain attached to record results.
The separate code review found no material integration defect. All 21
focused index/query/CLI tests pass. The full core run has 182 tests: 181 pass
and the existing optional schema check skips in Python 3.12. Repository
contracts and offline rebuilds pass. The installed wheel returns correct
same-record ammonium/HisF and cross-record CO2 results with network connections
blocked; the inherited Atlas-10 runtime hash is unchanged. All source snapshots,
compiled records, schema files and scientific gates remain unchanged from PR #33.

## Aldolase and transketolase source coverage

PR #34 merged at `7d19f5e64aad9eb53636cec51a4c8b90e7e0238c` after all four
CI jobs passed. Work continues on `codex/atlas-aldolase-transketolase`.

The selected batch is M0052 Class II aldolase, M0222 Class I aldolase, and
M0219 transketolase. The aldolases share source reaction participants but
different catalytic chemistry; transketolase adds distinct ThDP proposals.
A versioned successor review set inherits the earlier six cases and adds the
three declared cases. Default legacy checks remain strict, while batch paths
and declared case IDs replace the fixed-six limitation for successors.

- Root owns final adjudication/bindings, compiler/build and package/query
  integration, verification and publication.
- state_contracts owns batch paths, generic probe/gate support, focused tests
  and the nine-case successor probe/spec.
- source_ingestion owns the batch-aware importer and three source snapshots,
  manifest, attribution and receipt reuse.
- draft_integration_review owns the evidence-linked source challenge, informed
  by raw API/MRV files and root's specific M0222/M0052 leads.

Source inspection fetched three official entries and all 30 linked schemes:
31 requests, 569,327 bytes, all present and parsed. Root additionally inspected
the three official entry pages; their download bytes are not fabricated in
the raw-source receipt ledger. No old acquisition receipt is relabeled as new.

Challenge found M0222 step-1 text/drawing substrate disagreement and mixed
rabbit/archaeal applicability. M0219 has proposal-specific reaction/protein
contexts and unresolved native metal; ThDP covalent chemistry does not imply a
redox transition. M0052 retains an explicitly inferred step and extraenzymatic
cyclization. These remain scope limits and abstentions in the new records.

Final successor adjudications preserve the earlier six cases exactly and bind
all seven reviewed input files. The new source package compiles to three
Tier-1 records, four distinct proposals, 26 nonterminal steps, four terminal
states and 98 source arrows. Default batch selection remains the original
four records; the new named batch selects only its three newly declared cases.
Compact and full chemical queries preserve the explicit source conflicts.

Verification before publication: 19 focused source/batch/query tests passed;
the initial full core suite ran 196 tests (195 passed, one optional jsonschema skip).
The built wheel queries both batches from a fresh directory with network
connections blocked, including the two aldolases under shared participants.
Atlas-10 still has ten cases/30 typed objects and runtime hash
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
All 135 checked baseline atlas data/package files and the exposure ledger are
byte-identical to PR #34's merge. No independent, human, experimental, Tier-2,
or exact-reaction validation was added.

The separate-agent compiled-source inspection found no material defect:
entry/proposal contexts, source residue mappings, inference and evidence status,
and all mandatory abstentions survive packaged compact/full queries. A software
review found two gaps now corrected: explicit annotation selection cannot claim a
mechanism-draft operation, and live redirected responses are rejected before
their body is read or attributed. New regressions also reject reordered capture
ledgers. The receipt flag now correctly reports that complete raw API responses
are not committed; parsed entries and all linked diagrams are retained in source
wrappers. Root reviewed this exact metadata correction, updated its pins, and
rebuilt the successor package offline without changing source snapshot bytes.
Source research is checking whether
primary M0222 papers can resolve the substrate and protein-context conflicts
at a narrower scope. Repository contracts passed before the final narrow corrections; final checks and remote CI follow.

Final rerun after corrections: 199 core tests (198 passed, one optional skip),
repository contracts, both source batches and installed-wheel network-blocked
queries all passed. The next evidence-led task has a concrete lead: primary
rabbit aldolase structures support a DHAP-derived Lys229 covalent intermediate
(P00883 UniProt Lys230), while archaeal Tyr146/Lys177 work must remain separate.
That can support a narrower cited correction, without treating an entire source
proposal or detailed attack trajectory as experimentally established.

## Primary-evidence correction after the additional batch

PR #35 merged at `d4b4244c81343da2beaa8ad49b68f78d145849a0` after all four
Linux/Windows Python 3.10/3.12 jobs passed (Actions 34001622124). Its feature
commit is `5b499989ab5b647c64f73fe3affe05960b6f1efa`. Work continues on
`codex/atlas-primary-evidence`, initially based on that feature commit.

The highest-impact next step is resolving a source ambiguity with primary
structure evidence. Source ingestion inspected the underlying publications,
PDB records and numbering. A separate same-model challenge confirmed the narrow
result and caught a chemical-state trap: the bound DHAP-derived adduct must not
be equated with the free ChEBI species. 1J4E is an engineered, NaBH4-reduced trap,
not a direct observation of the native Schiff base. Its legacy sequence mapping
is not used; 2QUT maps author Lys229 to P00883 Lys230.

- Root owns final scientific adjudication/annotation, build/CLI/package wiring,
  documentation, verification and publication.
- state_contracts owns the generic optional annotation validator, query support
  and tests. It must preserve default v1 query results and immutable source
  records, reject stale review/source pins and forbid scope/tier promotion.
- source_ingestion owns the minimal 2QUT raw audit package and field projection,
  with truthful inventory, exact hash and attribution.
- draft_integration_review challenges the precise final annotation against
  primary evidence, including trapping chemistry, numbering and bound-species
  limits. These roles remain informed, same-model and statistically correlated.

The annotation retains source Step 1/7 prose-versus-scheme conflicts, supplies a
rabbit-site DHAP-derived covalent-moiety observation and sourced numbering, and
keeps whole-step trajectory, exact bound species, and full-proposal applicability
unasserted. One additive query annotation does not count as another mechanism,
reaction, Tier-2 case, project experiment or independent validation. The whole
2QUT CIF remains in the audit package; its original download lacks an HTTP
receipt, explicitly disclosed rather than reconstructed as a new acquisition.

Final source challenge narrowed two phrases: the captured adduct provides
structural counterevidence to Step 1's G3P wording, and resolves its deposited
DHAP parent-moiety designation rather than an exact bound chemical species.
The field projection now explicitly retains unknown bond order and protonation.
Root applied the precise reviewed changes and repinned the final payload to
`a7ec87ea2f5446e592c9288764069f49d95f9ff0f1dca056607272eb6076ec8c`.

A cross-check confirmed the actual raw hash, Lys229-to-Lys230 mapping, bound-state
limits and evidence roles. The generic validator does not rederive arbitrary
scientific prose or mappings from coordinates; an editor who recomputes the
manual review pin must repeat source-to-claim review. Its source-digest checks
establish integrity, not scientific truth. No additional semantic adjudication
engine is represented as implemented.

Final verification: 16 focused primary-evidence tests passed. The full core run
has 215 tests (214 passed, one optional jsonschema skip); repository contracts
and installed-wheel queries with networking blocked passed. The wheel excludes
raw CIF files, retains the source tier and all original abstentions, returns
the author/canonical residue mapping, and includes identical annotations in
compact/full query results. All 149 checked existing scientific files remain
byte-identical; only the additional package expectation gains the annotation
asset hash. The complete source records, snapshots and reviewed scope decisions
remain unchanged. Remote CI and publication follow this verified local state.

## Transketolase proposal-specific protein context

PR #36 merged at `cf26dfd4b530b463fc36bbb0e0c0777fd1c84d4f` after all four
Linux/Windows Python 3.10/3.12 jobs passed (Actions 34002531313). Its feature
commit is `f66c288f1b78be466c5b1746f58e25147db3a599`. The current branch,
`codex/transketolase-protein-context`, starts from that clean main revision.

The next decision-relevant question is whether M0219 proposal 2's cited human
model supplies an exact protein/site context despite blank source UniProt rows.
Proposal 1's yeast evidence must remain separate. Root owns adjudication,
the annotation sidecar, documentation, release checks and publication.
source_ingestion owns the minimal official structure/article audit package in
`review/transketolase_sources`. state_contracts owns the typed proposal/context
validator and focused regressions. draft_integration_review challenges the
source-to-claim mapping and then the final annotation. All agents use the same
model; their review is informed and correlated, not independent human review.

Primary-paper methods explicitly name human 4KXV and His258A/Lys244A. Its
protonation choices and proposed catalytic roles come from modeling and
cross-species experimental motivation. The current PDB entry has 637 deposited
polymer residues and a post-publication atomic-model revision, so author versus
entity numbering and the distinction between current mapping and the paper's
exact coordinate input require explicit checking before annotation.

The checks resolve that numbering question: the 14-residue expression tag is
at the C terminus (positions 624-637), so author and canonical positions 244
and 258 agree. Archived 4KXV v1.3 and current v2.1 both support the same
P29401 mapping. The cited 2020 paper explicitly names 4KXV and the chain-A
sites; it predicts protonation and computes catalytic roles. The annotation
therefore binds proposal 2's model-template identity and these two sites,
without promoting whole-mechanism applicability or transferring yeast evidence.

The separate challenge also distinguished chemical identifiers from drawings:
proposal 2's sugar-derived components have carbon counts consistent with its
X5P/E4P-to-G3P/F6P prose, while all six MRVs retain CHEBI:57483 labels. The
annotation states this narrower finding and preserves exact structures,
stereochemistry, speciation and reaction-equivalence abstentions. Root accepted
the reviewer's wording correction that the paper *cites prior* yeast experiments.

The successor annotation schema preserves the M0222 row exactly, adds typed
primary-source/projection bindings, and checks the compiled proposal/reference
and the projected protein/site tuple. At build time it compares the annotation
with the bound project extraction and checks raw-file hashes; installed queries
validate the packaged declarations and review pin without raw-source access.
These checks do not independently rederive arbitrary scientific claims from
coordinates or replace source-to-claim review. The same-model review remains
explicitly correlated and non-human.

Final scientific payload is pinned to
`575b0772268a6dd2b6e733d8e811eb9956c991fea6f88d0b167504594a4b2eb6`.
The projection pin is
`54d0bfeefc1ba24cf4020ec75380cc60b74a91f2b78016b32868daf92c098f64`.
The acquisition inventory distinguishes enumerated package requests from
unrecorded discovery/page-view traffic and discloses the reused article's
missing original HTTP receipt.

Local verification passed: 34 focused query/annotation tests, the full core
suite (221 tests: 220 passed, one optional jsonschema skip), repository
contracts, and fresh-directory installed-wheel queries with networking
blocked. Compact/full queries retain identical proposal context and keep
the source evidence tier at 1. The Atlas-10 runtime hash is unchanged, and
153 checked baseline scientific files are byte-identical to the PR #36 merge.
The inherited M0222 annotation and its original source bindings are unchanged.
Publication and remote CI follow this locally verified state.

## Proposal-component search across reviewed batches

PR #37 merged at `b92effb25bd4e9534de86fe51ebb8aa037c9b34b` after all four
Linux/Windows Python 3.10/3.12 jobs passed (Actions 34005760585). Its feature
commit is `44525f3965c0f294846241554312dbc526eb9a97`. The clean main revision
is the base of `codex/mechanism-component-search`.

The next bottleneck is using the existing source chemistry across batches.
Both the source challenge and engineering assessment favored exact
proposal-component retrieval over another isolated annotation or more equally
hard-to-search records. All seven drafts already preserve a source event
vocabulary in nine proposal summaries. This change makes that vocabulary
queryable; it adds no scientific coverage or validation claim.

- Root owns the batch catalog, CLI, integration/release checks, documentation
  and publication.
- state_contracts owns exact label matching, proposal-level query witnesses
  and focused regressions.
- draft_integration_review checks the implementation in a separate pass and
  remains a same-model, informed, correlated reviewer; it challenges false
  joins, source scopes and interpretation of the shared Schiff-base label.
- source_ingestion ran a bounded read-only HisF literature probe to assess
  whether another isolated correction would be more consequential. No source
  package, query annotation, or adjudication was changed from that probe.

Repeated component filters are ANDed within one proposal. M0107 proposal 2
contains decoordination while proposal 3 contains decarboxylation: their
conjunction correctly returns zero. Matching records retain all alternatives,
abstentions, primary annotations, and exact proposal/raw-summary witnesses.
The cross-batch Schiff-base query returns HisF M0753 and class I aldolase
M0222; it does not imply an enzyme-attached intermediate in both. Event labels
remain source taxonomy rather than atom-mapped edits or validated mechanisms.

`--batch all` dispatches separate queries with original batch selection and
review metadata, including empty results. It creates no merged scientific
bundle. The original default stays four records, and unused component filters
preserve v1/v2 query output. Event-filter responses use v3. Source participant
filters remain entry-level and do not ground matched proposals or steps.

The HisF probe found a concrete follow-up lead in Beismann-Driemeyer and
Sterner (2001), DOI 10.1074/jbc.M102012200 / PMID 11264293: the proposed
Step-5 acid/base assignments align with the M-CSA step description, while the
overall residue descriptions appear transposed. Precise roles remain proposals.
The publisher page/PDF was not directly captured; indexed primary-paper text
supplied the lead. Retain the current abstention until a source-to-claim review
and preserved evidence support a scoped correction; do not report this probe
as a new verified annotation.

The separate implementation challenge found no material issue. Focused checks
confirm proposal-local conjunction, exact label normalization, preserved batch
provenance and primary annotations, and unchanged legacy response structures.

Final local verification: 234 core tests ran (233 passed, one optional
jsonschema skip); repository contracts passed against the PR #37 merge base;
the built wheel passed fresh-directory Atlas-10 and source-draft queries with
networking blocked. All 167 checked baseline scientific files are byte-identical
to that merge. The original Atlas-10 runtime hash and all source/annotation
payloads remain unchanged. Remote CI and publication follow this verified state.
