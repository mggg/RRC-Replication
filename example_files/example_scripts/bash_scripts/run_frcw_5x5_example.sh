#!/bin/bash

# Trap Ctrl-C and kill all background jobs
trap 'echo .; echo "Keyboard interrupt detected. Exiting..."; kill 0; exit 1;' SIGINT


# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../../..")

recom_names=("ReComA" "ReComB" "ReComC" "ReComD")
recom_variants=("cut-edges-rmst" "district-pairs-rmst" "cut-edges-ust" "district-pairs-ust")

rng_seeds=(42 496189 20250123)

example_json_file="$TOP_DIR/example_files/5x5_example.json"

plan_name="assignment"
pop_col="TOTPOP"
n_steps=10000000

for seed in "${rng_seeds[@]}"
do
for i in {0..3}
do
    final_output_file="$TOP_DIR/example_files/example_raw_data/${recom_names[i]}_5x5_example_seed_${seed}_steps_${n_steps}.jsonl.ben"

    rm -f $final_output_file 

    frcw \
        --graph-json $example_json_file \
        --assignment-col $plan_name \
        --n-steps $n_steps \
        --n-threads 1 \
        --pop-col $pop_col \
        --rng-seed $seed \
        --tol 0.0 \
        --batch-size 1 \
        --variant ${recom_variants[i]} \
        --writer ben \
        --output-file $final_output_file &
done
done

n_steps=100000000
for seed in "${rng_seeds[@]}"
do
    final_output_file="$TOP_DIR/example_files/example_raw_data/RevReCom_5x5_example_seed_${seed}_steps_${n_steps}.jsonl.ben"

    rm -f $final_output_file

    frcw \
        --graph-json $example_json_file \
        --assignment-col $plan_name \
        --n-steps $n_steps \
        --n-threads 1 \
        --pop-col $pop_col \
        --rng-seed $seed \
        --tol 0.0 \
        --batch-size 12 \
        --variant reversible \
        --balance-ub 30 \
        --writer ben \
        --output-file $final_output_file &
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