#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

julia_cli_file="$TOP_DIR/cli_files/multi_cli.jl"

rng_seeds=(42 496189 20250123)

example_json_file="$TOP_DIR/example_files/5x5_example.json"

region_name="precinct"
subregion_name="precinct"
pop_col="TOTPOP"
n_dists=5
n_steps=1000000

for i in {0..2}
do
    final_output_file="$TOP_DIR/example_files/example_raw_data/Forest_5x5_example_seed_${rng_seeds[i]}_gamma_0_alpha_1_steps_${n_steps}.jsonl.ben"
    
    julia $julia_cli_file \
    --input-file-name=$example_json_file \
    --rng-seed="${rng_seeds[i]}" \
    --region-name=$region_name \
    --subregion-name=$subregion_name \
    --pop-name=$pop_col\
    --num-dists=$n_dists \
    --pop-dev=0 \
    --gamma=0 \
    --alpha=1 \
    --steps=$n_steps | \
    msms_parser -g $example_json_file -r $region_name -s $subregion_name | \
    ben -m encode -o $final_output_file -w -v 
done