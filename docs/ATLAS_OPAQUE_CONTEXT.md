# Covalent candidates with opaque source context

The opt-in context extractor retains supported stereochemical marks and
coordinate-bond annotations while computing covalent-bond and formal-charge
changes. It does not assign stereochemistry or interpret coordination chemistry.
The original candidate command and its retained scan remain unchanged.

```sh
catalytic-earth atlas-candidates --preserve-context \
  --source data/atlas/source_drafts/batches/aldolase-transketolase/sources/M0219.json \
  --mechanism-id 1 --before-step 2 --output context-candidate.json
```

The Python API is `extract_context_panel_candidate(snapshot_bytes,
mechanism_id=..., before_step_id=...)` in `atlas_context_candidates`. It returns
`catalytic-earth.context-panel-candidate.v1`, always with `status=unreviewed`.
Output paths must be new files. Input integrity errors raise `ValueError`;
unsupported or ambiguous source context produces `needs_review` and no edits.

## Representation and provenance

ChemAxon's [MRV documentation](https://docs.chemaxon.com/latest/formats_marvin-documents-mrv.html)
describes distinct stereo, parity and convention-bond fields. Its
[stereochemistry documentation](https://docs.chemaxon.com/latest/jchem-base_stereochemistry.html)
distinguishes their interpretation from merely retaining source tokens. Our
policy is to preserve a narrow witnessed subset as uninterpreted data, with no
CIP or donor/acceptor assignment.

Each panel exposes the original scheme hash and ordered `bond_stereo`,
`atom_parity` and `bond_conventions` arrays. This version accepts only W/H
`bondStereo` children without attributes and undecorated `cxn:coord` bonds with
no numeric order. `atom_parity` stays empty; parity/chirality forms and other
unsupported annotations require review. Local bond IDs are retained as source
locators. Correspondence compares ordered atom references and raw metadata,
using the unique atom-locator map rather than assuming bond IDs are stable.

A private parser view removes only the captured W/H markup and coordinate
bonds, then delegates mapping, arrows, edit derivation and replay to the frozen
v1 engine. No atom, formal charge, ordinary bond order or arrow is invented or
changed in that view. Public bindings always identify the original snapshot and
original panel bytes. Projected parser hashes never become raw source evidence.

The returned graphs cover all depicted atom tokens and integer covalent bonds;
coordinate bonds remain in the separate source arrays. Coverage names the exact
claim `full_covalent_graph_replay_asserted`. Graph stereochemistry remains
unmodeled; a null graph field does not mean that the source lacks stereo marks.
Raw lone-pair annotations also remain outside replay.

## Admission rules

Every special reference must have a unique mapped counterpart. The ordered
annotation rows must remain exactly unchanged under that map. Every proposed
edit endpoint must be disjoint from special references, and no covalent bond
crossing into unmatched context may touch a special reference in either panel.
An unchanged W/H token alone does not establish unchanged local context when a
neighboring hydrogen or substituent is omitted or redrawn.

Unknown placement, duplicate edges, overlapping covalent/convention edges,
decorated or unsupported forms, changed/reversed rows, unmatched references and
edit interactions all stop extraction. Missing atoms are never treated as atom
deletion. Capture completeness, context preservation and covalent replay are
separate checks; none establishes physical identity, a canonical participant,
an exact cofactor state, a complete mechanism or experimental validation.

## Retained-source evaluation

The first regression is M0219 mechanism 1 Step 2→3: all 75 depiction nodes align,
and twelve arrow-supported covalent/charge changes reproduce the next covalent
graph. Four raw stereo rows (`W,W,H,W`) and two coordinate rows remain unchanged
and are disjoint from those edits. M0219's existing proposal/reaction and
protein-applicability conflicts are unresolved.

The [context scan](../data/atlas/context_candidates/scan.json) compares this mode
with the frozen [v1 scan](../data/atlas/candidate_extraction/scan.json) on the same
101 adjacent pairs. It distinguishes newly supported candidates from the seven
existing candidates and verifies that shared accepted graphs and edits agree.
The result is twelve candidates: five retained baseline candidates and seven
newly supported candidates. Eighty-nine pairs need review. Two baseline M0222
candidates (Steps 1→2 and 3→4) are withheld by the stricter context mode because
their molecule-level `absStereo=true` annotation is unsupported. The frozen
v1 results remain unchanged; context mode is not a strict superset.

| Newly supported pair (mechanism 1) | Matched / before / after nodes | Confirmed / arrow-only edits | Raw stereo / coordinate rows per panel |
| --- | --- | --- | --- |
| M0106, 3 → 4 | 73 / 74 / 73 | 2 / 2 | 0 / 2 |
| M0106, 7 → 8 | 66 / 66 / 68 | 10 / 0 | 0 / 2 |
| M0106, 8 → 9 | 67 / 68 / 67 | 2 / 2 | 0 / 2 |
| M0212, 13 → 14 | 86 / 87 / 86 | 2 / 2 | 2 / 4 |
| M0212, 15 → 16 | 81 / 84 / 81 | 2 / 4 | 2 / 4 |
| M0219, 2 → 3 | 75 / 75 / 75 | 12 / 0 | 4 / 2 |
| M0219, 4 → 5 | 71 / 71 / 71 | 8 / 0 | 1 / 2 |

Both M0219 rows replay their complete covalent graphs. The other new candidates
replay only mapped projections, preserving omitted or introduced context as
unmatched nodes. These counts do not add reviewed transitions or experimental
evidence and do not change benchmark labels.
M0106 Step 8 remains an explicitly inferred return step; its Step 7 after-only
H–O fragment is additional panel context, not an asserted created water molecule.
M0212 Step 15 omits H `a83` and bond `a33–a83` without an arrow witness, so the
candidate cannot replay a complete proton inventory. Its retained annotations
do not resolve FeMo/P-cluster state, reactive atoms or metal oxidation state.
Diagnostics report the first blocking reason, not an exhaustive chemistry audit.

```sh
python scripts/scan_atlas_context_candidates.py \
  --check data/atlas/context_candidates/scan.json
```

The retained report pins implementation files, source inventory, baseline report
and full candidate payloads. Direct raw-XML checks and adversarial tests assess
the implementation; these informed same-model agent reviews may share errors.
