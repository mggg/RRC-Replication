"""
Last Updated: 16-01-2025
Author: Peter Rock <peter@mggg.org>

This script is used to generate the multigrid heatmaps for the square and linear
multigrids.
"""

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


def make_square_multigrid_heatmap(
    square_gdf, file_list, file_to_title_dict, output_folder
):
    """
    Generates a heatmap for the square multigrid.

    Parameters
    ----------
    square_gdf : geopandas.GeoDataFrame
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
    _, ax = plt.subplots(2, 3, figsize=(18, 12))

    outpath = Path(output_folder)

    for i, file in enumerate(file_list):
        with open(file, "r") as f:
            sq_data = f.readline()
            sq_data = ast.literal_eval(sq_data)

        square_gdf["reassign"] = sq_data

        col_pos = i % 3
        row_pos = i // 3

        square_gdf.plot(
            ax=ax[row_pos, col_pos],
            column="reassign",
            cmap="viridis",
            vmin=0.0,
            vmax=0.5,
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

    plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)
    plt.savefig(
        outpath.joinpath("square_multigrid_heatmap_all.png"), bbox_inches="tight"
    )


def make_square_multigrid(JSON_file, output_folder):
    """
    Makes the square multigrid dual graph graphic.

    Parameters
    ----------
    JSON_file : str
        The path to the JSON file containing the square multigrid dual graph.
    output_folder : str
        The path to the folder where the output figure should be saved.

    Returns
    -------
    None
    """
    square_multigrid = Graph.from_json(JSON_file)

    out_path = Path(output_folder)

    pos = {n: (d["x"], d["y"]) for n, d in square_multigrid.nodes(data=True)}
    sizes = [20 * d["TOTPOP"] for _, d in square_multigrid.nodes(data=True)]

    _, ax = plt.subplots(figsize=(8, 8))
    nx.draw(
        square_multigrid,
        pos,
        ax=ax,
        node_color="black",
        node_size=sizes,
        with_labels=False,
    )
    plt.savefig(
        out_path.joinpath("square_multigrid_dual_graph.png"), bbox_inches="tight"
    )


def make_linear_multigrid_heatmap(
    linear_gdf, file_list, file_to_title_dict, output_folder
):
    """
    Generates a heatmap for the linear multigrid.

    Parameters
    ----------
    linear_gdf : geopandas.GeoDataFrame
        The geodataframe containing the linear multigrid.
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
    _, ax = plt.subplots(3, 2, figsize=(33, 9))

    outpath = Path(output_folder)

    for i, file in enumerate(file_list):
        with open(file, "r") as f:
            lin_data = f.readline()
            lin_data = ast.literal_eval(lin_data)

        linear_gdf["reassign"] = lin_data

        col_pos = i % 2
        row_pos = i // 2

        linear_gdf.plot(
            ax=ax[row_pos, col_pos],
            column="reassign",
            cmap="viridis",
            vmin=0.0,
            vmax=0.5,
        )
        ax[row_pos, col_pos].set_xticks([])
        ax[row_pos, col_pos].set_yticks([])
        ax[row_pos, col_pos].spines["top"].set_visible(False)
        ax[row_pos, col_pos].spines["right"].set_visible(False)
        ax[row_pos, col_pos].spines["bottom"].set_visible(False)
        ax[row_pos, col_pos].spines["left"].set_visible(False)
        file_name = file.split("/")[-1].split(".")[0]
        if col_pos == 0:
            ax[row_pos, col_pos].text(
                0.03,
                0.5,
                file_to_title_dict[file_name],
                transform=ax[row_pos, col_pos].transAxes,
                rotation=90,
                ha="center",
                va="center",
                weight="bold",
                fontsize=20,
            )

        else:
            ax[row_pos, col_pos].text(
                0.97,
                0.5,
                file_to_title_dict[file_name],
                transform=ax[row_pos, col_pos].transAxes,
                rotation=270,
                ha="center",
                va="center",
                weight="bold",
                fontsize=20,
            )

    plt.tight_layout(w_pad=0)
    plt.savefig(
        outpath.joinpath("linear_multigrid_heatmap_all.png"), bbox_inches="tight"
    )


def make_linear_multigrid(JSON_file, output_folder):
    """
    Makes the linear multigrid dual graph graphic.

    Parameters
    ----------
    JSON_file : str
        The path to the JSON file containing the linear multigrid dual graph.
    output_folder : str
        The path to the folder where the output figure should be saved.

    Returns
    -------
    None
    """
    linear_multigrid = Graph.from_json(JSON_file)

    out_path = Path(output_folder)

    pos = {n: (d["x"], d["y"]) for n, d in linear_multigrid.nodes(data=True)}
    sizes = [10 * d["TOTPOP"] for _, d in linear_multigrid.nodes(data=True)]

    _, ax = plt.subplots(figsize=(60, 10))
    nx.draw(
        linear_multigrid,
        pos,
        ax=ax,
        node_color="black",
        node_size=sizes,
        with_labels=False,
    )
    plt.savefig(
        out_path.joinpath("linear_multigrid_dual_graph.png"), bbox_inches="tight"
    )


if __name__ == "__main__":
    # ===================================
    # == MAKE SQUARE MULTIGRID FIGURES ==
    # ===================================
    file_list = sorted(
        glob(
            "../../hpc_files/hpc_processed_data/square_multigrid/square*changed_assignments.txt"
        )
    )
    new_file_list = [None] * 6

    square_gdf = gpd.read_file("../../shapefiles/square_multigrid/square_multigrid.shp")

    new_order = [0, 1, 5, 2, 3, 4]
    for i in range(6):
        new_file_list[i] = file_list[new_order[i]]
    file_list = new_file_list

    base_file_names = [file.split("/")[-1].split(".")[0] for file in file_list]

    flie_to_title = {
        "square_A_10M_changed_assignments": "ReCom-A",
        "square_B_10M_changed_assignments": "ReCom-B",
        "square_C_10M_changed_assignments": "ReCom-C",
        "square_D_10M_changed_assignments": "ReCom-D",
        "square_rev_1B_changed_assignments": "RevReCom",
        "square_forest_1M_changed_assignments": "Forest ReCom",
    }

    make_square_multigrid_heatmap(
        square_gdf=square_gdf,
        file_list=file_list,
        file_to_title_dict=flie_to_title,
        output_folder="../figures",
    )

    make_square_multigrid(
        JSON_file="../../JSON_dualgraphs/square_multigrid.json",
        output_folder="../figures",
    )

    # ===================================
    # == MAKE LINEAR MULTIGRID FIGURES ==
    # ===================================

    file_list = sorted(
        glob(
            "../../hpc_files/hpc_processed_data/linear_multigrid/linear*changed_assignments.txt"
        )
    )
    new_file_list = [None] * 6

    linear_gdf = gpd.read_file("../../shapefiles/linear_multigrid/linear_multigrid.shp")

    for i, file in enumerate(file_list):
        print(i, file)

    new_order = [0, 1, 2, 3, 5, 4]
    for i in range(6):
        new_file_list[i] = file_list[new_order[i]]
    file_list = new_file_list

    base_file_names = [file.split("/")[-1].split(".")[0] for file in file_list]

    flie_to_title = {
        "linear_A_10M_changed_assignments": "ReCom-A",
        "linear_B_10M_changed_assignments": "ReCom-B",
        "linear_C_10M_changed_assignments": "ReCom-C",
        "linear_D_10M_changed_assignments": "ReCom-D",
        "linear_rev_1B_changed_assignments": "RevReCom",
        "linear_forest_1M_changed_assignments": "Forest ReCom",
    }

    make_linear_multigrid_heatmap(
        linear_gdf=linear_gdf,
        file_list=file_list,
        file_to_title_dict=flie_to_title,
        output_folder="../figures",
    )

    make_linear_multigrid(
        JSON_file="../../JSON_dualgraphs/linear_multigrid.json",
        output_folder="../figures",
    )

    # ===================
    # == MAKE COLORBAR ==
    # ===================

    norm = colors.Normalize(vmin=0.0, vmax=0.5)
    cmap = cm.get_cmap("viridis")

    sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    fig, cax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    cbar = fig.colorbar(sm, cax=cax, orientation="horizontal")
    cbar.ax.xaxis.set_ticks_position("top")
    cbar.ax.xaxis.set_label_position("top")
    cbar.ax.invert_xaxis()

    plt.savefig("../figures/multigrid_heatbar.png", bbox_inches="tight")
