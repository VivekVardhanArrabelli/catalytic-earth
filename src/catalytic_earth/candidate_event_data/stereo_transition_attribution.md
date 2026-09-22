# Raw-stereo transition source-candidate attribution

The retained source records and Marvin panels underlying these compiled,
unreviewed candidates come from the **Mechanism and Catalytic Site Atlas
(M-CSA)**:

- [M0066, D-amino-acid transaminase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/66/)
- [M0213, alanine racemase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/213/)

M-CSA data are available under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the M-CSA
authors for the curated mechanisms and source depictions, and cite Ribeiro AJM
et al., “Mechanism and Catalytic Site Atlas (M-CSA): a database of enzyme
reaction mechanisms and active sites,” *Nucleic Acids Research* 46(D1),
D618-D623 (2018),
[doi:10.1093/nar/gkx1012](https://doi.org/10.1093/nar/gkx1012).

The installed wheel contains hash-bound compiled covalent projections, the
captured raw `W` or `H` context delta, source bindings, source scope, and
mandatory abstentions. It does not contain the retained raw M-CSA snapshots or
MRV panel strings. Consequently, installed-wheel validation checks the
compiled payload and its declared provenance bindings; it does not recompute
the original snapshot or original panel hashes from unavailable source bytes.
Repository tests separately reconstruct each compiled row from the retained,
hash-matched source snapshot.

These rows are computationally checked, unreviewed source candidates. Their
same-model audits are not independent scientific review. A disappearing `W`
or `H` token is retained only as a source-drawing transition and is not
interpreted as R/S assignment, achirality, or a physical stereochemical event.
The covalent projections do not establish physical atom identity, canonical
participant identity, concertedness, a complete mechanism, an experimentally
observed intermediate, or experimental validation.

For M0066, preserve the source conflict between the D-glutamate entry/MRV and
the Step 1 L-glutamate prose; do not infer an exact normalized substrate
stereochemistry. Drawing normalization is a sufficient explanation for the
`H` marker disappearing when its bond becomes double. For M0213, preserve the
ordered L-alanine-to-D-alanine source transcription, the reverse-direction
role boundary, and the terminal drawing-label conflict described in the
packaged source draft.
