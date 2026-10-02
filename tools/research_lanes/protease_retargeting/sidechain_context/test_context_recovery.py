#!/usr/bin/env python3
"""Scientific invariance and missingness checks on the retained reference only."""
import argparse
import copy
import json
from pathlib import Path
import sys
import unittest
import numpy as np
sys.dont_write_bytecode = True
import measure_context_recovery as m

ap = argparse.ArgumentParser()
ap.add_argument("--helper-dir", required=True, type=Path)
ap.add_argument("--reference-scaffold", required=True, type=Path)
ap.add_argument("--decision", required=True, type=Path)
args = ap.parse_args()
h = m.helpers(args.helper_dir)
ca, groups = m.reference(args.reference_scaffold, h)
plan = json.loads(args.decision.read_text())

class GeometryInvariants(unittest.TestCase):
    def test_arbitrary_rigid_motion_and_reflection(self):
        # A frame change must not alter the result; a mirror is not a rigid fit.
        u, _, v = np.linalg.svd(np.array([[2.,3.,-1.], [1.,-2.,4.], [3.,1.,2.]]))
        r = u @ np.diag([1.,1.,np.linalg.det(u @ v)]) @ v
        t = np.array([17.4,-6.2,21.7])
        result = m.score_arrays(ca @ r+t, {k:a @ r+t for k,a in groups.items()}, ca, groups, h)
        self.assertLess(result["worst_group_rmsd_A"], 1e-10)
        mirror = np.diag([-1.,1.,1.])
        mirrored = m.score_arrays(ca @ mirror, {k:a @ mirror for k,a in groups.items()}, ca, groups, h)
        self.assertGreater(mirrored["enzyme_CA_rmsd_to_scaffold_A"], 1e-6)

    def test_equivalent_oxygen_swap_is_bijective(self):
        changed = copy.deepcopy(groups)
        for g in m.SWAPPABLE:
            changed[g] = changed[g][[0,2,1]]
        result = m.score_arrays(ca, changed, ca, groups, h)
        self.assertLess(result["worst_group_rmsd_A"], 1e-10)
        for g in m.SWAPPABLE:
            self.assertEqual(result["reference_atom_permutations"][g], [0,2,1])
        # Two atoms cannot both match the same reference oxygen.
        changed["general_base_37"][2] = changed["general_base_37"][1]
        result = m.score_arrays(ca, changed, ca, groups, h)
        self.assertGreater(result["group_rmsd_A"]["general_base_37"], 1e-6)

    def test_missing_outputs_retain_all_assignments(self):
        result = m.evaluate({"candidates": []}, plan, args.reference_scaffold, args.helper_dir)
        self.assertEqual(result["decision"], "incomplete_comparison")
        self.assertEqual(result["observed_ES"], 0)
        self.assertEqual(result["observed_monomer_context"], 0)
        self.assertEqual(sum(len(c["outputs"]) for c in result["candidates"]), 40)
        self.assertEqual(sum(len(c["structural_context"]["monomer"]) for c in result["candidates"]), 40)
        self.assertTrue(all(c["median_worst_group_rmsd_A"] is None for c in result["candidates"]))

    def test_no_regression_guard_blocks_scalar_only_win(self):
        candidates = []
        for a in plan["assignments"]:
            revealed = a["arm"] == "context_revealed"
            c = {**a, "complete_ES": True, "median_worst_group_rmsd_A": 3. if revealed else 4.,
                 "group_median_rmsd_A": {g: 2. if revealed else 3. for g in m.GROUPS}}
            if revealed:
                c["group_median_rmsd_A"]["water"] = 3.5
            candidates.append(c)
        outcome, _ = m.decision(candidates, plan["assignments"], 1e-6)
        self.assertEqual(outcome, "no_consistent_joint_reference_recovery_advantage")
        candidates[0]["complete_ES"] = False
        outcome, _ = m.decision(candidates, plan["assignments"], 1e-6)
        self.assertEqual(outcome, "incomplete_comparison")

unittest.main(argv=[sys.argv[0]], verbosity=2)
