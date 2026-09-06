# Unreviewed adjacent-panel candidates

The offline extractor derives candidate bond and formal-charge edits from two
retained M-CSA drawings and the first drawing's ordered electron-flow arrows.
It requires no authored edit list, external model, chemistry toolkit or network.
The output always remains unreviewed, including when graph replay is exact.

```sh
catalytic-earth atlas-candidates \
  --source data/atlas/atlas10/sources/mcsa/M0173.json \
  --mechanism-id 1 --before-step 2 --output candidate.json
```

`--source` is an explicit local snapshot; raw drawings are not packaged in the
wheel. `--output` creates a new file and refuses to overwrite existing evidence.
The Python API is `extract_panel_candidate(snapshot_bytes, mechanism_id=...,
before_step_id=...)`. It hashes the supplied bytes, verifies the selected embedded
panel hashes, and compares consecutive source steps, including terminal panels.
Malformed or inconsistent input raises `ValueError`.

## Evidence rules

Correspondence requires unique exact matches of element, 2D coordinates, isotope,
label, alias and R-group reference. Formal charge may change. Local atom IDs,
nearest coordinates, and chemical symmetry do not establish correspondence.
The map is a depiction alignment, not physical atom identity.

Mapped bond/charge differences require a unique direction-compatible arrow.
Each edit is marked `after_graph_confirmed` or `source_arrow_only`. Arrow-only
proposals are limited to removing an existing single bond or adding an absent
single bond where at least one endpoint is unmatched. Missing-node charges are
not inferred. Both full source graphs, unmatched nodes, crossing bonds, per-arrow
coverage and exact mapped-projection replay remain visible.

Every before-panel arrow and endpoint must be covered. Unsupported electronic
arrow attributes, ambiguous locator keys, contradictory arrows, unsupported
wildcards, source stereochemistry or coordinate-bond conventions cause
`needs_review` with no proposed edits. The next panel's future arrows are not
interpreted. Graph checks still apply to both panels. The first blocking reason
is reported; diagnostics are not an exhaustive classification of the chemistry.

Source omissions never become atom deletions or synthesized product structures.
Exact replay verifies a graph calculation, not a mechanism's experimental truth,
canonical participants, complete catalytic path or stereochemical assignment.
Graphs cover depicted atom tokens, covalent bond orders and formal charge. Raw
`lonePair` annotations are not replayed; even a complete graph replay is not a
complete electronic-state reconstruction. The output explicitly records this
limit as `lone_pair_annotations_replayed=false`.

## Retained-source scan

The [explicit source registry](../data/atlas/candidate_extraction/source_registry.json)
contains all 114 retained panels in 13 proposals across the 11 Tier-1 draft
records. The [reproducible scan](../data/atlas/candidate_extraction/scan.json)
attempts all 101 adjacent pairs. Seven produce candidates; 94 need additional
representation work or review. First-stop diagnostics are 67 stereochemistry or
bond-convention cases and 27 other unsupported representations.

| Record and source steps | Matched / before / after nodes | Graph-confirmed edits | Arrow-only edits | Replay |
| --- | --- | --- | --- | --- |
| M0222, 1 → 2 | 30 / 57 / 57 | 4 | 0 | Matched projection |
| M0222, 3 → 4 | 54 / 56 / 56 | 3 | 3 | Matched projection |
| M0049, 5 → 6 | 54 / 59 / 59 | 3 | 5 | Matched projection |
| M0049, 7 → 8 | 48 / 49 / 49 | 2 | 2 | Matched projection |
| M0066, 4 → 5 | 57 / 58 / 60 | 6 | 2 | Matched projection |
| M0066, 9 → 10 | 52 / 52 / 52 | 8 | 0 | Complete source graph |
| M0066, 10 → 11 | 51 / 52 / 53 | 8 | 2 | Matched projection |

All rows are mechanism 1. M0049 Step 7 is explicitly described as inferred by
the retained source. Raw-source audit also retains unresolved identity labels:
M0222 Step 1's CHEBI:57642 conflicts with its G3P source prose; M0049 Step 5's
CHEBI:32526 does not resolve its entry/source identity conflict; M0066's repeated
CHEBI:597326 does not establish PLP versus PMP state. M0066 Step 11 introduces an
unarrowed H53 depiction node, which remains unmatched. None of those issues is
resolved by replay. The seven candidates are not seven validated transitions;
they do not change the reviewed transformation catalog, evidence tiers or
benchmark labels. Before this scan, the generic extractor independently
reproduced the semantic edits of both existing M0173 comparisons from raw bytes.

```sh
python scripts/scan_atlas_candidates.py \
  --check data/atlas/candidate_extraction/scan.json
```

The report pins source bytes, implementation files and every complete candidate
payload. Corrupt hashes or incomplete panel inventories abort the scan rather
than count as scientific abstentions. Agent challenge tests and independent raw
source audits check this implementation; same-model reviews can share errors.

The largest measured representation gap is preserving stereochemical and
metal-coordinate information while extracting supported covalent changes.
That extension needs its own explicit representation and tests before it can
unlock the blocked cases.
