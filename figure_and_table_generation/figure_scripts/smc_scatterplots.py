"""Wasserstein trace plots for RevReCom paper (7x7 grid cut edges)."""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


smc_color = "#FDD06D"


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]
    output_dir = f"{top_dir}/figure_and_table_generation/figures"

    short_data = pd.read_csv(
        f"{top_dir}/other_data_files/processed_data_files/7x7/7x7_wasserstein_50_to_5000_data.csv"
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    short_data.plot.scatter(
        x="batch_size",
        y="wasserstein_distance",
        ax=ax,
        color=smc_color,
        linewidth=2,
    )

    for i in range(11):
        ax.hlines(
            y=i * 0.1,
            xmin=-50,
            xmax=5050,
            colors="lightgray",
            linewidth=1,
            zorder=0,
        )

    ax.set_xlim(-50, 5050)
    ax.set_ylim(0, 1.0)

    ax.set_xticks(
        [0, 1000, 2000, 3000, 4000, 5000],
        labels=["0", "1000", "2000", "3000", "4000", "5000"],
    )
    ax.set_yticks(
        [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        labels=["", "", "0.2", "", "0.4", "", "0.6", "", "0.8", "", ""],
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.margins(0)
    plt.savefig(
        f"{output_dir}/7x7_wasserstein_scatter_plot_50_to_5000.png",
        bbox_inches="tight",
        dpi=300,
    )
    plt.close(fig)

    large_data = pd.read_csv(
        f"{top_dir}/other_data_files/processed_data_files/7x7/7x7_wasserstein_5k_to_100k_data.csv"
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    large_data.plot.scatter(
        x="batch_size",
        y="wasserstein_distance",
        ax=ax,
        color=smc_color,
        linewidth=2,
    )

    ax.hlines(
        y=0.1,
        xmin=-0,
        xmax=105000,
        colors="lightgray",
        linewidth=1,
        zorder=0,
    )

    ax.set_xlim(0, 105000)
    ax.set_ylim(0, 0.2)

    ax.set_xticks(
        [20000, 40000, 60000, 80000, 100000],
        labels=["20K", "40K", "60K", "80K", "100K"],
    )
    ax.set_yticks(
        [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2],
        labels=["", "", "", "", "0.1", "", "", "", "0.2"],
    )

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.margins(0)

    plt.savefig(
        f"{output_dir}/7x7_wasserstein_scatter_plot_5k_to_100k.png",
        bbox_inches="tight",
        dpi=300,
    )
    plt.close(fig)
