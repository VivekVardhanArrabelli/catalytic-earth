# Reaction geometry to function coordination — 2026-09-09

Run owner: `catalytic-earth-work-loop:941da8e2-e883-4a49-b5ac-122b604220a5`

## Question and decision rule

- **Question:** Which retained substrate, intermediate, product-fragment, or
  transition-state-analogue arrangement can be joined to a compatible chemical
  state and measured function strongly enough to constrain catalytic geometry
  beyond a catalytic-triad distance?
- **Expected information gain:** either one reusable, provenance-exact join that
  exposes a design-relevant arrangement together with its functional scope, or
  a supported reason that the apparent best candidate is not transferable.
- **Stop condition:** stop extending a candidate when the structure, ligand,
  construct, reaction state, assay endpoint, or residue mapping requires an
  unsupported cross-context transfer. If every retained candidate fails, record
  the smallest missing evidence rather than adding a speculative relation.

## Assignments

| Lane | Question | Constraints | Status |
| --- | --- | --- | --- |
| source | Which retained case has the strongest primary-source bridge from a reaction-relevant bound arrangement to measured function? | Challenge source scope; no repository edits or acquisition without parent coordination. | complete |
| representation | Can the existing IR express the exact structure/state/function join without case-specific code? | Put chemistry in data; preserve uncertainty and identity namespaces. | complete |
| adversarial | What would make the best-looking join scientifically misleading or no better than incumbent resources? | Reject construct, ligand, state, or endpoint transfer and overclaim. | complete |

## Shared findings

- 6HA3 is the strongest available bridge. The study identifies the deposited
  human E160Q/F6P-ThDP structure and reports E160Q F6P-ThDP accumulation plus
  reversible adduct-formation kinetics. Earlier 4KXV, 2QUT and M0187 packets
  each fail an exact structure/construct/measured-endpoint join.
- The F6P stopped-flow endpoint is not full-cycle turnover. The study's
  steady-state turnover assay uses X5P plus R5P to form S7P plus G3P and remains
  a separate same-variant observation.
- T6F is one integrated substrate-cofactor component with nonuniform atom
  occupancies. Its four deposited `struct_conn` rows are metal coordination;
  absence of a protein-covalent connection is not absence of the internal
  component bond.
- A complete active-site representation would be false without symmetry
  expansion: only polymer asym A is deposited, while the paper's E366-prime
  contact comes from the biological-assembly mate.
- E160Q is not a selective geometry perturbation; it also changes charge and
  nearby acid-base chemistry. The coordinate-derived 24.19-degree deviation
  and measured rates can be associated at study/variant scope, but causation is
  not established.
- The reusable response is a bounded study-context packet with separate
  arrangement, observation and evidence-qualified relation fields. Existing
  observed-state and M0187-specific mechanism-evidence contracts cannot express
  this case unchanged without collapsing typed connections or endpoint scope.

## Integrated result

- Added `data/atlas/study_context/6ha3/` with the retained CC0 6HA3 mmCIF,
  project-authored evidence projection, six-capture receipt ledger, source
  inventory, manual review pins and attribution.
- Added a generic deterministic validator and core regression tests. The
  validator recomputes selected atom facts, component bonds, deposited
  distances, torsional deviation and typed connections, and rejects source,
  variant, occupancy, connection-type, review-pin and M0219-step promotions.
- Direct retained-body acquisition used six requests and 2,987,157 bytes under
  the 100-request/30-MiB batch ceiling. Web discovery traffic is disclosed
  separately because its underlying request and byte counts are unavailable.
