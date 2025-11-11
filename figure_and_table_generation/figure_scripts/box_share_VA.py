"""
Last Updated: 10-11-2025 (Nov 10)
Author: Peter Rock <peter@mggg.org>

This script is used to generate the boxplots for the Democratic Vote Shares for
each of the districts in VA. Boxplots are constructed for three different
ensembles of Reversible ReCom and one ensemble of Forest ReCom.

The reversible ensembles each contain 5B proposed steps and start from 3 different seed
plans: CD_12, CD_16, and rand_dist_eps0p01 (random districts with population deviance
of 0.01). The Forest ReCom ensemble is a single ensemble containing 1M proposed steps.
"""

import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from helper_files.box_share_helpers import get_weighted_stats, weighted_quantile
from helper_files.legend_saver import save_legend_png, box_handles

colors = [
    "#0099cd",
    "#ffca5d",
    "#fb8072",
    "#00cd99",
]

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]

    reversible_sample_1 = f"{top_dir}/hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_CD_12_20241106_152157_tallies.parquet"
    reversible_sample_2 = f"{top_dir}/hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_CD_16_20240618_174413_tallies.parquet"
    reversible_sample_3 = f"{top_dir}/hpc_files/hpc_processed_data/VA/VA_RevReCom_steps_5000000000_rng_seed_278986_plan_rand_dist_eps0p01_20241108_130356_tallies.parquet"
    forest_sample = f"{top_dir}/hpc_files/hpc_processed_data/VA/VA_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_11_20241112_124346_tallies.parquet"

    out_folder = f"{top_dir}/figure_and_table_generation/figures"
    out_path = Path(out_folder)

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
    rev_df1_weights = rev_df1_dem["n_reps"].to_numpy()
    rev_array1 = rev_df1_shares_total.to_numpy()
    rev_array1.sort(axis=1)

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
    rev_df2_weights = rev_df2["n_reps"].to_numpy()
    rev_array2 = rev_df2_shares_total.to_numpy()
    rev_array2.sort(axis=1)

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
    rev_df3_weights = rev_df3["n_reps"].to_numpy()
    rev_array3 = rev_df3_shares_total.to_numpy()
    rev_array3.sort(axis=1)

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
    forest_df_weights = forest_df["n_reps"].to_numpy()
    forest_array = forest_df_shares_total.to_numpy()
    forest_array.sort(axis=1)

    # ======================
    # + START MAKING PLOTS +
    # ======================
    fig, ax = plt.subplots(figsize=(15, 10), dpi=400)

    arrs = [rev_array1, rev_array2, rev_array3, forest_array]
    weights = [rev_df1_weights, rev_df2_weights, rev_df3_weights, forest_df_weights]

    ax.axhline(y=0.5, color="lightgrey", linestyle="--")

    handles = []
    from tqdm import tqdm

    for j in range(len(arrs)):
        arr = arrs[j]
        for i in tqdm(range(arr.shape[1])):
            data = arr[:, i]
            q1, med, q3 = get_weighted_stats(data, weights[j])
            whislo = weighted_quantile(data, 0.01, weights[j])
            whishi = weighted_quantile(data, 0.99, weights[j])
            boxplot_stats = {
                "med": med,
                "q1": q1,
                "q3": q3,
                "iqr": q3 - q1,
                "whislo": whislo,
                "whishi": whishi,
                "fliers": [],
            }

            res = ax.bxp(
                [boxplot_stats],
                positions=[2 * (i + 1) + (j * 0.45)],
                capprops={"color": colors[j]},
                boxprops={"facecolor": colors[j], "edgecolor": colors[j], "alpha": 0.6},
                whiskerprops={"color": colors[j]},
                medianprops={"color": colors[j]},
                widths=0.35,
                patch_artist=True,
            )

            # If we haven't already added a handle for this dataset's color, add one now.
            # We'll use the box to represent this dataset in the legend.
            if i == 0:
                # Each call to bxp returns lists inside the dictionary
                # For a single boxplot, there's one box element in res["boxes"]
                handles.append(res["boxes"][0])

        print(f"Done iteration {j+1}/{len(arrs)}")

    ax.set_xticks([2 * i + 0.75 for i in range(1, arrs[0].shape[1] + 1)])
    ax.set_xticklabels([i for i in range(1, arrs[0].shape[1] + 1)])

    plt.savefig(
        out_path.joinpath("dem_share_boxplots_VA.png"), dpi=300, bbox_inches="tight"
    )

    plt.close()

    save_legend_png(
        handles=handles,
        filename=out_path.joinpath("dem_share_boxplots_VA_legend.png"),
        labels=[
            "RevReCom 1",
            "RevReCom 2",
            "RevReCom 3",
            "Forest",
        ],
        label_fontsize=16,
        frameon=True,
    )
