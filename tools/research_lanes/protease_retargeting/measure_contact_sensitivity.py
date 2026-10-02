"""Recompute the exposed R19/S5 sample-sensitivity diagnostic from author PDBs.

Prints measurements without changing the saved relation. This is a coordinate
comparison, not a hydrogen-bond, energy, kinetic or population calculation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from measure_author_models import angle, distance, read_pdb


def measure(atoms):
    for residue, name in ((('A', 19), 'ARG'), (('A', 26), 'GLU'), (('B', 5), 'SER')):
        if atoms[(*residue, 'CA')]['residue_name'] != name:
            raise ValueError(f"Unexpected residue identity at {residue}")
    metrics = {
        f'R19_{donor}_to_S5_{oxygen}_A': distance(atoms, ('A', 19, donor), ('B', 5, oxygen))
        for donor in ('NE', 'NH1', 'NH2') for oxygen in ('OG', 'O')
    }
    for oxygen in ('OG', 'O'):
        for label, donors in (('terminal', ('NH1', 'NH2')), ('donor', ('NE', 'NH1', 'NH2'))):
            metrics[f'R19_min_{label}_N_to_S5_{oxygen}_A'] = min(
                metrics[f'R19_{donor}_to_S5_{oxygen}_A'] for donor in donors
            )
    for enzyme_oxygen in ('OE1', 'OE2'):
        for substrate_atom in ('OG', 'N'):
            metrics[f'E26_{enzyme_oxygen}_to_S5_{substrate_atom}_A'] = distance(
                atoms, ('A', 26, enzyme_oxygen), ('B', 5, substrate_atom)
            )
    for substrate_atom in ('OG', 'N'):
        metrics[f'E26_min_OE_to_S5_{substrate_atom}_A'] = min(
            metrics[f'E26_{oxygen}_to_S5_{substrate_atom}_A'] for oxygen in ('OE1', 'OE2')
        )
    for nitrogen in ('NH1', 'NH2'):
        metrics[f'R19_CZ_{nitrogen}_S5_OG_degrees'] = angle(
            atoms, ('A', 19, 'CZ'), ('A', 19, nitrogen), ('B', 5, 'OG')
        )
    p = [np.array(atoms[('B', 5, name)]['coordinates_angstrom']) for name in ('N', 'CA', 'CB', 'OG')]
    b0, b1, b2 = p[0] - p[1], p[2] - p[1], p[3] - p[2]
    b1 /= np.linalg.norm(b1)
    v, w = b0 - np.dot(b0, b1) * b1, b2 - np.dot(b2, b1) * b1
    metrics['S5_N_CA_CB_OG_dihedral_degrees'] = float(
        np.degrees(np.arctan2(np.dot(np.cross(b1, v), w), np.dot(v, w)))
    )
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', nargs='?', type=Path,
                        default=Path(__file__).with_name('r19_s5_state_sensitivity.json'))
    args = parser.parse_args()
    record = json.loads(args.record.read_text())
    results = []
    for model in record['models']:
        atoms = read_pdb(args.record.parent / model['file'], model['sha256'])
        metrics = measure(atoms)
        if set(metrics) != set(model['metrics']):
            raise ValueError('Saved metric names differ from the specified comparison')
        for key, value in metrics.items():
            if not math.isclose(value, model['metrics'][key], rel_tol=1e-12, abs_tol=1e-10):
                raise ValueError(f"Coordinate result differs: {model['file']}: {key}")
        results.append({key: model[key] for key in ('state', 'sample', 'pass_status', 'file')} | {'metrics': metrics})
    print(json.dumps({'models': results, 'decision': record['decision']}, indent=2))


if __name__ == '__main__':
    main()
