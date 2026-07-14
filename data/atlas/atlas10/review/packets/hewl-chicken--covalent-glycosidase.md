# Review packet: atlas10.hewl-chicken.covalent-glycosidase

- Packet ID: `review-packet:atlas10.hewl-chicken.covalent-glycosidase`
- Compiled hypothesis SHA-256: `d864960ad4aa4515ea1a2c00e247dcf40c2201513521d7de3bafd1192fb2deea`
- Source snapshot set SHA-256: `a6b6a0059835e8f3f78cd5da9897afb599560bc844c59e82ba523f9387d0550d`

## Scope

- Protein: Hen egg-white lysozyme (Gallus gallus)
- EC: 3.2.1.17
- UniProt: P00698
- Direct PDB: 1DPX
- Reaction status: `documented_query_gap`
- Reaction record: `None`
- Equation: NULL — documented source gap

## Source proposals

### M-CSA M0203 mechanism 1

Rating `3`; detailed `true`; preferred `true`.

Asp52 attacks the C1 of the peptidoglycan in a nucleophilic substitution that results in the NAG portion of the peptidoglycan being covalently attached to the enzyme and the NAM being released. NAM deprotonates Glu35. Glu35 deprotonates water, which attacks the C1 of the covalently bound NAG intermediate in a nucleophilic substitution that results in the NAG product and free Asp52

- Step 1 (source 1): During this step, the C1 migrates (in an electrophilic manner) from above the ring plane to below the ring plane to approach the catalytic nucleophile (Asp52), which hardly changes its position during the course of the reaction. Asp52 then attacks the C1 of the peptidoglycan in a nucleophilic substitution that results in the NAG portion of the peptidoglycan being covalently attached to the enzyme and the NAM being released. NAM deprotonates Glu35. Sites: `P00698:D70, P00698:E53`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 2 (source 2): During this step, the C1 migrates from its position below the ring plane to form a bond with a water molecule positioned in the location previously occupied by the substrate glycosidic oxygen [PMID:11518970]. Glu35 deprotonates water, which attacks the C1 of the covalently bound NAG intermediate in a nucleophilic substitution that results in the NAG product and free Asp52. Sites: `P00698:D70, P00698:E53`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.

### M-CSA M0203 mechanism 2

Rating `1`; detailed `true`; preferred `false`.

The so-called Phillips mechanism in which the enzyme proceeds via a oxycarbenium intermediate. Text book mechanism of Lysozyme, disproved.

- Step 1 (source 1): The anomeric oxygen eliminates the NAG with concomitant deprotontaion of Glu35. Sites: `P00698:E53`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.
- Step 2 (source 2): Glu35 deprotonates the catalytic water, which adds to the carbon of the oxycarbocation group. Sites: `P00698:E53`; source flows: `3`; inferred: `false`; atom map/bond edits: abstained.

## Sites and structures

- `P00698:E53` — hydrogen bond acceptor, hydrogen bond donor, proton acceptor, proton donor. Mappings: 1DPX:A author 35 label 35 (direct).
- `P00698:N64` — source listed no role string. Mappings: 1DPX:A author 46 label 46 (direct).
- `P00698:D66` — source listed no role string. Mappings: 1DPX:A author 48 label 48 (direct).
- `P00698:S68` — source listed no role string. Mappings: 1DPX:A author 50 label 50 (direct).
- `P00698:D70` — covalently attached, electrostatic stabiliser, nucleofuge, nucleophile, polar/non-polar interaction. Mappings: 1DPX:A author 52 label 52 (direct).
- `P00698:N77` — source listed no role string. Mappings: 1DPX:A author 59 label 59 (direct).

- `1DPX` (direct): The trapped covalent intermediate supports a route but does not directly observe every proton-transfer event.

## Counterevidence, uncertainty, and abstention

- Counterevidence `atlas10.hewl-chicken.covalent-glycosidase.rhea-source-gap`: No direct Rhea record was returned by this frozen EC query; this is not evidence that no reaction description exists in another source.
- Counterevidence `atlas10.hewl-chicken.covalent-glycosidase.structure-1dpx-limit`: The trapped covalent intermediate supports a route but does not directly observe every proton-transfer event.
- Counterevidence `atlas10.hewl-chicken.covalent-glycosidase.source-alternatives`: M-CSA preserves two detailed proposals with ratings 3 and 1, including a source description that calls the lower-rated Phillips route disproved.
- Open uncertainty `atlas10.hewl-chicken.covalent-glycosidase.uncertainty-1`: The selected M-CSA entry preserves mechanistic descriptions with different detail and ratings; they must remain separate source-scoped proposals.
- Open uncertainty `atlas10.hewl-chicken.covalent-glycosidase.uncertainty-2`: No direct Rhea reaction was returned by the frozen EC query, so M-CSA participant classes must not be mislabeled as a Rhea canonical reaction.
- Open uncertainty `atlas10.hewl-chicken.covalent-glycosidase.uncertainty-3`: A trapped covalent intermediate supports a route but does not observe every proton-transfer event.
- Mandatory detail abstention: The frozen source schemes preserve curved-arrow endpoints but do not establish a verified atom map, compiled bond-edit list, independent validation, or complete turnover trajectory.

## Evidence handles

- [source:UniProtKB:P00698](https://www.uniprot.org/uniprotkb/P00698/entry) — protein_identity; applicability `direct`; retrieval `bundled_snapshot`; snapshot `e101fad8a0fbe74372b6bfc96ec697883fc7c67c9656070629f7fe3cc1c0a494`.
- [source:Rhea:EC:3.2.1.17](https://www.rhea-db.org/rhea?query=ec%3A3.2.1.17) — official_net_reaction_search_gap; applicability `source_gap`; retrieval `bundled_query_gap_snapshot`; snapshot `77c567d2505f871f200cd20188a6bad47f460e73b06e2c244dae3ce2d5dce0bc`.
- [source:PDB:1DPX](https://www.rcsb.org/structure/1DPX) — experimental_structure; applicability `direct`; retrieval `bundled_snapshot`; snapshot `4225e131cc2351d4b028b3dd0fd81ffddefd2885f87be1f2e04c442949cce378`.
- [source:M-CSA:M0203](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/203/) — source_mechanism; applicability `direct`; retrieval `bundled_snapshot`; snapshot `f50de0f2b325cb7e7964a1c239acbfdc484a7513e11c9487073c8ac44f1d7df7`.
- [source:DOI:10.1038/35090602](https://doi.org/10.1038/35090602) — primary_mechanism_evidence; applicability `direct`; retrieval `reference_only_verified_handle`; snapshot `None`.
- [source:CATH:CATH:1.10.530.10](https://www.cathdb.info/version/latest/superfamily/1.10.530.10) — fold_classification; applicability `direct`; retrieval `bundled_snapshot`; snapshot `0a33d1a2d1b62d710910da5f393fb2b462e1ff97056a27a456174d2325a5a459`.

## Five micro-questions

1. Is the reaction or documented source gap correct for this protein scope?
2. Are the catalytic sites and numbering mappings faithful to the cited sources?
3. Are the represented steps faithful to source granularity, with unsupported detail abstained?
4. Are structure and mechanism applicability boundaries correct?
5. Does the claim boundary prevent an unjustified evidence-tier upgrade?

## Claim boundary

Supports:

- Compile the source gap, high-rated covalent mechanism, historical alternative, sites, and evidence as distinct queryable objects without inventing a canonical Rhea record or declaring the alternatives adjudicated.

Does not support:

- Mechanism truth beyond the frozen sources, unrestricted transfer across proteins or substrates, or replacement of experimental validation.

Review only the bounded case and cited source scope. A correction, uncertainty, or rejection is useful. Do not infer independent validation from upstream curation, source rating, fold similarity, or another case.
