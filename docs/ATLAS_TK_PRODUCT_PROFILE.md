# Transketolase competing-product profile

Yu et al. report a useful counterexample to treating nondetection of a side
product as improved target activity. With the same supplied glycolaldehyde and
pyruvate mixture, purified E. coli transketolase H473N accumulates less target
3,4-dihydroxy-2-butanone (DHB) than wild type, while erythrulose is undetected.

| Source-named construct | DHB after 24 hours | Erythrulose after 24 hours |
| --- | --- | --- |
| WT | 10.5 mM | 10.5 mM |
| H473N | 5.5 mM | Not detected; threshold unspecified |

These central values are printed in the accepted manuscript's Results
(PDF pages 10–11) and are consistent with Figure 3C (page 44). Figure 3's legend
(page 37) identifies triplicate means with SD error bars. Numeric SDs were not
transcribed or digitized. The assay uses 50 mM each glycolaldehyde and sodium
pyruvate, 50 mM Tris-HCl at pH 7.0, 0.13 mg/mL purified enzyme, and 30 °C for
24 hours. HPLC concentrations use standard curves (Methods, page 23).
The lysate cofactor preparation described elsewhere does not establish final
ThDP or MgCl2 concentrations for this selected purified assay.

The [institutional record](https://discovery.ucl.ac.uk/id/eprint/10084395/)
binds DOI 10.1111/febs.15108 to the
[accepted manuscript](https://discovery.ucl.ac.uk/id/eprint/10084395/1/Yu%20FEBSJ%202019%20Accepted%20online%20version.pdf).
The publisher version was inaccessible and was not compared. The exact PDF is
retained locally by SHA-256; only project-authored annotations are distributed
in the [source packet](../data/atlas/study_context/tk_2020/source_qualification.json).

## What the two products resolve

Figure 2, Scheme 1 (PDF page 43), depicts different net routes: glycolaldehyde
plus pyruvate gives DHB with carbon dioxide loss; two glycolaldehyde molecules
give erythrulose. Glycolaldehyde therefore supplies the acceptor in the target
route and both donor and acceptor molecules in the competing route. The same
supplied mixture supports both. The association between donor origin and
product identity is source chemical interpretation, not an isotope-traced atom
map. Carbon dioxide is depicted, not measured in the selected assay.

```sh
python scripts/query_atlas_perturbations.py --comparison tk_2020:H473N:DHB_accumulation
```

The shared query returns the three numeric concentrations and one censored
nondetection, their source reactions, assay and construct context, and a
descriptive H473N/WT DHB quotient of 0.52381. The two product-specific assay
wrappers share one experiment identifier; they are not independent experiments.
Erythrulose is context for this ratio. Its nondetection never becomes zero,
an infinite DHB/erythrulose ratio, or a microscopic specificity constant.
No uncertainty propagation, significance or equivalence is inferred.
Equal accumulated concentrations do not determine microscopic fluxes or remaining
substrate concentrations. The erythrulose route consumes two glycolaldehyde
molecules per product; DHB uses one glycolaldehyde and one pyruvate.

## What remains unresolved

The inherited donor-half question closes at a missing distinguishing endpoint.
The main manuscript's H100 assignment uses cross-acceptor final-yield correlation
for H100L, H100F, H100Y and WT, four points total (page 15). Its mechanism analysis
then docks a preconstructed ThDP-enamine into modeled variants (pages 19–21 and
28). These observations and calculations do not measure formation, occupancy,
decarboxylation or cleavage of a donor–cofactor state. Overall pyruvate KM and
product identity cannot provide those missing measurements. The supplementary
file was not acquired; this is a conclusion about the inspected main manuscript,
not a literature-wide absence claim.

The H473N profile is an overall product endpoint, integrating both reaction
halves, competition and possible reversibility or product release. It does not
identify an isolated residue mechanism. Source-named single-mutant identity is
supported by the selected Results and Figure 3C; exact assayed sequence, physical
specimen and mutant geometry remain unknown. Separate library naming errors do
not redefine the selected H473N record. The lysate panel's yield normalized by
protein densitometry is also kept separate from these purified concentrations.

Existing construct, reaction, endpoint, ratio and nondetection consumers suffice;
only a generic product-concentration parameter declaration is added in data.
This prevents a consequential product-profile inference, but does not establish
curation-time savings, a complete mechanistic chain or design performance.
The [source challenge](../data/atlas/study_context/tk_2020/source_review.json)
is correlated computational review. CE-045 in [the claim ledger](../CLAIMS.md)
and the [truth policy](ATLAS_TRUTH_POLICY.md) retain the evidence boundary;
[errata](../ERRATA.md) continue to control earlier claims.
