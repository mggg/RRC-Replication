#!/usr/env/bin bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

smc_cli_file="$TOP_DIR/cli_files/smc_cli.R"

example_shapefile="$TOP_DIR/example_files/5x5_example/5x5_example.shp"

region_name="precinct"
subregion_name="precinct"
pop_col="TOTPOP"
n_dists=5
n_sims=10000

smc_rng_seed=42

jsonl_output_file="$TOP_DIR/example_files/example_raw_data/SMC_5x5_example_seed_${rng_seeds[i]}_batch_size_${n_sims}.jsonl"

Rscript $smc_cli_file \
    --shapefile $example_shapefile \
    --rng-seed $smc_rng_seed \
    --pop-col $pop_col \
    --pop-tol 0.0001 \
    --n-dists $n_dists \
    --n-sims $n_sims \
    --resample \
    --print | \
    smc_parser --jsonl -o $jsonl_output_file -w && \
    ben -m encode $jsonl_output_file -v && rm -f $jsonl_output_file