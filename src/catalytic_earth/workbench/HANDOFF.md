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
  - python -m unittest tests.core.test_workbench_server   -> 12 tests, OK
  - python scripts/run_test_tier.py --check               -> tiers valid
  - python scripts/run_test_tier.py core/unit             -> see the commit
    message for the result recorded at commit time.
  - Real browser run (Chromium via Playwright, headed engine, headless mode):
    35 assertions covering load, stepping, selection, evidence filtering,
    the second mechanism, both pattern outcomes, and reload. All passed with
    no console errors. Screenshots were captured from the running application.
  - Wheel build and clean-venv install: succeeded; the app served every route
    from the installed package with no index access.

Actual Rosalind tools used and saved outputs:
  NONE. This session ran in Claude Code, where no Rosalind suite plugins are
  installed (the session plugin list is empty). No plugin call was made, and
  none is simulated or described as if it had succeeded. This remains the
  single outstanding owner action; see "Next single implementation task".

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
  - The pattern result renders clause witnesses as raw JSON. Precise, but it
    could be formatted more readably.
  - No recording has been made yet; only still screenshots.

Next single implementation task:
  OWNER ACTION (cannot be done from Claude Code): perform one real Rosalind
  literature/database or structure-viewing action in the authorized desktop
  environment, retain its actual output, and attach it to the workflow with
  plugin attribution kept separate from local Python calculations.

  Next local coding task: format the pattern-query clause witnesses as a
  readable table instead of raw JSON, then record the end-to-end demonstration.
```
