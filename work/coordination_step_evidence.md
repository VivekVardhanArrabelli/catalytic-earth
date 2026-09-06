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
| Root | CLI/query/catalog, package builder/assets, query tests, docs, this board, Git/CI/publication | Integrate reviewed evidence and implementation |
| source_ingestion | PLP primary sidecar and new `review/primary_sources/observed_state_v3/` only | Populate M0049/M0213/M0186 from captured sources; preserve old annotation and source bytes |
| state_contracts | `atlas_primary_evidence.py` and new `test_atlas_primary_observed_state.py` only | Generic v3 types, edge validation and portable falsification fixtures |
| draft_integration_review | Read-only scientific/source and integration challenge | Direct witnesses, objections, scoped review verdict |

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

PR #40 merged on 2026-09-06 at 06:39:55 UTC after all four Ubuntu/Windows
Python 3.10/3.12 jobs passed in Actions run `34016730558`. Scientific commit
`75d9c0ac1436a89bf64542d975dbb017737113db` and merge commit
`0e77f11a76fd9565fad6671298154caf701024ce` have identical trees. Local main
was clean and matched origin/main. The next goal milestone starts from that
merge on `codex/primary-observed-state-context`; the goal remains active.

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
  `/tmp/catalytic-primary-v3-implementation-20260906/`. After PR #40 merged,
  root authorized the disjoint validator/test edits listed above.
- `source_ingestion` is probing M0186/1PWH under
  `/tmp/catalytic-step-evidence-m0186-20260906/`, bounded to ten requests and
  5 MiB. It captured nine requests / 1,122,086 bytes (eight HTTP 200; ACS 403)
  without full publisher text. The primary abstract reports PLP-OMS aldimine
  and no subsequent dehydration; the deposited PLV dictionary has a single
  N-C4A bond. Retain that unresolved paper/deposit distinction. The inspected
  abstract does not explicitly designate an analogue, so represent a
  source-described bound adduct unless stronger evidence changes that scope.
- `draft_integration_review` requires edge-level falsification: reject
  standard-alignment-only mapping of modified PYR, global-count-as-ligand-bond
  inference, analogue classification without explicit primary support, and
  any propagation of a record-level observation into step/role/protonation or
  trajectory validation. A flat tuple equality check is insufficient.

## Second increment in progress

- Typed queries select a deposited state kind/component within one annotation.
  Combining with step filters joins at record scope only, with explicit
  `observed_state_grounds_step=false`. Legacy primary annotations remain
  available but are not automatically reclassified. Annotation counts are not
  independent observation counts.
- Root review rejected a case-specific validator rule that treated every
  bound adduct as a chemical disagreement; evidence and projection pins must
  retain this particular disagreement without defining all adducts that way.
  Unsupported state variants are being removed rather than exposed partially.
- Offline queries must include scoped projection edges and locators; hashes
  and dangling edge IDs alone cannot explain the mapping evidence. State and
  source agents are adding a factual excerpt mirrored against the bound
  repository projection. Raw structures and article bodies stay out of wheels.
- Independent source review caught a prototype error in 1PWH: four potassium
  instances are not its connection inventory. The mmCIF has 26 metal
  coordination rows and zero PLV connection rows. Correct both source edges
  and falsification fixtures before accepting the data package.
- After the second increment ships, the remaining useful generalization test
  is M0222's existing 2QUT DHAP-derived covalent intermediate. Preserving its
  v1 annotation prevents regression but does not yet permit a typed comparison
  with the PLP analogue and processed cofactor. `state_contracts` will inspect
  already retained 2QUT sources without network or branch edits, then propose
  the minimum validated covalent-attachment extension. Do not force that case
  into an unimplemented enum or expand the current PR before review. M0219's
  computational template context remains the negative control. M0186's
  unresolved chemistry needs primary clarification, not additional flags.
- Final source review accepted the four-annotation sidecar (three new typed
  contexts plus the untouched M0049 v1 annotation). Reviewed payload:
  `e14123f3f7757904124d4f85c21a83a8240f6177898abd2ed57c0097e28e7ad2`;
  repository and packaged file SHA:
  `a55b55d56791612dc9d76773f0a8eed6341bf7d23f729ffab7ba6e8f71d7162c`.
  M0186/M0213 now carry publication-era versus current-capture limits in
  offline annotations. Source requests remained bounded (six/738,363 bytes
  for M0213; nine/1,122,086 bytes for M0186); no full publisher text was acquired.
- Root review added a missing crosswalk invariant: the selected deposited
  site must agree with the M-CSA alias's PDB, author-chain and label position.
  Author residue numbers and label/author chain namespaces remain distinct.
  Retained source/projection pins cannot substitute for that structural join.
- The final core suite passed 288 tests with one optional dependency skip.
  Eighteen legacy query comparisons match the base for identical source inputs.
  The installed wheel passes from an empty directory with networking blocked,
  including exact observed-state filters, compact/full source witnesses,
  unresolved M0186 chemistry and record-only joins to Steps 6/7. Atlas10's
  runtime hash, all three source bundles, the 32-step sidecar, existing
  aldolase/transketolase primary sidecar and release manifest are unchanged.
  Repository contracts and four-platform CI remain before publication.
