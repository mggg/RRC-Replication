#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

for file in $(find "$SCRIPT_DIR" -type f -name "*.ben")
do
    sbatch --time=1-00:00:00 --mem=8G --wrap=" \
        ben-tally -g \"$TOP_DIR/JSON_dualgraphs/7x7.json\" -b \"$file\" && \
        output_file=\"\${file/.jsonl.ben/_cut_edges.parquet}\" && \
        mv \"\$output_file\" \"\$(dirname \"$output_file\")/../../hpc_processed_data/7x7/\$(basename \"$output_file\")\""
done