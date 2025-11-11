#!/usr/env/bin bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

for f in $(find "$TOP_DIR/other_data_files/raw_data_files" -type f -name "*square*.ben" )
do
    ben-tally -m changed-assignments -b $f --max-accepted 50000 --normalize && mv "${f/.jsonl.ben/_accept_50000_changed_assignments.txt}" "$TOP_DIR/other_data_files/processed_data_files/square_multigrid/" 
done

for f in $(find "$TOP_DIR/other_data_files/raw_data_files" -type f -name "*linear*.ben" )
do
    ben-tally -m changed-assignments -b $f --max-accepted 50000 --normalize && mv "${f/.jsonl.ben/_accept_50000_changed_assignments.txt}" "$TOP_DIR/other_data_files/processed_data_files/linear_multigrid/" 
done