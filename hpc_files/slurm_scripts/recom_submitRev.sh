#!/usr/env/bin bash

current_time=$(date +"%Y%m%d_%H%M%S")

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

# Some sbatch parameters
stime="2-08:00:00"
smem="8G"

pa_job_name="Reversible_PA"
pa_cores=8
pa_batch_size=8

pa_plan_seeds=("RANDCDN18" "RND2CDN18")
pa_random_seeds=(278986 224116 528170 444343 75723)

pa_json_file="${TOP_DIR}/JSON_dualgraphs/PA_VTD_20.json"
pa_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/PA"

pa_pop_col="TOTPOP"
pa_pop_tol="0.01"
pa_recom_steps=5000000000


for pa_plan in "${pa_plan_seeds[@]}"
do
    for pa_rng_seed in "${pa_random_seeds[@]}"
    do
        soutput="${TOP_DIR}/hpc_files/hpc_logs/PA/RevReCom_${pa_plan}_${pa_rng_seed}_%x_%j_${current_time}.out"
        serror="${TOP_DIR}/hpc_files/hpc_logs/PA/RevReCom_${pa_plan}_${pa_rng_seed}_%x_%j_${current_time}.log"

        pa_output_file="${pa_output_folder}/PA_RevReCom_steps_${pa_recom_steps}_rng_seed_${pa_rng_seed}_plan_${pa_plan}_${current_time}.jsonl.ben"

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
                --variant reversible \
                --writer ben \
                --balance-ub 30 \
                --output-file $pa_output_file"
    done
done


va_job_name="Reversible_VA"
va_cores=8
va_batch_size=8

va_plan_seeds=("CD_16" "CD_12" "rand_dist_eps0p01")
va_random_seeds=(278986)

va_json_file="${TOP_DIR}/JSON_dualgraphs/VA_precincts.json"
va_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/VA"

va_pop_col="TOTPOP"
va_pop_tol="0.01"
va_recom_steps=15000000000


for va_plan in "${va_plan_seeds[@]}"
do
    for va_rng_seed in "${va_random_seeds[@]}"
    do
        soutput="${TOP_DIR}/hpc_files/hpc_logs/VA/RevReCom_${va_plan}_${va_rng_seed}_%x_%j_${current_time}.out"
        serror="${TOP_DIR}/hpc_files/hpc_logs/VA/RevReCom_${va_plan}_${va_rng_seed}_%x_%j_${current_time}.log"

        va_output_file="${va_output_folder}/VA_RevReCom_steps_${va_recom_steps}_rng_seed_${va_rng_seed}_plan_${va_plan}_${current_time}.jsonl.ben"

        sbatch --time=$stime \
            --mem=$smem \
            --job-name=$va_job_name \
            --output=$soutput \
            --error=$serror \
            --nodes=1 \
            --cpus-per-task=$va_cores \
            --ntasks-per-node=1 \
            --wrap="frcw \
                --graph-json $va_json_file \
                --assignment-col $va_plan \
                --n-steps $va_recom_steps \
                --n-threads $va_cores \
                --pop-col $va_pop_col \
                --rng-seed $va_rng_seed \
                --tol $va_pop_tol \
                --batch-size $va_batch_size \
                --variant reversible \
                --writer ben \
                --balance-ub 30 \
                --output-file $va_output_file"
    done
done

seven_job_name="Reversible_7x7"
seven_cores=4
seven_batch_size=4

seven_plan_seeds=("district" "rand_dist")
seven_random_seeds=(278986)

seven_json_file="${TOP_DIR}/JSON_dualgraphs/7x7.json"
seven_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/7x7"

seven_pop_col="TOTPOP"
seven_pop_tol="0.00"
seven_recom_steps=10000000000

for seven_plan in "${seven_plan_seeds[@]}"
do
    for seven_rng_seed in "${seven_random_seeds[@]}"
    do
        soutput="${TOP_DIR}/hpc_files/hpc_logs/7x7/RevReCom_${seven_plan}_${seven_rng_seed}_%x_%j_${current_time}.out"
        serror="${TOP_DIR}/hpc_files/hpc_logs/7x7/RevReCom_${seven_plan}_${seven_rng_seed}_%x_%j_${current_time}.log"

        seven_output_file="${seven_output_folder}/7x7_RevReCom_steps_${seven_recom_steps}_rng_seed_${seven_rng_seed}_plan_${seven_plan}_${current_time}.jsonl.ben"

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
                --variant reversible \
                --writer ben \
                --balance-ub 30 \
                --output-file $seven_output_file"
    done
done


fifty_job_name="Reversible_50x50"
fifty_cores=4
fifty_batch_size=4

fifty_plan_seeds=("50x5_strip" "10x10_square" "50x1_strip")
fifty_n_dists=(10 25 50)
fifty_rng_seed=278986

fifty_json_file="${TOP_DIR}/JSON_dualgraphs/50x50_with_10_25_50.json"
fifty_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/50x50"

fifty_pop_col="TOTPOP"
fifty_pop_tol="0.00"
fifty_recom_steps=10000000000

for i in {0..2}
do
    soutput="${TOP_DIR}/hpc_files/hpc_logs/50x50/RevReCom_${fifty_n_dists[i]}_${fifty_rng_seed}_%x_%j_${current_time}.out"
    serror="${TOP_DIR}/hpc_files/hpc_logs/50x50/RevReCom_${fifty_n_dists[i]}_${fifty_rng_seed}_%x_%j_${current_time}.log"

    fifty_output_file="${fifty_output_folder}/50x50_RevReCom_steps_${fifty_recom_steps}_plan_${fifty_plan_seeds[i]}_ndists_${fifty_n_dists[j]}_${current_time}.jsonl.ben"


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
            --assignment-col ${fifty_plan_seeds[i]} \
            --n-steps $fifty_recom_steps \
            --n-threads $fifty_cores \
            --pop-col $fifty_pop_col \
            --rng-seed $fifty_rng_seed \
            --tol $fifty_pop_tol \
            --batch-size $fifty_batch_size \
            --variant reversible \
            --writer ben \
            --balance-ub 30 \
            --output-file $fifty_output_file"
done
