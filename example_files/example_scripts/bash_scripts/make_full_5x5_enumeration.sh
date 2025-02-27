#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

julia "$TOP_DIR/data_processing/other_processing_scripts/gridenum.jl" 5 5 5 5 > "$TOP_DIR/other_data_files/processed_data_files/5x5_to_5_enumeration.jsonl"
python "$TOP_DIR/data_processing/other_processing_scripts/tree_counter.py" "$TOP_DIR/other_data_files/processed_data_files/5x5_to_5_enumeration.jsonl" 5 5 5
rm "$TOP_DIR/other_data_files/processed_data_files/5x5_to_5_enumeration.jsonl"
mv "$TOP_DIR/other_data_files/processed_data_files/true_counts_5x5_5.csv" "$TOP_DIR/example_files"