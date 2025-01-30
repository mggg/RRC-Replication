"""
Last Updated: 16-01-2025
Author: Peter Rock <peter@mggg.org>

This script is used to generate the histograms for comparing the 50x50 cut edge distributions
for Forest ReCom and Reversible ReCom.
"""

import pandas as pd
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

colors = [
    "#0099cd",
    "#00cd99",
    "#ffca5d",
    "#99cd00",
    "#cd0099",
    "#9900cd",
    "#8dd3c7",
    "#bebada",
    "#fb8072",
    "#80b1d3",
]


def make_plot_dists(rrc_forest, lower, upper, n_dists, glob_expr):
    """
    Makes the histograms for the 50x50 cut edge distributions comparing
    Forest ReCom and Reversible ReCom.

    Parameters
    ----------
    rrc_forest : dict
        A dictionary mapping the legend label for a particular file to the path to that file.
    lower : float
        The lower bound on the x-axis to plot.
    upper : float
        The upper bound on the x-axis to plot.
    n_dists : int
        The number of districts the map is split into.
    glob_expr : str
        The regex passed to glob to find the files to plot.

    Returns
    -------
    None
    """

    out_path = Path("../figures")
    data_path = Path("../../hpc_files/hpc_processed_data/50x50")

    _, ax = plt.subplots(figsize=(25, 10), dpi=400)

    for i, (n, f) in enumerate(rrc_forest.items()):
        df = pd.read_parquet(f)
        prob_df = df.groupby("cut_edges").sum().reset_index()
        prob_df["prob"] = 100 * (prob_df["n_reps"] / prob_df["n_reps"].sum())

        ax.bar(
            prob_df["cut_edges"],
            prob_df["prob"],
            width=1,
            edgecolor=None,
            color=colors[i],
            alpha=0.8,
            label=n,
        )

    ax.set_xlim(lower - 20, upper + 20)
    ax.set_xticks(list(range(lower, upper, 50)))
    ax.set_xticklabels([str(i) for i in range(lower, upper, 50)])
    ax.set_yticks([])
    ax.legend(loc="right", bbox_to_anchor=(1.12, 0.5))
    plt.savefig(
        out_path.joinpath(f"50x50_{n_dists}_dist_forest_rrc_comparison.png"),
        bbox_inches="tight",
    )

    _, ax = plt.subplots(figsize=(25, 10), dpi=400)

    recom_files = glob(str(data_path.joinpath(glob_expr).resolve()))
    recom_files = [Path(file).resolve() for file in recom_files]
    recom_files.sort()

    all_recom_files = {}

    for file in recom_files:
        lst = file.name.split("_")
        all_recom_files[f"{lst[1]} (1B proposed)"] = file

    all_recom_files

    for i, (n, f) in enumerate(all_recom_files.items()):
        df = pd.read_parquet(f)
        prob_df = df.groupby("cut_edges").sum().reset_index()
        prob_df["prob"] = 100 * (prob_df["n_reps"] / prob_df["n_reps"].sum())

        ax.bar(
            prob_df["cut_edges"],
            prob_df["prob"],
            width=1,
            edgecolor=None,
            color=colors[i + 3],
            alpha=0.8,
            label=n.replace("Recom", "ReCom "),
        )

    ax.set_xlim(lower - 20, upper + 20)
    ax.set_xticks(list(range(lower, upper, 50)))
    ax.set_xticklabels([str(i) for i in range(lower, upper, 50)])
    ax.set_yticks([])
    ax.legend(loc="right", bbox_to_anchor=(1.12, 0.5))
    plt.savefig(
        out_path.joinpath(f"50x50_{n_dists}_dist_ReCom_comparison.png"),
        bbox_inches="tight",
    )


if __name__ == "__main__":
    rrc_forest_10 = {
        "RRC (10B proposed)": "../../hpc_files/hpc_processed_data/50x50/50x50_RevReCom_steps_10000000000_plan_50x5_strip_20240618_174413_cut_edges.parquet",
        "Forest (10M proposed)": "../../hpc_files/hpc_processed_data/50x50/50x50_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_10_20240830_142334_cut_edges.parquet",
    }

    make_plot_dists(rrc_forest_10, 350, 601, 10, "*_ReCom*50x5_*")

    rrc_forest_25 = {
        "RRC (10B proposed)": "../../hpc_files/hpc_processed_data/50x50/50x50_RevReCom_steps_10000000000_plan_10x10_square_20240618_174413_cut_edges.parquet",
        "Forest (10M proposed)": "../../hpc_files/hpc_processed_data/50x50/50x50_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_25_20240830_142334_cut_edges.parquet",
    }

    make_plot_dists(rrc_forest_25, 650, 880, 25, "*_ReCom*10x10_*")

    rrc_forest_50 = {
        "RRC (10B proposed)": "../../hpc_files/hpc_processed_data/50x50/50x50_RevReCom_steps_10000000000_plan_50x1_strip_20240618_174413_cut_edges.parquet",
        "Forest (10M proposed)": "../../hpc_files/hpc_processed_data/50x50/50x50_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_50_20240830_142334_cut_edges.parquet",
    }

    make_plot_dists(rrc_forest_50, 900, 1180, 50, "*_ReCom*50x1_*")
