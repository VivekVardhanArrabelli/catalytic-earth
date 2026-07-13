# Locked core reproduction

The canonical core is deliberately small: standard-library Python, no network,
no accelerator, no external binary, no current-working-directory assumption,
and no third-party data bundle.

From a wheel:

```bash
python -m venv .venv
. .venv/bin/activate              # Windows: .venv\Scripts\activate
python -m pip install --no-deps catalytic_earth-0.1.0-py3-none-any.whl
catalytic-earth reproduce
```

Expected result SHA-256:

```text
a2374c6530dfd3b4681db5c3db691fdcdedbf645604c6e7dfe0b95ab7e89ea98
```

The command loads four project-authored fixture records through the versioned
typed mechanism schema, counts exact object/evidence types, retains one
synthetic negative observation, and checks the canonical result hash. It is a
packaging, schema, determinism, and negative-record-retention result.

It is not a biological benchmark, mechanism prediction, external validation,
or evidence that any real enzyme record is correct. Those stronger claims need
licensed source snapshots, exact tool/model environments, independent review,
and prospective evidence.

The old research command surface remains available as
`catalytic-earth-legacy`, is outside the locked core guarantee, and is frozen
pending decomposition.
