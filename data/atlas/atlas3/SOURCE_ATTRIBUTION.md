# Atlas-3 source attribution and change notice

This directory contains the bounded source package for the first biological
kernel. Retrieval was frozen at `2026-07-14T02:46:42Z`. The authoritative
per-record URI, retrieval URL, evidence role, applicability, license,
attribution, transformation notice, byte count, and content hash are in
`source_manifest.json`.

- UniProtKB JSON for P11653, P11652, P00448, and P62593 is used under CC BY
  4.0. Credit UniProt. REST JSON was normalized to sorted UTF-8 JSON; no
  scientific fields were intentionally changed.
- Rhea records RHEA:22888, RHEA:20696, and RHEA:20401 are used under CC BY
  4.0. Credit Rhea. One official TSV row per reaction was transformed to
  sorted UTF-8 JSON with its request URL retained.
- M-CSA records M0062, M0138, and M0002 are used under CC BY 4.0. Credit M-CSA
  and Ribeiro et al. API JSON was normalized to sorted UTF-8 JSON; no
  scientific fields were intentionally changed.
- PDB archive files 1REQ, 1D5N, and 1BTL are exact gzip-compressed mmCIF bytes
  supplied under the PDB archive's CC0 terms. Cite each structure's authors,
  primary publication, RCSB PDB, and wwPDB.
- Four DOI handles and PMCID PMC14582 are reference-only. No publisher or
  article body text is bundled; article-specific access and reuse terms still
  apply.

The project's checked rights policy is
[`docs/SOURCE_DATA_RIGHTS.md`](../../../docs/SOURCE_DATA_RIGHTS.md). These
snapshots are provenance inputs, not independent validation of the compiled
Atlas interpretations.
