#!/usr/env/bin bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

# This makes the 5x5 -> 5 omino ensemble. The 7x7 takes a while. So this
# is left in for testing purposes.
echo "Running 5x5 to 5 enumeration"
julia "$TOP_DIR/data_processing/other_processing_scripts/gridenum.jl" 5 5 5 5 > "$TOP_DIR/other_data_files/processed_data_files/5x5_to_5_enumeration.jsonl"
python "$TOP_DIR/data_processing/other_processing_scripts/tree_counter.py" "$TOP_DIR/other_data_files/processed_data_files/5x5_to_5_enumeration.jsonl" 5 5 5
rm "$TOP_DIR/other_data_files/processed_data_files/5x5_to_5_enumeration.jsonl"

# echo "Running 7x7 to 7 enumeration"
# julia "$TOP_DIR/data_processing/other_processing_scripts/gridenum.jl" 7 7 7 7 > "$TOP_DIR/other_data_files/processed_data_files/7x7_to_7_enumeration.jsonl"
# python "$TOP_DIR/data_processing/other_processing_scripts/tree_counter.py" "$TOP_DIR/other_data_files/processed_data_files/7x7_to_7_enumeration.jsonl" 7 7 7
# rm "$TOP_DIR/other_data_files/processed_data_files/7x7_to_7_enumeration.jsonl"