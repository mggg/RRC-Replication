#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

for file in $(find "$SCRIPT_DIR" -type f -name "*.ben")
do
    sbatch --time 2-00:00:00 \
        --mem=160G \
        --output=PA_tally_new_%x_%j.out \
        --error=PA_tally_new_%x_%j.log \
        --nodes=1 \
        --cpus-per-task=12 \
        --ntasks-per-node=1 \
        --job-name="PA_tally" \
        --wrap="ben-tally -b '$file' \
        -g '$TOP_DIR/JSON_dualgraphs/PA_VTD_20.json' \
        -m tally-keys \
        -k TOTPOP PRES16D PRES16R SEND16D SEND16R && \
        output_file=\"\${file/.jsonl.ben/_tallies.parquet}\" && \
        mv \"\$output_file\" \"\$(dirname \"$output_file\")/../../hpc_processed_data/PA/\$(basename \"$output_file\")\""
done
