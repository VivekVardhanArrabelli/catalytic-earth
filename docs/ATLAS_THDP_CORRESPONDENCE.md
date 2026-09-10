# ThDP source-step correspondence

The retained M-CSA pyruvate-dehydrogenase and transketolase drawings support a
localized **reset correspondence**. Their activation drawings support only a
partial correspondence because one explicitly includes an additional hydrogen.
These are relationships between source-proposed depictions, not observations
of conserved enzyme function or a transferable complete catalytic cycle.

| Compared proposal-1 steps | Selected covalent actor graphs | Directed arrow endpoints |
| --- | --- | --- |
| M0106 step 7 / M0219 step 6: reset | All 34 ThDP/Glu-fragment nodes and 34 bonds correspond | All five arrows, including both transferred H atoms |
| M0106 step 1 / M0219 step 1: activation | 35 versus 34 nodes; a partial 34-node projection corresponds | All five arrows, including both transferred H atoms; file order differs |

M0106 activation explicitly draws spectator H `a65` on aminopyrimidine N
`a64`; the M0219 drawing omits its counterpart. The query exposes that excluded
atom and its N–H boundary bond. It does not complete implicit hydrogens or infer
equal protonation. M0219 also permits a different direction of conjugated-bond
rearrangement; the correspondence covers the particular drawn alternative.

The two declared maps for each pair differ only in nonreacting diphosphate
oxygen locators. Both give the same reaction-endpoint mapping. Elements,
parsed formal charges (omitted `formalCharge` defaults to 0), raw
lone-pair/isotope/R-group tokens, alias presence, covalent bond orders and
complete directed arrow endpoints are checked. Source labels and alias text
remain metadata, not matched chemical attributes. The
query checks supplied maps, without claiming exhaustive isomorphism search.

## Query the relation

Run from the repository with the retained sources; no external package or
network is required:

```sh
python scripts/compare_source_steps.py --spec data/atlas/source_step_correspondence/thdp.json
python scripts/compare_source_steps.py --spec data/atlas/source_step_correspondence/thdp.json --relation reset
```

This is a repository query, not an installed-wheel command. It joins unchanged
source snapshots and compiled source records using exact bindings, then checks
the [declared atom and flow maps](../data/atlas/source_step_correspondence/thdp.json).
Output retains source labels, scheme hashes, excluded atoms, boundary bonds,
uncompared source context and the original record-level abstentions. Source
changes, omitted flow endpoints, nonbijective maps and differing directed
arrows fail. This answers a localized part of the provisional ThDP crosswalk
question that proposal-level cofactor labels do not answer; the frozen
crosswalk and original source records remain unchanged.

## Scope of reuse

Only the depicted reset and qualified activation patterns are associated.
Glu fragments are not homologous-residue or physical-atom mappings. Mg
coordination remains uncompared context; the transketolase native-metal
question stays unresolved. The substrate wedge in M0219 step 6 lies outside
the compared actors and is retained without stereo transfer.

M0106's pyruvate/decarboxylation and E2-owned lipoyl acceptor do not become
M0219's sugar-transfer chemistry. The mobile carrier's accession, attachment
site and pose remain unresolved. M0219 proposal 2, its distinct protein and
substrate context, and the separate 6HA3 study cannot supply missing grounding.
Separate inferred enzyme-reset and extra-enzymatic steps also remain separate.

A shared adjacent post-state cannot be checked from these retained panels:
M0106 step 8 retains ThDP/Glu and a distinct His128/water return, while M0219
step 7 omits ThDP/Glu. This is a terminal witness gap for after-state replay.
There is no balanced proton accounting, exact microstate, whole-cycle
equivalence, productive geometry or new experiment.
The source/diff review is computational, with possible correlated errors;
it does not raise the Tier-1 evidence status. Zero sources were reacquired.

M-CSA data are CC BY 4.0: credit Ribeiro et al., *Nucleic Acids Research*
46(D1), D618–D623 (2018), doi:10.1093/nar/gkx1012, and the retained
[M0106](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/106/) and
[M0219](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/219/) snapshots.
The new contribution is the explicit cross-record correspondence and its
limits; original source bytes and source-specific permissions are preserved.
