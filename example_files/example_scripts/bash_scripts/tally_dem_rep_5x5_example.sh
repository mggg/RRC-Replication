#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

example_json_file="$TOP_DIR/example_files/5x5_example.json"

for f in $(find "$TOP_DIR/example_files/example_raw_data" -type f -name "*.ben" )
do
    ben-tally -m tally-keys -b $f -g $example_json_file -k dem_votes rep_votes && mv "${f/.jsonl.ben/_tallies.parquet}" "$TOP_DIR/example_files/example_processed_data" 
done