#!/bin/bash

current_time=$(date +"%Y%m%d_%H%M%S")

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP_DIR=$(realpath "$SCRIPT_DIR/../..")

# Some sbatch parameters
stime="3-00:00:00"
smem="128G"

julia_cli_file="${TOP_DIR}/cli_files/multi_cli.jl"


alpha=1.0

pa_job_name="Forest_PA"
pa_cores=32

pa_random_seeds=(278986 224116 528170 444343 75723 183080 491349 397747 885844 416713)

pa_json_file="${TOP_DIR}/JSON_dualgraphs/PA_VTD_20.json"
pa_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/PA"

pa_region="GEOID10"
pa_subregion="GEOID10"

pa_pop_col="TOT_POP"
pa_num_dists=18
pa_pop_dev=0.01
pa_gamma=0.0

pa_recom_steps=4000000

for pa_rng_seed in "${pa_random_seeds[@]}"
do
    soutput="${TOP_DIR}/hpc_files/hpc_logs/PA/Forest_%x_%j_${current_time}_seed_${pa_rng_seed}.out"
    serror="${TOP_DIR}/hpc_files/hpc_logs/PA/Forest_%x_%j_${current_time}_seed_${pa_rng_seed}.log"

    pa_output_file="${pa_output_folder}/PA_Forest_steps_${pa_recom_steps}_rng_seed_${pa_rng_seed}_gamma_${pa_gamma}_alpha_${alpha}_ndists_${pa_num_dists}_${current_time}.jsonl.ben"

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
        --wrap="julia $julia_cli_file \
            --input-file-name=$pa_json_file \
            --rng-seed=$pa_rng_seed \
            --region-name=$pa_region \
            --subregion-name=$pa_subregion \
            --pop-name=$pa_pop_col \
            --num-dists=$pa_num_dists \
            --pop-dev=$pa_pop_dev \
            --gamma=$pa_gamma \
            --alpha=$alpha \
            --steps=$pa_recom_steps | \
            msms_parser -g $pa_json_file -r $pa_region -s $pa_subregion | \
            ben -m encode -o $pa_output_file"
done


stime="4-08:00:00"
smem="64G"

va_job_name="Forest_VA"
va_cores=8

va_random_seeds=(278986)

va_json_file="${TOP_DIR}/JSON_dualgraphs/VA_precincts.json"
va_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/VA"

va_region="loc_prec"
va_subregion="loc_prec"


va_pop_col="TOTPOP"
va_num_dists=11
va_pop_dev=0.01
va_gamma=0.0

va_recom_steps=10000000

for va_rng_seed in "${va_random_seeds[@]}"
do
    soutput="${TOP_DIR}/hpc_files/hpc_logs/VA/Forest_%x_%j_${current_time}_seed_${va_rng_seed}.out"
    serror="${TOP_DIR}/hpc_files/hpc_logs/VA/Forest_%x_%j_${current_time}_seed_${va_rng_seed}.log"

    va_output_file="${va_output_folder}/VA_Forest_steps_${va_recom_steps}_rng_seed_${va_rng_seed}_gamma_${va_gamma}_alpha_${alpha}_ndists_${va_num_dists}_${current_time}.jsonl"

    sbatch --time=$stime \
        --mem=$smem \
        --job-name=$va_job_name \
        --output=$soutput \
        --error=$serror \
        --nodes=1 \
        --cpus-per-task=$va_cores \
        --ntasks-per-node=1 \
        --wrap="julia $julia_cli_file \
            --input-file-name=$va_json_file \
            --rng-seed=$va_rng_seed \
            --region-name=$va_region \
            --subregion-name=$va_subregion \
            --pop-name=$va_pop_col \
            --num-dists=$va_num_dists \
            --pop-dev=$va_pop_dev \
            --gamma=$va_gamma \
            --alpha=$alpha \
            --steps=$va_recom_steps | \
            msms_parser -g $va_json_file -r $va_region -s $va_subregion -o $va_output_file -w && \
            ben -m encode $va_output_file && \
            rm $va_output_file;"
done





stime="1-08:00:00"
smem="8G"


seven_job_name="Forest_7x7"
seven_cores=2

seven_random_seeds=(278986)

seven_json_file="${TOP_DIR}/JSON_dualgraphs/7x7.json"
seven_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/7x7"

seven_region="precinct"
seven_subregion="precinct"

seven_pop_col="TOTPOP"
seven_num_dists=7
seven_pop_dev=0.0
seven_gamma=0.0

seven_recom_steps=10000000

for seven_rng_seed in "${seven_random_seeds[@]}"
do
    soutput="${TOP_DIR}/hpc_files/hpc_logs/7x7/Forest_%x_%j_${current_time}_seed_${seven_rng_seed}.out"
    serror="${TOP_DIR}/hpc_files/hpc_logs/7x7/Forest_%x_%j_${current_time}_seed_${seven_rng_seed}.log"

    seven_output_file="${seven_output_folder}/7x7_Forest_steps_${seven_recom_steps}_rng_seed_${seven_rng_seed}_gamma_${seven_gamma}_alpha_${alpha}_ndists_${seven_num_dists}_${current_time}.jsonl.ben"

    sbatch --time=$stime \
        --mem=$smem \
        --job-name=$seven_job_name \
        --output=$soutput \
        --error=$serror \
        --nodes=1 \
        --cpus-per-task=$seven_cores \
        --ntasks-per-node=1 \
        --wrap="julia $julia_cli_file \
            --input-file-name=$seven_json_file \
            --rng-seed=$seven_rng_seed \
            --region-name=$seven_region \
            --subregion-name=$seven_subregion \
            --pop-name=$seven_pop_col \
            --num-dists=$seven_num_dists \
            --pop-dev=$seven_pop_dev \
            --gamma=$seven_gamma \
            --alpha=$alpha \
            --steps=$seven_recom_steps | \
            msms_parser -g $seven_json_file -r $seven_region -s $seven_subregion | \
            ben -m encode -o $seven_output_file"
done



stime="1-08:00:00"
smem="16G"


fifty_job_name="Forest_50x50"
fifty_cores=4

fifty_rng_seed=278986

fifty_json_file="${TOP_DIR}/JSON_dualgraphs/50x50_with_10_25_50.json"
fifty_output_folder="${TOP_DIR}/hpc_files/hpc_raw_data/50x50"

fifty_region="precinct"
fifty_subregion="precinct"

fifty_pop_col="TOTPOP"
fifty_num_dists=(10 25 50)
fifty_pop_dev=0.0
fifty_gamma=0.0

fifty_recom_steps=10000000

for n_dists in "${fifty_num_dists[@]}"
do
    soutput="${TOP_DIR}/hpc_files/hpc_logs/50x50/Forest_%x_%j_${current_time}_seed_${fifty_rng_seed}.out"
    serror="${TOP_DIR}/hpc_files/hpc_logs/50x50/Forest_%x_%j_${current_time}_seed_${fifty_rng_seed}.log"
    
    fifty_output_file="${fifty_output_folder}/50x50_Forest_steps_${fifty_recom_steps}_rng_seed_${fifty_rng_seed}_gamma_${fifty_gamma}_alpha_${alpha}_ndists_${n_dists}_${current_time}.jsonl"

    sbatch --time=$stime \
        --mem=$smem \
        --job-name=$fifty_job_name \
        --output=$soutput \
        --error=$serror \
        --nodes=1 \
        --cpus-per-task=$fifty_cores \
        --ntasks-per-node=1 \
        --wrap="julia $julia_cli_file \
            --input-file-name=$fifty_json_file \
            --rng-seed=$fifty_rng_seed \
            --region-name=$fifty_region \
            --subregion-name=$fifty_subregion \
            --pop-name=$fifty_pop_col \
            --num-dists=$n_dists \
            --pop-dev=$fifty_pop_dev \
            --gamma=$fifty_gamma \
            --alpha=$alpha \
            --steps=$fifty_recom_steps | \
            msms_parser -g $fifty_json_file -r $fifty_region -s $fifty_subregion -o $fifty_output_file -w;
            ben -m encode $fifty_output_file;
            rm $fifty_output_file;"
done