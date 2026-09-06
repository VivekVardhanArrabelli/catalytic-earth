# Adjacent-panel candidate extraction board

Date: 2026-09-06. Base: `810cdba6e836163a04f39f094d2da78bd0c2b7b4`.

## Objective and acceptance

Extract unreviewed graph-edit candidates directly from retained M-CSA source
drawings. Reproduce the two M0173 comparisons without loading authored edits,
then scan all adjacent panels in the 11 retained Tier-1 draft records. This
reduces manual transcription; it does not establish experimental validity.

The engine must bind original snapshot and panel bytes, use unique exact
depiction-locator correspondence, distinguish after-graph-confirmed changes from
source-arrow-only proposals, and fail closed on ambiguous or unsupported input.
Every source arrow and endpoint must be accounted for. Missing source nodes are
not atom deletions. No candidate receives review, tier, or benchmark credit.

## Ownership and messages

| Owner | Bounded responsibility | Status |
| --- | --- | --- |
| Root | CLI, reproducible scan, integration, release checks, publication | 388 core tests and fresh-wheel checks passed |
| state_contracts | Generic extraction module only | Implemented; scanner exploit fixes independently confirmed |
| draft_integration_review | Independent extraction tests only | 11 focused tests passed |
| source_ingestion | Read-only retained-source inventory and traps | All seven candidates mechanically reproduced from raw XML |

- Root → state/reviewer: API is `extract_panel_candidate(snapshot_bytes,
  mechanism_id=..., before_step_id=...)`. Successful candidates remain
  `status=unreviewed`; unsupported representations return `needs_review` with no
  edits or flow bindings. Input integrity errors raise `ValueError`.
- State → root/reviewer: coverage reuses the existing partial-panel coverage
  shape. Complete maps can assert full replay; partial maps only replay the
  mapped projection. Duplicate identity/coordinate keys are explicit ambiguity.
- Root → state: M0173 source flow shapes contain two ordered points; no head
  flags. Reject unfamiliar electron-count/flow attributes instead of guessing.

## Verification boundary

Gate the bounded scan on both M0173 semantic baselines and decisive negatives.
Preserve existing reviewed assets, Atlas-10 runtime digest, 702 benchmark labels,
and historical release manifest. Run core tests, repository contracts, and a
fresh offline wheel check. Publish only after the branch CI matrix passes.

## Results

The engine reproduces M0173 Step 1→2 (50 matches, six graph-confirmed edits,
complete replay) and Step 2→3 (40 matches, three confirmed and three arrow-only
edits, matched-projection replay), without reading the authored edits as inputs.

Independent challenge caught and corrected a missing source-step binding,
wrong-direction charge fallback, ignored raw arrow-head attributes and generated
IDs concealing absent source flow IDs. Root removed an unnecessary dependency on
the after panel's future arrows; graph representation checks still cover both
panels. Regression tests exercise each boundary, including renamed source IDs,
missing charged nodes, ambiguity, graph contradictions and corrupt hashes.

The final bounded inventory contains 11 records, 13 proposals, 114 retained
panels and all 101 adjacent pairs. The scan extracts seven unreviewed candidates:
M0222 1→2 and 3→4; M0049 5→6 and 7→8; M0066 4→5, 9→10 and 10→11. Only M0066
9→10 replays the complete source graph. First blockers on the other 94 pairs are
67 stereochemistry/bond-convention cases and 27 other unsupported formats.
Those categories are first-stop diagnostics, not exhaustive chemistry labels.

The installed `atlas-candidates` command consumes an explicit local source file
and refuses to overwrite output files. The retained scan pins sources, engine
dependencies and full candidate payloads; its scanner rejects hash corruption
and incomplete panel inventories. Fifteen focused and integration tests pass.

State's scanner audit found that splitting one mechanism across registry rows
could omit a pair, and an alternate repository root could misidentify executing
code in the implementation hashes. Root fixed both: mechanisms are unique,
entry/scheme/registry inventories agree, every adjacency is counted, IDs are
strict positive integers, duplicate JSON keys are rejected, and dependency
origins must match the executing repository. Regression exploits now fail.

Repository contracts passed; the first complete core run passed 387 tests.
A fresh wheel passed offline source queries and both M0173 extractions with
network connections blocked and RDKit absent. Atlas-10 retains runtime digest
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.

The independent raw-source audit used direct standard-library XML parsing,
without extraction or partial-panel helpers. It reproduced all seven mappings,
confirmed versus arrow-only edit sets and directional arrow witnesses. It
preserved source identity-label conflicts, the inferred M0049 Step 7, and the
unarrowed H53 node in M0066 Step 11. Raw lone-pair annotations change consistently
with formal charges but are outside graph replay; root added the explicit output
limit `lone_pair_annotations_replayed=false`. No candidate was promoted.
The final independent audit reported no blocker and has SHA256
`86626854593237bfa0b28cc863cf13e532e1ed153747e7b896e6d4d4bae2715a`.

Final local checks: 388 core tests passed; repository contracts passed; 15 focused
extraction/integration tests passed; retained scan reproduced byte-exactly; fresh
wheel queries and candidate extraction passed from an empty directory with
network connections blocked and RDKit absent. State independently reran and
confirmed rejection of both scanner exploits. Publication remains gated on CI.
