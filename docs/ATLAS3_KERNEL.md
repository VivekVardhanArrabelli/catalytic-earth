# Atlas-3: first biological kernel

Atlas-3 is the first end-to-end, non-fixture slice of the Catalytic Earth
Atlas. It turns three frozen biological cases into nine separately counted,
typed objects:

| Case | Tier 0 | Tier 1 | Tier 2 | Key truth boundary |
| --- | --- | --- | --- | --- |
| AdoCbl methylmalonyl-CoA mutase | RHEA:22888 | M-CSA M0062 mechanism 2 | six-step, seven-site radical hypothesis | exact radical/protonation microstates and internally inconsistent cobalt labels remain unresolved |
| *E. coli* MnSOD | RHEA:20696 | explicit abstention | two-half-reaction, four-ligand Mn redox/PCET hypothesis | Cu/Zn M-CSA M0138 is blocked from same-EC transfer; the trapped inhibited structure is not a turnover movie |
| TEM-1 beta-lactamase | RHEA:20401 | M-CSA M0002 mechanism 2 | five-step, six-site covalent acyl-enzyme hypothesis | the lower-rated Lys73 activation route remains an alternative; nitrocefin activity would not alone validate the proton path |

This is an Atlas kernel, not a benchmark. The useful output is searchable
knowledge with provenance and explicit abstention. The three cases were chosen
to force the representation to handle radical/cofactor chemistry, metal redox
and PCET, covalent catalysis, source conflict, protein/structure numbering, and
an attractive but invalid same-EC mechanism transfer.

## Durable artifacts

- [`atlas3_selection.json`](../data/atlas/atlas3_selection.json) freezes the
  cases, source handles, budgets, assay candidate, and exit gates before
  compilation.
- [`source_manifest.json`](../data/atlas/atlas3/source_manifest.json) binds 13
  redistributable source snapshots and five reference-only literature handles
  to exact identities, rights fields, retrieval metadata, and hashes.
- [`compilation_spec.json`](../data/atlas/atlas3/compilation_spec.json) is the
  human-auditable scientific compilation: steps, site mappings,
  counterevidence, uncertainty, and claim boundaries.
- [`kernel.json`](../data/atlas/atlas3/kernel.json) contains exactly three
  `net_reaction`, three `source_mechanism`, and three
  `mechanism_hypothesis` objects using `mechanism-record.v2`.
- [`case_truth_summary.sql`](../data/atlas/atlas3/queries/case_truth_summary.sql)
  asks what each case currently knows: highest tier, source-mechanism status,
  direct and counterexample handles, step/site counts, uncertainty,
  counterevidence, assay candidacy, and the key abstention.
- [`case_truth_summary_expected.json`](../data/atlas/atlas3/queries/case_truth_summary_expected.json)
  freezes the deterministic query result.
- [`SOURCE_ATTRIBUTION.md`](../data/atlas/atlas3/SOURCE_ATTRIBUTION.md) records
  source attribution and transformation notices.

The source snapshots total 1,223,884 bytes. Article content is not copied. The
five literature items remain verified reference-only handles.

## What was checked mechanically

The compiler does more than copy prose:

- Rhea identities, equations, EC numbers, and ChEBI participant sets must
  match the frozen selection.
- Direct M-CSA entries must match the selected UniProt proteins and the chosen
  three-star proposal. Product pseudo-steps are not counted as chemistry.
- Every hypothesis site must match its UniProt sequence residue, UniProt-to-PDB
  chain range, mmCIF author position, mmCIF label position, and coordinate
  residue identity.
- The P00448/1D5N crosswalk explicitly maps natural positions 27, 82, 168, and
  172 to structure positions 26, 81, 167, and 171 because 1D5N covers UniProt
  positions 2-206.
- TEM-1 natural Ser68/Lys71/Ser128/Glu164 map to Ambler/PDB author
  Ser70/Lys73/Ser130/Glu166 and mmCIF label positions 45/48/105/141.
- M-CSA M0138 cannot contribute a step or site to the MnSOD source object; that
  object must remain an explicit abstention.
- Evidence references must resolve to the frozen source manifest and carry the
  exact snapshot hash or the declared reference-only state.
- Unknown fields, fabricated tiers, missing uncertainty, broken evidence
  references, and provenance drift fail closed.

One source-level correction is deliberately visible: M-CSA M0062 step 1 says
a Co(II)-C bond produces Co(I), while the same entry's prose describes
formation of active Co(II). The Tier-1 record preserves this wording and flags
the conflict. The Tier-2 hypothesis asserts bond homolysis and a radical-pair
state but abstains from repeating the disputed oxidation labels as settled
chemistry.

## Reproduce locally

From the repository:

```bash
python scripts/build_atlas3_sources.py
python scripts/build_atlas3_kernel.py --check
python -m catalytic_earth.core_cli atlas3
```

From an installed wheel:

```bash
catalytic-earth atlas3
```

The current frozen digests are:

| Surface | SHA-256 |
| --- | --- |
| Selection | `d24361bb9fc000d39d7209c5538bd23df845a94aa2dce1fb38c18d56dd8e1ada` |
| Source snapshot set | `71a4d85f6bd0d50f9f51ef02f125220dd45545f5357fea5ced5b66783149822e` |
| Compilation spec | `07464adb302cfab80bedd91d66b092accc956a8338e463439c7694952f90f173` |
| Kernel | `daeb177b683dd833f44339c5d2d455debe65fb2e8348e6a1bb8c8ebfc986c6d4` |
| Query | `c656d025a851142c38487172f0bad57a18eb97ceffa9487bcb51d45b02c1bb98` |
| Runtime result | `1c21a74b09b5812f27c18d49e891cbe9cad6030364a4b6a41a895cdccb1f1921` |

## Claim boundary and remaining gate

Atlas-3 supports deterministic reproduction of a first small, useful,
source-grounded knowledge kernel. It does not establish biological validation,
coverage, accuracy, prospective discovery, or a completed assay.

Local compilation and reproduction are necessary but not the final exit gate.
The same packaged kernel and query must still pass the repository's clean
Windows/Linux CI matrix after publication. The TEM-1 assay remains
candidate-only until a separate executor/material/control/threshold contract
is preregistered and frozen before outcomes are visible.
