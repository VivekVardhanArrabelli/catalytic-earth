# Atlas-50 source challenge — 2026-09-05

This is a targeted computational challenge of eight decision-changing Atlas-50 issues. It is informed by the earlier 57-row crosswalk audit, so it is **not blind**. All computational reviewers in this run are same-model Codex agents. Their errors may be correlated; their agreement is not statistical independence, expert consensus, or human review. These decisions support corrected source-specific development work only. They do not confer independent-validation or gold status, authenticate a reviewer, or change the selection freeze.

The inspection used repository contracts, official M-CSA and RCSB records, and primary papers or authoritative primary-paper abstracts where the result could change a decision. It was bounded to public sources and less than 30 MiB of requests, with no paid access, literature corpus download, GPU work, or outreach. This is not a systematic literature review.

## Decisions

These are challenge recommendations. The later
[coordinating adjudication](COMPUTATIONAL_DEVELOPMENT_REVIEW.md) controls
operations: M0064 is annotation-only in this release, and M0753 carries an
additional abstention for conflicting source Asp11/Asp130 role assignments.

| Issue | Verdict | Development decision | Remaining boundary |
|---|---|---|---|
| M0049 as a PLP source | **Contradicted** | Remove M0049 from the PLP crosswalk. Retain it in the panel as a pyruvoyl/PTM covalent-cofactor case. | Do not describe pyruvoyl maturation as redox cycling without a source. |
| M0112 exact DHFR equivalence | **Supported at reaction-core granularity** | Keep `exact_duplicate` only for EC 1.5.1.3 NADPH-dependent DHF-to-THF chemistry. This revises the earlier audit's blanket aggregation proposal after reinspection of the implemented fingerprint boundary. | Protein/organism/resistance/fusion/structure applicability is narrower than reaction-core equivalence. |
| M0112 direct Asp/Glu proton donation | **Contradicted** | Encode water/solvent as the N5 proton source and Asp26/Asp27 as the pKa/electrostatic/water-network organizer. | Preserve species-specific numbering and evidence scope. |
| M0753 as a full HisH-HisF channel handle | **Contradicted** | Admit M0753 as the detailed HisF/free-ammonium cyclase half-reaction. Use 1GPW and HisH Q9X0C8 as separate context if a full-complex record is built. | 2A0N is HisF alone. Full channel/allostery and transported-ammonia claims must abstain unless separately sourced. |
| M0107 and M0212 having the same component-state burden | **Contradicted** | Encode M0107 as a fixed CODH assembly; encode M0212 as an ATP-coupled transient association cycle. Both can be development candidates with source-specific uncertainty. | M0107 has alternative/inferred cofactor steps. M0212's exact FeMo chemistry remains explicitly unclear and must abstain. |
| M0064's current reaction object completely representing topology | **Contradicted** | Keep M0064 as a development stressor and compile its sourced covalent cleavage/religation chemistry. Add typed topology and strand-role states. | CHEBI:9160 on both sides and apo 1D6M do not establish before/after topology or a DNA-bound structural state. |
| 1W85 containing the M0106 lipoyl carrier | **Contradicted** | Keep M0106 for development. Record P11961 as E2 binding-domain structure context and represent the substrate as an E2-owned tethered carrier. | Abstain from a Tier-2 lipoyl-carrier pose: the mobile lipoyl domain is absent from 1W85. |
| M0970/3VMT closing a complete polymer instance | **Insufficient** | Permit source annotation and retain the local SN2/SNi alternatives. | CHEBI:X00676, chain-length transition, initiation versus elongation, and processivity remain unresolved; mechanism drafting stays blocked. |

The useful resolution is scoped admission with explicit abstentions. A row does not need to be discarded merely because one evidence tier or state field is unresolved. The unresolved field must remain visible and must not be promoted by agent agreement.

## Evidence and counterarguments

### M0049: pyruvoyl chemistry, not PLP

[M-CSA 49](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/49/) identifies a covalently bound pyruvoyl group and a substrate-pyruvoyl Schiff base. The [1989 structure/mechanism paper](https://pubmed.ncbi.nlm.nih.gov/2745463/) calls the enzyme pyruvoyl-dependent, and a [later structure paper](https://pubmed.ncbi.nlm.nih.gov/8464063/) describes autocatalytic serine cleavage that creates the pyruvoyl cofactor. This directly falsifies the PLP mapping. It does not falsify the scientific value of M0049 itself.

### M0112: exact reaction core, corrected proton role

[M-CSA 112](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/112/) matches EC 1.5.1.3 NADPH-dependent dihydrofolate reduction. The repository's implemented DHFR admission contract also requires that narrow reaction center and excludes side-reaction contexts. On that explicitly named granularity, exact duplication is defensible. It does not transfer one bacterial structure across all protein contexts.

The proton-role objection is decisive. M-CSA assigns N5 proton donation to conserved water. The [kinetic study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4280594/) supports solvent-assisted delivery with Asp27/Tyr100 electrostatic and orienting roles, and [neutron/X-ray crystallography](https://pmc.ncbi.nlm.nih.gov/articles/PMC4280638/) identifies water positioned for N5 protonation. Calling Asp26/Asp27 the direct donor changes the mechanism.

### M0753: half-reaction and full channel are different source objects

[M-CSA 753](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/753/) gives a detailed HisF reaction with ammonium, and [RCSB 2A0N](https://www.rcsb.org/structure/2A0N) is a monomeric HisF-only structure. The M-CSA introduction notes physiological delivery from HisH, but neither selected identity nor selected structure is a full-complex observation.

[RCSB 1GPW](https://www.rcsb.org/structure/1GPW) is the separate T. maritima HisH-HisF heterodimer and identifies HisH as Q9X0C8. Its primary paper supports a *putative* 25 Å tunnel. A [contemporaneous primary simulation study](https://pmc.ncbi.nlm.nih.gov/articles/PMC164632/) distinguishes the two half-reactions and explicitly says conclusive experimental channeling evidence was then absent. The development record can therefore admit the sourced HisF half-reaction now while keeping channel/allostery fields abstained or separately sourced.

### M0107 versus M0212: fixed assembly versus nucleotide-driven partner cycle

[M-CSA 107](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/107/) and the [1N62 primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC138549/) describe aerobic CODH as a dimer of LMS heterotrimers with an intra-assembly Mo/Cu → two Fe-S clusters → FAD relay. By contrast, [M-CSA 212](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/212/) describes repeated Fe-protein/MoFe-protein association, ATP hydrolysis, electron delivery, dissociation, nucleotide exchange, and re-reduction. The [ADP·AlF4-stabilized complex paper](https://www.nature.com/articles/387370a0) directly ties nucleotide-switch conformational change to interprotein transfer.

A generic `multi_component` flag hides this material difference. A typed fixed assembly versus cycle-coupled association distinction resolves the representation objection for development. It does not validate every atomic cofactor step: M-CSA gives CODH alternatives and inferred steps, and explicitly says the exact atoms and much of the nitrogenase FeMo mechanism remain unclear.

### M0064: chemical steps do not encode topology

[M-CSA 64](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/64/) places the same single-stranded-DNA identifier on both sides while describing covalent cleavage, strand movement/uncoiling, and religation. [RCSB 1D6M and its primary paper](https://www.rcsb.org/structure/1D6M) establish the intact topoisomerase III fold and its capacity to relax, catenate, and decatenate, but the structure is an apo monomer and the paper says residue-role evidence was incomplete.

M0064 is still useful for development. Its local transesterification chemistry can be compiled, while complete Tier-0 outcome claims require typed substrate-segment roles and before/after linking or catenation state. Those values and DNA-bound Tier-2 applicability must remain explicit abstentions until directly sourced.

### M0106: the E2 binding domain is not the lipoyl carrier

[M-CSA 106](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/106/) consumes an E2-tethered lipoyl-Lys residue. [RCSB 1W85](https://www.rcsb.org/structure/1W85) contains E1 alpha/beta and a 49-residue P11961 **peripheral subunit-binding domain**; it contains no lipoyl-domain entity or lipoyl-Lys ligand. A [primary sequence/proteolysis study in the same species](https://pubmed.ncbi.nlm.nih.gov/3421911/) distinguishes the N-terminal lipoyl domain from the roughly 50-residue E1/E3-binding domain.

P11961 should be `structure_context_only`, not the carrier assignment. M0106 can still be admitted for source-specific development with the reaction participant represented as an E2-owned tethered carrier and with the 1W85 lipoyl-carrier pose marked unavailable.

### M0970: local transfer chemistry does not close the polymer instance

[M-CSA 970](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/970/) supports peptidoglycan glycosyltransferase identity and competing local SN2/SNi proposals, but its product is placeholder CHEBI:X00676 and the equation does not instantiate the incoming and outgoing polymer lengths. [RCSB 3VMT and its primary paper](https://www.rcsb.org/structure/3VMT) support a monofunctional glycosyltransferase bound to a Lipid II analog and the local donor/acceptor-site mechanism. They do not observe a processive trajectory or establish initiation, elongation, product chain length, or processivity. Source annotation can proceed, while a complete reaction-instance or source-scoped mechanism draft remains blocked.

## Peer-artifact cross-check

The corrected crosswalk v2 is consistent with the source challenge after two material corrections made during review. It now quarantines M0049 and every M0049-derived locator from the PLP row while preserving M0049 as a pyruvoyl panel candidate. M0112 appears once as an `exact_duplicate` at the explicit EC 1.5.1.3 reaction-core scope; it assigns N5 proton delivery to water and limits Asp26/Asp27 to the electrostatic and water-network role. Its machine-readable provenance records same-model agents, correlated-error risk, no statistical independence, no human reviewers, and no experimental validation. The deterministic builder check and all nine focused tests pass.

The state probe also agrees with the source challenge after adding mandatory computational-review provenance. Its six outcomes are one narrowly defined `PASS`, four `SCOPED_PASS` cases, and one `ABSTAIN`:

- M0064 permits source annotation only; topology and DNA-bound structural applicability remain abstained.
- M0106 permits a source-scoped carrier-state draft while carrier identity, numbered attachment site, and structural localization remain abstained.
- M0107 represents a fixed multisubunit assembly and source-proposal redox states. Its `PASS` authorizes only source annotation and a source-scoped proposal draft.
- M0212 represents the ATP-coupled association cycle while the complete FeMo/P-cluster state remains abstained.
- M0753 is narrowed to the HisF/free-ammonium half-reaction and does not project a full HisH-HisF channel into 2A0N.
- M0970 permits source annotation only; exact reaction-instance and mechanism-draft operations remain blocked.

The state-probe builder check and all nine focused tests pass. The JSON `cross_review` object pins the reviewed output hashes and records the one remaining material objection for M0970. This is an informed same-model consistency review. It remains correlated computational evidence and grants no human, expert, independent-validation, gold, tier, freeze, or mechanism-completion status.
