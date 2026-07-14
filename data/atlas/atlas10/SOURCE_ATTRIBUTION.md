# Atlas-10 source attribution and redistribution boundary

The Atlas-10 extension was compiled from the content-bound handles in
`source_manifest.json`, retrieved at `2026-07-14T17:42:17Z`. The manifest is
the authoritative per-record inventory of source URL, retrieval status,
snapshot path, media type, license note, attribution text, transformation
notice, byte count, and SHA-256 digest.

- UniProtKB records and Rhea query/record snapshots are redistributed under
  CC BY 4.0. Credit the respective database and cite its release/publication.
- M-CSA API records and linked Marvin schemes are redistributed under CC BY
  4.0. Credit M-CSA and cite Ribeiro et al. together with the accessed entry.
- CATH-Gene3D release rows are redistributed under CC BY 4.0. Credit CATH and
  cite the applicable release/publication.
- Frozen RCSB PDB/wwPDB coordinate archives are the exact CC0 gzip-compressed
  mmCIF bytes. Cite each PDB identifier, its structure authors/publication,
  RCSB PDB, and wwPDB.
- DOI records are reference-only verified handles. No article text is bundled;
  article-specific publisher terms still apply.

The compiled kernel copies only the bounded fields needed for reaction status,
source proposals, sites, structure applicability, evidence, uncertainty, and
relationship queries. It does not relicense upstream material, erase source
attribution, turn a reference-only article into a bundled source, or convert a
zero-row query into a canonical reaction record.
