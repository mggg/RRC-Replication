#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

# for f in $(find "$TOP_DIR/other_data_files/raw_data_files" -type f -name "*square*.ben" )
# do
#     ben-tally -m changed-assignments -b $f --max-accepted 50000 && mv "${f/.jsonl.ben/_changed_assignments.txt}" "$TOP_DIR/other_data_files/processed_data_files" 
# done

for f in $(find "$TOP_DIR/other_data_files/raw_data_files" -type f -name "*square*.ben" )
do
    ben-tally -m changed-assignments -b $f && mv "${f/.jsonl.ben/_changed_assignments.txt}" "$TOP_DIR/other_data_files/processed_data_files" 
done