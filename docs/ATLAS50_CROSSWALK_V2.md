# Atlas-50 computational crosswalk v2

**Status:** computationally provisional development artifact, dated 2026-09-05. It is not a human or expert review, an independent annotation, a Phase-B submission, a registry admission, a tier lift, or experimental evidence. The contributing computational agents used the same model family, can make correlated errors, and are not statistically independent reviewers.

## Result

Crosswalk v2 gives every one of the 57 Phase-A fingerprints an explicit successor row and an old-to-new change record. It makes 23 provisional classifications and leaves 34 classifications `unresolved`. The provisional set contains 18 aggregations, three specializations, one exact duplicate at a declared reaction-core granularity, and one unsupported/ill-defined row.

The v2 generator reads the frozen Phase-A draft and the computational source audit. It verifies their exact SHA-256 digests before repository publication. It does not read the historical 702-row automation registry. Historical assignments therefore cannot silently become positive mechanism evidence.

The generated artifacts are:

- `crosswalk.json`: all 57 successor rows, named relation targets, source identity, mechanistic applicability, corrected scopes, rejections, and claim boundaries.
- `change_map.json`: an explicit 57-row old-to-new map with prior/new classification, prior named records, new relation targets, correction reason, and wrong-anchor removal state.
- `manifest.json`: pinned input and output hashes plus the human-review, experimental, registry, and review-independence boundaries.

## Relation contract

Each relation target names both endpoints and records the direction from the fingerprint to the target. Source identity and mechanistic applicability are different objects:

```json
{
  "source_key": "mcsa",
  "target_id": "M0150",
  "relation": "exact_duplicate",
  "relation_direction": "fingerprint_to_target",
  "source_identity": {
    "status": "official_entry_checked",
    "name": "nucleoside-diphosphate kinase"
  },
  "mechanistic_applicability": {
    "status": "scope_unresolved",
    "scope": "NDPK overall reaction and phosphohistidine mechanism",
    "rationale": "The exact-reaction locator exists, but species-general equivalence has not been established."
  }
}
```

An official identifier proves that the source object exists and has the stated identity. It does not prove that its mechanism transfers across the fingerprint's full scope. A targetless aggregation, specialization, bridge, or exact-duplicate label cannot pass validation. Exact duplication additionally requires a source-checked target and an allowlisted, explicit granularity. This is why the NDPK row remains unresolved despite its strong exact-reaction locator.

## Corrected source decisions

| Fingerprint | Phase-A label | v2 label | Named evidence and correction |
|---|---|---|---|
| PLP-dependent enzyme | aggregation | aggregation, provisional | [M0049](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/49/) is pyruvoyl-dependent histidine decarboxylase and is rejected only as PLP evidence. Its Phase-A-derived EC, ChEBI, protein, structure, fold, and lookup bundle is recorded and dropped. Direct PLP branches are [M0066 transaminase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/66/), [M0213 alanine racemase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/213/), [M0186 serine ammonia-lyase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/186/), and [M0482 dialkylglycine decarboxylase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/482/). M0049 remains a valid pyruvoyl mechanism object outside this PLP mapping. |
| Heme peroxidase/oxidase | aggregation | aggregation, provisional | [M0239](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/239/) supplies direct heme-peroxidase coverage. [M0133 P450cam](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/133/) is scoped to the P450 row; [M0390 laccase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/390/) is scoped to copper oxidoreductase. |
| Cytochrome P450 | specialization | specialization, provisional | M0133 is the positive P450 target. M0239 and M0390 are explicit scope exclusions rather than interchangeable heme/redox evidence. |
| Copper oxidoreductase | aggregation | aggregation, provisional | [M0135 peptidylglycine monooxygenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/135/) and M0390 laccase are separate positive copper branches; heme M0239 is excluded. |
| Class-II metal aldolase | specialization | specialization, provisional | [M0052](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/52/) is the positive metal-dependent Class-II target. Same-EC [M0222](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/222/) is mandatory Class-I Schiff-base counterevidence. |
| Nucleoside-diphosphate kinase | specialization | unresolved | [M0150](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/150/) directly supplies the NDPK reaction and phosphohistidine ping-pong mechanism. The species/generalization boundary is still unresolved, so v2 rejects an invented exact-equivalence promotion. |
| Mn/Fe superoxide dismutase | specialization | unresolved | [M0138](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/138/) is kept only as Cu/Zn counterevidence. It is not positive Mn/Fe coverage. |
| Serine beta-lactamase | specialization | aggregation, provisional | [M0002 Class A](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/2/), [M0257 Class C](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/257/), and [M0210 Class D](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/210/) are separate branches with class-scoped catalytic networks. |
| Metallo-beta-lactamase | specialization | aggregation, provisional | [M0015](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/15/) and [M0016](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/16/) cover dimetallic and monometallic Class-B1 mechanisms. B2 and B3 remain unrepresented; v2 does not transfer B1 evidence to those classes. |
| Flavin disulfide reductase | specialization | aggregation, provisional | [M0006 glutathione reductase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/6/) and [M0381 thioredoxin reductase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/381/) are distinct branches with different relay/domain arrangements. |
| DHFR | exact duplicate | exact duplicate at reaction core, provisional | [M0112](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/112/) supports the EC 1.5.1.3 NADPH-dependent DHF-to-THF reaction core. Protein, organism, resistance, fusion, and structure applicability are narrower and are not asserted equivalent. The corrected proton role is explicit: conserved water supplies the N5 proton; Asp26 tunes the hydrogen-bond network and pKa rather than directly donating that proton. |

Other official identities already checked in the computational audit are normalized into relation targets only. A row remains unresolved when those identities do not establish the declared relation. Historical curated-702 locators with no direct official check are not emitted as v2 source targets.

## Reproduction and checks

From the repository root:

```bash
python scripts/build_atlas50_crosswalk_v2.py --check
PYTHONPATH=src python -m unittest tests.core.test_atlas50_crosswalk_v2 -v
```

To regenerate after an intentional, reviewed input-version update:

```bash
python scripts/build_atlas50_crosswalk_v2.py
```

The checked input digests are:

- `data/atlas/atlas50/phase_a/crosswalk_draft.json`: `838d74b142fc82c81183daa8d469db9e2baab52ffade4c8c6cf0b07826da1dac`
- `data/atlas/atlas50/computational_review/crosswalk_review.json`: `84150aff2cb563c1f624aa3ce000c91c3588c520604715e81197f87e77d8ad4e`

The focused regression tests alter an inherited M0049 bundle and verify that the invented handle is captured only in the rejected bundle, never in positive PLP targets. They also try to promote M0150 to an exact duplicate by changing labels and applicability status; the validator rejects that invented equivalence because the scope is not an accepted exact-equivalence boundary.

## Remaining boundary

This draft makes the computational substitute concrete for development use. It does not satisfy the repository's independent-human review requirement or provide experimental evidence. Thirty-four rows remain unresolved, mostly because the current source acquisition lacks a named, mechanistically applicable incumbent target. Even the 23 provisional relations can change after genuinely independent review or deeper source work.
