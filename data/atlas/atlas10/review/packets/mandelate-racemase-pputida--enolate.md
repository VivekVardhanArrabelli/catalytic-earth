# Review packet: atlas10.mandelate-racemase-pputida.enolate

- Packet ID: `review-packet:atlas10.mandelate-racemase-pputida.enolate`
- Compiled hypothesis SHA-256: `abf13fdc94787ebfb12bdaf45888c0a5c34e7c2f8bfbfebd4d930c1e38e02459`
- Source snapshot set SHA-256: `a6b6a0059835e8f3f78cd5da9897afb599560bc844c59e82ba523f9387d0550d`

## Scope

- Protein: Mandelate racemase (Pseudomonas putida)
- EC: 5.1.2.2
- UniProt: P11444
- Direct PDB: 1MNS
- Reaction status: `direct_record`
- Reaction record: `RHEA:13945`
- Equation: (S)-mandelate = (R)-mandelate

## Source proposals

### M-CSA M0187 mechanism 1

Rating `3`; detailed `true`; preferred `true`.

The mechanism shown in the following steps refers to the direction shown in overall reaction not in the reverse direction. Lys166 is the (S)-specific acid/base catalyst and His297 is the (R)-specific acid/base catalyst, thus in the reverse reaction, Lys166 deprotonates the (S)-mandelate and the intermediate is reprotonated from His297.

- Step 1 (source 1): His297 deprotonates the (R)-mandelate substrate, which results in a keto-enol tautomerisation. Sites: `P11444:H297`; source flows: `4`; inferred: `false`; atom map/bond edits: abstained.
- Step 2 (source 2): The intermediate undergoes another keto-enol tautomerisation which reprotonates the intermediate from Lys166. Sites: `P11444:K166`; source flows: `4`; inferred: `false`; atom map/bond edits: abstained.
- Step 3 (source 3): Lys166 deprotonates water, which deprotonates His297 in an inferred return step. Sites: `P11444:H297, P11444:K166`; source flows: `3`; inferred: `true`; atom map/bond edits: abstained.

## Sites and structures

- `P11444:K164` — electrostatic stabiliser, hydrogen bond donor. Mappings: 1MNS:A author 164 label 162 (direct).
- `P11444:K166` — electrostatic stabiliser, hydrogen bond acceptor, hydrogen bond donor, proton acceptor, proton donor. Mappings: 1MNS:A author 166 label 164 (direct).
- `P11444:D195` — metal ligand. Mappings: 1MNS:A author 195 label 193 (direct).
- `P11444:N197` — electrostatic stabiliser. Mappings: 1MNS:A author 197 label 195 (direct).
- `P11444:E221` — metal ligand. Mappings: 1MNS:A author 221 label 219 (direct).
- `P11444:E247` — metal ligand. Mappings: 1MNS:A author 247 label 245 (direct).
- `P11444:D270` — electrostatic stabiliser, hydrogen bond acceptor, increase basicity. Mappings: 1MNS:A author 270 label 268 (direct).
- `P11444:H297` — electrostatic stabiliser, hydrogen bond acceptor, hydrogen bond donor, proton acceptor, proton donor. Mappings: 1MNS:A author 297 label 295 (direct).
- `P11444:E317` — electrostatic stabiliser, hydrogen bond donor, proton acceptor, proton donor. Mappings: 1MNS:A author 317 label 315 (direct).

- `1MNS` (direct): Use for site geometry; do not interpret inhibitor-bound or chemically modified context as direct substrate turnover.

## Counterevidence, uncertainty, and abstention

- Counterevidence `atlas10.mandelate-racemase-pputida.enolate.structure-1mns-limit`: Use for site geometry; do not interpret inhibitor-bound or chemically modified context as direct substrate turnover.
- Open uncertainty `atlas10.mandelate-racemase-pputida.enolate.uncertainty-1`: PDB 1MNS contains inhibitor and chemical-modification context rather than a substrate turnover trajectory.
- Open uncertainty `atlas10.mandelate-racemase-pputida.enolate.uncertainty-2`: The source mechanism uses an inferred return half of the racemization cycle whose evidence must remain source-scoped.
- Open uncertainty `atlas10.mandelate-racemase-pputida.enolate.uncertainty-3`: Shared enolase-like fold and enolate stabilization with methylaspartate ammonia-lyase do not imply identical bases, substrates, or net chemistry.
- Mandatory detail abstention: The frozen source schemes preserve curved-arrow endpoints but do not establish a verified atom map, compiled bond-edit list, independent validation, or complete turnover trajectory.

## Evidence handles

- [source:UniProtKB:P11444](https://www.uniprot.org/uniprotkb/P11444/entry) — protein_identity; applicability `direct`; retrieval `bundled_snapshot`; snapshot `cb5efb114709e8f79f58376643fde10d8e2981296091d09936c41589ce7ae6ef`.
- [source:Rhea:RHEA:13945](https://www.rhea-db.org/rhea/13945) — net_reaction; applicability `direct`; retrieval `bundled_snapshot`; snapshot `dd9e64c0925d293e978fc31c518ae6e65fb5dacd87e10fd57aa6478a6ef6e98e`.
- [source:PDB:1MNS](https://www.rcsb.org/structure/1MNS) — experimental_structure; applicability `direct`; retrieval `bundled_snapshot`; snapshot `205f14186bf789b3033dcb361e726cd0179efd4a72a212b71c7376aeee2438c6`.
- [source:M-CSA:M0187](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/187/) — source_mechanism; applicability `direct`; retrieval `bundled_snapshot`; snapshot `45663712262387e7eec092c49b16994d03f9b6d186008b737b94c613a87458e3`.
- [source:DOI:10.1021/bi00102a019](https://doi.org/10.1021/bi00102a019) — primary_structure_evidence; applicability `direct`; retrieval `reference_only_verified_handle`; snapshot `None`.
- [source:CATH:CATH:3.20.20.120](https://www.cathdb.info/version/latest/superfamily/3.20.20.120) — fold_classification; applicability `direct`; retrieval `bundled_snapshot`; snapshot `8b57f92676b44fb43d4429d7403b78d6cd27040a7b3a2ec9baa82eff1787f5b4`.

## Five micro-questions

1. Is the reaction or documented source gap correct for this protein scope?
2. Are the catalytic sites and numbering mappings faithful to the cited sources?
3. Are the represented steps faithful to source granularity, with unsupported detail abstained?
4. Are structure and mechanism applicability boundaries correct?
5. Does the claim boundary prevent an unjustified evidence-tier upgrade?

## Claim boundary

Supports:

- Represent the two-base metal-stabilized racemization hypothesis and its structure-applicability boundary, then expose conserved versus repurposed features in the paired enolase query without mechanism transfer.

Does not support:

- Mechanism truth beyond the frozen sources, unrestricted transfer across proteins or substrates, or replacement of experimental validation.

Review only the bounded case and cited source scope. A correction, uncertainty, or rejection is useful. Do not infer independent validation from upstream curation, source rating, fold similarity, or another case.
