"""
Last Updated: 11-11-2025 (Nov 11)
Author: Peter Rock <peter@mggg.org>
"""

import pandas as pd
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from helper_files.legend_saver import save_legend_png, box_handles

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

script_dir = Path(__file__).resolve().parent
top_dir = script_dir.parents[1]

true_dist = [
    (28, 0.02080768776861115),
    (29, 0.07101439523160166),
    (30, 0.14977414247506296),
    (31, 0.1978572011208715),
    (32, 0.20743205775170162),
    (33, 0.1637179746934725),
    (34, 0.10381042970326829),
    (35, 0.05297581005301319),
    (36, 0.022250910144718795),
    (37, 0.007642717446682876),
    (38, 0.002149916875334781),
    (39, 0.00047719046900479204),
    (40, 7.998105439452792e-05),
    (41, 9.032906746485945e-06),
    (42, 5.523055148667346e-07),
]


def make_recom_plot(lower, upper, glob_expr):
    """
    Makes the histograms for the 50x50 cut edge distributions comparing
    ReCom A, B, C, and D.

    Parameters
    ----------
    lower : float
        The lower bound on the x-axis to plot.
    upper : float
        The upper bound on the x-axis to plot.
    glob_expr : str
        The regex passed to glob to find the files to plot.

    Returns
    -------
    None
    """
    out_path = Path(f"{script_dir}/../figures")
    data_path = Path(f"{top_dir}/hpc_files/hpc_processed_data/7x7")

    recom_files = glob(str(data_path.joinpath(glob_expr).resolve()))
    recom_files = [Path(file).resolve() for file in recom_files]
    recom_files.sort()

    all_recom_files = {}

    for file in recom_files:
        lst = file.name.split("_")
        all_recom_files[f"{lst[1]}"] = file

    zorders = [1, 4, 3, 2]
    for i, (n, f) in enumerate(all_recom_files.items()):
        _, ax = plt.subplots(figsize=(25, 10), dpi=500)
        df = pd.read_parquet(f)
        prob_df = df.groupby("cut_edges").sum().reset_index()
        prob_df["prob"] = 100 * (prob_df["n_reps"] / prob_df["n_reps"].sum())

        ax.bar(
            prob_df["cut_edges"],
            prob_df["prob"],
            width=1,
            edgecolor=None,
            color=colors[i + 3],
            alpha=0.5,
            zorder=zorders[i],
        )

        ax.bar(
            [x[0] for x in true_dist],
            [x[1] * prob_df["prob"].sum() for x in true_dist],
            width=1,
            edgecolor=None,
            color="#bbb",
            zorder=0,
        )
        ax.set_xlim(25, 44)
        ax.set_xticks(range(28, 41, 2))
        ax.set_xticklabels([str(i) for i in range(28, 41, 2)], fontsize=16)
        ax.set_yticks([])
        plt.savefig(
            out_path.joinpath(f"7x7_ReCom_comparison_{n}.png"),
            bbox_inches="tight",
        )
        plt.close()

    _, ax = plt.subplots(figsize=(25, 10), dpi=500)
    zorders = [1, 4, 3, 2]
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
            alpha=0.6,
            zorder=zorders[i],
        )

    ax.set_xlim(25, 44)
    ax.set_xticks(range(28, 41, 2))
    ax.set_xticklabels([str(i) for i in range(28, 41, 2)], fontsize=16)
    ax.set_yticks([])
    plt.savefig(
        out_path.joinpath(f"7x7_ReCom_comparison_all.png"),
        bbox_inches="tight",
    )
    plt.close()

    labels = list(
        map(lambda x: str(x).replace("ReCom", "ReCom-"), all_recom_files.keys())
    )
    handles = box_handles(labels, colors[3 : 3 + len(labels)])
    save_legend_png(
        handles,
        out_path.joinpath(f"7x7_ReCom_comparison_legend.png"),
        label_fontsize=16,
        frameon=True,
    )


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]

    make_recom_plot(30, 40, "*_ReCom*")
