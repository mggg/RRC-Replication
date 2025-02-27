import networkx as nx
import numpy as np
import jsonlines as jl
from tqdm import tqdm
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import splu
import pandas as pd
import click
from multiprocessing import Pool
import os
from functools import partial
from pathlib import Path


def node_set_to_int(node_set):
    return sum(1 << node for node in node_set)


def compute_n_spanning_trees(graph, subgraph_nodes):
    # Each process will have its own cache
    if not hasattr(compute_n_spanning_trees, "cache"):
        compute_n_spanning_trees.cache = {}
    cache = compute_n_spanning_trees.cache

    key = node_set_to_int(subgraph_nodes)
    if key in cache:
        return cache[key]
    else:
        subgraph = graph.subgraph(subgraph_nodes)
        L = nx.laplacian_matrix(subgraph)
        # Remove first row and column to get the minor
        if L.shape[0] > 1:
            L_minor = L[1:, 1:]
            # Compute LU decomposition
            lu = splu(csc_matrix(L_minor))
            diag_U = lu.U.diagonal()
            det_L_minor = np.prod(diag_U)
            num_spanning_trees = int(round(abs(det_L_minor)))
        else:
            # For single-node subgraphs, the number of spanning trees is 1
            num_spanning_trees = 1
        cache[key] = num_spanning_trees
        return num_spanning_trees


def process_line(graph, n_parts, line):
    assignment = np.array(line["assignment"])
    parts = {i: np.where(assignment == i)[0].tolist() for i in range(1, n_parts + 1)}

    # Compute total cuts
    tot_cuts = sum(1 for e1, e2 in graph.edges if assignment[e1] != assignment[e2])

    # Compute total spanning tree count
    tot_subs = 1
    for sub_idxs in parts.values():
        sub_nodes = frozenset(sub_idxs)
        num_trees = compute_n_spanning_trees(graph, sub_nodes)
        tot_subs *= num_trees

    return tot_cuts, tot_subs


@click.command()
@click.argument("file_name", type=str)
@click.argument("grid_size", type=int, nargs=2)
@click.argument("n_parts", type=int, nargs=1)
def main(file_name, grid_size, n_parts):
    total_lines = 0
    with jl.open(file_name) as f:
        total_lines = sum(1 for _ in f)

    def line_generator():
        with jl.open(file_name) as f:
            for line in f:
                yield line

    grid_graph = nx.grid_2d_graph(grid_size[0], grid_size[1])
    grid_graph = nx.convert_node_labels_to_integers(grid_graph)
    line_process_fn = partial(process_line, grid_graph, n_parts)

    # Number of processes to use
    num_processes = os.cpu_count() or 1
    print(f"Counting trees using {num_processes} processes")

    with Pool(processes=num_processes) as pool:
        results = []
        # Use imap_unordered for better performance with tqdm
        for res in tqdm(
            pool.imap_unordered(line_process_fn, line_generator()), total=total_lines
        ):
            results.append(res)

    cut_counts, spanning_counts = zip(*results)

    cuts_df = pd.DataFrame({"cuts": cut_counts, "tree_count": spanning_counts})
    prob_df = cuts_df.groupby("cuts")["tree_count"].sum().reset_index()
    prob_df["n_plans"] = list(cuts_df["cuts"].value_counts().sort_index())
    prob_df["probability"] = 100 * prob_df["tree_count"] / prob_df["tree_count"].sum()
    print(prob_df.to_string(index=False))

    script_dir = Path(__file__).resolve().parent
    top_dir = script_dir.parents[1]

    prob_df.to_csv(
        top_dir.joinpath(
            f"other_data_files/processed_data_files/true_counts_{grid_size[0]}x{grid_size[1]}_{n_parts}.csv"
        ),
        index=False,
    )


if __name__ == "__main__":
    main()
