# Review packet: atlas10.trypsin-fusarium.serine-protease

- Packet ID: `review-packet:atlas10.trypsin-fusarium.serine-protease`
- Compiled hypothesis SHA-256: `9bdfef07aa59ff535e3f42047e69b0ebb4aa50b8bcf2e529c7a8a8e3153910b9`
- Source snapshot set SHA-256: `a6b6a0059835e8f3f78cd5da9897afb599560bc844c59e82ba523f9387d0550d`

## Scope

- Protein: Fusarium oxysporum trypsin (Fusarium oxysporum)
- EC: 3.4.21.4
- UniProt: P35049
- Direct PDB: 1PQ5
- Reaction status: `documented_query_gap`
- Reaction record: `None`
- Equation: NULL — documented source gap

## Source proposals

### M-CSA M0173 mechanism 1

Rating `3`; detailed `true`; preferred `true`.

The key feature of the mechanism is the presence of the catalytic triad of serine, histidine and  aspartate. Serine, having been deprotonated by histidine, attacks the carbonyl of the substrate. The negatively charged tetrahedral intermediate is stabilised by the oxyanion hole, while the positive charge on histidine is stabilised by the aspartate residue. When the tetrahedral intermediate collapses, the amide bond of the substrate is broken. The acylenzyme intermediate is hydrolysed by a water molecule, activated by histidine, to release the product and restore the enzyme to its active state.

- Step 1 (source 1): His56 in a Ser-His-Asp triad deprotonates Ser195. Activated Ser195 then attacks the carbonyl carbon of the peptide bond in a nucleophilic addition. Sites: `P35049:H65, P35049:S204`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 2 (source 2): The oxyanion initiates an elimination reaction that cleaves the peptide bond, releasing the new N-terminus of the protein, which protonates from His56. Sites: `P35049:H65`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 3 (source 3): His56 deprotonates water, which attacks the carbonyl carbon bound to Ser195 in a nucleophilic addition. Sites: `P35049:H65, P35049:S204`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 4 (source 4): The oxyanion initiates an elimination that cleaves the acyl bond to Ser195, releasing the C-terminus of the protein. Ser195 then deprotonates His56, regenerating the active site. Sites: `P35049:H65, P35049:S204`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.

## Sites and structures

- `P35049:H65` — hydrogen bond acceptor, hydrogen bond donor, proton acceptor, proton donor. Mappings: 1PQ5:A author 56 label 41 (direct).
- `P35049:D108` — activator, electrostatic stabiliser, hydrogen bond acceptor. Mappings: 1PQ5:A author 99 label 84 (direct).
- `P35049:Q201` — electrostatic stabiliser, hydrogen bond donor, transition state stabiliser. Mappings: 1PQ5:A author 192 label 177 (direct).
- `P35049:G202` — electrostatic stabiliser, hydrogen bond donor, transition state stabiliser. Mappings: 1PQ5:A author 193 label 178 (direct).
- `P35049:D203` — electrostatic stabiliser, hydrogen bond donor, transition state stabiliser. Mappings: 1PQ5:A author 194 label 179 (direct).
- `P35049:S204` — covalently attached, electrostatic stabiliser, hydrogen bond acceptor, hydrogen bond donor, nucleofuge, nucleophile, proton acceptor, proton donor, transition state stabiliser. Mappings: 1PQ5:A author 195 label 180 (direct).

- `1PQ5` (direct): The 0.85 A pH-5 structure grounds sites but does not alone establish productive physiological protonation through turnover.

## Counterevidence, uncertainty, and abstention

- Counterevidence `atlas10.trypsin-fusarium.serine-protease.rhea-source-gap`: No direct Rhea record was returned by this frozen EC query; this is not evidence that no reaction description exists in another source.
- Counterevidence `atlas10.trypsin-fusarium.serine-protease.structure-1pq5-limit`: The 0.85 A pH-5 structure grounds sites but does not alone establish productive physiological protonation through turnover.
- Open uncertainty `atlas10.trypsin-fusarium.serine-protease.uncertainty-1`: M-CSA participant classes supply source-scoped peptide hydrolysis context but the frozen Rhea query supplies no direct canonical reaction.
- Open uncertainty `atlas10.trypsin-fusarium.serine-protease.uncertainty-2`: The high-resolution structure is condition-specific and does not uniquely establish productive protonation through turnover.
- Open uncertainty `atlas10.trypsin-fusarium.serine-protease.uncertainty-3`: The catalytic strategy converges with subtilisin, but fold, numbering, substrate context, and evidence remain protein-specific.
- Mandatory detail abstention: The frozen source schemes preserve curved-arrow endpoints but do not establish a verified atom map, compiled bond-edit list, independent validation, or complete turnover trajectory.

## Evidence handles

- [source:UniProtKB:P35049](https://www.uniprot.org/uniprotkb/P35049/entry) — protein_identity; applicability `direct`; retrieval `bundled_snapshot`; snapshot `2be2f38c0c1c8d66b7a69bd8af2eea08b445992f517e7e876c684b738cec5ffd`.
- [source:Rhea:EC:3.4.21.4](https://www.rhea-db.org/rhea?query=ec%3A3.4.21.4) — official_net_reaction_search_gap; applicability `source_gap`; retrieval `bundled_query_gap_snapshot`; snapshot `e4a7f09fdc7b8968fc95f8aff17899807034ba433a12a374b4681c77d7839dc8`.
- [source:PDB:1PQ5](https://www.rcsb.org/structure/1PQ5) — experimental_structure; applicability `direct`; retrieval `bundled_snapshot`; snapshot `b6b8b1fe752907f1252b83807f06c3fe78de2f0b980b07f282f9600b35566946`.
- [source:M-CSA:M0173](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/173/) — source_mechanism; applicability `direct`; retrieval `bundled_snapshot`; snapshot `d3db64e9a1db6e22e8baae48a738bff261a2296f375a884c19f2f4abc7d8f22e`.
- [source:DOI:10.1074/jbc.m306944200](https://doi.org/10.1074/jbc.m306944200) — primary_structure_evidence; applicability `direct`; retrieval `reference_only_verified_handle`; snapshot `None`.
- [source:CATH:CATH:2.40.10.10](https://www.cathdb.info/version/latest/superfamily/2.40.10.10) — fold_classification; applicability `direct`; retrieval `bundled_snapshot`; snapshot `a6c1336d96e6d54452b1285c1cca6acb68ed71886fcad5c1999b698c38247b3e`.

## Five micro-questions

1. Is the reaction or documented source gap correct for this protein scope?
2. Are the catalytic sites and numbering mappings faithful to the cited sources?
3. Are the represented steps faithful to source granularity, with unsupported detail abstained?
4. Are structure and mechanism applicability boundaries correct?
5. Does the claim boundary prevent an unjustified evidence-tier upgrade?

## Claim boundary

Supports:

- Produce a source-faithful trypsin mechanism and site mapping that can participate in the cross-fold convergence query while preserving the Rhea gap and refusing any residue or evidence transfer from subtilisin.

Does not support:

- Mechanism truth beyond the frozen sources, unrestricted transfer across proteins or substrates, or replacement of experimental validation.

Review only the bounded case and cited source scope. A correction, uncertainty, or rejection is useful. Do not infer independent validation from upstream curation, source rating, fold similarity, or another case.
