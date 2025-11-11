#!/usr/env/bin bash

# Trap Ctrl-C and kill all background jobs
trap 'echo .; echo "Keyboard interrupt detected. Exiting..."; kill 0; exit 1;' SIGINT

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

echo "Running FRCW"

frcw --graph-json "${TOP_DIR}/JSON_dualgraphs/square_multigrid.json" \
    --n-steps 100000000 \
    --n-threads 10 \
    --pop-col TOTPOP \
    --rng-seed 1000 \
    --tol 0.0 \
    --batch-size 12 \
    --variant reversible \
    --assignment-col assignment \
    --cut-edges-count \
    --balance-ub 40 \
    --writer ben -o "${TOP_DIR}/other_data_files/raw_data_files/square_multigrid/square_rev_100M.jsonl.ben" &

frcw --graph-json "${TOP_DIR}/JSON_dualgraphs/linear_multigrid.json" \
    --n-steps 200000000 \
    --n-threads 10 \
    --pop-col TOTPOP \
    --rng-seed 1000 \
    --tol 0.0 \
    --batch-size 12 \
    --variant reversible \
    --assignment-col assignment \
    --cut-edges-count \
    --balance-ub 40 \
    --writer ben -o "${TOP_DIR}/other_data_files/raw_data_files/linear_multigrid/linear_rev_200M.jsonl.ben" &


vars=("cut-edges-rmst" "district-pairs-rmst" "cut-edges-ust" "district-pairs-ust") 
var_names=("A" "B" "C" "D")

for i in {0..3}
do
    frcw --graph-json "${TOP_DIR}/JSON_dualgraphs/square_multigrid.json" \
        --n-steps 1000000 \
        --n-threads 1 \
        --pop-col TOTPOP \
        --rng-seed 1000 \
        --tol 0.0 \
        --batch-size 1 \
        --variant ${vars[$i]} \
        --assignment-col assignment \
        --writer ben -o "${TOP_DIR}/other_data_files/raw_data_files/square_multigrid/square_${var_names[$i]}_1M.jsonl.ben" &


    frcw --graph-json "${TOP_DIR}/JSON_dualgraphs/linear_multigrid.json" \
        --n-steps 1000000 \
        --n-threads 1 \
        --pop-col TOTPOP \
        --rng-seed 1000 \
        --tol 0.0 \
        --batch-size 1 \
        --variant ${vars[$i]} \
        --assignment-col assignment \
        --writer ben -o "${TOP_DIR}/other_data_files/raw_data_files/linear_multigrid/linear_${var_names[$i]}_1M.jsonl.ben" &
done 

spinner_chars='-\|/'
while [ $(jobs | grep -v "Done" | grep -c "[f]rcw --graph") -gt 0 ]; do
    for ((i=0; i<${#spinner_chars}; i++)); do
        
        if [ $(jobs | grep -v "Done" | grep -c "[f]rcw --graph") -eq 0 ]; then
            break
        fi
        printf "\rRunning FRCW... %s" "${spinner_chars:$i:1}"
        sleep 0.1
    done
done