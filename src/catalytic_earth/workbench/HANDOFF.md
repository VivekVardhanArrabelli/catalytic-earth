# Mechanism Workbench — handoff

Feature-local handoff for the Workbench slice. Keep this file current after
each meaningful work block. One writer per file.

```text
Actual branch / base / current commit:
  branch claude/catalytic-earth-workbench-dxmk7z
  base   312adf5b0a1463c69f709c000ed7ad8c860602db (matches the brief's snapshot)
  work committed on top of that base on the same branch

Uncommitted changes and owner:
  none at the time of writing; all Workbench files are committed

Working features verified:
  - M0187 and M0173 both load through the same renderer and the same adapter
    code path. Neither has a hard-coded scientific page.
  - Source-graph replay: before panel, per-edit stepping, after panel. Break,
    form, bond-order and charge edits are drawn distinctly. Each edit shows its
    edit id and its bound source arrow (flow) id.
  - Atom selection and supported-fragment selection open the inspector.
  - Inspector shows the residue relationship where the packaged query supports
    one, and "unresolved" where it does not.
  - H297N evidence: four observations with endpoint-specific labels, source
    witness quotes, comparator, and conditions. Endpoint filter narrows to the
    two isotope-exchange rows.
  - Shared-atom chemical pattern query with a structured clause builder, backed
    by the existing matcher. Worked examples for the shared-atom match, the
    disjoint-atom no-match, and the symmetric-assignment case.
  - The whole packaged evidence set is reachable: both variants, every
    endpoint, and each observation labelled with its own variant.
  - Guided walkthrough: five steps that drive the real controls and queries,
    covering the recorded question and adjudication, the before and after
    panels, the supported residue link selected by its own relation id, the
    endpoint comparison with focal and contextual variants separated, and the
    inspection request. Leaving it keeps the interface working normally.
  - Matched chemistry viewer: a returned candidate and assignment drawn from
    the retained source depiction coordinates, with bound atoms marked by
    variable name, per-clause witness edits and their support state, selectable
    alternative assignments, and the candidate marked unreviewed throughout.
  - External tool contribution panel, driven by the provider-neutral ledger.
    Verified in both states: empty (the real ledger) and populated (a
    throwaway ledger via the path override, never written to the repository).

Exact launch command and environment:
  pip install -e .            # or install the built wheel
  python -m catalytic_earth.workbench           # http://127.0.0.1:8765/
  python -m catalytic_earth.workbench --port 8790
  Standard library only. Loopback bind only. No network access at runtime.
  Verified from a clean virtualenv with a wheel installed using --no-index.

Commands/tests actually run and outcomes:
  - All seven documented CLI commands in docs/: ran, exit 0, outputs retained
    in the session scratchpad. Their schemas were read, not guessed.
  - python -m unittest tests.core.test_workbench_adapter  -> 21 tests, OK
  - python -m unittest tests.core.test_workbench_server   -> 13 tests, OK
  - python -m unittest tests.core.test_workbench_external_sources
                                                          -> 13 tests, OK
  - python -m unittest tests.core.test_workbench_labels    -> 15 tests, OK
  - python -m unittest tests.core.test_workbench_frontend_state
                                                          -> 12 tests, OK
  - python -m unittest tests.core.test_workbench_match_chemistry
                                                          -> 15 tests, OK
  - python -m unittest tests.core.test_workbench_external_results
                                                          -> 20 tests, OK
  - All seven workbench modules together              -> 138 tests, OK
  - python -m catalytic_earth.workbench.demo_check --sweep -> 0 defects.
    Exhaustive presentation sweep across three viewport widths, both
    mechanisms, every selectable atom and fragment, all twelve variant and
    endpoint combinations, and all three pattern presets. It found one real
    defect on its first run, a Python None leaking into an edit label, which
    is fixed and pinned by a test.
  - Claim-label and numbering audit (September 16 plan item): see below.
  - Base/head comparison for the three Atlas-50 errors, run in this same
    environment as the review asked. A detached worktree at the base commit
    312adf5b was created and the two modules were run there and at head. The
    error sets are byte-identical: the same three test ids fail at both, all
    raising CalledProcessError from `git ls-tree` against commit
    375548419e7435efa2bffc89be5e32aa70864875, which is absent because this
    checkout is shallow (65 commits, .git/shallow present). The repository's
    own contract validator fails the same way and says so itself, asking for a
    full-history clone. The errors are therefore attributable to the checkout,
    not to this branch. The worktree was removed after the comparison.
  - Clean-venv wheel install re-verified after the audit: every route served
    and the full browser demonstration passed against it with no index access.
  - python scripts/run_test_tier.py --check               -> tiers valid
  - python scripts/run_test_tier.py core/unit             -> see the commit
    message for the result recorded at commit time.
  - python -m catalytic_earth.workbench.demo_check --port 8766 --shots ./shots
    -> 71/71 checks passed, no console errors. With --video, 72/72 including
    the recording check. Also passes against a clean-directory wheel install. This drives a real Chromium
    browser against the running server and covers load, stepping, atom and
    fragment selection, evidence filtering, the second mechanism, all three
    pattern outcomes, and reload. Its screenshots are captures of the running
    application. It needs playwright, which is not a project dependency, so it
    is deliberately outside the test tiers.
  - Wheel build and clean-venv install: succeeded; the app served every route
    from the installed package with no index access.

Actual Rosalind tools used and saved outputs:
  NONE. This session ran in Claude Code, where the session plugin list is
  empty. A keyword search of the account plugin catalog for rosalind, protein
  structure viewer, literature search, molecular biology and PDB structure
  returned no entry named Rosalind at all; the connected connectors are Gmail
  and Google Drive only. No plugin call was made, and none is simulated or
  described as if it had succeeded.

  The contribution ledger at work/workbench_external_sources.json is the seam
  for this. It is provider-neutral and currently EMPTY, which the interface
  states plainly. Rosalind remains mandatory for submission: a contribution
  recorded through any other suite must be credited to that suite by name and
  cannot be presented as Rosalind output.

  An install card for the Bio Research plugin was rendered for the owner as a
  possible interim literature/database provider. It bundles remote PubMed,
  bioRxiv, ChEMBL and Open Targets servers. Whether its tool surface resembles
  Rosalind is UNVERIFIED; no structure-viewing server was visible in its
  component list, so the structure-view action may stay uncovered by it.

Known scientific or UI limitations:
  - Atom positions are a COMPUTED 2D layout from graph topology. The packaged
    transformation query returns no depiction coordinates for panel atoms, so
    no retained coordinates exist to draw the panel with. The UI says so on
    screen. It is not measured geometry and not a molecular conformation.
  - Retained source depiction coordinates (x2/y2) DO exist, but only for the
    source-fragment atoms in the mechanism-evidence query. The inspector
    reports how many fragment atoms carry them and labels them as depiction
    coordinates, not geometry.
  - The layout uses the union of before-panel and after-panel bonds so one
    frame can show both states. This is a drawing choice and asserts no
    chemistry. It is labeled on screen.
  - M0187: all seven changed atoms are unresolved by the direct atom-label
    site query. The His297 relationship comes only from the separate reviewed
    source-fragment relation. The UI shows both facts rather than merging them.
  - The Glu317 step-1 relation remains unresolved. Lys166 resolves to a site
    but carries no matched H297N observation; it is shown as reference-site
    context, not a matched control.
  - No deposited H297N mutant-context structure is available. The structure
    shown is a reference structure with its own declared limitation.
  - The candidate catalog is unreviewed; the UI shows that status and states
    that a match does not promote any candidate's evidence status.
  - Screenshots and the recording are not committed: the repository carries no
    image or video artifacts and declares its binary types explicitly.
    Regenerate both with demo_check, using --video for the recording.

September 16 audit findings, all fixed in this branch:
  - Four claim labels were misapplied. A resolved atlas site id, an external
    tool contribution and a reported "no detectable difference" outcome all
    reused styles whose legend entries meant something else, and two styles
    used in the interface had no legend entry at all. The label vocabulary is
    now closed, split into provenance and reported outcome, and checked by a
    test so the defect cannot recur.
  - Two different resolutions are visible in one interface: the reference
    structure's, and the one reported for the structural comparison. They are
    different records and different structures. The packaged data already says
    so in its structure-applicability abstention, but that text sat behind a
    closed disclosure. The abstentions are now visible on the evidence panel,
    and a structure-kind observation states that it names no deposited
    structure.
  - A no-difference result reused nondetection wording. The two are now worded
    separately.
  - Numbering was checked against the packaged queries and the documents and
    matched exactly: M0187 a58 gives UniProt His297, 1MNS author 297, mmCIF
    295; a19 gives Lys166, author 166, mmCIF 164; M0173 a44 gives Ser204,
    1PQ5 author 195, mmCIF 180; a21 gives His65, author 56, mmCIF 41.

Rosalind session checklist (OWNER ACTION, cannot be done from Claude Code):
  Rosalind is an OpenAI product. The Life Sciences Research plugin runs in
  Codex and ChatGPT; the restricted GPT-Rosalind model is a separate thing and
  the plugins do not require it. Rosalind Workbench is reachable at
  chatgpt.com/rosalind-workbench/ with the models already on the account.
  Claude Code cannot reach or operate it, so the call is made there and only
  its result is recorded here.

  Do at least one of these two, whichever the plugin surface supports:

  1. Structure view. Open PDB 1MNS, the reference structure for the M0187
     His297 site context. It is inhibitor-bound and chemically modified, and
     it is NOT an H297N mutant structure; do not let the session imply it is.
  2. Literature lookup. Retrieve the bibliographic record for PMID 1909893,
     the single paper behind all four H297N observations.

  Capture, from the real call: the exact plugin/tool name, the exact query
  sent, and the identifiers or values returned. Then record it here:

    python -m catalytic_earth.workbench.external_sources \
      --provider-suite "Rosalind" --provider-tool "<exact tool name>" \
      --action structure_view --query "<exact query sent>" \
      --subject "PDB:1MNS" --retrieved "<what came back>"

    python -m catalytic_earth.workbench.external_sources \
      --provider-suite "Rosalind" --provider-tool "<exact tool name>" \
      --action literature_lookup --query "<exact query sent>" \
      --subject "paper:PMID:1909893" --retrieved "<what came back>"

  The subject strings above are what the interface keys on: a PDB subject
  badges the reference structure block, a paper subject badges that evidence
  id. Any other subject still records fine, it just will not badge.

  Record only a call that actually happened and whose output is in hand.
  Do not retrieve full text or acquire new sources as part of this; that is a
  new source acquisition needing its own permission review, and it is not what
  this step is for. This step adds attribution, not evidence.

External review repairs (R1-R4), all reproduced first and then fixed:
  - R1 stale selected fragment. The selection held a relation object from an
    earlier evidence response, so after changing a filter the inspector kept
    showing that response's observations. Reproduced live: main panel 2,
    inspector 4. The selection is now a stable relation id, re-resolved against
    the current result and dropped when the result no longer supports it.
  - R2 out-of-order responses. loadMechanism set the selected id before
    awaiting and installed whatever returned. Reproduced live by delaying one
    mechanism's responses: the selector read M0173 while the graph showed
    M0187. All three async loaders now carry a request generation guard,
    selection and results commit together, and an obsolete error cannot
    replace current state.
  - R3 subject-only badge. Any contribution with a PDB subject rendered as a
    structure view, including a database lookup that returned nothing. The
    ledger index now carries each record's action, provider, tool and result
    count, the interface badges by recorded action, and an empty result is
    disclosed as returning nothing.
  - R4 silent numeric coercion. A fractional clause value was truncated and
    the query ran anyway: 0.9 became 0 and returned two candidates. Values are
    now parsed exactly or refused at both boundaries. Canonical integer
    strings are accepted and give identical results to the same integers;
    blank, fractional, boolean, non-finite and malformed values fail visibly.

  The browser harness previously checked only the main observation count, so
  it could not see R1. It now compares the inspector against the main panel,
  drives out-of-order responses, and exercises the refused clause values. All
  four regressions were confirmed to fail against the reintroduced defects.

Follow-up review repairs (S1-S2), both reproduced first and then fixed:
  - S1 a refusal could be overwritten by an older search. runPattern advanced
    its request generation only after validation, so a refused attempt
    returned without retiring the request already in flight, and that older
    response replaced the "Query not run" message with results. The generation
    now advances at the top of every attempt, including one that never reaches
    the network, and there is exactly one increment.
  - S2 a failed current request left the controls describing something else.
    Failures replaced only an error area, so after a failed mechanism load the
    selector read M0173 while the 9-edit M0187 graph remained, and after a
    failed evidence load the filter read isotope_exchange while the inspector
    still held four observations. A failed request now restores the controls to
    the state that is actually displayed and says so in a notice, or clears the
    dependent views when nothing was ever loaded.

  Both were verified in a browser. The harness gained regressions for the
  refusal surviving a stale response, and for control agreement after a failed
  mechanism load and a failed evidence load. Console capture is suspended only
  for the deliberately injected failures and resumes afterwards, so the
  injected 500s are not mistaken for application errors.

Second external review repairs (A, B, C), all reproduced first:
  - A1 the focal variant was read before the filters were cleared, so starting
    from K166R produced an empty focal table with H297N listed as contextual.
    Reproduced live. Both filters are now cleared and the query awaited before
    the focal variant is derived, and an unresolved focal variant shows nothing
    rather than guessing.
  - A2 the guided residue step selected the M0187 fragment while M0173 was the
    loaded mechanism, so the graph and the selected relation belonged to
    different cases. Reproduced live. The guide now resolves its mechanism from
    the case's own transformation binding and loads it first; a failed load
    stops the step.
  - A3 a step was marked done after any fulfilled return, including early
    returns. Steps now report success and are marked only on success.
  - B1 chemistry inspection read the support and M-CSA controls at click time,
    so editing them without re-running mixed old clauses with new filters.
    Reproduced by capturing the posted request. The complete accepted query is
    now captured with its result and used for inspection.
  - B2 a delayed chemistry response could populate the panel under a newer
    no-match result. Reproduced live. Every search attempt, valid or refused,
    retires the accepted query and any open chemistry, and a response is
    installed only while both its own request and its parent result are current.
  - C1 a bond between two witness atoms was highlighted even when no bond edit
    touched it. Witness bonds are now exact pairs taken from bond operations
    only. No packaged candidate currently exhibits the spurious case, checked
    across the catalog, so this was a latent logic defect.
  - C2 the after panel was annotated with before-panel identifiers. Two of the
    twelve packaged candidates have non-identity atom maps, so this was live,
    not latent. After-panel marks now go through the retained correspondence,
    and a bound atom with no mapping is left unmarked and disclosed. Verified
    on M0212 steps 15-16, where bound atom a81 has no mapping: the before panel
    marks two atoms and the after panel one.
  - C3 source-graph confirmation reused the style reserved for a published
    measurement. It has its own label and legend entry now.

Presentation pass (single bounded pass, no redesign):
  - The walkthrough is a compact horizontal stepper rather than a full-height
    list, so the question, diagram and outcome stay in frame.
  - Packaged enumeration values are phrased for reading at render time only,
    with the raw token kept beside them in a subordinate style. No data is
    rewritten and every raw field remains in the expert disclosures.
  - The header states what the product does, with a visible scope note in place
    of the implementation disclaimer.

External result-return path (this block):
  - external_results.py completes the other half of the ledger. It consumes a
    file a tool actually saved, hashes and measures it from disk, ties it to
    the case it answers, and records it beside the packaged evidence.
  - One resolver serves both packaged record families with no enzyme-specific
    branch. The mandelate case resolves through the mechanism-evidence query
    and the transketolase comparison tk_2020:H473N:DHB_accumulation through the
    perturbation projection; only the identifier differs. Verified for both.
  - A comparison selects only its own study's sources. Source identity is read
    from the observations' providers and the comparison's evidence pointers, not
    derived from a text prefix of the study id: tk2020, tk2024 and tktf all
    start "tk", and only tk2020 belongs to a tk_2020 comparison.
  - Conflicts and unresolved matches are preserved, never accepted. A declared
    publication, site or structure the record does not carry is recorded as a
    conflict naming what it does carry; an unresolved case is recorded as
    unresolved and the result is still kept, without the association it lacks.
  - A confirmation is membership plus one relation. Identifiers the case carries
    are checked again against its individual relations, so a publication from
    one evidence relation and a site from another read as the conflict they are
    rather than as a confirmed pair.
  - Source roles stay apart. A case's publications are its functional-observation
    sources; the primary citation of a deposited structure is a role these
    records do not enumerate, so under a structure the case carries it is kept
    as separately sourced external context, never called a contradiction and
    never swapped for a functional source that would match.
  - Context values are recorded, not checked, and the result says so.
  - The interface shows the returned scientific context, the saved artifacts
    with type, size and hash, and the per-field association table with reasons,
    not only a badge. Each artifact opens from its row, read back by its
    recorded digest and shown as text; a moved or edited file says so rather
    than standing in for the result. Association chips have their own styling
    and never borrow the measurement or nondetection chips.
  - Nothing is merged into the packaged records. A test asserts the packaged
    query output is byte-identical before and after an import.

  REPO LEDGER IS STILL EMPTY. No external suite has run, so no real output
  exists to consume. The path was exercised with local fixtures in a temporary
  ledger and in tests; none of it was written to work/workbench_external_sources.json.
  The recording's external segment uses fixtures whose provider suite is named
  "LOCAL FIXTURE (not a tool call)" so it cannot read as a Rosalind result.

Reproduction, exactly as run here:
  pip install -e .
  python -m unittest tests.core.test_workbench_adapter \
    tests.core.test_workbench_server tests.core.test_workbench_external_sources \
    tests.core.test_workbench_external_results tests.core.test_workbench_labels \
    tests.core.test_workbench_frontend_state tests.core.test_workbench_match_chemistry
  python scripts/run_test_tier.py core/unit
  python -m catalytic_earth.workbench --port 8766          # real, empty ledger
  python -m catalytic_earth.workbench.demo_check --port 8766 --shots ./shots --video ./video
  python -m catalytic_earth.workbench.demo_check --port 8766 --sweep
  # To exercise the return path without touching the repository ledger:
  export CATALYTIC_EARTH_WORKBENCH_LEDGER=/tmp/demo-ledger.json
  python -m catalytic_earth.workbench.external_results \
    --provider-suite "<suite>" --provider-tool "<tool>" --action structure_view \
    --query "<query>" --case atlas10.mandelate-racemase-pputida.enolate \
    --publication paper:PMID:1909893 --site P11444:H297 --artifact <saved file>

Next single implementation task:
  Nothing further is possible here without the external suite. Every plan item
  that does not depend on it is complete: both mechanisms through one renderer,
  the structured pattern builder, the full demonstration including the
  shared-atom match and the disjoint-atom no-match, the numbering and claim
  label audit, relaunch from the documented environment, the recording and
  screenshots, and the submission notes in docs/WORKBENCH_SUBMISSION.md.

  Remaining, both owner actions: record one Rosalind contribution per the
  checklist above, then confirm the organizer's deadline and approve posting.
  Nothing has been posted, published or shared.

  Next local coding task: record the end-to-end demonstration as a short
  screen capture, using demo_check as the script for what to show.
```
