# CTAC changes an apparent amine coefficient, with a defined denominator

Schmidt et al. (2013), *Organic & Biomolecular Chemistry* 11:8419–8425,
[DOI 10.1039/c3ob41898g](https://doi.org/10.1039/c3ob41898g), provides a
same-study butylamine comparison on methodol. Table 2 reports apparent
second-order coefficients of 2.1 × 10⁻⁶ without detergent and 2.5 × 10⁻⁴
M⁻¹ s⁻¹ with 1 mM CTAC. Dividing the printed central values gives **119.05**;
the source rounds its relative coefficient to **120**.

This is an effect of adding CTAC on a coefficient normalized to nominal bulk
amine and substrate concentrations. It does not isolate hydrophobicity:
CTAC can change charge, partitioning, local concentrations and micellar
organization. The effective micellar amine concentration was not used in the
fit normalization. No intrinsic micellar-site rate or hydrophobic energy follows.

The [source packet](../data/atlas/study_context/schmidt_2013/micellar_controls.json)
is bound to the retained PMC author manuscript, not a publisher-final PDF.
The [review](../data/atlas/study_context/schmidt_2013/source_review.json) records
source challenge and the accepted scope. The common consumer resolves the
original arm records, chemical systems, protocol, normalization and exclusions:

```sh
python scripts/query_atlas_perturbations.py --study schmidt_2013
python scripts/query_atlas_perturbations.py --control-relation schmidt_2013:BuAm:CTAC-over-no-detergent
```

## The missing controls prevent a component decomposition

The paper explicitly says it could not measure octylamine or dodecylamine
without micelles because of their low water solubility. Its reported 710-fold
and 9,500-fold relative factors use **no-detergent butylamine** as the denominator.
They are not the respective amines' detergent effects. The within-CTAC
DoAm/BuAm ratio of about 80 also changes amine identity, the concentration
range used in fitting, partitioning and ionization context.

Thus the observed cells do not identify an environment-by-amine interaction.
Missing measurements are not zero. An amine-free product-appearance rate or
intercept would also have a different meaning from a coefficient normalized
by amine concentration; it cannot fill a missing k₂ corner by assumption.
The packet retains these missing premises rather than computing a double ratio.

Table 1 separately reports fixed-concentration product rates with a CTAC/no-
detergent factor of 33. That endpoint remains distinct from Table 2's fitted
coefficient factor of 120; they are not merged into a universal detergent factor.
Table 3's partial ionization comparison is outside this selected numerical
relation. No solution-pKa factor is transferred into the micellar result.

## Protocol and source boundaries

The selected Table 2 context uses 22 °C, pH 7.5, 50 mM sodium phosphate,
5% DMSO, stirring at 600 rpm, methodol titrations of 30–350 µM and butylamine
concentrations of 0.2–4 mM. Product fluorescence uses excitation at 330 nm and
emission at 452 nm, calibrated with a product standard curve for each detergent
condition. No-detergent means buffered 5% DMSO, not pure water. NaCl is unstated;
it is not recorded as zero. Per-row errors, replicate counts and raw fits are
unavailable in the acquired main, and the supplementary-file response was HTML.
No enantiopure substrate, separate R/S kinetics or exact reacted state is inferred.

The RA61 value in Table 2 is imported from Lassila2010. Schmidt's “same
conditions” wording does not establish exact assay identity: the retained RA61
protocol uses 25 °C and 300 mM NaCl. No matched enzyme/micelle ranking or
independent RA61 replicate is created. HMP changes substrate and readout;
BSA changes catalyst normalization and retains the source's contaminant
alternative. Neither supplies an extra cell for this comparison.

## Reuse across chemical systems and protein preparations

The previous arithmetic path requires a protein mutation and its genetic
reference. The new parallel `system_ratio` relation compares two original
source rows without inventing protein constructs for chemical mixtures.
It checks row/system/assay identities, parameter and units, a common source
protocol, declared normalization and substrate evidence, and source-derived
condition fields. Unknown or mismatched inputs refuse arithmetic. There is no
factorial or interaction operation on this path.

One second context reuses the already curated calmodulin measurements:

```sh
python scripts/query_atlas_perturbations.py --control-relation calmodulin_2015:Ac-CaMWN:over-CaMWN-preparation
```

It resolves the original CaMWN and Ac-CaMWN Table I rows and returns
0.004/0.005 = **0.8** as a chemical-preparation contrast. The old observations
and genetic comparisons remain exact. Source-reported acetylation, unknown
occupancy, the unspecified error statistic and the Table I/Figure 5 protocol
conflict remain attached. The ratio adds no measurement, statistical equivalence,
significance or isolated terminal-amine contribution.

Condition fields are source-reviewed declarations. Their equality does not
prove that every physical property of two preparations is equal. These two
contexts demonstrate an operation working with different experimental systems;
manual source interpretation and normalization review are still required.
No curation-time saving, incumbent superiority, independent human validation,
project experiment or design-performance result is established.

The [acquisition appendix](../data/atlas/study_context/ra61_2010/micellar_acquisition_appendix.json)
continues the same RA61 batch: six requests / 201,684 response-body bytes added,
now **58 requests / 4,697,605 bytes**. The bounded inquiry is complete; no
failed access route needs repeating.
