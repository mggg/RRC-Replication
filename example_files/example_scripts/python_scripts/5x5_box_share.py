import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from helper_files.box_share_helpers import get_weighted_stats, weighted_quantile

colors = [
    "#0099cd",
    "#ffca5d",
    "#fb8072",
    "#00cd99",
]

if __name__ == "__main__":

    reversible_sample_1 = "../../example_processed_data/RevReCom_5x5_example_seed_42_steps_100000000_tallies.parquet"
    reversible_sample_2 = "../../example_processed_data/RevReCom_5x5_example_seed_496189_steps_100000000_tallies.parquet"
    reversible_sample_3 = "../../example_processed_data/RevReCom_5x5_example_seed_20250123_steps_100000000_tallies.parquet"
    forest_sample = "../../example_processed_data/Forest_5x5_example_seed_42_gamma_0_alpha_1_steps_1000000_tallies.parquet"

    out_folder = "../../example_figures"
    out_path = Path(out_folder)

    # ======================
    # + REV RECOM SAMPLE 1 +
    # ======================
    rev_df1 = pd.read_parquet(reversible_sample_1)
    rev_df2 = pd.read_parquet(reversible_sample_2)
    rev_df3 = pd.read_parquet(reversible_sample_3)
    forest_df = pd.read_parquet(forest_sample)

    rev_df1_dem = rev_df1[rev_df1["sum_columns"] == "dem_votes"].reset_index()
    rev_df1_rep = rev_df1[rev_df1["sum_columns"] == "rep_votes"].reset_index()
    rev_df1_shares_total = rev_df1_dem[[f"district_{i}" for i in range(1, 6)]] / (
        rev_df1_dem[[f"district_{i}" for i in range(1, 6)]]
        + rev_df1_rep[[f"district_{i}" for i in range(1, 6)]]
    )
    rev_df1_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 6)},
        inplace=True,
    )
    rev_df1_shares_total.sort_index(axis=1, inplace=True)
    rev_df1_weights = rev_df1_dem["n_reps"].to_numpy()
    rev_array1 = rev_df1_shares_total.to_numpy()
    rev_array1.sort(axis=1)

    # ======================
    # + REV RECOM SAMPLE 2 +
    # ======================
    rev_df2_dem = rev_df2[rev_df2["sum_columns"] == "dem_votes"].reset_index()
    rev_df2_rep = rev_df2[rev_df2["sum_columns"] == "rep_votes"].reset_index()
    rev_df2_shares_total = rev_df2_dem[[f"district_{i}" for i in range(1, 6)]] / (
        rev_df2_dem[[f"district_{i}" for i in range(1, 6)]]
        + rev_df2_rep[[f"district_{i}" for i in range(1, 6)]]
    )
    rev_df2_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 6)},
        inplace=True,
    )
    rev_df2_shares_total.sort_index(axis=1, inplace=True)
    rev_df2_weights = rev_df2["n_reps"].to_numpy()
    rev_array2 = rev_df2_shares_total.to_numpy()
    rev_array2.sort(axis=1)

    # ======================
    # + REV RECOM SAMPLE 3 +
    # ======================
    rev_df3_dem = rev_df3[rev_df3["sum_columns"] == "dem_votes"].reset_index()
    rev_df3_rep = rev_df3[rev_df3["sum_columns"] == "rep_votes"].reset_index()
    rev_df3_shares_total = rev_df3_dem[[f"district_{i}" for i in range(1, 6)]] / (
        rev_df3_dem[[f"district_{i}" for i in range(1, 6)]]
        + rev_df3_rep[[f"district_{i}" for i in range(1, 6)]]
    )
    rev_df3_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 6)},
        inplace=True,
    )
    rev_df3_shares_total.sort_index(axis=1, inplace=True)
    rev_df3_weights = rev_df3["n_reps"].to_numpy()
    rev_array3 = rev_df3_shares_total.to_numpy()
    rev_array3.sort(axis=1)

    # =======================
    # + FOREST RECOM SAMPLE +
    # =======================
    forest_df_dem = forest_df[forest_df["sum_columns"] == "dem_votes"].reset_index()
    forest_df_rep = forest_df[forest_df["sum_columns"] == "rep_votes"].reset_index()
    forest_df_shares_total = forest_df_dem[[f"district_{i}" for i in range(1, 6)]] / (
        forest_df_dem[[f"district_{i}" for i in range(1, 6)]]
        + forest_df_rep[[f"district_{i}" for i in range(1, 6)]]
    )
    forest_df_shares_total.rename(
        columns={f"district_{i}": f"district_{i:02d}" for i in range(1, 6)},
        inplace=True,
    )
    forest_df_shares_total.sort_index(axis=1, inplace=True)
    forest_df_weights = forest_df["n_reps"].to_numpy()
    forest_array = forest_df_shares_total.to_numpy()
    forest_array.sort(axis=1)

    # ======================
    # + START MAKING PLOTS +
    # ======================
    fig, ax = plt.subplots(figsize=(15, 10))

    arrs = [rev_array1, rev_array2, rev_array3, forest_array]
    weights = [rev_df1_weights, rev_df2_weights, rev_df3_weights, forest_df_weights]

    ax.axhline(y=0.5, color="lightgrey", linestyle="--")

    handles = []

    for j in range(len(arrs)):
        arr = arrs[j]
        for i in range(arr.shape[1]):
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
                boxprops={"color": colors[j]},
                whiskerprops={"color": colors[j]},
                medianprops={"color": colors[j]},
                widths=0.35,
            )

            # If we haven't already added a handle for this dataset's color, add one now.
            # We'll use the box to represent this dataset in the legend.
            if i == 0:
                # Each call to bxp returns lists inside the dictionary
                # For a single boxplot, there's one box element in res["boxes"]
                handles.append(res["boxes"][0])

    ax.set_xticks([2 * i + 0.5 for i in range(1, arrs[0].shape[1] + 1)])
    ax.set_xticklabels([i for i in range(1, arrs[0].shape[1] + 1)])

    ax.legend(
        handles=handles,
        labels=[
            "RRC Seed 42 (100M proposed)", 
            "RRC Seed 496189 (100M proposed)",
            "RRC Seed 20250123 (100M proposed)",
            "Forest Seed 42 (1M proposed)",
        ],
        loc="upper left",
    )

    plt.savefig(out_path.joinpath("dem_share_boxplots_5x5_example.png"), dpi=300)