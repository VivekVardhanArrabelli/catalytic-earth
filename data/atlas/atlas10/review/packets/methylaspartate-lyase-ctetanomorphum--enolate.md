# Review packet: atlas10.methylaspartate-lyase-ctetanomorphum.enolate

- Packet ID: `review-packet:atlas10.methylaspartate-lyase-ctetanomorphum.enolate`
- Compiled hypothesis SHA-256: `491bdc5276ad225f1cc3f59a3a0b3859eada3b0ca027d3fbca0af7acc05dbb96`
- Source snapshot set SHA-256: `a6b6a0059835e8f3f78cd5da9897afb599560bc844c59e82ba523f9387d0550d`

## Scope

- Protein: Methylaspartate ammonia-lyase (Clostridium tetanomorphum)
- EC: 4.3.1.2
- UniProt: Q05514
- Direct PDB: 1KCZ
- Reaction status: `direct_record`
- Reaction record: `RHEA:12829`
- Equation: (2S,3S)-3-methyl-L-aspartate = mesaconate + NH4(+)

## Source proposals

### M-CSA M0468 mechanism 2

Rating `3`; detailed `true`; preferred `true`.

Lys 331 acts as a general base to remove the 3-proton from 3-methyl aspartate to generate an enolic intermediate. An Mg(II) cation and His 194 provide positive charges to stabilise the accumulation of negative charge on the substrate carboxyl group during the formation of this intermediate. Collapse of the enolate leads to elimination of ammonia in an E1cB mechanism.

- Step 1 (source 1): Lys331 abstracts the alpha proton from the substrate. Sites: `Q05514:K331`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 2 (source 2): The negatively charged intermediate collapses, eliminating ammonia. Sites: `none source-resolved`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 3 (source 3): Inferred return step, using the product ammonia as the base. Sites: `none source-resolved`; source flows: `2`; inferred: `true`; atom map/bond edits: abstained.

## Sites and structures

- `Q05514:Q172` — electrostatic stabiliser. Mappings: 1KCZ:A author 172 label 172 (direct), 1KCZ:B author 172 label 172 (direct).
- `Q05514:H194` — electrostatic stabiliser. Mappings: 1KCZ:A author 194 label 194 (direct), 1KCZ:B author 194 label 194 (direct).
- `Q05514:D238` — metal ligand. Mappings: 1KCZ:A author 238 label 238 (direct), 1KCZ:B author 238 label 238 (direct).
- `Q05514:E273` — metal ligand. Mappings: 1KCZ:A author 273 label 273 (direct), 1KCZ:B author 273 label 273 (direct).
- `Q05514:D307` — metal ligand. Mappings: 1KCZ:A author 307 label 307 (direct), 1KCZ:B author 307 label 307 (direct).
- `Q05514:Q329` — electrostatic stabiliser. Mappings: 1KCZ:A author 329 label 329 (direct), 1KCZ:B author 329 label 329 (direct).
- `Q05514:K331` — electrostatic stabiliser, proton acceptor, proton donor. Mappings: 1KCZ:A author 331 label 331 (direct), 1KCZ:B author 331 label 331 (direct).

- `1KCZ` (direct): Use for both domain anchors and catalytic sites; shared catalytic fold does not collapse the additional N-terminal domain.

## Counterevidence, uncertainty, and abstention

- Counterevidence `atlas10.methylaspartate-lyase-ctetanomorphum.enolate.structure-1kcz-limit`: Use for both domain anchors and catalytic sites; shared catalytic fold does not collapse the additional N-terminal domain.
- Open uncertainty `atlas10.methylaspartate-lyase-ctetanomorphum.enolate.uncertainty-1`: The selected protein includes an additional N-terminal domain beyond the shared enolase-like catalytic domain.
- Open uncertainty `atlas10.methylaspartate-lyase-ctetanomorphum.enolate.uncertainty-2`: The source mechanism includes an inferred return or regeneration step whose support must remain explicit.
- Open uncertainty `atlas10.methylaspartate-lyase-ctetanomorphum.enolate.uncertainty-3`: A common metal-stabilized enolate strategy with mandelate racemase does not make elimination and racemization interchangeable.
- Mandatory detail abstention: The frozen source schemes preserve curved-arrow endpoints but do not establish a verified atom map, compiled bond-edit list, independent validation, or complete turnover trajectory.

## Evidence handles

- [source:UniProtKB:Q05514](https://www.uniprot.org/uniprotkb/Q05514/entry) — protein_identity; applicability `direct`; retrieval `bundled_snapshot`; snapshot `178ee97c99c10d3bdd41a274745e89f5ebe745b766ee5a085886b0cd756c59dd`.
- [source:Rhea:RHEA:12829](https://www.rhea-db.org/rhea/12829) — net_reaction; applicability `direct`; retrieval `bundled_snapshot`; snapshot `d40c4e9c3ce2e70eb01be9df24c1a6ace25f97a07457e4c2ce4473f2aa8a9520`.
- [source:PDB:1KCZ](https://www.rcsb.org/structure/1KCZ) — experimental_structure; applicability `direct`; retrieval `bundled_snapshot`; snapshot `6e67d7bfd6b43f0de7a2c4d73e21d533227fb4e0d4a7ad269fb4a344b66861c8`.
- [source:M-CSA:M0468](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/468/) — source_mechanism; applicability `direct`; retrieval `bundled_snapshot`; snapshot `1e6fc303f8f7416b19b701b5921a309b439743941f3c5253e8d353318ca9e9d7`.
- [source:DOI:10.1074/jbc.m111180200](https://doi.org/10.1074/jbc.m111180200) — primary_structure_evidence; applicability `direct`; retrieval `reference_only_verified_handle`; snapshot `None`.
- [source:CATH:CATH:3.20.20.120](https://www.cathdb.info/version/latest/superfamily/3.20.20.120) — fold_classification; applicability `direct`; retrieval `bundled_snapshot`; snapshot `8b57f92676b44fb43d4429d7403b78d6cd27040a7b3a2ec9baa82eff1787f5b4`.
- [source:CATH:CATH:3.30.390.10](https://www.cathdb.info/version/latest/superfamily/3.30.390.10) — fold_classification; applicability `direct`; retrieval `bundled_snapshot`; snapshot `b8bc2e1b1a2286fe9d9a1cf252977aada355cfa1ac5d599bb10e01d1895df764`.

## Five micro-questions

1. Is the reaction or documented source gap correct for this protein scope?
2. Are the catalytic sites and numbering mappings faithful to the cited sources?
3. Are the represented steps faithful to source granularity, with unsupported detail abstained?
4. Are structure and mechanism applicability boundaries correct?
5. Does the claim boundary prevent an unjustified evidence-tier upgrade?

## Claim boundary

Supports:

- Represent the magnesium-stabilized E1cB elimination, both domain anchors, and inferred-step uncertainty, then expose conserved versus repurposed features in the paired enolase query without forcing a historical fingerprint assignment.

Does not support:

- Mechanism truth beyond the frozen sources, unrestricted transfer across proteins or substrates, or replacement of experimental validation.

Review only the bounded case and cited source scope. A correction, uncertainty, or rejection is useful. Do not infer independent validation from upstream curation, source rating, fold similarity, or another case.
