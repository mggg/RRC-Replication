"""
Last Updated: 29-01-2025
Author: Peter Rock <peter@mggg.org>

This is a small script that is used to account for the average number of Dem
districts in the 5x5 gridacross all of the collected samples. These averages are then
printed into a text file report that can be used to generate the corresponding
table in the paper.
"""

import pandas as pd
from glob import glob
from tqdm import tqdm
from pathlib import Path

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[2]

    out_folder = Path(f"{top_dir}/example_files/example_table_outputs")
    all_files = glob(f"{top_dir}/example_files/example_processed_data/*tallies.parquet")
    all_files = [Path(file).resolve() for file in all_files]

    sample_type_lst = [file.name.split("_")[0] for file in all_files]
    print(sample_type_lst)
    outputs_dict = {key: [] for key in sorted(sample_type_lst)}

    for i in tqdm(range(len(all_files))):
        file = all_files[i]
        sample_type = sample_type_lst[i]
        df = pd.read_parquet(file)
        df_dem = df[df["sum_columns"] == "dem_votes"].reset_index()[
            [f"district_{i}" for i in range(1, 6)]
        ]
        df_rep = df[df["sum_columns"] == "rep_votes"].reset_index()[
            [f"district_{i}" for i in range(1, 6)]
        ]
        df_mean = (df_dem > df_rep).sum(axis=1).mean()
        outputs_dict[sample_type].append((Path(file).name, df_mean))

    with open(out_folder.joinpath("5x5_averages_report.txt"), "w") as f:
        for key, list_tup in outputs_dict.items():
            print("=" * 100, file=f)
            print(str(key).upper().center(100), file=f)
            print("=" * 100, file=f)
            dem_tot = 0
            for name, dem_share in list_tup:
                print(f"\t{name}\n\t\tDem Share: {dem_share}", file=f)
                dem_tot += dem_share

            dem_avg = 0
            if len(list_tup) > 0:
                dem_avg = dem_tot / len(list_tup)
                print("", file=f)
                print(f"Average Dem Share {key}: {dem_avg}", file=f)
                print("", file=f)
