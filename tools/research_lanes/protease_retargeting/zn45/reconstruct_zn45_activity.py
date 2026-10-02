"""Read retained author CSVs; never execute the author notebooks.

Reconstruct the notebook's positional slope window and an explicitly labeled
comment-window sensitivity, preserving one assayed well per variant.
"""
from __future__ import annotations

import csv
import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "source"
RAW = DATA / "Zn45-SSM-raw-activity.csv"
MAP = DATA / "Zn45-SSM-normalized-activity.csv"
SCORES = DATA / "Zn45-SSM-author-AF3-data.csv"
NOTEBOOK = DATA / "Zn45-SSM-activity-screen.ipynb"
COLLECTION_HELPER = DATA / "Zn45-SSM-author-collect-data.py"
METRICS = ["complex_plddt", "per_chain_plddt_A", "per_chain_plddt_B",
           "per_chain_plddt_C", "pae_interface", "ptm", "iptm", "ipae_min"]
CORRELATION_METRICS = [m for m in METRICS if not m.startswith("per_chain_")]


def read_progress() -> pd.DataFrame:
    rows = list(csv.reader(RAW.open()))
    out = []
    for i, row in enumerate(rows):
        if row[0] != "485,528":
            continue
        wells = rows[i + 2][3:]
        for measurement in rows[i + 3:]:
            if not measurement[1] or measurement[0] in ("485,528", "485,610"):
                break
            hh, mm, ss = map(int, measurement[1].split(":"))
            for well, value in zip(wells, measurement[3:]):
                if value:
                    row_index = ord(well[0]) - ord("A")
                    column = int(well[1:])
                    out.append({
                        "well": well,
                        "time_s": 3600 * hh + 60 * mm + ss,
                        "rfu": float(value),
                        "plate_number": 5 + 2 * (row_index >= 8) + (column % 2 == 0),
                        "well_id": f"{chr(ord('A') + row_index % 8)}{(column + 1) // 2}",
                    })
    df = pd.DataFrame(out)
    mapping = pd.read_csv(MAP)
    assert not mapping.duplicated(["plate_number", "well_id"]).any()
    df = df.merge(mapping[["plate_number", "well_id", "design_name"]],
                  on=["plate_number", "well_id"], validate="many_to_one")
    assert len(df) == 384 * 41
    assert df.groupby("well").size().eq(41).all()
    assert not df.duplicated(["well", "time_s"]).any()
    return df.sort_values(["well", "time_s"])


def fit_window(df: pd.DataFrame, times: list[int]) -> tuple[pd.DataFrame, dict]:
    out = []
    for well, progress in df.groupby("well", sort=True):
        selected = progress[progress.time_s.isin(times)]
        assert len(selected) == len(times)
        slope, intercept = np.polyfit(selected.time_s, selected.rfu, 1)
        residual = selected.rfu - (intercept + slope * selected.time_s)
        out.append({"well": well, "design_name": progress.design_name.iloc[0],
                    "raw_slope_rfu_per_s": slope,
                    "fit_residual_sum_squares": float(np.sum(residual ** 2))})
    results = pd.DataFrame(out)
    blank = results.loc[results.design_name.eq("blank"), "raw_slope_rfu_per_s"]
    blank_mean = blank.mean()
    results["blank_corrected_slope_rfu_per_s"] = results.raw_slope_rfu_per_s - blank_mean
    wt = results.loc[results.design_name.eq("wt"), "blank_corrected_slope_rfu_per_s"]
    results["fold_over_wt"] = results.blank_corrected_slope_rfu_per_s / wt.mean()
    results["key"] = results.design_name.str.strip().str.lower()
    return results, {
        "times_s": times,
        "blank_slopes_rfu_per_s": blank.tolist(),
        "blank_mean_slope_rfu_per_s": blank_mean,
        "blank_corrected_WT_slopes_rfu_per_s": wt.tolist(),
        "WT_mean_slope_rfu_per_s": wt.mean(),
        "WT_sample_SD_rfu_per_s": wt.std(ddof=1),
        "WT_sample_CV": wt.std(ddof=1) / wt.mean(),
    }


def correlation_table(df: pd.DataFrame) -> dict:
    return {metric: {
        "n_assayed_variants": len(df),
        "Pearson_r": float(df[metric].corr(df.fold_over_wt)),
        "Spearman_rho": float(df[metric].rank(method="average").corr(df.fold_over_wt.rank(method="average"))),
    } for metric in CORRELATION_METRICS}


def summarize_filter(df: pd.DataFrame, passed: pd.Series) -> dict:
    result = {"pass_count": int(passed.sum()), "fail_count": int((~passed).sum())}
    for threshold in (1.0, 1.3, 1.5, 3.0):
        improved = df.fold_over_wt > threshold
        result[f"fold_gt_{threshold}"] = {
            "all_variants_count": int(improved.sum()),
            "retained_count": int((improved & passed).sum()),
            "excluded_design_names": df.loc[improved & ~passed, "design_name"].tolist(),
        }
    return result


def notebook_checkpoints(progress: pd.DataFrame, wells: pd.DataFrame) -> dict:
    notebook = json.loads(NOTEBOOK.read_text())

    def printed_text(cell: int) -> str:
        return "".join("".join(out.get("text", [])) +
                       "".join(out.get("data", {}).get("text/plain", []))
                       for out in notebook["cells"][cell].get("outputs", []))

    def displayed_rows(cell: int) -> list[list[str]]:
        html = "".join("".join(out.get("data", {}).get("text/html", []))
                       for out in notebook["cells"][cell].get("outputs", []))
        return [re.findall(r"<t[dh][^>]*>\s*(.*?)\s*</t[dh]>", row, re.S)
                for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S)]

    progress_checks = []
    for row in displayed_rows(6)[1:]:
        if row[0] == "...":
            continue
        _, well, time, rfu, plate, source_well, name = row
        actual = progress[(progress.well == well) & (progress.time_s == int(time))].iloc[0]
        assert actual.rfu == float(rfu)
        assert actual.plate_number == int(plate)
        assert actual.well_id == source_well and actual.design_name == name
        progress_checks.append({"well": well, "time_s": int(time), "rfu": float(rfu)})
    assert "15744 rows" in printed_text(6)
    slope_checks = []
    grouped = wells.groupby("design_name").agg(
        slope=("blank_corrected_slope_rfu_per_s", "mean"),
        fold=("fold_over_wt", "mean"), n=("well", "nunique"))
    for row in displayed_rows(11)[1:]:
        _, name, _, _, slope, fold, count = row
        actual = grouped.loc[name]
        assert abs(actual.slope - float(slope)) < 5e-7
        assert abs(actual.fold - float(fold)) < 5e-7
        assert actual.n == int(count)
        slope_checks.append({"design_name": name, "displayed_slope": float(slope),
                             "displayed_fold": float(fold)})
    printed_names = re.findall(r"chainA_[A-Z]\d+[A-Z]", printed_text(23))
    observed_names = wells.loc[wells.fold_over_wt.gt(1.5), "design_name"].tolist()
    assert set(printed_names) == set(observed_names) and len(printed_names) == 19
    return {
        "notebook_sha256": hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest(),
        "cell6_progress_display": {"exact_rows_verified": progress_checks,
                                   "displayed_total_rows_matches": 15744,
                                   "exact_match_includes_plate_well_variant_metadata": True},
        "cell11_normalized_result_display": {"verified_rows": slope_checks,
                                             "absolute_tolerance": 5e-7},
        "cell23_retest_list": {"exact_names_verified": printed_names, "count": 19},
        "identity_boundary": "Notebook references Book2.csv; deposited member is ssm.csv, whose experiment-header basename is 260112_zn45_ssm_plate6.xpt and date is 1/14/2026. Saved notebook raw-value, mapping and normalized-output checkpoints agree, but original Book2.csv bytes are unavailable for a file-hash identity check. This verifies displayed checkpoints, not every unpublished intermediate.",
    }


def main() -> None:
    progress = read_progress()
    # Notebook cell 10 executes iloc[2:5]. Actual data begin at 0,180,360,...
    # The printed comment incorrectly says 540-900 s / fourth-sixth points.
    primary, primary_control = fit_window(progress, [360, 540, 720])
    sensitivity, sensitivity_control = fit_window(progress, [540, 720, 900])
    primary.to_csv(ROOT / "zn45_reconstructed_well_activity.csv", index=False)
    singles = primary[primary.key.str.startswith("chaina_")].copy()
    assert len(singles) == 378 and singles.key.nunique() == 378
    parts = singles.design_name.str.extract(r"chainA_([A-Z])(\d+)([A-Z])")
    singles[["parent_amino_acid", "position", "mutant_amino_acid"]] = parts
    singles.position = singles.position.astype(int)
    assert singles.groupby("position").size().eq(18).all()
    assert not singles.mutant_amino_acid.eq("C").any()
    scores = pd.read_csv(SCORES)
    scores["key"] = scores.description.str.strip().str.lower()
    assert scores.groupby("key").size().eq(5).all()
    assert len(scores) == 1895
    assert set(singles.key) < set(scores.key)
    mean_scores = scores.groupby("key")[METRICS].mean()
    median_scores = scores.groupby("key")[METRICS].median()
    joined = singles.merge(mean_scores, on="key", validate="one_to_one")
    for metric in METRICS:
        for agg in ("min", "max", "std"):
            values = scores.groupby("key")[metric].agg(agg)
            joined[f"{metric}_five_sample_{agg}"] = joined.key.map(values)
    # Exact computational-heatmap selection, distinct from the all-sample scatter.
    heatmap_scores = scores.drop_duplicates("key", keep="last").set_index("key")[METRICS]
    heatmap_join = singles.merge(heatmap_scores, on="key", validate="one_to_one")
    for metric in METRICS:
        joined[f"{metric}_author_heatmap"] = joined.key.map(heatmap_scores[metric])
    joined.to_csv(ROOT / "zn45_activity_af3_join.csv", index=False)
    filter_mean = (joined.complex_plddt > 94) & (joined.ipae_min < 1.5)
    med_join = singles.merge(median_scores, on="key", validate="one_to_one")
    filter_median = (med_join.complex_plddt > 94) & (med_join.ipae_min < 1.5)
    scores["joint_filter_pass"] = (scores.complex_plddt > 94) & (scores.ipae_min < 1.5)
    n_pass = scores.groupby("key").joint_filter_pass.sum()
    pass_any = joined.key.map(n_pass).gt(0)
    pass_all = joined.key.map(n_pass).eq(5)
    sens = sensitivity[sensitivity.key.str.startswith("chaina_")]
    sens_join = joined[["key", "design_name", "fold_over_wt"]].merge(
        sens[["key", "fold_over_wt"]], on="key", suffixes=("_executed", "_comment"))
    sample_stats = {}
    sample_pattern = re.compile(r"sample[-_](\d+)")
    scores["sample_id"] = scores.pdb_path.apply(lambda p: int(sample_pattern.search(p).group(1)))
    for sample, table in scores.groupby("sample_id"):
        one = singles.merge(table[["key"] + METRICS], on="key", validate="one_to_one")
        passed = (one.complex_plddt > 94) & (one.ipae_min < 1.5)
        sample_stats[str(sample)] = {"filter": summarize_filter(one, passed),
                                    "all_correlations": correlation_table(one),
                                    "passing_correlations": correlation_table(one[passed])}
    counts_by_position = []
    for position, table in joined.groupby("position"):
        best = table.loc[table.fold_over_wt.idxmax()]
        counts_by_position.append({"position": int(position), "n_substitutions": len(table),
                                   "best_design": best.design_name,
                                   "best_fold": float(best.fold_over_wt),
                                   "n_fold_gt_1p3": int(table.fold_over_wt.gt(1.3).sum()),
                                   "n_fold_gt_1p5": int(table.fold_over_wt.gt(1.5).sum())})
    summary = {
        "analysis_type": "Retrospective independent reconstruction of author CSV and notebook logic; no author notebook execution",
        "source_files": {p.name: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                  "bytes": p.stat().st_size} for p in (RAW, MAP, SCORES, NOTEBOOK, COLLECTION_HELPER,
                                                                       DATA / "Zn45-SSM-computational.ipynb")},
        "notebook_checkpoint_verification": notebook_checkpoints(progress, primary),
        "denominator": {"single_variants": len(singles), "sites": singles.position.nunique(),
                        "wells_per_single_variant": 1, "WT_wells": 3, "blank_wells": 3,
                        "time_points_per_well": 41, "time_range_s": [0, 7200],
                        "missing_activity_variants": [], "missing_score_variants": [],
                        "AF3_samples_per_variant": 5, "AF3_seeds_per_variant": 1,
                        "sample_rows_are_not_independent_assayed_variants": True},
        "executed_notebook_window": primary_control,
        "source_thresholds": {
            "single_screen_retrospective_AF3_filter": {
                "logic": "AND", "complex_plddt": {"operator": ">", "value": 94, "unit": "pLDDT score"},
                "ipae_min": {"operator": "<", "value": 1.5, "unit": "angstrom"},
                "source": "Chen v3 Supplementary Discussion 6; described retrospectively for the single-mutation landscape",
                "aggregation_for_primary_analysis": "Arithmetic mean over five AF3 samples from seed1, chosen explicitly for this retrospective reconstruction",
            },
            "screen_retest_signal": {"endpoint": "fold of blank-corrected RFU slope over WT", "operator": ">", "value": 1.5, "unit": "dimensionless fold", "source": "Supplementary screening methods and activity notebook cell22"},
            "distinct_combination_ordering_filter": {"complex_plddt_gt": 93, "ipae_min_lt_A": 1.5, "source": "Supplementary screening methods; NOT used for the 211-of-378 single-screen result"},
        },
        "metric_definition_and_quarantine": {
            "helper_sha256": hashlib.sha256(COLLECTION_HELPER.read_bytes()).hexdigest(),
            "complex_plddt": "sum(atom_plddts) / len(atom_plddts), across the entire complex",
            "ipae_min": "min(chain_pair_pae_min[0][1], chain_pair_pae_min[1][0]) from summary_confidences, between protein A and substrate B",
            "pae_interface": "0.5 * mean(PAE_A_to_B) + 0.5 * mean(PAE_B_to_A), using declared protein sequence lengths",
            "per_chain_plddt_columns": "Retained as source-exported numbers only and omitted from inferential correlations: the helper slices atom_plddts with residue sequence lengths, not atom-chain indices, so biological interpretation as chain means is quarantined.",
        },
        "comment_window_sensitivity": sensitivity_control,
        "window_discrepancy": "Author cell10 names/comments 540-900 seconds, but iloc[2:5] selects 360,540,720 seconds from the captured data.",
        "reconstructed_gt1p5_variants": joined.loc[joined.fold_over_wt.gt(1.5), ["design_name", "fold_over_wt"]].to_dict("records"),
        "positions": counts_by_position,
        "five_sample_mean": {"all": correlation_table(joined),
                             "above_joint_source_threshold": correlation_table(joined[filter_mean]),
                             "filter": summarize_filter(joined, filter_mean)},
        "five_sample_median_filter": summarize_filter(med_join, filter_median),
        "author_heatmap_choice_sensitivity": {
            "method": "Last CSV score row for each mutant, reproducing computational notebook cell9 overwrite. Activity notebook cells27-28 scatter all five samples instead; that scatter is not reduced to these last rows.",
            "filter": summarize_filter(heatmap_join, (heatmap_join.complex_plddt > 94) & (heatmap_join.ipae_min < 1.5)),
            "all_correlations": correlation_table(heatmap_join),
            "passing_correlations": correlation_table(heatmap_join[(heatmap_join.complex_plddt > 94) & (heatmap_join.ipae_min < 1.5)]),
        },
        "at_least_one_sample_passes_filter": summarize_filter(joined, pass_any),
        "all_five_samples_pass_filter": summarize_filter(joined, pass_all),
        "per_sample": sample_stats,
        "window_sensitivity": {
            "Pearson_r": float(sens_join.fold_over_wt_executed.corr(sens_join.fold_over_wt_comment)),
            "Spearman_rho": float(sens_join.fold_over_wt_executed.rank(method="average").corr(sens_join.fold_over_wt_comment.rank(method="average"))),
            "comment_window_n_gt1p5": int(sens_join.fold_over_wt_comment.gt(1.5).sum()),
            "comment_window_n_gt1p3": int(sens_join.fold_over_wt_comment.gt(1.3).sum()),
            "gt1p5_membership_changes": sens_join.loc[
                sens_join.fold_over_wt_executed.gt(1.5) != sens_join.fold_over_wt_comment.gt(1.5)
            ].to_dict("records"),
        },
        "inference_limit": "Correlations describe an exposed, single-scaffold, fixed-reporter screen. Each mutant has one well, shared WT/blank normalization, and five model samples. Neither model samples nor timepoints are experimental replicates; no confidence interval or predictive validation is claimed.",
        "csv_metric_columns": "Bare metric names are the arithmetic mean over five AF3 samples from one seed. Suffixes identify sample minimum/maximum/SD and the exact author computational-heatmap choice.",
    }
    (ROOT / "zn45_activity_score_analysis.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"denominator": summary["denominator"],
                      "controls": primary_control,
                      "mean_filter": summary["five_sample_mean"]["filter"],
                      "correlations": {k: {x: summary["five_sample_mean"][k][x]
                                           for x in ("complex_plddt", "ipae_min", "pae_interface")}
                                       for k in ("all", "above_joint_source_threshold")},
                      "window_sensitivity": summary["window_sensitivity"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA,
                        help="Directory containing the six retained author source files")
    parser.add_argument("--out-dir", type=Path, default=ROOT,
                        help="Directory for reconstructed CSV and JSON outputs")
    args = parser.parse_args()
    DATA, ROOT = args.data_dir.resolve(), args.out_dir.resolve()
    ROOT.mkdir(parents=True, exist_ok=True)
    RAW = DATA / "Zn45-SSM-raw-activity.csv"
    MAP = DATA / "Zn45-SSM-normalized-activity.csv"
    SCORES = DATA / "Zn45-SSM-author-AF3-data.csv"
    NOTEBOOK = DATA / "Zn45-SSM-activity-screen.ipynb"
    COLLECTION_HELPER = DATA / "Zn45-SSM-author-collect-data.py"
    main()
