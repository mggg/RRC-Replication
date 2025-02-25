#!/bin/bash

current_time=$(date +"%Y%m%d_%H%M%S")

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

# Some sbatch parameters
stime="3-00:00:00"
smem="96G"
smail_type="ALL"
smail_user="prock01@tufts.edu"


smc_cli_file="/cluster/tufts/mggg/prock01/Reversible_Recom_May_2024/SMC/smc_cli.R"

pa_job_name="SMC_PA"
pa_cores=16

pa_random_seeds=(278986 224116 528170 444343 75723 183080 491349 397747 885844 416713)

pa_shapefile="${TOP_DIR}/shapefiles/shape/PA_VTD_20"
pa_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/PA"

pa_pop_col="TOTPOP"
pa_num_dists=18
pa_num_sims=70000


for pa_rng_seed in "${pa_random_seeds[@]}"
do
    soutput="${TOP_DIR}/hpc_files/hpc_logs/PA/SMC_%x_%j_${current_time}_seed_${pa_rng_seed}.out"
    serror="${TOP_DIR}/hpc_files/hpc_logs/PA/SMC_%x_%j_${current_time}_seed_${pa_rng_seed}.log"

    pa_output_file="${pa_output_folder}/PA_SMC_batch_size_${pa_num_sims}_rng_seed_${pa_rng_seed}_dists_${pa_num_dists}_${current_time}.jsonl"

    sbatch --time=$stime \
        --mem=$smem \
        --job-name=$pa_job_name \
        --output=$soutput \
        --error=$serror \
        --nodes=1 \
        --cpus-per-task=$pa_cores \
        --ntasks-per-node=1 \
        --mail-type=$smail_type \
        --mail-user=$smail_user \
        --wrap="Rscript $smc_cli_file \
            --shapefile $pa_shapefile \
            --rng-seed $pa_rng_seed \
            --pop-col $pa_pop_col \
            --pop-tol 0.01 \
            --n-dists $pa_num_dists \
            --n-sims $pa_num_sims \
            --resample \
            --print | \
            smc_parser --jsonl -o $pa_output_file -w";
done



smem="32G"


fifty_job_name="SMC_50x50"
fifty_cores=16

fifty_random_seed=278986

fifty_shapefile="${TOP_DIR}/shapefiles/50x50_grid"

fifty_pop_col="TOTPOP"
fifty_num_dists=(10 25 50)
fifty_num_sims=100000

for n_dists in "${fifty_num_dists[@]}"
do
    soutput="${TOP_DIR}/hpc_files/hpc_logs/PA/SMC_%x_%j_${current_time}_dists_${n_dists}_seed_${fifty_random_seed}.out"
    serror="${TOP_DIR}/hpc_files/hpc_logs/PA/SMC_%x_%j_${current_time}_dists_${n_dists}_seed_${fifty_random_seed}.log"
    fifty_output_file="${TOP_DIR}/hpc_files/hpc_raw_data/50x50/50x50_batch_size_${fifty_num_sims}_rng_seed_${fifty_random_seed}_dists_${n_dists}_${current_time}.jsonl"

    sbatch --time=$stime \
        --mem=$smem \
        --job-name=$fifty_job_name \
        --output=$soutput \
        --error=$serror \
        --nodes=1 \
        --cpus-per-task=$fifty_cores \
        --ntasks-per-node=1 \
        --mail-type=$smail_type \
        --mail-user=$smail_user \
        --wrap="Rscript $smc_cli_file \
            --shapefile $fifty_shapefile \
            --rng-seed $fifty_random_seed \
            --pop-col $fifty_pop_col \
            --pop-tol 0.0 \
            --n-dists $n_dists \
            --n-sims $fifty_num_sims \
            --resample \
            --print | \
            smc_parser --jsonl -o $fifty_output_file -w";
done