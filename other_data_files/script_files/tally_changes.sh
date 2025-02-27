#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

for f in $(find "$TOP_DIR/other_data_files/raw_data_files" -type f -name "*.ben" )
do
    output_file="${f/.jsonl.ben/_accept_50000_changed_assignments.txt}"
    relative_dir="${f#$TOP_DIR/other_data_files/raw_data_files/}"  # Get relative path
    target_dir="$TOP_DIR/other_data_files/processed_data_files/$(dirname "$relative_dir")"

    ben-tally -m changed-assignments -b "$f" --max-accepted 50000 --normalize && \
    mv "$output_file" "$target_dir/"
done
