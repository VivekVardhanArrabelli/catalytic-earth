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
  - python -m unittest tests.core.test_workbench_labels    -> 12 tests, OK
  - python -m catalytic_earth.workbench.demo_check --sweep -> 0 defects.
    Exhaustive presentation sweep across three viewport widths, both
    mechanisms, every selectable atom and fragment, all twelve variant and
    endpoint combinations, and all three pattern presets. It found one real
    defect on its first run, a Python None leaking into an edit label, which
    is fixed and pinned by a test.
  - Claim-label and numbering audit (September 16 plan item): see below.
  - Clean-venv wheel install re-verified after the audit: every route served
    and the full browser demonstration passed against it with no index access.
  - python scripts/run_test_tier.py --check               -> tiers valid
  - python scripts/run_test_tier.py core/unit             -> see the commit
    message for the result recorded at commit time.
  - python -m catalytic_earth.workbench.demo_check --port 8766 --shots ./shots
    -> 33/33 checks passed, no console errors. With --video, 34/34 including
    the recording check. This drives a real Chromium
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
