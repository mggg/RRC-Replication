#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

smc_cli_file="$TOP_DIR/cli_files/smc_cli.R"

example_shape_file="$TOP_DIR/example_files/5x5_example/5x5_example.shp"

region_name="precinct"
subregion_name="precinct"
pop_col="TOTPOP"
n_dists=5
n_sims=10000

smc_rng_seed=42

final_output_file="$TOP_DIR/example_files/example_raw_data/SMC_5x5_example_seed_${rng_seeds[i]}_batch_size_${n_sims}.jsonl.ben"

Rscript $smc_cli_file \
    --shapefile $pa_shapefile \
    --rng-seed $smc_rng_seed \
    --pop-col $pop_col \
    --pop-tol 0.0 \
    --n-dists $n_dists \
    --n-sims $n_sims \
    --resample \
    --print | \
    smc_parser --jsonl -o $pa_output_file -w