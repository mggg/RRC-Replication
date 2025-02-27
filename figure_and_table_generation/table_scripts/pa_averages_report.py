"""
Last Updated: 11-02-2025
Author: Peter Rock <peter@mggg.org>

This is a small script that is used to account for the average number of Dem
districts in PA across all of the collected samples. These averages are then
printed into a text file report that can be used to generate the corresponding
table in the paper.
"""

import pandas as pd
from glob import glob
from tqdm import tqdm
from pathlib import Path

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
