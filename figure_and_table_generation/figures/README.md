# Descritions for Images in this Folder


### 50x50_10_dist_forest_rrc_comparison.png

This is a histogram comparing the cut-edge distributions of the Reversible ReCom and Forest ReCom
methods for a 50x50 grid split into 10 districts. The Reversible ensemble contains 10 billion
proposed assignments, while the Forest ensemble contains 10 million proposed assignments.

### 50x50_10_dist_forest_rrc_smc_comparison.png

This is a histogram comparing the cut-edge distributions of the Reversible ReCom, Forest ReCom
and Sequential Monte Carlo (SMC) methods for a 50x50 grid split into 10 districts. The Reversible
ensemble contains 10 billion proposed assignments, the Forest ensemble contains 10 million proposed
assignments, and the SMC ensemble contains 100 thousand proposed assignments.

### 50x50_10_dist_ReCom_comparison.png

This is a histogram comparing the cut-edge distributions of the various ReCom methods
(A, B, C, D) for a 50x50 grid split into 10 districts. All of the ReCom methods are run with
1 billion proposed assignments.

### 50x50_25_dist_forest_rrc_comparison.png

This is a histogram comparing the cut-edge distributions of the Reversible ReCom and Forest ReCom
methods for a 50x50 grid split into 25 districts. The Reversible ensemble contains 10 billion
proposed assignments, while the Forest ensemble contains 10 million proposed assignments.

### 50x50_25_dist_forest_rrc_smc_comparison.png

This is a histogram comparing the cut-edge distributions of the Reversible ReCom, Forest ReCom
and Sequential Monte Carlo (SMC) methods for a 50x50 grid split into 25 districts. The Reversible
ensemble contains 10 billion proposed assignments, the Forest ensemble contains 10 million proposed
assignments, and the SMC ensemble contains 100 thousand proposed assignments.

### 50x50_25_dist_ReCom_comparison.png

This is a histogram comparing the cut-edge distributions of the various ReCom methods
(A, B, C, D) for a 50x50 grid split into 25 districts. All of the ReCom methods are run with
1 billion proposed assignments.

### 50x50_50_dist_forest_rrc_comparison.png

This is a histogram comparing the cut-edge distributions of the Reversible ReCom and Forest ReCom
methods for a 50x50 grid split into 50 districts. The Reversible ensemble contains 10 billion
proposed assignments, while the Forest ensemble contains 10 million proposed assignments.

### 50x50_50_dist_forest_rrc_smc_comparison.png

This is a histogram comparing the cut-edge distributions of the Reversible ReCom, Forest ReCom
and Sequential Monte Carlo (SMC) methods for a 50x50 grid split into 50 districts. The Reversible
ensemble contains 10 billion proposed assignments, the Forest ensemble contains 10 million proposed
assignments, and the SMC ensemble contains 100 thousand proposed assignments.

### 50x50_50_dist_ReCom_comparison.png

This is a histogram comparing the cut-edge distributions of the various ReCom methods
(A, B, C, D) for a 50x50 grid split into 50 districts. All of the ReCom methods are run with
1 billion proposed assignments.

### dem_share_boxplots_VA.png

This is a boxplot comparing three different Reversible ReCom ensembles (each started with a
different seed plan) each containing 5 billion proposed assignments and a Forest ReCom ensemble
containing 10 million proposed assignments. There are 11 box plots along the x-axis where each
box plot represents a different district in VA, and the boxplots were obtained from sorting each
of the proposed assignments by the democratic vote share. So, for a particular assignment, the
district with the smallest democratic vote share has its share count used to construct the 
boxplot at x-tick 1. Thus, given a random partition of VA into districts, the boxplot at x-tick 1 
shows the expected democratic vote share of the district with the smallest democratic vote share
in that assignment. Likewise, the boxplot at x-tick 2 shows the expected democratic vote share of
the district with the second smallest democratic vote share in that assignment, and so on.

### linear_multigrid_dual_graph.png

This is a dual graph for the linear multigrid. The linear multigrid is composed of 6 sections:
a 64x64 grid, a 32x32 grid, a 16x16 grid, a 8x8 grid, a 4x4 grid, and a 2x2 grid. These grids
is connected in a line (hence "linear multigrid") to one or two other grids in the order 
(64x64, 32x32), (32x32, 16x16), (16x16, 8x8), (8x8, 4x4), and (4x4, 2x2). The populations
of each of the nodes in the grid increases by a factor of 4 for each section, so nodes in the
64x64 grid have a population of 1, the nodes in the 32x32 grid have a population of 4, the 
nodes in the 16x16 grid have a population of 16, and so on.

### linear_multigrid_heatbar.png

This is just a heatbar to accompany the 'linear_multigrid_heatmap_all' file.

### linear_multigrid_heatmap_all.png

This is a heatmap showing the number of times an individual geographic unit has been reassigned
over the course the generation of a districting ensemble for partitioning the linear_multigrid
into 6 districts using Markov Chain Monte Carlo methods. There are 6 methods displayed in this 
graph: ReCom-A, ReCom-B, ReCom-C, ReCom-D, Reversible ReCom, and Forest ReCom. Here, we compare 
the normalized frequency with which a node has been reassigned in the first 50k accepted proposals.

### square_multigrid_dual_graph.png

This is a dual graph for the square multigrid. The square multigrid is composed of 4 sections:
a 16x16 grid in the lower-left corner, an 8x8 grid in the upper-left corner, a 4x4 grid in 
the lower-right corner, and a 2x2 grid in the upper-right corner. The populations of
each of the nodes in the grid increases by a factor of 4 for each section, so the nodes
in the 16x16 grid have a population of 1, the nodes in the 8x8 grid have a population of 4,
the nodes in the 4x4 grid have a population of 16, and the nodes in the 2x2 grid have a 
population of 64.

### square_multigrid_heatbar_horizontal.png

This is just a horizontal heatbar to accompany the 'square_multigrid_heatmap_all' file

### square_multigrid_heatbar_vertical.png

This is just a vertical heatbar to accompany the 'square_multigrid_heatmap_all' file

### square_multigrid_heatmap_all.png

This is a heatmap showing the number of times an individual geographic unit has been reassigned
over the course the generation of a districting ensemble for partitioning the square_multigrid
into 4 districts using Markov Chain Monte Carlo methods. There are 6 methods displayed in this 
graph: ReCom-A, ReCom-B, ReCom-C, ReCom-D, Reversible ReCom, and Forest ReCom. Here, we compare 
the normalized frequency with which a node has been reassigned in the first 50k accepted proposals.

### Wasserstein_distances_7x7_compare_reversible_forest.png

This is a graph comparing the trace of the Wasserstein distance between Reversible ReCom
with two different starting plan seeds, Forest ReCom, and the spanning tree distribution
on the 7x7 grid when cut into 7-ominos. The Reversible ReCom seeds are labeled "Seed 1"
and "Seed 2" whereas the spanning tree distribution on the 7x7 is called "Truth".

### Wasserstein_distances_recom_comparison_10000000_n_accepted.png

This is a graph comparing the trace of the Wasserstein distances between several
ReCom methods and the spanning tree distribution on the 7x7 grid when cut into 7-ominos.
We run each of the samples until 10 million accepted plans are found.

### Wasserstein_distances_VA_comparison_Dem_Stares_v_Full_Forest.png

This image is meant to be similar to the 7x7 comparison graph except instead of comparing
against the fully known true spanning tree distribution, we instead compare against
the distribution of Democtratic vote shares on a 10M proposal Forest ReCom ensemble.
That is to say, we allow for the number of points in the Rev ReCom sample to change
and we track the convergence in Wasserstein distance of several Reversible ReCom samples,
each starting from a different seed plan ("CD 16", "CD 12", or "Rand Plan") to the
distribution of Democratic vote shares given by the 10M plan Forest ensemble.