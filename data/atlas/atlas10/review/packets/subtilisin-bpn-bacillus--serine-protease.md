# Review packet: atlas10.subtilisin-bpn-bacillus.serine-protease

- Packet ID: `review-packet:atlas10.subtilisin-bpn-bacillus.serine-protease`
- Compiled hypothesis SHA-256: `8df3ff79a3866361f9deac6e915d186732c0979bc28136c64cadfdd4d6583df4`
- Source snapshot set SHA-256: `a6b6a0059835e8f3f78cd5da9897afb599560bc844c59e82ba523f9387d0550d`

## Scope

- Protein: Subtilisin BPN' (Bacillus amyloliquefaciens)
- EC: 3.4.21.62
- UniProt: P00782
- Direct PDB: 1SUP
- Reaction status: `documented_query_gap`
- Reaction record: `None`
- Equation: NULL — documented source gap

## Source proposals

### M-CSA M0723 mechanism 1

Rating `3`; detailed `true`; preferred `true`.

His 171 acts as a general base, deprotonating Ser 328. Ser 328 performs nucleophilic attack on the carbonyl carbon of the amide bond.  This results in a tetrahedral transition state, which is stabilised through Coulombic interactions with protonated His 171, hydrogen bonding with the backbone amide of Ser 328 and the amide side-chain of Asn 262. The transition state is also stabilised by hydrogen bonding between the P1 amide nitrogen and the carbonyl oxygen of Ser 232. His 171 is stabilised by electrostatic interactions with Asp 139.  The tetrahedral transition state collapses, forming an acyl-enzyme and His 171 acts as a general acid, protonating the amide leaving group. His 171 acts as a general base, deprotonating a water molecule. The activated water molecule performs nucleophilic attack upon the acyl enzyme, forming a tetrahedral transition state. The tetrahedral transition state collapses, forming the acid component of the substrate and Ser 328. His 171 acts as a general acid, protonating the leaving group Ser 328.

- Step 1 (source 1): His171 deprotonates Ser328 activating it to attack the carbon of the peptide bond in a nucleophilic addition. Sites: `P00782:H171, P00782:S328`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 2 (source 2): The tetrahedral transition state collapses, forming an acyl-enzyme and His171 acts as a general acid, protonating the amide leaving group Sites: `P00782:H171`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 3 (source 3): His171 abstracts a proton from a water which in turn activates it to attack the carbon of the ester bond in a nucleophilic addition to produce another transition state tetrahedral intermediate Sites: `P00782:H171`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 4 (source 4): The tetrahedral transition state collapses, forming the acid component of the substrate and Ser328. His171 acts as a general acid, protonating the leaving group Ser328 which returns the enzyme to its native state. Sites: `P00782:H171, P00782:S328`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.

## Sites and structures

- `P00782:D139` — electrostatic interaction, electrostatic stabiliser. Mappings: 1S01:A author 32 label 32 (engineered_source_reference), 1SUP:A author 32 label 32 (direct).
- `P00782:H171` — proton acceptor, proton donor. Mappings: 1S01:A author 64 label 64 (engineered_source_reference), 1SUP:A author 64 label 64 (direct).
- `P00782:N262` — electrostatic interaction, electrostatic stabiliser. Mappings: 1S01:A author 155 label 155 (engineered_source_reference), 1SUP:A author 155 label 155 (direct).
- `P00782:S328` — electrostatic interaction, electrostatic stabiliser, nucleofuge, nucleophile, proton acceptor, proton donor. Mappings: 1S01:A author 221 label 221 (engineered_source_reference), 1SUP:A author 221 label 221 (direct).

- `1SUP` (direct): Use as the direct P00782 target structure for identity and geometry, not as an uninterrupted catalytic trajectory.
- `1S01` (engineered_source_reference): Retain for M-CSA source traceability and residue numbering only; do not label it the unmodified target.

## Counterevidence, uncertainty, and abstention

- Counterevidence `atlas10.subtilisin-bpn-bacillus.serine-protease.rhea-source-gap`: No direct Rhea record was returned by this frozen EC query; this is not evidence that no reaction description exists in another source.
- Counterevidence `atlas10.subtilisin-bpn-bacillus.serine-protease.structure-1sup-limit`: Use as the direct P00782 target structure for identity and geometry, not as an uninterrupted catalytic trajectory.
- Counterevidence `atlas10.subtilisin-bpn-bacillus.serine-protease.structure-1s01-limit`: Retain for M-CSA source traceability and residue numbering only; do not label it the unmodified target.
- Open uncertainty `atlas10.subtilisin-bpn-bacillus.serine-protease.uncertainty-1`: M-CSA's reference PDB 1S01 is engineered and cannot be treated as the unmodified P00782 target structure.
- Open uncertainty `atlas10.subtilisin-bpn-bacillus.serine-protease.uncertainty-2`: The direct target structure 1SUP supports identity and geometry but not an uninterrupted catalytic trajectory.
- Open uncertainty `atlas10.subtilisin-bpn-bacillus.serine-protease.uncertainty-3`: M-CSA participant stoichiometry differs in presentation from the paired trypsin entry and must remain source-scoped rather than normalized silently.
- Mandatory detail abstention: The frozen source schemes preserve curved-arrow endpoints but do not establish a verified atom map, compiled bond-edit list, independent validation, or complete turnover trajectory.

## Evidence handles

- [source:UniProtKB:P00782](https://www.uniprot.org/uniprotkb/P00782/entry) — protein_identity; applicability `direct`; retrieval `bundled_snapshot`; snapshot `d826f1f10c912acb484de3492a511cf023d29b16369e728abec28f9124eb3b89`.
- [source:Rhea:EC:3.4.21.62](https://www.rhea-db.org/rhea?query=ec%3A3.4.21.62) — official_net_reaction_search_gap; applicability `source_gap`; retrieval `bundled_query_gap_snapshot`; snapshot `4e477f638494fcb18ee98c837dc1502c3c18debc6eb4a21c4608bb2bd707822d`.
- [source:PDB:1SUP](https://www.rcsb.org/structure/1SUP) — experimental_structure; applicability `direct`; retrieval `bundled_snapshot`; snapshot `40c3fe986db69bdcb11cbb61294dc78b1a0911c9bc255082831b7f7b4a308b8b`.
- [source:PDB:1S01](https://www.rcsb.org/structure/1S01) — engineered_source_reference_structure; applicability `engineered_source_reference`; retrieval `bundled_snapshot`; snapshot `d715f581e1c9976eadfc888a379e5b1738c32a31ce31ffe2c510014111c70dca`.
- [source:M-CSA:M0723](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/723/) — source_mechanism; applicability `direct`; retrieval `bundled_snapshot`; snapshot `ad94c81dcdd316d18dbc054f0d22086210f4901dd47a56c1060f53fa3e7c6258`.
- [source:DOI:10.1107/S0907444996007500](https://doi.org/10.1107/S0907444996007500) — primary_structure_evidence; applicability `direct`; retrieval `reference_only_verified_handle`; snapshot `None`.
- [source:DOI:10.1073/pnas.83.11.3743](https://doi.org/10.1073/pnas.83.11.3743) — primary_mechanism_evidence; applicability `direct`; retrieval `reference_only_verified_handle`; snapshot `None`.
- [source:CATH:CATH:3.40.50.200](https://www.cathdb.info/version/latest/superfamily/3.40.50.200) — fold_classification; applicability `direct`; retrieval `bundled_snapshot`; snapshot `77f982742ddff893e9a5e05ccf45600fa7a5dd5e53084f40619ca0ff76106bb4`.

## Five micro-questions

1. Is the reaction or documented source gap correct for this protein scope?
2. Are the catalytic sites and numbering mappings faithful to the cited sources?
3. Are the represented steps faithful to source granularity, with unsupported detail abstained?
4. Are structure and mechanism applicability boundaries correct?
5. Does the claim boundary prevent an unjustified evidence-tier upgrade?

## Claim boundary

Supports:

- Compile an unmodified-target record grounded to P00782/1SUP, preserve 1S01 as engineered source-reference counterevidence, and answer the convergence query without importing trypsin-specific numbering, steps, or evidence.

Does not support:

- Mechanism truth beyond the frozen sources, unrestricted transfer across proteins or substrates, or replacement of experimental validation.

Review only the bounded case and cited source scope. A correction, uncertainty, or rejection is useful. Do not infer independent validation from upstream curation, source rating, fold similarity, or another case.
