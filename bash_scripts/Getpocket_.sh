#!/bin/bash 
# copyright by caoduanhua(caodh@zju.edu.cn)

# source ~/miniconda3/bin/activate equiscore
eval "$(conda shell.bash hook)"
source activate base
conda activate equiscore
conda-unpack
# export TORCH_DISTRIBUTED_DEBUG=INFO

export CUDA_VISIBLE_DEVICES="0,1,2,3"
# for multi screening task ,you can do cycle for this command
cd /run_equiscore
export PYTHONPATH=/run_equiscore

root_folder="/EquiScore"

# echo "root folder is $root_folder"

for dir in "$root_folder"/*/; do
    if [ -d "$dir" ]; then
        command=`python get_pocket/get_pocket.py \
        --single_sdf_save_path "${dir}tmp_sdfs" \
        --recptor_pdb "${dir}protein.pdb" \
        --docking_result "${dir}compounds.sdf" \
        --pocket_save_dir "${dir}tmp_pockets" \
        --process_num 10`
        state=$command
    fi
done

# rm tmp files
# rm -rf ./*.pdb
