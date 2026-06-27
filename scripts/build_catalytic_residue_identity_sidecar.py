#!/usr/bin/env python3
"""Read-only builder for the catalytic-residue-identity sidecar.

Reads the active-site POSITIONS already stored in the bronze rows, fetches each accession's
sequence from UniProt in batches, and records the amino acid at each ACT_SITE position. Writes
ONLY the sidecar artifact -- the registry is never touched. The sidecar is a leakage-safe
structural-evidence map (accession -> catalytic residue identities), the same category as cofactor
identity; it lets the representation add catalytic-residue-identity features that separate the
cofactor-free no-Rhea-reaction families (e.g. cysteine_protease catalytic Cys vs ser_his catalytic
Ser) which the reaction representation cannot reach.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.adapters import USER_AGENT  # noqa: E402
from catalytic_earth.registry_io import load_json  # noqa: E402
from catalytic_earth.coverage_redundancy_audit import (  # noqa: E402
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
)

DEFAULT_OUT = "artifacts/v3_catalytic_residue_identity_sidecar_current702.json"
_UNIPROT_SEARCH = "https://rest.uniprot.org/uniprotkb/search"


def _mech(row: dict) -> dict:
    return row.get("evidence", {}).get("mechanism_evidence", {}) or {}


def _accession(row: dict) -> str | None:
    eid = row.get("entry_id") or ""
    if eid.startswith("uniprot:"):
        return eid.split(":", 1)[1]
    prov = row.get("evidence", {}).get("sequence_provenance", {}) or {}
    return prov.get("source_accession")


def _act_site_positions(row: dict) -> list[int]:
    return [
        int(a["position"])
        for a in (_mech(row).get("active_site_residues") or [])
        if a.get("feature_code") == "ACT_SITE" and a.get("position")
    ]


def _fetch_sequences(accessions: list[str], batch: int = 100) -> dict[str, str]:
    out: dict[str, str] = {}
    for i in range(0, len(accessions), batch):
        chunk = accessions[i : i + batch]
        query = " OR ".join(f"accession:{a}" for a in chunk)
        params = {"query": query, "fields": "accession,sequence", "format": "tsv", "size": str(batch)}
        url = f"{_UNIPROT_SEARCH}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310 - public UniProt REST
            text = resp.read().decode("utf-8", "replace")
        for line in text.splitlines()[1:]:
            cols = line.split("\t")
            if len(cols) >= 2 and cols[1]:
                out[cols[0]] = cols[1]
        print(f"  fetched {min(i + batch, len(accessions))}/{len(accessions)} accessions", file=sys.stderr)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", nargs="+", default=None, help="optional fingerprint_id filter (bounded run)")
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--batch", type=int, default=100)
    args = parser.parse_args()

    rows = load_json(DEFAULT_EXPANSION_REGISTRY_PATH) + load_json(DEFAULT_FROZEN_BENCHMARK_PATH)
    family_filter = set(args.families) if args.families else None

    want: dict[str, list[int]] = {}
    for row in rows:
        if family_filter and str(row.get("fingerprint_id")) not in family_filter:
            continue
        acc = _accession(row)
        pos = _act_site_positions(row)
        if acc and pos:
            want.setdefault(acc, sorted(set(pos)))

    print(f"accessions needing sequences: {len(want)}"
          + (f" (families={sorted(family_filter)})" if family_filter else ""), file=sys.stderr)
    seqs = _fetch_sequences(sorted(want), batch=args.batch)

    sidecar: dict[str, dict] = {}
    missing_seq = 0
    out_of_range = 0
    for acc, positions in want.items():
        seq = seqs.get(acc)
        if not seq:
            missing_seq += 1
            continue
        residues = []
        for p in positions:
            if 1 <= p <= len(seq):
                residues.append(seq[p - 1])
            else:
                out_of_range += 1
        if residues:
            sidecar[acc] = {"act_site_positions": positions, "act_site_residues": residues}

    payload = {
        "artifact_id": "v3_catalytic_residue_identity_sidecar_current702",
        "schema_version": "catalytic_earth.residue_identity_sidecar.v1",
        "leakage_safe": True,
        "leakage_basis": "curated UniProt active-site position + sequence residue = structural/"
                         "mechanistic evidence; NOT EC/name/prose/fingerprint. Registry untouched.",
        "method": "read-only batched UniProt FASTA fetch at the ACT_SITE positions already stored in "
                  "the bronze rows; writes only this sidecar artifact",
        "family_filter": sorted(family_filter) if family_filter else None,
        "counts": {
            "accessions_requested": len(want),
            "accessions_with_sequence": len(seqs),
            "accessions_in_sidecar": len(sidecar),
            "accessions_missing_sequence": missing_seq,
            "positions_out_of_range": out_of_range,
        },
        "residue_identity_by_accession": dict(sorted(sidecar.items())),
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(sidecar)} accessions "
          f"(missing seq {missing_seq}, out-of-range pos {out_of_range})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
