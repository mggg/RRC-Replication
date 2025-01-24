#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

for f in $(find "$TOP_DIR/example_files/example_raw_data" -type f -name "*.ben" )
do
    ben-tally -m changed-assignments -b $f && mv "${f/.jsonl.ben/_changed_assignments.txt}" "$TOP_DIR/example_files/example_processed_data" 
done