#!/bin/bash

recom_names=("ReComA" "ReComB" "ReComC" "ReComD")
recom_variants=("cut-edges-rmst" "district-pairs-rmst" "cut-edges-ust" "district-pairs-ust")

current_time=$(date +"%Y%m%d_%H%M%S")

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

# Some sbatch parameters
stime="2-00:00:00"
smem="8G"

pa_json_file="$TOP_DIR/JSON_dualgraphs/PA_VTDs.json"
pa_output_folder="$TOP_DIR/hpc_files/hpc_raw_data/PA"

for i in {0..3}
do 
    soutput="$TOP_DIR/hpc_files/hpc_logs/PA/${recom_names[i]}_%x_%j_${current_time}.out"
    serror="$TOP_DIR/hpc_files/hpc_logs/PA/${recom_names[i]}_%x_%j_${current_time}.log"

    pa_job_name="${recom_names[i]}_PA"
    pa_cores=2
    pa_batch_size=2

    pa_plan_seeds=("2011_PLA_1" "rand_dist_eps0p01")
    pa_random_seeds=(278986 224116 528170 444343 75723)

    pa_pop_col="TOT_POP"
    pa_pop_tol="0.01"
    pa_recom_steps=100000000

    for pa_plan in "${pa_plan_seeds[@]}"
    do
        for pa_rng_seed in "${pa_random_seeds[@]}"
        do
            pa_output_file="${pa_output_folder}/PA_${recom_names[i]}_steps_${pa_recom_steps}_rng_seed_${pa_rng_seed}_plan_${pa_plan}_${current_time}.jsonl.ben"

            sbatch --time=$stime \
                --mem=$smem \
                --job-name=$pa_job_name \
                --output=$soutput \
                --error=$serror \
                --nodes=1 \
                --cpus-per-task=$pa_cores \
                --ntasks-per-node=1 \
                --wrap="frcw \
                    --graph-json $pa_json_file \
                    --assignment-col $pa_plan \
                    --n-steps $pa_recom_steps \
                    --n-threads $pa_cores \
                    --pop-col $pa_pop_col \
                    --rng-seed $pa_rng_seed \
                    --tol $pa_pop_tol \
                    --batch-size $pa_batch_size \
                    --variant ${recom_variants[i]} \
                    --writer ben \
                    --output-file $pa_output_file"
        done
    done
done 

seven_json_file="$TOP_DIR/JSON_dualgraphs/7x7.json"
seven_output_folder="$TOP_DIR/hpc_files/hpc_raw_data/7x7"

for i in {0..3}
do 
    soutput="$TOP_DIR/hpc_files/hpc_logs/7x7/${recom_names[i]}_%x_%j_${current_time}.out"
    serror="$TOP_DIR/hpc_files/hpc_logs/7x7/${recom_names[i]}_%x_%j_${current_time}.log"

    seven_job_name="${recom_names[i]}_7x7"
    seven_cores=2
    seven_batch_size=2

    seven_plan_seeds=("district" "rand_dist")
    seven_random_seeds=(278986)

    seven_pop_col="TOTPOP"
    seven_pop_tol="0.00"

    seven_recom_steps=1000000000

    for seven_plan in "${seven_plan_seeds[@]}"
    do
        for seven_rng_seed in "${seven_random_seeds[@]}"
        do
            seven_output_file="${seven_output_folder}/7x7_${recom_names[i]}_steps_${seven_recom_steps}_rng_seed_${seven_rng_seed}_plan_${seven_plan}_${current_time}.jsonl.ben"

            sbatch --time=$stime \
                --mem=$smem \
                --job-name=$seven_job_name \
                --output=$soutput \
                --error=$serror \
                --nodes=1 \
                --cpus-per-task=$seven_cores \
                --ntasks-per-node=1 \
                --wrap="frcw \
                    --graph-json $seven_json_file \
                    --assignment-col $seven_plan \
                    --n-steps $seven_recom_steps \
                    --n-threads $seven_cores \
                    --pop-col $seven_pop_col \
                    --rng-seed $seven_rng_seed \
                    --tol $seven_pop_tol \
                    --batch-size $seven_batch_size \
                    --variant ${recom_variants[i]} \
                    --writer ben \
                    --output-file $seven_output_file"
        done
    done
done 


fifty_plan_seeds=("50x5_strip" "10x10_square" "50x1_strip")
fifty_n_dists=(10 25 50)
fifty_rng_seed=278986


fifty_cores=2
fifty_batch_size=2

fifty_json_file="$TOP_DIR/JSON_dualgraphs/50x50_with_10_25_50.json"
fifty_output_folder="$TOP_DIR/hpc_files/hpc_raw_data/50x50"

for i in {0..3}
do
for j in {0..2}
do
    soutput="$TOP_DIR/hpc_files/hpc_logs/50x50/${recom_names[i]}_%x_%j_${current_time}.out"
    serror="$TOP_DIR/hpc_files/hpc_logs/50x50/${recom_names[i]}_%x_%j_${current_time}.log"

    fifty_job_name="${recom_names[i]}_50x50_${fifty_n_dists[j]}"

    fifty_pop_col="TOTPOP"
    fifty_pop_tol="0.00"

    fifty_recom_steps=1000000000

    fifty_plan="${fifty_plan_seeds[j]}"

    fifty_output_file="${fifty_output_folder}/50x50_${recom_names[i]}_steps_${fifty_recom_steps}_plan_${fifty_plan}_ndists_${fifty_n_dists[j]}_${current_time}.jsonl.ben"

    sbatch --time=$stime \
        --mem=$smem \
        --job-name=$fifty_job_name \
        --output=$soutput \
        --error=$serror \
        --nodes=1 \
        --cpus-per-task=$fifty_cores \
        --ntasks-per-node=1 \
        --wrap="frcw \
            --graph-json $fifty_json_file \
            --assignment-col $fifty_plan \
            --n-steps $fifty_recom_steps \
            --n-threads $fifty_cores \
            --pop-col $fifty_pop_col \
            --rng-seed $fifty_rng_seed \
            --tol $fifty_pop_tol \
            --batch-size $fifty_batch_size \
            --variant ${recom_variants[i]} \
            --writer ben \
            --output-file $fifty_output_file"

done
done
