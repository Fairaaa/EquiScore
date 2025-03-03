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

command=`python Screening.py \
--ngpu 1 \
--test \
--test_path  /data_lmdb/ \
--pred_save_path  /data_lmdb/screening_result.csv \
--save_model /checkpoints/sava_model_LeadOpt.pt`
state=$command