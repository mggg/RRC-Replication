"""
Last Updated: 05-03-2025
Author: Peter Rock <peter@mggg.org>

This is a small script that is used to account for the average number of Dem
districts in PA across all of the collected samples. These averages are then
plotted into a dotplot that is used in the paper to demonstrate the stability
of the various methods output statistics.
"""

import pandas as pd
from glob import glob
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


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


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]

    out_folder = Path(f"{top_dir}/figure_and_table_generation/table_outputs")
    all_files = glob(f"{top_dir}/hpc_files/hpc_processed_data/PA/*.parquet")
    all_files = [Path(file).resolve() for file in all_files]

    sample_type_lst = [file.name.split("_")[1] for file in all_files]
    outputs_dict = {key: [] for key in sorted(sample_type_lst)}

    for i in tqdm(range(len(all_files))):
        file = all_files[i]
        sample_type = sample_type_lst[i]
        df = pd.read_parquet(file)
        df_dem_pres = df[df["sum_columns"] == "PRES16D"].reset_index()[
            [f"district_{i}" for i in range(1, 19)] + ["n_reps"]
        ]
        df_rep_pres = df[df["sum_columns"] == "PRES16R"].reset_index()[
            [f"district_{i}" for i in range(1, 19)] + ["n_reps"]
        ]
        df_dem_sen = df[df["sum_columns"] == "SEND16D"].reset_index()[
            [f"district_{i}" for i in range(1, 19)] + ["n_reps"]
        ]
        df_rep_sen = df[df["sum_columns"] == "SEND16R"].reset_index()[
            [f"district_{i}" for i in range(1, 19)] + ["n_reps"]
        ]

        assert df_dem_pres["n_reps"].equals(df_rep_pres["n_reps"])
        assert df_dem_sen["n_reps"].equals(df_rep_sen["n_reps"])

        pres_mean = (
            (df_dem_pres > df_rep_pres).sum(axis=1) * df_dem_pres["n_reps"]
        ).sum() / df_dem_pres["n_reps"].sum()
        sen_mean = (
            (df_dem_sen > df_rep_sen).sum(axis=1) * df_dem_sen["n_reps"]
        ).sum() / df_dem_sen["n_reps"].sum()
        outputs_dict[sample_type].append((Path(file).name, pres_mean, sen_mean))

    with open(out_folder.joinpath("pa_averages_report.txt"), "w") as f:
        for key, list_tup in outputs_dict.items():
            print("=" * 100, file=f)
            print(str(key).upper().center(100), file=f)
            print("=" * 100, file=f)
            pres_tot = 0
            sen_tot = 0
            list_tup = outputs_dict[key]
            for name, pres, sen in list_tup:
                print(f"\t{name}\n\t\tPres: {pres}\n\t\tSen: {sen}", file=f)
                pres_tot += pres
                sen_tot += sen

            if list_tup:
                pres_avg = pres_tot / len(list_tup)
                sen_avg = sen_tot / len(list_tup)
                print("", file=f)
                print(f"Average Pres {key}: {pres_avg}", file=f)
                print(f"Average Sen {key}: {sen_avg}", file=f)
                print("", file=f)

    y_offsets = {
        "RevReCom": 6,
        "Forest": 5,
        "SMC": 4,
        "ReComA": 3,
        "ReComB": 2,
        "ReComC": 1,
        "ReComD": 0,
    }
    tmp = outputs_dict.copy()
    outputs_dict.clear()
    for k in y_offsets.keys():
        outputs_dict[k] = tmp[k]

    pres_values_dict = {
        k: [float(v[1]) for v in vals] for k, vals in outputs_dict.items()
    }
    sen_values_dict = {
        k: [float(v[2]) for v in vals] for k, vals in outputs_dict.items()
    }

    pres_points = {
        k: [(v, y_offsets[k]) for v in pres_values_dict[k]]
        for k in pres_values_dict.keys()
    }
    sen_points = {
        k: [(v, y_offsets[k]) for v in sen_values_dict[k]]
        for k in sen_values_dict.keys()
    }

    fig, ax = plt.subplots(figsize=(10, 3), dpi=500)

    # Cheeky way of making the legend work
    for i, (k, vlst) in enumerate(pres_points.items()):
        ax.scatter(
            [0 for v in vlst],
            [0 for v in vlst],
            label=k,
            alpha=1.0,
            s=70,
            color=colors[i],
        )

    for i, (k, vlst) in enumerate(pres_points.items()):
        ax.scatter(
            [v[0] for v in vlst],
            [v[1] for v in vlst],
            alpha=0.5,
            s=70,
            color=colors[i],
        )

    for i, (k, vlst) in enumerate(sen_points.items()):
        ax.scatter(
            [v[0] for v in vlst],
            [v[1] for v in vlst],
            alpha=0.5,
            s=70,
            color=colors[i],
        )

    for i in range(4, 10):
        ax.axvline(i, color="grey", linewidth=0.5)

    ax.set_xticks(range(4, 10))
    ax.set_xticklabels([f"{i}" for i in range(4, 10)], fontsize=24)
    ax.set_xlim(3.9, 9.1)
    ax.set_yticks([])
    ax.set_ylim(-1, 7)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), prop={"size": 8})
    plt.savefig(f"{script_dir}/../figures/pa_pres_sen_dotplot.png", bbox_inches="tight")
