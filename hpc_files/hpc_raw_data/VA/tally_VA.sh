#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

for file in $(find "$SCRIPT_DIR" -type f -name "*.ben")
do
    sbatch --time 10:00:00 \
        --mem=64G \
        --output=VA_tally_new_%x_%j.out \
        --error=VA_tally_new_%x_%j.log \
        --nodes=1 \
        --cpus-per-task=12 \
        --ntasks-per-node=1 \
        --job-name="VA_tally" \
        --wrap="ben-tally -b '$file' \
        -g \"$TOP_DIR/JSON_dualgraphs/VA_precincts.json\" \
        -m tally-keys \
        -k G16DPRS G16RPRS && \
        output_file=\"\${file/.jsonl.ben/_tallies.parquet}\" && \
        mv \"\$output_file\" \"\$(dirname \"$output_file\")/../../hpc_processed_data/VA/\$(basename \"$output_file\")\""
done