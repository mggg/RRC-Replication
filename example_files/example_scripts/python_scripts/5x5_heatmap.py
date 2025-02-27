import matplotlib.pyplot as plt
from matplotlib import colormaps as cm
import matplotlib.colors as colors
import matplotlib
import ast
from glob import glob
import geopandas as gpd
from pathlib import Path
from gerrychain import Graph
import networkx as nx
from matplotlib import font_manager


def make_heatmap(gdf, file_list, file_to_title_dict, output_folder):
    """
    Generates a heatmap for the square multigrid.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The geodataframe containing the square multigrid.
    file_list : list
        The list of files containing the reassignments for each step.
    file_to_title_dict : dict
        A dictionary mapping the file names to their labels on the figure.
    output_folder : str
        The path to the folder where the output figure should be saved.

    Returns
    -------
    None
    """
    fig, ax = plt.subplots(2, 3, figsize=(18, 12), dpi=400)

    outpath = Path(output_folder)

    max_val = 0
    min_val = float("inf")
    for i, file in enumerate(file_list):
        with open(file, "r") as f:
            sq_data = f.readline()
            sq_data = ast.literal_eval(sq_data)
            max_val = max(max_val, max(sq_data))
            min_val = min(min_val, min(sq_data))

    for i, f_name in enumerate(file_to_title_dict.keys()):
        file = None
        for f in file_list:
            if f_name in f:
                file = f
                break
        with open(file, "r") as f:
            sq_data = f.readline()
            sq_data = ast.literal_eval(sq_data)

        gdf["reassign"] = sq_data

        col_pos = i % 3
        row_pos = i // 3

        gdf.plot(
            ax=ax[row_pos, col_pos],
            column="reassign",
            cmap="viridis",
            vmin=min_val,
            vmax=max_val,
        )
        ax[row_pos, col_pos].set_xticks([])
        ax[row_pos, col_pos].set_yticks([])
        ax[row_pos, col_pos].spines["top"].set_visible(False)
        ax[row_pos, col_pos].spines["right"].set_visible(False)
        ax[row_pos, col_pos].spines["bottom"].set_visible(False)
        ax[row_pos, col_pos].spines["left"].set_visible(False)
        file_name = file.split("/")[-1].split(".")[0]
        if row_pos > 0:
            ax[row_pos, col_pos].set_title(
                file_to_title_dict[file_name], y=-0.03, size=20, weight="bold"
            )
        else:
            ax[row_pos, col_pos].set_title(
                file_to_title_dict[file_name], y=0.97, size=20, weight="bold"
            )

    cax = fig.add_axes([1.01, 0.1, 0.02, 0.8])  # [left, bottom, width, height]
    sm = plt.cm.ScalarMappable(
        cmap="viridis", norm=plt.Normalize(vmin=min_val, vmax=max_val)
    )
    cbar = fig.colorbar(sm, cax=cax, orientation="vertical")

    font_properties = font_manager.FontProperties(weight="bold", size=16)
    for label in cbar.ax.get_yticklabels():
        label.set_fontproperties(font_properties)

    plt.savefig(outpath.joinpath("5x5_heatmap_all.png"), bbox_inches="tight")


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[2]

    file_list = sorted(
        glob(
            f"{top_dir}/example_files/example_processed_data/*seed_42*changed_assignments.txt",
        )
    )

    gdf = gpd.read_file(f"{top_dir}/example_files/5x5_example")

    base_file_names = [file.split("/")[-1].split(".")[0] for file in file_list]

    flie_to_title = {
        "ReComA_5x5_example_seed_42_steps_10000000_accept_50000_changed_assignments": "ReCom-A",
        "ReComB_5x5_example_seed_42_steps_10000000_accept_50000_changed_assignments": "ReCom-B",
        "RevReCom_5x5_example_seed_42_steps_100000000_accept_50000_changed_assignments": "RevReCom",
        "ReComC_5x5_example_seed_42_steps_10000000_accept_50000_changed_assignments": "ReCom-C",
        "ReComD_5x5_example_seed_42_steps_10000000_accept_50000_changed_assignments": "ReCom-D",
        "Forest_5x5_example_seed_42_gamma_0_alpha_1_steps_1000000_accept_50000_changed_assignments": "Forest ReCom",
    }

    make_heatmap(
        gdf=gdf,
        file_list=file_list,
        file_to_title_dict=flie_to_title,
        output_folder=f"{top_dir}/example_files/example_figures",
    )
