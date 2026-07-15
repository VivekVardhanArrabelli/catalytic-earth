# Source data rights and attribution matrix

**Checked:** 2026-07-14

This is an engineering control, not legal advice. Code licensing does not
relicense upstream data. A release may include a source-derived record only
when its exact source release, license, attribution, and redistribution status
are recorded. Unknown means blocked, not implicitly open.

| Source | Current terms checked | Attribution | Bundled redistribution policy |
|---|---|---|---|
| UniProt | [CC BY 4.0 for copyrightable database parts](https://www.uniprot.org/help/license) | Credit UniProt and cite the relevant release/publication | Allowed with attribution and change notice; preserve warnings about patents and third-party rights |
| Rhea | [CC BY 4.0](https://www.rhea-db.org/help/license-disclaimer) | Credit Rhea and cite the release/publication | Allowed with attribution and change notice |
| M-CSA | [CC BY 4.0](https://www.ebi.ac.uk/thornton-srv/m-csa/) | Credit M-CSA and cite Ribeiro et al. plus the accessed release | Allowed with attribution and change notice |
| PDB archive | [Archive data files are CC0 1.0](https://www.rcsb.org/pages/policies) | Cite PDB IDs, structure authors/publications, and RCSB/wwPDB as requested | Allowed for PDB archive files; integrated external API fields retain provider terms |
| CATH | [CC BY 4.0](https://www.cathdb.info/version/latest/home) | Credit CATH-Gene3D, cite the applicable release/publication, and preserve superfamily identifiers | Allowed with attribution and change notice; freeze the accessed version because `latest` classifications can change |
| AlphaFold DB | [CC BY 4.0; academic and commercial use](https://alphafold.ebi.ac.uk/) | Credit AlphaFold DB/EMBL-EBI/Google DeepMind and cite the resource and applicable model publication | Allowed with attribution, confidence/disclaimer text, and change notice |
| BRENDA | [CC BY 4.0 for copyrightable parts](https://www.brenda-enzymes.org/license.php) | Credit BRENDA and cite the current release/publication | Allowed only after the download-time acceptance is recorded; preserve DSI/benefit-sharing and third-party cautions |
| SABIO-RK | Current license page could not be reliably retrieved; release-specific terms remain unresolved | Cite SABIO-RK and source publications when referenced | **Blocked from bundled redistribution** until current written terms and commercial scope are captured |
| ChEBI | [CC BY 4.0](https://www.ebi.ac.uk/ols4/ontologies/chebi) | Credit ChEBI/EMBL-EBI and cite release/version | Allowed with attribution and change notice |
| MGnify | [EMBL-EBI terms](https://www.ebi.ac.uk/about/terms-of-use/) impose no extra restriction beyond original owners | Credit MGnify/EMBL-EBI and each underlying dataset as required | Conditional: include only records whose original-owner terms are captured; otherwise reference/fetch instructions only |
| CAZy | Site shows [copyright ownership](https://www.cazy.org/About-Us.html) but no general open-data license was located | Cite CAZy and relevant source publications | **Reference-only; no bundled CAZy table redistribution** without permission or explicit release terms |
| PAZy | [Legal notice](https://www.pazy.eu/legal-notice) identifies ownership but grants no general reuse license | Cite PAZy and the underlying publication | **Reference-only; no bundled PAZy table redistribution** without permission or explicit terms |
| PlasticDB | The database publication is open access, but no database-wide reuse grant was located | Cite PlasticDB and each source publication | **Reference-only; no bundled database export** until dataset-specific terms are verified |
| EnzymeMap v2 | [Zenodo record 8254726 is CC BY 4.0](https://zenodo.org/records/8254726) | Credit the EnzymeMap authors, underlying sources, version, and record DOI | Dataset redistribution is allowed under CC BY 4.0, but Phase A carries metadata and EC lookup keys only; no reaction file or atom map is bundled |
| MechFind / M-CSA arrow environments | [MechFind v1.0.0 record](https://zenodo.org/records/18674529) states a non-profit/non-commercial license; underlying M-CSA attribution also applies | Credit MechFind and M-CSA and preserve the exact release/commit | **Reference-only in Phase A**; no rule, prediction, or arrow-environment body is bundled |
| EC-BLAST | The interactive service is public, but no stable API release or result-redistribution grant was frozen | Credit EC-BLAST and its source publication if a later result is used | **Reference-only** until result terms, stable version, and provenance are captured |
| InterPro / Pfam | [InterPro, Pfam, PRINTS, and SFLD downloadable data are CC0 1.0](https://www.ebi.ac.uk/interpro/about/license/) | Credit the contributing databases and accessed release/publication | Permissible under CC0, but Phase A carries protein lookup links only and makes no domain assignment |
| EnzyMM | Software 0.3.1 is reported as MIT; M-CSA-derived template attribution and source terms still apply | Credit EnzyMM, M-CSA, and any structure/source record used later | No software, template, structure, or match result is bundled in Phase A |
| EzMechanism | Public documentation is available, but the service requires registration and generated-result terms were not separately captured | Credit M-CSA/EzMechanism and later inputs/results if access is authorized | **Reference-only**; no account, input, generated result, or outreach is claimed |
| ENZYME / EC nomenclature | Per-EC pages are public; a bulk release and redistribution terms were not authenticated in Phase A | Cite the EC number and accessed nomenclature source | Per-record links only; no bulk ENZYME body is bundled |

## Release rules

1. A published release manifest lists every included dataset or compiled data
   surface and its exact hash, source release/snapshot, rights row, and
   attribution. The frozen v0.1.0 truth-reset manifest predates Atlas-3; a new
   release cannot reuse it unchanged.
2. The locked `catalytic-earth reproduce` surface contains project-authored
   fixture records only. The Atlas-3 wheel surface additionally packages the
   attributed compiled kernel and source hashes, but not raw third-party
   structures, sequences, article bodies, kinetics tables, or
   restricted/reference-only exports. Its raw 1.2 MB source package remains a
   repository audit input under `data/atlas/atlas3/sources`. The Atlas-10 raw
   audit package contains 36 redistributed snapshots under
   `data/atlas/atlas10/sources` plus eight DOI reference-only handles. Its wheel
   surface packages the attributed compiled kernel, queries, expected result,
   and source hashes, not raw sequences, structures, source API payloads,
   linked Marvin schemes, or article bodies.
   The Atlas-50 Phase A package adds only identifiers, links, acquisition
   metadata, response hashes, rights boundaries, and deterministic project
   projections. It bundles no raw M-CSA page, EnzymeMap reaction file,
   MechFind rule/arrow environment, EnzyMM template, EC-BLAST/EzMechanism
   result, or article body.
3. CC BY-derived fields retain source identifiers and change notices. Database
   citations are additional to, not substitutes for, record-level literature
   citations.
4. If source terms change or cannot be verified, the source becomes
   reference/fetch-only until reviewed again.
