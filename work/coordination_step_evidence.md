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
| source_ingestion | Aldolase/transketolase primary sidecar and new `review/primary_sources/observed_state_v3/` only | Add M0222 covalent context; preserve all old annotation objects and source files |
| state_contracts | `atlas_primary_evidence.py` and new `test_atlas_primary_covalent_state.py` only | Minimal covalent attachments, edge validation and portable falsification fixtures |
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
  Repository contracts and all four CI jobs remain before publication.
- PR #41 is open from scientific commit
  `c8d5e8e081994de291f3d0a008546f7b6606e608`. Initial CI run `34018644383`
  passed both Ubuntu jobs and failed the new synthetic fixtures on Windows:
  their helper hashed temporary JSON as raw CRLF bytes instead of using the
  repository's canonical text hash. Root changed only the fixture helper and
  added a regression that forces CRLF writes before source pins are computed.
  It reproduces all three positive-case failures with the old helper and
  passes with the fix; all twenty observed-state validator tests pass.
  Production code, reviewed evidence and package bytes are unchanged. The
  corrected CI run must pass before merging.

## Third increment in progress

PR #41 merged on 2026-09-06 at 07:31:10 UTC after all four jobs passed in
Actions run `34018987268`. Final head `87d1987c230bca6043d00ebf7e5c3ea64b35c320`
and merge `b30a8dfdd59274040d53b8710974d17c8df17786` have identical trees.
Main was clean and matched origin/main. Current branch:
`codex/covalent-observed-state-context`.

- The retained 2QUT audit supports four 13P instances and four exact
  Lys229 NZ–13P C2 covalent connections, with raw bond order `?`. All modeled
  instances omit O2 while the generic component dictionary has C2–O2 `doub`.
  Keep those scopes separate; neither supplies a normalized bound molecule.
- Root authorized two primary-source requests after the retained-source audit
  found an experimental-description gap: PMID17728250 XML and Europe PMC
  availability. Both returned HTTP 200, totaling 9,174 bytes. Europe PMC
  reported no OA/PMC/PDF copy; no article-body request was made. Ledger:
  `/tmp/catalytic-observed-m0222-20260906/receipts.json`, SHA
  `00cf1132fc611ddfe425eef31f97f4adcdf9ddf3ff51904dc79908548aae1c96`.
- The primary abstract compares native enzyme with Lys146Met and reports an
  enamine versus putative iminium. Preserve its construct wording without
  assigning every statement to every listed PDB entry or inferring that no
  reducing treatment occurred. The 2QUT title/remark provides the specific
  deposited enamine description. Current 2024 bytes are not publication-era
  bytes. Raw PubMed XML remains local; a factual projection may be retained.
- The new type adds only exact protein attachments and evidence for deposited
  description/connectivity/dictionary-versus-modeled atom inventory. Canonical
  Lys230 alignment stays in the existing v1 annotation and audit; it is deferred
  from the new typed attachments. M0219 remains an untyped computational
  negative control. Existing PLP v3 annotations and all old v1/v2 objects stay
  unchanged. Temp work is under `/tmp/catalytic-primary-covalent-v3-20260906/`
  and `/tmp/catalytic-observed-m0222-20260906/` until reviewed integration.
- A later high-impact check is deterministic comparison of declared mmCIF
  tuples to retained source rows. Existing private parsers are narrow and
  should not be imported from frozen large modules or advertised as complete
  mmCIF support. Evaluate a small build-time reader after the covalent
  comparison ships; additional records or normalization flags are lower value.
- Source and integration review accepted the materialized M0222 annotation,
  full projection and primary-abstract factual projection. Reviewed payload:
  `c6f0d2e76d3edf29f4f453b333536fa089a57e78d6ff1b944611b85a41cb71d4`.
  The typed row refines the same 2QUT observation as the unchanged v1 row;
  it is not independent experimental corroboration. The actual source/free
  identifier `CHEBI:57642` is a negative control for typed component matching.
- Root corrected two old tests that assumed exactly two annotations or their
  array positions. The final core suite ran 298 tests successfully, with one
  optional dependency skip. Installed-wheel queries passed from an empty
  directory with network connections blocked, including exact 13P retrieval,
  unknown attachment order, O2 omission and rejection of DHAP/ChEBI aliases.
  Atlas10 retained runtime SHA
  `57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
  Byte comparisons preserved 70 frozen/package input paths, both old primary
  annotation objects and the retained 2QUT mmCIF. CI remains before merge.
- The next bounded increment is a raw-source factual checker, prepared only
  in `/tmp/catalytic-primary-source-check-20260906/` while this change ships.
  `state_contracts` implements selected mmCIF checks at draft-build time;
  `draft_integration_review` challenges correlated edits with all JSON pins
  recomputed; `source_ingestion` independently extracted four-case raw
  expectations and is assessing remaining scientific gaps. M0049 selects
  chain F only, whereas the complete source contains three PYR instances;
  preserve that declared scope. Do not equate syntax/tuple verification with
  protein crosswalk, article interpretation or chemical validation.

## Fourth increment: rederive deposited facts

PR #42 merged on 2026-09-06 at 07:57:13 UTC after all four jobs passed in
Actions run `34020227412`. Scientific head
`9dea2dc608ddf47d88ff05378c402a7f13df9204` and merge
`e306cd1d82be0ca7cc1a8006878b492366893f1d` have identical trees. Main was
clean and matched origin/main. Current branch:
`codex/primary-structure-source-check`.

- `source_ingestion` independently extracted exact retained-source
  expectations for 1PYA, 1PWH, 1L6G and 2QUT, without network acquisition.
  `state_contracts` implements a narrow parser and build-time factual audit;
  `draft_integration_review` challenges correlated JSON edits with all authored
  pins recomputed. Root integrates the build gate and checks package/CI behavior.
- Early review found three real gaps in the prototype: it did not compare
  component/entity identity or all declared protein context; an invented atom
  name could pass as an omitted atom; and connection inventories needed
  explicit required-field checks. These are raw-source factual checks, not
  a reason to expand into chemical interpretation or a general CIF framework.
- Build-time auditing follows the existing primary-evidence validation and
  applies only to typed observed-state annotations. Existing synthetic schema
  fixtures and v1/v2 annotations retain their intended validation path.
  No new permanent scientific output, source capture or package data is needed.
- The source checker was approved at module SHA
  `9af012cb1e08bdb6bc8c410806afee5716c7d242f668ddd53d09c25da4f088e8`.
  Root ported those exact bytes and normalized only test imports/root paths.
  All fourteen targeted tests passed, including a real C2-O2 bond accompanied
  by a fictitious omitted atom: the authored layers accept its recomputed pins,
  but raw dictionary membership rejects it. All four retained structures and
  both typed batch builders pass. The complete core suite ran 312 tests
  successfully with one optional dependency skip. Scientific data, existing
  annotations and package projections are unchanged. Installed-wheel checks,
  repository contracts and all four CI jobs are required before this merge.

## Remaining scientific boundary

The delivered step layer retrieves exact source cofactor labels, directionally
scoped role text, inferred/assumed details and extra-enzymatic steps across all
32 PLP/pyruvoyl reaction steps. Four typed structural contexts distinguish
processed PYR, a PDD analogue, a PLV adduct and the covalent 13P intermediate.
None establishes an exact source-step trajectory; every such record join
retains `observed_state_grounds_step=false`.

After the raw-source checker ships, no additional internal schema expansion
identified in this review would change that conclusion. The next scientific
bottleneck is authoritative correspondence between a net reaction and its
source steps. M0213 exposes the clearest existing conflict: its entry reports
L-alanine to D-alanine while scheme identifiers retain L-alanine despite drawn
inversion. The retained package has no authoritative reaction atom map that
resolves it. More flags, examples or records cannot supply that missing evidence.

Human availability is not a prerequisite for completing this computational
goal or for further scoped development. Same-model agent review is correlated
and does not confer independent expert review. Physical and mechanistic claims
still require appropriately scoped evidence; these software checks establish
neither chemical identity/protonation nor causal residue roles or trajectories.

## M0213 reaction correspondence follow-up

Owner authorized the next scientific question after completion of the previous
goal. PR #43 merged at 2026-09-06 08:13:51 UTC, merge
`ea201cf249238405358a92a732699e146f50538e`; its tree matches tested head
`fd26b4153a44f5e3dbb3830eab38d8a1651b3336`. All four PR CI jobs passed in
run `34020940597`. Main was clean and matched origin/main before this branch:
`codex/m0213-reaction-correspondence`.

- Scientific question: which direction and stereochemical correspondence
  between M0213's net reaction and ordered source steps is actually supported?
  Correct a concrete retrieval/representation defect if the evidence permits;
  do not invent an atom map, resolve a source conflict by agreement, or expand
  schema simply to record another abstention.
- `source_ingestion`: primary Rhea/UniProt/ChEBI reaction evidence and precise
  direction/chemical-form semantics, using retained sources first. Additional
  acquisition cap is twelve requests and 3 MiB, within the existing cumulative
  batch limit of one hundred requests and 30 MiB. Count retries/redirects and
  preserve receipts. No paid calls, outreach or experiments.
- `draft_integration_review`: independently inspect the six source steps and
  terminal scheme, including actual drawn stereochemistry and persistent
  identifiers; challenge reversal, protonation/form collapse, proposal-scope
  leakage and unsupported atom mapping.
- `state_contracts`: inspect the current representation and propose the
  smallest useful query/contract after source findings are known. No speculative
  implementation before the supported correction is concrete.
- Root coordinates this board, source budget, integration, tests and publication.
  Initial agent work stays under `/tmp/catalytic-m0213-reaction-20260906/`.
  Existing source captures, primary/step annotations, frozen benchmarks and
  Atlas10 remain preserved unless a separately reviewed correction is justified.

### Source result and implementation boundary

The official Rhea machine row is `20250 / LR / 20249 / M0213`.
RHEA:20249 is the unspecified master, 20250 is left-to-right, 20251 is
right-to-left and 20252 is bidirectional. Retained UniProt P10724 and the
M-CSA proposal/Steps 1 and 6 agree on L-alanine to D-alanine. A flattened
browser-table interpretation was challenged and rejected using the exact
TSV row; no Rhea-versus-M-CSA direction conflict is retained.

The substantive correction concerns the drawings. The pinned optional
RDKit 2025.03.3 diagnostic reads the source endpoints R then S, opposite
the S(L)-to-R(D) curated references. The endpoint alanine fragments have
charge -1 while the curated zwitterions have charge 0. Source label
`chebi:57972` remains on the terminal fragment. Step 3 includes an explicit
alpha H and parses S; Step 4 has no assigned tetrahedral center. Per-panel
readouts are R, R, S, null, S, S, S. These are separate depiction diagnostics,
not a coherent reverse mechanism or an atom map. The initial fragment's
additional bond beyond the six labeled heavy atoms is to an explicit N-H,
not to PLP.

Root's optional script pins both reference-file hashes, their expected
CIP/charge and the original M0213 source hash. Script SHA-256 is
`fa9dfdafb089f3471238ff23ec2446bb67c4e0724a284182f7c8a4f90b7a3eaf`;
reproduced output is
`8e58483cd525c35ec4448575df0bb7ed4302240db0194aa87f67ecb239abf232`.
Swapping the reference files is rejected. RDKit remains outside production
requirements. The source agent used twelve acquisition requests and
1,267,489 response bytes; unavailable/header-only probes are negative capture
records, not positive chemical evidence. The HTTP 403 RXN capture establishes
no atom-pair correspondence.

The implementation is an additive curated-reaction sidecar. It preserves
original source, primary and step evidence bytes. Existing PLP/pyruvoyl CLI
queries automatically attach the correction using query v6; a containing
catalog uses v4. No new query flag or chemical identity alias is introduced.
Library calls without a sidecar and other source batches keep their existing
behavior. Original entry participant filters remain exact. Review is
same-model, nonblind and correlated, with zero independent human reviewers.

### Final reviewed inputs and local verification

- Reaction sidecar/source and package SHA-256:
  `c62b985e879f1877e009a4fa1f50282a6a5c701049311c0751a4e0cc589ad118`.
  Scientific payload pin:
  `3e80898cf0d9a4d7d5236f9f7587c1a8e2493b88fbf6c37795c10fb8ad1cfff3`.
  Projection SHA-256:
  `3bbf80d42ba7c9aceb48d38873509b7d1154b046fe8a19a55e18e3668af23c7c`.
- The source-bound validator is frozen at SHA-256
  `ccfb1572e0bcfd7ca89e9d93c7cb28c59bff56c8b15d7c4bc94a4ae81653551f`.
  Review found and closed a substring-witness loophole: a reverse-direction
  sentence could not substitute for the complete source proposal passage.
  Build checks also rederive Rhea direction rows, source endpoint labels and
  charges, the explicit Step 3 hydrogen, participant MOL facts and linkage
  to the pinned computational diagnostic. These checks do not independently
  calculate general chemistry at runtime.
- `draft_integration_review` owns nine adversarial tests. Internally consistent
  false annotations/projections with refreshed review hashes still fail against
  unchanged raw Rhea/source/diagnostic evidence. Root's five query tests cover
  exact forward participant retrieval, rejected reverse/form aliases, unchanged
  non-sidecar behavior, package pins and equal compact/full corrections.
- Final core suite: 326 tests passed with one optional dependency skip.
  A fresh wheel built from this exact validator passed source-draft queries
  with network connections blocked and no raw-source checkout. Atlas10's
  10-case/30-object runtime SHA remains
  `57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
  Rhea attribution is packaged separately with an exact hash; the earlier
  source/primary/step attribution and annotation bytes are untouched.
- Local verification logs are under `/tmp/catalytic-m0213-*-final-20260906.log`.
  Repository contracts and report-index checks passed. Four-job CI remains
  before merge. No further scientific work is required for this bounded
  correspondence correction; a separate question requires separate evidence.
