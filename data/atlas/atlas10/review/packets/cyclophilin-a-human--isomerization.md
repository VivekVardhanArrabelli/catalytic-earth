# Review packet: atlas10.cyclophilin-a-human.isomerization

- Packet ID: `review-packet:atlas10.cyclophilin-a-human.isomerization`
- Compiled hypothesis SHA-256: `e51bfc88601e9c76a5088adadac633f8f83a288ae72f5b9bd49b697460fac3b1`
- Source snapshot set SHA-256: `a6b6a0059835e8f3f78cd5da9897afb599560bc844c59e82ba523f9387d0550d`

## Scope

- Protein: Human cyclophilin A (Homo sapiens)
- EC: 5.2.1.8
- UniProt: P62937
- Direct PDB: 1M9C
- Reaction status: `direct_record`
- Reaction record: `RHEA:16237`
- Equation: [protein]-peptidylproline (omega=180) = [protein]-peptidylproline (omega=0)

## Source proposals

### M-CSA M0189 mechanism 1

Rating `3`; detailed `false`; preferred `true`.

The 'reaction' is only a rotation of a peptide bond preceding the substrate proline. The proline itself remains more or less stationary, with the N-terminal residues rotating anticlockwise 180 degrees. The catalysis is mainly through stabilisation of the transition state. There is also a steric clash between the side chain of the residue preceding the substrate Pro and Arg 55 in the trans conformation. (HIV-1 CA protein has a Gly residue in this position so binding of the trans conformation is more favourable compared to other substrates.)

- No discrete steps compiled; see the mandatory detail abstention below.

## Sites and structures

- `P62937:R55` — electrostatic stabiliser, hydrogen bond donor, steric role. Mappings: 1M9C:A author 55 label 55 (direct), 1M9C:B author 55 label 55 (direct).
- `P62937:F60` — polar/non-polar interaction, steric role. Mappings: 1M9C:A author 60 label 60 (direct), 1M9C:B author 60 label 60 (direct).
- `P62937:Q63` — electrostatic stabiliser, hydrogen bond acceptor, hydrogen bond donor. Mappings: 1M9C:A author 63 label 63 (direct), 1M9C:B author 63 label 63 (direct).
- `P62937:N102` — electrostatic stabiliser, hydrogen bond acceptor, hydrogen bond donor. Mappings: 1M9C:A author 102 label 102 (direct), 1M9C:B author 102 label 102 (direct).
- `P62937:F113` — polar/non-polar interaction, steric role. Mappings: 1M9C:A author 113 label 113 (direct), 1M9C:B author 113 label 113 (direct).
- `P62937:L122` — polar/non-polar interaction, steric role. Mappings: 1M9C:A author 122 label 122 (direct), 1M9C:B author 122 label 122 (direct).
- `P62937:H126` — polar/non-polar interaction, steric role. Mappings: 1M9C:A author 126 label 126 (direct), 1M9C:B author 126 label 126 (direct).

- `1M9C` (direct): Direct for unmutated human cyclophilin A in this HIV-1 capsid complex; do not generalize the substrate context to every cyclophilin target.

## Counterevidence, uncertainty, and abstention

- Counterevidence `atlas10.cyclophilin-a-human.isomerization.structure-1m9c-limit`: Direct for unmutated human cyclophilin A in this HIV-1 capsid complex; do not generalize the substrate context to every cyclophilin target.
- Counterevidence `atlas10.cyclophilin-a-human.isomerization.non-detailed-source`: M-CSA M0189 is explicitly non-detailed and its linked Marvin scheme returns HTTP 404 in the frozen acquisition.
- Open uncertainty `atlas10.cyclophilin-a-human.isomerization.uncertainty-1`: M-CSA M0189 is high-rated but explicitly non-detailed; rating and mechanistic granularity are different dimensions.
- Open uncertainty `atlas10.cyclophilin-a-human.isomerization.uncertainty-2`: Peptidyl-proline isomerization does not require a conventional net bond-change list, and forcing one would misrepresent the chemistry.
- Open uncertainty `atlas10.cyclophilin-a-human.isomerization.uncertainty-3`: PDB 1M9C has an HIV-1 capsid substrate context that cannot be generalized silently to every cyclophilin target.
- Mandatory detail abstention: M-CSA explicitly marks the selected proposal non-detailed and the linked scheme was unavailable; rating 3 does not authorize fabrication of discrete chemistry.

## Evidence handles

- [source:UniProtKB:P62937](https://www.uniprot.org/uniprotkb/P62937/entry) — protein_identity; applicability `direct`; retrieval `bundled_snapshot`; snapshot `fd854c2994f70b48d8514f594e41b4ce64066f984148e4c97d03db1e2cdbefc1`.
- [source:Rhea:RHEA:16237](https://www.rhea-db.org/rhea/16237) — net_reaction; applicability `direct`; retrieval `bundled_snapshot`; snapshot `17e11f814f4685614e1604dc416da979adeee7fa644956bab8b7082410979e6c`.
- [source:PDB:1M9C](https://www.rcsb.org/structure/1M9C) — experimental_structure; applicability `direct`; retrieval `bundled_snapshot`; snapshot `8a6b4c51252b08b7f98d1f20537565c4d206229122da7d00a8f38a42d43f14dc`.
- [source:M-CSA:M0189](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/189/) — source_mechanism; applicability `direct_non_detailed`; retrieval `bundled_snapshot`; snapshot `929daa856c1096a4eabae1ec8308cd5b1a0fd2a0176697013d698845080353d6`.
- [source:DOI:10.1038/nsb927](https://doi.org/10.1038/nsb927) — primary_structure_evidence; applicability `direct`; retrieval `reference_only_verified_handle`; snapshot `None`.
- [source:CATH:CATH:2.40.100.10](https://www.cathdb.info/version/latest/superfamily/2.40.100.10) — fold_classification; applicability `direct`; retrieval `bundled_snapshot`; snapshot `b75adfd431aeef86287662fc375c078ca39e597e73b051f45dfc85c0bde8c4b9`.

## Five micro-questions

1. Is the reaction or documented source gap correct for this protein scope?
2. Are the catalytic sites and numbering mappings faithful to the cited sources?
3. Are the represented steps faithful to source granularity, with unsupported detail abstained?
4. Are structure and mechanism applicability boundaries correct?
5. Does the claim boundary prevent an unjustified evidence-tier upgrade?

## Claim boundary

Supports:

- Produce a site-grounded Tier-2 transition-state/isomerization hypothesis with a valid reaction and applicability record, zero fabricated discrete electron-flow edits, and a machine-visible mandatory abstention from unsupported detail.

Does not support:

- Mechanism truth beyond the frozen sources, unrestricted transfer across proteins or substrates, or replacement of experimental validation.

Review only the bounded case and cited source scope. A correction, uncertainty, or rejection is useful. Do not infer independent validation from upstream curation, source rating, fold similarity, or another case.
