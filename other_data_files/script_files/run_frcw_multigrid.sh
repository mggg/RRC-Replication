#!/bin/bash

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

wait
echo "Done!"