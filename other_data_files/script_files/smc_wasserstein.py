"""
Last Updated: 11-11-2025 (Nov 11)
Author: Parker Rule, Peter Rock <peter@mggg.org>

This script is used to generate the scatter plots for the SMC ensembles. Most of this code is
adapted from code written by Parker Rule for an earlier version of the RRC paper.
"""

import glob
import pyreadr
import geopandas as gpd
from pathlib import Path
from joblib import Parallel, delayed
from joblib_progress import joblib_progress

import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from scipy.stats import wasserstein_distance
from tqdm import tqdm
from gerrychain import Graph, Partition
from gerrychain.updaters import cut_edges

GROUND_TRUTH = """32      7.32191421608e11
40      2.82316256e8
39      1.6843817279999998e9
35      1.86993438208e11
34      3.6642892581799994e11
42      1.9495219999999998e6
29      2.5066583999999997e11
37      2.6977180927999996e10
28      7.344675e10
38      7.588753206e9
31      6.983941968e11
36      7.854102064799998e10
41      3.1884255999999996e7
33      5.77889926624e11
30      5.286711393e11"""


def load_smc(graph, rds_path, weights_path=None) -> Counter:
    """Computes the cut edge count distribution of an SMC grid run."""
    run_plans = pyreadr.read_r(rds_path)
    assignments = run_plans[None].values.astype(int).T.copy()
    partitions = [
        Partition(
            assignment=dict(enumerate(row)),
            graph=graph,
            updaters={"cut_edges": cut_edges},
        )
        for row in assignments
    ]

    if weights_path is not None:
        weights = pyreadr.read_r(weights_path)[None].values.T
        weighted_hist = defaultdict(float)
        for weight, part in zip(weights[0].tolist(), partitions):
            weighted_hist[len(part["cut_edges"])] += weight
        return partitions, weighted_hist
    return partitions, Counter(len(part["cut_edges"]) for part in partitions)


def determine_wasserstein_to_truth(weights_path, graph, ref_counts, ref_weights):
    plans_path = weights_path.replace(".wgt", ".plans")
    n_samples = int(float(plans_path.split(" __ ")[-1].split(" .rds")[0]))

    _, hist_smc_weighted = load_smc(
        graph=graph,
        rds_path=plans_path,
        weights_path=weights_path,
    )
    smc_counts = list(hist_smc_weighted.keys())
    smc_weights = list(hist_smc_weighted.values())
    smc_full_enum_distance = wasserstein_distance(
        smc_counts,
        ref_counts,
        smc_weights,
        ref_weights,
    )

    return n_samples, smc_full_enum_distance


def collect_wasserstein_data(
    smc_shapefile,
    smc_trace_prefix,
    output_csv_file,
):
    ref_counts = [int(line.split()[0]) for line in GROUND_TRUTH.split("\n")]
    ref_weights = [float(line.split()[1]) for line in GROUND_TRUTH.split("\n")]

    if smc_shapefile is not None:
        gdf = gpd.read_file(smc_shapefile)
        gdf.crs = "epsg:26918"  # fake! (suppresses spurious projection warnings)
        graph = Graph.from_geodataframe(gdf)
    else:
        gdf = graph = None

    weights_files = glob.glob(f"{smc_trace_prefix}*.rds .wgt")
    with joblib_progress(
        description="Computing Wasserstein Distances", total=len(weights_files)
    ):
        all_pairs = Parallel(n_jobs=-1)(
            delayed(determine_wasserstein_to_truth)(
                weights_path=weights_path,
                graph=graph,
                ref_counts=ref_counts,
                ref_weights=ref_weights,
            )
            for weights_path in weights_files
        )

    all_pairs.sort()
    with open(Path(output_csv_file), "w") as f:
        f.write("batch_size,wasserstein_distance\n")
        for x, y in all_pairs:
            f.write(f"{x},{y}\n")


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]
    output_folder = f"{top_dir}/other_data_files/processed_data_files/7x7"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    collect_wasserstein_data(
        smc_shapefile=f"{top_dir}/shapefiles/7x7/7x7.shp",
        smc_trace_prefix=f"{top_dir}/other_data_files/raw_data_files/7x7_smc/7x7_compactness_1",
        output_csv_file=f"{output_folder}/7x7_wasserstein_5k_to_100k_data.csv",
    )

    collect_wasserstein_data(
        smc_shapefile=f"{top_dir}/shapefiles/7x7/7x7.shp",
        smc_trace_prefix=f"{top_dir}/other_data_files/raw_data_files/7x7_smc/7x7_short_compactness_1",
        output_csv_file=f"{output_folder}/7x7_wasserstein_50_to_5000_data.csv",
    )
