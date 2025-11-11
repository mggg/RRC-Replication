"""
Last Updated: 10-11-2025 (Nov 10)
Author: Peter Rock <peter@mggg.org>

This script is used to generate the Wasserstein trace plots for the 7x7 grid.
"""

import pandas as pd
from pathlib import Path
from helper_files.wasserstein_trace_tally import (
    wasserstein_trace,
    wasserstein_trace_ground_truth,
)
from helper_files.legend_saver import save_legend_png, marker_handles
import seaborn as sns
import matplotlib.pyplot as plt

colors = [
    # "#0099cd",
    "#8cd1c4",
    "#00cd99",
    # "#ffca5d",
    "#69369c",
    "#99cd00",
    "#cd0099",
    "#9900cd",
    "#8dd3c7",
    "#bebada",
    # "#fb8072",
    "#c92b91",
    "#80b1d3",
]


def make_rev_forest_comparison(
    reversible_sample_1,
    reversible_sample_2,
    forest_sample,
    truth_csv,
    n_accepted,
    n_items,
    n_forest,
    output_folder,
):
    """
    Makes the Wasserstein trace plots for the 7x7 grid comparing
    Reversible ReCom and Forest ReCom to the ground truth cut edge
    distribution on the 7x7 grid.

    Parameters
    ----------
    reversible_sample_1 : str
        The path to the reversible sample 1 ensemble parquet file.
    reversible_sample_2 : str
        The path to the reversible sample 2 ensemble parquet file.
    forest_sample : str
        The path to the forest sample ensemble parquet file.
    truth_csv : str
        The path to the ground truth distribution on cut edges.
    n_accepted: int
        The number of accepted plans to use for the trace plot of the reversible ensemble.
    n_items: int
        The number of items that need to appear on the x-axis of the trace plot.
    n_forest: int
        The number of accepted plans to use for the trace plot of the forest ensemble.
    output_folder: str
        The path to the folder where the output figures should be saved.

    Returns
    -------
    None
    """
    out_path = Path(output_folder)

    df_truth = pd.read_csv(truth_csv)
    df_truth["prob"] = df_truth["probability"] / 100
    df_truth.rename(columns={"cuts": "cut_edges", "tree_count": "n_reps"}, inplace=True)

    rev_df1 = pd.read_parquet(reversible_sample_1)
    rev_df2 = pd.read_parquet(reversible_sample_2)

    forest_df = pd.read_parquet(forest_sample)

    was_compare_ticks, was_distances_compare = wasserstein_trace(
        counts1=rev_df1.iloc[:n_accepted, :]["cut_edges"],
        counts2=rev_df2.iloc[:n_accepted, :]["cut_edges"],
        weights1=rev_df1.iloc[:n_accepted, :]["n_reps"],
        weights2=rev_df2.iloc[:n_accepted, :]["n_reps"],
        resolution=n_accepted / n_items,
    )
    was_rev1_ticks, was_distances_rev1 = wasserstein_trace_ground_truth(
        counts=rev_df1.iloc[:n_accepted, :]["cut_edges"],
        ref_counts=df_truth["cut_edges"],
        weights=rev_df1.iloc[:n_accepted, :]["n_reps"],
        ref_weights=df_truth["n_reps"],
        resolution=n_accepted / n_items,
    )
    was_rev2_ticks, was_distances_rev2 = wasserstein_trace_ground_truth(
        counts=rev_df2.iloc[:n_accepted, :]["cut_edges"],
        ref_counts=df_truth["cut_edges"],
        weights=rev_df2.iloc[:n_accepted, :]["n_reps"],
        ref_weights=df_truth["n_reps"],
        resolution=n_accepted / n_items,
    )

    was_forest_ticks, was_distances_forest = wasserstein_trace_ground_truth(
        counts=forest_df.iloc[:n_forest, :]["cut_edges"],
        ref_counts=df_truth["cut_edges"],
        weights=forest_df.iloc[:n_forest, :]["n_reps"],
        ref_weights=df_truth["n_reps"],
        resolution=n_forest / n_items,
    )

    _, ax = plt.subplots(figsize=(15, 10), dpi=400)

    # Adjust font sizes
    plt.rcParams.update(
        {
            "legend.fontsize": 16,  # Legend font size
        }
    )

    for i in range(4):
        ax.axhline(y=i * 0.1, color="lightgrey", linewidth=1)

    sns.lineplot(
        x=was_compare_ticks,
        y=was_distances_compare,
        ax=ax,
        linewidth=3,
        color=colors[0],
    )
    sns.lineplot(
        x=was_rev1_ticks,
        y=was_distances_rev1,
        ax=ax,
        linewidth=3,
        color=colors[2],
    )
    sns.lineplot(
        x=was_rev2_ticks,
        y=was_distances_rev2,
        ax=ax,
        linewidth=3,
        color=colors[8],
    )
    sns.lineplot(
        x=was_forest_ticks,
        y=was_distances_forest,
        ax=ax,
        linewidth=3,
        color=colors[1],
    )

    plot_tick_step = 500_000
    plot_tick_list = list(range(500_000, 5_000_000, plot_tick_step))
    ax.set_xticks(plot_tick_list)
    ax.set_xticklabels([f"{i/1_000_000:0}M" for i in plot_tick_list])
    ax.set_xlim(0, 4_900_000)
    ax.set_xlabel("accepted", loc="right", fontsize=12)

    plt.savefig(
        out_path.joinpath("Wasserstein_distances_7x7_compare_reversible_forest.png"),
        bbox_inches="tight",
    )

    plt.close()

    labels = [
        "RevReCom1 vs RevReCom2",
        "RevReCom1 vs full",
        "RevReCom2 vs full",
        "Forest vs full",
    ]
    colors_legend = [colors[0], colors[2], colors[8], colors[1]]
    handles = marker_handles(labels=labels, colors=colors_legend, linestyle="-")
    save_legend_png(
        handles=handles,
        filename=out_path.joinpath(
            "Wasserstein_distances_7x7_compare_reversible_forest_legend.png"
        ),
        ncol=1,
        frameon=True,
        dpi=200,
        label_fontsize=14,
    )


def make_recom_comparison(
    recomA_sample,
    recomB_sample,
    recomC_sample,
    recomD_sample,
    truth_csv,
    n_accepted,
    n_items,
    output_folder,
):
    """
    Makes a Wasserstein trace plot comparing various ReCom ensemble generation methods.

    Parameters
    ----------
    recomA_sample : str
        The path to the ReCom-A ensemble parquet file.
    recomB_sample : str
        The path to the ReCom-B ensemble parquet file.
    recomC_sample : str
        The path to the ReCom-C ensemble parquet file.
    recomD_sample : str
        The path to the ReCom-D ensemble parquet file.
    truth_csv : str
        The path to the ground truth distribution on cut edges CSV file.
    n_accepted: int
        The number of accepted plans to use for the trace plot of the reversible ensemble.
    n_items: int
        The number of items that need to appear on the x-axis of the trace plot.
    output_folder: str
        The path to the folder where the output figures should be saved.

    Returns
    -------
    None
    """
    out_path = Path(output_folder)

    df_truth = pd.read_csv(truth_csv)
    df_truth["prob"] = df_truth["probability"] / 100
    df_truth.rename(columns={"cuts": "cut_edges", "tree_count": "n_reps"}, inplace=True)

    recomA_df = pd.read_parquet(recomA_sample)
    recomB_df = pd.read_parquet(recomB_sample)
    recomC_df = pd.read_parquet(recomC_sample)
    recomD_df = pd.read_parquet(recomD_sample)

    was_recomA_ticks, was_distances_recomA = wasserstein_trace_ground_truth(
        counts=recomA_df.iloc[:n_accepted, :]["cut_edges"],
        ref_counts=df_truth["cut_edges"],
        weights=recomA_df.iloc[:n_accepted, :]["n_reps"],
        ref_weights=df_truth["n_reps"],
        resolution=n_accepted / n_items,
    )
    was_recomB_ticks, was_distances_recomB = wasserstein_trace_ground_truth(
        counts=recomB_df.iloc[:n_accepted, :]["cut_edges"],
        ref_counts=df_truth["cut_edges"],
        weights=recomB_df.iloc[:n_accepted, :]["n_reps"],
        ref_weights=df_truth["n_reps"],
        resolution=n_accepted / n_items,
    )
    was_recomC_ticks, was_distances_recomC = wasserstein_trace_ground_truth(
        counts=recomC_df.iloc[:n_accepted, :]["cut_edges"],
        ref_counts=df_truth["cut_edges"],
        weights=recomC_df.iloc[:n_accepted, :]["n_reps"],
        ref_weights=df_truth["n_reps"],
        resolution=n_accepted / n_items,
    )
    was_recomD_ticks, was_distances_recomD = wasserstein_trace_ground_truth(
        counts=recomD_df.iloc[:n_accepted, :]["cut_edges"],
        ref_counts=df_truth["cut_edges"],
        weights=recomD_df.iloc[:n_accepted, :]["n_reps"],
        ref_weights=df_truth["n_reps"],
        resolution=n_accepted / n_items,
    )

    _, ax = plt.subplots(figsize=(15, 10), dpi=400)

    plt.rcParams.update(
        {
            "legend.fontsize": 14,  # Legend font size
        }
    )

    for i in range(17):
        ax.axhline(y=0.1 * i, color="lightgrey", linewidth=2)

    linewidth = 5

    if n_accepted > 4_000_000:
        sns.lineplot(
            x=was_recomA_ticks,
            y=was_distances_recomA,
            ax=ax,
            linewidth=linewidth,
            color=colors[3],
        )
        sns.lineplot(
            x=was_recomB_ticks,
            y=was_distances_recomB,
            ax=ax,
            linewidth=linewidth,
            color=colors[4],
        )
        sns.lineplot(
            x=was_recomC_ticks,
            y=was_distances_recomC,
            ax=ax,
            linewidth=linewidth,
            color=colors[5],
        )
        sns.lineplot(
            x=was_recomD_ticks,
            y=was_distances_recomD,
            ax=ax,
            linewidth=linewidth,
            color=colors[6],
        )
        plot_tick_list = list(range(2_000_000, n_accepted + 1_000_000, 2_000_000))
        ax.set_xticks(plot_tick_list)
        ax.set_xticklabels([f"{i//1_000_000}M" for i in plot_tick_list])
        ax.set_ylim(-0.05, 1.05)
    else:
        sns.lineplot(
            x=was_recomA_ticks,
            y=was_distances_recomA,
            ax=ax,
            linewidth=linewidth,
            color=colors[3],
        )
        sns.lineplot(
            x=was_recomB_ticks,
            y=was_distances_recomB,
            ax=ax,
            linewidth=linewidth,
            color=colors[4],
        )
        sns.lineplot(
            x=was_recomC_ticks,
            y=was_distances_recomC,
            ax=ax,
            linewidth=linewidth,
            color=colors[5],
        )
        sns.lineplot(
            x=was_recomD_ticks,
            y=was_distances_recomD,
            ax=ax,
            linewidth=linewidth,
            color=colors[6],
        )
        plot_tick_list = list(range(10_000, n_accepted, 10_000))
        ax.set_xticks(plot_tick_list)
        ax.set_xticklabels([f"{i//1_000}k" for i in plot_tick_list])

    ax.set_xlim(0, 0.99 * n_accepted)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=24)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    ax.set_xlabel("accepted", loc="right", fontsize=24)

    plt.savefig(
        out_path.joinpath(
            f"Wasserstein_distances_7x7_recom_comparison_{n_accepted}_n_accepted.png"
        ),
        bbox_inches="tight",
    )
    plt.close()

    labels = [
        "ReCom-A vs full",
        "ReCom-B vs full",
        "ReCom-C vs full",
        "ReCom-D vs full",
    ]
    colors_legend = [colors[3], colors[4], colors[5], colors[6]]
    handles = marker_handles(labels=labels, colors=colors_legend, linestyle="-")
    save_legend_png(
        handles=handles,
        filename=out_path.joinpath(
            f"Wasserstein_distances_7x7_recom_comparison_{n_accepted}_n_accepted_legend.png"
        ),
        ncol=1,
        frameon=True,
        dpi=200,
        label_fontsize=14,
    )


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]

    truth_csv = f"{top_dir}/other_data_files/processed_data_files/true_counts_7x7_7.csv"

    reversible_sample_1 = f"{top_dir}/hpc_files/hpc_processed_data/7x7/7x7_RevReCom_steps_10000000000_rng_seed_278986_plan_district_20241024_115741_cut_edges.parquet"

    reversible_sample_2 = f"{top_dir}/hpc_files/hpc_processed_data/7x7/7x7_RevReCom_steps_10000000000_rng_seed_278986_plan_rand_dist_20241024_115741_cut_edges.parquet"

    forest_sample = f"{top_dir}/hpc_files/hpc_processed_data/7x7/7x7_Forest_steps_10000000_rng_seed_278986_gamma_0.0_alpha_1.0_ndists_7_20240830_142334_cut_edges.parquet"

    make_rev_forest_comparison(
        reversible_sample_1=reversible_sample_1,
        reversible_sample_2=reversible_sample_2,
        forest_sample=forest_sample,
        truth_csv=truth_csv,
        n_accepted=5_000_000,
        n_forest=1_500_000,
        n_items=500,
        output_folder=f"{top_dir}/figure_and_table_generation/figures",
    )

    recomA_sample = f"{top_dir}/hpc_files/hpc_processed_data/7x7/7x7_ReComA_steps_1000000000_rng_seed_278986_plan_rand_dist_20241031_122133_cut_edges.parquet"
    recomB_sample = f"{top_dir}/hpc_files/hpc_processed_data/7x7/7x7_ReComB_steps_1000000000_rng_seed_278986_plan_rand_dist_20241031_122133_cut_edges.parquet"
    recomC_sample = f"{top_dir}/hpc_files/hpc_processed_data/7x7/7x7_ReComC_steps_1000000000_rng_seed_278986_plan_rand_dist_20241031_122133_cut_edges.parquet"
    recomD_sample = f"{top_dir}/hpc_files/hpc_processed_data/7x7/7x7_ReComD_steps_1000000000_rng_seed_278986_plan_rand_dist_20241031_122133_cut_edges.parquet"

    make_recom_comparison(
        recomA_sample=recomA_sample,
        recomB_sample=recomB_sample,
        recomC_sample=recomC_sample,
        recomD_sample=recomD_sample,
        truth_csv=truth_csv,
        n_accepted=10_000_000,
        n_items=500,
        output_folder=f"{top_dir}/figure_and_table_generation/figures",
    )
