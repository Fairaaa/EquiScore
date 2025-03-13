#!/bin/bash 
# copyright by caoduanhua(caodh@zju.edu.cn)

# source ~/miniconda3/bin/activate equiscore
eval "$(conda shell.bash hook)"
source activate base
conda activate equiscore
conda-unpack

export CUDA_VISIBLE_DEVICES="0,1,2,3"
# for multi screening task ,you can do cycle for this command
cd /run_equiscore
export PYTHONPATH=/run_equiscore
command=$(python -c "import numpy; print(numpy.__version__)")
echo "Current numpy version: $command"
command=$(python -c "import dgl; print(dgl.__version__)")
echo "Current dgl version: $command"

root_folder="/EquiScore"
# model_path=$2


# echo "root folder is $root_folder"
# echo "model path is $model_path"

for dir in "$root_folder"/*/; do
    if [ -d "$dir" ]; then
        echo "Processing $dir"
        command=`python Screening.py \
        --ngpu 1 \
        --test \
        --test_path  "$dir" \
        --test_name tmp_pockets \
        --pred_save_path  "${dir}screening_result.csv" \
        --save_model /checkpoints/save_model_screen.pt`
        state=$command
    fi
done