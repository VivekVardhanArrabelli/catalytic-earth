# PLP step correspondence stops at stereochemistry and state

The retained M0066 transaminase, M0186 serine ammonia-lyase and M0213 alanine
racemase proposal-1 step-2 drawings share a local directed-arrow pattern.
They do **not establish a qualified shared actor-state relation** with the
current source-step consumer. Each required substrate nitrogen touches an
uninterpreted source stereobond; their larger cofactor/adduct graphs also have
different charge, explicit-H and substrate contexts.

This is a supported limit on the proposed comparison, not evidence that the
enzymes lack a common transaldimination step. It prevents an endpoint-only
match from becoming an unsupported chemical-state or function transfer.

## The local pattern and the boundary

The two arrows have the same declared local roles: the electron pair in the
lysine-N–adduct-C bond is directed to the lysine N, while the substrate-N lone
pair is directed to the existing substrate-N–adduct-C single bond. These are
arrow endpoints, not inferred bond edits. The three endpoints have matching
element, parsed formal-charge and raw lone-pair tokens: neutral substrate N
with `lonePair=1`, central carbon and positively charged lysine N. Source
labels and explicit-H adjacency remain distinct. No transferred explicit
hydrogen is an endpoint of these arrows.

| Proposal-1 step 2 | Substrate N / adduct C / lysine N | Directed flows | Stereo touching required substrate N |
| --- | --- | --- | --- |
| M0066 | a19 / a57 / a40 | o38 bond-to-N; o39 N-to-bond | b18: ordered a18–a19, raw H |
| M0186 | a21 / a13 / a23 | o27 bond-to-N; o28 N-to-bond | b31: ordered a17–a21, raw W |
| M0213 | a20 / a13 / a22 | o37 bond-to-N; o38 N-to-bond | b20: ordered a17–a20, raw W |

Here `H` and `W` are the raw hashed/wedged bond tokens, not hydrogen atoms or
canonical absolute configurations. Neither different tokens nor matching
tokens alone establish an R/S relationship. Omitting the adjacent alpha carbon
does not remove the stereobond touching the required nitrogen.

The connected actors contain 31/31, 30/30 and 28/28 atoms/bonds respectively.
Their three-node local projections each have two existing single bonds.
The larger actors retain material differences:

- Pyridine N a4 has explicit charge +1 in M0066; M0186/M0213 omit that charge
  and carry raw `lonePair=1`.
- Cofactor oxygen a10 has explicit charge −1 and `lonePair=3` in M0213;
  M0066/M0186 omit that charge and carry `lonePair=2`.
- M0186 phosphate O a15 is bonded to explicit H a39. Its lysine N a23 also
  has H a40. M0213 instead draws lysine N a22–H a68 and an anionic phosphate
  O a15; M0066 draws no explicit H anywhere in this panel.
- The substrate portions are glutamate-, serine- and alanine-labeled source
  contexts. Their different sidechains are not interchangeable state data.

Omitted `formalCharge` parses as zero in the existing graph reader; omitted H
does not establish physical absence or complete protonation. The source prose
calls the result “free PLP,” but the proposed event displaces lysine from a
substrate–cofactor adduct. That phrase cannot supply an unbound-cofactor state.
No after-state replay or corrected source trajectory is claimed here.

## Within M0186, the next state stops at explicit hydrogen continuity

The [step-2 to step-3 audit](../data/atlas/source_step_correspondence/m0186_continuity.json)
asks a different question from the cross-entry comparison above: do M0186's
two arrows account for its next depicted state? They account for the selected
heavy-atom bond and electronic changes under the reviewed source-locator map:

| Step-2 arrow | Change supported by step-3 start |
| --- | --- |
| o27, Lys N–PLP C bond to Lys N | Remove a23–a13; a23 changes from +1 to neutral with a drawn lone pair. |
| o28, substrate N lone pair to substrate N–PLP C bond | Change a21–a13 from single to double; a21 becomes +1 and loses the drawn lone-pair token. |

Step 3 retains the covalently bound substrate–PLP adduct. Thus the step-2
phrase “free PLP” cannot supply an unbound-cofactor state. This is compatible
heavy-atom topology, not an accepted complete chemical-state replay.

The complete selected actor has 30 drawn atoms in each panel: 28 heavy atoms
and two explicit H atoms. After the two reviewed arrows, the H neighbors are
oxygen and nitrogen; at step-3 start they are oxygen and carbon. This multiset
is invariant under any element-preserving graph bijection. Neither of the two
possible H permutations can repair it. The same-locator residual is Lys
N a23–H a40 versus substrate alpha-C a17–H a40; neither step-2 arrow touches H.
The result therefore goes beyond finding a different bond at the same raw ID.

The source may draw different hydrogens when they become relevant to a step.
Step 3's own o27/o30 arrows use its alpha-C-bound H. That possible explanation
does not identify the H across panels or establish a physical proton transfer
during step 2. Missing implicit H is not completed to force a match. The
ordered a17–a21 stereobond remains raw `W` in both drawings; neither its token
nor the heavy-atom match establishes stereochemical continuity or R/S.

The bounded inquiry closes at this first unaccounted explicit-H change. The
source chemistry is not disproved. No new runtime relation or claim is added,
and the original cross-entry diagnostic and strict consumer guards are
unchanged. The [supplemental review](../data/atlas/source_step_correspondence/m0186_continuity_review.json)
records the source objection and its computational adjudication. Source and
compiled-record hashes bind the audit; no new source request was made.

## Reproduce and reuse the finding

The [bound diagnostic](../data/atlas/source_step_correspondence/plp_step2_boundary.json)
stores exact source/compiled-record hashes, step locators, local atom and flow
roles, existing local bonds, raw electronic/label tokens, all drawn H atoms
and ordered stereo witnesses. Distal lysine alias labels remain source metadata;
no numbered protein-site correspondence is inferred.
The [source review](../data/atlas/source_step_correspondence/plp_step2_review.json)
records the challenged interpretation. Original sources and compiled records
are unchanged, and no new scientific request or response byte was acquired.

Run the focused checks from the repository:

```sh
python -m unittest discover -s tests/core -p test_source_step_correspondence.py
```

They check the two local arrow roles against the retained raw and compiled
sources, then require the unchanged consumer to reject all three full actor
selections and all three adversarial endpoint-only selections. The exact
rejection is `compared graph touches uninterpreted source stereochemistry`.
This diagnostic is not a successful `compare_source_steps.py --spec` relation.
No enzyme-specific code or relaxed stereo/charge/H matching was added.

M0066's D-glutamate identifiers versus Step-1 L-glutamate prose, M0213's
direction/terminal-label conflict and analogue context, and M0186's later
inferred/assumed roles and extra-enzymatic steps remain unresolved at their
original scopes. No canonical stereochemistry, physical atom identity,
homologous residue mapping, whole mechanism, experiment or evidence tier is
established. The reviews are computational and may share errors.

M-CSA content is CC BY 4.0; credit Ribeiro et al., *Nucleic Acids Research*
46(D1), D618–D623 (2018), doi:10.1093/nar/gkx1012. The retained
[M0066](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/66/),
[M0186](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/186/) and
[M0213](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/213/) snapshots are the
source witnesses. The added contribution is the explicit rejected comparison
and the boundary preventing overinterpretation of its local arrow match.
