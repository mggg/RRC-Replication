"""
Last Updated: 16-01-2025
Author: Peter Rock <peter@mggg.org>

This script is used to generate the Wasserstein trace plots for the VA ensembles.
"""

import pandas as pd
from pathlib import Path
from helper_files.wasserstein_trace_tally import wasserstein_trace_v_full
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
    reversible_sample_1 = "../../hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_CD_12_20241106_152157_tallies.parquet"
    reversible_sample_2 = "../../hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_CD_16_20240618_174413_tallies.parquet"
    reversible_sample_3 = "../../hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_rand_dist_eps0p01_20241108_130356_tallies.parquet"
    forest_sample = "../../hpc_files/hpc_processed_data/VA/VA_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_11_20241112_124346_tallies.parquet"

    out_folder = "../figures"
    out_path = Path(out_folder)

    n_accepted = 3_300_000
    n_items = 800

    # n_accepted = 300_000
    # n_items = 5

    # ======================
    # + REV RECOM SAMPLE 1 +
    # ======================
    rev_df1 = pd.read_parquet(reversible_sample_1)
    rev_df2 = pd.read_parquet(reversible_sample_2)
    rev_df3 = pd.read_parquet(reversible_sample_3)
    forest_df = pd.read_parquet(forest_sample)

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

    # ======================
    # + REV RECOM SAMPLE 3 +
    # ======================
    rev_df3_dem = rev_df3[rev_df3["sum_columns"] == "G16DPRS"].reset_index()
    rev_df3_rep = rev_df3[rev_df3["sum_columns"] == "G16RPRS"].reset_index()
    rev_df3_shares_total = rev_df3_dem[[f"district_{i}" for i in range(1, 12)]] / (
        rev_df3_dem[[f"district_{i}" for i in range(1, 12)]]
        + rev_df3_rep[[f"district_{i}" for i in range(1, 12)]]
    )
    rev_df3_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 12)},
        inplace=True,
    )
    rev_df3_shares_total.sort_index(axis=1, inplace=True)

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

    # =======================
    # + COLLECT WASSERSTEIN +
    # =======================
    was_full_1f_ticks, was_full_1f_distances = wasserstein_trace_v_full(
        shares_df=rev_df1_shares_total.iloc[:n_accepted, :],
        full_df=forest_df_shares_total,
        weights=rev_df1_dem.iloc[:n_accepted, :]["n_reps"],
        weights_full=forest_df_dem["n_reps"],
        resolution=n_accepted / n_items,
    )

    was_full_2f_ticks, was_full_2f_distances = wasserstein_trace_v_full(
        shares_df=rev_df2_shares_total.iloc[:n_accepted, :],
        full_df=forest_df_shares_total,
        weights=rev_df2_dem.iloc[:n_accepted, :]["n_reps"],
        weights_full=forest_df_dem["n_reps"],
        resolution=n_accepted / n_items,
    )

    was_full_3f_ticks, was_full_3f_distances = wasserstein_trace_v_full(
        shares_df=rev_df3_shares_total.iloc[:n_accepted, :],
        full_df=forest_df_shares_total,
        weights=rev_df3_dem.iloc[:n_accepted, :]["n_reps"],
        weights_full=forest_df_dem["n_reps"],
        resolution=n_accepted / n_items,
    )

    # ======================
    # + START MAKING PLOTS +
    # ======================
    _, ax = plt.subplots(figsize=(25, 10), dpi=400)

    sns.lineplot(
        x=was_full_1f_ticks,
        y=was_full_1f_distances,
        ax=ax,
        linewidth=3,
        color=colors[1],
        label="Rev ReCom DYNAMIC (5B Proposed)     CD 16 vs Full Forest STATIC (10M Proposed)",
    )
    sns.lineplot(
        x=was_full_2f_ticks,
        y=was_full_2f_distances,
        ax=ax,
        linewidth=3,
        color=colors[0],
        label="Rev ReCom DYNAMIC (5B Proposed)     CD 12 vs Full Forest STATIC (10M Proposed)",
    )
    sns.lineplot(
        x=was_full_3f_ticks,
        y=was_full_3f_distances,
        ax=ax,
        linewidth=3,
        color=colors[3],
        label="Rev ReCom DYNAMIC (5B Proposed) Rand Plan vs Full Forest STATIC (10M Proposed)",
    )

    ax.legend(prop={"size": 20})
    ax.tick_params(axis="both", labelsize=14)

    plt.savefig(
        out_path.joinpath(
            "Wasserstein_distances_VA_comparison_Dem_Shares_v_Full_Forest.png"
        ),
        bbox_inches="tight",
    )
