# Evidence-bound mechanism steps: internal message board

## Goal and completion boundary

The user requested sustained autonomous work while asleep, with parallel agents
and priority determined by scientific impact. The active goal in the current
chat is to deliver an offline-queryable mechanism-step evidence layer, then
validate its generality and ship it through green CI. Starting main is
`592b1f02d2fd47017ccd3ce1decc914db629a680` (PR #39). Work branch:
`codex/step-evidence-context`.

Success means a user can retrieve an exact source step and understand what
evidence supports its context, what was merely inferred or assumed, and which
identities or roles remain unresolved. Every assertion needs a source locator
and scope. More rows, agreement between agents, or a new schema alone do not
meet the goal. Atom maps, bond changes, exact reaction instances and complete
observed trajectories must remain unasserted without direct evidence.

The current session permits root plus three concurrent agents. Reuse these
agents in successive independent work packages. An hourly continuation in this
same chat is scheduled for twelve runs; it must coordinate with active work,
not start duplicate writers. Keep this board sufficient to resume after a
context reset. Root owns this file.

## Milestones and decisive questions

1. Verify M0049's processed-chain pyruvoyl context against versioned 1PYA and
   protein evidence. Preserve precursor, processed-chain and legacy numbering.
   Determine the strongest directly supportable PLP comparator contexts.
2. Implement one generic additive step-evidence representation. Bind record,
   proposal, source step and scheme hash; distinguish primary observations from
   source-only assertions. Populate the complete four-record PLP/pyruvoyl batch
   with witnessed contexts or explicit unresolved values.
3. Prove useful retrieval: PLP versus pyruvoyl at the actual supported scope;
   M0186's extra-enzymatic Steps 6/7; precisely scoped inferred/assumed roles;
   direction-qualified M0213 roles if supported; unresolved M0049/M0066/M0213
   chemical identity conflicts. A record-level context must not become a
   step-level observation simply because the step is attached to that record.
4. Test generality against the existing aldolase/transketolase primary
   annotations. Preserve their source pins and existing query behavior. Ship
   compact/full/empty and installed-wheel offline results with their witnesses,
   appropriate tests, documentation, repository checks, and green CI on main.

Reassess after each milestone. Acquire additional sources only when they can
change a selected claim or decision. A failed evidence search yields a bounded
abstention and a pivot to another useful work package, not endless retries.

## Ownership and live handoffs

| Agent | Owned paths/work | Next handoff |
| --- | --- | --- |
| Root | Shared CLI/catalog integration, durable sidecars, docs, this board, Git/CI/publication | Integrate only reviewed evidence and implementation |
| source_ingestion | `/tmp/catalytic-step-evidence-m0049-20260906/`; public 1PYA captures and proposed primary annotation | Exact source bytes, locators, hashes, request ledger and limitations |
| state_contracts | New `atlas_step_evidence.py` and `test_atlas_step_evidence.py`; generic additive validation/query module | Data shape first, then negative tests and implementation |
| draft_integration_review | `/tmp/catalytic-step-evidence-review-20260906/`; four-record scientific context inventory and adversarial review | Direct witnesses, objections, scoped review verdict |

Agents message one another when a dependency is ready. They share model and
prior context; this is correlated computational review, not statistically
independent expert or human review. No agent commits shared work; root handles
integration and publication.

## Preserved boundaries and operating rules

- Atlas10, its runtime hash, the 702 frozen benchmark labels/scores, and all
  existing raw/compiled source bundles remain unchanged.
- No benchmark rescoring, registry promotion, exact-reaction admission,
  completed human review or experimental validation is implied.
- Public primary-source acquisition stays within 100 requests / 30 MiB per
  batch with truthful receipts. No paid services, GPU work, outreach or lab work.
- Do not infer a cofactor's involvement in every step from the record's family.
  Do not infer native bound chemistry from an analogue or engineered trap.
- Current source conflicts remain visible; projection and hash checks validate
  provenance and declared scope, not arbitrary scientific truth.
- After staging final changes under `work/`, rebuild and stage the report
  archive index from those exact Git-index blobs. Verify ordinary and
  partial-clone index checks before commit. A later board edit repeats this
  sequence. Never exclude this board to bypass the archive contract.

## Execution log

- 2026-09-06: All three agents independently compared possible next actions.
  The integration reviewer favored typed step retrieval over more coverage;
  the contract reviewer identified exact step/proposal/source binding as the
  reusable gap; the source reviewer selected M0049 processed-chain context as
  the strongest immediate positive evidence target. Root combined these into
  the staged goal above and activated all three implementation/review lanes.
- Goal created in this chat with no artificial token budget. Existing Catalytic
  automations were all paused and addressed older work. A distinct, bounded
  continuation schedule was created for this goal rather than reviving them.
- The first implementation is an additive step sidecar, with opt-in CLI
  filters. All clauses must match one source step; an existing proposal-level
  component filter must match that same proposal. Native/analogue state stays
  unresolved until an appropriately typed primary-state projection exists.
  Verbatim roles remain source labels, with their source-order direction.
- Chemical review produced the complete 32-step batch: 18 steps explicitly
  mention PLP, three pyruvoyl, and one PMP. These are literal text witnesses,
  not cofactor-state assignments. M0186 Steps 6/7 alone have explicit
  outside-active-site wording. M0049 Step 7 is a whole-step inference;
  M0186 Steps 4/5 qualify a particular inferred/assumed role. All source
  identity conflicts and arrow-label distinctions are retained.
- Root reviewed the candidate and changed only its set ID from candidate-v1
  to v1. Reviewer confirmed the durable annotations were otherwise unchanged.
  The initial integrated step payload was
  `21ee9b52cb79f5c43c4426a0365bd9faafa914e65632b69af528e77dc66f4b9c`;
  its repository and packaged bytes had SHA
  `aeb26047034a94f1434d1403f01c8f554dfc14651da983ac5c82fdc905f2abb9`.
- The source audit found a consequential 1PYA numbering distinction: chain F
  processed label position 1 is PYR at PDB author residue 82. UniProt P00862
  annotates precursor Ser83 as pyruvic acid. The deposited standard-residue
  alignment starts at label 2 and cannot independently map modified label 1.
  Current and historical v1.3 coordinate rows preserve the same processed
  state; twelve PYR atom-name rows changed across the later revision. The
  record-only structure observation will retain author82/label1, with the
  canonical crosswalk separately qualified until curated protein evidence can
  be represented honestly in the typed annotation.
- The scientific reviewer narrowed one literature statement: PMID6698997's
  abstract identifies a Ser81/Ser82 cleavage bond; it does not by itself assign
  which serine becomes pyruvoyl. The source agent is incorporating that
  correction before the primary package's final review pin.
- Initial integration ran 260 core tests (one optional dependency skip).
  Subsequent tests add M0107 same-record/different-proposal rejection and
  M0219 proposal-level versus M0222 record-level primary-link scope. All
  nineteen focused step tests pass. Fifteen legacy query comparisons matched
  the starting code when given the same source and primary sidecars.
- Implementation review found and root fixed a malformed-empty-filter bypass
  and unhelpful CLI error handling. Filter normalization now runs even for an
  absent sidecar, and invalid CLI labels fail during argument parsing.
- Final scientific review found that selected role fragments lost M0186
  Step 3's conditional concerted model and water-identity qualification in
  compact output. Root added that specific limitation and made compact/full
  queries retain complete step summaries and separately scoped proposal text.
  A second correction attributes Ser83 to the bound M-CSA table in the step
  sidecar, leaving current UniProt evidence in the separate primary audit.
  The revised reviewed step payload is
  `4993aaafa12ad4473a55367dca3c1f2d946d1a717629aebc6c37de76c1f13385`.
- The primary package passed final source-to-claim review and validation. Its
  reviewed payload is
  `943b22251864d442868ef1059da8422706a09c8e87f1fd423c514e3a49093c1f`.
  It retains current/historical CIF and UniProt bytes plus a scoped projection,
  attribution, inventory and the nine-request acquisition ledger (eight HTTP
  200 responses, 1,351,490 bytes). PubMed and RCSB API bodies remain local-only
  with explicitly null repository paths; bibliography and capture hashes are
  retained. No full publisher article was acquired.
- Final build regenerated both sidecars and package pins. Reviewer confirmed
  exact repository/wheel-asset equality and no remaining material objection.
  Root ran 263 core tests (262 passed, one optional dependency skip), including
  twenty focused step tests, and verified an installed wheel from an empty
  directory with networking blocked. Atlas10's runtime SHA remains
  `57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
  All pre-existing source bundles and Atlas objects are unchanged; the PLP
  package metadata adds the new sidecar hashes. The architecture inventory
  updates the CLI hash and adds fifteen new repository paths. Git-index
  report-archive checks and remote CI are the final publication steps.

## Resume after this increment

The active goal remains incomplete after shipping this first increment. The
next useful deliverable is typed record-only primary observed-state context,
with evidence for each mapping kept distinct. A v3 projection must distinguish
the directly observed PDB author/label site from a cross-source curated
canonical correspondence. UniProt can support curated identity; it cannot
stand in for primary structural evidence. Existing primary v1/v2 annotations
remain unchanged, and a record-context query must report that it does not
ground a matching source step.

- `state_contracts` captured M0213/1L6G in
  `/tmp/catalytic-step-evidence-m0213-20260906/`: six HTTP-200 requests,
  738,363 bytes. PDD is a source-designated analogue. No deposited PDD
  `_struct_conn` row exists; the aggregate four covalent rows concern peptide
  connections and cannot imply PDD-protein attachment. Preserve author
  residue 1390 versus nonpolymer source-author 390 for the second instance.
- The same agent is preparing an isolated v3 implementation prototype under
  `/tmp/catalytic-primary-v3-implementation-20260906/`, with no current-branch
  edits. Integrate it only after the first increment is shipped and reviewed.
- `source_ingestion` is probing M0186/1PWH under
  `/tmp/catalytic-step-evidence-m0186-20260906/`, bounded to ten requests and
  5 MiB. Await its exact analogue/connectivity/protein-context findings.
- `draft_integration_review` requires edge-level falsification: reject
  standard-alignment-only mapping of modified PYR, global-count-as-ligand-bond
  inference, analogue classification without explicit primary support, and
  any propagation of a record-level observation into step/role/protonation or
  trajectory validation. A flat tuple equality check is insufficient.
