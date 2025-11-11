"""
Last Updated: 10-11-2025 (Nov 10)
Author: Peter Rock <peter@mggg.org>

This script is used to generate the Wasserstein trace plots for the VA ensembles.
"""

import pandas as pd
from pathlib import Path
from helper_files.wasserstein_trace_tally import wasserstein_trace_shares
from helper_files.legend_saver import save_legend_png, marker_handles
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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


def add_shares_df(df):
    """
    Creats a new dataframe with the democratic vote share for each district.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the election data to extract the vote shares from.

    Returns
    -------
    pandas.DataFrame
        The dataframe containing the democratic vote shares for each district.
    """
    df_dem = df[df["sum_columns"] == "G16DPRS"].reset_index()
    df_rep = df[df["sum_columns"] == "G16RPRS"].reset_index()
    df_shares_total = df_dem[[f"district_{i}" for i in range(1, 12)]] / (
        df_dem[[f"district_{i}" for i in range(1, 12)]]
        + df_rep[[f"district_{i}" for i in range(1, 12)]]
    )
    df_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 12)},
        inplace=True,
    )
    df_shares_total.sort_index(axis=1, inplace=True)
    return df_shares_total


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]

    reversible_sample_1 = f"{top_dir}/hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_CD_12_20241106_152157_tallies.parquet"
    reversible_sample_2 = f"{top_dir}/hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_CD_16_20240618_174413_tallies.parquet"
    forest_sample = f"{top_dir}/hpc_files/hpc_processed_data/VA/VA_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_11_20241112_124346_tallies.parquet"

    out_folder = f"{top_dir}/figure_and_table_generation/figures"
    out_path = Path(out_folder)

    n_accepted = 1_900_000
    n_items = 500

    rev_df1 = pd.read_parquet(reversible_sample_1)
    rev_df2 = pd.read_parquet(reversible_sample_2)
    forest_df = pd.read_parquet(forest_sample)

    # ======================
    # + REV RECOM SAMPLE 1 +
    # ======================
    rev_df1_dem = rev_df1[rev_df1["sum_columns"] == "G16DPRS"].reset_index()
    rev_df1_rep = rev_df1[rev_df1["sum_columns"] == "G16RPRS"].reset_index()
    rev_df1_shares_total = rev_df1_dem[[f"district_{i}" for i in range(1, 12)]] / (
        rev_df1_dem[[f"district_{i}" for i in range(1, 12)]]
        + rev_df1_rep[[f"district_{i}" for i in range(1, 12)]]
    )
    rev_df1_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 12)},
        inplace=True,
    )
    rev_df1_shares_total.sort_index(axis=1, inplace=True)
    rev_df1_shares_total.reset_index(inplace=True, drop=True)

    # ======================
    # + REV RECOM SAMPLE 2 +
    # ======================
    rev_df2_dem = rev_df2[rev_df2["sum_columns"] == "G16DPRS"].reset_index()
    rev_df2_rep = rev_df2[rev_df2["sum_columns"] == "G16RPRS"].reset_index()
    rev_df2_shares_total = rev_df2_dem[[f"district_{i}" for i in range(1, 12)]] / (
        rev_df2_dem[[f"district_{i}" for i in range(1, 12)]]
        + rev_df2_rep[[f"district_{i}" for i in range(1, 12)]]
    )
    rev_df2_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 12)},
        inplace=True,
    )
    rev_df2_shares_total.sort_index(axis=1, inplace=True)
    rev_df2_shares_total.reset_index(inplace=True, drop=True)

    # =======================
    # + FOREST RECOM SAMPLE +
    # =======================
    forest_df_dem = forest_df[forest_df["sum_columns"] == "G16DPRS"].reset_index()
    forest_df_rep = forest_df[forest_df["sum_columns"] == "G16RPRS"].reset_index()
    forest_df_shares_total = forest_df_dem[[f"district_{i}" for i in range(1, 12)]] / (
        forest_df_dem[[f"district_{i}" for i in range(1, 12)]]
        + forest_df_rep[[f"district_{i}" for i in range(1, 12)]]
    )
    forest_df_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 12)},
        inplace=True,
    )
    forest_df_shares_total.sort_index(axis=1, inplace=True)
    forest_df_shares_total.reset_index(inplace=True, drop=True)

    # =======================
    # + COLLECT WASSERSTEIN +
    # =======================
    was_rrc_compare_ticks, was_rrc_compare_distances = wasserstein_trace_shares(
        shares1_df=rev_df1_shares_total.iloc[:n_accepted, :],
        shares2_df=rev_df2_shares_total.iloc[:n_accepted, :],
        weights1=rev_df1_dem.iloc[:n_accepted, :]["n_reps"],
        weights2=rev_df2_dem.iloc[:n_accepted, :]["n_reps"],
        resolution=n_accepted / n_items,
    )

    was_full_1f_ticks, was_full_1f_distances = wasserstein_trace_shares(
        shares1_df=rev_df1_shares_total.iloc[:n_accepted, :],
        shares2_df=forest_df_shares_total.iloc[:n_accepted, :],
        weights1=rev_df1_dem.iloc[:n_accepted, :]["n_reps"],
        weights2=forest_df_dem.iloc[:n_accepted, :]["n_reps"],
        resolution=n_accepted / n_items,
    )

    was_full_2f_ticks, was_full_2f_distances = wasserstein_trace_shares(
        shares1_df=rev_df2_shares_total.iloc[:n_accepted, :],
        shares2_df=forest_df_shares_total.iloc[:n_accepted, :],
        weights1=rev_df2_dem.iloc[:n_accepted, :]["n_reps"],
        weights2=forest_df_dem.iloc[:n_accepted, :]["n_reps"],
        resolution=n_accepted / n_items,
    )

    # ======================
    # + START MAKING PLOTS +
    # ======================
    _, ax = plt.subplots(figsize=(25, 10), dpi=400)

    sns.lineplot(
        x=was_rrc_compare_ticks,
        y=was_rrc_compare_distances,
        ax=ax,
        linewidth=3,
        color=colors[0],
    )
    sns.lineplot(
        x=was_full_1f_ticks,
        y=was_full_1f_distances,
        ax=ax,
        linewidth=3,
        color=colors[1],
    )
    sns.lineplot(
        x=was_full_2f_ticks,
        y=was_full_2f_distances,
        ax=ax,
        linewidth=3,
        color=colors[3],
    )

    ax.tick_params(axis="both", labelsize=14)
    ax.set_xlabel("accepted", loc="right", fontsize=12)
    ticks = list(range(250_000, 2_000_000, 250_000))
    ax.set_xticks(ticks)
    ax.set_xlim(0, 1_900_000)
    ax.set_xticklabels([f"{i/1_000_000:.2f}M" for i in ticks])

    plt.savefig(
        out_path.joinpath(
            "Wasserstein_distances_VA_comparison_Dem_Shares_rrc_and_forest.png"
        ),
        bbox_inches="tight",
    )
    plt.close()

    labels = [
        "RevReCom1 vs RevReCom2",
        "RevReCom1 vs Forest",
        "RevReCom2 vs Forest",
    ]
    colors_legend = [colors[0], colors[1], colors[3]]
    handles = marker_handles(labels=labels, colors=colors_legend, linestyle="-")

    save_legend_png(
        handles=handles,
        filename=out_path.joinpath(
            "Wasserstein_distances_VA_comparison_Dem_Shares_rrc_and_forest_legend.png"
        ),
        ncol=1,
        frameon=True,
        dpi=200,
        label_fontsize=14,
    )
